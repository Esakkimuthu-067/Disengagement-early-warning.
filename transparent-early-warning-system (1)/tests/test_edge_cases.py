"""
Automated validation of the required Edge/Failure Cases (Section 20).
Ensures the system does not fall prey to single-punitive-indicator biases.
"""

import pytest
import numpy as np
import pandas as pd
from src.data_generator import generate_synthetic_data
from src.preprocessing import LearnerDataPreprocessor
from src.feature_engineering import engineer_features
from src.train_model import prepare_datasets, train_models, CORE_FEATURES
from src.uncertainty import calculate_prediction_uncertainty
from src.baseline import RuleBasedBaseline


@pytest.fixture(scope="module")
def trained_models():
    raw_df = generate_synthetic_data(n_learners=400, n_weeks=4, random_seed=42)
    preprocessor = LearnerDataPreprocessor()
    clean_df = preprocessor.fit_transform(raw_df)
    feat_df = engineer_features(clean_df)
    X_train, X_test, y_train, y_test = prepare_datasets(feat_df, random_seed=42)
    models = train_models(X_train, y_train, random_seed=42)
    return models, preprocessor


def test_edge_case_1_high_marks_low_engagement(trained_models):
    """
    Case 1: Student has high assessment score (90%) but very low activity (25 mins)
    and declining attendance (20%).
    Requirement: System should NOT blindly classify as 'No Support Needed' purely based on high score.
    """
    models, _ = trained_models
    rf = models["random_forest"]
    
    # Construct synthetic learner record
    edge_row = pd.DataFrame([{
        "attendance_rate": 0.20,
        "sessions_attended": 1,
        "attendance_change": -0.50,
        "active_minutes": 25.0,
        "login_count": 2,
        "content_views": 4,
        "assignment_submissions": 0,
        "activity_change": -120.0,
        "submission_rate": 0.0,
        "average_score": 90.0,
        "assessment_attempts": 1,
        "score_trend": 0.0,
        "score_change": 0.0,
        "help_requests": 0,
        "forum_questions": 0,
        "mentor_contacts": 0,
        "help_seeking_frequency": 0,
        "feedback_score": 3.0,
        "feedback_sentiment": -0.2,
        "feedback_signal": 0.54,
        "overall_engagement_score": 38.0,
        "engagement_trend": -45.0,
        "missing_feature_count": 0
    }])
    
    prob = float(rf.predict_proba(edge_row[CORE_FEATURES])[:, 1][0])
    uncertainty = calculate_prediction_uncertainty(prob, missing_count=0)
    
    # Even with high marks (90%), the severe drops in activity, attendance, and submissions
    # must elevate probability above trivial low-risk (<0.20)
    assert prob >= 0.35, f"High score blinded model to disengagement! Probability: {prob}"
    assert uncertainty["risk_level"] in ["Moderate Support Need", "High Support Need"]


def test_edge_case_2_low_attendance_high_engagement(trained_models):
    """
    Case 2: Self-directed asynchronous learner.
    Low live session attendance (25%), but high active minutes (260m), 2 submissions, score 88%.
    Requirement: System must NOT unfairly penalize or flag student as High Support Need solely for attendance.
    """
    models, _ = trained_models
    rf = models["random_forest"]
    baseline = RuleBasedBaseline()
    
    edge_row = pd.DataFrame([{
        "attendance_rate": 0.25,
        "sessions_attended": 1,
        "attendance_change": 0.0,
        "active_minutes": 260.0,
        "login_count": 9,
        "content_views": 35,
        "assignment_submissions": 2,
        "activity_change": 10.0,
        "submission_rate": 1.2,
        "average_score": 88.0,
        "assessment_attempts": 1,
        "score_trend": 2.0,
        "score_change": 2.0,
        "help_requests": 1,
        "forum_questions": 2,
        "mentor_contacts": 0,
        "help_seeking_frequency": 3,
        "feedback_score": 4.5,
        "feedback_sentiment": 0.6,
        "feedback_signal": 1.17,
        "overall_engagement_score": 78.5,
        "engagement_trend": 5.0,
        "missing_feature_count": 0
    }])
    
    # Check baseline vs ML model
    # Heuristic baseline might flag if attendance rule is crude, but ML should recognize high engagement
    prob = float(rf.predict_proba(edge_row[CORE_FEATURES])[:, 1][0])
    uncertainty = calculate_prediction_uncertainty(prob, missing_count=0)
    
    assert prob < 0.50, f"Learner unfairly flagged despite high active minutes & scores! Prob: {prob}"
    assert uncertainty["risk_level"] in ["Low Support Need", "Moderate Support Need"]


def test_edge_case_3_missing_data_insufficient_evidence():
    """
    Case 3: Student has missing telemetry (missing activity, feedback, help-seeking).
    Requirement: System must assign 'Insufficient Data' and downgrade confidence.
    """
    # 4 critical fields missing
    uncertainty = calculate_prediction_uncertainty(probability=0.82, missing_count=4)
    
    assert uncertainty["risk_level"] == "Insufficient Data"
    assert uncertainty["uncertainty_category"] == "Insufficient evidence"
    assert "deferred" in uncertainty["uncertainty_warning"].lower()


def test_edge_case_4_sudden_behaviour_change(trained_models):
    """
    Case 4: Previously active student displays sharp collapse in engagement trend.
    Requirement: engagement_trend feature reflects sharp negative slope.
    """
    models, _ = trained_models
    rf = models["random_forest"]
    
    collapsed_row = pd.DataFrame([{
        "attendance_rate": 0.33,
        "sessions_attended": 1,
        "attendance_change": -0.67,
        "active_minutes": 40.0,
        "login_count": 1,
        "content_views": 3,
        "assignment_submissions": 0,
        "activity_change": -180.0,
        "submission_rate": 0.0,
        "average_score": 62.0,
        "assessment_attempts": 1,
        "score_trend": -22.0,
        "score_change": -22.0,
        "help_requests": 0,
        "forum_questions": 0,
        "mentor_contacts": 0,
        "help_seeking_frequency": 0,
        "feedback_score": 2.0,
        "feedback_sentiment": -0.5,
        "feedback_signal": 0.30,
        "overall_engagement_score": 32.0,
        "engagement_trend": -70.0,
        "missing_feature_count": 0
    }])
    
    prob = float(rf.predict_proba(collapsed_row[CORE_FEATURES])[:, 1][0])
    assert prob > 0.60, f"Sudden drop was not captured! Probability: {prob}"
