from module.base.button import Button, ButtonGrid
from module.base.timer import Timer
from module.logger import logger
from module.meowfficer.assets import *
from module.meowfficer.base import MeowfficerBase

MEOWFFICER_TALENT_GRID_1 = ButtonGrid(
    origin=(875, 559), delta=(105, 0), button_shape=(16, 16), grid_shape=(3, 1),
    name='MEOWFFICER_TALENT_GRID_1')
MEOWFFICER_TALENT_GRID_2 = MEOWFFICER_TALENT_GRID_1.move(vector=(-40, -20),
                                                       name='MEOWFFICER_TALENT_GRID_2')
MEOWFFICER_SHIFT_DETECT = Button(
    area=(1260, 669, 1280, 720), color=(117, 106, 84), button=(1260, 669, 1280, 720),
    name='MEOWFFICER_SHIFT_DETECT')


class MeowfficerCollect(MeowfficerBase):
    def _meow_detect_shift(self, skip_first_screenshot=True):
        """
        Serves as innate wait mechanism for loading
        of meowfficer acquisition complete screen
        During which screen may shift left randomly

        Args:
            skip_first_screenshot (bool):

        Returns:
            bool
        """
        flag = False
        confirm_timer = Timer(3, count=6).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            # End - Random left shift
            if self.image_color_count(MEOWFFICER_SHIFT_DETECT,
                                      color=MEOWFFICER_SHIFT_DETECT.color, threshold=221, count=650):
                if not flag:
                    confirm_timer.reset()
                    flag = True
                if confirm_timer.reached():
                    break
                continue

            # End - No shift at all
            if self.appear(MEOWFFICER_GET_CHECK, offset=(40, 40)):
                if flag:
                    confirm_timer.reset()
                    flag = False
                if confirm_timer.reached():
                    break
        return flag

    def _meow_is_talented(self):
        """
        Examine meowfficer for special talented abilities
        i.e. no tiers or is rainbow colored

        Returns:
            bool
        """
        # Wait for complete load before examining talents
        logger.info('Configured to retain this type of meowfficer, '
                    'wait complete load and examine base talents')
        grid = MEOWFFICER_TALENT_GRID_2 if self._meow_detect_shift() else MEOWFFICER_TALENT_GRID_1

        # Appropriate grid acquired, scan for special talents
        talented = False
        for _ in grid.buttons:
            # Empty slot; check for many white pixels
            if self.image_color_count(_, color=(255, 255, 247), threshold=221, count=200):
                continue

            # Non-empty slot; check for few white pixels
            # i.e. roman numerals
            if self.image_color_count(_, color=(255, 255, 255), threshold=221, count=25):
                continue

            # Detected special talent; break
            talented = True
            break

        logger.info('At least one special talent ability detected') if talented else \
        logger.info('No special talent abilities detected')
        return talented

    def _meow_apply_lock(self, skip_first_screenshot=True):
        """
        Apply lock onto the acquired trained meowfficer
        Prevents the meowfficer being used as feed / enhance
        material

        Args:
            skip_first_screenshot (bool):
        """
        confirm_timer = Timer(1.5, count=3).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if self.appear_then_click(MEOWFFICER_UNLOCKED, offset=(40, 40), interval=3):
                confirm_timer.reset()
                continue

            # End
            if self.appear(MEOWFFICER_LOCKED, offset=(40, 40)):
                if confirm_timer.reached():
                    break

        # Wait until info bar disappears
        self.ensure_no_info_bar(timeout=1)

    def _meow_skip_lock(self):
        """
        Applicable to only gold variant meowfficer
        Handle skip transitions; proceeds slowly
        with caution to prevent unintentional actions
        """
        # Trigger lock popup appearance to initiate sequence
        self.ui_click(MEOWFFICER_TRAIN_CLICK_SAFE_AREA,
                      appear_button=MEOWFFICER_GET_CHECK, check_button=MEOWFFICER_CONFIRM,
                      offset=(40, 40), retry_wait=3, skip_first_screenshot=True)

        # Transition out of lock popup
        # Use callable as screen is variable
        def check_popup_exit():
            if self.appear(MEOWFFICER_GET_CHECK, offset=(40, 40)):
                return True

            if self.appear(MEOWFFICER_TRAIN_START, offset=(20, 20)):
                return True

            return False

        self.ui_click(MEOWFFICER_CANCEL, check_button=check_popup_exit,
                      offset=(40, 20), retry_wait=3, skip_first_screenshot=True)

    def meow_get(self, skip_first_screenshot=True):
        """
        Transition through all the necessary screens
        to acquire each trained meowfficer
        Animation is waited for as the amount can vary
        Only gold variant meowfficer will prompt for
        confirmation

        Args:
            skip_first_screenshot (bool): Skip first
            screen shot or not

        Pages:
            in: MEOWFFICER_GET_CHECK
            out: MEOWFFICER_TRAIN
        """
        # Loop through possible screen transitions
        confirm_timer = Timer(1.5, count=3).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if self.handle_meow_popup_dismiss():
                confirm_timer.reset()
                continue
            if self.appear(MEOWFFICER_GET_CHECK, offset=(40, 40), interval=3):
                if self.appear(MEOWFFICER_GOLD_CHECK, offset=(40, 40)):
                    if not self.config.Meowfficer_RetainTalentedGold or not self._meow_is_talented():
                        self._meow_skip_lock()
                        skip_first_screenshot = True
                        confirm_timer.reset()
                        continue
                    self._meow_apply_lock()

                if self.appear(MEOWFFICER_PURPLE_CHECK, offset=(40, 40)):
                    if self.config.Meowfficer_RetainTalentedPurple and self._meow_is_talented():
                        self._meow_apply_lock()

                # Susceptible to exception when collecting multiple
                # Mitigate by popping click_record
                self.device.click(MEOWFFICER_TRAIN_CLICK_SAFE_AREA)
                self.device.click_record.pop()
                confirm_timer.reset()
                self.interval_reset(MEOWFFICER_GET_CHECK)
                continue

            # End
            if self.appear(MEOWFFICER_TRAIN_START, offset=(20, 20)):
                if confirm_timer.reached():
                    break
            else:
                confirm_timer.reset()

    def meow_collect(self, is_sunday=False):
        """
        Collect one or all trained meowfficer(s)
        Completed slots are automatically moved
        to top of queue, assume to check top-left
        slot only

        Args:
            is_sunday (bool): Whether today is Sunday or not

        Pages:
            in: MEOWFFICER_TRAIN
            out: MEOWFFICER_TRAIN

        Returns:
            Bool whether collected or not
        """
        logger.hr('Meowfficer collect', level=2)

        if self.appear(MEOWFFICER_TRAIN_COMPLETE, offset=(20, 20)):
            # Today is Sunday, finish all else get just one
            if is_sunday:
                logger.info('Collect all trained meowfficers')
                button = MEOWFFICER_TRAIN_FINISH_ALL
            else:
                logger.info('Collect single trained meowfficer')
                button = MEOWFFICER_TRAIN_COMPLETE
            self.ui_click(button, check_button=MEOWFFICER_GET_CHECK,
                          additional=self.handle_meow_popup_dismiss,
                          offset=(40, 40), skip_first_screenshot=True)

            # Get loop mechanism to collect trained meowfficer(s)
            self.meow_get()
            return True
        return False
