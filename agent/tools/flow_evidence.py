from langchain_core.tools import tool
import pandas as pd
from pathlib import Path

@tool
def get_flow_evidence(event_id: str, max_flows: int = 10) -> str:
    """Retrieve raw suspicious network flow records and Isolation Forest anomaly scores supporting a specific event ID."""
    flows_path = Path("outputs/suspicious_flows_with_metadata.csv")
    if not flows_path.exists():
        return f"Error: suspicious_flows_with_metadata.csv not found."
    
    # Assuming flows are linked to event_id or filtered by matching source/destination in attack events
    events_path = Path("outputs/attack_events.csv")
    if not events_path.exists():
        return f"Error: attack_events.csv not found."
    
    events_df = pd.read_csv(events_path)
    match = events_df[events_df['event_id'].astype(str) == str(event_id)]
    if match.empty:
        return f"Event ID {event_id} not found."
    
    event = match.iloc[0]
    flows_df = pd.read_csv(flows_path)
    
    # Filter flows matching source IP and destination IP of the event
    matched_flows = flows_df[(flows_df['src_ip'] == event['src_ip']) & (flows_df['dst_ip'] == event['dst_ip'])]
    if matched_flows.empty:
        return f"No individual flow records found matching event {event_id} (Src: {event['src_ip']}, Dst: {event['dst_ip']})."
    
    return matched_flows.head(max_flows).to_json(orient='records')