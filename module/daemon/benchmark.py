import time

import numpy as np
from prettytable import PrettyTable
from rich.table import Table
from rich.text import Text

from module.base.utils import float2str as float2str_
from module.base.utils import random_rectangle_point
from module.daemon.daemon_base import DaemonBase
from module.logger import logger
from module.ui.ui import UI, page_campaign


def float2str(n, decimal=3):
    if not isinstance(n, (float, int)):
        return str(n)
    else:
        return float2str_(n, decimal=decimal) + 's'


class Benchmark(DaemonBase, UI):
    TEST_TOTAL = 15
    TEST_BEST = int(TEST_TOTAL * 0.8)

    def benchmark_test(self, func, *args, **kwargs):
        """
        Args:
            func: Function to test.
            *args: Passes to func.
            **kwargs: Passes to func.

        Returns:
            float: Time cost on average.
        """
        logger.hr(f'Benchmark test', level=2)
        logger.info(f'Testing function: {func.__name__}')
        record = []

        for n in range(1, self.TEST_TOTAL + 1):
            start = time.time()

            try:
                func(*args, **kwargs)
            except Exception as e:
                logger.exception(e)
                logger.warning(f'Benchmark tests failed on func: {func.__name__}')
                return 'Failed'

            cost = time.time() - start
            logger.attr(
                f'{str(n).rjust(2, "0")}/{self.TEST_TOTAL}',
                f'{float2str(cost)}'
            )
            record.append(cost)

        logger.info('Benchmark tests done')
        average = float(np.mean(np.sort(record)[:self.TEST_BEST]))
        logger.info(f'Time cost {float2str(average)} ({self.TEST_BEST} best results out of {self.TEST_TOTAL} tests)')
        return average

    @staticmethod
    def evaluate_screenshot(cost):
        if not isinstance(cost, (float, int)):
            return Text(cost, style="bold bright_red")

        if cost < 0.25:
            return Text('Very Fast', style="bright_green")
        if cost < 0.45:
            return Text('Fast', style="green")
        if cost < 0.65:
            return Text('Medium', style="yellow")
        if cost < 0.95:
            return Text('Slow', style="red")
        return Text('Very Slow', style="bright_red")

    @staticmethod
    def evaluate_click(cost):
        if not isinstance(cost, (float, int)):
            return Text(cost, style="bold bright_red")

        if cost < 0.1:
            return Text('Fast', style="bright_green")
        if cost < 0.2:
            return Text('Medium', style="yellow")
        if cost < 0.4:
            return Text('Slow', style="red")
        return Text('Very Slow', style="bright_red")

    @staticmethod
    def show(test, data, evaluate_func):
        """
        +--------------+--------+--------+
        |  Screenshot  |  time  | Speed  |
        +--------------+--------+--------+
        |     ADB      | 0.319s |  Fast  |
        | uiautomator2 | 0.476s | Medium |
        |  aScreenCap  | Failed | Failed |
        +--------------+--------+--------+
        """
        # table = PrettyTable()
        # table.field_names = [test, 'Time', 'Speed']
        # for row in data:
        #     table.add_row([row[0], f'{float2str(row[1])}', evaluate_func(row[1])])

        # for row in table.get_string().split('\n'):
        #     logger.info(row)
        table = Table(show_lines=True)
        table.add_column(
            test, header_style="bright_cyan", style="cyan", no_wrap=True
        )
        table.add_column("Time", style="magenta")
        table.add_column("Speed", style="green")
        for row in data:
            table.add_row(
                row[0],
                float2str(row[1]),
                evaluate_func(row[1]),
            )
        logger.print(table, justify='center')

    def run(self):
        logger.hr('Benchmark', level=1)
        self.device.remove_minicap()
        self.ui_ensure(page_campaign)

        data = []
        if self.config.Benchmark_TestScreenshotMethod:
            data.append(['ADB', self.benchmark_test(self.device._screenshot_adb)])
            data.append(['uiautomator2', self.benchmark_test(self.device._screenshot_uiautomator2)])
            data.append(['aScreenCap', self.benchmark_test(self.device._screenshot_ascreencap)])
        screenshot = data

        data = []
        area = (124, 4, 649, 106)  # Somewhere save to click.
        if self.config.Benchmark_TestClickMethod:
            x, y = random_rectangle_point(area)
            data.append(['ADB', self.benchmark_test(self.device._click_adb, x, y)])
            x, y = random_rectangle_point(area)
            data.append(['uiautomator2', self.benchmark_test(self.device._click_uiautomator2, x, y)])
            x, y = random_rectangle_point(area)
            data.append(['minitouch', self.benchmark_test(self.device._click_minitouch, x, y)])
        control = data

        def compare(res):
            res = res[1]
            if not isinstance(res, (int, float)):
                return 100
            else:
                return res

        logger.hr('Benchmark Results', level=1)
        if screenshot:
            self.show(test='Screenshot', data=screenshot, evaluate_func=self.evaluate_screenshot)
            fastest = sorted(screenshot, key=lambda item: compare(item))[0]
            logger.info(f'Recommend screenshot method: {fastest[0]} ({float2str(fastest[1])})')
        if control:
            self.show(test='Control', data=control, evaluate_func=self.evaluate_click)
            fastest = sorted(control, key=lambda item: compare(item))[0]
            logger.info(f'Recommend control method: {fastest[0]} ({float2str(fastest[1])})')


if __name__ == '__main__':
    b = Benchmark('alas', task='Benchmark')
    b.run()
