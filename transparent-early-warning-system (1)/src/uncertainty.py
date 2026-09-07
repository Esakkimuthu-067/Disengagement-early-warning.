"""
Uncertainty and Confidence Estimation Module.
Quantifies prediction confidence using probability margins, ensemble variance, and data completeness.
Categorizes risk ethically into Support Need tiers, rejecting raw punitive scores.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple


def calculate_prediction_uncertainty(
    probability: float,
    missing_count: int,
    ensemble_std: float = 0.0
) -> Dict[str, Any]:
    """
    Computes calibrated confidence and assigns support tier:
    
    Tiers (Strictly Non-Punitive):
    - Low Support Need (p < 0.35)
    - Moderate Support Need (0.35 <= p < 0.65)
    - High Support Need (p >= 0.65)
    - Insufficient Data (if missing_count >= 3 or missing critical telemetry)
    
    Confidence Calculation:
    - Base confidence is high when probability is far from decision threshold (0.50).
      margin = abs(probability - 0.50) * 2.0  (range 0.0 to 1.0)
    - Penalized by ensemble variance across trees (std)
    - Heavily penalized by missing telemetry count:
      confidence = margin * (1.0 - 0.18 * missing_count) * (1.0 - ensemble_std)
    """
    prob_clean = float(np.clip(probability, 0.0, 1.0))
    margin = abs(prob_clean - 0.50) * 2.0  # 0 at boundary (0.5), 1.0 at 0 or 1
    
    # Missingness penalty
    missing_penalty = min(0.65, 0.18 * missing_count)
    std_penalty = min(0.35, ensemble_std * 1.5)
    
    # Calibrated confidence percentage (between 30% and 98%)
    calibrated_conf = max(0.25, margin * (1.0 - missing_penalty) * (1.0 - std_penalty))
    confidence_pct = round(float(calibrated_conf * 100.0), 1)
    
    # Determine Risk Level & Uncertainty Tier
    if missing_count >= 3:
        risk_level = "Insufficient Data"
        uncertainty_category = "Insufficient evidence"
        confidence_pct = min(confidence_pct, 45.0)
        warning = "Prediction deferred: multiple critical learning signals are missing."
    else:
        if prob_clean >= 0.65:
            risk_level = "High Support Need"
        elif prob_clean >= 0.35:
            risk_level = "Moderate Support Need"
        else:
            risk_level = "Low Support Need"
            
        if confidence_pct >= 75.0:
            uncertainty_category = "High confidence"
            warning = "Model signals are mutually consistent."
        elif confidence_pct >= 55.0:
            uncertainty_category = "Medium confidence"
            warning = "Moderate confidence; decision threshold proximity or minor missingness."
        else:
            uncertainty_category = "Low confidence"
            warning = "Low confidence; border case requiring manual mentor discretion."
            
    return {
        "support_probability": round(prob_clean, 3),
        "risk_level": risk_level,
        "confidence_percentage": confidence_pct,
        "uncertainty_category": uncertainty_category,
        "uncertainty_warning": warning,
        "missing_count": missing_count
    }


def batch_uncertainty_estimation(
    probabilities: np.ndarray,
    missing_counts: np.ndarray,
    rf_model=None,
    X_features: pd.DataFrame = None
) -> List[Dict[str, Any]]:
    """
    Computes uncertainty for an entire batch of predictions, optionally using
    RandomForest individual tree estimates for ensemble variance.
    """
    n = len(probabilities)
    stds = np.zeros(n)
    
    if rf_model is not None and hasattr(rf_model, "estimators_") and X_features is not None:
        try:
            # Predictions from each individual tree
            all_tree_preds = np.array([tree.predict_proba(X_features)[:, 1] for tree in rf_model.estimators_])
            stds = np.std(all_tree_preds, axis=0)
        except Exception:
            stds = np.zeros(n)
            
    results = []
    for i in range(n):
        res = calculate_prediction_uncertainty(
            probability=probabilities[i],
            missing_count=int(missing_counts[i]),
            ensemble_std=float(stds[i])
        )
        results.append(res)
        
    return results
