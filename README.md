# N-CALAS
## Nigerian Critical AI Literacy Assessment System

N-CALAS is a proposed, institution-configurable assessment prototype that operationalises the **Verify–Localize–Defend (VLD)** framework for assessing students' critical engagement with AI-supported academic and technical work.

> **Research and safety status:** This repository contains an early software demonstrator, not a validated assessment instrument. It does not establish factual truth, determine whether text was written by AI, or produce defensible student grades. Outputs are review cues for a qualified human examiner. Do not use it for high-stakes decisions or upload identifiable student work.

## VLD workflow

- **Verify:** surface claims, numeric expressions, citations and other items that may need evidence-based checking. The current prototype only identifies review cues; it does not fact-check claims.
- **Localize:** compare submitted text with institution-configured terminology and requirements. The current prototype performs literal term matching only; it does not interpret regulations or technical standards.
- **Defend:** draft questions grounded in the submitted report and collect responses. The current prototype provides prompts and descriptive text-overlap signals only; it does not determine whether a student understands or authored the work.

The three pillars are kept separate. A difference from a local convention is not automatically a factual error.

## Institution configuration

Copy `config/institution.example.json` to `config/institution.json` and edit it for the institution, programme and assessment. The local file is git-ignored to avoid accidentally publishing institutional settings. Configure only requirements that the institution is authorised to use. Record source, version, effective date and scope for each formal standard before building standards-based checks.

## Run locally

Python 3.11 or newer is recommended.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local Streamlit address shown in the terminal (normally http://localhost:8501).

## Run with Docker

```bash
docker compose up --build
```

Then open http://localhost:8501.

## Temporary remote demonstration

For a controlled demonstration only, you may expose the local app using a temporary HTTPS tunnel, for example Cloudflare Tunnel:

```bash
cloudflared tunnel --url http://localhost:8501
```

Treat the resulting URL as public. Use synthetic documents only, do not expose databases or administrative services, and stop the tunnel when finished. Add authentication and institutional approval before any real deployment.

## Current prototype limitations

- No LLM or retrieval-augmented generation (RAG) integration.
- No authoritative standards corpus or automated standards interpretation.
- No validated scoring model, AI-authorship detector or empirical performance claims.
- No production authentication, role-based access control, encryption-at-rest design, backup policy or security audit.
- Text-matching signals can miss context and produce false positives/negatives.
- SQLite stores basic local activity metadata; avoid entering personal data.

## Research and validation direction

Before any pilot use, define transparent pillar-specific rubrics and evidence requirements; build versioned, traceable institutional knowledge sources; involve subject experts; and retain examiner review. Validation should compare system outputs with independent expert annotations and independently rated student defenses. Suitable analyses may include precision/recall/F1 for classification tasks, weighted kappa for ordinal agreement, ICC for continuous ratings, question relevance ratings, reliability, usability and utility. Do not validate the system against its own outputs.

## Suggested next development stages

1. Requirements specification and institution configuration schema.
2. Secure document ingestion and provenance-preserving evidence extraction.
3. Versioned institutional standards / policy retrieval with citations.
4. Transparent Verify and Localize review workflows.
5. Report-grounded Defense question generation and examiner rubric.
6. Authentication, privacy controls, auditability and deployment hardening.
7. Expert evaluation and a small, ethically approved pilot.

## License

No open-source license has been selected. Until a license is added, standard copyright applies.
