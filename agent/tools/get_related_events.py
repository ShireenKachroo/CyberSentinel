from langchain_core.tools import tool
import pandas as pd
from pathlib import Path

@tool
def get_related_events(event_id: str, max_results: int = 10) -> str:
    """Find other suspicious events sharing the source or destination IP within a temporal window of the target event."""
    events_path = Path("outputs/attack_events.csv")
    if not events_path.exists():
        return f"Error: attack_events.csv not found."
    
    df = pd.read_csv(events_path)
    target_match = df[df['event_id'].astype(str) == str(event_id)]
    if target_match.empty:
        return f"Event ID {event_id} not found."
    
    target = target_match.iloc[0]
    src_ip = target['src_ip']
    dst_ip = target['dst_ip']
    
    # Find events sharing source or destination IP, excluding self
    related = df[(df['event_id'].astype(str) != str(event_id)) & ((df['src_ip'] == src_ip) | (df['dst_ip'] == dst_ip))]
    if related.empty:
        return f"No related events found sharing source IP {src_ip} or destination IP {dst_ip}."
    
    return related.head(max_results).to_json(orient='records')