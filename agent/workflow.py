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
    system_prompt = SystemMessage(content="""You are an expert Principal SOC Cyber Threat Intelligence Analyst and Incident Commander.
Your objective is to investigate security events by evaluating tool evidence, network graph topologies, and anomaly scores, and writing a comprehensive, professional, human-readable SOC Incident Investigation Report.

CRITICAL REPORT STRUCTURE REQUIREMENTS:
1. EXECUTIVE SUMMARY: High-level overview of what happened, sources, targets, and threat severity.
2. DETAILED MALICIOUS INTENT ANALYSIS (Why it is malicious): Explain behavioral anomalies, protocol abuse (e.g., SSH-Patator / FTP-Patator brute-force patterns, packet flags, rapid successive connections), and why these signatures deviate from normal baseline traffic.
3. RISK SCORING JUSTIFICATION: Detail how the anomaly scores, flow volume, and attack category weights justify the risk assessment.
4. CORRELATED THREAT PATHS: Explain precursor or successor attack chains discovered via graph topology.
5. ACTIONABLE SOC REMEDIATION PLAYBOOKS: Provide precise, technical mitigation steps (e.g., firewall rule blocking, daemon hardening, fail2ban configuration) that an analyst can execute immediately.

NEVER dump raw JSON arrays or unstructured logs directly into the narrative. Synthesize everything into professional Markdown with clear headings and tables.""")
    
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