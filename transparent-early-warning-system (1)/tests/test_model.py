"""
Unit tests for model training, feature engineering, and baseline evaluation.
"""

import pytest
import numpy as np
import pandas as pd
from src.data_generator import generate_synthetic_data
from src.preprocessing import LearnerDataPreprocessor
from src.feature_engineering import engineer_features
from src.baseline import RuleBasedBaseline, evaluate_model
from src.train_model import prepare_datasets, train_models, CORE_FEATURES
from src.uncertainty import calculate_prediction_uncertainty


@pytest.fixture
def sample_pipeline_data():
    raw_df = generate_synthetic_data(n_learners=200, n_weeks=3, random_seed=42)
    preprocessor = LearnerDataPreprocessor()
    clean_df = preprocessor.fit_transform(raw_df)
    feat_df = engineer_features(clean_df)
    return feat_df


def test_feature_engineering_outputs(sample_pipeline_data):
    df = sample_pipeline_data
    assert "activity_change" in df.columns
    assert "score_change" in df.columns
    assert "attendance_change" in df.columns
    assert "submission_rate" in df.columns
    assert "engagement_trend" in df.columns
    assert "help_seeking_frequency" in df.columns
    assert "feedback_signal" in df.columns
    assert "overall_engagement_score" in df.columns
    
    # Range check overall engagement score
    assert df["overall_engagement_score"].min() >= 0.0
    assert df["overall_engagement_score"].max() <= 100.0


def test_baseline_and_improved_training(sample_pipeline_data):
    df = sample_pipeline_data
    X_train, X_test, y_train, y_test = prepare_datasets(df, test_size=0.3, random_seed=42)
    
    # Baseline
    baseline = RuleBasedBaseline()
    base_preds = baseline.predict(X_test)
    base_metrics = evaluate_model(y_test, base_preds)
    assert "f1" in base_metrics
    assert "recall" in base_metrics
    
    # Train ML models
    models = train_models(X_train, y_train, random_seed=42)
    assert "logistic_regression" in models
    assert "random_forest" in models
    
    rf = models["random_forest"]
    rf_preds = rf.predict(X_test)
    rf_probs = rf.predict_proba(X_test)[:, 1]
    rf_metrics = evaluate_model(y_test, rf_preds, rf_probs)
    
    # ML model should have solid discriminatory capability
    assert rf_metrics["roc_auc"] > 0.70


def test_uncertainty_bounds():
    # Boundary case near 0.50 should have lower confidence
    res_border = calculate_prediction_uncertainty(0.51, missing_count=0)
    assert res_border["confidence_percentage"] < 65.0
    assert res_border["uncertainty_category"] in ["Low confidence", "Medium confidence"]
    
    # Clear high-confidence case
    res_clear = calculate_prediction_uncertainty(0.95, missing_count=0)
    assert res_clear["confidence_percentage"] >= 75.0
    assert res_clear["uncertainty_category"] == "High confidence"
    
    # Severe missingness forces Insufficient Data
    res_missing = calculate_prediction_uncertainty(0.90, missing_count=4)
    assert res_missing["risk_level"] == "Insufficient Data"
    assert res_missing["uncertainty_category"] == "Insufficient evidence"
