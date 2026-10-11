# TOGAF — The Open Group Architecture Framework for AI Systems

## What is TOGAF?

TOGAF (The Open Group Architecture Framework) is the world's most widely adopted Enterprise
Architecture (EA) framework. It provides a systematic approach for designing, planning, implementing,
and governing enterprise information architecture.

**For AI Architects**: TOGAF gives you the language, structure, and governance model to position
AI systems within the broader enterprise — connecting AI initiatives to business strategy, existing
IT landscape, data governance, and change management.

---

## The Four Architecture Domains (BDAT)

TOGAF organizes enterprise architecture into four domains. Every AI system touches all four:

### B — Business Architecture
Defines the business strategy, governance, organization, and key business processes.

**For AI**: Maps the AI capability to a business process or outcome.
- Which business process does this AI system automate or augment?
- What is the value stream? Where does AI create value?
- What roles/jobs are affected? (change management implications)
- What are the KPIs the AI system must move?

**AI Business Architecture artifacts**:
- Business Motivation Model: vision → mission → goals → objectives → KPIs
- Value Stream Map: where AI touches customer/employee journeys
- Capability Map: new AI capabilities vs existing capabilities
- RACI for AI decision-making (who approves model outputs in high-stakes decisions?)

### D — Data Architecture
Defines the structure of an organization's logical and physical data assets.

**For AI**: This is critical. Data architecture determines what AI is possible.
- What data exists? Where? In what format? At what quality?
- Data governance: who owns each dataset? Who can access it?
- Master data management: canonical entities (customer, product, order)
- Data lineage: where did training data come from? Is it auditable?
- Privacy and residency: where can data travel? (GDPR, data sovereignty)

**AI Data Architecture artifacts**:
- Enterprise Data Map: all data sources, owners, classification, location
- AI Data Lineage: raw data → features → training sets → model outputs
- Data Governance Policy for AI: who approves training datasets?
- Data Quality SLAs: freshness, completeness thresholds per data source

### A — Application Architecture
Defines the individual applications, their interactions, and their relationships to business processes.

**For AI**: Where does the AI system sit in the application landscape?
- Which applications produce data for the AI system?
- Which applications consume AI outputs?
- Is AI embedded in an existing app or a new standalone service?
- What are the integration points? (APIs, event streams, databases)
- How does AI fit into the existing integration architecture? (ESB, API gateway, event bus)

**AI Application Architecture artifacts**:
- Application Landscape Diagram: existing apps + new AI services + their connections
- API Contract: OpenAPI spec for all AI service endpoints
- Event Flow Diagram: data events that trigger AI inference
- Dependency Map: upstream data producers and downstream AI consumers

### T — Technology Architecture
Defines the hardware, software, and network infrastructure.

**For AI**: The compute, storage, and network foundation for AI.
- Cloud provider strategy: single cloud, multi-cloud, hybrid?
- GPU/accelerator strategy: cloud-burst vs reserved vs on-prem
- MLOps platform: where do experiments run? where do models live?
- Network: latency between data store and inference service (critical for real-time AI)
- Security: network segmentation, secrets management, model artifact security

**AI Technology Architecture artifacts**:
- Infrastructure Diagram: compute, storage, network, security zones
- MLOps Platform Design: experiment tracking, model registry, serving infrastructure
- Cost Model: TCO for AI infrastructure (compute, storage, API costs)

---

## The ADM — Architecture Development Method

The ADM is the core of TOGAF: a cycle of phases for developing and managing enterprise architecture.

```
        ┌─────────────────────────────────┐
        │    Requirements Management      │  ← runs throughout ALL phases
        └─────────────────────────────────┘
                        │
        ┌───────────────▼──────────────────┐
        │   Preliminary Phase              │
        │   (Set up EA capability)         │
        └───────────────┬──────────────────┘
                        │
        ┌───────────────▼──────────────────┐
        │   Phase A: Architecture Vision   │
        │   (Scope, stakeholders, vision)  │
        └───────────────┬──────────────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
     Phase B        Phase C        Phase D
    Business      Information    Technology
   Architecture    Systems       Architecture
                 Architecture
          └─────────────┬─────────────┘
                        ▼
        ┌───────────────────────────────────┐
        │   Phase E: Opportunities &        │
        │   Solutions                       │
        └───────────────┬───────────────────┘
                        ▼
        ┌───────────────────────────────────┐
        │   Phase F: Migration Planning     │
        └───────────────┬───────────────────┘
                        ▼
        ┌───────────────────────────────────┐
        │   Phase G: Implementation         │
        │   Governance                      │
        └───────────────┬───────────────────┘
                        ▼
        ┌───────────────────────────────────┐
        │   Phase H: Architecture Change    │
        │   Management                      │
        └───────────────────────────────────┘
```

### Applying ADM to AI Initiatives

**Preliminary Phase** — Set up the EA practice for AI
- Establish AI Architecture Board (governance)
- Define AI Architecture Principles (see below)
- Identify tools: model registry, experiment tracking, architecture repository
- Define AI-specific ADM tailoring

**Phase A — Architecture Vision for an AI Initiative**
Key questions:
- What business problem are we solving with AI?
- Who are the stakeholders? (sponsors, users, regulators, affected employees)
- What is the Target Architecture vision in plain language?
- What are the constraints? (budget, timeline, regulatory, data availability)

Deliverables: Statement of Architecture Work, Stakeholder Map, Architecture Vision Document

**Phase B — Business Architecture**
Map the AI system to business:
- Baseline: How is the process done today (without AI)?
- Target: How does it work with AI? What changes?
- Gap: What organizational changes, training, and process redesign are needed?
- Value: Quantify the business value (time saved, error reduction, revenue impact)

**Phase C — Information Systems Architecture**
Two sub-phases for AI:
1. **Data Architecture**: What data flows into the AI system? From where?
2. **Application Architecture**: What applications interact with the AI system?

Baseline → Target → Gap for both.

**Phase D — Technology Architecture**
Define the target infrastructure:
- AI training environment (cloud, GPU type, auto-scaling)
- AI serving environment (latency requirements, redundancy)
- Integration infrastructure (API gateway, event bus, service mesh)
- Security and compliance infrastructure

**Phase E — Opportunities & Solutions**
- Identify work packages: what needs to be built?
- Sequence: what comes first? (data pipeline before model, platform before product)
- Build-vs-buy-vs-partner decisions for each component
- Identify transition architectures (intermediate states on the way to target)

**Phase F — Migration Planning**
- Full project/program plan with AI-specific considerations:
  - Data migration and preparation timeline
  - Model training and evaluation cycles (not predictable like code builds)
  - User acceptance testing for AI (different from functional testing)
  - Change management and training plan for affected users
  - Parallel-run period (AI system alongside existing process)

**Phase G — Implementation Governance**
- Architecture Review Board (ARB): review implementations for conformance
- AI-specific conformance checks:
  - Does the implementation use approved models and data sources?
  - Are evaluation results above threshold?
  - Is observability in place?
  - Are AI principles being followed?

**Phase H — Architecture Change Management**
- Monitor for changes that necessitate architecture updates:
  - New AI regulations (EU AI Act updates)
  - New model generations (GPT-5, Claude 4, etc.)
  - Significant data drift requiring architecture changes
  - Business strategy changes affecting AI scope

---

## TOGAF AI Architecture Principles

Principles are high-level rules that guide all architectural decisions. Define these upfront:

| # | Principle | Rationale | Implications |
|---|---|---|---|
| 1 | **AI serves business outcomes** | AI is a means, not an end | Every AI project must have measurable business KPIs |
| 2 | **Data is a strategic asset** | AI quality = data quality | Data governance investment is non-negotiable |
| 3 | **AI decisions must be explainable** | Trust and regulation require transparency | Prefer interpretable approaches; log all AI decisions |
| 4 | **Human oversight is maintained** | AI augments, not replaces, human judgment in critical decisions | Define escalation paths; keep humans in the loop for high-stakes outputs |
| 5 | **Privacy by design** | Regulatory compliance + user trust | PII minimization, data residency compliance from day one |
| 6 | **AI systems must be monitored** | Models degrade over time | All AI systems have monitoring dashboards and alerts |
| 7 | **Vendor independence** | Avoid lock-in | Abstract model providers behind interfaces; own your data |
| 8 | **Security is embedded** | AI systems are high-value targets | Security review for all AI components before deployment |

---

## TOGAF Architecture Repository for AI

The Architecture Repository stores all architecture artifacts. For AI teams:

```
Architecture Repository/
├── Architecture Metamodel
│   └── AI component types, relationship types
├── Architecture Landscape
│   ├── Strategic Architecture (3-5 year AI roadmap)
│   ├── Segment Architecture (domain-level AI designs)
│   └── Capability Architecture (specific AI systems)
├── Standards Library
│   ├── Approved LLM providers and models
│   ├── Approved vector databases
│   ├── API design standards
│   └── Data format standards
├── Reference Library
│   ├── AI design patterns (RAG, agentic, fine-tune)
│   ├── Industry reference architectures
│   └── Regulatory guidance (EU AI Act, NIST AI RMF)
└── Governance Log
    ├── Architecture Decision Records (ADRs)
    ├── Compliance waivers
    └── Architecture review outcomes
```

---

## Enterprise Continuum — AI Positioning

TOGAF's Enterprise Continuum classifies architectures from generic to specific:

```
Foundation Architectures          Common Systems          Industry Architectures          Org-Specific
(Generic patterns)                Architectures           (Domain-specific)               Architectures
       │                               │                          │                            │
  RAG Pattern                  Enterprise AI              Healthcare AI              MyCompany
  Agent Pattern                Platform Design            Architecture               Customer AI
  Fine-tune Pattern             Data Mesh                 Financial AI               Platform
                                for AI                    Architecture
```

Use the continuum to avoid reinventing: start from established patterns and customize right.

---

## TOGAF Governance for AI

### AI Architecture Review Board (AI-ARB)
Composition:
- Chief AI Architect (chair)
- Data Governance Officer
- Security Architect
- Business Domain Representatives
- Legal/Compliance Representative
- External AI Ethics Advisor (for high-risk AI)

Review triggers:
- New AI system > $50K budget
- Existing AI system major change (new model, new data source)
- AI system reaching new risk tier (e.g., starts making automated decisions)
- Regulatory change affecting existing AI systems

### Architecture Compliance Levels
| Level | Description | AI Example |
|---|---|---|
| **Conformant** | Fully implements target architecture | Uses approved LLM, meets eval gate, has monitoring |
| **Compliant** | Meets spirit, minor deviations with ARB approval | Uses unapproved vector DB with ARB waiver |
| **Non-compliant** | Significant deviation, must remediate | No eval process, no monitoring, unapproved data |

---

## TOGAF + SDLC Integration

TOGAF is strategic (what to build and why); SDLC is tactical (how to build it). They integrate as:

```
TOGAF ADM                          SDLC
─────────────────────────────────────────────────────
Phase A: Architecture Vision    →  Project Kickoff, Problem Framing
Phase B/C/D: Architecture       →  Requirements, System Design
Phase E/F: Solutions/Migration  →  Sprint Planning, Roadmap
Phase G: Governance             →  Code Review, Architecture Review, Release Gates
Phase H: Change Management      →  Retrospectives, Architecture Evolution
Requirements Management         →  Product Backlog, Continuous Feedback
```

**In practice**: TOGAF runs at the program level (months to years). SDLC runs at the project/sprint
level (days to weeks). The AI Architect bridges both, translating enterprise constraints from TOGAF
into concrete engineering requirements in the SDLC backlog.

---

## TOGAF Deliverables for AI Projects — Quick Reference

| TOGAF Artifact | AI-Specific Content |
|---|---|
| Architecture Vision | AI opportunity statement, stakeholder map, scope |
| Business Architecture | Process maps before/after AI, value quantification |
| Data Architecture | Data lineage, training data governance, privacy classification |
| Application Architecture | AI service APIs, integration points, dependency map |
| Technology Architecture | MLOps platform, GPU infra, serving architecture |
| Architecture Roadmap | AI capability phases, model generations, data maturity milestones |
| Architecture Definition Document | Full system design, all four domains |
| Architecture Requirements Spec | Functional + non-functional requirements for AI system |
| Risk Register | Model risks, data risks, regulatory risks, operational risks |
| ADRs | Every major technology and design decision with rationale |
