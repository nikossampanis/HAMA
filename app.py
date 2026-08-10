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


st.set_page_config(
    page_title="HAMA School Energy Startup",
    page_icon="🤖",
    layout="wide",
)

st.markdown("""
<style>
.block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
.hama-title {font-size: 2.4rem; font-weight: 800; margin-bottom: .2rem;}
.hama-sub {opacity: .78; margin-bottom: 1.2rem;}
.card {
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 16px;
    padding: 1rem 1.1rem;
    background: rgba(255,255,255,.03);
    margin-bottom: .8rem;
}
.pass {border-left: 6px solid #00c2a8;}
.reject {border-left: 6px solid #ff5f6d;}
.wait {border-left: 6px solid #f4c95d;}
.small {font-size: .88rem; opacity: .8;}
.agent-flow {
    font-weight: 700;
    text-align:center;
    padding:.8rem;
    border-radius: 12px;
    border:1px solid rgba(255,255,255,.10);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hama-title">HAMA — School Energy Startup Lab</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hama-sub">Human–AI Master Agent • Μαθητική επιχειρηματικότητα • Μαθηματική μοντελοποίηση • Ενεργειακή απόφαση</div>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("🎯 Mission Control")
    mode = st.radio("Τρόπος λειτουργίας", ["Demo School", "Real School Data"])
    target_percent = st.slider("Στόχος μείωσης κόστους (%)", 5, 40, 15, 1)
    max_budget_enabled = st.checkbox("Περιορισμός επενδυτικού budget", value=True)
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
        help="Εισάγει σκόπιμο λάθος 1.000 € στο Σενάριο Β για να φανεί ο έλεγχος του Audit Agent."
    )
    st.caption("Οι agents λειτουργούν με δομημένα handoffs — χωρίς εξωτερικό API.")

if mode == "Demo School":
    area_m2 = 1500.0
    annual_kwh = 76500.0
    annual_cost = 20400.0
else:
    st.subheader("🏫 Real School Data")
    c1, c2, c3 = st.columns(3)
    with c1:
        area_m2 = st.number_input("Επιφάνεια σχολείου (m²)", min_value=1.0, value=1500.0, step=50.0)
    with c2:
        annual_kwh = st.number_input("Ετήσια κατανάλωση (kWh)", min_value=1.0, value=76500.0, step=500.0)
    with c3:
        annual_cost = st.number_input("Συνολικό ετήσιο κόστος (€)", min_value=1.0, value=20400.0, step=100.0)

st.markdown("### 🚀 Startup Mission")
m1, m2, m3, m4 = st.columns(4)
m1.metric("School area", f"{area_m2:,.0f} m²")
m2.metric("Annual energy", f"{annual_kwh:,.0f} kWh")
m3.metric("Annual cost", f"€{annual_cost:,.0f}")
m4.metric("Target reduction", f"{target_percent}%")

st.progress(min(target_percent / 40, 1.0), text=f"Mission KPI: μείωση ετήσιου κόστους κατά τουλάχιστον {target_percent}%")

st.markdown("### 🤝 Human–AI Master Agent Workflow")
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
        st.markdown(f'<div class="agent-flow">{icon}<br>{name}</div>', unsafe_allow_html=True)

st.divider()

# Editable scenarios
st.markdown("### 🧪 Επενδυτικά σενάρια")
scenarios = deepcopy(DEFAULT_SCENARIOS)
edited = []
for i, sc in enumerate(scenarios):
    with st.expander(sc["name"], expanded=(i == 0)):
        name = st.text_input("Όνομα", value=sc["name"], key=f"name_{i}")
        investment = st.number_input(
            "Κόστος επένδυσης (€)", min_value=0.0, value=float(sc["investment_cost"]),
            step=500.0, key=f"inv_{i}"
        )
        reduction = st.slider(
            "Εκτιμώμενη μείωση κόστους (%)", 0.0, 60.0,
            float(sc["reduction_percent"]), 0.5, key=f"red_{i}"
        )
        description = st.text_input("Περιγραφή", value=sc["description"], key=f"desc_{i}")
        edited.append({
            "name": name,
            "investment_cost": investment,
            "reduction_percent": reduction,
            "description": description,
        })
scenarios = edited

run = st.button("▶ RUN HAMA MISSION", type="primary", use_container_width=True)

if run:
    st.session_state["ran"] = True
    st.session_state["payloads"] = {}

    data_payload = run_data_agent(area_m2, annual_kwh, annual_cost)
    math_payload = run_math_agent(data_payload, target_percent)
    energy_payload = evaluate_scenarios(annual_cost, scenarios, inject_error=inject_error)
    audit_payload = run_audit_agent(annual_cost, energy_payload)

    # Αν υπάρχει σκόπιμο audit error, κρατάμε το rejection ως εκπαιδευτικό event
    # και κάνουμε auto-resubmit ώστε το demo να μπορεί να ολοκληρωθεί.
    audit_event = None
    if audit_payload["status"] == "REJECTED":
        audit_event = audit_payload
        corrected_energy_payload = evaluate_scenarios(annual_cost, scenarios, inject_error=False)
        audit_payload = run_audit_agent(annual_cost, corrected_energy_payload)

    business_payload = run_business_agent(
        audit_payload,
        target_percent,
        max_budget if max_budget_enabled else None,
    )
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

if st.session_state.get("ran"):
    p = st.session_state["payloads"]
    st.markdown("## 🛰 Agent Communication Log")

    # Data Agent
    d = p["data"]
    cls = "pass" if d["status"] == "PASS" else "reject"
    st.markdown(f"""
    <div class="card {cls}">
      <b>📊 DATA AGENT → MATH AGENT</b><br>
      STATUS: {d["status"]}<br>
      <span class="small">{d["message"]}</span>
    </div>
    """, unsafe_allow_html=True)

    if d["status"] == "PASS":
        c1, c2, c3 = st.columns(3)
        c1.metric("Energy intensity", f'{d["eui"]:.2f} kWh/m²/year')
        c2.metric("Cost intensity", f'€{d["cost_intensity"]:.2f}/m²/year')
        c3.metric("Effective cost", f'€{d["effective_price"]:.3f}/kWh')

    # Math Agent
    m = p["math"]
    cls = "pass" if m["status"] == "PASS" else "wait"
    st.markdown(f"""
    <div class="card {cls}">
      <b>🧮 MATH AGENT → ENERGY AGENT</b><br>
      STATUS: {m["status"]}<br>
      <span class="small">{m["message"]}</span>
    </div>
    """, unsafe_allow_html=True)

    if m["status"] == "PASS":
        c1, c2 = st.columns(2)
        c1.metric("Required annual saving", f'€{m["required_saving"]:,.0f}')
        c2.metric("Maximum target cost", f'€{m["target_cost"]:,.0f}')

    # Audit teaching event
    if p.get("audit_event") is not None:
        ae = p["audit_event"]
        rejected_rows = [x for x in ae["results"] if x["audit_status"] == "REJECTED"]
        st.error("🔍 AUDIT AGENT: Εντοπίστηκε λάθος — RETURN TO ENERGY TEAM")
        for x in rejected_rows:
            st.write(
                f'**{x["name"]}**: αναφέρθηκαν €{x["reported_saving"]:,.0f}, '
                f'αναμένονταν €{x["expected_saving"]:,.0f}. '
                f'Διαφορά: €{x["audit_error"]:,.0f}.'
            )
        st.success("⚡ ENERGY AGENT — RESUBMITTED • 🔍 AUDIT AGENT — PASS")

    # Audited scenario table
    a = p["audit"]
    rows = []
    for x in a["results"]:
        rows.append({
            "Scenario": x["name"],
            "Investment (€)": x["investment_cost"],
            "Reduction (%)": x["reduction_percent"],
            "Annual saving (€)": x["expected_saving"],
            "New annual cost (€)": annual_cost - x["expected_saving"],
            "Payback (years)": x["payback_years"],
            "Audit": x["audit_status"],
        })
    df = pd.DataFrame(rows)

    st.markdown("### 📈 Verified Scenario Comparison")
    st.dataframe(
        df.style.format({
            "Investment (€)": "{:,.0f}",
            "Reduction (%)": "{:.1f}",
            "Annual saving (€)": "{:,.0f}",
            "New annual cost (€)": "{:,.0f}",
            "Payback (years)": "{:.2f}",
        }),
        use_container_width=True,
        hide_index=True
    )

    fig = px.bar(
        df,
        x="Scenario",
        y="Annual saving (€)",
        text_auto=".2s",
        title="Verified annual savings by scenario",
    )
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(
        df,
        x="Investment (€)",
        y="Annual saving (€)",
        size="Reduction (%)",
        hover_name="Scenario",
        title="Investment vs annual saving",
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Business / Coordinator
    b = p["business"]
    if b["status"] == "PASS":
        selected = b["selected"]
        st.markdown("## 💼 Business Agent Recommendation")
        st.success(f'Προτεινόμενο σενάριο: **{selected["name"]}**')
        q1, q2, q3, q4 = st.columns(4)
        q1.metric("Investment", f'€{selected["investment_cost"]:,.0f}')
        q2.metric("Reduction", f'{selected["reduction_percent"]:.1f}%')
        q3.metric("Annual saving", f'€{selected["expected_saving"]:,.0f}')
        q4.metric("Payback", f'{selected["payback_years"]:.2f} years')
    else:
        st.warning(b["message"])

    coord = p["coordinator"]
    st.markdown("## 🤖 Master Coordinator")
    if coord["status"] == "MISSION ACCOMPLISHED":
        selected = coord["selected"]
        new_cost = annual_cost - selected["expected_saving"]
        st.balloons()
        st.success("### ✅ MISSION ACCOMPLISHED")
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Initial cost", f"€{annual_cost:,.0f}")
        r2.metric("New cost", f"€{new_cost:,.0f}")
        r3.metric("Achieved", f'{selected["reduction_percent"]:.1f}%')
        r4.metric("Target", f"{target_percent}%")
        st.info(
            "🎓 Εκπαιδευτικό reinvestment scenario: η σχολική κοινότητα μπορεί να "
            "αναγνωρίσει την επιτυχία με STEM εξοπλισμό, εκπαιδευτική επίσκεψη ή άλλη δράση."
        )
    else:
        st.error(f'### ❌ {coord["status"]}')
        st.write(coord["message"])

    # Export
    st.markdown("### 📦 Export")
    csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "Download verified scenarios CSV",
        csv_bytes,
        file_name="hama_verified_scenarios.csv",
        mime="text/csv",
    )

    export_payload = {
        "mode": mode,
        "school": {
            "area_m2": area_m2,
            "annual_kwh": annual_kwh,
            "annual_cost": annual_cost,
        },
        "target_percent": target_percent,
        "max_budget": max_budget if max_budget_enabled else None,
        "coordinator": coord,
    }
    st.download_button(
        "Download mission report JSON",
        json.dumps(export_payload, ensure_ascii=False, indent=2).encode("utf-8"),
        file_name="hama_mission_report.json",
        mime="application/json",
    )

st.divider()
st.caption(
    "HAMA educational prototype • The app does not claim that estimated savings are guaranteed "
    "real-world outcomes. Real deployment requires actual bills, technical audit and validated intervention data."
)
