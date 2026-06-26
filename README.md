# 🤖 Agentic AI System

A modern Streamlit-based Multi-Agent AI Research Assistant featuring autonomous planning, execution, workflow visualization, live logs, and PDF report generation.

## Features

- Multi-Agent Planning
- Live Execution Dashboard
- Workflow Graph
- PDF Reports
- Responsive UI
- Failure Simulation

## Run

```bash
pip install -r requirements.txt
streamlit run app.py

## Project structure

agentic-ai-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│   ├── style.css
│   └── logo.png
│
├── components/
│   ├── header.py
│   ├── sidebar.py
│   ├── metrics.py
│   ├── workflow.py
│   ├── report.py
│   └── logs.py
│
├── agents/
├── orchestrator/
├── utils/
├── reports/
│
├── docs/
│   ├── System_Design.md
│   └── Post_Mortem.md
│
└── demo/
    └── demo_script.md
