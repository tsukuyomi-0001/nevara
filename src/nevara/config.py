from pathlib import Path
import tomllib
import config

config_path = Path(config.__file__).absolute().parent

with open(config_path / 'config.toml', 'rb') as f:
    config = tomllib.load(f)