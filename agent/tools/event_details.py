from langchain_core.tools import tool
import pandas as pd
from pathlib import Path

@tool
def get_event_details(event_id: str) -> str:
    """Retrieve detailed metadata, timestamps, anomaly scores, and flow counts for a specific attack event ID."""
    events_path = Path("outputs/attack_events.csv")
    if not events_path.exists():
        return f"Error: attack_events.csv not found at {events_path}"
    
    df = pd.read_csv(events_path)
    match = df[df['event_id'].astype(str) == str(event_id)]
    if match.empty:
        return f"Event ID {event_id} not found in attack events."
    
    return match.iloc[0].to_json()