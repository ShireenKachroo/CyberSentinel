from langchain_core.tools import tool
import pandas as pd
from pathlib import Path

@tool
def get_host_history(ip_address: str, max_records: int = 15) -> str:
    """Retrieve all historical suspicious events associated with a specific source or destination IP address."""
    events_path = Path("outputs/attack_events.csv")
    if not events_path.exists():
        return f"Error: attack_events.csv not found."
    
    df = pd.read_csv(events_path)
    history = df[(df['src_ip'] == ip_address) | (df['dst_ip'] == ip_address)]
    if history.empty:
        return f"No historical events found for IP address {ip_address}."
    
    return history.head(max_records).to_json(orient='records')