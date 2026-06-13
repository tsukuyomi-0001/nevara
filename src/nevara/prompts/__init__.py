from pathlib import Path

def load_prompt(path, **kwargs):
    file_path = Path(__file__).absolute().parent
    file = file_path / f"{path}.md"
    if not file.exists(): raise FileNotFoundError
    
    with open(file) as f: return f.read().format(**kwargs)