import json
from copy import deepcopy

import pandas as pd
import plotly.express as px
import streamlit as st

from agents.data_agent import run_data_agent
from agents.math_agent import run_math_agent
from agents.energy_agent import evaluate_scenarios
from agents.audit_agent import run_audit_agent
from agents.business_agent import run_business_agent
from agents.coordinator import run_coordinator
from data.scenarios import DEFAULT_SCENARIOS


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="HAMA Virtual Student Startup Lab",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# CUSTOM DESIGN / CSS
# ============================================================

st.markdown("""
<style>

/* Main page spacing */
.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
}


/* ---------------------------------------------------------
   HERO / TITLE AREA
--------------------------------------------------------- */

.hero-badge {
    display: inline-block;
    padding: .35rem .75rem;
    border: 1px solid rgba(0, 194, 168, .45);
    border-radius: 999px;
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-bottom: .8rem;
    background: rgba(0, 194, 168, .08);
}


.hama-title {
    font-size: 2.7rem;
    font-weight: 850;
    letter-spacing: -.03em;
    margin-bottom: .2rem;
}


.hama-sub {
    font-size: 1rem;
    opacity: .80;
    margin-bottom: .4rem;
}


.developer-line {
    font-size: .9rem;
    opacity: .70;
    margin-top: .25rem;
    margin-bottom: 1.5rem;
}


/* ---------------------------------------------------------
   AGENT CARDS
--------------------------------------------------------- */

.card {
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 16px;
    padding: 1rem 1.1rem;
    background: rgba(255,255,255,.03);
    margin-bottom: .8rem;
}


.pass {
    border-left: 6px solid #00c2a8;
}


.reject {
    border-left: 6px solid #ff5f6d;
}


.wait {
    border-left: 6px solid #f4c95d;
}


.small {
    font-size: .88rem;
    opacity: .8;
}


/* ---------------------------------------------------------
   AGENT WORKFLOW
--------------------------------------------------------- */

.agent-flow {
    font-weight: 700;
    text-align: center;
    padding: .9rem;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,.10);
    background: rgba(255,255,255,.02);
    transition: 0.25s ease;
}


.agent-flow:hover {
    transform: translateY(-3px);
    border-color: rgba(0,194,168,.50);
}


/* ---------------------------------------------------------
   HAMA FOOTER
--------------------------------------------------------- */

.hama-footer {
    margin-top: 3.2rem;
    padding: 1.4rem 1rem 1rem 1rem;
    text-align: center;
    border-top: 1px solid rgba(255,255,255,.12);
    opacity: .88;
}


.hama-footer .brand {
    font-size: 1rem;
    font-weight: 800;
    letter-spacing: .08em;
}


.hama-footer .developer {
    margin-top: .35rem;
    font-size: .88rem;
}


.hama-footer .version {
    margin-top: .25rem;
    font-size: .72rem;
    opacity: .60;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    '<div class="hero-badge">'
    'Research Prototype • Release 1.0'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hama-title">'
    'HAMA — Virtual Student Startup Lab'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hama-sub">'
    'Human–AI Multi-Agent Collaboration • '
    'Student Entrepreneurship • '
    'Mathematical Modelling • '
    'School Energy Decision-Making'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="developer-line">'
    'Designed & Developed by '
    '<b>Nikolaos Sampanis</b> • PhD Candidate'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR — MISSION CONTROL
# ============================================================

with st.sidebar:

    st.header("🎯 Mission Control")

    mode = st.radio(
        "Τρόπος λειτουργίας",
        [
            "Demo School",
            "Real School Data"
        ]
    )

    target_percent = st.slider(
        "Στόχος μείωσης κόστους (%)",
        5,
        40,
        15,
        1
    )

    max_budget_enabled = st.checkbox(
        "Περιορισμός επενδυτικού budget",
        value=True
    )

    max_budget = st.number_input(
        "Μέγιστο budget (€)",
        min_value=0.0,
        value=15000.0,
        step=500.0,
        disabled=not max_budget_enabled,
    )

    inject_error = st.checkbox(
        "🎓 Demo Audit Error",
        value=False,
        help=(
            "Εισάγει σκόπιμο λάθος 1.000 € στο Σενάριο Β "
            "για να φανεί ο έλεγχος του Audit Agent."
        )
    )

    st.divider()

    st.caption(
        "HAMA Release 1.0 uses structured agent handoffs "
        "without an external LLM API."
    )


# ============================================================
# SCHOOL DATA
# ============================================================

if mode == "Demo School":

    area_m2 = 1500.0
    annual_kwh = 76500.0
    annual_cost = 20400.0

else:

    st.subheader("🏫 Real School Data")

    c1, c2, c3 = st.columns(3)

    with c1:

        area_m2 = st.number_input(
            "Επιφάνεια σχολείου (m²)",
            min_value=1.0,
            value=1500.0,
            step=50.0
        )

    with c2:

        annual_kwh = st.number_input(
            "Ετήσια κατανάλωση (kWh)",
            min_value=1.0,
            value=76500.0,
            step=500.0
        )

    with c3:

        annual_cost = st.number_input(
            "Συνολικό ετήσιο κόστος (€)",
            min_value=1.0,
            value=20400.0,
            step=100.0
        )


# ============================================================
# STARTUP MISSION
# ============================================================

st.markdown("### 🚀 Startup Mission")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "School area",
    f"{area_m2:,.0f} m²"
)

m2.metric(
    "Annual energy",
    f"{annual_kwh:,.0f} kWh"
)

m3.metric(
    "Annual cost",
    f"€{annual_cost:,.0f}"
)

m4.metric(
    "Target reduction",
    f"{target_percent}%"
)


st.progress(
    min(target_percent / 40, 1.0),
    text=(
        f"Mission KPI: reduce annual school energy cost "
        f"by at least {target_percent}%"
    )
)


# ============================================================
# HUMAN–AI WORKFLOW
# ============================================================

st.markdown(
    "### 🤝 Human–AI Multi-Agent Startup Workflow"
)

flow = st.columns(6)

labels = [

    ("📊", "Data"),

    ("🧮", "Math"),

    ("⚡", "Energy"),

    ("🔍", "Audit"),

    ("💼", "Business"),

    ("🤖", "Master"),

]


for col, (icon, name) in zip(flow, labels):

    with col:

        st.markdown(
            f"""
            <div class="agent-flow">
                {icon}<br>
                {name}
            </div>
            """,
            unsafe_allow_html=True
        )


st.divider()


# ============================================================
# INVESTMENT SCENARIOS
# ============================================================

st.markdown(
    "### 🧪 Startup Investment Scenarios"
)

scenarios = deepcopy(
    DEFAULT_SCENARIOS
)

edited = []


for i, sc in enumerate(scenarios):

    with st.expander(
        sc["name"],
        expanded=(i == 0)
    ):

        name = st.text_input(
            "Scenario name",
            value=sc["name"],
            key=f"name_{i}"
        )

        investment = st.number_input(
            "Investment cost (€)",
            min_value=0.0,
            value=float(sc["investment_cost"]),
            step=500.0,
            key=f"inv_{i}"
        )

        reduction = st.slider(
            "Estimated annual cost reduction (%)",
            0.0,
            60.0,
            float(sc["reduction_percent"]),
            0.5,
            key=f"red_{i}"
        )

        description = st.text_input(
            "Scenario description",
            value=sc["description"],
            key=f"desc_{i}"
        )

        edited.append(
            {
                "name": name,
                "investment_cost": investment,
                "reduction_percent": reduction,
                "description": description,
            }
        )


scenarios = edited


# ============================================================
# RUN MISSION
# ============================================================

run = st.button(
    "▶ RUN HAMA STARTUP MISSION",
    type="primary",
    use_container_width=True
)


if run:

    st.session_state["ran"] = True

    st.session_state["payloads"] = {}


    # --------------------------------------------------------
    # DATA AGENT
    # --------------------------------------------------------

    data_payload = run_data_agent(
        area_m2,
        annual_kwh,
        annual_cost
    )


    # --------------------------------------------------------
    # MATH AGENT
    # --------------------------------------------------------

    math_payload = run_math_agent(
        data_payload,
        target_percent
    )


    # --------------------------------------------------------
    # ENERGY AGENT
    # --------------------------------------------------------

    energy_payload = evaluate_scenarios(
        annual_cost,
        scenarios,
        inject_error=inject_error
    )


    # --------------------------------------------------------
    # AUDIT AGENT
    # --------------------------------------------------------

    audit_payload = run_audit_agent(
        annual_cost,
        energy_payload
    )


    # --------------------------------------------------------
    # EDUCATIONAL AUDIT EVENT
    # --------------------------------------------------------

    audit_event = None


    if audit_payload["status"] == "REJECTED":

        audit_event = audit_payload

        corrected_energy_payload = evaluate_scenarios(
            annual_cost,
            scenarios,
            inject_error=False
        )

        audit_payload = run_audit_agent(
            annual_cost,
            corrected_energy_payload
        )


    # --------------------------------------------------------
    # BUSINESS AGENT
    # --------------------------------------------------------

    business_payload = run_business_agent(

        audit_payload,

        target_percent,

        max_budget
        if max_budget_enabled
        else None,

    )


    # --------------------------------------------------------
    # MASTER COORDINATOR
    # --------------------------------------------------------

    coordinator_payload = run_coordinator(

        data_payload,

        math_payload,

        audit_payload,

        business_payload,

    )


    st.session_state["payloads"] = {

        "data": data_payload,

        "math": math_payload,

        "energy": energy_payload,

        "audit_event": audit_event,

        "audit": audit_payload,

        "business": business_payload,

        "coordinator": coordinator_payload,

    }


# ============================================================
# AGENT RESULTS
# ============================================================

if st.session_state.get("ran"):

    p = st.session_state["payloads"]


    st.markdown(
        "## 🛰 Agent-to-Agent Communication Log"
    )


    # ========================================================
    # DATA AGENT
    # ========================================================

    d = p["data"]


    cls = (
        "pass"
        if d["status"] == "PASS"
        else "reject"
    )


    st.markdown(
    f'<div class="card {cls}">'
    f'<b>📊 DATA AGENT → MATH AGENT</b><br>'
    f'<b>STATUS:</b> {d["status"]}<br>'
    f'<span class="small">{d["message"]}</span>'
    f'</div>',
    unsafe_allow_html=True
)


    if d["status"] == "PASS":

        c1, c2, c3 = st.columns(3)


        c1.metric(
            "Energy intensity",
            f'{d["eui"]:.2f} kWh/m²/year'
        )


        c2.metric(
            "Cost intensity",
            f'€{d["cost_intensity"]:.2f}/m²/year'
        )


        c3.metric(
            "Effective cost",
            f'€{d["effective_price"]:.3f}/kWh'
        )


    # ========================================================
    # MATH AGENT
    # ========================================================

    m = p["math"]


    cls = (
        "pass"
        if m["status"] == "PASS"
        else "wait"
    )


    st.markdown(
    f'<div class="card {cls}">'
    f'<b>🧮 MATH AGENT → ENERGY AGENT</b><br>'
    f'<b>STATUS:</b> {m["status"]}<br>'
    f'<span class="small">{m["message"]}</span>'
    f'</div>',
    unsafe_allow_html=True
)


    if m["status"] == "PASS":

        c1, c2 = st.columns(2)


        c1.metric(
            "Required annual saving",
            f'€{m["required_saving"]:,.0f}'
        )


        c2.metric(
            "Maximum target cost",
            f'€{m["target_cost"]:,.0f}'
        )


    # ========================================================
    # AUDIT TEACHING EVENT
    # ========================================================

    if p.get("audit_event") is not None:

        ae = p["audit_event"]


        rejected_rows = [

            x

            for x in ae["results"]

            if x["audit_status"] == "REJECTED"

        ]


        st.error(
            "🔍 AUDIT AGENT — CALCULATION REJECTED"
        )


        for x in rejected_rows:

            st.write(

                f'**{x["name"]}**: '

                f'Reported saving: '

                f'€{x["reported_saving"]:,.0f} | '

                f'Expected saving: '

                f'€{x["expected_saving"]:,.0f} | '

                f'Difference: '

                f'€{x["audit_error"]:,.0f}.'

            )


        st.warning(
            "↩ RETURN TO ENERGY AGENT"
        )


        st.success(
            "⚡ ENERGY AGENT — RESUBMITTED "
            "• 🔍 AUDIT AGENT — PASS"
        )


    # ========================================================
    # VERIFIED SCENARIOS TABLE
    # ========================================================

    a = p["audit"]


    rows = []


    for x in a["results"]:

        rows.append(
            {

                "Scenario":
                    x["name"],

                "Investment (€)":
                    x["investment_cost"],

                "Reduction (%)":
                    x["reduction_percent"],

                "Annual saving (€)":
                    x["expected_saving"],

                "New annual cost (€)":
                    annual_cost
                    - x["expected_saving"],

                "Payback (years)":
                    x["payback_years"],

                "Audit":
                    x["audit_status"],

            }
        )


    df = pd.DataFrame(rows)


    st.markdown(
        "### 📈 Verified Scenario Comparison"
    )


    st.dataframe(

        df.style.format(
            {

                "Investment (€)":
                    "{:,.0f}",

                "Reduction (%)":
                    "{:.1f}",

                "Annual saving (€)":
                    "{:,.0f}",

                "New annual cost (€)":
                    "{:,.0f}",

                "Payback (years)":
                    "{:.2f}",

            }
        ),

        use_container_width=True,

        hide_index=True
    )


    # ========================================================
    # CHART 1
    # ========================================================

    fig = px.bar(

        df,

        x="Scenario",

        y="Annual saving (€)",

        text_auto=".2s",

        title=(
            "Verified Annual Savings "
            "by Startup Scenario"
        ),

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 2
    # ========================================================

    fig2 = px.scatter(

        df,

        x="Investment (€)",

        y="Annual saving (€)",

        size="Reduction (%)",

        hover_name="Scenario",

        title=(
            "Startup Investment "
            "vs Annual Saving"
        ),

    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )


    # ========================================================
    # BUSINESS AGENT
    # ========================================================

    b = p["business"]


    if b["status"] == "PASS":

        selected = b["selected"]


        st.markdown(
            "## 💼 Business Agent Recommendation"
        )


        st.success(
            f'Recommended startup scenario: '
            f'**{selected["name"]}**'
        )


        q1, q2, q3, q4 = st.columns(4)


        q1.metric(
            "Investment",
            f'€{selected["investment_cost"]:,.0f}'
        )


        q2.metric(
            "Reduction",
            f'{selected["reduction_percent"]:.1f}%'
        )


        q3.metric(
            "Annual saving",
            f'€{selected["expected_saving"]:,.0f}'
        )


        q4.metric(
            "Payback",
            f'{selected["payback_years"]:.2f} years'
        )


    else:

        st.warning(
            b["message"]
        )


    # ========================================================
    # MASTER COORDINATOR
    # ========================================================

    coord = p["coordinator"]


    st.markdown(
        "## 🤖 HAMA Master Coordinator"
    )


    if coord["status"] == "MISSION ACCOMPLISHED":

        selected = coord["selected"]


        new_cost = (
            annual_cost
            - selected["expected_saving"]
        )


        st.balloons()


        st.success(
            "### ✅ MISSION ACCOMPLISHED"
        )


        r1, r2, r3, r4 = st.columns(4)


        r1.metric(
            "Initial cost",
            f"€{annual_cost:,.0f}"
        )


        r2.metric(
            "Projected new cost",
            f"€{new_cost:,.0f}"
        )


        r3.metric(
            "Achieved reduction",
            f'{selected["reduction_percent"]:.1f}%'
        )


        r4.metric(
            "Mission target",
            f"{target_percent}%"
        )


        st.info(
            "🎓 Educational reinvestment scenario: "
            "the school community may recognize "
            "the successful student startup through "
            "STEM equipment, an educational visit "
            "or another learning activity."
        )


        st.markdown(
            "### 🧑‍⚖️ HUMAN APPROVAL REQUIRED"
        )


        st.caption(
            "The Master Coordinator provides a "
            "recommendation. Final decision-making "
            "remains with the human team."
        )


    else:

        st.error(
            f'### ❌ {coord["status"]}'
        )

        st.write(
            coord["message"]
        )


    # ========================================================
    # EXPORT
    # ========================================================

    st.markdown(
        "### 📦 Export Mission Results"
    )


    csv_bytes = (
        df
        .to_csv(index=False)
        .encode("utf-8-sig")
    )


    st.download_button(

        "Download verified scenarios CSV",

        csv_bytes,

        file_name=(
            "hama_verified_scenarios.csv"
        ),

        mime="text/csv",

    )


    export_payload = {

        "mode":
            mode,

        "school": {

            "area_m2":
                area_m2,

            "annual_kwh":
                annual_kwh,

            "annual_cost":
                annual_cost,

        },

        "target_percent":
            target_percent,

        "max_budget":
            max_budget
            if max_budget_enabled
            else None,

        "coordinator":
            coord,

    }


    st.download_button(

        "Download HAMA Mission Report JSON",

        json.dumps(
            export_payload,
            ensure_ascii=False,
            indent=2
        ).encode("utf-8"),

        file_name=(
            "hama_mission_report.json"
        ),

        mime="application/json",

    )


# ============================================================
# DISCLAIMER
# ============================================================

st.divider()


st.caption(

    "HAMA educational prototype • "
    "Estimated savings are not guaranteed real-world outcomes. "
    "Real deployment requires actual school bills, "
    "technical energy auditing and validated intervention data."

)


# ============================================================
# FOOTER / AUTHORSHIP
# ============================================================

st.markdown("""
<div class="hama-footer"><div class="brand">HAMA • HUMAN–AI MULTI-AGENT VIRTUAL STUDENT STARTUP LAB</div><div class="developer">Designed &amp; Developed by <strong>Nikolaos Sampanis</strong> • PhD Candidate</div><div class="version">Research Prototype • Release 1.0 • Streamlit / Python</div></div>
""", unsafe_allow_html=True)
