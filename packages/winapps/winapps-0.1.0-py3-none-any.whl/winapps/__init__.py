import re
import shlex
import winreg
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Optional, Generator, Any, Tuple, Callable, Mapping

import plumbum


@dataclass
class InstalledApplication:
    name: str
    version: Optional[str] = None
    install_date: Optional[date] = None
    install_location: Optional[Path] = None
    install_source: Optional[Path] = None
    modify_path: Optional[str] = None
    publisher: Optional[str] = None
    uninstall_string: Optional[str] = None

    def modify(self, quiet: bool = True) -> None:
        command = _command(self.modify_path, quiet=quiet)
        command()

    def uninstall(self, quiet: bool = True) -> None:
        command = _command(self.uninstall_string, quiet=quiet)
        command()


def list_installed() -> Generator[InstalledApplication, None, None]:
    application_or_none_generator = (_installed_application(application_key)
                                     for application_key in _installed_application_keys())
    return (application for application in application_or_none_generator if application is not None)


def search_installed(name: Optional[str] = None,
                     flags: int = re.IGNORECASE,
                     **kwargs
                     ) -> Generator[InstalledApplication, None, None]:
    patterns = {key: value for key, value in {'name': name, **kwargs}.items() if value}
    for app in list_installed():
        matches = True
        for field_name, pattern in patterns.items():
            if not re.search(pattern=pattern, string=str(getattr(app, field_name, '')), flags=flags):
                matches = False
                break
        if matches:
            yield app


_ROOT_KEY = winreg.HKEY_LOCAL_MACHINE
_VALUE_NOT_SET = '(value not set)'


def _none_on_value_not_set(value: Any) -> Any:
    return value if value != _VALUE_NOT_SET else None


REGISTRY_KEY_TO_APPLICATION_FIELD_DICT: Mapping[str, Optional[Callable]] = defaultdict(lambda: None, **{
    'DisplayName': lambda value: ('name', _none_on_value_not_set(value)),
    'DisplayVersion': lambda value: ('version', _none_on_value_not_set(str(value))),
    'InstallDate': lambda value: (
        'install_date', _none_on_value_not_set(value) and datetime.strptime(value, '%Y%m%d').date()),
    'InstallLocation': lambda value: ('install_location', _none_on_value_not_set(value) and Path(value)),
    'InstallSource': lambda value: ('install_source', _none_on_value_not_set(value) and Path(value)),
    'ModifyPath': lambda value: ('modify_path', _none_on_value_not_set(value)),
    'Publisher': lambda value: ('publisher', _none_on_value_not_set(value)),
    'UninstallString': lambda value: ('uninstall_string', _none_on_value_not_set(value)),
})


def _installed_application_keys() -> Generator[str, None, None]:
    uninstall_keys = [
        r'Software\Microsoft\Windows\CurrentVersion\Uninstall',
        r'Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
    ]
    for uninstall_key in uninstall_keys:
        uninstall_opened_key = winreg.OpenKey(_ROOT_KEY, uninstall_key)
        i = 0
        while True:
            try:
                application = winreg.EnumKey(uninstall_opened_key, i)
                yield f'{uninstall_key}\\{application}'
                i += 1
            except OSError:
                break


def _installed_application_registry_values(application_key: str) -> Generator[Tuple[str, Any, int], None, None]:
    application_opened_key = winreg.OpenKey(_ROOT_KEY, application_key)
    i = 0
    while True:
        try:
            data = winreg.EnumValue(application_opened_key, i)
            yield data
            i += 1
        except OSError:
            return


def _installed_application(application_key: str) -> Optional[InstalledApplication]:
    def skip() -> bool:
        def guid_to_squid(guid: str) -> str:
            """Taken from salt.utils.win_functions"""
            guid_pattern = re.compile(
                r'^\{(\w{8})-(\w{4})-(\w{4})-(\w\w)(\w\w)-(\w\w)(\w\w)(\w\w)(\w\w)(\w\w)(\w\w)\}$')
            guid_match = guid_pattern.match(guid)
            # noinspection PyShadowingNames
            result = ''
            if guid_match is not None:
                for index in range(1, 12):
                    result += guid_match.group(index)[::-1]
            return result

        def key_exists(key: int, sub_key: str) -> bool:
            try:
                winreg.OpenKey(key, sub_key)
                return True
            except FileNotFoundError:
                return False

        is_system_component = name == 'SystemComponent' and value > 0
        is_win_installer_absent_in_products = False
        if name == 'WindowsInstaller' and value > 0:
            squid = guid_to_squid(application_key.rpartition('\\')[2])
            products_key = r'Software\Classes\Installer\Products' + '\\' + squid
            if not key_exists(_ROOT_KEY, products_key):
                is_win_installer_absent_in_products = True
        is_update = ((name == 'ReleaseType' and value not in ['Hotfix', 'Security Update', 'Update Rollup'])
                     or (name == 'ParentKeyName'))
        is_win_update = name == 'DisplayName' and bool(re.match(r'^KB[0-9]{6}', value))
        # noinspection PyShadowingNames
        result = is_system_component or is_win_installer_absent_in_products or is_update or is_win_update
        return result

    result = InstalledApplication(name='')
    for data in _installed_application_registry_values(application_key):
        name, value, type_ = data
        if skip():
            return None
        f = REGISTRY_KEY_TO_APPLICATION_FIELD_DICT[name]
        if f is not None:
            setattr(result, *f(value))
    if not result.name:
        return None
    return result


def _command(command_str: str, quiet: bool = True) -> 'plumbum.machines.local.LocalCommand':
    command_list = shlex.split(command_str, posix=False)
    command_path, command_args = command_list[0], tuple(command_list[1:])
    if command_path.startswith('"') and command_path.endswith('"'):
        command_path = command_path[1:-1]
    if quiet:
        command_args += ('/quiet', )
    return plumbum.local[command_path][command_args]
