# User & Practitioner Guide

Welcome to the **Transparent Disengagement Early-Warning Tool** user guide. This manual provides step-by-step instructions for educators, mentors, course administrators, and developers to install, execute, and interpret the early-warning system.

---

## 1. Installation

Clone or extract the repository and install dependencies in your Python environment:

```bash
# Optional: Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

---

## 2. Dataset Generation

The system includes a reproducible synthetic data generator simulating longitudinal learning telemetry:

```bash
# Generates 6,000 multi-signal records (1,200 learners × 5 weeks)
python3 -c "from src.data_generator import generate_synthetic_data; df = generate_synthetic_data(); df.to_csv('data/raw/synthetic_learners.csv', index=False); print('Dataset generated!')"
```

The output file will be saved to `data/raw/synthetic_learners.csv`.

---

## 3. Model Training & Pipeline Execution

Execute the full end-to-end training, validation, back-testing, and uncertainty calibration pipeline:

```bash
python3 run_pipeline.py
```

This single command:
1. Validates and preprocesses raw telemetry.
2. Performs non-leaking feature engineering and composite engagement scoring.
3. Evaluates the baseline rule-based heuristic.
4. Trains Logistic Regression, Random Forest, and Gradient Boosting models.
5. Runs stratified 5-fold cross-validation.
6. Conducts multi-signal ablation experiments.
7. Executes longitudinal back-testing across Weeks 1 to 5.
8. Produces explainability rationales and serializes results to `data/processed/pipeline_results.json`.

---

## 4. Running the Dashboard

Launch the interactive Streamlit interface:

```bash
streamlit run app.py
```

The dashboard will open automatically in your default browser at `http://localhost:8501`.

---

## 5. Understanding Risk Levels

The tool strictly classifies learners into **Support Prioritisation Tiers** rather than assigning punitive scores:

* 🟢 **Low Support Need**: The learner exhibits stable or improving engagement across attendance, platform study hours, assignment submissions, and assessment scores.
* 🟡 **Moderate Support Need**: Early subtle declines detected across two or more dimensions (e.g. slight dip in study minutes combined with negative feedback or missed forum activity). Mentor check-in advised during weekly drop-in hours.
* 🔴 **High Support Need**: Pronounced compound disengagement across multiple learning channels. Recommended for prioritized 1-on-1 empathetic outreach.
* ⚪ **Insufficient Data**: Three or more critical signals are absent. Automated classification is deferred to prevent erroneous assumptions.

---

## 6. Understanding Prediction Confidence

Prediction confidence communicates the **reliability of the model's evidence**:
* **High Confidence (≥ 75%)**: Telemetry is complete, and the student's behavioral signals are mutually consistent.
* **Medium Confidence (55%–74%)**: Moderate evidence; signals may be near decision margins or show minor inconsistencies.
* **Low Confidence (< 55%)**: Borderline case requiring mentor qualitative discretion.
* **Insufficient Evidence**: Signal sparsity exceeds safety thresholds.

*Note: Confidence measures evidence clarity, not deterministic certainty of student outcome.*

---

## 7. Understanding Missing-Data Warnings

Whenever data fields are missing (e.g., student did not fill out optional survey, or studied offline), the system displays explicit alerts:
> *"Confidence reduced because feedback and activity data are unavailable."*

Mentors are encouraged to verify offline study habits before assuming disengagement.

---

## 8. Understanding Explanations

Each flagged learner card presents natural-language bullet points highlighting positive strengths and areas of concern:
* `✓ Learning activity decreased by 45 minutes compared to previous week`
* `✓ Live session attendance dropped by 50% this week`
* `★ Solid academic performance (82% quiz score)`

---

## 9. Using Mentor Recommendations

Recommendations are formulated with a trauma-informed, student-first ethos:
* **High Support**: *"Empathetic 1-on-1 Mentor Outreach: Check in on personal/technical roadblocks and offer flexible catch-up milestones."*
* **Moderate Support**: *"Study Group Invitation: Suggest relevant tutorials and invite to weekly drop-in office hours."*
* **Insufficient Data**: *"Data Verification Check: Inquire whether learner is studying offline or experiencing LMS sync issues."*

---

## 10. Limitations

1. **Synthetic Telemetry**: The current prototype is trained on simulated data and must be re-calibrated on real institutional LMS logs before deployment.
2. **Context Blindness**: The system cannot detect external personal emergencies (illness, bereavement, job shifts) unless reported directly by the learner.
3. **Mentor Capacity**: The tool prioritizes outreach based on need but cannot substitute for sufficient mentor staffing.
