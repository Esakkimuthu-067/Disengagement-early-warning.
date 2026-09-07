"""
Feature Engineering Module for Disengagement Early-Warning System.
Creates interpretable, non-punitive multi-signal features across 5 core learning dimensions.
"""

import numpy as np
import pandas as pd
from typing import List, Tuple


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes domain-grounded longitudinal and composite engagement features:
    
    1. Longitudinal Changes (by learner_id ordered by week):
       - activity_change = active_minutes_t - active_minutes_(t-1)
       - score_change = average_score_t - average_score_(t-1)
       - attendance_change = attendance_rate_t - attendance_rate_(t-1)
       
    2. Behavioral Frequency:
       - submission_rate = assignment_submissions / max(1, sessions_available / 2)
       - help_seeking_frequency = help_requests + forum_questions + mentor_contacts
       
    3. Sentiment / Feedback:
       - feedback_signal = (feedback_score / 5.0) * (1.0 + 0.5 * feedback_sentiment)
       
    4. Multi-Signal Overall Engagement Score (0 to 100):
       Balanced composite index:
         - Attendance contribution: 25% (attendance_rate * 100)
         - Activity contribution: 25% (min(active_minutes / 240.0, 1.0) * 100)
         - Assessment contribution: 25% (average_score)
         - Help-seeking & interaction: 15% (min(help_seeking_frequency / 4.0, 1.0) * 100)
         - Feedback contribution: 10% (min(feedback_signal, 1.0) * 100)
       
       Total: exactly 100 points maximum.
       
    5. engagement_trend:
       Weighted combination of delta slopes:
       0.4 * normalized_activity_change + 0.3 * normalized_score_change + 0.3 * attendance_change
    """
    data = df.sort_values(by=["learner_id", "week"]).copy()
    
    # Longitudinal changes grouped by learner
    data["prev_active_minutes"] = data.groupby("learner_id")["active_minutes"].shift(1)
    data["prev_average_score"] = data.groupby("learner_id")["average_score"].shift(1)
    data["prev_attendance_rate"] = data.groupby("learner_id")["attendance_rate"].shift(1)
    
    data["activity_change"] = data["active_minutes"] - data["prev_active_minutes"]
    data["activity_change"] = data["activity_change"].fillna(0.0)
    
    data["score_change"] = data["average_score"] - data["prev_average_score"]
    data["score_change"] = data["score_change"].fillna(0.0)
    
    data["attendance_change"] = data["attendance_rate"] - data["prev_attendance_rate"]
    data["attendance_change"] = data["attendance_change"].fillna(0.0)
    
    # Behavioral ratios
    expected_subs = np.maximum(1.0, data["sessions_available"] / 2.0)
    data["submission_rate"] = np.clip(data["assignment_submissions"] / expected_subs, 0.0, 1.5)
    
    # Help seeking
    data["help_seeking_frequency"] = (
        data["help_requests"] + data["forum_questions"] + data["mentor_contacts"]
    )
    
    # Feedback signal
    norm_fb = np.clip(data["feedback_score"] / 5.0, 0.2, 1.0)
    sent_factor = 1.0 + (0.5 * data["feedback_sentiment"])
    data["feedback_signal"] = np.clip(norm_fb * sent_factor, 0.0, 1.5)
    
    # Overall Engagement Score (0 to 100)
    att_comp = np.clip(data["attendance_rate"], 0.0, 1.0) * 25.0
    act_comp = np.clip(data["active_minutes"] / 240.0, 0.0, 1.0) * 25.0
    scr_comp = np.clip(data["average_score"] / 100.0, 0.0, 1.0) * 25.0
    hlp_comp = np.clip(data["help_seeking_frequency"] / 3.0, 0.0, 1.0) * 15.0
    fdb_comp = np.clip(data["feedback_signal"] / 1.0, 0.0, 1.0) * 10.0
    
    data["overall_engagement_score"] = np.round(
        att_comp + act_comp + scr_comp + hlp_comp + fdb_comp, 1
    )
    
    # Engagement Trend: composite direction (-100 to +100 normalized range)
    norm_act_delta = np.clip(data["activity_change"] / 120.0, -1.0, 1.0)
    norm_scr_delta = np.clip(data["score_change"] / 30.0, -1.0, 1.0)
    norm_att_delta = np.clip(data["attendance_change"] / 0.5, -1.0, 1.0)
    
    data["engagement_trend"] = np.round(
        (0.4 * norm_act_delta + 0.3 * norm_scr_delta + 0.3 * norm_att_delta) * 50.0, 1
    )
    
    # Drop temporary lagged columns
    data = data.drop(columns=["prev_active_minutes", "prev_average_score", "prev_attendance_rate"])
    
    return data


def get_feature_groups() -> dict:
    """Returns mapping of feature names to semantic signal group for ablation experiments."""
    return {
        "attendance": ["attendance_rate", "sessions_attended", "attendance_change"],
        "activity": ["active_minutes", "login_count", "content_views", "assignment_submissions", "activity_change", "submission_rate"],
        "assessment": ["average_score", "assessment_attempts", "score_trend", "score_change"],
        "help_seeking": ["help_requests", "forum_questions", "mentor_contacts", "help_seeking_frequency"],
        "feedback": ["feedback_score", "feedback_sentiment", "feedback_signal"],
        "meta": ["overall_engagement_score", "engagement_trend", "missing_feature_count"]
    }
