import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Risk Assessment",
    page_icon="⚠️",
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
    font-size: 0.8rem;
}

.rule {
    height: 1px;
    background: #1c2938;
    margin: 30px 0;
}

.callout {
    border: 1px solid #234c6a;
    border-left: 3px solid #49a8ff;
    background: #0b1824;
    border-radius: 10px;
    padding: 16px;
    color: #91abc1;
}

.risk-card {
    background: #0e1722;
    border: 1px solid #26374b;
    border-radius: 14px;
    padding: 24px;
}

.risk-label {
    color: #6f9fc8;
    font-size: 0.70rem;
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

.step-row {
    display: flex;
    gap: 18px;
    padding: 16px 0;
    border-bottom: 1px solid #182432;
}

.step-number {
    color: #49a8ff;
    font-size: 0.72rem;
    font-weight: 800;
    min-width: 30px;
}

.step-title {
    color: #edf3fa;
    font-weight: 800;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🛡️ CyberSentinel")
    st.caption("ML-Based Cyber Attack Detection")

    st.divider()

    st.page_link(
        "app.py",
        label="Dashboard",
    )

    st.page_link(
        "pages/attack_detection.py",
        label="Attack Detection",
    )

    st.markdown("**INVESTIGATION**")

    st.page_link(
        "pages/incident_investigation.py",
        label="Incident Investigation",
    )

    st.page_link(
        "pages/attack_graph.py",
        label="Attack Graph",

    )

    st.page_link(
        "pages/risk_assessment.py",
        label="Risk Assessment",
    )

    st.page_link(
        "pages/ai_investigation.py",
        label="AI Investigation",
    )


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    '<div class="smallcaps">CYBERSENTINEL INVESTIGATION</div>',
    unsafe_allow_html=True
)

st.title("Risk Assessment")

st.markdown(
    '<div class="subtitle">Evaluate incident severity using correlated detection evidence.</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div style="margin:16px 0;color:#8fd7ff;font-weight:800;">● RISK ENGINE READY</div>',
    unsafe_allow_html=True
)


# ============================================================
# RISK OVERVIEW
# ============================================================

st.markdown(
    '<div class="rule"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="smallcaps">RISK OVERVIEW</div>',
    unsafe_allow_html=True
)

st.markdown("## Incident Risk Summary")


# ============================================================
# SUMMARY CARDS
# ============================================================

cols = st.columns(4)

summary = [
    ("CURRENT RISK", "HIGH", "Prototype assessment"),
    ("RISK SCORE", "78 / 100", "Prototype score"),
    ("INCIDENTS", "04", "Cases under assessment"),
    ("FACTORS", "04", "Evidence dimensions"),
]

for col, (label, value, description) in zip(cols, summary):

    card_html = (
        '<div class="card">'
        f'<div class="smallcaps">{label}</div>'
        f'<div class="value">{value}</div>'
        f'<div class="desc">{description}</div>'
        '</div>'
    )

    with col:
        st.markdown(
            card_html,
            unsafe_allow_html=True
        )


# ============================================================
# RISK ENGINE
# ============================================================

st.markdown(
    '<div class="rule"></div>',
    unsafe_allow_html=True
)

left, right = st.columns([1, 1.5])


# ============================================================
# LEFT — RISK SCORE
# ============================================================

with left:

    st.markdown(
        '<div class="smallcaps">CURRENT ASSESSMENT</div>',
        unsafe_allow_html=True
    )

    st.markdown("## Risk Score")

    risk_html = (
        '<div class="risk-card">'
        '<div class="risk-label">INCIDENT RISK</div>'
        '<div class="risk-score">'
        '78 '
        '<span style="font-size:1rem;color:#718196;font-weight:600;">/ 100</span>'
        '</div>'
        '<div class="desc" style="margin-top:10px;">'
        'Prototype risk value pending connection to the finalized risk engine.'
        '</div>'
        '</div>'
    )

    st.markdown(
        risk_html,
        unsafe_allow_html=True
    )


# ============================================================
# RIGHT — RISK FACTORS
# ============================================================

with right:

    st.markdown(
        '<div class="smallcaps">RISK INTERPRETATION</div>',
        unsafe_allow_html=True
    )

    st.markdown("## What Contributes to Risk?")

    factors = [
        (
            "Detection Evidence",
            "Anomalous flows identified by the Isolation Forest detection stage."
        ),
        (
            "Event Correlation",
            "Related suspicious events provide additional incident context."
        ),
        (
            "Attack Graph Evidence",
            "Relationships between source hosts, events, attack types and targets."
        ),
        (
            "Temporal Relationships",
            "Event ordering and temporal proximity contribute to incident reconstruction."
        ),
    ]

    for title, description in factors:

        factor_html = (
            '<div class="factor">'
            f'<div style="color:#edf3fa;font-weight:800;">{title}</div>'
            f'<div class="desc" style="margin-top:7px;">{description}</div>'
            '</div>'
        )

        st.markdown(
            factor_html,
            unsafe_allow_html=True
        )


# ============================================================
# INCIDENT ASSESSMENT
# ============================================================

st.markdown(
    '<div class="rule"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="smallcaps">INCIDENT ASSESSMENT</div>',
    unsafe_allow_html=True
)

st.markdown("## Select Incident")

incident = st.selectbox(
    "Incident",
    [
        "INC-001 — Multi-stage network activity",
        "INC-002 — Repeated anomalous connection pattern",
        "INC-003 — Suspicious service interaction",
        "INC-004 — Repeated attack traffic",
    ]
)

selected_html = (
    '<div class="callout" style="margin-top:15px;">'
    '<div class="smallcaps">SELECTED INCIDENT</div>'
    f'<div style="color:#edf3fa;font-weight:800;margin-top:8px;">{incident}</div>'
    '<div class="desc" style="margin-top:12px;">'
    'The finalized risk engine will calculate incident severity from '
    'detection results, correlated events, attack graph relationships '
    'and other evidence.'
    '</div>'
    '</div>'
)

st.markdown(
    selected_html,
    unsafe_allow_html=True
)


# ============================================================
# RISK PIPELINE
# ============================================================

st.markdown(
    '<div class="rule"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="smallcaps">RISK PIPELINE</div>',
    unsafe_allow_html=True
)

st.markdown("## How Risk Assessment Fits the System")


steps = [
    (
        "01",
        "Detection Evidence",
        "Isolation Forest identifies suspicious network flows."
    ),
    (
        "02",
        "Correlated Events",
        "Suspicious flows are grouped into meaningful attack events."
    ),
    (
        "03",
        "Attack Graph",
        "Relationships between hosts and attack activity are reconstructed."
    ),
    (
        "04",
        "Risk Assessment",
        "Evidence is combined to support an incident-level risk assessment."
    ),
]


for number, title, description in steps:

    step_html = (
        '<div class="step-row">'
        f'<div class="step-number">{number}</div>'
        '<div>'
        f'<div class="step-title">{title}</div>'
        f'<div class="desc" style="margin-top:5px;">{description}</div>'
        '</div>'
        '</div>'
    )

    st.markdown(
        step_html,
        unsafe_allow_html=True
    )


# ============================================================
# BACKEND STATUS
# ============================================================

st.markdown(
    '<div class="rule"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="callout">'
    '<b>Backend connection:</b> '
    'The risk assessment interface is prepared for the finalized '
    'correlation, attack graph and risk outputs. The values currently '
    'displayed are prototype UI values and are not being presented as '
    'final model calculations.'
    '</div>',
    unsafe_allow_html=True
)