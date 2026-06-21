Current progress:
Made a converstational System as Base for Agentic System.
Currently its simple chatbot style, with with memory system, storing last few messages and rest convert to summary and saved in history.

Following is plan_1 designed for making strong structure for moving chat system to agentic system
long plan 1:
- Memory System R1: last N messages, message summary history, saving and loading memory.
- Personalization: saves user info.
- TTS implementation
- providing for history as memory, use vector DB, persistant, use last 5 history as fresh_memory and retrieve 3K history as old_memory. no dublicate between fresh and old memory.

Following is plan_2 designed for giving brain LM workers, we wouldn't be directly providing tools, but a abstract layer as (worker-executor) pair. currently as plan_2 brain is just a reAct style agent which commands worker rather than using tools itself.
long plan 2:
- STD FS worker:
    - read_file
    - write_file
    - delete_file
    - copy_file
    - move_file
    - rename_file
    - create_dir
    - delete_dir
    - list_dir
    - change_dir
    - tree
    - find_files
    - stat
    - exists

- System worker:
    - full_info_device (disk_usage, memory_info, cpu_info)
    - shell_command
    - run_application

- Scheduler:
    - schedule reminding task.

- Search:
    - duckduckgo search

- document manager:
    - handling documents like - txt, pdf, ppt, docx throught RAG.
    - its just InMemory RAG.

- Memory System R2: artifacts, current working directory, current date/time, schedular reminder.
- Implementation of STT.
- Rover Control Connection through Mobile.
- as Startup Service.

long plan 3:
to properly and best way to make this system deep agent, which can schedule task based on priority, while at the same, leaving converstation/brain agent free all the time. i plan to use a sever-agent invoke system

Zeta Agentic Server
1) take task from brain.
2) re-rank priority list based on priority.
3) assign task to a specialized deep agent.
4) if brain invoke another task, re-rank. if given new task is more priority, pause on going task, save state, and switch.

number of deep agent assignment can be set to N worker throught config.

to invoke zeta agentic server, we plan to make use of MCP, brain agent not only can do simple Agentic Workflow task throught executor, but invoke tools for zeta agentic system.