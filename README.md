# 🤖 Agentic AI Multi-Agent Research Assistant

A powerful multi-agent AI research assistant that autonomously plans research tasks, retrieves information from the web, analyzes findings using an LLM, and generates professional PDF reports through an orchestrated AI workflow.

**🔬 Autonomous Research • 🤖 Multi-Agent Orchestration • 📄 Intelligent Report Generation**

---

# 🌟 Features

* 🤖 **Multi-Agent Architecture**

  * Planner Agent
  * Retriever Agent
  * Analyzer Agent
  * Writer Agent

* 🌐 **Automated Web Research**

  * Retrieves relevant information using the Tavily Search API.

* 🧠 **LLM-Based Analysis**

  * Summarizes and analyzes retrieved content using a local Ollama model.

* 📝 **Professional Report Generation**

  * Produces structured research reports with recommendations.

* 📄 **PDF Export**

  * Automatically generates downloadable PDF reports.

* 📊 **Interactive Streamlit Dashboard**

  * Modern UI with workflow visualization.
  * Live execution status.
  * Research planning.
  * Agent logs.
  * Failure simulation.

* ⚡ **Batch Processing**

  * Executes retrieval tasks concurrently for improved performance.

* 🔄 **Failure Simulation**

  * Test workflow resilience using simulated retrieval failures.

---

# 🏗️ Architecture

```
                 ┌────────────────────────────┐
                 │      Streamlit UI          │
                 │         app.py             │
                 └─────────────┬──────────────┘
                               │
                     User Research Query
                               │
                               ▼
                 ┌────────────────────────────┐
                 │      Planner Agent         │
                 │      planner.py            │
                 └─────────────┬──────────────┘
                               │
                     Research Plan (Tasks)
                               │
                               ▼
                 ┌────────────────────────────┐
                 │        Executor            │
                 │      executor.py           │
                 └─────────────┬──────────────┘
                               │
                Batch Retrieval Execution
                               │
          ┌────────────────────┴───────────────────┐
          ▼                                        ▼
┌─────────────────────┐                 ┌─────────────────────┐
│ Retriever Agent     │                 │ Batch Processing    │
│ retriever.py        │                 │ batching.py         │
└──────────┬──────────┘                 └─────────────────────┘
           │
     Tavily Search API
           │
           ▼
 Retrieved Web Results
           │
           ▼
┌─────────────────────┐
│ Analyzer Agent      │
│ analyzer.py         │
└──────────┬──────────┘
           │
     LLM Analysis
           │
           ▼
┌─────────────────────┐
│ Writer Agent        │
│ writer.py           │
└──────────┬──────────┘
           │
 Professional Report
           │
           ▼
 PDF Generator
```

---

# 🤖 Agent Responsibilities

## 🧩 Planner Agent

* Breaks complex research queries into multiple executable tasks.
* Creates a structured workflow for downstream agents.

---

## 🌐 Retriever Agent

* Searches the web using Tavily API.
* Retrieves relevant information.
* Supports simulated failures for testing.

---

## 🧠 Analyzer Agent

* Uses the configured Ollama LLM.
* Summarizes retrieved information.
* Produces concise analytical insights.

---

## ✍️ Writer Agent

* Generates a professional report.
* Adds recommendations.
* Structures findings into readable sections.

---

## ⚙️ Executor

* Coordinates the complete workflow.
* Executes retrieval in batches.
* Handles orchestration between agents.
* Maintains execution logs.

---

# 🛠️ Technologies Used

| Technology    | Purpose                |
| ------------- | ---------------------- |
| Python        | Backend                |
| Streamlit     | User Interface         |
| Ollama        | Local LLM              |
| Tavily API    | Web Search             |
| Graphviz      | Workflow Visualization |
| ReportLab     | PDF Generation         |
| Asyncio       | Concurrent Execution   |
| Python-dotenv | Environment Variables  |

---

# 📋 Prerequisites

* Python 3.10+
* Ollama installed locally
* Tavily API Key
* Graphviz installed

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/vjsai5/agentic-ai-multi-agent-AI-system.git

cd agentic-ai-multi-agent-research-assistant
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file

```
TAVILY_API_KEY=your_api_key

MODEL_NAME=gemma4
```

---

# 💡 Usage

Run the Streamlit dashboard

```bash
streamlit run app.py
```

Open

```
http://localhost:8501
```

---

# 📁 Project Structure

```
.
├── app.py
├── requirements.txt
├── reports/
│
├── agents/
│   ├── planner.py
│   ├── retriever.py
│   ├── analyzer.py
│   └── writer.py
│
├── orchestrator/
│   ├── executor.py
│   ├── batching.py
│   └── retry.py
│
└── utils/
    ├── graph.py
    ├── llm.py
    ├── logger.py
    └── pdf_generator.py
```

---

# 🔄 Workflow

1. User enters a research topic.
2. Planner Agent generates a task plan.
3. Executor batches retrieval tasks.
4. Retriever Agent searches the web.
5. Analyzer Agent summarizes findings.
6. Writer Agent creates a professional report.
7. PDF report is generated.
8. Execution logs and workflow graph are displayed.

---

# 📊 Example Output

The generated report contains:

* Executive Summary
* Research Findings
* Analysis
* Recommendations
* Conclusion

The application also provides:

* Workflow graph
* Live execution status
* Agent logs
* Downloadable PDF report

---

# 🧪 Failure Simulation

Enable **"Simulate Retrieval Failure"** from the sidebar to test:

* Retrieval failures
* Exception handling
* Workflow robustness
* Error reporting

---

# 🚀 Future Improvements

* LangGraph integration
* Memory-enabled agents
* Multi-LLM support
* Vector database integration
* Human-in-the-loop approvals
* Parallel agent execution
* Citation generation
* RAG-based document research

---


---



# 🙏 Acknowledgements

* Streamlit
* Ollama
* Tavily Search API
* Graphviz
* ReportLab

---

# 📧 Contact

For questions, suggestions, or improvements, open an issue in this repository.

---

⭐ If you found this project useful, consider giving it a star on GitHub!
