from langchain_core.tools import tool
import pandas as pd
from pathlib import Path

@tool
def get_flow_evidence(event_id: str, max_flows: int = 5) -> str:
    """Retrieve summarized network flow evidence and anomaly scores supporting a specific event ID."""
    flows_path = Path("outputs/suspicious_flows_with_metadata.csv")
    if not flows_path.exists():
        return f"Error: suspicious_flows_with_metadata.csv not found."
    
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
    
    # Summarize top flows into a readable text format instead of a massive raw JSON dump
    summary_lines = [f"Found {len(matched_flows)} matching flow records for Event {event_id} (Showing top {min(max_flows, len(matched_flows))}):"]
    
    for idx, row in matched_flows.head(max_flows).iterrows():
        flow_id = row.get('flow id', 'N/A')
        src = f"{row.get('src_ip')}:{int(row.get('src_port', 0))}"
        dst = f"{row.get('dst_ip')}:{int(row.get('dst_port', 0))}"
        duration = row.get('flow duration', 0)
        fwd_pkts = row.get('total fwd packets', 0)
        bwd_pkts = row.get('total backward packets', 0)
        label = row.get('label', 'Unknown')
        score = row.get('anomaly_score', 'N/A')
        
        # Extract key flags safely
        flags = []
        if row.get('syn flag count', 0) == 1: flags.append('SYN')
        if row.get('ack flag count', 0) == 1: flags.append('ACK')
        if row.get('psh flag count', 0) == 1: flags.append('PSH')
        if row.get('rst flag count', 0) == 1: flags.append('RST')
        flag_str = ", ".join(flags) if flags else "None"
        
        summary_lines.append(
            f"- **Flow ID**: `{flow_id}`\n"
            f"  - **Connection Path**: `{src}` -> `{dst}`\n"
            f"  - **Classification**: `{label}` | **Anomaly Score**: `{score}`\n"
            f"  - **Duration**: `{duration} µs` | **Packets**: Fwd={fwd_pkts}, Bwd={bwd_pkts}\n"
            f"  - **TCP Flags**: `{flag_str}`"
        )
        
    return "\n".join(summary_lines)