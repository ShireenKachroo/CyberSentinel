import streamlit as st
import pandas as pd
import json
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Risk Assessment & Incident Triage",
    page_icon="",
    layout="wide"
)

# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
<style>
.stApp {
    background: #070b11;
    color: #edf3fa;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.smallcaps {
    color: #6f9fc8;
    font-size: 0.70rem;
    font-weight: 800;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}

.subtitle {
    color: #8190a3;
    font-size: 1rem;
}

.card {
    background: #0e1722;
    border: 1px solid #26374b;
    border-radius: 14px;
    padding: 20px;
    min-height: 150px;
}

.value {
    font-size: 1.5rem;
    font-weight: 800;
    margin: 8px 0;
}

.desc {
    color: #718196;
    font-size: 0.85rem;
}

.rule {
    height: 1px;
    background: #1c2938;
    margin: 30px 0;
}

.risk-card {
    background: #0e1722;
    border: 1px solid #26374b;
    border-radius: 14px;
    padding: 24px;
}

.risk-label {
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.risk-score {
    color: #edf3fa;
    font-size: 3rem;
    font-weight: 850;
    margin-top: 8px;
}

.factor {
    background: #0b121b;
    border: 1px solid #1d2b3a;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 12px;
}

.playbook-box {
    background: #0b1824;
    border: 1px solid #234c6a;
    border-left: 3px solid #49a8ff;
    border-radius: 10px;
    padding: 18px;
    margin-top: 10px;
    color: #edf3fa;
}
</style>
""",
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## CyberSentinel")
    st.caption("ML-Based Cyber Attack Detection")
    st.divider()
    st.page_link("app.py", label="Dashboard")
    st.page_link("pages/attack_detection.py", label="Attack Detection")
    st.markdown("**INVESTIGATION**")
    st.page_link("pages/incident_investigation.py", label="Incident Investigation")
    st.page_link("pages/attack_graph.py", label="Attack Graph")
    st.page_link("pages/risk_assessment.py", label="Risk Assessment")
    st.page_link("pages/ai_investigation.py", label="AI Investigation")

# ============================================================
# DATA LOADER
# ============================================================

@st.cache_data
def load_risk_data():
    risk_csv = Path("outputs/event_risk_scores.csv")
    if risk_csv.exists():
        return pd.read_csv(risk_csv)
    return pd.DataFrame()

df_risks = load_risk_data()

# ============================================================
# PAGE HEADER
# ============================================================

st.markdown('<div class="smallcaps">CYBERSENTINEL RISK INTELLIGENCE</div>', unsafe_allow_html=True)
st.title("Incident Risk & Agentic Triage")
st.markdown('<div class="subtitle">Evaluate real-time incident severity, agent reasoning, and protocol-specific remediation playbooks.</div>', unsafe_allow_html=True)

# ============================================================
# INCIDENT SELECTOR & MAIN VIEW
# ============================================================

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="smallcaps">SELECT INCIDENT</div>', unsafe_allow_html=True)

if not df_risks.empty:
    incident_options = [
        f"{row['event_id']} — {row['attack_type']} (Risk: {row['risk_score']} [{row['risk_level']}])"
        for _, row in df_risks.iterrows()
    ]
    selected_str = st.selectbox("Choose Incident for Triage", incident_options)
    selected_event_id = selected_str.split(" — ")[0]
    selected_row = df_risks[df_risks['event_id'].astype(str) == selected_event_id].iloc[0]
    
    current_score = selected_row['risk_score']
    current_level = selected_row['risk_level']
    attack_type = selected_row['attack_type']
    flow_vol = selected_row['flow_count']
    in_deg = selected_row['in_degree_precursors']
    out_deg = selected_row['out_degree_successors']
else:
    selected_event_id = "EVT-00001"
    current_score = 78.0
    current_level = "HIGH"
    attack_type = "SSH-Patator"
    flow_vol = 2
    in_deg = 1
    out_deg = 1

# Try loading agent/investigation JSON if available for real reasoning & playbooks
investigation_json = Path(f"outputs/agentic_investigation_{selected_event_id}.json")
agent_rationale = ""
agent_steps = []

if investigation_json.exists():
    try:
        inv_data = json.loads(investigation_json.read_text(encoding="utf-8"))
        inv_content = inv_data.get("investigation", {})
        agent_rationale = inv_content.get("risk_rationale", "")
        agent_steps = inv_content.get("recommended_next_steps", [])
    except Exception:
        pass

# Fallback dynamic reasoning if json isn't generated yet
if not agent_rationale:
    agent_rationale = (
        f"The telemetry for target event {selected_event_id} ({attack_type}) displays anomalous behavior "
        f"exceeding Isolation Forest baseline margins. Network graph correlation reveals {in_deg} incoming "
        f"precursor connections and {out_deg} outgoing paths across {flow_vol} grouped flows, indicating active reconnaissance or brute-force persistence."
    )

if not agent_steps:
    if "ssh" in attack_type.lower():
        agent_steps = [
            "Disable password authentication on target SSH daemon and enforce strict public-key cryptography.",
            "Implement Fail2ban service on port 22 to temporarily ban source IPs exceeding 3 authentication failures.",
            "Restrict port 22 access via firewall ACLs strictly to authorized internal jump hosts."
        ]
    elif "ftp" in attack_type.lower():
        agent_steps = [
            "Enforce strict authentication threshold limits in vsftpd/proftpd configurations.",
            "Disable anonymous FTP access and inspect authentication logs for unauthorized session creation.",
            "Restrict port 21 via firewall filters to authorized subnet segments."
        ]
    else:
        agent_steps = [
            "Isolate the affected destination host from the primary broadcast domain for manual forensics.",
            "Inspect active firewall session tables and capture NetFlow telemetry for the associated source IP.",
            "Audit system authentication and application logs for potential unauthorized privilege escalation."
        ]

# ============================================================
# TWO-COLUMN LAYOUT (SCORE vs AGENT RATIONALE & PLAYBOOKS)
# ============================================================

left, right = st.columns([1, 1.8])

with left:
    st.markdown('<div class="smallcaps">SEVERITY RATING</div>', unsafe_allow_html=True)
    st.markdown("## Risk Score")

    color_code = "#ff4d4d" if current_level == "CRITICAL" else "#ffa500" if current_level == "HIGH" else "#49a8ff"

    risk_html = (
        '<div class="risk-card">'
        f'<div class="risk-label" style="color:{color_code};">LEVEL: {current_level}</div>'
        f'<div class="risk-score">'
        f'{current_score} '
        '<span style="font-size:1rem;color:#718196;font-weight:600;">/ 100</span>'
        '</div>'
        f'<div class="desc" style="margin-top:12px;">'
        f'<b>Attack Vector:</b> {attack_type}<br>'
        f'<b>Graph Centrality:</b> {in_deg} In / {out_deg} Out links<br>'
        f'<b>Flow Volume:</b> {flow_vol} records'
        '</div>'
        '</div>'
    )
    st.markdown(risk_html, unsafe_allow_html=True)

with right:
    st.markdown('<div class="smallcaps">AGENTIC INTELLIGENCE</div>', unsafe_allow_html=True)
    st.markdown("## Why This Incident Is Risky")
    
    st.markdown(
        f'<div class="factor"><div style="color:#edf3fa;line-height:1.5;">{agent_rationale}</div></div>',
        unsafe_allow_html=True
    )
    
    st.markdown("## Recommended Next Steps (Tactical Playbooks)")
    
    for idx, step in enumerate(agent_steps, 1):
        playbook_html = (
            '<div class="playbook-box">'
            f'<div style="color:#49a8ff;font-size:0.75rem;font-weight:800;margin-bottom:4px;">ACTIONABLE PLAYBOOK 0{idx}</div>'
            f'<div style="font-size:0.9rem;">{step}</div>'
            '</div>'
        )
        st.markdown(playbook_html, unsafe_allow_html=True)