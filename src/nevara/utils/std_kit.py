from prompt_toolkit import PromptSession

def input_prompt(prefix: str):
    session = PromptSession(multiline=True)
    return session.prompt_async(prefix)