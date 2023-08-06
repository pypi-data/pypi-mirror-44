"""Add python related paths to the user's PATH environment variable."""
import ctypes
import sys
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM as LRESULT, LPVOID
from os.path import abspath

import winreg

HKCU = winreg.HKEY_CURRENT_USER
ENV = "Environment"
PATH = "PATH"

HWND_BROADCAST = 0xFFFF
WM_SETTINGCHANGE = 0x1A


def notify_windows():
    """Notifies all windows about a settings change.
    See: <https://docs.microsoft.com/en-us/windows/desktop/winmsg/wm-settingchange>
    """
    SendMessage = ctypes.windll.user32.SendMessageW
    SendMessage.argtypes = HWND, UINT, WPARAM, LPVOID
    SendMessage.restype = LRESULT
    SendMessage(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u'Environment')


def fix_user_env_path():
    """Interactively add important python related paths to the user's PATH
    environment variable."""
    to_check = {
        abspath(sys.prefix),
        abspath(sys.prefix + "\\Scripts"),
    }

    with winreg.CreateKey(HKCU, ENV) as key:
        try:
            current = winreg.QueryValueEx(key, PATH)[0]
        except FileNotFoundError:
            current = ""

        existing = {abspath(p.strip()) for p in current.split(";") if
                    p.strip()}
        to_add = sorted(to_check - existing)
        if not to_add:
            print("Nothing to add.")
            return

        while True:
            print("* The following folders should be added to the PATH"
                  " environment variable:")
            for p in to_add:
                print(p)
            answer = input("* Fix the PATH environment variables on your"
                           " account? [Yn]: ")
            if answer.strip().lower() in ['', 'y', 'yes']:
                break
            if answer.strip().lower() in ['n', 'no']:
                print("Nothing added.")
                return

        new = current.rstrip().rstrip(';') + ";" + ";".join(to_add) + ';'
        winreg.SetValueEx(key, PATH, 0, winreg.REG_EXPAND_SZ, new)

    notify_windows()

    print("Updated.")
    print("PATH will be updated on new sessions.")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Interactive mode.', required=True)
    args = parser.parse_args()

    fix_user_env_path()
