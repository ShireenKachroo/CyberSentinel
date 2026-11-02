from __future__ import annotations
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, HumanMessage

from agent.state import InvestigationState
from agent.tools.event_details import get_event_details
from agent.tools.get_related_events import get_related_events
from agent.tools.host_history import get_host_history
from agent.tools.temporal_paths import find_temporal_paths
from agent.tools.flow_evidence import get_flow_evidence

tools = [get_event_details, get_related_events, get_host_history, find_temporal_paths, get_flow_evidence]
tool_node = ToolNode(tools)

def get_gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set in .env")
    return ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0.1, google_api_key=api_key).bind_tools(tools)

def call_model(state: InvestigationState):
    print("🤖 Calling Gemini API model for reasoning...")
    model = get_gemini_model()
    system_prompt = SystemMessage(content="""You are an expert autonomous SOC cybersecurity investigation agent.
Your objective is to investigate suspicious network activity events using your available tools.
Execute a concise multi-step investigation:
1. Fetch event details.
2. Check related events and temporal paths if needed.
3. Once you have gathered sufficient evidence, provide a final structured investigation summary report in plain text. Do not keep calling tools endlessly.""")
    
    messages = [system_prompt] + state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state: InvestigationState):
    messages = state["messages"]
    last_message = messages[-1]
    # Agar agent ne tool call karne ko bola hai toh 'tools' node par jao, warna END karo
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
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