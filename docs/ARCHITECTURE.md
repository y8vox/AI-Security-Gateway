# Architecture & Data Flow

## Request lifecycle

1. The client submits a prompt/payload.
2. Flask validates the request body.
3. The rule engine checks known attack signatures.
4. The ML layer vectorizes the input with TF-IDF and predicts malicious probability with Logistic Regression.
5. The risk scorer combines detector evidence into a 0–100 risk score.
6. Policy enforcement blocks requests at risk >= 70 and allows lower-risk requests.
7. Every decision is written to SQLite with request ID, threats, ML probability, risk, and latency.
8. The React dashboard polls the summary and event endpoints for operational visibility.

## Threat classes

- SQL Injection
- Cross-Site Scripting (XSS)
- Directory Traversal
- Command Injection
- Prompt Injection
- Credential Exfiltration
- ML Anomaly

## Design rationale

The hybrid design is deliberate: signature rules are deterministic and explainable, while the ML classifier provides a second signal for patterns not explicitly covered by a rule. The dashboard exposes both the decision and the reason so a demonstration can be audited rather than reduced to a binary result.
