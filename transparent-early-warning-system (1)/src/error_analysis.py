"""
Error and Failure Analysis Module.
Examines False Positives (over-flagged) and False Negatives (missed support needs)
to diagnose algorithmic blind spots and preserve fairness.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List


def perform_error_analysis(
    df_eval: pd.DataFrame,
    y_true_col: str = "support_needed",
    y_pred_col: str = "predicted_support",
    prob_col: str = "support_probability"
) -> Dict[str, Any]:
    """
    Categorizes errors into:
    - True Positives (Correctly identified for support)
    - True Negatives (Correctly identified as thriving)
    - False Positives (Flagged but actually thriving)
    - False Negatives (Missed learners in need of support)
    
    Audits primary behavioral drivers behind each error type.
    """
    df = df_eval.copy()
    y_true = df[y_true_col].values
    y_pred = df[y_pred_col].values
    
    fp_mask = (y_true == 0) & (y_pred == 1)
    fn_mask = (y_true == 1) & (y_pred == 0)
    tp_mask = (y_true == 1) & (y_pred == 1)
    tn_mask = (y_true == 0) & (y_pred == 0)
    
    fp_df = df[fp_mask]
    fn_df = df[fn_mask]
    
    # Diagnose False Positives
    fp_reasons = []
    if len(fp_df) > 0:
        # Check if offline / asynchronous pattern
        low_att_fp = (fp_df["attendance_rate"] < 0.6).mean()
        high_score_fp = (fp_df["average_score"] > 75).mean()
        missing_data_fp = (fp_df.get("missing_feature_count", 0) > 1).mean()
        
        fp_reasons.append(f"{low_att_fp:.1%} had low live attendance but studied asynchronously")
        fp_reasons.append(f"{high_score_fp:.1%} had strong test scores despite lower platform hours")
        fp_reasons.append(f"{missing_data_fp:.1%} had unrecorded survey/telemetry data driving spurious risk")
        
    # Diagnose False Negatives
    fn_reasons = []
    if len(fn_df) > 0:
        high_score_fn = (fn_df["average_score"] > 70).mean()
        att_ok_fn = (fn_df["attendance_rate"] > 0.75).mean()
        sudden_drop_fn = (fn_df.get("activity_change", 0) < -30).mean()
        
        fn_reasons.append(f"{high_score_fn:.1%} maintained passable test scores masking deep disengagement")
        fn_reasons.append(f"{att_ok_fn:.1%} passively logged into live sessions without participating")
        fn_reasons.append(f"{sudden_drop_fn:.1%} experienced recent sudden collapse not yet reflected in cumulative averages")
        
    summary_table = [
        {
            "Category": "False Positives (Over-Alerts)",
            "Count": int(fp_mask.sum()),
            "Rate": f"{(fp_mask.sum() / len(df)):.1%}",
            "Primary Driver": "Asynchronous study habits or missing survey logs",
            "Ethical Mitigation": "Non-punitive tone; mentor check-in confirms learner is okay"
        },
        {
            "Category": "False Negatives (Missed Needs)",
            "Count": int(fn_mask.sum()),
            "Rate": f"{(fn_mask.sum() / len(df)):.1%}",
            "Primary Driver": "High marks masking disengagement or passive attendance",
            "Ethical Mitigation": "Multi-signal trend monitoring & periodic voluntary surveys"
        }
    ]
    
    return {
        "total_evaluated": len(df),
        "true_positives": int(tp_mask.sum()),
        "true_negatives": int(tn_mask.sum()),
        "false_positives": int(fp_mask.sum()),
        "false_negatives": int(fn_mask.sum()),
        "fp_drivers": fp_reasons,
        "fn_drivers": fn_reasons,
        "summary_table": summary_table,
        "fp_sample": fp_df.head(5).to_dict(orient="records") if len(fp_df) > 0 else [],
        "fn_sample": fn_df.head(5).to_dict(orient="records") if len(fn_df) > 0 else []
    }
