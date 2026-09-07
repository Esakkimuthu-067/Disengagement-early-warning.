# Transparent Disengagement Early-Warning Tool: System Architecture

## 1. Executive Summary

The **Transparent Disengagement Early-Warning Tool** is an ethical, multi-signal artificial intelligence framework designed to identify online course learners who may benefit from proactive mentor outreach. Rejecting punitive scoring, surveillance heuristics, or single-metric penalties (such as flagging students solely based on attendance or exam marks), the system synthesizes five holistic behavioral streams:

1. **Attendance** (Live lecture attendance, consistency, session rates)
2. **Learning Activity** (Active minutes, platform login frequency, content views, assignment submissions)
3. **Assessment Performance** (Quiz attempts, average scores, grade trajectory, score deltas)
4. **Help-Seeking Behaviour** (Mentor inquiries, forum participation, question volume)
5. **Learner Feedback** (Surveys, course sentiment ratings, subjective feedback scores)

---

## 2. End-to-End Pipeline Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                            1. SYNTHETIC DATA ENGINE                               |
|   1,200 Learners × 5 Longitudinal Weeks (6,000 Records)                           |
|   Controlled Latent Profiles • Multi-Signal Interdependence • Realistic Noise     |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                         2. DATA AUDIT & PREPROCESSING                             |
|   Domain Boundary Validation • Missingness Indicator Masking                      |
|   Median Imputation (Strictly Non-Leaking Fold Basis)                             |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        3. MULTI-SIGNAL FEATURE ENGINEERING                        |
|   Longitudinal Trends (Δ Activity, Δ Scores, Δ Attendance)                        |
|   Composite Engagement Score (0-100) • Help-Seeking Frequency • Feedback Signal   |
+-----------------------------------------+-----------------------------------------+
                                          |
                     +--------------------+--------------------+
                     |                                         |
                     v                                         v
+------------------------------------------+ +--------------------------------------+
|        4A. BASELINE HEURISTIC MODEL      | |     4B. IMPROVED MACHINE LEARNING    |
|   Static Cutoffs:                        | |   Logistic Regression (Transparent)  |
|   (Attendance < 60% & Activity < 90m)    | |   Random Forest (Non-Linear Ensemble)|
|   OR (Average Score < 55%)               | |   Gradient Boosting Benchmark        |
+--------------------+---------------------+ +------------------+------------------+
                     |                                         |
                     +--------------------+--------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                     5. UNCERTAINTY & CONFIDENCE CALIBRATION                       |
|   Probability Margin to Boundary • Ensemble Tree Variance                         |
|   Missingness Penalty Function • Calibration Tiers (High, Med, Low, Deferred)     |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                      6. MISSING DATA & RELIABILITY SHIELD                         |
|   Missingness Profiling • Critical Threshold Defenses (≥3 Missing Signals)        |
|   Automatic Routing to "Insufficient Data" Category (Defers Overconfident Guesses)|
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                     7. HUMAN-CENTRIC EXPLAINABILITY ENGINE                        |
|   Plain-Language Drivers (e.g. "Activity dropped by 42m")                         |
|   Identification of Strengths • Empathetic Mentor Action Recommendation           |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                  8. INTERACTIVE DASHBOARD (STREAMLIT & WEB UI)                    |
|   Bilingual Accessibility (English & Tamil) • High-Contrast WCAG Compliant        |
|   Interactive Filter Panels • Detailed Learner Deep Dives • Backtest Visualizer   |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                    9. NON-PUNITIVE MENTOR ACTION & SUPPORT                        |
|   1-on-1 Check-ins • Flexible Catch-Up Milestones • Technical Barrier Resolution  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Detailed Component Specifications

### 3.1 Data Generator (`src/data_generator.py`)
- Generates 6,000 longitudinal records (1,200 unique learners tracked across 5 course weeks).
- Assigns learners to distinct realistic behavioral profiles:
  - Consistently high engagement (50%)
  - Moderate steady engagement (25%)
  - Gradual disengagement (18%)
  - Sudden disengagement (7%)
- Simulates realistic missingness across optional feedback (22%), help-seeking (12%), assessments (7%), activity (6%), and attendance (4%).

### 3.2 Preprocessing (`src/preprocessing.py`)
- Clips physical impossibility bounds (attendance between 0.0 and 1.0; scores between 0.0 and 100.0).
- Explicitly encodes `_missing` indicator flags.
- Aggregates `missing_feature_count`.
- Fits median imputation values strictly on the training partition.

### 3.3 Feature Engineering (`src/feature_engineering.py`)
- Computes trajectory deltas (`activity_change`, `score_change`, `attendance_change`).
- Constructs balanced `overall_engagement_score` (0 to 100):
  - Attendance: 25%
  - Activity: 25%
  - Assessment: 25%
  - Help-seeking: 15%
  - Feedback: 10%

### 3.4 Baseline vs. Improved ML (`src/baseline.py`, `src/train_model.py`)
- **Baseline**: Emulates traditional institutional alerts using simplistic thresholds.
- **Improved**: Evaluates Logistic Regression, Random Forest, and Gradient Boosting with stratified train/test splits and 5-fold cross-validation.

### 3.5 Uncertainty & Confidence (`src/uncertainty.py`)
- Uses distance from the classification decision boundary combined with missingness counts and ensemble standard deviations to produce a calibrated confidence score.
- Categorizes predictions into:
  - *High confidence* (≥ 75%)
  - *Medium confidence* (55%–74%)
  - *Low confidence* (< 55%)
  - *Insufficient evidence* (when ≥ 3 critical signals are missing)

### 3.6 Explainability (`src/explainability.py`)
- Translates model weights and deviations into concise, supportive bullet points.
- Pairs each alert with an empathetic mentor outreach suggestion (both in English and Tamil).
