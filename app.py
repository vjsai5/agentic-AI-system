import asyncio
import html
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from agents.planner import PlannerAgent
from orchestrator.executor import Executor
from utils.graph import build_graph
from utils.logger import logs
from utils.pdf_generator import create_pdf


load_dotenv()

REPORT_PATH = Path("reports") / "report.pdf"
TASK_STYLES = {
    "retrieval": ("Research", "#2f80ed"),
    "analysis": ("Analysis", "#8a5cf6"),
    "writing": ("Writing", "#0f9f6e"),
}
EXAMPLE_PROMPTS = [
    "Analyze the business impact of AI agents in customer support",
    "Research latest renewable energy storage trends for startups",
    "Compare cloud cost optimization strategies for SaaS companies",
]


st.set_page_config(
    page_title="Agentic AI System",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles():
    st.markdown(
        """
        <style>
            :root {
                --surface: #ffffff;
                --surface-soft: #f6f8fb;
                --ink: #172033;
                --muted: #64748b;
                --line: #dbe3ef;
                --accent: #2563eb;
                --accent-soft: #eaf1ff;
                --success: #0f9f6e;
                --warning: #b45309;
            }

            .block-container {
                padding-top: 1.4rem;
                padding-bottom: 2rem;
                max-width: 1320px;
            }

            div[data-testid="stSidebar"] {
                background: #f8fafc;
                border-right: 1px solid var(--line);
            }

            h1, h2, h3 {
                letter-spacing: 0;
                color: var(--ink);
            }

            .hero {
                border: 1px solid var(--line);
                background: linear-gradient(135deg, #ffffff 0%, #f4f8ff 52%, #f7fbf8 100%);
                border-radius: 8px;
                padding: 1.35rem 1.45rem;
                margin-bottom: 1rem;
            }

            .hero-title {
                font-size: clamp(1.8rem, 3vw, 3rem);
                font-weight: 760;
                line-height: 1.05;
                margin: 0 0 .45rem 0;
                color: #0f172a;
            }

            .hero-copy {
                color: var(--muted);
                font-size: 1rem;
                line-height: 1.55;
                max-width: 820px;
                margin: 0;
            }

            .metric-card {
                border: 1px solid var(--line);
                border-radius: 8px;
                padding: .9rem 1rem;
                background: var(--surface);
                min-height: 92px;
            }

            .metric-label {
                color: var(--muted);
                font-size: .78rem;
                text-transform: uppercase;
                letter-spacing: .04em;
                margin-bottom: .3rem;
            }

            .metric-value {
                color: var(--ink);
                font-size: 1.45rem;
                font-weight: 730;
                line-height: 1.2;
            }

            .panel {
                border: 1px solid var(--line);
                border-radius: 8px;
                background: var(--surface);
                padding: 1rem;
                margin-bottom: 1rem;
            }

            .panel-title {
                color: var(--ink);
                font-size: 1rem;
                font-weight: 730;
                margin-bottom: .7rem;
            }

            .task-row {
                display: grid;
                grid-template-columns: 42px minmax(0, 1fr) auto;
                gap: .75rem;
                align-items: start;
                border: 1px solid var(--line);
                border-radius: 8px;
                padding: .75rem;
                margin-bottom: .55rem;
                background: #fbfdff;
            }

            .task-index {
                width: 34px;
                height: 34px;
                border-radius: 8px;
                display: grid;
                place-items: center;
                font-weight: 760;
                color: #ffffff;
                background: var(--accent);
            }

            .task-title {
                color: var(--ink);
                font-weight: 700;
                margin-bottom: .18rem;
            }

            .task-desc {
                color: var(--muted);
                line-height: 1.4;
                overflow-wrap: anywhere;
            }

            .pill {
                border-radius: 999px;
                padding: .22rem .55rem;
                background: var(--accent-soft);
                color: #1d4ed8;
                font-size: .75rem;
                font-weight: 700;
                white-space: nowrap;
            }

            .step {
                border-left: 3px solid var(--accent);
                padding: .35rem .65rem;
                margin-bottom: .45rem;
                background: #f8fbff;
                border-radius: 0 8px 8px 0;
                color: var(--ink);
            }

            .empty-state {
                border: 1px dashed #b6c3d5;
                border-radius: 8px;
                padding: 1.2rem;
                color: var(--muted);
                background: #fbfdff;
                line-height: 1.55;
            }

            .log-line {
                border-bottom: 1px solid #e8eef6;
                padding: .42rem 0;
                color: var(--ink);
                overflow-wrap: anywhere;
            }

            .stTextArea textarea {
                border-radius: 8px;
            }

            .stButton > button,
            .stDownloadButton > button {
                border-radius: 8px;
                min-height: 2.65rem;
                font-weight: 720;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def ensure_state():
    defaults = {
        "query": "",
        "plan": [],
        "report": "",
        "duration": None,
        "status_events": [],
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def render_metric(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    st.markdown(
        """
        <section class="hero">
            <div class="hero-title">Agentic AI System for Multi-step tasks</div>
            <p class="hero-copy">
                Turn a complex research question into a planned multi-agent workflow,
                tracked execution, and a polished downloadable report.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        st.header("Workspace")
        fail = st.toggle(
            "Simulate retrieval failure",
            value=False,
            help="Useful for testing fallback and error paths.",
        )
        show_graph = st.toggle("Show workflow graph", value=True)
        show_logs = st.toggle("Show agent logs", value=True)

        st.divider()
        st.caption("Example prompts")
        selected = st.selectbox("Load an example", ["Custom prompt"] + EXAMPLE_PROMPTS)
        if selected != "Custom prompt" and st.button("Use selected prompt", use_container_width=True):
            st.session_state.query = selected
            st.rerun()

        st.divider()
        if st.button("Reset workspace", use_container_width=True):
            logs.clear()
            st.session_state.plan = []
            st.session_state.report = ""
            st.session_state.duration = None
            st.session_state.status_events = []
            st.rerun()

    return fail, show_graph, show_logs


def render_plan(plan):
    st.markdown('<div class="panel"><div class="panel-title">Execution Plan</div>', unsafe_allow_html=True)
    if not plan:
        st.markdown(
            '<div class="empty-state">Enter a task and click Run Research to generate the agent plan.</div>',
            unsafe_allow_html=True,
        )
    else:
        for task in plan:
            label, color = TASK_STYLES.get(task.task_type, (task.task_type.title(), "#2563eb"))
            safe_label = html.escape(label)
            safe_description = html.escape(task.description)
            safe_type = html.escape(task.task_type)
            st.markdown(
                f"""
                <div class="task-row">
                    <div class="task-index" style="background:{color};">{task.id}</div>
                    <div>
                        <div class="task-title">{safe_label}</div>
                        <div class="task-desc">{safe_description}</div>
                    </div>
                    <div class="pill">{safe_type}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)


def render_status(events):
    if not events:
        st.markdown(
            '<div class="empty-state">Live progress will appear here while the agents are running.</div>',
            unsafe_allow_html=True,
        )
        return

    for event in events:
        st.markdown(f'<div class="step">{html.escape(event)}</div>', unsafe_allow_html=True)


def render_logs():
    if not logs:
        st.markdown('<div class="empty-state">No agent logs yet.</div>', unsafe_allow_html=True)
        return

    for entry in logs[-12:]:
        st.markdown(f'<div class="log-line">{html.escape(entry)}</div>', unsafe_allow_html=True)


async def run_workflow(plan, fail, status_slot):
    status_events = []

    def stream(message):
        status_events.append(message)
        st.session_state.status_events = status_events
        with status_slot.container():
            render_status(status_events)

    return await Executor(fail).execute(plan, stream)


def main():
    inject_styles()
    ensure_state()
    fail, show_graph, show_logs = render_sidebar()
    render_header()

    metric_cols = st.columns(4)
    with metric_cols[0]:
        render_metric("Agents", "4")
    with metric_cols[1]:
        render_metric("Retrieval batches", "2 max")
    with metric_cols[2]:
        render_metric("Report", "PDF ready" if st.session_state.report else "Pending")
    with metric_cols[3]:
        elapsed = f"{st.session_state.duration:.1f}s" if st.session_state.duration else "Not run"
        render_metric("Last runtime", elapsed)

    input_col, workflow_col = st.columns([1.05, .95], gap="large")

    with input_col:
        with st.form("research_form", clear_on_submit=False):
            query = st.text_area(
                "Research task",
                key="query",
                height=155,
                placeholder="Example: Analyze latest AI agent adoption trends for enterprise support teams",
            )
            submit = st.form_submit_button("Run Research", type="primary", use_container_width=True)

        if submit:
            clean_query = query.strip()
            if not clean_query:
                st.warning("Add a research task before running the workflow.")
            else:
                logs.clear()
                st.session_state.report = ""
                st.session_state.duration = None
                st.session_state.status_events = []
                st.session_state.plan = PlannerAgent().create_plan(clean_query)

                start = time.perf_counter()
                status_slot = st.empty()
                with st.spinner("Agents are working through the plan..."):
                    try:
                        st.session_state.report = asyncio.run(
                            run_workflow(st.session_state.plan, fail, status_slot)
                        )
                        st.session_state.duration = time.perf_counter() - start
                        st.success("Workflow completed. Report is ready.")
                    except Exception as exc:
                        st.session_state.duration = time.perf_counter() - start
                        st.error(f"Workflow stopped: {exc}")

        render_plan(st.session_state.plan)

    with workflow_col:
        if show_graph:
            st.markdown('<div class="panel"><div class="panel-title">Agent Workflow</div>', unsafe_allow_html=True)
            st.graphviz_chart(build_graph().source, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="panel"><div class="panel-title">Live Status</div>', unsafe_allow_html=True)
        render_status(st.session_state.status_events)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-title">Research Report</div>', unsafe_allow_html=True)
    if st.session_state.report:
        st.markdown(st.session_state.report)
        pdf_path = create_pdf(st.session_state.report, str(REPORT_PATH))
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                "Download PDF Report",
                pdf_file,
                "agentic_research_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    else:
        st.markdown(
            '<div class="empty-state">Your generated report will appear here after the agents finish.</div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    if show_logs:
        with st.expander("Agent logs", expanded=bool(logs)):
            render_logs()


if __name__ == "__main__":
    main()
