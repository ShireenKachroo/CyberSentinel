import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import json

load_dotenv()
from agent.workflow import create_investigation_graph

def test_investigation():
    print("Initializing investigation test...")
    
    events_path = Path("outputs/attack_events.csv")
    if not events_path.exists():
        print(f"Error: Could not find {events_path}.")
        return
    
    df = pd.read_csv(events_path)
    sample_event_id = str(df.iloc[0]['event_id'])
    print(f"Selected sample Event ID for investigation: {sample_event_id}")

    graph = create_investigation_graph()

    initial_state = {
        "event_id": sample_event_id,
        "target_ip": None,
        "messages": [
            HumanMessage(content=f"Investigate event ID {sample_event_id}. Use your tools to fetch details, check related events, and provide a final summary report.")
        ],
        "investigation_steps": [],
        "retrieved_evidence": {},
        "investigation_complete": False,
        "final_report": None
    }

    print("\nStarting agentic multi-step investigation loop...")
    print("-" * 60)

    config = {"recursion_limit": 15}
    last_report_content = ""

    for step in graph.stream(initial_state, config=config, stream_mode="updates"):
        for node_name, output in step.items():
            print(f"\n[Node Executed: {node_name.upper()}]")
            if "messages" in output:
                for msg in output["messages"]:
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tc in msg.tool_calls:
                            print(f"Agent calling tool: '{tc['name']}' with args: {tc['args']}")
                    elif hasattr(msg, "content") and msg.content:
                        content_text = msg.content
                        print(f"LLM Output / Summary:\n{content_text}")
                        # Capture the latest substantive LLM response as the report
                        if len(content_text) > 100:
                            last_report_content = content_text

    # Automatically save report if generated
    if last_report_content:
        output_dir = Path("agentic_investigation_output")
        output_dir.mkdir(parents=True, exist_ok=True)

        md_path = output_dir / f"agentic_investigation_{sample_event_id}.md"
        md_path.write_text(last_report_content, encoding="utf-8")

        json_path = output_dir / f"agentic_investigation_{sample_event_id}.json"
        json_path.write_text(json.dumps({"event_id": sample_event_id, "report": last_report_content}, indent=2), encoding="utf-8")

        print(f"\nReport successfully saved to:\n- {md_path}\n- {json_path}")

    print("\n" + "=" * 60)
    print("Investigation test finished successfully!")

if __name__ == "__main__":
    test_investigation()