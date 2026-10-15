# claudeskills

Amir Jabri's Claude skills, kept in one place so they can be edited once and picked up everywhere.

**72 skills in 11 installable plugins.** One folder per skill — edit `SKILL.md`, commit, push, and every machine that has the marketplace picks it up on the next update.

## Install

```bash
claude plugin marketplace add majabri/claudeskills

# then install only what that machine needs
claude plugin install engineering@claudeskills
claude plugin install lovable@claudeskills
```

## Update after you edit a skill

```bash
git add -A && git commit -m "tighten lovable/lovabledatabase" && git push
claude plugin marketplace update claudeskills   # on each machine
```

Skills are namespaced by their plugin, so `lovable/skills/lovabledatabase/SKILL.md` is invoked as `lovable:lovabledatabase`.

A session can also read any skill directly, without installing it:

```
https://raw.githubusercontent.com/majabri/claudeskills/main/plugins/<plugin>/skills/<skill>/SKILL.md
```

## Layout

```
.claude-plugin/marketplace.json   # the catalog — add an entry here for a new plugin
plugins/
  <plugin>/
    .claude-plugin/plugin.json    # name, version, author
    skills/
      <skill-name>/SKILL.md       # edit here
```

## Adding a new skill

1. `mkdir -p plugins/<plugin>/skills/<skill-name>` and write `SKILL.md` with `name:` and `description:` frontmatter.
2. Commit and push. No manifest change needed — skills are auto-discovered inside `skills/`.
3. `claude plugin marketplace update claudeskills` on each machine.

A whole new plugin also needs an entry in `.claude-plugin/marketplace.json`. Validate before pushing:

```bash
claude plugin validate .
```

## Contents

### `engineering` — 10 skills

Software engineering across four altitudes (debug, build, operate, architect) plus AI architecture, MCP server authoring, UI testing, web artifacts, and project management.

| skill | invoked as | description |
|---|---|---|
| `ai-architect` | `engineering:ai-architect` | Transform Claude into a world-class AI Architect and Enterprise Architecture expert for designing, building, and governing production AI systems end-to-end. Tri… |
| `devops` | `engineering:devops` | Use this skill as the entry point for substantial software engineering work — building features, fixing bugs, reviewing PRs, designing systems, handling product… |
| `mcp-builder` | `engineering:mcp-builder` | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when b… |
| `project-management` | `engineering:project-management` | Use this skill as the entry point for ANY project management work — planning projects, running sprints, managing stakeholders, handling risk, writing charters, … |
| `software-l0-debug` | `engineering:software-l0-debug` | Use this skill whenever the user is troubleshooting a specific bug, error, exception, traceback, failing test, or any "why is this not working" question at the … |
| `software-l1-operate` | `engineering:software-l1-operate` | Use this skill whenever the user is dealing with a live system in trouble, an active or past production incident, performance issues under load, on-call duties,… |
| `software-l2-build` | `engineering:software-l2-build` | Use this skill whenever the user is doing code-level engineering at the module, feature, or class scale — designing new functions/modules/APIs, refactoring exis… |
| `software-l3-architect` | `engineering:software-l3-architect` | Use this skill for system-level or architecture engineering work — designing new systems/services, planning migrations, choosing foundational technologies, desi… |
| `ui-tester` | `engineering:ui-tester` | Autonomous end-to-end UI and product feature tester that replaces or front-runs human QA for web platforms. Walks a live application in the browser page by page… |
| `web-artifacts-builder` | `engineering:web-artifacts-builder` | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for… |


### `documents` — 8 skills

Document and file production: Word, PDF, PowerPoint, Excel, Claude Docs, Google Workspace, doc co-authoring, and internal comms.

| skill | invoked as | description |
|---|---|---|
| `doc-coauthoring` | `documents:doc-coauthoring` | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs,… |
| `docs` | `documents:docs` | 'docs (editable docs people share and comment on; the default for any document, named as a doc or not: a document, report, proposal, resume, cover letter, lette… |
| `docx` | `documents:docx` | Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx) or Word templates (.dotx). Triggers include: any mention of M… |
| `google-workspace` | `documents:google-workspace` | Read this before the first Google Drive, Docs, Sheets or Slides connector call whenever the task creates or changes a Google file. Use this skill whenever the u… |
| `internal-comms` | `documents:internal-comms` | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever … |
| `pdf` | `documents:pdf` | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple P… |
| `pptx` | `documents:pptx` | Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentat… |
| `xlsx` | `documents:xlsx` | Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xl… |


### `creative` — 7 skills

Visual and creative work: canvas design, algorithmic art, brand guidelines, theming, Slack GIFs, short-form video packages, and marketing/brand expertise.

| skill | invoked as | description |
|---|---|---|
| `algorithmic-art` | `creative:algorithmic-art` | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generati… |
| `brand-guidelines` | `creative:brand-guidelines` | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand color… |
| `canvas-design` | `creative:canvas-design` | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, d… |
| `marketing-expert` | `creative:marketing-expert` | Use for creative, design, and marketing work spanning brand identity (logos, naming, color, typography, brand systems), digital and product design (websites, la… |
| `short-form-video-package` | `creative:short-form-video-package` | Use this skill whenever the user wants to create, make, or produce a video of any kind — short film, explainer, social media post (TikTok, Reels, Shorts), ad, f… |
| `slack-gif-creator` | `creative:slack-gif-creator` | Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request a… |
| `theme-factory` | `creative:theme-factory` | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fo… |


### `personal` — 6 skills

Amir's own working set: NEXUS project coordination, morning brief, memory import, skill authoring, privacy/legal compliance, and the trading desk.

| skill | invoked as | description |
|---|---|---|
| `import-memory` | `personal:import-memory` | Import a memory export from another AI assistant into Claude's memory — conversationally, additively, and with the content treated as data. |
| `morning` | `personal:morning` | Render the user's morning brief as a styled HTML artifact, or set it up as a recurring weekday task. Use only when the user explicitly asks to run, see, or set … |
| `nexus` | `personal:nexus` | NEXUS v2.0 — Neural Exchange & Unified Coordination System. Full-scale autonomous AI project manager for Claude Chat and Cowork sessions. Triggers on: start nex… |
| `privacy-legal` | `personal:privacy-legal` | Privacy and legal compliance skill for SaaS and career platforms. Covers GDPR, CCPA/CPRA, PIPEDA, UAE/KSA data protection laws, EU AI Act hiring rules, consent … |
| `skill-creator` | `personal:skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an e… |
| `trading-desk` | `personal:trading-desk` | Expert trading desk, chart analyst and risk officer for Amir's investment-pal / Investment OS — swing trading, short selling, options (single-leg, spreads, cove… |


### `lovable` — 2 skills — v2.0.0

Working with Lovable projects — direct database work through the Lovable MCP server, and the Cloud constraints that make ordinary advice wrong.

| skill | invoked as | description |
|---|---|---|
| `lovable-mcp-setup` | `lovable:lovable-mcp-setup` | Connect Claude Code (or another agent) to the Lovable MCP server so it can work on Lovable projects directly — reading files and diffs, checking analytics, and … |
| `lovabledatabase` | `lovable:lovabledatabase` | Do database work on a Lovable Cloud project through the Lovable MCP server — read-backs, live reads and diagnostics directly via query_database, and every schem… |


### `legal` — 9 skills — v1.3.0

Speed up contract review, NDA triage, and compliance workflows for in-house legal teams. Draft legal briefs, organize precedent research, and manage institutional knowledge.

| skill | invoked as | description |
|---|---|---|
| `brief` | `legal:brief` | Generate contextual briefings for legal work — daily summary, topic research, or incident response. Use when starting your day and need a scan of legal-relevant… |
| `compliance-check` | `legal:compliance-check` | Run a compliance check on a proposed action, product feature, or business initiative, surfacing applicable regulations, required approvals, and risk areas. Use … |
| `legal-response` | `legal:legal-response` | Generate a response to a common legal inquiry using configured templates, with built-in escalation checks for situations that shouldn't use a templated reply. U… |
| `legal-risk-assessment` | `legal:legal-risk-assessment` | Assess and classify legal risks using a severity-by-likelihood framework with escalation criteria. Use when evaluating contract risk, assessing deal exposure, c… |
| `meeting-briefing` | `legal:meeting-briefing` | Prepare structured briefings for meetings with legal relevance and track resulting action items. Use when preparing for contract negotiations, board meetings, c… |
| `review-contract` | `legal:review-contract` | Review a contract against your organization's negotiation playbook — flag deviations, generate redlines, provide business impact analysis. Use when reviewing ve… |
| `signature-request` | `legal:signature-request` | Prepare and route a document for e-signature — run a pre-signature checklist, configure signing order, and send for execution. Use when a contract is finalized … |
| `triage-nda` | `legal:triage-nda` | Rapidly triage an incoming NDA and classify it as GREEN (standard approval), YELLOW (counsel review), or RED (full legal review). Use when a new NDA arrives fro… |
| `vendor-check` | `legal:vendor-check` | Check the status of existing agreements with a vendor across all connected systems — CLM, CRM, email, and document storage — with gap analysis and upcoming dead… |


### `marketing` — 8 skills — v1.2.0

Create content, plan campaigns, and analyze performance across marketing channels. Maintain brand voice consistency, track competitors, and report on what's working.

| skill | invoked as | description |
|---|---|---|
| `brand-review` | `marketing:brand-review` | Review content against your brand voice, style guide, and messaging pillars, flagging deviations by severity with specific before/after fixes. Use when checking… |
| `campaign-plan` | `marketing:campaign-plan` | Generate a full campaign brief with objectives, audience, messaging, channel strategy, content calendar, and success metrics. Use when planning a product launch… |
| `competitive-brief` | `marketing:competitive-brief` | Research competitors and generate a positioning and messaging comparison with content gaps, opportunities, and threats. Use when building sales battlecards, whe… |
| `content-creation` | `marketing:content-creation` | Draft marketing content across channels — blog posts, social media, email newsletters, landing pages, press releases, and case studies. Use when writing any mar… |
| `draft-content` | `marketing:draft-content` | Draft blog posts, social media, email newsletters, landing pages, press releases, and case studies with channel-specific formatting and SEO recommendations. Use… |
| `email-sequence` | `marketing:email-sequence` | Design and draft multi-email sequences with full copy, timing, branching logic, exit conditions, and performance benchmarks. Use when building onboarding, lead … |
| `performance-report` | `marketing:performance-report` | Build a marketing performance report with key metrics, trend analysis, wins and misses, and prioritized optimization recommendations. Use when wrapping a campai… |
| `seo-audit` | `marketing:seo-audit` | Run a comprehensive SEO audit — keyword research, on-page analysis, content gaps, technical checks, and competitor comparison. Use when assessing a site's SEO h… |


### `data` — 10 skills — v1.1.0

Write SQL, explore datasets, and generate insights faster. Build visualizations and dashboards, and turn raw data into clear stories for stakeholders.

| skill | invoked as | description |
|---|---|---|
| `analyze` | `data:analyze` | Answer data questions -- from quick lookups to full analyses. Use when looking up a single metric, investigating what's driving a trend or drop, comparing segme… |
| `build-dashboard` | `data:build-dashboard` | Build an interactive HTML dashboard with charts, filters, and tables. Use when creating an executive overview with KPI cards, turning query results into a share… |
| `create-viz` | `data:create-viz` | Create publication-quality visualizations with Python. Use when turning query results or a DataFrame into a chart, selecting the right chart type for a trend or… |
| `data-context-extractor` | `data:data-context-extractor` | Generate or improve a company-specific data analysis skill by extracting tribal knowledge from analysts.\nBOOTSTRAP MODE - Triggers: \"Create a data context ski… |
| `data-visualization` | `data:data-visualization` | Create effective data visualizations with Python (matplotlib, seaborn, plotly). Use when building charts, choosing the right chart type for a dataset, creating … |
| `explore-data` | `data:explore-data` | Profile and explore a dataset to understand its shape, quality, and patterns. Use when encountering a new table or file, checking null rates and column distribu… |
| `sql-queries` | `data:sql-queries` | Write correct, performant SQL across all major data warehouse dialects (Snowflake, BigQuery, Databricks, PostgreSQL, etc.). Use when writing queries, optimizing… |
| `statistical-analysis` | `data:statistical-analysis` | Apply statistical methods including descriptive stats, trend analysis, outlier detection, and hypothesis testing. Use when analyzing distributions, testing for … |
| `validate-data` | `data:validate-data` | QA an analysis before sharing -- methodology, accuracy, and bias checks. Use when reviewing an analysis before a stakeholder presentation, spot-checking calcula… |
| `write-query` | `data:write-query` | Write optimized SQL for your dialect with best practices. Use when translating a natural-language data need into SQL, building a multi-CTE query with joins and … |


### `customer-support` — 5 skills — v1.3.0

Triage tickets, draft responses, escalate issues, and build your knowledge base. Research customer context and turn resolved issues into self-service content.

| skill | invoked as | description |
|---|---|---|
| `customer-escalation` | `customer-support:customer-escalation` | Package an escalation for engineering, product, or leadership with full context. Use when a bug needs engineering attention beyond normal support, multiple cust… |
| `customer-research` | `customer-support:customer-research` | Multi-source research on a customer question or topic with source attribution. Use when a customer asks something you need to look up, investigating whether a b… |
| `draft-response` | `customer-support:draft-response` | Draft a professional customer-facing response tailored to the situation and relationship. Use when answering a product question, responding to an escalation or … |
| `kb-article` | `customer-support:kb-article` | Draft a knowledge base article from a resolved issue or common question. Use when a ticket resolution is worth documenting for self-service, the same question k… |
| `ticket-triage` | `customer-support:ticket-triage` | Triage and prioritize a support ticket or customer issue. Use when a new ticket comes in and needs categorization, assigning P1-P4 priority, deciding which team… |


### `enterprise-search` — 5 skills — v1.3.0

Search across all of your company's tools in one place. Find anything across email, chat, documents, and wikis without switching between apps.

| skill | invoked as | description |
|---|---|---|
| `digest` | `enterprise-search:digest` | Generate a daily or weekly digest of activity across all connected sources. Use when catching up after time away, starting the day and wanting a summary of ment… |
| `knowledge-synthesis` | `enterprise-search:knowledge-synthesis` | Combines search results from multiple sources into coherent, deduplicated answers with source attribution. Handles confidence scoring based on freshness and aut… |
| `search` | `enterprise-search:search` | Search across all connected sources in one query. Trigger with "find that doc about...", "what did we decide on...", "where was the conversation about...", or w… |
| `search-strategy` | `enterprise-search:search-strategy` | Query decomposition and multi-source search orchestration. Breaks natural language questions into targeted searches per source, translates queries into source-s… |
| `source-management` | `enterprise-search:source-management` | Manages connected MCP sources for enterprise search. Detects available sources, guides users to connect new ones, handles source priority ordering, and manages … |


### `cowork-plugin-management` — 2 skills — v0.2.2

Create, customize, and manage plugins tailored to your organization's tools and workflows. Configure MCP servers, adjust plugin behavior, and adapt templates to match how your team works.

| skill | invoked as | description |
|---|---|---|
| `cowork-plugin-customizer` | `cowork-plugin-management:cowork-plugin-customizer` | Customize a Claude Code plugin for a specific organization's tools and workflows. Use when: customize plugin, set up plugin, configure plugin, tailor plugin, ad… |
| `create-cowork-plugin` | `cowork-plugin-management:create-cowork-plugin` | Guide users through creating a new plugin from scratch in a cowork session. Use when users want to create a plugin, build a plugin, make a new plugin, develop a… |

