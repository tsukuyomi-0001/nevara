from pathlib import Path
import tomllib
import configs

config_path = Path(configs.__file__).absolute().parent

with open(config_path / 'config.toml', 'rb') as f:
    config = tomllib.load(f)