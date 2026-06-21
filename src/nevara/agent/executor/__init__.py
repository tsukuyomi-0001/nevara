from pathlib import Path
import importlib
    
def get_executors_index() -> dict:
    scan_dir = Path(__file__).parent.glob('*.py')
    executors_table = {}
    
    for file in scan_dir:
        file_stem = file.stem
        if file.stem == '__init__': continue
        module = importlib.import_module(f"nevara.agent.executor.{file_stem}")
        if not hasattr(module, 'executor_agent'): raise AttributeError(f"Special 'executor_agent' was not found in module: {module}")
        executors_table[file_stem] = module.executor_agent
        
    return executors_table