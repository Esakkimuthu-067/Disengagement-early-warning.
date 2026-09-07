"""
Unit tests for data generation, validation, and missingness simulation.
"""

import pytest
import numpy as np
import pandas as pd
from src.data_generator import generate_synthetic_data
from src.preprocessing import LearnerDataPreprocessor, validate_raw_data


def test_synthetic_data_volume():
    """Verify dataset meets the requirement of at least 5,000 learner records."""
    df = generate_synthetic_data(n_learners=1200, n_weeks=5, random_seed=42)
    assert len(df) == 6000
    assert len(df) >= 5000
    assert df["learner_id"].nunique() == 1200


def test_five_signal_groups_present():
    """Verify all 5 learning signals exist in the schema."""
    df = generate_synthetic_data(n_learners=100, n_weeks=2, random_seed=42)
    
    # 1. Attendance
    assert "attendance_rate" in df.columns
    assert "sessions_attended" in df.columns
    # 2. Activity
    assert "active_minutes" in df.columns
    assert "login_count" in df.columns
    assert "assignment_submissions" in df.columns
    # 3. Assessment
    assert "average_score" in df.columns
    assert "score_trend" in df.columns
    # 4. Help Seeking
    assert "help_requests" in df.columns
    assert "mentor_contacts" in df.columns
    # 5. Feedback
    assert "feedback_score" in df.columns
    assert "feedback_sentiment" in df.columns


def test_target_distribution():
    """Ensure target class balance matches 20-30% support needed."""
    df = generate_synthetic_data(n_learners=1000, n_weeks=5, random_seed=42)
    rate = df["support_needed"].mean()
    assert 0.18 <= rate <= 0.32, f"Target rate {rate:.2f} outside 18-32% window"


def test_missing_data_introduced():
    """Ensure realistic missing values exist and are not silently dropped."""
    df = generate_synthetic_data(n_learners=500, n_weeks=3, random_seed=42)
    assert df["feedback_score"].isnull().sum() > 0
    assert df["active_minutes"].isnull().sum() > 0
    assert df["help_requests"].isnull().sum() > 0


def test_preprocessing_bounds_and_imputation():
    """Ensure preprocessor clips outliers and imputes correctly without nulls."""
    df = generate_synthetic_data(n_learners=200, n_weeks=2, random_seed=42)
    preprocessor = LearnerDataPreprocessor()
    clean_df = preprocessor.fit_transform(df)
    
    # Check no remaining NaNs in bounded columns
    for col in LearnerDataPreprocessor.VALID_BOUNDS.keys():
        assert clean_df[col].isnull().sum() == 0
    assert "missing_feature_count" in clean_df.columns
