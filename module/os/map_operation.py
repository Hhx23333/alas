from module.base.decorator import Config
from module.base.timer import Timer
from module.base.utils import *
from module.exception import ScriptError, MapDetectionError
from module.logger import logger
from module.ocr.ocr import Ocr
from module.os.assets import *
from module.os.globe_zone import Zone
from module.os.map_fleet_selector import OSFleetSelector
from module.os_handler.map_order import MapOrderHandler
from module.os_handler.mission import MissionHandler
from module.os_handler.port import PortHandler
from module.os_handler.storage import StorageHandler


class OSMapOperation(MapOrderHandler, MissionHandler, PortHandler, StorageHandler, OSFleetSelector):
    zone: Zone
    is_zone_name_hidden = False

    def is_meowfficer_searching(self):
        """
        Returns:
            bool:

        Page:
            in: IN_MAP
        """
        return self.appear(MEOWFFICER_SEARCHING, offset=(10, 10))

    def get_meowfficer_searching_percentage(self):
        """
        Returns:
            float: 0 to 1.

        Pages:
            in: IN_MAP, is_meowfficer_searching == True
        """
        return color_bar_percentage(
            self.device.image, area=MEOWFFICER_SEARCHING_PERCENTAGE.area, prev_color=(74, 223, 255))

    @Config.when(SERVER='en')
    def get_zone_name(self):
        # For EN only
        from string import whitespace
        ocr = Ocr(MAP_NAME, lang='cnocr', letter=(214, 235, 235), threshold=96, name='OCR_OS_MAP_NAME')
        name = ocr.ocr(self.device.image)
        name = name.translate(dict.fromkeys(map(ord, whitespace)))
        name = name.lower()
        self.is_zone_name_hidden = 'safe' in name
        if '-' in name:
            name = name.split('-')[0]
        if 'é' in name:  # Méditerranée name maps
            name = name.replace('é', 'e')
        if 'nvcity' in name:  # NY City Port read as 'V' rather than 'Y'
            name = 'nycity'
        return name

    @Config.when(SERVER='jp')
    def get_zone_name(self):
        # For JP only
        ocr = Ocr(MAP_NAME, lang='jp', letter=(214, 231, 255), threshold=127, name='OCR_OS_MAP_NAME')
        name = ocr.ocr(self.device.image)
        self.is_zone_name_hidden = '安全' in name
        # Remove '安全海域' or '秘密海域' at the end of jp ocr.
        name = name.rstrip('安全海域秘密海域')
        # Kanji '一' and '力' are not used, while Katakana 'ー' and 'カ' are misread as Kanji sometimes.
        # Katakana 'ペ' may be misread as Hiragana 'ぺ'.
        name = name.replace('一', 'ー').replace('力', 'カ').replace('ぺ', 'ペ')
        return name

    @Config.when(SERVER='tw')
    def get_zone_name(self):
        # For TW only
        ocr = Ocr(MAP_NAME, lang='tw', letter=(214, 231, 255), threshold=127, name='OCR_OS_MAP_NAME')
        name = ocr.ocr(self.device.image)
        self.is_zone_name_hidden = '安全' in name
        # Remove '安全海域' or '隱秘海域' at the end of tw ocr.
        name = name.rstrip('安全海域隱秘海域一')
        return name

    @Config.when(SERVER=None)
    def get_zone_name(self):
        # For CN only
        ocr = Ocr(MAP_NAME, lang='cnocr', letter=(214, 231, 255), threshold=127, name='OCR_OS_MAP_NAME')
        name = ocr.ocr(self.device.image)
        self.is_zone_name_hidden = '安全' in name
        if '-' in name:
            name = name.split('-')[0]
        else:
            name = name.rstrip('安全海域-')
        return name

    def get_current_zone(self):
        """
        Returns:
            Zone:

        Raises:
            MapDetectionError: If failed to parse zone name.
            ScriptError:
        """
        name = self.get_zone_name()
        logger.info(f'Map name processed: {name}')
        try:
            self.zone = self.name_to_zone(name)
        except ScriptError as e:
            if self.is_zone_name_hidden:
                # 2021.12.09
                # Safe zones don't display zone names like `NA Ocean SE Sector F - Safe zone`, only display `Safe Zone`.
                # Goto globe map and calculate current zone from pinned location,
                # but this requires higher level APIs.
                logger.info('Zone name is hidden, get current zone from globe map instead')
                if hasattr(self, 'get_current_zone_from_globe'):
                    self.zone = self.get_current_zone_from_globe()
                else:
                    raise ScriptError(
                        'Zone name is hidden, require OperationSiren.get_current_zone_from_globe() to solve')
            else:
                raise MapDetectionError(*e.args)
        logger.attr('Zone', self.zone)
        return self.zone

    def zone_init(self, skip_first_screenshot=True):
        """
        Wrap get_current_zone(), set self.zone to the current zone.
        This method must be called after entering a new zone.
        Handle map events and the animation that zone names appear from the top.

        Args:
            skip_first_screenshot (bool):

        Returns:
            Zone: Current zone.

        Raises:
            MapDetectionError: If failed to parse zone name.
        """
        timeout = Timer(1.5, count=5).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if timeout.reached():
                logger.warning('Zone init timeout')
                break

            if self.handle_map_event():
                timeout.reset()
                continue
            if self.is_in_map():
                try:
                    return self.get_current_zone()
                except MapDetectionError:
                    continue
            else:
                timeout.reset()

        if not self.is_in_map():
            logger.warning('Trying to get zone name, but not in OS map')
        return self.get_current_zone()

    def is_in_special_zone(self):
        """
        Returns:
            bool: If in an obscure zone, abyssal zone, or stronghold.
        """
        return self.appear(MAP_EXIT, offset=(20, 20))

    def map_exit(self, skip_first_screenshot=True):
        """
        Exit from an obscure zone, abyssal zone, or stronghold.

        Args:
            skip_first_screenshot:

        Pages:
            in: is_in_map
            out: is_in_map, zone that you came from
        """
        logger.hr('Map exit')
        confirm_timer = Timer(1, count=2)
        changed = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            # End
            if changed and self.is_in_map():
                if confirm_timer.reached():
                    break
            else:
                confirm_timer.reset()

            if self.appear_then_click(MAP_EXIT, offset=(20, 20), interval=5):
                continue
            if self.handle_popup_confirm('MAP_EXIT'):
                self.interval_reset(MAP_EXIT)
                continue
            if self.handle_map_event():
                self.interval_reset(MAP_EXIT)
                changed = True
                continue

        self.zone_init()
