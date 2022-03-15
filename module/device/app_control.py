from lxml import etree

from module.device.method.adb import Adb
from module.device.method.wsa import WSA
from module.device.method.uiautomator_2 import Uiautomator2
from module.device.method.utils import HierarchyButton
from module.logger import logger


class AppControl(Adb, WSA, Uiautomator2):
    hierarchy: etree._Element

    def app_is_running(self) -> bool:
        method = self.config.Emulator_ControlMethod
        if method == 'uiautomator2' or method == 'minitouch':
            package = self.app_current_uiautomator2()
        else:
            package = self.app_current_adb()

        package = package.strip(' \t\r\n')
        logger.attr('Package_name', package)
        target = self.config.Emulator_PackageName.strip(' \t\r\n')
        return package == target

    def app_start(self):
        package = self.config.Emulator_PackageName
        method = self.config.Emulator_ControlMethod
        wsa = self.config.Emulator_WSA
        logger.info(f'App start: {package}')
        if wsa == "display_0":
            self.app_start_wsa_display_0(package)
        elif method == 'uiautomator2' or method == 'minitouch':
            self.app_start_uiautomator2(package)
        else:
            self.app_start_adb(package)

    def app_stop(self):
        package = self.config.Emulator_PackageName
        method = self.config.Emulator_ControlMethod
        logger.info(f'App stop: {package}')
        if method == 'uiautomator2' or method == 'minitouch':
            self.app_stop_uiautomator2(package)
        else:
            self.app_stop_adb(package)

    def dump_hierarchy(self) -> etree._Element:
        """
        Returns:
            etree._Element: Select elements with `self.hierarchy.xpath('//*[@text="Hermit"]')` for example.
        """
        method = self.config.Emulator_ControlMethod
        if method == 'uiautomator2' or method == 'minitouch':
            self.hierarchy = self.dump_hierarchy_uiautomator2()
        else:
            self.hierarchy = self.dump_hierarchy_adb()
        return self.hierarchy

    def xpath_to_button(self, xpath: str) -> HierarchyButton:
        """
        Args:
            xpath (str):

        Returns:
            HierarchyButton:
                An object with methods and properties similar to Button.
                If element not found or multiple elements were found, return None.
        """
        return HierarchyButton(self.hierarchy, xpath)
