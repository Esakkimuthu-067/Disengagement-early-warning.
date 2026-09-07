"""
Model Training Module for Disengagement Early-Warning System.
Trains transparent, interpretable classifiers (Logistic Regression, Random Forest, Gradient Boosting).
Saves models with joblib and performs multi-signal ablation experiments.
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from src.baseline import evaluate_model
from src.feature_engineering import get_feature_groups


# Full candidate feature set across all 5 learning signals
CORE_FEATURES = [
    # Attendance
    "attendance_rate",
    "sessions_attended",
    "attendance_change",
    # Activity
    "active_minutes",
    "login_count",
    "content_views",
    "assignment_submissions",
    "activity_change",
    "submission_rate",
    # Assessment
    "average_score",
    "assessment_attempts",
    "score_trend",
    "score_change",
    # Help Seeking
    "help_requests",
    "forum_questions",
    "mentor_contacts",
    "help_seeking_frequency",
    # Feedback
    "feedback_score",
    "feedback_sentiment",
    "feedback_signal",
    # Meta / Composite
    "overall_engagement_score",
    "engagement_trend",
    "missing_feature_count"
]


def prepare_datasets(df: pd.DataFrame, test_size: float = 0.25, random_seed: int = 42):
    """
    Stratified split of learners into train and held-out test sets.
    """
    X = df[CORE_FEATURES].copy()
    y = df["support_needed"].values
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_seed, stratify=y
    )
    return X_train, X_test, y_train, y_test


def train_models(
    X_train: pd.DataFrame,
    y_train: np.ndarray,
    random_seed: int = 42
) -> Dict[str, Any]:
    """
    Trains:
    1. Logistic Regression (scaled, L2 penalty, interpretable odds-ratios)
    2. Random Forest (balanced class weights, shallow depth for transparency)
    3. Gradient Boosting (for comparison)
    """
    models = {}
    
    # 1. Logistic Regression (Transparent linear combination)
    lr_pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(
            C=0.8,
            class_weight="balanced",
            max_iter=1000,
            random_state=random_seed
        ))
    ])
    lr_pipe.fit(X_train, y_train)
    models["logistic_regression"] = lr_pipe
    
    # 2. Random Forest (Transparent non-linear ensemble)
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        min_samples_split=10,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=random_seed,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    models["random_forest"] = rf
    
    # 3. Gradient Boosting Classifier
    gb = GradientBoostingClassifier(
        n_estimators=80,
        learning_rate=0.08,
        max_depth=4,
        random_state=random_seed
    )
    gb.fit(X_train, y_train)
    models["gradient_boosting"] = gb
    
    return models


def run_cross_validation(models: Dict[str, Any], X: pd.DataFrame, y: np.ndarray, cv: int = 5) -> Dict[str, Dict[str, float]]:
    """Evaluates 5-fold stratified cross-validation on all models."""
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    cv_results = {}
    
    for name, model in models.items():
        f1_scores = cross_val_score(model, X, y, cv=skf, scoring="f1")
        roc_scores = cross_val_score(model, X, y, cv=skf, scoring="roc_auc")
        rec_scores = cross_val_score(model, X, y, cv=skf, scoring="recall")
        prec_scores = cross_val_score(model, X, y, cv=skf, scoring="precision")
        
        cv_results[name] = {
            "f1_mean": round(float(np.mean(f1_scores)), 4),
            "f1_std": round(float(np.std(f1_scores)), 4),
            "roc_auc_mean": round(float(np.mean(roc_scores)), 4),
            "roc_auc_std": round(float(np.std(roc_scores)), 4),
            "recall_mean": round(float(np.mean(rec_scores)), 4),
            "precision_mean": round(float(np.mean(prec_scores)), 4)
        }
    return cv_results


def run_ablation_experiment(
    df_train: pd.DataFrame,
    df_test: pd.DataFrame,
    random_seed: int = 42
) -> List[Dict[str, Any]]:
    """
    Section 19: Avoid Single-Indicator Dependence.
    Trains Random Forest models using:
    1. Attendance only
    2. Assessment only
    3. Activity only
    4. Attendance + Assessment
    5. All five signal groups
    """
    groups = get_feature_groups()
    configs = [
        ("Attendance only", groups["attendance"]),
        ("Assessment only", groups["assessment"]),
        ("Activity only", groups["activity"]),
        ("Attendance + Assessment", groups["attendance"] + groups["assessment"]),
        ("All signals", CORE_FEATURES)
    ]
    
    y_train = df_train["support_needed"].values
    y_test = df_test["support_needed"].values
    
    results = []
    for name, features in configs:
        rf = RandomForestClassifier(
            n_estimators=80, max_depth=5, class_weight="balanced", random_state=random_seed
        )
        rf.fit(df_train[features], y_train)
        preds = rf.predict(df_test[features])
        probs = rf.predict_proba(df_test[features])[:, 1]
        
        metrics = evaluate_model(y_test, preds, probs)
        results.append({
            "configuration": name,
            "feature_count": len(features),
            "f1": metrics["f1"],
            "recall": metrics["recall"],
            "precision": metrics["precision"],
            "accuracy": metrics["accuracy"],
            "roc_auc": metrics["roc_auc"]
        })
        
    return results


def save_artifacts(models: Dict[str, Any], output_dir: str = "models"):
    """Persist trained models to disk using joblib."""
    os.makedirs(output_dir, exist_ok=True)
    for name, model in models.items():
        path = os.path.join(output_dir, f"{name}.joblib")
        joblib.dump(model, path)
        print(f"Saved model artifact: {path}")
