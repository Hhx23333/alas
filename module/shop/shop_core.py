from module.base.button import ButtonGrid
from module.base.decorator import cached_property
from module.logger import logger
from module.ocr.ocr import Digit
from module.shop.assets import *
from module.shop.base import ShopBase, ShopItemGrid

OCR_SHOP_CORE = Digit(SHOP_CORE, letter=(239, 239, 239), name='OCR_SHOP_CORE')
OCR_SHOP_AMOUNT = Digit(SHOP_AMOUNT, letter=(239, 239, 239), name='OCR_SHOP_AMOUNT')


class CoreShop(ShopBase):
    _shop_core = 0

    def shop_core_get_currency(self):
        """
        Ocr shop core currency
        """
        self._shop_core = OCR_SHOP_CORE.ocr(self.device.image)
        logger.info(f'Core: {self._shop_core}')
        return self._shop_core

    @cached_property
    def shop_core_items(self):
        """
        Returns:
            ShopItemGrid:
        """
        shop_grid = self.shop_grid
        shop_core_items = ShopItemGrid(shop_grid, templates={}, amount_area=(60, 74, 96, 95))
        shop_core_items.load_template_folder('./assets/shop/core')
        shop_core_items.load_cost_template_folder('./assets/shop/cost')
        return shop_core_items

    def shop_core_check_item(self, item):
        """
        Args:
            item: Item to check

        Returns:
            bool:
        """
        if item.price > self._shop_core:
            return False
        return True

    def shop_buy_amount_execute(self, item):
        """
        Args:
            item: Item to check

        Returns:
            bool: implicating failed to execute
        """
        index_offset = (40, 20)
        limit = 0

        # In case either -/+ shift position, use
        # shipyard ocr trick to accurately parse
        self.appear(AMOUNT_MINUS, offset=index_offset)
        self.appear(AMOUNT_PLUS, offset=index_offset)
        area = OCR_SHOP_AMOUNT.buttons[0]
        OCR_SHOP_AMOUNT.buttons = [(AMOUNT_MINUS.button[2] + 3, area[1], AMOUNT_PLUS.button[0] - 3, area[3])]

        # Total number that can be purchased
        # altogether based on clicking max
        # Needs small delay for stable image
        self.appear_then_click(AMOUNT_MAX)
        self.device.sleep((0.3, 0.5))
        self.device.screenshot()
        limit = OCR_SHOP_AMOUNT.ocr(self.device.image)
        if not limit:
            self.device.click(SHOP_CLICK_SAFE_AREA)  # Close amount prompt
            return False

        # Adjust purchase amount if needed
        while 1:
            if (limit * item.price) <= self._shop_core:
                break
            else:
                limit -= 1

        self.ui_ensure_index(limit, letter=OCR_SHOP_AMOUNT, prev_button=AMOUNT_MINUS, next_button=AMOUNT_PLUS,
                             skip_first_screenshot=True)
        self.device.click(SHOP_BUY_CONFIRM_AMOUNT)
        return True

    def shop_core_interval_clear(self):
        """
        Clear interval on select assets for
        shop_core_buy_handle
        """
        self.interval_clear(SHOP_BUY_CONFIRM_AMOUNT)

    def shop_core_buy_handle(self, item):
        """
        Handle shop_core buy interface if detected

        Args:
            item: Item to handle

        Returns:
            bool: whether interface was detected and handled
        """
        if self.appear(SHOP_BUY_CONFIRM_AMOUNT, offset=(20, 20), interval=3):
            if not self.shop_buy_amount_execute(item):
                logger.warning('Failed to purchase amount item')
            self.interval_reset(SHOP_BUY_CONFIRM_AMOUNT)
            return True

        return False
