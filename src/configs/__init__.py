from pathlib import Path
import tomllib

def get_config():
    global_path = Path(__file__).absolute().parent
    with open(global_path / 'config.toml', 'rb') as f:
        config = tomllib.load(f)
        
    return config