import argparse
import logging
import queue
import time
from datetime import datetime
from multiprocessing import Manager, Process
from multiprocessing.managers import SyncManager
from typing import Dict, Generator, List

from filelock import FileLock
from pywebio import config as webconfig
from pywebio.exceptions import SessionClosedException, SessionNotFoundException
from pywebio.output import (clear, close_popup, output, popup, put_button,
                            put_buttons, put_collapse, put_column, put_error,
                            put_html, put_loading, put_markdown, put_row,
                            put_text, toast)
from pywebio.pin import pin, pin_wait_change
from pywebio.session import go_app, info, register_thread, run_js, set_env

# This must be the first to import
from module.logger import logger  # Change folder

import module.webui.lang as lang
import module.config.server as server
from module.config.config import AzurLaneConfig, Function
from module.config.config_updater import ConfigUpdater
from module.config.utils import (alas_instance, deep_get, deep_iter, deep_set,
                                 dict_to_kv, filepath_args, filepath_config,
                                 read_file, write_file)
from module.webui.config import WebuiConfig
from module.webui.base import Frame
from module.webui.lang import _t, t
from module.webui.pin import put_input, put_select
from module.webui.translate import translate
from module.webui.utils import (Icon, QueueHandler, Task, Thread, add_css,
                                filepath_css, get_output,
                                get_window_visibility_state, login,
                                parse_pin_value, re_fullmatch)
from module.webui.widgets import ScrollableCode, put_group, put_icon_buttons

config_updater = ConfigUpdater()
webui_config = WebuiConfig()


class AlasManager:
    sync_manager: SyncManager
    all_alas: Dict[str, "AlasManager"] = {}

    def __init__(self, config_name: str = 'alas') -> None:
        self.config_name = config_name
        self.log_queue = self.sync_manager.Queue()
        self.log = []
        self.log_max_length = 500
        self.log_reduce_length = 100
        self._process = Process()
        self.thd_log_queue_handler = Thread()

    def start(self, func: str = 'Alas') -> None:
        if not self.alive:
            self._process = Process(
                target=AlasManager.run_alas,
                args=(self.config_name, self.log_queue, func))
            self._process.start()
            self.thd_log_queue_handler = Thread(
                target=self._thread_log_queue_handler)
            register_thread(self.thd_log_queue_handler)
            self.thd_log_queue_handler.start()
        else:
            toast(t("Gui.Toast.AlasIsRunning"), position='right', color='warn')

    def stop(self) -> None:
        lock = FileLock(f"{filepath_config(self.config_name)}.lock")
        with lock:
            if self.alive:
                self._process.terminate()
                self.log.append("Scheduler stopped.\n")
            if self.thd_log_queue_handler.is_alive():
                self.thd_log_queue_handler.stop()

    def _thread_log_queue_handler(self) -> None:
        while self.alive:
            log = self.log_queue.get()
            self.log.append(log)
            if len(self.log) > self.log_max_length:
                self.log = self.log[self.log_reduce_length:]

    @property
    def alive(self) -> bool:
        return self._process.is_alive()

    @classmethod
    def get_alas(cls, config_name: str) -> "AlasManager":
        """
        Create a new alas if not exists.
        """
        if config_name not in cls.all_alas:
            cls.all_alas[config_name] = AlasManager(config_name)
        return cls.all_alas[config_name]

    @staticmethod
    def run_alas(config_name, q: queue.Queue, func: str) -> None:
        # Setup logger
        qh = QueueHandler(q)
        formatter = logging.Formatter(
            fmt='%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        webconsole = logging.StreamHandler(stream=qh)
        webconsole.setFormatter(formatter)
        logging.getLogger('alas').addHandler(webconsole)

        # Set server before loading any buttons.
        config = AzurLaneConfig(config_name=config_name)
        server.server = deep_get(config.data, keys='Alas.Emulator.Server', default='cn')

        # Run alas
        if func == 'Alas':
            from alas import AzurLaneAutoScript
            AzurLaneAutoScript(config_name=config_name).loop()
        elif func == 'Daemon':
            from module.daemon.daemon import AzurLaneDaemon
            AzurLaneDaemon(config=config_name, task='Daemon').run()
        elif func == 'OpsiDaemon':
            from module.daemon.os_daemon import AzurLaneDaemon
            AzurLaneDaemon(config=config_name, task='OpsiDaemon').run()
        elif func == 'AzurLaneUncensored':
            from module.daemon.uncensored import AzurLaneUncensored
            AzurLaneUncensored(config=config_name, task='AzurLaneUncensored').run()
            q.put("Scheduler stopped.\n")  # Prevent status turns to warning
        elif func == 'Benchmark':
            from module.daemon.benchmark import Benchmark
            Benchmark(config=config_name, task='Benchmark').run()
            q.put("Scheduler stopped.\n")  # Prevent status turns to warning
        elif func == 'GameManager':
            from module.daemon.game_manager import GameManager
            GameManager(config=config_name, task='GameManager').run()
            q.put("Scheduler stopped.\n")
        else:
            logger.critical("No function matched")


class AlasGUI(Frame):
    ALAS_MENU: Dict[str, Dict[str, List[str]]]
    ALAS_ARGS: Dict[str, Dict[str, Dict[str, Dict[str, str]]]]
    path_to_idx: Dict[str, str] = {}
    idx_to_path: Dict[str, str] = {}
    theme = 'default'

    @classmethod
    def shorten_path(cls, prefix='a') -> None:
        """
        Reduce pin_wait_change() command content-length
        Using full path name will transfer ~16KB per command,
        may lag when remote control or in bad internet condition.
        Use ~4KB after doing this.
        Args:
            prefix: all idx need to be a valid html, so a random character here
        """
        cls.ALAS_MENU = read_file(filepath_args('menu'))
        cls.ALAS_ARGS = read_file(filepath_args('args'))
        i = 0
        for list_path, _ in deep_iter(cls.ALAS_ARGS, depth=3):
            cls.path_to_idx['.'.join(list_path)] = f'{prefix}{i}'
            cls.idx_to_path[f'{prefix}{i}'] = '.'.join(list_path)
            i += 1

    def __init__(self) -> None:
        super().__init__()
        # modified keys, return values of pin_wait_change()
        self.modified_config_queue = queue.Queue()
        # alas config name
        self.alas_name = ''
        self.alas_config = AzurLaneConfig('template')
        self.alas_logs = ScrollableCode()
        self.alas_running = output().style("container-overview-task")
        self.alas_pending = output().style("container-overview-task")
        self.alas_waiting = output().style("container-overview-task")

    def set_aside(self) -> None:

        # note: value doesn't matters if onclick is a list, button binds to functions in order.
        # when onclick isn't a list, value will pass to function.
        self.aside.reset(
            put_icon_buttons(Icon.DEVELOP, buttons=[{"label": t(
                "Gui.Aside.Develop"), "value": "Develop", "color": "aside"}], onclick=[self.ui_develop]),
            *[put_icon_buttons(Icon.RUN,
                               buttons=[{"label": name, "value": name, "color": "aside"}],
                               onclick=self.ui_alas)
              for name in alas_instance()],
            put_icon_buttons(Icon.ADD, buttons=[{"label": t(
                "Gui.Aside.AddAlas"), "value": "AddAlas", "color": "aside"}], onclick=[self.ui_add_alas]),
        )
        self.aside_setting.reset(
            put_icon_buttons(
                Icon.SETTING,
                buttons=[
                    {"label": t("Gui.Aside.Setting"),
                     "value": "setting", "color": "aside"}],
                onclick=[self.ui_setting],
            )
        )

    def set_status(self, status: int) -> None:
        """
        Args:
            status (int): 
                1 (running),
                2 (not running),
                -1 (warning, stop unexpectedly),
                0 (hide)
        """
        if not self.visible:
            return
        if self._status == status:
            return
        self._status = status

        if status == 1:
            s = put_row([
                put_loading(color='success').style(
                    "width:1.5rem;height:1.5rem;border:.2em solid currentColor;border-right-color:transparent;"),
                None,
                put_text(t("Gui.Status.Running"))
            ], size='auto 2px 1fr')
        elif status == 2:
            s = put_row([
                put_loading(color='secondary').style("width:1.5rem;height:1.5rem;border:.2em solid currentColor;"),
                None,
                put_text(t("Gui.Status.Inactive"))
            ], size='auto 2px 1fr')
        elif status == -1:
            s = put_row([
                put_loading(shape='grow', color='warning').style("width:1.5rem;height:1.5rem;"),
                None,
                put_text(t("Gui.Status.Warning"))
            ], size='auto 2px 1fr')
        else:
            s = ''

        self.status.reset(s)

    @classmethod
    def set_theme(cls, theme='default') -> None:
        cls.theme = theme
        webui_config.Theme = theme
        webconfig(theme=theme)

    # Alas

    def alas_set_menu(self) -> None:
        """
        Set menu for alas
        """
        self.menu.append(
            put_buttons([
                {"label": t("Gui.MenuAlas.Overview"),
                 "value": "Overview", "color": "menu"}
            ], onclick=[self.alas_overview]).style(f'--menu-Overview--'),
        )
        for key, tasks in deep_iter(self.ALAS_MENU, depth=2):
            # path = '.'.join(key)
            menu = key[1]

            if menu == 'Tool':
                _onclick = self.alas_daemon_overview
            else:
                _onclick = self.alas_set_group

            task_btn_list = []
            for task in tasks:
                task_btn_list.append(
                    put_buttons([
                        {"label": t(f'Task.{task}.name'), "value": task, "color": "menu"}
                    ], onclick=_onclick).style(f'--menu-{task}--')
                )

            self.menu.append(
                put_collapse(
                    title=t(f"Menu.{menu}.name"),
                    content=task_btn_list
                )
            )

        self.alas_overview()

    def alas_set_group(self, task: str) -> None:
        """
        Set arg groups from dict
        """
        self.init_menu(name=task)
        self.title.reset(f"{t(f'Task.{task}.name')}")

        group_area = output()
        navigator = output()

        if self.is_mobile:
            content_alas = group_area
        else:
            content_alas = put_row([
                None,
                group_area,
                navigator,
            ], size="1fr minmax(25rem, 5fr) 2fr")

        self.content.append(content_alas)

        config = config_updater.update_config(self.alas_name)

        for group, arg_dict in deep_iter(self.ALAS_ARGS[task], depth=1):
            group = group[0]
            group_help = t(f"{group}._info.help")
            if group_help == "" or not group_help:
                group_help = None
            arg_group = put_group(t(f"{group}._info.name"), group_help)
            list_arg = []
            for arg, d in deep_iter(arg_dict, depth=1):
                arg = arg[0]
                arg_type = d['type']
                if arg_type == 'disable':
                    continue
                value = deep_get(config, f'{task}.{group}.{arg}', d['value'])
                value = str(value) if isinstance(value, datetime) else value

                # Option
                options = deep_get(d, 'option', None)
                if options:
                    option = []
                    for opt in options:
                        o = {"label": t(f"{group}.{arg}.{opt}"), "value": opt}
                        if value == opt:
                            o["selected"] = True
                        option.append(o)
                else:
                    option = None

                # Help
                arg_help = t(f"{group}.{arg}.help")
                if arg_help == "" or not arg_help:
                    arg_help = None

                # Invalid feedback
                invalid_feedback = t("Gui.Text.InvalidFeedBack").format(d['value'])

                list_arg.append(get_output(
                    arg_type=arg_type,
                    name=self.path_to_idx[f"{task}.{group}.{arg}"],
                    title=t(f"{group}.{arg}.name"),
                    arg_help=arg_help,
                    value=value,
                    options=option,
                    invalid_feedback=invalid_feedback,
                ))
            if list_arg:
                group_area.append(arg_group)
                arg_group.append(*list_arg)

    def alas_overview(self) -> None:
        self.init_menu(name="Overview")
        self.title.reset(f"{t(f'Gui.MenuAlas.Overview')}")

        scheduler = put_row([
            put_text(t("Gui.Overview.Scheduler")).style(
                "font-size: 1.25rem; margin: auto .5rem auto;"),
            None,
            put_buttons(
                buttons=[
                    {"label": t("Gui.Button.Start"),
                     "value": "Start", "color": "scheduler-on"},
                    {"label": t("Gui.Button.Stop"),
                     "value": "Stop", "color": "scheduler-off"},
                ],
                onclick=[
                    lambda: self.alas.start('Alas'),
                    self.alas.stop,
                ]
            )
        ], size="auto 1fr auto").style("container-overview-group")

        log = put_row([
            put_text(t("Gui.Overview.Log")).style(
                "font-size: 1.25rem; margin: auto .5rem auto;"),
            None,
            put_buttons(
                buttons=[
                    {"label": t("Gui.Button.ClearLog"),
                     "value": "ClearLog", "color": "scheduler-on"},
                    {"label": t("Gui.Button.ScrollON"),
                     "value": "ScrollON", "color": "scheduler-on"},
                    {"label": t("Gui.Button.ScrollOFF"),
                     "value": "ScrollOFF", "color": "scheduler-on"},
                ],
                onclick=[
                    self.alas_logs.reset,
                    lambda: self.alas_logs.set_scroll(True),
                    lambda: self.alas_logs.set_scroll(False),
                ],
            )
        ], size="auto 1fr auto").style("container-overview-group")

        running = put_column([
            put_text(t("Gui.Overview.Running")).style("group-overview-title"),
            put_html('<hr class="hr-group">'),
            self.alas_running,
        ], size="auto auto 1fr").style("container-overview-group")

        pending = put_column([
            put_text(t("Gui.Overview.Pending")).style("group-overview-title"),
            put_html('<hr class="hr-group">'),
            self.alas_pending,
        ], size="auto auto 1fr").style("container-overview-group")

        waiting = put_column([
            put_text(t("Gui.Overview.Waiting")).style("group-overview-title"),
            put_html('<hr class="hr-group">'),
            self.alas_waiting,
        ], size="auto auto 1fr").style("container-overview-group")

        if self.is_mobile:
            self.content.append(
                put_column([
                    scheduler,
                    running,
                    pending,
                    waiting,
                ], size="auto 7.75rem 13rem 13rem"),
                put_column([
                    log,
                    self.alas_logs.output
                ], size="auto 1fr").style("height: 100%; overflow-y: auto")
            )
        else:
            self.content.append(
                put_row([
                    put_column([
                        scheduler,
                        running,
                        pending,
                        waiting,
                    ], size="auto 7.75rem minmax(7.75rem, 13rem) minmax(7.75rem, 1fr)"
                    ).style("height: 100%; overflow-y: auto"),
                    put_column([
                        log,
                        self.alas_logs.output
                    ], size="auto 1fr").style("height: 100%; overflow-y: auto"),
                ], size="minmax(16rem, 20rem) minmax(24rem, 1fr)"
                ).style("height: 100%; overflow-y: auto"),
            )

        def refresh_overview_tasks():
            while True:
                yield self.alas_update_overiew_tasks()

        self.task_handler.add(refresh_overview_tasks(), 10, True)
        self.task_handler.add(self.alas_put_log(), 0.2, True)

    def alas_put_log(self) -> Generator[None, None, None]:
        last_idx = len(self.alas.log)
        self.alas_logs.append(''.join(self.alas.log))
        lines = 0
        while True:
            yield
            idx = len(self.alas.log)
            if idx < last_idx:
                last_idx -= self.alas.log_reduce_length
            if idx != last_idx:
                try:
                    self.alas_logs.append(''.join(self.alas.log[last_idx:idx]))
                except SessionNotFoundException:
                    break
                lines += idx - last_idx
                last_idx = idx

    def _alas_thread_wait_config_change(self) -> None:
        paths = []
        for path, d in deep_iter(self.ALAS_ARGS, depth=3):
            if d['type'] == 'disable':
                continue
            paths.append(self.path_to_idx['.'.join(path)])
        while self.alive:
            try:
                val = pin_wait_change(*paths)
                self.modified_config_queue.put(val)
            except SessionClosedException:
                break

    def _alas_thread_update_config(self) -> None:
        modified = {}
        valid = []
        invalid = []
        while self.alive:
            try:
                d = self.modified_config_queue.get(timeout=10)
                config_name = self.alas_name
            except queue.Empty:
                continue
            modified[self.idx_to_path[d['name']]] = parse_pin_value(d['value'])
            while True:
                try:
                    d = self.modified_config_queue.get(timeout=1)
                    modified[self.idx_to_path[d['name']]] = parse_pin_value(d['value'])
                except queue.Empty:
                    config = read_file(filepath_config(config_name))
                    for k, v in modified.copy().items():
                        validate = deep_get(self.ALAS_ARGS, k + '.validate')
                        if not len(str(v)):
                            default = deep_get(self.ALAS_ARGS, k + '.value')
                            deep_set(config, k, default)
                            valid.append(self.path_to_idx[k])
                            modified[k] = default
                        elif not validate or re_fullmatch(validate, v):
                            deep_set(config, k, v)
                            valid.append(self.path_to_idx[k])
                        else:
                            modified.pop(k)
                            invalid.append(self.path_to_idx[k])
                            logger.warning(f'Invalid value {v} for key {k}, skip saving.')
                            # toast(t("Gui.Toast.InvalidConfigValue").format(
                            #       t('.'.join(k.split('.')[1:] + ['name']))),
                            #       duration=0, position='right', color='warn')
                    self.pin_remove_invalid_mark(valid)
                    self.pin_set_invalid_mark(invalid)
                    if modified:
                        toast(t("Gui.Toast.ConfigSaved"),
                              duration=1, position='right', color='success')
                        logger.info(f'Save config {filepath_config(config_name)}, {dict_to_kv(modified)}')
                        write_file(filepath_config(config_name), config)
                    modified.clear()
                    valid.clear()
                    invalid.clear()
                    break

    def alas_update_status(self) -> None:
        if hasattr(self, 'alas'):
            if self.alas.alive:
                self.set_status(1)
            elif len(self.alas.log) == 0 or self.alas.log[-1] == "Scheduler stopped.\n":
                self.set_status(2)
            else:
                self.set_status(-1)
        else:
            self.set_status(0)

    def alas_update_overiew_tasks(self) -> None:
        if not self.visible:
            return
        self.alas_config.load()
        self.alas_config.get_next_task()

        if len(self.alas_config.pending_task) >= 1:
            if self.alas.alive:
                running = self.alas_config.pending_task[:1]
                pending = self.alas_config.pending_task[1:]
            else:
                running = []
                pending = self.alas_config.pending_task[:]
        else:
            running = []
            pending = []
        waiting = self.alas_config.waiting_task

        def box(func: Function):
            return put_row([
                put_column([
                    put_text(t(f'Task.{func.command}.name')).style("arg-title"),
                    put_text(str(func.next_run)).style("arg-help"),
                ], size="auto auto"),
                put_button(
                    label=t("Gui.Button.Setting"),
                    onclick=lambda: self.alas_set_group(func.command),
                    color="scheduler-on"
                ),
            ], size="1fr auto").style("container-overview-args")
            # Another version without setting button, box become clickable
            # return put_column([
            #     put_text(t(f'Task.{func.command}.name')).style("arg-title"),
            #     put_text(str(func.next_run)).style("arg-help"),
            # ], size="auto auto"
            # ).style("container-overview-args"
            # ).onclick(lambda: self.alas_set_group(func.command))

        no_task_style = "text-align:center; font-size: 0.875rem; color: darkgrey;"

        if running:
            self.alas_running.reset(*[box(task) for task in running])
        else:
            self.alas_running.reset(
                put_text(t("Gui.Overview.NoTask")).style(no_task_style)
            )
        if pending:
            self.alas_pending.reset(*[box(task) for task in pending])
        else:
            self.alas_pending.reset(
                put_text(t("Gui.Overview.NoTask")).style(no_task_style)
            )
        if waiting:
            self.alas_waiting.reset(*[box(task) for task in waiting])
        else:
            self.alas_waiting.reset(
                put_text(t("Gui.Overview.NoTask")).style(no_task_style)
            )

    def alas_daemon_overview(self, task: str) -> None:
        self.init_menu(name=task)
        self.title.reset(f"{t(f'Task.{task}.name')}")

        scheduler = put_row([
            put_text(t("Gui.Overview.Scheduler")).style(
                "font-size: 1.25rem; margin: auto .5rem auto;"),
            None,
            put_buttons(
                buttons=[
                    {"label": t("Gui.Button.Start"),
                     "value": "Start", "color": "scheduler-on"},
                    {"label": t("Gui.Button.Stop"),
                     "value": "Stop", "color": "scheduler-off"},
                ],
                onclick=[
                    lambda: self.alas.start(task),
                    self.alas.stop,
                ]
            )
        ], size="auto 1fr auto").style("container-overview-group")

        log = put_row([
            put_text(t("Gui.Overview.Log")).style(
                "font-size: 1.25rem; margin: auto .5rem auto;"),
            None,
            put_buttons(
                buttons=[
                    {"label": t("Gui.Button.ClearLog"),
                     "value": "ClearLog", "color": "scheduler-on"},
                    {"label": t("Gui.Button.ScrollON"),
                     "value": "ScrollON", "color": "scheduler-on"},
                    {"label": t("Gui.Button.ScrollOFF"),
                     "value": "ScrollOFF", "color": "scheduler-on"},
                ],
                onclick=[
                    self.alas_logs.reset,
                    lambda: self.alas_logs.set_scroll(True),
                    lambda: self.alas_logs.set_scroll(False),
                ],
            )
        ], size="auto 1fr auto").style("container-overview-group")

        setting = output().style("container-overview-group")

        if self.is_mobile:
            self.content.append(
                put_column([
                    scheduler,
                    setting,
                    log,
                    self.alas_logs.output
                ], size="auto auto auto 1fr"
                ).style("height: 100%; overflow-y: auto")
            )
        else:
            self.content.append(
                put_row([
                    None,
                    put_column([
                        put_row([
                            scheduler,
                            log,
                        ], size="auto auto"),
                        setting,
                        self.alas_logs.output
                    ], size="auto minmax(6rem, auto) minmax(15rem, 1fr)"
                    ).style("height: 100%; overflow-y: auto"),
                    None,
                ], size="1fr minmax(25rem, 6fr) 1fr"
                ).style("height: 100%; overflow-y: auto")
            )

        config = config_updater.update_config(self.alas_name)

        for group, arg_dict in deep_iter(self.ALAS_ARGS[task], depth=1):
            group = group[0]
            setting.append(put_text(t(f"{group}._info.name")).style("group-title"))
            group_help = t(f"{group}._info.help")
            if group_help:
                setting.append(put_text(group_help).style("group-help"))

            list_arg = []
            for arg, d in deep_iter(arg_dict, depth=1):
                arg = arg[0]
                arg_type = d['type']
                if arg_type == 'disable':
                    continue
                value = deep_get(config, f'{task}.{group}.{arg}', d['value'])
                value = str(value) if isinstance(value, datetime) else value

                # Option
                options = deep_get(d, 'option', None)
                if options:
                    option = []
                    for opt in options:
                        o = {"label": t(f"{group}.{arg}.{opt}"), "value": opt}
                        if value == opt:
                            o["selected"] = True
                        option.append(o)
                else:
                    option = None

                # Help
                arg_help = t(f"{group}.{arg}.help")
                if arg_help == "" or not arg_help:
                    arg_help = None

                list_arg.append(get_output(
                    arg_type=arg_type,
                    name=self.path_to_idx[f"{task}.{group}.{arg}"],
                    title=t(f"{group}.{arg}.name"),
                    arg_help=arg_help,
                    value=value,
                    options=option,
                ))
            if list_arg:
                setting.append(*list_arg)

        self.task_handler.add(self.alas_put_log(), 0.2, True)

    # Develop

    def dev_set_menu(self) -> None:
        self.init_menu(collapse_menu=False, name="Develop")

        self.menu.append(
            put_buttons([
                {"label": t("Gui.MenuDevelop.HomePage"),
                 "value": "HomePage", "color": "menu"}
            ], onclick=[self.show]).style(f'--menu-HomePage--'),

            put_buttons([
                {"label": t("Gui.MenuDevelop.Translate"),
                 "value": "Translate", "color": "menu"}
            ], onclick=[self.dev_translate]).style(f'--menu-Translate--'),

            # put_buttons([
            #     {"label": t("Gui.MenuDevelop.Something"),
            #      "value": "Something", "color": "menu"}
            # ], onclick=[self.dev_something]).style(f'--menu-Something--'),
        )

    def dev_translate(self) -> None:
        go_app('translate', new_window=True)
        lang.TRANSLATE_MODE = True
        self.show()

    # Aside UI route

    def ui_develop(self) -> None:
        self.init_aside(name="Develop")
        self.title.reset(f"{t('Gui.Aside.Develop')}")
        self.dev_set_menu()
        self.alas_name = ''
        if hasattr(self, 'alas'):
            del self.alas
        self.set_status(0)

    def ui_alas(self, config_name: str) -> None:
        if config_name == self.alas_name:
            self.expand_menu()
            return
        self.init_aside(name=config_name)
        self.content.reset()
        self.alas_name = config_name
        self.alas = AlasManager.get_alas(config_name)
        self.alas_config = AzurLaneConfig(config_name, '')
        self.alas_update_status()
        self.alas_set_menu()

    def ui_setting(self) -> None:
        toast('Not implemented', position='right', color='error')
        return
        self.init_aside(name="Setting")
        self.alas_name = ''

    def ui_add_alas(self) -> None:
        with popup(t("Gui.AddAlas.PopupTitle")) as s:
            def get_unused_name():
                all_name = alas_instance()
                for i in range(2, 100):
                    if f'alas{i}' not in all_name:
                        return f'alas{i}'
                else:
                    return ''

            def add():
                name = pin["AddAlas_name"]
                origin = pin["AddAlas_copyfrom"]

                if name not in alas_instance():
                    r = read_file(filepath_config(origin))
                    write_file(filepath_config(name), r)
                    self.set_aside()
                    self.active_button("aside", self.alas_name)
                    close_popup()
                else:
                    clear(s)
                    put(name, origin)
                    put_error(t("Gui.AddAlas.FileExist"), scope=s)

            def put(name=None, origin=None):
                put_input(
                    name="AddAlas_name",
                    label=t("Gui.AddAlas.NewName"),
                    value=name or get_unused_name(),
                    scope=s
                ),
                put_select(
                    name="AddAlas_copyfrom",
                    label=t("Gui.AddAlas.CopyFrom"),
                    options=['template'] + alas_instance(),
                    value=origin or 'template',
                    scope=s
                ),
                put_button(
                    label=t("Gui.AddAlas.Confirm"),
                    onclick=add,
                    scope=s
                )

            put()

    def show(self) -> None:
        clear()
        self.main_area.show()
        self.set_aside()
        self.collapse_menu()
        self.alas_name = ''
        if hasattr(self, 'alas'):
            del self.alas
        self.set_status(0)

        def set_language(l):
            lang.set_language(l)
            self.show()

        def set_theme(t):
            self.set_theme(t)
            run_js("location.reload()")

        # temporary buttons, there is no setting page now :(
        self.content.append(
            put_text("Select your language / 选择语言").style("text-align: center"),
            put_buttons(
                [{"label": "简体中文", "value": "zh-CN"},
                {"label": "繁體中文", "value": "zh-TW"},
                {"label": "English", "value": "en-US"},
                {"label": "日本語", "value": "ja-JP"}],
                onclick=lambda l: set_language(l),
            ).style("text-align: center"),
            put_text("Change theme / 更改主题").style("text-align: center"),
            put_buttons(
                [{"label": "Light", "value": "default", "color": "light"},
                 {"label": "Dark", "value": "dark", "color": "dark"}],
                onclick=lambda t: set_theme(t),
            ).style("text-align: center")
        )

        # show something
        self.content.append(output(output(
            put_markdown("""
            Alas is a free open source software, if you paid for Alas from any channel, please refund.
            Alas 是一款免费开源软件，如果你在任何渠道付费购买了Alas，请退款。
            Project repository 项目地址：`https://github.com/LmeSzinc/AzurLaneAutoScript`
            """)).style('text-align: center')))
        # self.content.append(output(output(
        #     put_markdown("""
        #     ## AzurLaneAutoScript
        #     if you encounter any error or find a bug, [create new issue](https://github.com/LmeSzinc/AzurLaneAutoScript/issues/new/choose) or `@18870#0856` in discord with error logs.
        #     You may found logs in python console or browser console (`Ctrl`+`Shift`+`I` - `Console`)
        #     ![](https://i.loli.net/2021/10/03/5pNYoS8EFcvrhIs.png)
        #     ![](https://i.loli.net/2021/10/03/5xCaATjl6oK7S1f.png)

        #     ## Join in translation
        #     Go `Develop` - `Translate`
        #     """)).style('welcome')))

        if lang.TRANSLATE_MODE:
            lang.reload()

            def _disable():
                lang.TRANSLATE_MODE = False
                self.show()

            toast(_t("Gui.Toast.DisableTranslateMode"), duration=0, position='right', onclick=_disable)

    def run(self) -> None:
        # setup gui
        set_env(title="Alas", output_animation=False)
        add_css(filepath_css('alas'))
        if self.is_mobile:
            add_css(filepath_css('alas-mobile'))
        else:
            add_css(filepath_css('alas-pc'))

        if self.theme == 'dark':
            add_css(filepath_css('dark-alas'))
        else:
            add_css(filepath_css('light-alas'))

        self.show()

        # detect config change
        _thread_wait_config_change = Thread(
            target=self._alas_thread_wait_config_change)
        register_thread(_thread_wait_config_change)
        _thread_wait_config_change.start()

        # save config
        _thread_save_config = Thread(
            target=self._alas_thread_update_config)
        register_thread(_thread_save_config)
        _thread_save_config.start()

        def refresh_status():
            while True:
                yield self.alas_update_status()

        def refresh_visibility_state():
            _visible = self.visible
            while True:
                v = get_window_visibility_state()
                if v != _visible:
                    self.task_handler.remove_running_task()
                    self.visible = v
                    if v:
                        logger.info("Window running in the foreground")
                        self.task_handler.add_task(
                            Task(refresh_visibility_state(), 15, time.time() + 15))
                    else:
                        logger.info("Window running in the background")
                        self.task_handler.add_task(
                            Task(refresh_visibility_state(), 2, time.time() + 2))
                yield

        self.task_handler.add(refresh_status(), 2)
        self.task_handler.add(refresh_visibility_state(), 15)
        self.task_handler.start()


def debug():
    """For interactive python.
        $ python3
        >>> from gui import *
        >>> debug()
        >>> 
    """
    AlasManager.sync_manager = Manager()
    AlasGUI.shorten_path()
    lang.reload()
    AlasGUI().run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Alas web service')
    parser.add_argument('-p', '--port', type=int,
                        help='Port to listen. Default to WebuiPort in deploy setting')
    parser.add_argument('-b', '--backend', type=str, default='starlette',
                        help='Backend framework of web server, starlette or tornado. Default to starlette')
    parser.add_argument('-k', '--key', type=str,
                        help='Password of alas. No password by default')
    parser.add_argument("--cdn", action="store_true",
                        help="Use jsdelivr cdn for pywebio static files (css, js). Self host cdn by default.")
    args = parser.parse_args()

    # Apply config
    AlasGUI.set_theme(theme=webui_config.Theme)
    lang.LANG = webui_config.Language
    port = args.port or int(webui_config.WebuiPort) or 22267
    key = args.key or webui_config.Password
    cdn = args.cdn or (webui_config.CDN == 'true') or False

    logger.hr('Webui configs')
    logger.attr('Theme', webui_config.Theme)
    logger.attr('Language', lang.LANG)
    logger.attr('Port', port)
    logger.attr('Password', True if key else False)
    logger.attr('CDN', cdn)

    AlasManager.sync_manager = Manager()
    AlasGUI.shorten_path()
    lang.reload()


    def index():
        if key != '' and not login(key):
            logger.warning(f"{info.user_ip} login failed.")
            time.sleep(1.5)
            run_js('location.reload();')
            return
        AlasGUI().run()


    if args.backend == 'starlette':
        from pywebio.platform.fastapi import start_server
    else:
        from pywebio.platform.tornado import start_server

    try:
        start_server([index, translate], port=port, debug=True, cdn=cdn)
    finally:
        for alas in AlasManager.all_alas.values():
            alas.stop()
        logger.info("Alas closed.")
