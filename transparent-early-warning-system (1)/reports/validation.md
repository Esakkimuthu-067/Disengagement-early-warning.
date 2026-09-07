# Stakeholder and Representative User Validation Report

> **Notice**: As specified in Section 25, this study utilizes simulated and role-played representative participants (2 Mentors, 2 Learners, and 1 Course Administrator) to evaluate usability, ethical tone, explainability, and linguistic accessibility.

---

## 1. Study Objectives & Methodology

The validation protocol evaluated five key human-interaction dimensions:
1. **Explainability**: Can mentors easily discern *why* a student received a support alert?
2. **Confidence Comprehension**: Do users understand that confidence reflects evidence quality rather than deterministic certainty?
3. **Non-Punitive Tone**: Do learners perceive the notifications as supportive interventions or punitive judgments?
4. **Bilingual Usability**: Are technical and educational terms clearly and accurately rendered in Tamil and English?
5. **Actionability**: Are suggested mentor interventions realistic and practical within mentor time constraints?

---

## 2. Participant Profiles

- **Mentor 1 (Senior STEM Tutor)**: 6 years online coaching experience; manages 150 learners weekly.
- **Mentor 2 (Junior Teaching Assistant)**: 1 year experience; needs rapid triage of at-risk students.
- **Learner 1 (Part-Time Adult Learner)**: Asynchronous learner with full-time employment; irregular live lecture attendance.
- **Learner 2 (First-Year Student)**: High test scores initially, but struggling with isolation and declining weekly hours.
- **Course Administrator**: Oversees course retention metrics and mentor workload distribution.

---

## 3. Validation Task Matrix

| User Profile | Assigned Evaluation Task | Result | Identified Issue / Feedback | Implemented Improvement |
| :--- | :--- | :--- | :--- | :--- |
| **Mentor 1** | Prioritize 10 high-support learners from the Week 5 active dashboard. | **Success** | Initial column sorting was strictly alphabetical rather than by support probability. | Added single-click sort by Support Probability, Risk Tier, and Missing Data Count. |
| **Mentor 2** | Interpret natural-language rationale for Learner LNR-0042. | **Success** | Requested positive reinforcement bullet points alongside risk factors. | Introduced "Observed Strengths" section (e.g. acknowledging on-time assignment submissions). |
| **Learner 1** | Review support flag explanation as an asynchronous student with low attendance. | **Success** | Feared low live attendance would trigger an automatic failing reprimand. | Verified system categorized student as Low Support Need due to high activity (260m) and 88% marks. |
| **Learner 2** | Check notification wording after sudden decrease in platform logins. | **Success** | Wanted confirmation that mentors would approach with empathy. | Tailored outreach copy to offer flexible 1-on-1 check-ins rather than performance critiques. |
| **Course Admin** | Review language switcher and Tamil translations. | **Success** | Verified Tamil terminology: 'ஆதரவு தேவை' (Support Needed), 'நம்பகத்தன்மை' (Confidence). | Standardized font sizing for Tamil script glyphs to prevent text wrap on mobile screens. |

---

## 4. Key Qualitative Responses to Structured Inquiries

1. **"Can you understand why a learner was flagged?"**
   - *100% affirmative*. The breakdown of activity deltas, score trends, and attendance dips provided concrete behavioral rationale rather than black-box probabilities.
2. **"Is the confidence information understandable?"**
   - *Understood well*. Mentors appreciated that "Insufficient Data" cases prevented them from making erroneous assumptions about offline learners.
3. **"Does the system feel punitive?"**
   - *Strong consensus: No*. Labeling tiers as "Support Need" rather than "Risk of Failure" or "Dropout Risk" transformed mentor outreach into a welcoming, constructive touchpoint.
4. **"Is the bilingual support functional?"**
   - *High praise for Tamil localization*. Essential terms (ஆதரவு நிலை, நம்பகத்தன்மை, வழிகாட்டி பரிந்துரை) accurately preserved educational nuance without robotic translation artifacts.
