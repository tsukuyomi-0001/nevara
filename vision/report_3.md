# current progress
1) successfully completed long_plan_2.
2) successfully watched one piece 400 episode today. marking complete!

## progress report
1) documentation is added.
2) three executors are available:- search_executor, fs_executor, doc_executor. i didn't feel right to give sys_executor yet.
3) better input prompt.
4) now STT is also available.

# Future heading
again, after decision of zeta agent server and brain_agent seperation. and testing brain agent i saw problems in model, because we are using Small Language Model. currently this is how workflow is happening

workflow:
user_input -> brain -> router_tool OR reminder_tool
where:
router_tool -> executor (SLM) -> tool_call -> return result.
reminder_tool -> set reminder -> return

## problem lies with brain:
1) every converstation, every big system prompt which includes managers prompt generation, history are filling up context. this leads to hallucination AND repeatative decisions.
2) since direct thinking is blocked, and reasoning happens single form by brain directly leads to bad or improper dicision.
3) anything brain output goes to TTS, which means all special characters, all code are spoken which is bad as f.

## 10 shine feature for "GREAT LONG PLAN 1"
1) agent workflow agent recalibrate.
user_input -> brain (decides what to do) options: [SPEAK, THINK, ACT, REASON, DEEP MIND, MEMORY_BUILD]

explain:
SPEAK: brain tells speak node what it want to speak.
REASON: this means to think on along with ongoing context and converstation.
ACT: this means its going to use tool or run execute.
THINK: this is bit different than reasoning, this take current context only, and does the thinking, its like clear mind thinking.
DEEP MIND: this means 1) context isolation, 2) before deep mind execute it retrieval all necessary informaton from on-going context and converstation, old history memorys, knowledge back, and than do thinking.
MEMORY_BUILD: brain literally as memory cortext to build problem processing information memory.

idea is pretty sure it would be similar to this, but maybe happen bit changes.

2) memory cortex:

"UNTIL 10 Shine feature i acknowledged i wouldn't be starting greate_long_plan_1"