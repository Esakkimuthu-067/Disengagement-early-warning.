"""
Data Preprocessing Pipeline for Disengagement Early-Warning System.
Provides deterministic, transparent data cleaning, outlier clipping, and missingness imputation.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any, List


class LearnerDataPreprocessor:
    """
    Standardized Preprocessor for longitudinal multi-signal learner telemetry.
    Adheres to transparent data rules:
    - Clips values to valid domain limits (e.g., attendance in [0, 1], scores in [0, 100])
    - Creates explicit missingness indicators (crucial for uncertainty estimation)
    - Applies median-based imputation derived strictly from training folds
    - Retains raw values for explainability audits
    """
    
    VALID_BOUNDS = {
        "attendance_rate": (0.0, 1.0),
        "login_count": (0, 100),
        "active_minutes": (0.0, 1440.0),
        "content_views": (0, 500),
        "assignment_submissions": (0, 20),
        "assessment_attempts": (0, 20),
        "average_score": (0.0, 100.0),
        "score_trend": (-100.0, 100.0),
        "help_requests": (0, 50),
        "forum_questions": (0, 50),
        "mentor_contacts": (0, 20),
        "feedback_score": (1.0, 5.0),
        "feedback_sentiment": (-1.0, 1.0)
    }

    def __init__(self):
        self.imputation_values: Dict[str, float] = {}
        self.fitted: bool = False
        
    def fit(self, df: pd.DataFrame) -> "LearnerDataPreprocessor":
        """Learn median imputation values from training data without data leakage."""
        for col in self.VALID_BOUNDS.keys():
            if col in df.columns:
                valid_vals = df[col].dropna()
                self.imputation_values[col] = float(valid_vals.median()) if len(valid_vals) > 0 else 0.0
        self.fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean, clip outliers, generate missingness masks, and impute."""
        if not self.fitted:
            raise ValueError("Preprocessor must be fitted before transform.")
            
        data = df.copy()
        
        # 1. Remove exact duplicates if any
        data = data.drop_duplicates(subset=["learner_id", "week"], keep="first")
        
        # 2. Compute missing feature indicators before imputation
        for col in self.VALID_BOUNDS.keys():
            if col in data.columns:
                data[f"{col}_missing"] = data[col].isnull().astype(int)
        
        # Overall missing feature count per record
        missing_cols = [f"{col}_missing" for col in self.VALID_BOUNDS.keys() if f"{col}_missing" in data.columns]
        data["missing_feature_count"] = data[missing_cols].sum(axis=1)
        
        # 3. Clip outliers to domain valid boundaries
        for col, (lower, upper) in self.VALID_BOUNDS.items():
            if col in data.columns:
                data[col] = data[col].clip(lower=lower, upper=upper)
                
        # 4. Impute missing values with pre-fitted medians
        for col, imp_val in self.imputation_values.items():
            if col in data.columns:
                data[col] = data[col].fillna(imp_val)
                
        return data

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fit on dataset and transform."""
        return self.fit(df).transform(df)


def validate_raw_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform audit validation on raw input dataframe.
    Returns audit status, row count, null percentages, and range violations.
    """
    report: Dict[str, Any] = {
        "total_records": len(df),
        "unique_learners": df["learner_id"].nunique() if "learner_id" in df.columns else 0,
        "weeks_present": sorted(df["week"].unique().tolist()) if "week" in df.columns else [],
        "missing_summary": df.isnull().mean().to_dict(),
        "violations": []
    }
    
    # Check bounds
    for col, (low, high) in LearnerDataPreprocessor.VALID_BOUNDS.items():
        if col in df.columns:
            non_null = df[col].dropna()
            out_of_bounds = non_null[(non_null < low) | (non_null > high)]
            if len(out_of_bounds) > 0:
                report["violations"].append(f"{col}: {len(out_of_bounds)} values outside [{low}, {high}]")
                
    return report
