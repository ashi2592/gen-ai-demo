from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda
from utils.llm_model import llm


SUPPORTED_TASKS = ["chat", "transaction", "youtube", "prompt", "calendar", "ms_teams", "todo"]

# This is the correct way: template with {task_list} as a variable
intent_prompt = ChatPromptTemplate.from_template("""
You are an intent classifier for a multi-agent system.

Given a user input, count how many actions relate to each of these task types:
{task_list}

Output a JSON object with a number for each task. If not mentioned, set count to 0.

Example output:
{{"chat": 1, "transaction": 2, "youtube": 0, "prompt": 0, "calendar": 1, "ms_teams": 0, "todo": 1}}

User input: {input}
""")

# Now bind task_list dynamically
intent_prompt = intent_prompt.partial(task_list="\n".join([f"- {task}" for task in SUPPORTED_TASKS]))

# Output parser
parser = JsonOutputParser()

# Chain
intent_classifier_chain = intent_prompt | llm | parser

# RunnableLambda agent
IntentClassifierAgent = RunnableLambda(lambda input: intent_classifier_chain.invoke({"input": input}))
