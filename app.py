import streamlit as st
import os
import json
import re
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ProjectIQ",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .main {
        background-color: #0e1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .hero {
        padding: 25px;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            #151b2d 0%,
            #111827 50%,
            #172033 100%
        );
        border: 1px solid #29344d;
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        color: #9ca3af;
        font-size: 16px;
    }

    .card {
        padding: 20px;
        border-radius: 16px;
        background: #151922;
        border: 1px solid #29303d;
        margin-bottom: 15px;
    }

    .project-title {
        font-size: 21px;
        font-weight: 700;
    }

    .muted {
        color: #9ca3af;
    }

    .big-number {
        font-size: 32px;
        font-weight: 800;
    }

    .status-badge {
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }

    .success-box {
        padding: 15px;
        border-radius: 12px;
        background: #123524;
        border: 1px solid #1d7047;
    }

    .warning-box {
        padding: 15px;
        border-radius: 12px;
        background: #3a2c0b;
        border: 1px solid #8a6b15;
    }

    .danger-box {
        padding: 15px;
        border-radius: 12px;
        background: #3a1519;
        border: 1px solid #8b2d35;
    }

    .ai-box {
        padding: 20px;
        border-radius: 16px;
        background: linear-gradient(
            135deg,
            #17152d,
            #151922
        );
        border: 1px solid #5b4bb7;
    }

    div[data-testid="stMetric"] {
        background-color: #151922;
        border: 1px solid #29303d;
        padding: 15px;
        border-radius: 14px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA
# ============================================================

projects = [
    {
        "id": 1,
        "name": "ABC Retail Implementation",
        "customer": "ABC Retail",
        "owners": ["Pranav Kale", "Rahul Sharma"],
        "status": "In Progress",
        "progress": 80,
        "last_update": "2 hours ago",
        "description": "Implementation and deployment of the retail management platform.",
        "milestones": [
            {
                "name": "Requirements",
                "status": "Done",
                "tasks": [
                    ("Collect requirements", "Done"),
                    ("Approve requirements", "Done")
                ]
            },
            {
                "name": "Development",
                "status": "In Progress",
                "tasks": [
                    ("Backend development", "Done"),
                    ("API integration", "Blocked"),
                    ("Testing", "Open")
                ]
            },
            {
                "name": "Deployment",
                "status": "Open",
                "tasks": [
                    ("Production setup", "Open"),
                    ("Final deployment", "Open")
                ]
            }
        ],
        "issues": [
            {
                "title": "API authentication failing",
                "category": "Bug",
                "status": "Open"
            },
            {
                "title": "Need additional dashboard filter",
                "category": "Feature Request",
                "status": "Open"
            }
        ],
        "updates": [
            (
                "10:30 AM",
                "API integration is blocked because client credentials are pending.",
                "Blocked"
            ),
            (
                "Yesterday",
                "Backend development has been completed successfully.",
                "Done"
            ),
            (
                "2 days ago",
                "Testing will begin after API integration.",
                "Open"
            )
        ]
    },

    {
        "id": 2,
        "name": "XYZ Logistics Integration",
        "customer": "XYZ Logistics",
        "owners": ["Sneha Patil"],
        "status": "Blocked",
        "progress": 55,
        "last_update": "8 days ago",
        "description": "Integration of logistics APIs with the customer platform.",
        "milestones": [
            {
                "name": "API Integration",
                "status": "Blocked",
                "tasks": [
                    ("API setup", "Done"),
                    ("Authentication", "Blocked"),
                    ("Integration testing", "Open")
                ]
            },
            {
                "name": "User Testing",
                "status": "Open",
                "tasks": [
                    ("Prepare test environment", "Open"),
                    ("Customer testing", "Open")
                ]
            }
        ],
        "issues": [
            {
                "title": "Authentication credentials missing",
                "category": "Implementation",
                "status": "Blocked"
            }
        ],
        "updates": [
            (
                "8 days ago",
                "Integration is blocked while waiting for authentication credentials.",
                "Blocked"
            )
        ]
    },

    {
        "id": 3,
        "name": "DEF Analytics Deployment",
        "customer": "DEF Analytics",
        "owners": ["Amit Shah"],
        "status": "Completed",
        "progress": 100,
        "last_update": "1 day ago",
        "description": "Deployment of analytics and reporting solution.",
        "milestones": [
            {
                "name": "Analytics Setup",
                "status": "Done",
                "tasks": [
                    ("Configure analytics", "Done"),
                    ("Connect data sources", "Done")
                ]
            },
            {
                "name": "Deployment",
                "status": "Done",
                "tasks": [
                    ("Production deployment", "Done"),
                    ("Customer handover", "Done")
                ]
            }
        ],
        "issues": [],
        "updates": [
            (
                "Yesterday",
                "Production deployment completed successfully.",
                "Done"
            )
        ]
    }
]


# ============================================================
# HELPERS
# ============================================================

def status_icon(status):
    status = status.lower()

    if status in ["done", "completed"]:
        return "🟢"

    if status in ["in progress", "open"]:
        return "🟡"

    if status in ["blocked"]:
        return "🔴"

    return "⚪"


def status_color(status):
    status = status.lower()

    if status in ["done", "completed"]:
        return "success-box"

    if status in ["blocked"]:
        return "danger-box"

    return "warning-box"


def get_statistics():

    total = len(projects)

    completed = len([
        p for p in projects
        if p["status"] == "Completed"
    ])

    blocked = len([
        p for p in projects
        if p["status"] == "Blocked"
    ])

    in_progress = len([
        p for p in projects
        if p["status"] == "In Progress"
    ])

    avg_progress = int(
        sum(p["progress"] for p in projects) / total
    )

    issues = sum(len(p["issues"]) for p in projects)

    return (
        total,
        completed,
        blocked,
        in_progress,
        avg_progress,
        issues
    )


# ============================================================
# AI
# ============================================================

def get_openai_client():

    try:

        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:

            try:
                api_key = st.secrets["OPENAI_API_KEY"]
            except Exception:
                api_key = None

        if not api_key:
            return None

        return OpenAI(api_key=api_key)

    except Exception:
        return None


def ai_analyze_update(update_text):

    client = get_openai_client()

    # --------------------------------------------------------
    # REAL AI
    # --------------------------------------------------------

    if client:

        prompt = f"""
You are an AI project management assistant.

Analyze this project update:

{update_text}

Return a concise project status analysis.

Identify:

1. Status: one of
   - BLOCKED
   - IN PROGRESS
   - COMPLETED
   - OPEN

2. Reason

3. Key action required

4. Risk level:
   - LOW
   - MEDIUM
   - HIGH

5. One-line project manager recommendation

Format exactly like:

STATUS: ...
REASON: ...
ACTION: ...
RISK: ...
RECOMMENDATION: ...
"""

        try:

            response = client.responses.create(
                model="gpt-5.6",
                input=prompt
            )

            return response.output_text

        except Exception as e:

            return f"""
STATUS: IN PROGRESS
REASON: AI service could not be reached.
ACTION: Review the update manually.
RISK: MEDIUM
RECOMMENDATION: Continue monitoring the project.

Technical note: {str(e)}
"""

    # --------------------------------------------------------
    # FALLBACK AI LOGIC
    # --------------------------------------------------------

    text = update_text.lower()

    if any(
        word in text
        for word in [
            "blocked",
            "waiting",
            "cannot start",
            "credentials",
            "dependency",
            "failed"
        ]
    ):

        status = "BLOCKED"
        risk = "HIGH"

    elif any(
        word in text
        for word in [
            "complete",
            "completed",
            "finished",
            "successfully deployed"
        ]
    ):

        status = "COMPLETED"
        risk = "LOW"

    else:

        status = "IN PROGRESS"
        risk = "MEDIUM"

    if "credential" in text:

        reason = "Waiting for client authentication credentials."

        action = "Follow up with the client and obtain credentials."

    elif "testing" in text:

        reason = "Testing activity is pending or underway."

        action = "Complete testing and record test results."

    elif "complete" in text or "completed" in text:

        reason = "The reported work has been completed."

        action = "Validate completion and move to the next milestone."

    else:

        reason = "Project work is currently progressing."

        action = "Continue execution and monitor for blockers."

    return f"""
STATUS: {status}
REASON: {reason}
ACTION: {action}
RISK: {risk}
RECOMMENDATION: Project manager should review the update and track the next action.
"""


def parse_ai_result(result):

    data = {
        "status": "IN PROGRESS",
        "reason": "Project update received.",
        "action": "Review the latest update.",
        "risk": "MEDIUM",
        "recommendation": "Continue monitoring the project."
    }

    lines = result.splitlines()

    for line in lines:

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip().lower()
        value = value.strip()

        if key == "status":
            data["status"] = value

        elif key == "reason":
            data["reason"] = value

        elif key == "action":
            data["action"] = value

        elif key == "risk":
            data["risk"] = value

        elif key == "recommendation":
            data["recommendation"] = value

    return data


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="text-align:center; padding:15px;">
        <div style="font-size:42px;">🚀</div>
        <h2>ProjectIQ</h2>
        <p style="color:#9ca3af;">
            Intelligent Project Operations
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "📁 Projects",
        "🎫 Issues",
        "🤖 AI Update Parser",
        "🧠 AI Copilot",
        "👤 Customer View"
    ]
)

st.sidebar.divider()

st.sidebar.caption("ProjectIQ")
st.sidebar.caption("Hackathon Prototype")


# ============================================================
# DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">
                🚀 ProjectIQ
            </div>
            <div class="hero-subtitle">
                AI-powered project monitoring, risk detection and customer visibility.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    (
        total,
        completed,
        blocked,
        in_progress,
        avg_progress,
        issues
    ) = get_statistics()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Projects", total)
    col2.metric("Completed", completed)
    col3.metric("In Progress", in_progress)
    col4.metric("Blocked", blocked)
    col5.metric("Avg Progress", f"{avg_progress}%")

    st.divider()

    st.subheader("📈 Portfolio Overview")

    for project in projects:

        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:

            st.markdown(
                f"""
                <div class="project-title">
                    {status_icon(project["status"])}
                    {project["name"]}
                </div>
                <div class="muted">
                    {project["customer"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.progress(project["progress"] / 100)

            st.caption(
                f"{project['progress']}% complete"
            )

        with col3:

            st.metric(
                "Status",
                project["status"]
            )

    st.divider()

    st.subheader("⚠️ Attention Required")

    blocked_projects = [
        p for p in projects
        if p["status"] == "Blocked"
    ]

    if blocked_projects:

        for project in blocked_projects:

            st.error(
                f"🔴 **{project['name']}** — "
                f"{project['description']}"
            )

    else:

        st.success("No blocked projects.")


# ============================================================
# PROJECTS
# ============================================================

elif page == "📁 Projects":

    st.title("📁 Projects")

    st.caption(
        "Centralized project portfolio and delivery tracking."
    )

    for project in projects:

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                st.subheader(
                    f"{status_icon(project['status'])} "
                    f"{project['name']}"
                )

                st.write(
                    f"**Customer:** {project['customer']}"
                )

                st.write(
                    project["description"]
                )

                st.caption(
                    f"Owners: {', '.join(project['owners'])}"
                )

            with col2:

                st.metric(
                    "Progress",
                    f"{project['progress']}%"
                )

                st.write(
                    f"**{project['status']}**"
                )

            st.progress(project["progress"] / 100)

            st.divider()

            st.markdown("### 🏁 Milestones")

            for milestone in project["milestones"]:

                st.write(
                    f"{status_icon(milestone['status'])} "
                    f"**{milestone['name']}** — "
                    f"{milestone['status']}"
                )

                for task, status in milestone["tasks"]:

                    st.caption(
                        f"   {status_icon(status)} {task} — {status}"
                    )


# ============================================================
# ISSUES
# ============================================================

elif page == "🎫 Issues":

    st.title("🎫 Issues & Tickets")

    st.caption(
        "Centralized project issue tracking."
    )

    categories = [
        "Bug",
        "Feature Request",
        "Question",
        "Support",
        "Implementation"
    ]

    selected_category = st.selectbox(
        "Filter by category",
        ["All"] + categories
    )

    found_any = False

    for project in projects:

        for issue in project["issues"]:

            if (
                selected_category != "All"
                and issue["category"] != selected_category
            ):
                continue

            found_any = True

            st.markdown(
                f"""
                <div class="card">
                    <div class="project-title">
                        🔴 {issue["title"]}
                    </div>
                    <div class="muted">
                        Project: {project["name"]}
                        &nbsp; | &nbsp;
                        Category: {issue["category"]}
                        &nbsp; | &nbsp;
                        Status: {issue["status"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    if not found_any:

        st.info("No issues found.")


# ============================================================
# AI UPDATE PARSER
# ============================================================

elif page == "🤖 AI Update Parser":

    st.title("🤖 AI Update Parser")

    st.caption(
        "Convert unstructured chat/email updates into structured project intelligence."
    )

    st.markdown(
        """
        <div class="ai-box">
            <b>AI Project Intelligence</b><br>
            Paste an email, Slack message or client update.
            ProjectIQ will identify status, reason, action,
            risk and recommendation.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    update = st.text_area(
        "Paste a project update",
        height=180,
        placeholder=(
            "Example:\n\n"
            "The API integration is blocked because the client "
            "has not provided authentication credentials. "
            "Backend development is complete. Testing cannot "
            "start until the credentials are received."
        )
    )

    if st.button(
        "✨ Analyze Update",
        type="primary",
        use_container_width=False
    ):

        if not update.strip():

            st.warning(
                "Please enter a project update first."
            )

        else:

            with st.spinner("AI is analyzing the update..."):

                raw_result = ai_analyze_update(update)

                result = parse_ai_result(raw_result)

            st.success(
                "Update successfully converted into structured status."
            )

            st.divider()

            st.subheader("🧠 Structured Update")

            status = result["status"].upper()

            if "BLOCK" in status:

                st.error(
                    f"🔴 **Status: {status}**"
                )

            elif "COMPLETE" in status:

                st.success(
                    f"🟢 **Status: {status}**"
                )

            else:

                st.warning(
                    f"🟡 **Status: {status}**"
                )

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("### 🔍 Reason")

                st.write(
                    result["reason"]
                )

            with col2:

                st.markdown("### ⚡ Required Action")

                st.write(
                    result["action"]
                )

            col3, col4 = st.columns(2)

            with col3:

                st.markdown("### 🚨 Risk")

                risk = result["risk"].upper()

                if risk == "HIGH":

                    st.error(risk)

                elif risk == "MEDIUM":

                    st.warning(risk)

                else:

                    st.success(risk)

            with col4:

                st.markdown("### 💡 Recommendation")

                st.write(
                    result["recommendation"]
                )

            st.divider()

            st.subheader("📄 Original Update")

            st.info(update)

# ============================================================
# AI COPILOT
# ============================================================

elif page == "🧠 AI Copilot":

    st.title("🧠 AI Project Copilot")

    st.caption(
        "Ask questions about projects, customers, risks, blockers and delivery status."
    )

    st.markdown(
        """
        <div class="ai-box">
            <b>ProjectIQ Copilot</b><br>
            Ask questions in natural language and get answers
            from the current project portfolio.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    question = st.text_input(
        "Ask your project question",
        placeholder="Example: Which projects are at risk and why?"
    )

    example_col1, example_col2, example_col3 = st.columns(3)

    with example_col1:

        if st.button(
            "🚨 Projects at risk",
            use_container_width=True
        ):
            question = "Which projects are at risk and why?"

    with example_col2:

        if st.button(
            "⏰ Behind schedule",
            use_container_width=True
        ):
            question = "Which projects are behind schedule?"

    with example_col3:

        if st.button(
            "🎯 What needs attention?",
            use_container_width=True
        ):
            question = "What should the team focus on today?"

    if question:

        st.divider()

        with st.spinner("🧠 Analyzing project portfolio..."):

            q = question.lower()

            blocked_projects = [
                p for p in projects
                if p["status"] == "Blocked"
            ]

            active_projects = [
                p for p in projects
                if p["status"] != "Completed"
            ]

            if (
                "risk" in q
                or "at risk" in q
                or "danger" in q
            ):

                st.subheader("🚨 AI Risk Analysis")

                if blocked_projects:

                    for p in blocked_projects:

                        st.error(
                            f"""
                            🔴 **{p['name']}**

                            **Customer:** {p['customer']}

                            **Progress:** {p['progress']}%

                            **Why at risk:**  
                            The project is currently blocked and requires
                            an external dependency to move forward.

                            **Recommended action:**  
                            Follow up with the customer and resolve the
                            blocking dependency immediately.
                            """
                        )

                else:

                    st.success(
                        "No projects are currently showing critical risk."
                    )

            elif (
                "behind" in q
                or "schedule" in q
                or "delay" in q
                or "late" in q
            ):

                st.subheader("⏰ Schedule Analysis")

                behind = [
                    p for p in projects
                    if p["status"] == "Blocked"
                    or p["progress"] < 70
                ]

                if behind:

                    for p in behind:

                        st.warning(
                            f"""
                            **{p['name']}**

                            Progress: **{p['progress']}%**

                            Status: **{p['status']}**

                            Customer: **{p['customer']}**
                            """
                        )

                else:

                    st.success(
                        "All active projects are progressing normally."
                    )

            elif (
                "attention" in q
                or "today" in q
                or "focus" in q
                or "priority" in q
            ):

                st.subheader("🎯 Recommended Priorities")

                priority_projects = sorted(
                    active_projects,
                    key=lambda x: (
                        x["status"] != "Blocked",
                        x["progress"]
                    )
                )

                for i, p in enumerate(
                    priority_projects,
                    start=1
                ):

                    st.markdown(
                        f"""
                        ### {i}. {p['name']}

                        **Customer:** {p['customer']}  
                        **Status:** {p['status']}  
                        **Progress:** {p['progress']}%

                        **Recommended action:** Review current blockers,
                        confirm the next milestone and communicate the
                        latest status to the customer.
                        """
                    )

            elif (
                "summary" in q
                or "overview" in q
                or "status" in q
            ):

                st.subheader("📊 Portfolio Summary")

                total = len(projects)

                completed = len([
                    p for p in projects
                    if p["status"] == "Completed"
                ])

                blocked = len([
                    p for p in projects
                    if p["status"] == "Blocked"
                ])

                avg = int(
                    sum(p["progress"] for p in projects)
                    / len(projects)
                )

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Projects",
                    total
                )

                col2.metric(
                    "Completed",
                    completed
                )

                col3.metric(
                    "Blocked",
                    blocked
                )

                col4.metric(
                    "Avg Progress",
                    f"{avg}%"
                )

                st.write(
                    "The portfolio currently contains "
                    f"**{total} projects** with an average "
                    f"completion of **{avg}%**."
                )

                if blocked:

                    st.error(
                        f"{blocked} project(s) require immediate attention."
                    )

            elif "xyz" in q:

                project = projects[1]

                st.subheader(
                    f"🔎 {project['name']}"
                )

                st.write(
                    f"**Customer:** {project['customer']}"
                )

                st.write(
                    f"**Status:** {project['status']}"
                )

                st.write(
                    f"**Progress:** {project['progress']}%"
                )

                st.error(
                    "The project is blocked and requires "
                    "resolution of its current dependency."
                )

                st.write(
                    "**Recommended action:** Follow up with "
                    "the customer and resolve the authentication dependency."
                )

            else:

                st.info(
                    """
                    I can help answer questions such as:

                    • Which projects are at risk?

                    • Which projects are behind schedule?

                    • What should the team focus on today?

                    • Give me a project status summary.

                    • Why is XYZ Logistics blocked?
                    """
                )
# ============================================================
# CUSTOMER VIEW
# ============================================================

elif page == "👤 Customer View":

    st.title("👤 Customer Portal")

    st.caption(
        "Customer-safe view of project progress."
    )

    selected = st.selectbox(
        "Select Project",
        [p["name"] for p in projects]
    )

    project = next(
        p for p in projects
        if p["name"] == selected
    )

    st.subheader(
        f"{status_icon(project['status'])} "
        f"{project['name']}"
    )

    st.write(
        f"**Customer:** {project['customer']}"
    )

    st.progress(
        project["progress"] / 100
    )

    st.metric(
        "Overall Progress",
        f"{project['progress']}%"
    )

    status = project["status"]

    if status == "Blocked":

        st.error(
            f"🔴 **Current Status:** {status}"
        )

    elif status == "Completed":

        st.success(
            f"🟢 **Current Status:** {status}"
        )

    else:

        st.warning(
            f"🟡 **Current Status:** {status}"
        )

    st.divider()

    st.subheader("🏁 Milestones")

    for milestone in project["milestones"]:

        icon = status_icon(
            milestone["status"]
        )

        st.write(
            f"{icon} **{milestone['name']}** — "
            f"{milestone['status']}"
        )

        for task, task_status in milestone["tasks"]:

            st.caption(
                f"{status_icon(task_status)} "
                f"{task} — {task_status}"
            )

    st.divider()

    st.subheader("📝 Recent Updates")

    for time, update_text, update_status in project["updates"]:

        st.write(
            f"**{time}** — "
            f"{update_text}"
        )

        st.caption(
            f"Status: {update_status}"
        )

    st.divider()

    st.subheader("📄 Documents")

    documents = [
        "📄 Project Timeline.pdf",
        "📄 Implementation Guide.pdf",
        "📄 Deployment Checklist.pdf"
    ]

    for document in documents:

        st.write(document)

    st.success(
        "This view contains only customer-facing information."
    )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.markdown(
    """
    <div style="text-align:center; color:#777;">
        <b>ProjectIQ AI</b><br>
        <small>Built with ❤️ by Pranav Kale</small><br>
        <small>AI • Project Intelligence • Automation</small>
    </div>
    """,
    unsafe_allow_html=True
)