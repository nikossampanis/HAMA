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

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
}

.hero-badge {
    display: inline-block;
    padding: .35rem .75rem;
    border: 1px solid rgba(0,194,168,.45);
    border-radius: 999px;
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-bottom: .8rem;
    background: rgba(0,194,168,.08);
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

.agent-flow {
    font-weight: 700;
    text-align: center;
    padding: .9rem;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,.10);
    background: rgba(255,255,255,.02);
}

.agent-flow.active {
    border-color: rgba(0,194,168,.75);
    background: rgba(0,194,168,.10);
}

.agent-flow.done {
    border-color: rgba(0,194,168,.45);
    background: rgba(0,194,168,.06);
}

.agent-flow.locked {
    opacity: .42;
}

.handoff {
    padding: .8rem 1rem;
    border-radius: 12px;
    background: rgba(0,194,168,.06);
    border: 1px solid rgba(0,194,168,.18);
    margin: .5rem 0 1rem 0;
}

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
# HERO
# ============================================================

st.markdown(
    '<div class="hero-badge">Research Prototype • Release 1.1</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hama-title">HAMA — Virtual Student Startup Lab</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hama-sub">'
    'Human–AI Multi-Agent Collaboration • '
    'Student Entrepreneurship • '
    'Mathematical Modelling • '
    'School Energy Decision-Making'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="developer-line">'
    'Designed &amp; Developed by '
    '<b>Nikolaos Sampanis</b> • PhD Candidate'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "mission_started": False,
    "stage": 0,
    "mission_config": None,
    "payloads": {},
    "audit_needs_correction": False,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_mission():

    st.session_state["mission_started"] = False
    st.session_state["stage"] = 0
    st.session_state["mission_config"] = None
    st.session_state["payloads"] = {}
    st.session_state["audit_needs_correction"] = False


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
            "Εισάγει σκόπιμο λάθος 1.000 € "
            "στο Σενάριο Β για να φανεί το "
            "REJECT → CORRECT → RESUBMIT."
        ),
    )

    st.divider()

    st.caption(
        "Release 1.1 uses sequential clickable agent handoffs. "
        "The specialist agents are deterministic Python modules; "
        "no external LLM API is required."
    )

    if st.button(
        "↺ Reset Mission",
        use_container_width=True
    ):

        reset_mission()
        st.rerun()


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
    ),
)


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
            key=f"inv_{i}",
        )

        reduction = st.slider(
            "Estimated annual cost reduction (%)",
            0.0,
            60.0,
            float(sc["reduction_percent"]),
            0.5,
            key=f"red_{i}",
        )

        description = st.text_input(
            "Scenario description",
            value=sc["description"],
            key=f"desc_{i}",
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
# START MISSION
# ============================================================

if not st.session_state["mission_started"]:

    if st.button(
        "🚀 START HAMA STARTUP MISSION",
        type="primary",
        use_container_width=True,
    ):

        st.session_state["mission_started"] = True

        st.session_state["stage"] = 1

        st.session_state["payloads"] = {}

        st.session_state[
            "audit_needs_correction"
        ] = False

        st.session_state[
            "mission_config"
        ] = {

            "mode":
                mode,

            "area_m2":
                area_m2,

            "annual_kwh":
                annual_kwh,

            "annual_cost":
                annual_cost,

            "target_percent":
                target_percent,

            "max_budget":
                max_budget
                if max_budget_enabled
                else None,

            "inject_error":
                inject_error,

            "scenarios":
                deepcopy(scenarios),

        }

        st.rerun()

else:

    st.info(
        "🔒 Mission snapshot active: "
        "this run uses the values captured "
        "when START MISSION was pressed. "
        "Use Reset Mission to begin again "
        "with new inputs."
    )


# ============================================================
# WORKFLOW MAP
# ============================================================

st.markdown(
    "### 🤝 Human–AI Multi-Agent Startup Workflow"
)

stage = st.session_state["stage"]

flow = st.columns(6)

labels = [

    ("📊", "Data", 1),

    ("🧮", "Math", 2),

    ("⚡", "Energy", 3),

    ("🔍", "Audit", 4),

    ("💼", "Business", 5),

    ("🤖", "Master", 6),

]

for col, (icon, name, idx) in zip(
    flow,
    labels
):

    if not st.session_state["mission_started"]:

        state_class = "locked"
        state_text = "LOCKED"

    elif stage > idx:

        state_class = "done"
        state_text = "DONE"

    elif stage == idx:

        state_class = "active"
        state_text = "ACTIVE"

    else:

        state_class = "locked"
        state_text = "LOCKED"

    with col:

        st.markdown(
            f'<div class="agent-flow {state_class}">'
            f'{icon}<br>'
            f'{name}<br>'
            f'<span class="small">{state_text}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


st.divider()


# ============================================================
# SEQUENTIAL AGENT EXECUTION
# ============================================================

if st.session_state["mission_started"]:

    cfg = st.session_state[
        "mission_config"
    ]

    p = st.session_state[
        "payloads"
    ]

    st.markdown(
        "## 🛰 Live Agent Handoffs"
    )


    # ========================================================
    # 1. DATA AGENT
    # ========================================================

    if stage == 1:

        st.markdown(
            '<div class="handoff">'
            '<b>Human Data Team:</b> '
            'verify the school inputs, '
            'then authorize the Data Agent.'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "📊 RUN DATA AGENT",
            type="primary",
            use_container_width=True,
        ):

            p["data"] = run_data_agent(
                cfg["area_m2"],
                cfg["annual_kwh"],
                cfg["annual_cost"],
            )

            if p["data"]["status"] == "PASS":

                st.session_state[
                    "stage"
                ] = 2

            else:

                st.session_state[
                    "stage"
                ] = 1

            st.rerun()


    if "data" in p:

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
            f'<span class="small">'
            f'{d["message"]}'
            f'</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if d["status"] == "PASS":

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Energy intensity",
                f'{d["eui"]:.2f} '
                f'kWh/m²/year'
            )

            c2.metric(
                "Cost intensity",
                f'€{d["cost_intensity"]:.2f}'
                f'/m²/year'
            )

            c3.metric(
                "Effective cost",
                f'€{d["effective_price"]:.3f}'
                f'/kWh'
            )


    # ========================================================
    # 2. MATH AGENT
    # ========================================================

    if stage == 2:

        st.markdown(
            '<div class="handoff">'
            '<b>Human Mathematics Team:</b> '
            'inspect the validated baseline '
            'and send it to the Math Agent.'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "🧮 SEND TO MATH AGENT",
            type="primary",
            use_container_width=True,
        ):

            p["math"] = run_math_agent(
                p["data"],
                cfg["target_percent"],
            )

            if p["math"]["status"] == "PASS":

                st.session_state[
                    "stage"
                ] = 3

            else:

                st.session_state[
                    "stage"
                ] = 2

            st.rerun()


    if "math" in p:

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
            f'<span class="small">'
            f'{m["message"]}'
            f'</span>'
            f'</div>',
            unsafe_allow_html=True,
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
    # 3. ENERGY AGENT
    # ========================================================

    if stage == 3:

        st.markdown(
            '<div class="handoff">'
            '<b>Human Energy Team:</b> '
            'review the three candidate '
            'interventions and authorize '
            'scenario evaluation.'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "⚡ SEND SCENARIOS TO ENERGY AGENT",
            type="primary",
            use_container_width=True,
        ):

            p["energy"] = evaluate_scenarios(
                cfg["annual_cost"],
                cfg["scenarios"],
                inject_error=cfg[
                    "inject_error"
                ],
            )

            st.session_state[
                "stage"
            ] = 4

            st.rerun()


    if "energy" in p:

        st.markdown(
            '<div class="card pass">'
            '<b>⚡ ENERGY AGENT → AUDIT AGENT</b><br>'
            '<b>STATUS:</b> SCENARIOS EVALUATED<br>'
            '<span class="small">'
            'Candidate interventions converted '
            'into investment, reduction, saving '
            'and payback outputs.'
            '</span>'
            '</div>',
            unsafe_allow_html=True,
        )


    # ========================================================
    # 4. AUDIT AGENT
    # ========================================================

    if (
        stage == 4
        and not st.session_state[
            "audit_needs_correction"
        ]
    ):

        st.markdown(
            '<div class="handoff">'
            '<b>Human Audit Team:</b> '
            'do not trust the previous output '
            'automatically. Run an independent '
            'verification.'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "🔍 RUN INDEPENDENT AUDIT",
            type="primary",
            use_container_width=True,
        ):

            audit_payload = run_audit_agent(
                cfg["annual_cost"],
                p["energy"],
            )

            p["audit"] = audit_payload

            if (
                audit_payload["status"]
                == "REJECTED"
            ):

                p[
                    "audit_event"
                ] = audit_payload

                st.session_state[
                    "audit_needs_correction"
                ] = True

            else:

                st.session_state[
                    "stage"
                ] = 5

            st.rerun()


    # ========================================================
    # AUDIT REJECT / CORRECTION LOOP
    # ========================================================

    if st.session_state[
        "audit_needs_correction"
    ]:

        ae = p[
            "audit_event"
        ]

        rejected_rows = [

            x

            for x in ae["results"]

            if x["audit_status"]
            == "REJECTED"

        ]

        st.error(
            "🔍 AUDIT AGENT — "
            "CALCULATION REJECTED"
        )

        for x in rejected_rows:

            st.write(
                f'**{x["name"]}** — '
                f'Reported saving: '
                f'€{x["reported_saving"]:,.0f} | '
                f'Expected: '
                f'€{x["expected_saving"]:,.0f} | '
                f'Difference: '
                f'€{x["audit_error"]:,.0f}'
            )

        st.warning(
            "↩ RETURN TO ENERGY TEAM"
        )

        if st.button(
            "⚡ CORRECT & RESUBMIT TO AUDIT",
            type="primary",
            use_container_width=True,
        ):

            p["energy"] = evaluate_scenarios(
                cfg["annual_cost"],
                cfg["scenarios"],
                inject_error=False,
            )

            p["audit"] = run_audit_agent(
                cfg["annual_cost"],
                p["energy"],
            )

            st.session_state[
                "audit_needs_correction"
            ] = False

            if (
                p["audit"]["status"]
                == "PASS"
            ):

                st.session_state[
                    "stage"
                ] = 5

            else:

                st.session_state[
                    "stage"
                ] = 4

            st.rerun()


    # ========================================================
    # VERIFIED SCENARIOS
    # ========================================================

    if (
        "audit" in p
        and p["audit"]["status"]
        == "PASS"
    ):

        st.success(
            "🔍 AUDIT AGENT — PASS • "
            "Verified results released "
            "to Business Agent"
        )

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
                        cfg["annual_cost"]
                        - x["expected_saving"],

                    "Payback (years)":
                        x["payback_years"],

                    "Audit":
                        x["audit_status"],
                }
            )

        df = pd.DataFrame(
            rows
        )

        p[
            "df_rows"
        ] = rows

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
            hide_index=True,
        )


        # ====================================================
        # CHART 1
        # ====================================================

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
            use_container_width=True,
        )


        # ====================================================
        # CHART 2
        # ====================================================

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
            use_container_width=True,
        )


    # ========================================================
    # 5. BUSINESS AGENT
    # ========================================================

    if stage == 5:

        st.markdown(
            '<div class="handoff">'
            '<b>Human Business Team:</b> '
            'compare only audited scenarios '
            'against the target and budget.'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "💼 RUN BUSINESS REVIEW",
            type="primary",
            use_container_width=True,
        ):

            p[
                "business"
            ] = run_business_agent(
                p["audit"],
                cfg["target_percent"],
                cfg["max_budget"],
            )

            st.session_state[
                "stage"
            ] = 6

            st.rerun()


    if "business" in p:

        b = p[
            "business"
        ]

        st.markdown(
            "## 💼 Business Agent Recommendation"
        )

        if b["status"] == "PASS":

            selected = b[
                "selected"
            ]

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
    # 6. MASTER COORDINATOR
    # ========================================================

    if stage == 6:

        st.markdown(
            '<div class="handoff">'
            '<b>Human Coordination Team:</b> '
            'authorize the final orchestration step. '
            'The Master Coordinator can recommend '
            '— not decide.'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "🤖 RUN MASTER COORDINATOR",
            type="primary",
            use_container_width=True,
        ):

            p[
                "coordinator"
            ] = run_coordinator(
                p["data"],
                p["math"],
                p["audit"],
                p["business"],
            )

            st.session_state[
                "stage"
            ] = 7

            st.rerun()


    # ========================================================
    # MASTER RESULT
    # ========================================================

    if "coordinator" in p:

        coord = p[
            "coordinator"
        ]

        st.markdown(
            "## 🤖 HAMA Master Coordinator"
        )

        if (
            coord["status"]
            == "MISSION ACCOMPLISHED"
        ):

            selected = coord[
                "selected"
            ]

            new_cost = (
                cfg["annual_cost"]
                - selected[
                    "expected_saving"
                ]
            )

            st.balloons()

            st.success(
                "### ✅ MISSION ACCOMPLISHED"
            )

            r1, r2, r3, r4 = st.columns(4)

            r1.metric(
                "Initial cost",
                f'€{cfg["annual_cost"]:,.0f}'
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
                f'{cfg["target_percent"]}%'
            )

            st.info(
                "🎓 Educational reinvestment scenario: "
                "the school community may recognize "
                "the successful student startup "
                "through STEM equipment, "
                "an educational visit "
                "or another learning activity."
            )

            st.markdown(
                "### 🧑‍⚖️ HUMAN APPROVAL REQUIRED"
            )

            st.caption(
                "The Master Coordinator provides "
                "a recommendation. "
                "Final decision-making remains "
                "with the human team."
            )

        else:

            st.error(
                f'### ❌ {coord["status"]}'
            )

            st.write(
                coord["message"]
            )


        # ====================================================
        # EXPORT RESULTS
        # ====================================================

        if "df_rows" in p:

            df = pd.DataFrame(
                p["df_rows"]
            )

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
                    cfg["mode"],

                "school": {

                    "area_m2":
                        cfg["area_m2"],

                    "annual_kwh":
                        cfg["annual_kwh"],

                    "annual_cost":
                        cfg["annual_cost"],

                },

                "target_percent":
                    cfg["target_percent"],

                "max_budget":
                    cfg["max_budget"],

                "coordinator":
                    coord,

            }

            st.download_button(
                "Download HAMA Mission Report JSON",

                json.dumps(
                    export_payload,
                    ensure_ascii=False,
                    indent=2,
                ).encode(
                    "utf-8"
                ),

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
    "Estimated savings are not guaranteed "
    "real-world outcomes. "
    "Real deployment requires actual school bills, "
    "technical energy auditing "
    "and validated intervention data."
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="hama-footer">'
    '<div class="brand">'
    'HAMA • HUMAN–AI MULTI-AGENT '
    'VIRTUAL STUDENT STARTUP LAB'
    '</div>'
    '<div class="developer">'
    'Designed &amp; Developed by '
    '<strong>Nikolaos Sampanis</strong> '
    '• PhD Candidate'
    '</div>'
    '<div class="version">'
    'Research Prototype '
    '• Release 1.1 '
    '• Streamlit / Python'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)
