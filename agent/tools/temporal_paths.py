from langchain_core.tools import tool
import networkx as nx
from pathlib import Path

@tool
def find_temporal_paths(event_id: str) -> str:
    """Investigate chronological graph relationships, predecessors, and successors for an event using the NetworkX attack graph."""
    graph_path = Path("outputs/attack_graph.gexf")
    if not graph_path.exists():
        return f"Error: attack_graph.gexf not found."
    
    G = nx.read_gexf(graph_path)
    node_key = f"event:{event_id}"
    if node_key not in G:
        return f"Node {node_key} not present in attack graph."
    
    predecessors = list(G.predecessors(node_key))
    successors = list(G.successors(node_key))
    
    result = {
        "event_id": event_id,
        "node_attributes": dict(G.nodes[node_key]),
        "predecessors": [{"node": p, "edge": dict(G.edges[p, node_key])} for p in predecessors],
        "successors": [{"node": s, "edge": dict(G.edges[node_key, s])} for s in successors]
    }
    import json
    return json.dumps(result, default=str)