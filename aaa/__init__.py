from typing import Dict, Any
from pathlib import Path
from threading import Lock
from dotenv import dotenv_values
from aaa.schema import SimConfig
import sys

class ThreadSafeSingleton(type):
    '''
    Thread-safe implementation of Singleton.
    '''
    _instances: Dict = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=ThreadSafeSingleton):

    try:
        '''
        February 10, 2022
        With the intended approach of making this entire repository pip installable,
        we are minimizing the amount of repository pre-configuration before this entire
        simulator can be used after pip installing.
        '''
        #__config: Dict[str, Any] = dotenv_values('.env')
        #__sim_confs: Dict[str, Any] = sim_conf
        __sim_confs: Dict[str, Any] = SimConfig().dict()
        __version  = "1.0.0"
        __package: str = __package__
        __base_dir = str(Path(__file__).resolve(strict=True).parent.parent)
        __logfile_name = f'{__package}-{__version}.log'
        __config_dir = Path().home() / '.config' / __package
        __default_env = 'dev'
        #__env = str(__config["APP_ENV"])
        __env = 'dev'
    except KeyError as error:
        sys.stderr.write(f"Dotenv config erro: {error} is missing\n")
        sys.exit(1)

    @classmethod
    @property
    def version(cls) -> str:
        '''
        Getter for version of package
        '''
        return cls.__version

    @classmethod
    @property
    def package(cls) -> str:
        return cls.__package

    @classmethod
    @property
    def base_dir(cls) -> str:
        return cls.__base_dir

    @classmethod
    @property
    def logfile_name(cls) -> str: return cls.__logfile_name

    @classmethod
    @property
    def config_dir(cls) -> Path:
        return cls.__config_dir

    @classmethod
    @property
    def default_env(cls) -> str:
        return cls.__default_env

    @classmethod
    @property
    def env(cls) -> str:
        return cls.__env

    @classmethod
    @property
    def sim_confs(cls) -> dict:
        return cls.__sim_confs
