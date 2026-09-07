"""
Missing Data Impact and Reliability Analysis Module.
Quantifies missing data patterns across learning signals, measures performance degradation,
and issues structured warnings when telemetry is incomplete.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from src.baseline import evaluate_model


def analyze_missingness(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes summary missingness metrics across features and learners.
    """
    total_records = len(df)
    missing_by_feature = df.isnull().mean() * 100.0
    
    # Missing counts per learner
    # Count missing values across primary observational fields
    primary_cols = [
        "attendance_rate", "active_minutes", "content_views",
        "average_score", "score_trend", "help_requests",
        "feedback_score", "feedback_sentiment"
    ]
    present_cols = [c for c in primary_cols if c in df.columns]
    learner_missing_counts = df[present_cols].isnull().sum(axis=1)
    
    distribution = learner_missing_counts.value_counts().sort_index().to_dict()
    insufficient_data_count = int((learner_missing_counts >= 3).sum())
    
    return {
        "total_records": total_records,
        "feature_missing_percentages": {k: round(float(v), 2) for k, v in missing_by_feature.items() if v > 0},
        "learner_missing_distribution": {int(k): int(v) for k, v in distribution.items()},
        "records_with_any_missing": int((learner_missing_counts > 0).sum()),
        "insufficient_data_count": insufficient_data_count,
        "insufficient_data_rate": round(float(insufficient_data_count / total_records), 4)
    }


def compare_complete_vs_missing_performance(
    model,
    X_test: pd.DataFrame,
    y_test: np.ndarray,
    df_test_raw: pd.DataFrame
) -> Dict[str, Any]:
    """
    Evaluates model performance on:
    1. Complete records subset (zero missing raw values)
    2. Records with missing data
    """
    primary_cols = [
        "attendance_rate", "active_minutes", "content_views",
        "average_score", "score_trend", "help_requests",
        "feedback_score", "feedback_sentiment"
    ]
    present_cols = [c for c in primary_cols if c in df_test_raw.columns]
    has_missing = df_test_raw[present_cols].isnull().any(axis=1).values
    
    complete_idx = np.where(~has_missing)[0]
    missing_idx = np.where(has_missing)[0]
    
    # Predict
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
    
    overall_metrics = evaluate_model(y_test, preds, probs)
    
    complete_metrics = (
        evaluate_model(y_test[complete_idx], preds[complete_idx], probs[complete_idx] if probs is not None else None)
        if len(complete_idx) > 0 else {}
    )
    
    missing_metrics = (
        evaluate_model(y_test[missing_idx], preds[missing_idx], probs[missing_idx] if probs is not None else None)
        if len(missing_idx) > 0 else {}
    )
    
    return {
        "overall": overall_metrics,
        "complete_cohort": {
            "sample_size": len(complete_idx),
            "metrics": complete_metrics
        },
        "missing_cohort": {
            "sample_size": len(missing_idx),
            "metrics": missing_metrics
        },
        "reliability_chain": {
            "low_missingness": "Reliability: High (90-95%)",
            "moderate_missingness": "Reliability: Moderate (70-85%) - Mentor Check Advised",
            "severe_missingness": "Reliability: Insufficient - Do Not Make Automated Judgment"
        }
    }


def get_missing_data_warning(row_dict: Dict[str, Any]) -> str:
    """
    Produces human-readable missing data warning for a learner record.
    """
    missing_signals = []
    if pd.isna(row_dict.get("feedback_score")) or pd.isna(row_dict.get("feedback_sentiment")):
        missing_signals.append("feedback")
    if pd.isna(row_dict.get("active_minutes")) or pd.isna(row_dict.get("content_views")):
        missing_signals.append("activity telemetry")
    if pd.isna(row_dict.get("help_requests")) or pd.isna(row_dict.get("forum_questions")):
        missing_signals.append("help-seeking history")
    if pd.isna(row_dict.get("average_score")):
        missing_signals.append("assessment scores")
    if pd.isna(row_dict.get("attendance_rate")):
        missing_signals.append("attendance records")
        
    if not missing_signals:
        return "Complete data profile available."
    elif len(missing_signals) >= 3:
        return f"CRITICAL: Insufficient data. Missing {', '.join(missing_signals)}. Automated prediction deferred."
    else:
        return f"Confidence reduced because {', '.join(missing_signals)} are unavailable."
