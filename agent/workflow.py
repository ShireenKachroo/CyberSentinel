from __future__ import annotations
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, HumanMessage

from agent.state import InvestigationState
from agent.tools.event_details import get_event_details
from agent.tools.related_events import get_related_events
from agent.tools.host_history import get_host_history
from agent.tools.temporal_paths import find_temporal_paths
from agent.tools.flow_evidence import get_flow_evidence

tools = [get_event_details, get_related_events, get_host_history, find_temporal_paths, get_flow_evidence]
tool_node = ToolNode(tools)

def get_gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set in .env")
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1, google_api_key=api_key).bind_tools(tools)

def call_model(state: InvestigationState):
    model = get_gemini_model()
    system_prompt = SystemMessage(content="""You are an expert autonomous SOC cybersecurity investigation agent.
Your objective is to thoroughly investigate suspicious network activity events using your available tools.
You must execute a multi-step investigation:
1. First, retrieve event details.
2. Investigate related events and host history.
3. Check temporal attack graph paths.
4. Retrieve raw flow evidence.
5. Synthesize your findings into an evidence-backed incident investigation report.
Do not fabricate evidence. Rely solely on tool outputs.""")
    
    messages = [system_prompt] + state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state: InvestigationState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

def create_investigation_graph():
    workflow = StateGraph(InvestigationState)
    
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    
    workflow.set_entry_point("agent")
    
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()