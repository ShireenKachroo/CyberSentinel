import pandas as pd
import networkx as nx
from pathlib import Path

def calculate_incident_risks(events_csv_path, graph_gexf_path, output_csv_path):
    print("Loading events and attack graph for risk assessment...")
    
    # Load events data
    if not Path(events_csv_path).exists():
        raise FileNotFoundError(f"Events file not found at {events_csv_path}")
    df = pd.read_csv(events_csv_path)
    
    # Load NetworkX graph if available
    graph = None
    if Path(graph_gexf_path).exists():
        graph = nx.read_gexf(graph_gexf_path)
    
    risk_results = []
    
    # Threshold defined in your pipeline
    if_threshold = 0.032849
    
    for _, row in df.iterrows():
        event_id = str(row['event_id'])
        anomaly_score = float(row['mean_anomaly_score']) if pd.notna(row['mean_anomaly_score']) else 0.0
        flow_count = int(row['flow_count']) if pd.notna(row['flow_count']) else 0
        
        # Topological feature extraction from NetworkX graph
        node_key = f"event:{event_id}"
        in_deg, out_deg = 0, 0
        if graph and node_key in graph:
            in_deg = graph.in_degree(node_key)
            out_deg = graph.out_degree(node_key)
            
        # Heuristic Risk Scoring Formula (Anomaly Intensity + Flow Volume + Graph Propagation)
        # 1. Anomaly component (lower score means higher anomaly below threshold)
        anomaly_weight = max(0.0, (if_threshold - anomaly_score) / if_threshold) * 45 if anomaly_score < if_threshold else 10
        
        # 2. Volume component (grouped flow records)
        volume_weight = min(25, flow_count * 1.5)
        
        # 3. Topological spread component (predecessors & successors in attack graph)
        topological_weight = min(30, (in_deg + out_deg) * 10)
        
        total_risk_score = round(anomaly_weight + volume_weight + topological_weight, 2)
        
        # Categorize risk severity level
        if total_risk_score > 70:
            risk_level = "CRITICAL"
        elif total_risk_score > 40:
            risk_level = "HIGH"
        elif total_risk_score > 20:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
            
        risk_results.append({
            "event_id": event_id,
            "attack_type": row.get('attack_type', 'Unknown'),
            "risk_score": total_risk_score,
            "risk_level": risk_level,
            "in_degree_precursors": in_deg,
            "out_degree_successors": out_deg,
            "flow_count": flow_count
        })
        
    out_df = pd.DataFrame(risk_results)
    Path(output_csv_path).parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(output_csv_path, index=False)
    print(f"Risk analysis successfully completed! Results saved to {output_csv_path}")

if __name__ == "__main__":
    # Adjust paths according to your project structure
    calculate_incident_risks(
        events_csv_path="outputs/attack_events.csv",
        graph_gexf_path="outputs/attack_graph.gexf",
        output_csv_path="outputs/event_risk_scores.csv"
    )