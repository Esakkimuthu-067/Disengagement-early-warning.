"""
Explainability and Human-Centric Interpretation Module.
Generates accessible, transparent natural-language rationale for every prediction
without technical jargon, paired with compassionate mentor action recommendations.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple


def generate_learner_explanation(
    learner_row: Dict[str, Any],
    cohort_medians: Dict[str, float],
    risk_level: str,
    support_probability: float
) -> Dict[str, Any]:
    """
    Translates mathematical model inputs into natural-language reasons:
    - Activity changes and level relative to cohort
    - Assessment trajectory
    - Attendance stability
    - Help-seeking presence / isolation
    - Feedback signal
    
    Generates actionable, non-punitive mentor recommendations.
    """
    reasons = []
    strengths = []
    
    # 1. Activity Signals
    act_min = learner_row.get("active_minutes", 0.0)
    act_change = learner_row.get("activity_change", 0.0)
    med_act = cohort_medians.get("active_minutes", 150.0)
    
    if act_change <= -40.0:
        reasons.append(f"Learning activity decreased by {abs(int(act_change))} minutes compared to previous week")
    elif act_min < 0.5 * med_act:
        reasons.append(f"Weekly study time ({act_min:.0f} mins) is significantly below the course average ({med_act:.0f} mins)")
    elif act_min >= med_act:
        strengths.append(f"Consistent platform engagement ({act_min:.0f} active minutes)")

    # 2. Assessment Trajectory
    score = learner_row.get("average_score", 0.0)
    score_change = learner_row.get("score_change", 0.0)
    score_trend = learner_row.get("score_trend", 0.0)
    
    if score_change <= -12.0 or score_trend <= -12.0:
        delta = abs(int(score_change if score_change != 0 else score_trend))
        reasons.append(f"Assessment performance declined by {delta} points on recent quiz")
    elif score < 50.0:
        reasons.append(f"Quiz scores ({score:.0f}%) indicate concept mastery challenges")
    elif score >= 75.0:
        strengths.append(f"Solid academic performance ({score:.0f}%)")

    # 3. Attendance Stability
    att_rate = learner_row.get("attendance_rate", 1.0)
    att_change = learner_row.get("attendance_change", 0.0)
    if att_change <= -0.25:
        reasons.append(f"Live session attendance dropped by {int(abs(att_change)*100)}% this week")
    elif att_rate < 0.50:
        reasons.append(f"Attendance in live workshops is currently at {int(att_rate*100)}%")
    elif att_rate >= 0.85:
        strengths.append(f"Excellent live session attendance ({int(att_rate*100)}%)")

    # 4. Assignment Submissions
    subs = learner_row.get("assignment_submissions", 1)
    if subs == 0:
        reasons.append("No assignment submissions recorded for the current module")
    elif subs >= 2:
        strengths.append("All assignments submitted on schedule")

    # 5. Help Seeking & Isolation
    help_freq = learner_row.get("help_seeking_frequency", 0)
    if help_freq == 0 and risk_level in ["High Support Need", "Moderate Support Need"]:
        reasons.append("No active help requests or forum participation despite emerging difficulties")
    elif help_freq >= 2:
        strengths.append("Proactive help-seeking (contacted mentor or participated in forum)")

    # 6. Feedback Sentiment
    fb_score = learner_row.get("feedback_score")
    fb_sent = learner_row.get("feedback_sentiment")
    if fb_score is not None and fb_score <= 2.5:
        reasons.append(f"Learner expressed dissatisfaction in recent survey (rating {fb_score:.1f}/5.0)")
    elif fb_sent is not None and fb_sent < -0.3:
        reasons.append("Feedback sentiment suggests frustration with course material")

    # Fallback if no specific red flags triggered
    if not reasons and support_probability >= 0.50:
        reasons.append("Subtle downward trend across multiple simultaneous engagement signals")
    elif not reasons:
        reasons.append("Engagement signals remain stable across all learning dimensions")

    # Non-punitive Recommended Action
    if risk_level == "High Support Need":
        action = "Empathetic 1-on-1 Mentor Outreach: Check in on personal/technical roadblocks and offer flexible catch-up milestone."
        action_tamil = "பரிவுமிக்க வழிகாட்டி தொடர்பு: தொழில்நுட்ப அல்லது தனிப்பட்ட தடைகளை விசாரித்து நெகிழ்வான உதவி வழங்கவும்."
    elif risk_level == "Moderate Support Need":
        action = "Targeted Peer & Study Group Invitation: Suggest relevant tutorial resources and invite to weekly drop-in office hour."
        action_tamil = "படிப்பு குழு அழைப்பு: கூடுதல் பயிற்சி வளங்களை பரிந்துரைத்து கலந்துரையாடலுக்கு அழைக்கவும்."
    elif risk_level == "Insufficient Data":
        action = "Data Verification & Gentle Check-in: Verify if learner is studying offline or experiencing LMS tracking issues."
        action_tamil = "தரவு சரிபார்ப்பு: மாணவர் ஆஃப்லைனில் படிக்கிறாரா அல்லது இணையதள சிக்கல்கள் உள்ளதா என அறியவும்."
    else:
        action = "Standard Encouragement: Acknowledge positive progress and maintain open support channels."
        action_tamil = "வழக்கமான ஊக்கம்: நற்பணியை பாராட்டி ஆதரவு வழிகளை திறந்து வைக்கவும்."

    return {
        "reasons": reasons[:4],  # Top concise bullet points
        "strengths": strengths[:3],
        "recommended_action": action,
        "recommended_action_tamil": action_tamil
    }


def get_feature_importance_summary(rf_model, feature_names: List[str]) -> List[Dict[str, Any]]:
    """
    Extracts sorted global feature importances for transparency display.
    """
    if not hasattr(rf_model, "feature_importances_"):
        return []
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    summary = []
    for idx in indices:
        summary.append({
            "feature": feature_names[idx],
            "importance": round(float(importances[idx]), 4),
            "percentage": round(float(importances[idx] * 100.0), 2)
        })
    return summary
