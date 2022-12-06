from wdlci.config.config_file import ConfigFile
from wdlci.config.config_env import ConfigEnv
from wdlci.exception.wdl_test_cli_exit_exception import WdlTestCliExitException

class Config(object):
    _cli_kwargs = None
    _instance = None
    
    @classmethod
    def __new__(cls, cli_kwargs):
        file = ConfigFile.__new__()
        env = ConfigEnv.__new__(cli_kwargs)
        instance = super(Config, cls).__new__(cls)
        instance.__init__(file, env)
        
        return instance

    @classmethod
    def load(cls, cli_kwargs):
        if cls._instance is not None:
            raise WdlTestCliExitException("Cannot load Config, already loaded", 1)
        
        cls._cli_kwargs = cli_kwargs
        cls._instance = cls.__new__(cli_kwargs)
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            raise WdlTestCliExitException("Config not loaded, use load() first")
        return cls._instance
    
    def __init__(self, file, env):
        self._file = file
        self._env = env
    
    @property
    def file(self):
        return self._file
    
    @property
    def env(self):
        return self._env