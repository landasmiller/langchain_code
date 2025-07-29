#Built using GoogleColab

!pip install langchain
!pip install openai
!pip install langgraph
!pip install langchain_community
!pip install langchainhub
!pip install langchain-groq

from langgraph.graph import StateGraph as Graph
from langchain_groq import ChatGroq

import os
from google.colab import userdata

os.environ["GROQ_API_KEY"] = userdata.get('GROQ_API_KEY')

llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=os.environ.get("GROQ_API_KEY"))
llm.invoke("hi how are you?")
print(llm.invoke("hi how are you?"))

from langchain_core.messages import HumanMessage

def function1(state):
  llm=ChatGroq(model="llama-3.3-70b-versatile")
  response = llm.invoke(state['messages'][-1].content).content
  return {"messages": [HumanMessage(content=response)]}

function1("hi how are you?")

from langchain_core.messages import HumanMessage

def function2(state):
  last_message = state['messages'][-1]
  upper_string = last_message.content.upper()
  return {"messages": [HumanMessage(content=upper_string)]}

try:
    workflow = Graph()
    print("Successfully created workflow object.")
except NameError:
    print("Error: 'Graph' is not defined. Please make sure you have imported it correctly using 'from langgraph.graph import StateGraph as Graph'")

from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

workflow = Graph(AgentState)
print("Successfully created workflow object.")

workflow.add_node("node1", function1)
workflow.add_node("node2", function2)

#Nodes are the functions that will be executed as part of the workflow

workflow.set_entry_point("node1")
workflow.add_edge("node1", "node2")

# Edges define the flow of control between the nodes in your graph. It is the relationship. how the node is connected to another node.

# First, you need to set the entry point of your graph. The entry point is the node that will be executed first when you run the graph.

# Then, you can add edges between the nodes to define the order in which they will be executed.

def should_continue(state):
    messages = state['messages']
    last_message = messages[-1]
    if len(last_message.content) < 10:
        return "continue"
    else:
        return "end"

workflow.add_conditional_edges(
    "node2",
    should_continue,
    {
        "continue": "node1",
        "end": "__end__",
    },
)

app = workflow.compile()

from langchain_core.messages import HumanMessage

output = app.invoke({"messages": [HumanMessage(content="who were the founding fathers of the United States?")]})

print(output['messages'][-1].content)

from iPython.display import Image, display
try:
  display(Image(app.get_graph().draw_mermaid_png()))
except Exception as e:
  print(e)

