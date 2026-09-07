"""
Baseline Rule-Based Model for Disengagement Early-Warning System.
Demonstrates the limitations of relying solely on simplistic punitive cut-offs (e.g. attendance & marks).
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix


class RuleBasedBaseline:
    """
    Standard legacy heuristic rule:
    Flags a student if:
      (attendance_rate < 0.60 AND active_minutes < 90)
      OR
      (average_score < 55)
      
    Limitations demonstrated:
    - High false positive rate for self-directed learners who study offline or asynchronously.
    - High false negative rate for struggling learners with inflated or legacy test marks but collapsed engagement.
    """
    
    def __init__(self, att_thresh: float = 0.60, act_thresh: float = 90.0, score_thresh: float = 55.0):
        self.att_thresh = att_thresh
        self.act_thresh = act_thresh
        self.score_thresh = score_thresh

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """Binary predictions based on rule cutoffs."""
        cond1 = (df["attendance_rate"] < self.att_thresh) & (df["active_minutes"] < self.act_thresh)
        cond2 = df["average_score"] < self.score_thresh
        preds = (cond1 | cond2).astype(int).values
        return preds

    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        """
        Approximate continuous score for ROC-AUC calculation:
        Combines inverse attendance and inverse score heuristics.
        """
        att = df["attendance_rate"].fillna(0.7).clip(0.0, 1.0)
        act = (df["active_minutes"].fillna(120).clip(0, 300) / 300.0)
        scr = (df["average_score"].fillna(70).clip(0, 100) / 100.0)
        
        # Heuristic risk score
        risk = (0.5 * (1.0 - att)) + (0.3 * (1.0 - act)) + (0.2 * (1.0 - scr))
        probs = np.clip(risk, 0.01, 0.99)
        # return (N, 2) array like sklearn
        return np.column_stack([1.0 - probs, probs])


def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray = None) -> Dict[str, Any]:
    """
    Computes standard classification metrics:
    Accuracy, Precision, Recall, F1-Score, ROC-AUC, Confusion Matrix.
    """
    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, zero_division=0))
    rec = float(recall_score(y_true, y_pred, zero_division=0))
    f1 = float(f1_score(y_true, y_pred, zero_division=0))
    
    auc = float(roc_auc_score(y_true, y_prob)) if y_prob is not None else 0.0
    cm = confusion_matrix(y_true, y_pred).tolist()
    
    return {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1": round(f1, 4),
        "roc_auc": round(auc, 4),
        "confusion_matrix": cm,
        "tn": cm[0][0] if len(cm) > 1 else 0,
        "fp": cm[0][1] if len(cm) > 1 else 0,
        "fn": cm[1][0] if len(cm) > 1 else 0,
        "tp": cm[1][1] if len(cm) > 1 else 0,
    }
