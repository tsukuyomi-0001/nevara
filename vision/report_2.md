# current progress
1) successfully completed long_plan_1.
2) long_plan_2 is near completion.

after through thinking about curren and to future archecture, along with maximizing agent's capability (specifically Small LM models). i plan to have following structural changes.

## project splits
reviewing long_plan_2 (a workflow agentic style agent) and long_plan_3 (a MCP server with multiple deep agent). i plan to treat both as different project.

because currently brain is similar to reAct agent but with abstraction for tools. it clear that problem for reasoning, thinking for critical or even general task would be pain specifically for Small LM. for that purpose i plan to make intelligent workflow system wrapped around nevara. while idea for zeta server wouldn't be much of change.

### progress report
1) code clean up is going on.
2) Following are Executor are there complete structurally, and tools that are mentioned will only be the onces.

- fs_executor:
    - read_file
    - write_file
    - create_file
    - delete_file
    - create_dir
    - delete_dir
    - list_directory
    - change_directory
- search_executor:
    - duckduckgo_search
- doc_executor:
    - handling documents like - txt, pdf, ppt, docx, through RAG
    - its inMemory DB.
    - tools like search_document, search_on_documents.

3) bit of changes to prompting.

### task left are
1) implementing executors like
- sys_executor:
    - full_info_device
    - shell_command
    - run_application
2) implementation of STT.
3) memory system transition from R1 -> R2.
4) run as Startup Service.
5) Rover Control Connection through Mobile.


## Zeta Agentic Server.
Zeta Agentic Server is house to manage many deep agents. brain invokes server to launch agent in background by providing tasks, server than add that task to its priority list and re-ranks the tasks, top priority task assigned to specialized deep agent. if brain invoke new tasks, and it has more priority than server should have capability to save agent's state and switch task gracefully.

vision of deep agents are:
1) self research - this agent takes topic, search though online, find books, research papers, site scraping, read them, and make final stitch pdf. pdf is information document so it would be store into special folder called "knowledge bank" which can be accessed by brain of any agent.
2) document Maker - this agent takes task, uses information online, or document from knowledge bank to get information, it also uses online image gneration api to make images, this agent should be able to make documents like txt, docx, ppt, pdf, csv, etc.
3) Vi-Book Maker - this agent takes task, make use of HTML, CSS, JS to make a visual clean interactive web page. 
4) Coding Deep Agent - as name suggest specifically for coding.

to invoke zeta agentic server, we plan to make use of MCP, brain agent not only can do simple Agentic Workflow task throught executor, but invoke tools for zeta agentic system.