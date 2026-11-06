# Agentic Cybersecurity Incident Detection and Investigation Using Anomaly Detection and Attack Graphs

An intelligent cybersecurity monitoring and investigation system that combines **Machine Learning, Attack Graph Analysis, Risk Assessment, and Agentic AI** to identify suspicious network activity, correlate related events, assess potential threats, and assist in security incident investigation.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Project Objectives](#project-objectives)
- [System Architecture](#system-architecture)
- [Key Features](#key-features)
- [Methodology](#methodology)
  - [1. Dataset Preprocessing](#1-dataset-preprocessing)
  - [2. Anomaly Detection](#2-anomaly-detection)
  - [3. Attack Event Generation](#3-attack-event-generation)
  - [4. Attack Graph Construction](#4-attack-graph-construction)
  - [5. Risk Assessment](#5-risk-assessment)
  - [6. Agentic AI Investigation](#6-agentic-ai-investigation)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [Evaluation and Performance](#evaluation-and-performance)
- [Future Scope](#future-scope)
- [Limitations](#limitations)

---

## Overview

Modern networks generate large volumes of traffic, making it difficult for security teams to manually identify suspicious activities and understand how individual security events may be connected. Traditional intrusion detection approaches often focus on identifying malicious traffic at the individual flow level. However, detecting suspicious activity is only the first step. Security analysts also need to understand the relationships between events, assess their potential impact, and investigate the underlying evidence.

This project presents an integrated cybersecurity investigation framework that addresses these challenges through multiple stages:

- **Anomaly Detection:** Uses Isolation Forest to identify potentially suspicious network traffic.
- **Attack Event Correlation:** Groups related suspicious network flows into meaningful attack events.
- **Attack Graph Construction:** Represents relationships between hosts, events, and attack categories through a graph-based structure.
- **Risk Assessment:** Evaluates and prioritizes suspicious events based on their associated risk.
- **Agentic AI Investigation:** Uses a LangGraph-based AI agent with specialized investigation tools to retrieve evidence, analyze incidents, and generate structured investigation reports.

The system provides an interactive Streamlit dashboard through which users can explore detected anomalies, investigate incidents, visualize attack relationships, assess risks, and interact with the AI investigation workflow. The overall objective is to move beyond isolated anomaly detection towards a more structured and investigation-oriented Security Operations Center (SOC) workflow.

---

## Problem Statement

Existing network intrusion detection systems can identify suspicious traffic but often provide limited support for understanding the broader context of security incidents.

Some of the major challenges include:

- Large volumes of network traffic make manual monitoring difficult.
- Individual suspicious flows do not always provide enough context to understand an attack.
- Relationships between different suspicious events are difficult to identify.
- Security analysts need to manually correlate evidence from multiple sources.
- Prioritizing incidents based on their potential severity can be challenging.
- Investigation processes often require significant time and domain expertise.

The proposed system addresses these challenges by integrating machine learning-based anomaly detection, graph-based event correlation, risk assessment, and tool-using AI investigation into a unified framework.

---

## Project Objectives

The primary objectives of the project are:

1. Develop an anomaly detection pipeline capable of identifying suspicious network traffic using an unsupervised machine learning approach.
2. Convert suspicious network flows into structured attack events by correlating related records.
3. Construct an attack graph to represent relationships between hosts, attack events, and attack categories.
4. Develop a risk assessment mechanism to support incident prioritization.
5. Implement an agentic AI investigation workflow that can retrieve relevant evidence and perform structured incident analysis using specialized tools.
6. Build an interactive dashboard to provide visibility into the detection, analysis, and investigation processes.
7. Establish a foundation for an intelligent and adaptive SOC investigation framework.

---

## System Architecture

The system follows a multi-stage architecture in which the output of one stage serves as the input to subsequent stages.

### High-Level Workflow

```text
              CICIDS2017 Dataset
                      |
                      v
              Data Preprocessing
                      |
                      v
              Cleaned Network Flows
                      |
                      v
              Isolation Forest
              Anomaly Detection
                      |
                      v
              Suspicious Network Flows
                      |
                      v
              Attack Event Generation
                      |
                      v
              Attack Graph Construction
                      |
                      v
                Risk Assessment
                      |
                      v
              Agentic AI Investigation
                      |
                      v
          Evidence-Based Investigation
                 and Analysis
                      |
                      v
             Streamlit Dashboard
```

The dashboard provides separate interfaces for exploring the outputs of the different stages, including anomaly detection, incident investigation, attack graph visualization, risk assessment, and AI-assisted investigation.

### Architectural Components

| Component | Responsibility |
|---|---|
| Data Processing | Cleans and prepares network traffic records for analysis. |
| Anomaly Detection | Identifies potentially suspicious network flows using Isolation Forest. |
| Event Builder | Groups related suspicious flows into attack events. |
| Graph Builder | Constructs a graph representing relationships between hosts and attack events. |
| Risk Analyzer | Calculates risk scores and supports incident prioritization. |
| AI Agent | Orchestrates investigation tasks through a structured LangGraph workflow. |
| Investigation Tools | Retrieve flow evidence and relevant event and graph information. |
| Streamlit Dashboard | Provides an interactive interface for detection, analysis, and investigation. |

---

## Key Features

### 1. Machine Learning-Based Anomaly Detection

- Unsupervised anomaly detection using Isolation Forest.
- Identification of suspicious network flows.
- Analysis of anomaly scores and model evaluation metrics.
- Comparison of detected anomalies against available dataset labels for evaluation.

### 2. Attack Event Correlation

- Groups related suspicious network flows into meaningful events.
- Uses network attributes and time-based grouping.
- Preserves relevant metadata for further investigation.
- Generates structured attack event records.

### 3. Interactive Attack Graph

- Graph-based representation of network activity.
- Visualizes relationships between source hosts, attack events, attack categories, and target hosts.
- Represents connections such as initiation, classification, targeting, and temporal relationships.
- Helps explore how suspicious activities are connected.

### 4. Risk Assessment and Incident Prioritization

- Computes risk scores for identified attack events.
- Combines relevant anomaly and event information to support prioritization.
- Provides an overview of suspicious events and their relative risk.
- Helps focus investigation efforts on potentially important incidents.

### 5. Agentic AI Investigation

- LangGraph-based agent orchestration.
- Specialized tools for retrieving network flow evidence and investigation context.
- Structured investigation workflow.
- Context-based analysis of suspicious events.
- Generation of investigation records and findings.

### 6. Interactive Security Dashboard

- Multi-page Streamlit application.
- Detection metrics and suspicious flow analysis.
- Incident-level investigation.
- Interactive attack graph visualization.
- Risk assessment interface.
- AI-assisted incident investigation.

---

## Methodology

### 1. Dataset Preprocessing

The project uses the **CICIDS2017 dataset**, a publicly available network intrusion detection dataset containing benign and malicious network traffic. The dataset contains network flow records with features describing different characteristics of network communication. The preprocessing stage prepares the raw data for machine learning and subsequent investigation stages.

Key preprocessing activities include:
- Handling missing and invalid values.
- Removing unsuitable or redundant columns.
- Preparing numerical features for model training.
- Cleaning and standardizing the dataset.
- Preserving relevant network metadata for subsequent analysis.

The processed dataset is stored in Parquet format for efficient access.

**Processed Dataset:**
- Records: Approximately 2.23 million
- Features: 69 network features
- Target: 1 label column
- Format: Parquet

**NOTE:** The datasets can be found in the GitHub Releases section of this repo.

### 2. Anomaly Detection

The anomaly detection component uses **Isolation Forest**, an unsupervised machine learning algorithm designed to identify observations that differ significantly from normal data patterns. Unlike supervised classification algorithms, Isolation Forest does not require malicious traffic labels during model training. The model identifies anomalies by isolating observations through randomly constructed decision trees. Observations that require fewer splits to become isolated are generally considered more anomalous.

#### Why Isolation Forest?
- Suitable for unsupervised anomaly detection.
- Effective for identifying unusual patterns in large datasets.
- Does not require labelled attack examples during training.
- Can identify previously unseen or unusual traffic patterns based on learned normal behaviour.

#### Detection Process
1. Prepare the cleaned network flow features.
2. Train the Isolation Forest model primarily on benign traffic.
3. Generate anomaly scores for network flow records.
4. Apply the selected decision threshold to classify observations.
5. Extract suspicious flows for subsequent analysis.

The model produces two types of predictions:
- `1`: Normal observation
- `-1`: Anomalous observation

The anomaly scores and predictions are subsequently used in the attack event generation and risk assessment stages.
Ground-truth dataset labels are retained separately for evaluating the model's detection performance.

### 3. Attack Event Generation

Individual suspicious network flows may not provide sufficient information to understand the context of an incident.
To address this, the project introduces an attack event generation stage that groups related suspicious flows into higher-level events.

The grouping process considers relevant network attributes, including:
- Source IP address
- Destination IP address
- Network protocol
- Attack label
- Time window

A 60-second time window is used to group related suspicious activity. This transforms individual flow-level detections into structured attack events that can be analyzed more effectively.

The generated attack events are stored in: `outputs/attack_events.csv`

### 4. Attack Graph Construction

The attack graph provides a structured representation of the relationships between different network entities and suspicious events.
The graph is constructed using **NetworkX**.

#### Graph Components

The graph contains different types of nodes:

| Node Type | Description |
|---|---|
| Source Host | Represents the originating network host. |
| Attack Event | Represents a correlated suspicious event. |
| Attack Type | Represents the associated attack category. |
| Target Host | Represents the destination network host. |

#### Graph Relationships
The graph represents relationships through different types of edges:

| Relationship | Description |
|---|---|
| Initiates | Connects a source host to an attack event. |
| Classified As | Connects an attack event to its attack category. |
| Targets | Connects an attack event to a target host. |
| Precedes | Represents temporal relationships between events. |

These relationships allow the system to represent suspicious network activity as a connected structure instead of treating every event independently.
The generated graph is exported in GEXF format, allowing it to be stored and further explored using compatible graph visualization tools.

**Graph Output:** `outputs/attack_graph.gexf`

### 5. Risk Assessment

The risk assessment module evaluates suspicious attack events and helps prioritize them for further investigation. Instead of considering anomaly detection as the only indicator of threat severity, this stage uses event-level information to derive risk scores. The risk analysis considers relevant information associated with detected events, including anomaly-related scores and available event characteristics. The generated scores help distinguish between events that may require greater investigative attention and those with comparatively lower risk.

**Output:** `outputs/event_risk_scores.csv`

The risk assessment module also provides an interactive interface for exploring event-level risk information.

### 6. Agentic AI Investigation

The agentic investigation component introduces an AI-powered investigation workflow to assist in understanding suspicious security incidents.
It is implemented using **LangGraph**, which provides a structured way to orchestrate an agent's execution through defined states, workflow nodes, and transitions.
Rather than relying on a single LLM prompt to interpret an entire incident, the system uses specialized investigation tools to retrieve relevant information and support evidence-based analysis.

#### Agent Architecture

The investigation agent consists of three major components:

**1. State Management**
A shared state maintains the information required throughout the investigation workflow, allowing different stages of the agent to access and update relevant investigation context.

**2. Workflow Orchestration**
LangGraph manages the execution flow of the investigation process.
It coordinates the interaction between the agent, available tools, and subsequent investigation stages.

**3. Investigation Tools**
Specialized tools allow the agent to retrieve information from the project's existing outputs and data sources.
These tools provide access to relevant investigation evidence, including individual network flow records and event-related information.

#### Investigation Process

The general investigation workflow follows these stages:

1. Receive an incident or attack event for investigation.
2. Initialize the investigation state with the relevant context.
3. Identify the information required for further analysis.
4. Invoke appropriate investigation tools to retrieve supporting evidence.
5. Analyze the retrieved information using the AI model.
6. Produce structured investigation findings.
7. Save the generated investigation output for future reference.

The tool-based approach enables the agent to work with actual network evidence rather than depending entirely on information supplied in a prompt.

#### Role of Agentic AI

The primary purpose of this component is to assist with incident investigation by combining language-model reasoning with access to specialized tools.
The agent helps organize the investigation process, retrieve relevant evidence, and generate understandable findings that can support security analysis.
It acts as an investigation assistant rather than an automated replacement for a human security analyst.

---

## Technology Stack

The project combines machine learning, graph analysis, AI orchestration, and application development technologies.

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and preprocessing |
| NumPy | Numerical operations |
| Scikit-learn | Isolation Forest and model evaluation |
| PyArrow | Parquet dataset handling |
| NetworkX | Attack graph construction and analysis |
| LangChain | LLM integration and tool development |
| LangGraph | Agent workflow orchestration and state management |
| Streamlit | Interactive multi-page dashboard |
| Plotly | Interactive data visualization |
| Python-dotenv | Environment variable management |
| Jupyter Notebook | Data preprocessing and model experimentation |
| GEXF | Attack graph export format |

**Note:** The LLM provider and its corresponding model are configured through the project's environment variables. (template in .env.example)

---

## Project Structure

```text
major/
│
├── .streamlit/
│   └── config.toml
│
├── agent/
│   ├── agent.py
│   ├── state.py
│   ├── workflow.py
│   └── tools/
│       └── [Investigation tool modules]
│
├── attack_graph/
│   ├── __init__.py
│   ├── event_builder.py
│   ├── graph_builder.py
│   └── if_attack_graph_pipeline.py
│
├── agentic_investigation_output/
│
├── data/
│   └── cleaned_cicids2017.parquet
│
├── notebooks/
│   ├── dataset_preprocessing.ipynb
│   └── isolation_forest.ipynb
│
├── outputs/
│   ├── agentic_investigation_output/
│   ├── attack_events.csv
│   ├── attack_graph.gexf
│   ├── event_risk_scores.csv
│   └── suspicious_flows_with_metadata.csv
│
├── pages/
│   ├── attack_detection.py
│   ├── attack_graph.py
│   ├── incident_investigation.py
│   └── risk_assessment.py
│
├── .env.example
├── .gitattributes
├── .gitignore
├── agentic.py
├── app.py
├── instructions.txt
├── README.md
├── requirements.txt
├── risk_analyzer.py
└── test_agent.py
```

## Installation and Setup

Follow the steps below to set up the project locally.

### 1. Clone the Repository

```bash
git clone [<repository-url>](https://github.com/ShireenKachroo/CyberSentinel.git)
```

Navigate to the project directory:

```bash
cd major
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file using the provided template:

```bash
cp .env.example .env
```

For Windows Command Prompt:

```cmd
copy .env.example .env
```

Add the required API credentials and configuration values to the `.env` file.

### 5. Prepare the Dataset and Outputs

Ensure that the required preprocessed dataset is available at:

```text
data/cleaned_cicids2017.parquet
```

---

## Running the Application

### Launch the Streamlit Dashboard

From the project's root directory, execute:

```bash
streamlit run app.py
```

The dashboard will be accessible through the local URL displayed in the terminal.


### Run Agent Tests

To execute the agent component testing script:

```bash
python test_agent.py
```

---

## Dashboard Modules

The Streamlit application provides multiple interfaces for exploring different stages of the cybersecurity investigation pipeline.

| Module | Functionality |
|---|---|
| Attack Detection | Displays anomaly detection results, evaluation metrics, and suspicious traffic information. |
| Incident Investigation | Provides event-level information and details about detected incidents. |
| Attack Graph | Visualizes the relationships between network hosts, attack events, and attack categories. |
| Risk Assessment | Displays calculated risk scores and supports incident prioritization. |
| AI Investigation & Risk Analysis | Provides an interface for interacting with the agentic investigation workflow. |

Together, these modules provide a unified view of the detection and investigation process.

---

## Evaluation and Performance

The Isolation Forest model is evaluated using the available ground-truth labels in the CICIDS2017 dataset. Although the model is trained using an unsupervised approach, labelled observations can be used after prediction to compare the detected anomalies against known attack and benign records.

The following evaluation metrics are used:

- **Accuracy:** Measures the proportion of correctly classified observations.
- **Precision:** Measures how many observations identified as attacks are actually attacks.
- **Recall:** Measures how many actual attacks are successfully detected.
- **F1-Score:** Provides a balance between precision and recall.
- **ROC-AUC:** Evaluates the model's ability to distinguish between normal and anomalous observations across different thresholds.
- **PR-AUC:** Measures the precision-recall trade-off, particularly useful when dealing with imbalanced datasets.

### Reported Model Results

| Evaluation Metric | Score |
|---|---:|
| Accuracy | 0.8966 |
| Precision | 0.6386 |
| Recall | 0.7250 |
| F1-Score | 0.6791 |
| ROC-AUC | 0.8862 |
| PR-AUC | 0.6801 |

These results provide an initial evaluation of the anomaly detection component.

The overall system also produces event-level outputs, graph representations, risk scores, and AI-generated investigation records to support subsequent stages of security analysis.

---

## UI Overview
<img width="1917" height="750" alt="image" src="https://github.com/user-attachments/assets/a9c7d6f8-870a-4898-b234-8e99dfe5ef8b" />
<img width="1917" height="795" alt="image" src="https://github.com/user-attachments/assets/6e8f6557-2765-4c5d-9dd5-a4dc32dcd00d" />
<img width="1917" height="695" alt="image" src="https://github.com/user-attachments/assets/6a6119f4-2f7a-4873-8294-8031b98c68bf" />
<img width="1916" height="662" alt="image" src="https://github.com/user-attachments/assets/a501e198-d1ff-4c99-b202-e7455067e060" />
<img width="1856" height="811" alt="image" src="https://github.com/user-attachments/assets/f0b1541a-35c5-41b6-9063-a13e329742af" />
<img width="1143" height="821" alt="image" src="https://github.com/user-attachments/assets/0a14b39a-07e8-492c-a3f9-cca26aebcd2c" />
<img width="1917" height="786" alt="image" src="https://github.com/user-attachments/assets/6f21c8ab-d88b-4ccf-889e-d0bf85dd6f44" />
<img width="1912" height="717" alt="image" src="https://github.com/user-attachments/assets/72e5c65f-722d-4a48-94f5-8fae7038cc57" />
<img width="1912" height="717" alt="image" src="https://github.com/user-attachments/assets/3f5ebdf1-1f4b-49de-8875-a6b59f4d6af9" />

---

## Future Scope

The current implementation establishes a foundation for an integrated, AI-assisted cybersecurity investigation framework. Several improvements can be explored to make the system more capable and closer to a practical SOC environment.

### 1. Adaptive Security Operations Center (SOC)

Extend the system towards an adaptive SOC framework that can continuously monitor incoming network traffic, identify suspicious behaviour, and update its investigation context as new events emerge.

### 2. Real-Time Network Traffic Monitoring

Integrate live network traffic sources to enable continuous anomaly detection instead of relying exclusively on preprocessed datasets.

### 3. Advanced Attack Graph Analysis

Introduce more advanced graph algorithms and temporal analysis to identify complex attack patterns, multi-stage attacks, and relationships across larger incident sequences.

### 4. Enhanced Agentic Investigation

Extend the investigation agent with additional specialized tools and more advanced reasoning workflows.

Potential improvements include:

- Multi-step investigation planning.
- Investigation across multiple related incidents.
- Better evidence correlation.
- Confidence and uncertainty reporting.
- More comprehensive investigation summaries.

### 5. Automated Threat Intelligence Integration

Integrate external threat intelligence sources to enrich suspicious IP addresses, domains, and other network indicators with additional security context.

### 6. Feedback-Driven Detection

Introduce analyst feedback into the detection pipeline to improve anomaly identification, reduce false positives, and support adaptive model updates.

### 7. SOC Workflow Integration

Explore integration with SIEM platforms, alert management systems, and incident response tools to support more complete security investigation workflows.

### 8. Explainable AI

Improve the explainability of anomaly detection and investigation results by providing clearer reasons behind model predictions, risk scores, and AI-generated conclusions.

---

## Limitations

The current implementation has certain limitations that provide opportunities for future improvement:

- The system currently uses a preprocessed CICIDS2017 dataset rather than continuous live network traffic.
- Isolation Forest identifies unusual traffic patterns but does not independently establish whether an observation represents a confirmed attack.
- Attack event grouping depends on the selected network attributes and time-window configuration.
- Risk scores are intended to support prioritization and should not be treated as definitive measures of real-world threat severity.
- AI-generated investigation findings depend on the quality of the retrieved evidence and the underlying language model.
- The investigation workflow is designed to assist analysts and does not independently perform production-level incident containment or remediation.

---

*This project is developed for academic and research purposes. Its outputs are intended to assist security analysis and should not be considered a replacement for professional security monitoring and incident response systems.*
