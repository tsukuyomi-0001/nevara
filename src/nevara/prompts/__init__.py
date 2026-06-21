from langchain_core.messages import BaseMessage, SystemMessage
from pathlib import Path

from nevara.manager import BaseManager
from nevara.components import util

def load_prompt(path, **kwargs: str) -> str:
    file_path = Path(__file__).absolute().parent
    file = file_path / f"{path}.md"
    if not file.exists(): raise FileNotFoundError
    
    with open(file) as f: return f.read().format(**kwargs)
    
class PromptManager:
    def __init__(self, managers: list[BaseManager]):
        self.managers = managers
        self.prompt_gen_attrib = [manager.prompt_generation() for manager in self.managers]
        
    def prompt_generation(self):
        stitched_prompt = '\n'.join(self.prompt_gen_attrib)
        return stitched_prompt
    
    def stitch_prompts(self, *args: str):
        return '\n'.join(args)
    
    # def store_prompt_template(self, *args: BaseMessage):
    #     self.prompt_template = args
        
    # def load_prompt_template(self) -> tuple[BaseMessage, ...]:
    #     return self.prompt_template
    
    def build_brain_system_prompt(self, history_prompt: str) -> SystemMessage:
        date, time = util.get_time_date()
    
        system_prompt = load_prompt('brain/system', time=time, date=date)
        managers_prompt = self.prompt_generation()
    
        system_content = self.stitch_prompts(
            system_prompt,
            managers_prompt,
            history_prompt 
        ) 
        print(system_content)
        systemMessage = SystemMessage(content=system_content)
        return systemMessage
    
    def build_router_system_prompt(self, task: str) -> SystemMessage:
        system_content = self.stitch_prompts(
            load_prompt('brain/system', task_from_brain=task), 
            self.prompt_generation()
        )
        systemMessage = SystemMessage(content=system_content)
        print(systemMessage.content)
        return systemMessage