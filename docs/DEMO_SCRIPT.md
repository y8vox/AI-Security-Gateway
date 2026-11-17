# 5-Minute Final Demo

**Opening — 30 sec**

“AI applications introduce a new attack surface. Our AI Security Gateway places a security enforcement layer between the client and the model. Every request is inspected, scored, and either allowed or blocked.”

**Live scanner — 2 min**

- Benign prompt → ALLOW.
- SQL injection → BLOCK.
- XSS → BLOCK.
- Prompt injection → BLOCK.

**Architecture — 90 sec**

Explain: request → Flask API → rule detector → TF-IDF → Logistic Regression → risk score → policy → audit log.

**Evidence — 60 sec**

Show the event stream and test results. Point out request ID, threat category, risk score and latency.

**Close — 30 sec**

“The prototype demonstrates a hybrid security control: deterministic detection for known patterns, ML classification for an additional signal, explicit policy enforcement, and an auditable evidence trail.”
