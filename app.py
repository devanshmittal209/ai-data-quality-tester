
import os

import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="DataGuard AI | Data Quality",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==================================================
# CUSTOM UI
# ==================================================

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,440;0,9..144,560;0,9..144,650;1,9..144,500&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

        :root {
            --void: #0B1220;
            --panel: #111D2E;
            --panel-raised: #16233F;
            --border: #23324C;
            --ink: #E7ECF3;
            --muted: #8695AC;
            --faint: #57657D;
            --brass: #C9A24A;
            --brass-bright: #E8C878;
            --high: #E2574C;
            --medium: #D8A24A;
            --low: #5B9FD8;
            --good: #59B37A;
        }

        /* ---------- Global ---------- */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: var(--void);
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.4rem;
            padding-bottom: 4rem;
        }

        /* Remove Streamlit's fixed toolbar so it does not obstruct the app. */
        header[data-testid="stHeader"] {
            display: none;
        }

        .stMarkdown p,
        .stMarkdown li,
        .stCaption,
        label {
            color: var(--ink);
        }

        /* Keep native Streamlit controls readable on the dark theme. */
        [data-testid="stFileUploader"] *,
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary *,
        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"],
        [data-testid="stMetricDelta"] {
            color: var(--ink) !important;
        }

        [data-testid="stFileUploader"] small {
            color: var(--muted) !important;
        }

        [data-testid="stFileUploader"] button {
            color: var(--ink) !important;
            background: var(--panel-raised) !important;
            border-color: var(--border) !important;
        }

        [data-testid="stChatInput"] {
            background: var(--panel);
            border-color: var(--border);
        }

        [data-testid="stChatInput"] textarea {
            color: var(--ink) !important;
            background: var(--panel) !important;
        }

        [data-testid="stChatInput"] textarea::placeholder {
            color: var(--muted) !important;
        }

        /* ---------- Header ---------- */
        .brand {
            display: flex;
            align-items: baseline;
            gap: 0.65rem;
            margin-bottom: 3rem;
            padding-bottom: 1.1rem;
            border-bottom: 1px solid var(--border);
        }

        .brand-mark {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            color: var(--void);
            background: var(--brass);
            padding: 0.22rem 0.5rem;
            border-radius: 4px;
        }

        .brand-name {
            font-family: 'Fraunces', serif;
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--ink);
        }

        .brand-subtitle {
            color: var(--faint);
            font-size: 0.82rem;
            font-family: 'IBM Plex Mono', monospace;
            margin-left: 2px;
        }

        /* ---------- Hero ---------- */
        .hero-title {
            color: var(--ink);
            font-family: 'Fraunces', serif;
            font-size: 3rem;
            line-height: 1.1;
            font-weight: 560;
            letter-spacing: -0.01em;
            margin: 0;
        }

        .hero-title em {
            font-style: italic;
            color: var(--brass-bright);
        }

        .hero-text {
            color: var(--muted);
            font-size: 1.02rem;
            line-height: 1.65;
            margin-top: 1.15rem;
        }

        .hero-note {
            color: var(--faint);
            font-size: 0.8rem;
            margin-top: 1.3rem;
            font-family: 'IBM Plex Mono', monospace;
            line-height: 1.5;
        }

        /* ---------- Sample readout (hero illustration) ---------- */
        .ledger {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.82rem;
            margin-top: 0.4rem;
        }

        .ledger-head {
            padding: 0.7rem 1.1rem;
            color: var(--faint);
            border-bottom: 1px solid var(--border);
            font-size: 0.74rem;
        }

        .ledger-row {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            padding: 0.7rem 1.1rem;
            border-bottom: 1px solid var(--border);
        }

        .ledger-row:last-child { border-bottom: none; }

        .ledger-row .col-name { color: var(--ink); }
        .ledger-row .flag-high { color: var(--high); }
        .ledger-row .flag-medium { color: var(--medium); }
        .ledger-row .flag-low { color: var(--low); }
        .ledger-row .flag-ok { color: var(--good); }

        /* ---------- Section labels ---------- */
        .section-label {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            color: var(--ink);
            font-family: 'Fraunces', serif;
            font-size: 1.08rem;
            font-weight: 600;
            margin: 2.6rem 0 1.1rem 0;
        }

        .section-label::before {
            content: '';
            width: 16px;
            height: 1px;
            background: var(--brass);
            flex-shrink: 0;
        }

        /* ---------- Metric rows (overview) ---------- */
        .metric-row {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1.05rem 1.2rem;
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.76rem;
            font-family: 'IBM Plex Mono', monospace;
        }

        .metric-value {
            color: var(--ink);
            font-size: 1.7rem;
            font-family: 'Fraunces', serif;
            font-weight: 600;
            margin-top: 0.25rem;
        }

        .metric-description {
            color: var(--faint);
            font-size: 0.76rem;
            margin-top: 0.2rem;
        }

        /* ---------- Score ---------- */
        .score-card {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.5rem 1.6rem;
            min-height: 190px;
        }

        .score-label {
            color: var(--muted);
            font-size: 0.76rem;
            font-family: 'IBM Plex Mono', monospace;
        }

        .gauge-wrap {
            display: flex;
            align-items: center;
            gap: 1.3rem;
            margin-top: 0.9rem;
        }

        .gauge {
            width: 96px;
            height: 96px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            flex-shrink: 0;
        }

        .gauge::before {
            content: '';
            position: absolute;
            inset: 9px;
            border-radius: 50%;
            background: var(--panel);
        }

        .gauge-value {
            position: relative;
            font-family: 'Fraunces', serif;
            font-size: 1.55rem;
            font-weight: 600;
            color: var(--ink);
        }

        .score-status {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.84rem;
            font-weight: 600;
        }

        .status-good { color: var(--good); }
        .status-warning { color: var(--medium); }
        .status-poor { color: var(--high); }

        .score-summary {
            color: var(--muted);
            font-size: 0.88rem;
            line-height: 1.55;
        }

        .breakdown {
            display: flex;
            gap: 1.6rem;
            margin-top: 1.1rem;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.82rem;
        }

        .breakdown span.n-high { color: var(--high); }
        .breakdown span.n-medium { color: var(--medium); }
        .breakdown span.n-low { color: var(--low); }

        /* ---------- Issue rows ---------- */
        [data-testid="stExpander"] {
            background: var(--panel);
            border: 1px solid var(--border) !important;
            border-radius: 10px;
            margin-bottom: 0.6rem;
        }

        [data-testid="stExpander"] summary {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            color: var(--ink) !important;
        }

        [data-testid="stExpander"] [data-testid="stMarkdownContainer"],
        [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stExpander"] [data-testid="stMarkdownContainer"] strong {
            color: var(--ink);
        }

        .sev-tag {
            font-family: 'IBM Plex Mono', monospace;
            font-weight: 600;
            font-size: 0.85rem;
        }

        .sev-tag.sev-high { color: var(--high); }
        .sev-tag.sev-medium { color: var(--medium); }
        .sev-tag.sev-low { color: var(--low); }

        /* ---------- AI panel ---------- */
        .ai-panel {
            background: var(--panel-raised);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.6rem 1.8rem;
        }

        .ai-tag {
            font-family: 'IBM Plex Mono', monospace;
            color: var(--brass-bright);
            font-size: 0.78rem;
        }

        .ai-title {
            font-family: 'Fraunces', serif;
            color: var(--ink);
            font-size: 1.35rem;
            font-weight: 600;
            margin-top: 0.35rem;
        }

        .ai-description {
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.6;
            margin-top: 0.55rem;
        }

        /* ---------- Buttons ---------- */
        .stButton > button {
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--panel);
            color: var(--ink);
            font-weight: 600;
            min-height: 2.7rem;
        }

        .stButton > button[kind="primary"] {
            background: var(--brass);
            border-color: var(--brass);
            color: var(--void) !important;
        }

        .stButton > button[kind="primary"] p {
            color: var(--void) !important;
        }

        .stButton > button[kind="primary"]:hover {
            background: var(--brass-bright);
            border-color: var(--brass-bright);
            color: var(--void);
        }

        /* ---------- Upload ---------- */
        [data-testid="stFileUploader"] {
            background: var(--panel);
            border: 1.5px dashed var(--border);
            border-radius: 12px;
            padding: 0.5rem;
        }

        [data-testid="stFileUploader"] section {
            background: transparent;
        }

        /* ---------- Footer ---------- */
        .footer {
            text-align: left;
            color: var(--faint);
            font-size: 0.78rem;
            font-family: 'IBM Plex Mono', monospace;
            padding-top: 3rem;
            border-top: 1px solid var(--border);
            margin-top: 2rem;
        }

        /* ---------- Hide Streamlit chrome ---------- */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# GEMINI SETUP
# ==================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)


# ==================================================
# SESSION STATE
# ==================================================

defaults = {
    "file_name": None,
    "df": None,
    "analyzed": False,
    "issues": [],
    "score": None,
    "ai_analysis": None,
    "chat_history": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==================================================
# DATA QUALITY ANALYSIS
# ==================================================

def analyze_dataset(df):
    issues = []
    total_rows = len(df)

    if total_rows == 0:
        return issues

    # Missing values
    for column in df.columns:
        missing_count = int(df[column].isna().sum())

        if missing_count > 0:
            percentage = (missing_count / total_rows) * 100

            if percentage >= 20:
                severity = "High"
            elif percentage >= 5:
                severity = "Medium"
            else:
                severity = "Low"

            issues.append({
                "column": column,
                "issue": "Missing Values",
                "affected_rows": missing_count,
                "percentage": round(percentage, 2),
                "severity": severity,
            })

    # Duplicate rows
    duplicate_count = int(df.duplicated().sum())

    if duplicate_count > 0:
        percentage = (duplicate_count / total_rows) * 100

        severity = (
            "High" if percentage >= 10
            else "Medium" if percentage >= 2
            else "Low"
        )

        issues.append({
            "column": "Dataset",
            "issue": "Duplicate Rows",
            "affected_rows": duplicate_count,
            "percentage": round(percentage, 2),
            "severity": severity,
        })

    # Numeric checks
    numeric_columns = df.select_dtypes(include=np.number).columns

    for column in numeric_columns:
        series = df[column].dropna()

        if len(series) == 0:
            continue

        # Negative values
        negative_count = int((series < 0).sum())

        if negative_count > 0:
            percentage = (negative_count / total_rows) * 100

            issues.append({
                "column": column,
                "issue": "Negative Values",
                "affected_rows": negative_count,
                "percentage": round(percentage, 2),
                "severity": "Medium",
            })

        # Potential outliers using IQR
        if len(series) >= 10:
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1

            if iqr > 0:
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr

                outliers = series[
                    (series < lower_bound) |
                    (series > upper_bound)
                ]

                outlier_count = len(outliers)

                if outlier_count > 0:
                    percentage = (outlier_count / total_rows) * 100

                    severity = (
                        "Medium" if percentage >= 5
                        else "Low"
                    )

                    issues.append({
                        "column": column,
                        "issue": "Potential Outliers",
                        "affected_rows": outlier_count,
                        "percentage": round(percentage, 2),
                        "severity": severity,
                    })

    # Categorical consistency
    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns

    for column in categorical_columns:
        values = df[column].dropna()

        if len(values) == 0:
            continue

        string_values = values.astype(str)

        whitespace_count = int(
            string_values.str.strip().ne(string_values).sum()
        )

        if whitespace_count > 0:
            percentage = (whitespace_count / total_rows) * 100

            issues.append({
                "column": column,
                "issue": "Whitespace Inconsistency",
                "affected_rows": whitespace_count,
                "percentage": round(percentage, 2),
                "severity": "Low",
            })

    return issues


# ==================================================
# QUALITY SCORE
# ==================================================

def calculate_quality_score(issues):
    score = 100

    for issue in issues:
        percentage = issue["percentage"]
        severity = issue["severity"]

        if severity == "High":
            deduction = max(5, min(20, percentage))
        elif severity == "Medium":
            deduction = max(2, min(10, percentage / 2))
        else:
            deduction = max(1, min(5, percentage / 2))

        score -= deduction

    return round(max(0, score), 1)


# ==================================================
# GEMINI FUNCTIONS
# ==================================================

def build_issue_summary(issues):
    if not issues:
        return "No data quality issues were detected."

    return "\n".join(
        [
            f"- Column: {issue['column']} | "
            f"Issue: {issue['issue']} | "
            f"Affected rows: {issue['affected_rows']} | "
            f"Percentage: {issue['percentage']}% | "
            f"Severity: {issue['severity']}"
            for issue in issues
        ]
    )


def get_ai_analysis(issues, score, df):
    issue_summary = build_issue_summary(issues)

    prompt = f"""
You are a data quality expert.

Analyze these automated data quality results.

Dataset:
- Rows: {len(df)}
- Columns: {len(df.columns)}
- Quality Score: {score}/100

Detected Issues:
{issue_summary}

Provide a concise analysis with these sections:

### Overall Assessment
Give a short summary of the dataset's quality.

### Most Important Issues
Explain the most relevant detected issues.

### Potential Business Impact
Explain what these issues could affect.

### Recommended Actions
Give practical next steps.

Important:
- Do not assume every outlier or unusual value is incorrect.
- Clearly distinguish potential issues from confirmed errors.
- Do not invent facts that are not present in the results.
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )

    return interaction.output_text


def ask_ai(question, issues, score, df):
    issue_summary = build_issue_summary(issues)

    prompt = f"""
You are an AI data quality assistant.

Dataset:
- Rows: {len(df)}
- Columns: {len(df.columns)}
- Quality Score: {score}/100

Automated quality results:
{issue_summary}

Answer this user question based only on the available analysis:

User question:
{question}

Rules:
- Be concise and practical.
- Do not invent information.
- Distinguish confirmed issues from potential issues.
- If the analysis is insufficient, say so.
- Provide Pandas code when useful.
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )

    return interaction.output_text


# ==================================================
# HELPER: AFFECTED RECORDS
# ==================================================

def get_affected_records(df, issue):
    column = issue["column"]
    issue_type = issue["issue"]

    if issue_type == "Duplicate Rows":
        return df[df.duplicated(keep=False)]

    if column not in df.columns:
        return pd.DataFrame()

    if issue_type == "Missing Values":
        return df[df[column].isna()]

    if issue_type == "Negative Values":
        return df[df[column] < 0]

    if issue_type == "Potential Outliers":
        series = df[column].dropna()

        if len(series) < 10:
            return pd.DataFrame()

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        if iqr <= 0:
            return pd.DataFrame()

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        return df[
            (df[column] < lower_bound) |
            (df[column] > upper_bound)
        ]

    if issue_type == "Whitespace Inconsistency":
        values = df[column].astype(str)

        return df[
            values.str.strip() != values
        ]

    return pd.DataFrame()


# ==================================================
# HEADER
# ==================================================

st.markdown(
    """
    <div class="brand">
        <div class="brand-mark">DQ</div>
        <div class="brand-name">DataGuard AI</div>
        <div class="brand-subtitle">/ dataset inspection</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# UPLOAD
# ==================================================

uploaded_file = st.file_uploader(
    "Upload your CSV dataset",
    type=["csv"],
    label_visibility="collapsed",
)

if uploaded_file is None and st.session_state.df is None:
    hero_col, preview_col = st.columns([1.15, 1], gap="large")

    with hero_col:
        st.markdown(
            """
            <h1 class="hero-title">Every dataset<br>leaves a <em>trail</em>.</h1>
            <p class="hero-text">
                Upload a CSV and it's checked for missing values, duplicate
                rows, negative values, outliers and formatting drift —
                then an AI assistant reviews the findings and explains
                what actually matters.
            </p>
            <p class="hero-note">
                Runs in this session only. Just the summarized findings —
                never the raw data — are sent to the AI model.
            </p>
            """,
            unsafe_allow_html=True,
        )

    with preview_col:
        st.markdown(
            """
            <div class="ledger">
                <div class="ledger-head">sample readout</div>
                <div class="ledger-row">
                    <span class="col-name">customer_id</span>
                    <span class="flag-high">41% missing</span>
                </div>
                <div class="ledger-row">
                    <span class="col-name">email</span>
                    <span class="flag-medium">3.2% missing</span>
                </div>
                <div class="ledger-row">
                    <span class="col-name">order_id</span>
                    <span class="flag-ok">0 duplicates</span>
                </div>
                <div class="ledger-row">
                    <span class="col-name">amount</span>
                    <span class="flag-medium">12 outliers flagged</span>
                </div>
                <div class="ledger-row">
                    <span class="col-name">region</span>
                    <span class="flag-low">inconsistent casing</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


if uploaded_file is not None:
    file_name = uploaded_file.name

    if st.session_state.get("file_name") != file_name:
        st.session_state.file_name = file_name
        st.session_state.df = pd.read_csv(uploaded_file)

        st.session_state.analyzed = False
        st.session_state.issues = []
        st.session_state.score = None
        st.session_state.ai_analysis = None
        st.session_state.chat_history = []

    df = st.session_state.df

    # --------------------------------------------------
    # DATASET HEADER
    # --------------------------------------------------

    st.markdown(
        f"""
        <h1 class="hero-title" style="font-size: 2.2rem;">{st.session_state.file_name}</h1>
        <p class="hero-text" style="font-size: 0.95rem;">
            Review the dataset overview, run automated quality checks,
            and ask the AI assistant about the results.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------
    # OVERVIEW
    # --------------------------------------------------

    st.markdown(
        '<div class="section-label">Dataset overview</div>',
        unsafe_allow_html=True,
    )

    total_missing = int(df.isna().sum().sum())
    total_duplicates = int(df.duplicated().sum())

    overview_cols = st.columns(4)

    overview_data = [
        ("Rows", f"{len(df):,}", "Records in dataset"),
        ("Columns", f"{len(df.columns):,}", "Fields detected"),
        ("Missing Values", f"{total_missing:,}", "Empty cells"),
        ("Duplicate Rows", f"{total_duplicates:,}", "Repeated records"),
    ]

    for col, (label, value, description) in zip(
        overview_cols, overview_data
    ):
        with col:
            st.markdown(
                f"""
                <div class="metric-row">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-description">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with st.expander("View dataset preview"):
        st.dataframe(
            df.head(10),
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------
    # RUN ANALYSIS
    # --------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "Run Data Quality Check",
        type="primary",
        use_container_width=True,
    ):
        with st.spinner("Running data quality checks..."):
            issues = analyze_dataset(df)
            score = calculate_quality_score(issues)

            st.session_state.issues = issues
            st.session_state.score = score
            st.session_state.analyzed = True
            st.session_state.ai_analysis = None
            st.session_state.chat_history = []

        st.rerun()

    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    if st.session_state.get("analyzed", False):

        issues = st.session_state.issues
        score = st.session_state.score

        st.markdown(
            '<div class="section-label">Quality assessment</div>',
            unsafe_allow_html=True,
        )

        score_col, summary_col = st.columns([1, 2])

        if score >= 90:
            status = "Excellent"
            status_class = "status-good"
            gauge_color = "var(--good)"
        elif score >= 70:
            status = "Needs attention"
            status_class = "status-warning"
            gauge_color = "var(--medium)"
        else:
            status = "Poor"
            status_class = "status-poor"
            gauge_color = "var(--high)"

        gauge_deg = round((score / 100) * 360, 1)

        with score_col:
            st.markdown(
                f"""
                <div class="score-card">
                    <div class="score-label">Overall quality score</div>
                    <div class="gauge-wrap">
                        <div class="gauge" style="background: conic-gradient({gauge_color} {gauge_deg}deg, var(--border) {gauge_deg}deg 360deg);">
                            <div class="gauge-value">{score}</div>
                        </div>
                        <div>
                            <div class="score-status {status_class}">{status}</div>
                            <div class="score-summary" style="margin-top:0.4rem;">
                                Based on the automated checks<br>performed on this dataset.
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with summary_col:
            issue_count = len(issues)
            affected_rows = sum(
                issue["affected_rows"] for issue in issues
            )

            high_count = sum(
                issue["severity"] == "High" for issue in issues
            )
            medium_count = sum(
                issue["severity"] == "Medium" for issue in issues
            )
            low_count = sum(
                issue["severity"] == "Low" for issue in issues
            )

            st.markdown(
                f"""
                <div class="score-card">
                    <div class="score-label">Quality summary</div>
                    <div style="display:flex;gap:2.2rem;margin-top:1.1rem;">
                        <div>
                            <div class="metric-value">{issue_count}</div>
                            <div class="metric-description">Issues detected</div>
                        </div>
                        <div>
                            <div class="metric-value">{affected_rows:,}</div>
                            <div class="metric-description">Affected rows</div>
                        </div>
                    </div>
                    <div class="breakdown">
                        <span class="n-high">{high_count} high</span>
                        <span class="n-medium">{medium_count} medium</span>
                        <span class="n-low">{low_count} low</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # --------------------------------------------------
        # ISSUES
        # --------------------------------------------------

        st.markdown(
            '<div class="section-label">Detected issues</div>',
            unsafe_allow_html=True,
        )

        if not issues:
            st.success("No data quality issues were detected.")

        else:
            for i, issue in enumerate(issues):
                severity = issue["severity"]
                severity_class = f"sev-{severity.lower()}"

                with st.expander(
                    f"{issue['column']}  ·  {issue['issue']}  ·  {severity}"
                ):
                    detail_col1, detail_col2, detail_col3 = st.columns(3)

                    with detail_col1:
                        st.metric(
                            "Affected Rows",
                            f"{issue['affected_rows']:,}",
                        )

                    with detail_col2:
                        st.metric(
                            "Percentage",
                            f"{issue['percentage']}%",
                        )

                    with detail_col3:
                        st.markdown(
                            f"""
                            <div class="metric-label">Severity</div>
                            <div class="sev-tag {severity_class}" style="margin-top:0.4rem;">
                                {severity}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    affected = get_affected_records(df, issue)

                    if not affected.empty:
                        st.write(
                            f"**{len(affected):,} affected records**"
                        )

                        if st.button(
                            "View affected records",
                            key=f"view_{i}",
                        ):
                            st.dataframe(
                                affected,
                                use_container_width=True,
                                hide_index=True,
                            )
                    else:
                        st.caption(
                            "No affected records could be displayed for this check."
                        )

        # --------------------------------------------------
        # AI ANALYSIS
        # --------------------------------------------------

        st.markdown(
            '<div class="section-label">AI insights</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="ai-panel">
                <div class="ai-tag">Gemini-powered analysis</div>
                <div class="ai-title">Understand what the issues mean</div>
                <div class="ai-description">
                    The quality engine detects issues deterministically.
                    AI helps interpret their potential impact and suggests practical next steps.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.get("ai_analysis") is None:
            st.caption("AI analysis is generated only when you request it, so your Gemini quota is not consumed during every quality check.")
            if st.button("Generate AI Insights", type="primary", use_container_width=True):
                with st.spinner("Generating AI insights..."):
                    try:
                        st.session_state.ai_analysis = get_ai_analysis(
                            issues,
                            score,
                            df,
                        )
                    except Exception as e:
                        error_text = str(e)
                        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text or "quota" in error_text.lower():
                            st.session_state.ai_analysis = (
                                "### AI analysis temporarily unavailable\n\n"
                                "The Gemini API project has reached its current quota. "
                                "Your data-quality checks are still available. Please try again after the quota resets."
                            )
                        else:
                            st.session_state.ai_analysis = (
                                "### AI analysis unavailable\n\n"
                                "Gemini could not generate the analysis right now. "
                                "Your deterministic data-quality results are still available."
                            )
                st.rerun()
        else:
            st.markdown(st.session_state.ai_analysis)

        # --------------------------------------------------
        # ASK AI
        # --------------------------------------------------

        st.markdown(
            '<div class="section-label">Ask your AI assistant</div>',
            unsafe_allow_html=True,
        )

        st.caption(
            "Ask questions about the detected issues, possible causes, "
            "recommended actions, or how to investigate them with Pandas."
        )

        for message in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(message["question"])

            with st.chat_message("assistant"):
                st.markdown(message["answer"])

        question = st.chat_input(
            "e.g. Should I remove the sales_amount outliers?"
        )

        if question:
            with st.spinner("Thinking..."):
                try:
                    answer = ask_ai(
                        question,
                        issues,
                        score,
                        df,
                    )

                    st.session_state.chat_history.append(
                        {
                            "question": question,
                            "answer": answer,
                        }
                    )

                    st.rerun()

                except Exception as e:
                    error_text = str(e)
                    if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text or "quota" in error_text.lower():
                        st.warning(
                            "AI assistant is temporarily unavailable because the Gemini API project has reached its current quota. "
                            "Your data-quality results are still available."
                        )
                    else:
                        st.error(
                            "AI assistant could not respond right now. Your data-quality results are still available."
                        )


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer">
        DataGuard AI — automated data quality testing with AI-assisted insights
    </div>
    """,
    unsafe_allow_html=True,
)
