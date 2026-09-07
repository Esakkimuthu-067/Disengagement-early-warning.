# Ethical and Technical Risk Register

This risk register outlines potential systemic, ethical, and algorithmic failure modes of the **Transparent Disengagement Early-Warning Tool**, detailing concrete mitigation strategies implemented in the system architecture.

| Risk | Impact | Likelihood | Systemic & Operational Mitigation |
| :--- | :--- | :--- | :--- |
| **False Positives (Over-Alerting)** | Medium | Medium | Human-in-the-loop triage; all alerts are framed as voluntary offers of support rather than deficits or reprimands; mentor confirms before taking action. |
| **False Negatives (Missed Disengagement)** | High | Medium | Multi-signal holistic monitoring (incorporating help-seeking dips, feedback sentiment, and activity rate drops rather than test marks alone); longitudinal trend tracking across weeks. |
| **Missing Data Distortions** | High | High | Explicit missingness indicator tracking; automatic downgrade of confidence; assignment to "Insufficient Data" status when ≥ 3 critical signals are missing. |
| **Algorithmic & Demographic Bias** | High | Medium | Fairness audits across course cohorts and user subgroups; explicit removal of demographic features as direct model inputs. |
| **Punitive / Surveillance Use by Institutions** | High | Medium | Strict policy constraint; prohibition of punitive labels (no "dropout", "lazy", "failing"); replacing numerical scores with supportive tiers ("Low Support Need", "Moderate Support Need", "High Support Need"). |
| **Poor Model Explainability** | Medium | Medium | Natural-language rationale generation; plain-English bullet points explaining the driving signals; positive reinforcement acknowledging learner strengths. |
| **Language & Accessibility Barriers** | Medium | Medium | Complete bilingual English and Tamil localization; screen-reader friendly descriptive text labels; non-color-exclusive status indicators (emojis/text badges paired with color). |
| **Telemetry Sync Latency** | Low | Medium | Asynchronous queueing of LMS telemetry; time-stamped weekly aggregation windows; mentor notifications clearly marked with data capture timestamp. |
| **Over-Reliance by Mentors (Automation Bias)** | Medium | Medium | Confidence calibration display reminding mentors that model output is a prioritization suggestion, not a definitive psychological diagnostic. |
