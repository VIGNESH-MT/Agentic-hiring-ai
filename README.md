# Agentic Hiring Intelligence Platform

Deterministic • Explainable • Governance-First Decision Intelligence for Hiring

<p align="center">
  <b>Not an ATS. Not an LLM demo.</b><br/>
  <b>A production-grade decision intelligence system for high-stakes hiring.</b>
</p>

<p align="center">
  <a href="#why-this-project">Why This Project</a> •
  <a href="#core-design-principles">Core Principles</a> •
  <a href="#system-architecture">Architecture</a> •
  <a href="#capabilities">Capabilities</a> •
  <a href="#local-demo">Local Demo</a> •
  <a href="#technology-choices">Technology</a> •
  <a href="#intended-audience">Audience</a>
</p>

---

## Why This Project

Most AI hiring tools reduce hiring to a similarity-scoring problem.

That approach does not survive real-world deployment, regulatory scrutiny,
or organizational accountability.

Hiring is not a prediction task.  
It is a **governed decision process**.

This project is built on that premise.

### What typical systems fail at

- Opaque similarity or embedding scores  
- Unverifiable LLM reasoning  
- No causal attribution  
- No bias governance  
- No audit trail  
- No enforceable human accountability  

Such systems cannot be defended — technically, legally, or ethically.

### What this system is designed to do

- Deterministic, agent-based decision reasoning  
- Explicit hiring policy encoded as executable logic  
- Bias-aware, bounded, and reversible adjustments  
- Causal and counterfactual analysis  
- Immutable, replayable audit logs  
- Human-in-the-loop enforcement by design  

This is a system intended to be **deployed, audited, and defended**.

---

## Core Design Principles

- **Models generate signals — agents make decisions**
- **Policy is code, not configuration afterthought**
- **Every decision must be explainable, replayable, and attributable**
- **Uncertainty triggers abstention, not hallucination**
- **Humans retain accountability at all times**

This is decision engineering, not model experimentation.

---
```bash
## System Architecture

Resumes / Job Descriptions
↓
Skill Extraction
(Exact • Fuzzy • Controlled Semantic)
↓
Canonical Skill Normalization
↓
Baseline Interpretable Model
↓
Agentic Decision Layer
├─ Alignment Agent
├─ Bias-Aware Agent
├─ Calibration Agent
├─ Confidence & Abstention Agent
├─ Causal Impact Agent
├─ Stability & Sensitivity Agent
├─ Counterfactual Simulation Agent
├─ Hiring Committee & Panel Agents
↓
Governance & Control Layer
├─ Risk Profiling
├─ Human Override Enforcement
├─ Immutable Audit Logging
↓
Recruiter, Committee & Executive Outputs
```
The architecture prioritizes determinism, testability, and governance over raw model complexity.

---

## Capabilities

### Agentic Decision System (Not Just ML)

- Each agent has a single, well-defined responsibility  
- Deterministic execution paths  
- Fully testable and auditable logic  
- No hallucinations in decision flow  

### Bias-Aware by Construction

- Job description inflation detection  
- Skill density imbalance checks  
- Vocabulary and proxy bias heuristics  
- Bounded, transparent, reversible score adjustments  

Bias mitigation is enforced policy, not post-hoc explanation.

---

### Causal & Counterfactual Reasoning

- Which signals materially affected the decision?  
- What is the minimal change required to flip the outcome?  
- Decision stability classification: **ROBUST** vs **FRAGILE**  

This enables defensible explanations, not narrative justifications.

---

### Confidence & Abstention Logic

- Confidence is not a score  
- System can explicitly refuse to decide under uncertainty  
- Mandatory escalation to human review when required  

Abstention is treated as a first-class outcome.

---

### Audit & Compliance Readiness

- Immutable decision traces (JSON / Parquet)  
- Versioned models, agents, and policies  
- Mandatory justification for human overrides  
- Every decision is replayable and inspectable  

Designed for internal audit, legal review, and external scrutiny.

---

### Executive-Grade Outputs

- Recruiter-friendly summaries  
- Hiring committee simulations  
- Offer probability estimation  
- Board-safe, regulator-safe decision explanations  

Built for real organizational workflows.

---

## Local Demo

```bash
git clone https://github.com/your-username/agentic-hiring-intelligence.git
cd agentic-hiring-intelligence

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```
Open: http://localhost:8501

Example Outputs

Match outcome with causal explanation

Matched vs missing skills

Bias flags (when triggered)

Decision stability: ROBUST / FRAGILE

Human review requirement

Machine-readable audit logs

This system provides decision support — not blind automation.
```bash
Technology Choices

Python

scikit-learn (interpretable ML)

LangChain (tool orchestration, not free-form reasoning)

Pydantic (schema-safe contracts)

Streamlit (decision review interface)

RapidFuzz / TF-IDF (controlled NLP)

Parquet / JSON (audit-friendly storage)

Every dependency is chosen for predictability, traceability, and governance.
```
Repository Structure
```bash
agentic-hiring-intelligence/
│
├── app.py
├── README.md
├── requirements.txt
│
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_interpretable_modeling.ipynb
│   └── 03_skills_catalog_integration.ipynb
│
├── src/
│   ├── agents/
│   ├── matching/
│   ├── skills/
│   ├── governance/
│   └── config/
│
├── mcp_server/
├── outputs/
├── tests/
└── docs/
```
---

## Intended Audience

This project is designed for practitioners and teams working on
**high-stakes, real-world decision systems**, including:

- **Senior / Staff / Principal Engineers**
- **AI Architects & Platform Leads**
- **Hiring Technology Teams**
- **Responsible AI & Governance Groups**
- **Decision Intelligence Researchers**

If you care about **explainability, fairness, auditability, and deployability**,  
this system is built for you.

---

## Why This Project Exists

**Not a toy.**  
**Not an LLM wrapper.**  
**Not a demo.**

This is **end-to-end AI system design for high-stakes decision-making** —
implemented with the constraints of real organizations in mind:
regulation, accountability, failure modes, and human oversight.

---

## Author

**Vignesh Murugesan**  
AI / Data Science Engineer  

**Focus Areas**  
Agentic AI • Decision Intelligence • Governed & Responsible ML
