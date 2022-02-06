import os

import lz4.block
from adbutils.errors import AdbError

from module.base.utils import *
from module.device.connection import Connection
from module.device.method.utils import handle_adb_error, RETRY_TRIES, RETRY_DELAY
from module.exception import ScriptError, RequestHumanTakeover
from module.logger import logger


class AscreencapError(Exception):
    pass


def retry(func):
    def retry_wrapper(self, *args, **kwargs):
        """
        Args:
            self (AScreenCap):
        """
        for _ in range(RETRY_TRIES):
            try:
                return func(self, *args, **kwargs)
            except RequestHumanTakeover:
                # Can't handle
                break
            except ConnectionResetError as e:
                # When adb server was killed
                logger.error(e)
                self.adb_connect(self.serial)
            except AscreencapError as e:
                # When ascreencap not installed
                logger.error(e)
                self.ascreencap_init()
            except AdbError as e:
                if not handle_adb_error(e):
                    break
            except Exception as e:
                # Unknown
                # Probably trucked image
                logger.exception(e)

            self.sleep(RETRY_DELAY)

        logger.critical(f'Retry {func.__name__}() failed')
        raise RequestHumanTakeover

    return retry_wrapper


class AScreenCap(Connection):
    __screenshot_method = [0, 1, 2]
    __screenshot_method_fixed = [0, 1, 2]
    __bytepointer = 0

    def ascreencap_init(self):
        logger.hr('aScreenCap init')
        self.__bytepointer = 0

        arc = self.adb_shell(['getprop', 'ro.product.cpu.abi'])
        sdk = self.adb_shell(['getprop', 'ro.build.version.sdk'])
        logger.info(f'cpu_arc: {arc}, sdk_ver: {sdk}')

        filepath = os.path.join(self.config.ASCREENCAP_FILEPATH_LOCAL, arc, 'ascreencap')
        if int(sdk) not in range(21, 26) or not os.path.exists(filepath):
            logger.critical('No suitable version of aScreenCap lib available for this device')
            logger.critical('Please use ADB or uiautomator2 for screenshots instead')
            raise RequestHumanTakeover

        logger.info(f'pushing {filepath}')
        self.adb_push(filepath, self.config.ASCREENCAP_FILEPATH_REMOTE)

        logger.info(f'chmod 0777 {self.config.ASCREENCAP_FILEPATH_REMOTE}')
        self.adb_shell(['chmod', '0777', self.config.ASCREENCAP_FILEPATH_REMOTE])

    def uninstall_ascreencap(self):
        logger.info('Removing ascreencap')
        self.adb_shell(['rm', self.config.ASCREENCAP_FILEPATH_REMOTE])

    def _ascreencap_reposition_byte_pointer(self, byte_array):
        """Method to return the sanitized version of ascreencap stdout for devices
            that suffers from linker warnings. The correct pointer location will be saved
            for subsequent screen refreshes
        """
        while byte_array[self.__bytepointer:self.__bytepointer + 4] != b'BMZ1':
            self.__bytepointer += 1
            if self.__bytepointer >= len(byte_array):
                text = 'Repositioning byte pointer failed, corrupted aScreenCap data received'
                logger.warning(text)
                raise AscreencapError(text)
        return byte_array[self.__bytepointer:]

    def _ascreencap_execute(self):
        stream = self.adb_shell([self.config.ASCREENCAP_FILEPATH_REMOTE, '--pack', '2', '--stdout'], stream=True)

        content = b""
        while True:
            chunk = stream.read(4096)
            if not chunk:
                break
            content += chunk

        return self.__process_screenshot(content)

    def __load_screenshot(self, screenshot, method):
        if method == 0:
            pass
        elif method == 1:
            screenshot = screenshot.replace(b'\r\n', b'\n')
        elif method == 2:
            screenshot = screenshot.replace(b'\r\r\n', b'\n')
        else:
            raise ScriptError(f'Unknown method to load screenshots: {method}')

        raw_compressed_data = self._ascreencap_reposition_byte_pointer(screenshot)

        # See headers in:
        # https://github.com/ClnViewer/Android-fast-screen-capture#streamimage-compressed---header-format-using
        compressed_data_header = np.frombuffer(raw_compressed_data[0:20], dtype=np.uint32)
        if compressed_data_header[0] != 828001602:
            compressed_data_header = compressed_data_header.byteswap()
            if compressed_data_header[0] != 828001602:
                text = f'aScreenCap header verification failure, corrupted image received. ' \
                    f'HEADER IN HEX = {compressed_data_header.tobytes().hex()}'
                logger.warning(text)
                raise AscreencapError(text)

        _, uncompressed_size, _, width, height = compressed_data_header
        channel = 3
        data = lz4.block.decompress(raw_compressed_data[20:], uncompressed_size=uncompressed_size)

        image = np.frombuffer(data, dtype=np.uint8)
        # Equivalent to cv2.imdecode()
        shape = image.shape[0]
        image = image[shape - width * height * channel:].reshape(height, width, channel)
        image = cv2.flip(image, 0)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def __process_screenshot(self, screenshot):
        for method in self.__screenshot_method_fixed:
            try:
                result = self.__load_screenshot(screenshot, method=method)
                self.__screenshot_method_fixed = [method] + self.__screenshot_method
                return result
            except lz4.block.LZ4BlockError:
                self.__bytepointer = 0
                continue

        self.__screenshot_method_fixed = self.__screenshot_method
        if len(screenshot) < 100:
            logger.warning(f'Unexpected screenshot: {screenshot}')
        raise OSError(f'cannot load screenshot')

    @retry
    def screenshot_ascreencap(self):
        stream = self.adb_shell([self.config.ASCREENCAP_FILEPATH_REMOTE, '--pack', '2', '--stdout'], stream=True)

        content = b""
        while True:
            chunk = stream.read(4096)
            if not chunk:
                break
            content += chunk

        return self.__process_screenshot(content)
