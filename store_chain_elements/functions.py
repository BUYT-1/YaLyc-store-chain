import os.path
from typing import Union, Optional, Dict
from hashlib import pbkdf2_hmac
import sqlite3
import configparser

from PyQt5.QtWidgets import QComboBox, QSpinBox, QLineEdit

CONFIG_FILE_STRUCTURE = {
    'Localization': {'language': 'English'},
    'Database': {'path_to_db': 'None'},
}


def fix_config_file():
    """Create or fix config file.

    Create a config file if it doesn't exist and repair it if it is malformed.
    """
    if not os.path.isfile('configuration.cfg'):
        with open('configuration.cfg', 'x'):
            pass

    config = configparser.ConfigParser()
    config.read('configuration.cfg')
    for section in CONFIG_FILE_STRUCTURE:
        if section not in config.sections():
            config[section] = {}
        for parameter, default in CONFIG_FILE_STRUCTURE[section].items():
            if parameter not in config[section]:
                config[section][parameter] = default
    with open('configuration.cfg', 'w') as config_file:
        config.write(config_file)


def hash_data(data: str, salt: str) -> str:
    return str(pbkdf2_hmac('sha3_512', data.encode('utf-8'), salt.encode('utf-8'), 100000))


def check_password(password: str):
    if len(password) < 8:
        return False
    return True


def get_db_path() -> Optional[str]:
    config = configparser.ConfigParser()
    config.read('configuration.cfg')
    path = config['Database']['path_to_db']
    if path is None:
        return None
    if not os.path.isfile(path):
        return None
    return path


def quick_query(query: str) -> list:
    """Query the db once without maintaining a persistent connection."""
    path = get_db_path()
    if path is None:
        return []
    try:
        with sqlite3.connect(path) as connection:
            cursor = connection.cursor()
            return cursor.execute(query).fetchall()
    except sqlite3.Error:
        return []


def get_info(
        obj: Union[QLineEdit, QComboBox, QSpinBox],
        index_mapping: Dict[QComboBox, Dict[int, Optional[int]]]
) -> Optional[str]:
    if isinstance(obj, (QLineEdit, QSpinBox)):
        return obj.text()
    if isinstance(obj, QComboBox):
        v = index_mapping[obj][obj.currentIndex()]
        return v if v is None else str(v)
    raise TypeError(f'Info getter undefined for type {type(obj).__name__}')

