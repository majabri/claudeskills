# SDLC — Software Development Life Cycle for AI Systems

## What is SDLC?

SDLC is the structured process governing how software is planned, created, tested, deployed, and
maintained. For AI-driven systems, standard SDLC is extended with data, model, and experiment
management phases — creating **AI-SDLC**.

---

## Core SDLC Models & When to Use Each

### 1. Waterfall
Sequential phases. Each phase fully completes before the next begins.
```
Requirements → Design → Implementation → Verification → Maintenance
```
**Use for AI when**: regulatory compliance (FDA, financial), fixed-scope integrations,
embedded AI in hardware. Never use for model R&D — requirements are too uncertain.

**Risk**: Discovering model doesn't work in "Verification" after months of build.

---

### 2. Agile / Scrum (Most Common for AI Products)
Iterative 2-week sprints. Ship working software every sprint.

```
Product Backlog → Sprint Planning → Sprint (2 weeks) → Sprint Review → Retrospective → repeat
```

**AI-specific adaptations**:
- AI stories include both engineering tasks AND experiment tasks
- "Definition of Done" must include eval metrics, not just unit tests
- Reserve 20% of sprint capacity for model iteration (not just feature work)
- Use "experiment spikes" as story type: time-boxed research with a report output

**Sprint structure for AI teams**:
| Day | Activity |
|---|---|
| 1 | Sprint planning, break down AI stories |
| 2-8 | Feature dev + model experiments running in parallel |
| 9 | Integration + eval runs |
| 10 | Sprint review + demo + retrospective |

---

### 3. Kanban
Continuous flow, work-in-progress limits. Good for AI ops/maintenance teams.

```
Backlog → In Progress → In Review → Done
WIP limits: prevent bottlenecks at model review, data annotation stages
```

**Use for**: ongoing model monitoring, data pipeline maintenance, A/B test management.

---

### 4. DevOps / MLOps (AI-Specific Extension)
Merges Dev + Ops into continuous loops. For AI systems: **MLOps** extends this to include:
- Continuous Training (CT): models retrain on new data automatically
- Continuous Evaluation (CE): every model version is auto-evaluated before deploy
- Continuous Monitoring: drift detection, performance degradation alerts

```
Plan → Code → Build → Test → Release → Deploy → Operate → Monitor → Plan...
                                                              ↑
                                               + Data drift detection
                                               + Model performance tracking
                                               + Automatic retraining triggers
```

---

### 5. Spiral Model
Risk-driven. Each cycle: plan → risk analysis → engineer → evaluate.
**Use for**: large AI programs with novel models, high technical risk, government/defense.

---

## AI-SDLC: The Extended Lifecycle

Standard SDLC phases + AI-specific additions:

```
Phase 0: Problem Framing
  ↓
Phase 1: Data Discovery & Assessment
  ↓
Phase 2: Architecture & Design
  ↓
Phase 3: Data Preparation & Feature Engineering
  ↓
Phase 4: Model Development & Experimentation
  ↓
Phase 5: Evaluation & Validation
  ↓
Phase 6: Deployment & Integration
  ↓
Phase 7: Monitoring & Continuous Improvement
```

### Phase 0 — Problem Framing
- Is ML/AI the right solution? (check: rule-based might be simpler)
- Define success metrics in business terms AND technical terms
- Map out stakeholders: who owns the data? who approves the model?
- Regulatory check: GDPR, CCPA, HIPAA, EU AI Act applicability
- Build-vs-buy decision: fine-tune vs API vs custom train

### Phase 1 — Data Discovery & Assessment
Deliverables: Data Inventory, Data Quality Report, Data Lineage Map

- Catalog all relevant data sources
- Assess quality: completeness, consistency, recency, bias
- Privacy assessment: PII identification, anonymization requirements
- Volume estimate: enough for training? enough for eval?
- Data access agreements: who owns it legally?

**Data readiness scorecard**:
| Dimension | Questions |
|---|---|
| Volume | Enough examples per class/use case? |
| Quality | Missing values, outliers, noise level? |
| Relevance | Does it reflect production distribution? |
| Freshness | How old? Still representative? |
| Bias | Underrepresented groups or scenarios? |
| Legality | Licensed for training use? |

### Phase 2 — Architecture & Design
Deliverables: Architecture Decision Records (ADRs), System Design Doc, Experiment Plan

- Choose architecture pattern (RAG, fine-tune, agentic, etc.)
- Define experiment plan: what models, what hyperparameters, what eval metrics
- Design data pipelines: ingestion, transformation, serving
- Define API contracts: input/output schemas, latency SLAs
- Write ADRs for every major decision (see ADR format below)

**ADR Template**:
```markdown
# ADR-001: Use RAG over Fine-tuning for Knowledge Retrieval

## Status: Accepted

## Context
Our knowledge base updates weekly. Fine-tuning would require weekly retraining cycles
at $X cost. We have 50K documents and user queries are factual lookups.

## Decision
Use RAG with hybrid search. Fine-tuning reserved for query understanding layer only.

## Consequences
+ Knowledge base updates don't require model retraining
+ Answers are grounded and citable
- Retrieval quality depends on chunking and indexing quality
- Added latency of ~200ms for retrieval step
```

### Phase 3 — Data Preparation & Feature Engineering
- Data cleaning: deduplication, normalization, outlier removal
- Annotation: human labeling for supervised tasks (use Label Studio, Scale AI)
- Splitting: train/validation/test split (never contaminate test set)
- For LLMs: prompt-response pair formatting, quality filtering
- Feature stores (if using tabular ML): Feast, Tecton, Hopsworks

### Phase 4 — Model Development & Experimentation
**Experiment tracking is mandatory** — use MLflow, W&B, or Comet:

```python
import mlflow

with mlflow.start_run(run_name="rag-v2-hybrid-search"):
    mlflow.log_params({
        "chunk_size": 512,
        "chunk_overlap": 50,
        "retriever": "hybrid",
        "llm": "claude-sonnet-4"
    })
    
    results = run_eval(config)
    
    mlflow.log_metrics({
        "faithfulness": results.faithfulness,
        "context_recall": results.recall,
        "latency_p95": results.latency_p95
    })
```

**Experiment discipline**:
- Change ONE variable at a time
- Establish a baseline before experimenting
- Document failed experiments — they prevent repeating mistakes
- Gate progress on the eval set (not vibes)

### Phase 5 — Evaluation & Validation
- Offline eval: golden set, domain-specific benchmarks
- Human eval: 100-500 samples rated by subject matter experts
- Red teaming: adversarial inputs, edge cases, jailbreak attempts
- Bias audit: performance across demographic groups, languages
- Regulatory validation: document the eval for compliance artifacts

**Release criteria (gate before Phase 6)**:
- [ ] Primary metric ≥ baseline threshold
- [ ] No regression on critical failure cases
- [ ] Latency P95 within SLA
- [ ] Human eval score ≥ X
- [ ] Red team findings addressed or accepted with mitigation

### Phase 6 — Deployment & Integration
- Staged rollout: internal → beta users → 10% → 50% → 100%
- Feature flags: enable/disable AI features without deploy
- Canary deployment: new model version gets 5% traffic, compare metrics
- Rollback plan: define trigger metrics that auto-roll back (error rate > 2%)
- Integration testing: end-to-end test with real upstream/downstream systems

### Phase 7 — Monitoring & Continuous Improvement
- **Data drift**: input distribution shifting from training distribution
- **Concept drift**: relationship between input and correct output changes
- **Performance degradation**: metrics declining over time (user satisfaction, task completion)
- **Cost monitoring**: token usage, compute costs trending up without explanation

**Monitoring cadence**:
| Check | Frequency |
|---|---|
| Latency / error rate | Real-time alerts |
| User satisfaction | Daily |
| Eval metric spot-check | Weekly |
| Full eval suite | Every deploy |
| Bias audit | Quarterly |
| Full model refresh | When drift detected or quarterly |

---

## SDLC Roles in AI Projects

| Role | Responsibilities |
|---|---|
| **AI Architect** | System design, technology decisions, ADRs, cross-team alignment |
| **ML Engineer** | Model training, experiment infra, MLOps pipelines |
| **Data Engineer** | Data pipelines, feature stores, data quality |
| **AI Product Manager** | Requirements, prioritization, success metrics, stakeholder alignment |
| **ML Researcher** | Novel model approaches, evaluation methodology, publications |
| **AI QA Engineer** | Eval framework, golden sets, red teaming, bias audits |
| **Platform/MLOps Engineer** | Serving infra, CI/CD, monitoring, cost optimization |

---

## SDLC Artifacts Checklist

| Phase | Key Artifacts |
|---|---|
| Problem Framing | Problem Statement, Success Metrics, Go/No-Go Decision |
| Data Discovery | Data Inventory, Quality Report, Privacy Assessment |
| Architecture | ADRs, System Design Doc, API Contracts, Experiment Plan |
| Data Prep | Data Card, Annotation Guidelines, Train/Val/Test Splits |
| Model Dev | Experiment Log, Model Card, Hyperparameter Report |
| Evaluation | Eval Report, Human Eval Results, Red Team Report, Bias Audit |
| Deployment | Deployment Runbook, Rollback Plan, Release Notes |
| Monitoring | Monitoring Dashboard, SLA Report, Drift Alerts, Improvement Backlog |

---

## CI/CD for AI Systems (MLOps Pipeline)

```yaml
# Triggered on every PR + nightly
stages:
  - lint_and_unit_test      # Code quality, unit tests
  - data_validation         # Great Expectations / Soda checks on datasets
  - model_eval              # Run golden set eval, compare to baseline
  - integration_test        # End-to-end API tests with mock LLM
  - security_scan           # Prompt injection, PII leakage tests
  - performance_test        # Latency benchmark at 100 RPS
  - deploy_staging          # Deploy to staging environment
  - smoke_test_staging      # Automated smoke tests in staging
  - deploy_prod_canary      # 5% traffic canary
  - promote_or_rollback     # Auto based on canary metrics
```
