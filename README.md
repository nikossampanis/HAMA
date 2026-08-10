# 🤖 HAMA
## Human–AI Multi-Agent Virtual Student Startup Lab

> **Student teams. Specialized digital agents. One real-world mission.**
>
> HAMA is an educational research prototype that transforms a classroom into a **virtual Human–AI startup**, where students and specialized digital agents collaborate to solve a real school energy decision-making problem.

---

## 🚀 Live Application

### 👉 HAMA Release 1.0

**Live Streamlit App:**  
https://hamasampanis.streamlit.app/

---

## 🎯 The Mission

Imagine a school that wants to reduce its annual energy cost.

The challenge is not simply:

> *“Calculate 15% of the electricity bill.”*

Instead, students receive a startup mission:

> **Design an economically feasible strategy that reduces the school's annual energy cost by at least 15%, while respecting a predefined investment budget.**

To complete the mission, students must work with data, mathematical models, investment scenarios, verification procedures and business constraints.

The final answer is not produced by a single chatbot.

It emerges from a structured **Human–AI multi-agent workflow**.

---

# 🧠 The HAMA Concept

HAMA stands for:

## **Human–AI Multi-Agent**

The central idea is simple:

```text
STUDENT TEAMS
      +
SPECIALIZED DIGITAL AGENTS
      +
STRUCTURED HANDOFFS
      +
INDEPENDENT VERIFICATION
      +
HUMAN DECISION
      =
HAMA
```

Instead of using AI as a system that simply gives students an answer, HAMA distributes the problem across specialized roles.

Each student team works together with a corresponding digital agent.

---

# 🏢 A Virtual Student Startup

The classroom operates as a small virtual company.

Each team has a specific responsibility.

| Student Team | Digital Agent | Mission |
|---|---|---|
| 📊 Data Team | Data Agent | Validate school and energy data |
| 🧮 Mathematics Team | Math Agent | Transform the mission into mathematical KPIs |
| ⚡ Energy Team | Energy Agent | Evaluate energy-saving scenarios |
| 🔍 Audit Team | Audit Agent | Independently verify calculations |
| 💼 Business Team | Business Agent | Evaluate investment constraints and payback |
| 🤖 Startup Coordination | Master Coordinator | Integrate validated results |

The complete workflow is:

```text
DATA
  ↓
MATHEMATICS
  ↓
ENERGY
  ↓
AUDIT
  ↓
BUSINESS
  ↓
MASTER COORDINATOR
  ↓
HUMAN APPROVAL
```

---

# ⚡ The School Energy Challenge

HAMA Release 1.0 includes a demonstration school with the following baseline:

```text
School area          = 1,500 m²
Annual consumption   = 76,500 kWh
Annual energy cost   = €20,400
Target reduction     = 15%
Default budget       = €15,000
```

From these values, the system calculates indicators such as:

```text
Energy Intensity
kWh / m² / year

Cost Intensity
€ / m² / year

Effective Energy Cost
€ / kWh
```

The business mission is then converted into a mathematical condition.

For example:

```text
Initial annual cost = €20,400

Target reduction = 15%

Required saving = €3,060/year

Maximum acceptable new cost = €17,340/year
```

This transforms a real-world sustainability problem into a mathematical decision problem.

---

# 🧪 Investment Scenarios

Release 1.0 includes three editable example scenarios.

| Scenario | Investment | Estimated Reduction |
|---|---:|---:|
| 💡 LED & Smart Lighting | €7,500 | 16% |
| 🌡 Smart HVAC Control | €13,500 | 23% |
| 🏢 Integrated Energy Upgrade | €27,000 | 31% |

For every scenario, HAMA calculates:

- annual financial saving,
- projected new annual cost,
- reduction percentage,
- investment cost,
- simple payback period,
- audit status.

The values are fully editable in the application.

This allows the same environment to be used as either a predefined classroom demonstration or a configurable decision-making laboratory.

---

# 🔍 The Audit Agent

## This is one of the core ideas behind HAMA.

AI-generated or algorithmically produced results should **not automatically be trusted**.

HAMA therefore includes an independent verification layer.

The **Audit Agent** recalculates critical numerical outputs before they can influence the final decision.

The workflow becomes:

```text
CALCULATE
    ↓
VERIFY
    ↓
PASS
```

or, if something is wrong:

```text
CALCULATE
    ↓
VERIFY
    ↓
REJECT
    ↓
RETURN
    ↓
CORRECT
    ↓
RESUBMIT
    ↓
VERIFY
```

---

# 💥 Controlled Failure Demonstration

Release 1.0 includes an optional:

## 🎓 Demo Audit Error

When enabled, the Energy Agent intentionally reports an incorrect result.

Example:

```text
Reported saving:
€5,692

Correct saving:
€4,692
```

The Audit Agent independently recalculates the value and detects:

```text
Difference = €1,000
```

The system then produces:

```text
AUDIT AGENT
STATUS: REJECTED

RETURN TO ENERGY AGENT
```

The result is corrected, resubmitted and verified again.

```text
ENERGY AGENT
RESUBMITTED

AUDIT AGENT
PASS
```

This controlled failure is not intended to simulate the natural error rate of AI systems.

It is an **educational mechanism for making verification visible**.

---

# 💼 From Mathematics to Entrepreneurship

Energy efficiency alone does not determine the final decision.

A solution may save more energy but still be economically impossible.

For example:

```text
Scenario C

Reduction:
31%

Investment:
€27,000

Available budget:
€15,000
```

Despite achieving the greatest reduction, the scenario violates the investment constraint.

Therefore:

```text
TECHNICALLY ATTRACTIVE
≠
BUSINESS FEASIBLE
```

Students must evaluate multiple criteria instead of simply selecting the largest percentage.

This connects:

**mathematics → modelling → constraints → entrepreneurship → decision-making**

---

# 🤖 Master Coordinator

The Master Coordinator acts as the final orchestration layer.

It verifies that the required stages have successfully completed:

```text
DATA       → PASS
MATH       → PASS
AUDIT      → PASS
BUSINESS   → PASS
```

and checks whether the startup mission has been achieved.

If all conditions are satisfied:

# ✅ MISSION ACCOMPLISHED

The application presents:

- initial annual cost,
- projected new cost,
- annual saving,
- achieved reduction,
- mission target,
- selected investment,
- payback period.

However, the final stage remains:

# 🧑‍⚖️ HUMAN APPROVAL REQUIRED

The system provides a recommendation.

The human team retains responsibility for the final decision.

---

# 🎓 Educational Philosophy

HAMA is based on a simple idea:

> **Students should not learn merely how to ask AI for answers.  
> They should learn how to work with AI without surrendering their judgement to it.**

The intended learning process is:

```text
COLLECT
   ↓
MODEL
   ↓
CALCULATE
   ↓
VERIFY
   ↓
QUESTION
   ↓
COMPARE
   ↓
DECIDE
```

The student therefore remains inside the decision loop.

---

# 🧮 Mathematical Learning

The prototype provides an applied environment for concepts such as:

- percentages,
- ratios,
- unit rates,
- mathematical modelling,
- inequalities,
- cost functions,
- normalized indicators,
- multi-criteria comparison,
- simple payback period,
- decision-making under constraints.

Instead of solving:

```text
What is 15% of €20,400?
```

students investigate:

> **Which intervention can achieve at least a 15% reduction while remaining inside the available budget, and how can we justify that decision mathematically?**

The arithmetic may be simple.

The **decision structure is not**.

---

# 🌱 Sustainability & School Context

The energy problem provides a real-world context connecting:

- mathematics,
- environmental education,
- energy literacy,
- economics,
- AI literacy,
- entrepreneurship,
- collaborative problem solving.

HAMA is not an energy certification tool.

It is an **educational decision laboratory**.

Real-world deployment would require actual school bills, technical inspection and validated engineering estimates.

---

# 🖥️ Application Modes

## 1️⃣ Demo School

Uses predefined values for immediate classroom or conference demonstration.

Perfect for showing the complete HAMA workflow in a few minutes.

## 2️⃣ Real School Data

Allows the user to enter:

- school area,
- annual electricity consumption,
- annual total energy cost.

The application then recalculates the entire HAMA workflow using the supplied data.

---

# 📊 Interactive Decision Dashboard

The application includes:

- KPI cards,
- energy intensity indicators,
- financial indicators,
- verified scenario tables,
- interactive Plotly charts,
- investment versus saving analysis,
- audit messages,
- agent-to-agent communication logs,
- final mission evaluation.

Results can also be exported as:

```text
CSV
JSON
```

for further analysis.

---

# 🛰️ Agent-to-Agent Communication

One of the design goals of HAMA is to make the reasoning pipeline visible.

Instead of hiding intermediate steps, the application exposes structured handoffs such as:

```text
DATA AGENT
      ↓
MATH AGENT

MATH AGENT
      ↓
ENERGY AGENT

ENERGY AGENT
      ↓
AUDIT AGENT
```

and, when verification fails:

```text
AUDIT AGENT
      ↓
REJECT
      ↓
ENERGY AGENT
      ↓
RESUBMIT
```

This makes the workflow observable to both students and educators.

---

# 🧱 Architecture

```text
HAMA/
│
├── app.py
│
├── agents/
│   ├── data_agent.py
│   ├── math_agent.py
│   ├── energy_agent.py
│   ├── audit_agent.py
│   ├── business_agent.py
│   └── coordinator.py
│
├── data/
│   └── scenarios.py
│
├── .streamlit/
│   └── config.toml
│
├── requirements.txt
│
└── README.md
```

The prototype uses a modular architecture rather than placing the entire system inside a single Python script.

Each agent performs a defined task.

---

# ⚙️ Technology Stack

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-purple?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-blueviolet?logo=plotly)

Core technologies:

```text
Python
Streamlit
Pandas
Plotly
```

Release 1.0 requires **no external LLM API key**.

---

# 🧠 Are These Autonomous AI Agents?

Not yet.

And this distinction is intentional.

HAMA Release 1.0 is a **proof-of-concept agentic educational architecture**.

The agents are implemented as deterministic Python modules with:

```text
DEFINED ROLE
DEFINED INPUT
DEFINED PROCESS
DEFINED OUTPUT
DEFINED HANDOFF
```

This makes Release 1.0:

- transparent,
- reproducible,
- auditable,
- reliable for classroom demonstrations,
- independent of external API availability.

Future versions may replace selected deterministic agents with LLM-backed agents while maintaining the same verification architecture.

---

# 🔮 Roadmap

## HAMA Release 2.0

Potential extensions include:

```text
✓ LLM-backed specialist agents
✓ Natural-language agent-to-agent communication
✓ Persistent mission logs
✓ Student approval/rejection controls
✓ Greek school energy benchmarking
✓ CO₂ indicators
✓ Real electricity bill analysis
✓ Automated mission report generation
✓ Sensitivity analysis
✓ Optimization under budget constraints
```

A future architecture could therefore become:

```text
STUDENT TEAM
      ↕
LLM AGENT
      ↕
SPECIALIST AGENT
      ↕
AUDIT AGENT
      ↕
MASTER COORDINATOR
      ↕
HUMAN APPROVAL
```

---

# 🔬 Research Direction

HAMA can support future classroom research comparing:

```text
Human-only problem solving

vs.

Human + Single AI Assistant

vs.

Human + Multi-Agent HAMA Workflow
```

Potential research variables include:

- mathematical reasoning,
- error detection,
- decision quality,
- AI literacy,
- calibrated trust,
- collaborative regulation,
- student agency.

Release 1.0 demonstrates the **technical and pedagogical feasibility of the workflow**.

It does not yet claim experimentally proven learning gains.

---

# 📚 Research Background

The project is inspired by research in:

- Human–AI collaboration,
- multi-agent learning environments,
- socially shared regulation,
- mathematical modelling,
- project-based learning,
- entrepreneurship education,
- school energy benchmarking.

Relevant literature discussed in the associated research work includes DOI references such as:

```text
10.1111/bjet.13325
10.1111/bjet.13534
10.1016/j.compedu.2025.105472
10.1016/j.compedu.2025.105489
10.1007/s41959-022-00078-8
10.1007/s41959-023-00099-x
10.1016/j.rser.2014.08.010
10.1016/j.enbuild.2021.111150
```

---

# 🚀 Running HAMA Locally

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

Move into the project directory:

```bash
cd HAMA
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

---

# 🌐 Deployment

HAMA can be deployed directly through **Streamlit Community Cloud**.

The current public prototype is available at:

### https://hamasampanis.streamlit.app/

---

# ⚠️ Important Disclaimer

HAMA is an **educational and research prototype**.

The energy-saving percentages included in the demo are configurable educational scenarios.

They should not be interpreted as guaranteed performance estimates for a real school building.

Real-world implementation requires:

- actual electricity bills,
- validated building data,
- technical energy auditing,
- engineering assessment,
- verified intervention costs.

---

## 🌍 Language

HAMA Release 1.0 currently provides a **Greek-language user interface**, reflecting
its initial development for Greek secondary education and classroom experimentation.

The project documentation is maintained in English to support international
academic visibility, reproducibility and future collaboration.

A bilingual Greek/English interface is planned for a future release.
# 👨‍💻 Author

## Nikolaos Sampanis

**Designed & Developed by Nikolaos Sampanis**

PhD Candidate  
Mathematics • Artificial Intelligence • Educational Technology

---

# 💡 The HAMA Principle

> ### AI should not remove students from the reasoning process.
>
> ### It should create new reasons for them to think, verify and decide.

---

## 🤖 HAMA

### Human–AI Multi-Agent Virtual Student Startup Lab

**From AI-generated answers to Human–AI verified decisions.**


