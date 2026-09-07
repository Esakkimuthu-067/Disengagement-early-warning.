"""
Synthetic Learner Data Generator for Disengagement Early-Warning System.
Generates realistic multi-signal longitudinal learner records with realistic missingness.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any


def generate_synthetic_data(
    n_learners: int = 1200,
    n_weeks: int = 5,
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Generate synthetic learner records across 5 weeks.
    Total records = n_learners * n_weeks (default 1,200 * 5 = 6,000 records >= 5,000).
    
    Signals included:
    1. Attendance (sessions_available, sessions_attended, attendance_rate)
    2. Activity (login_count, active_minutes, content_views, assignment_submissions)
    3. Assessment (assessment_attempts, average_score, score_trend)
    4. Help Seeking (help_requests, forum_questions, mentor_contacts)
    5. Feedback (feedback_score, feedback_sentiment)
    """
    np.random.seed(random_seed)
    
    courses = ["CS-101", "DATA-201", "AI-301", "WEB-102"]
    course_probs = [0.35, 0.25, 0.25, 0.15]
    
    records = []
    
    # Each learner has an underlying trajectory and base engagement level
    for i in range(1, n_learners + 1):
        learner_id = f"LNR-{i:04d}"
        course_id = np.random.choice(courses, p=course_probs)
        
        # Latent learner profiles:
        # 0: Consistently high engagement (~50%)
        # 1: Moderate steady engagement (~25%)
        # 2: Gradual disengagement / struggles (~18%)
        # 3: Sudden disengagement (~7%)
        profile = np.random.choice([0, 1, 2, 3], p=[0.50, 0.25, 0.18, 0.07])
        
        # Base abilities
        base_ability = np.random.normal(72, 12)
        base_ability = np.clip(base_ability, 35, 98)
        
        prev_score = base_ability
        prev_attendance = np.random.uniform(0.7, 1.0)
        prev_activity = np.random.uniform(120, 300)
        
        for week in range(1, n_weeks + 1):
            sessions_available = np.random.choice([2, 3, 4], p=[0.2, 0.6, 0.2])
            
            # Trajectory modulation based on profile
            if profile == 0:  # High engagement
                att_prob = np.random.uniform(0.85, 1.0)
                active_min = np.random.normal(210, 40)
                logins = int(np.random.poisson(9) + 2)
                views = int(np.random.poisson(28) + 5)
                submissions = np.random.choice([1, 2], p=[0.2, 0.8])
                attempts = np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])
                score = np.random.normal(base_ability + 2, 6)
                help_req = int(np.random.poisson(0.8))
                forum_q = int(np.random.poisson(1.2))
                mentor_c = int(np.random.poisson(0.4))
                fb_score = np.random.choice([4.0, 4.5, 5.0], p=[0.2, 0.4, 0.4])
                fb_sentiment = np.random.uniform(0.4, 0.9)
                
            elif profile == 1:  # Moderate engagement
                att_prob = np.random.uniform(0.65, 0.85)
                active_min = np.random.normal(140, 35)
                logins = int(np.random.poisson(6) + 1)
                views = int(np.random.poisson(18) + 3)
                submissions = np.random.choice([0, 1, 2], p=[0.1, 0.7, 0.2])
                attempts = np.random.choice([1, 2], p=[0.8, 0.2])
                score = np.random.normal(base_ability, 8)
                help_req = int(np.random.poisson(0.5))
                forum_q = int(np.random.poisson(0.7))
                mentor_c = int(np.random.poisson(0.2))
                fb_score = np.random.choice([3.0, 3.5, 4.0], p=[0.3, 0.4, 0.3])
                fb_sentiment = np.random.uniform(0.0, 0.5)
                
            elif profile == 2:  # Gradual disengagement
                decay = max(0.2, 1.0 - (week - 1) * 0.18)
                att_prob = np.random.uniform(0.2, 0.6) * decay
                active_min = max(10, np.random.normal(130 * decay, 30))
                logins = max(0, int(np.random.poisson(5 * decay)))
                views = max(1, int(np.random.poisson(15 * decay)))
                submissions = 1 if (np.random.rand() > 0.4 * (week / 2)) else 0
                attempts = max(0, int(np.random.poisson(1.5 * decay)))
                score = np.random.normal(base_ability - (week * 5), 10)
                help_req = int(np.random.poisson(0.3))  # Help seeking often drops!
                forum_q = int(np.random.poisson(0.2))
                mentor_c = int(np.random.poisson(0.1))
                fb_score = np.random.choice([1.5, 2.0, 2.5, 3.0], p=[0.3, 0.4, 0.2, 0.1])
                fb_sentiment = np.random.uniform(-0.6, 0.1)
                
            else:  # Sudden drop around week 3 or 4
                if week <= 2:
                    att_prob = np.random.uniform(0.75, 0.95)
                    active_min = np.random.normal(180, 30)
                    logins = int(np.random.poisson(7) + 1)
                    views = int(np.random.poisson(22) + 2)
                    submissions = 1
                    attempts = 1
                    score = np.random.normal(base_ability, 7)
                    help_req = 1
                    forum_q = 1
                    mentor_c = 0
                    fb_score = 4.0
                    fb_sentiment = 0.5
                else:
                    att_prob = np.random.uniform(0.05, 0.35)
                    active_min = max(5, np.random.normal(30, 15))
                    logins = max(0, int(np.random.poisson(1.2)))
                    views = max(0, int(np.random.poisson(3.0)))
                    submissions = 0
                    attempts = np.random.choice([0, 1], p=[0.7, 0.3])
                    score = np.random.normal(base_ability - 25, 12)
                    help_req = 0
                    forum_q = 0
                    mentor_c = 0
                    fb_score = np.random.choice([1.0, 2.0], p=[0.7, 0.3])
                    fb_sentiment = np.random.uniform(-0.8, -0.2)
            
            # Sessions attended
            sessions_attended = int(np.clip(np.round(sessions_available * att_prob), 0, sessions_available))
            attendance_rate = round(sessions_attended / sessions_available, 4)
            
            # Clip bounds
            active_min = round(float(np.clip(active_min, 0.0, 480.0)), 1)
            score = round(float(np.clip(score, 0.0, 100.0)), 1)
            score_trend = round(float(score - prev_score), 1)
            prev_score = score
            
            # Calculate Ground Truth: support_needed
            # Multi-signal latent score: Disengagement increases when multiple signals deteriorate.
            # Never depend solely on attendance or score!
            signal_att = 1.0 - attendance_rate  # 0 to 1
            signal_act = 1.0 - np.clip(active_min / 200.0, 0.0, 1.0)
            signal_sub = 1.0 if submissions == 0 else (0.4 if submissions == 1 else 0.0)
            signal_score = 1.0 - np.clip(score / 80.0, 0.0, 1.0)
            signal_feedback = 1.0 - np.clip((fb_score - 1.0) / 4.0, 0.0, 1.0)
            signal_help_isolation = 1.0 if (help_req + forum_q + mentor_c == 0 and signal_score > 0.4) else 0.0
            
            # Weighted latent disengagement propensity
            propensity = (
                0.22 * signal_att +
                0.24 * signal_act +
                0.18 * signal_sub +
                0.18 * signal_score +
                0.12 * signal_feedback +
                0.06 * signal_help_isolation
            )
            
            # Add stochastic noise so target is not a deterministic function
            noise = np.random.normal(0, 0.08)
            propensity_noisy = np.clip(propensity + noise, 0.0, 1.0)
            
            # Classification threshold targeting 22% - 27% positive support need (70-80% No Support)
            support_needed = 1 if propensity_noisy > 0.46 else 0
            
            # Edge-case safety checks:
            # High marks (score > 85) alone must NOT guarantee support_needed=0 if activity and attendance collapsed
            # High activity + submissions alone must NOT be penalized simply for low attendance
            
            records.append({
                "learner_id": learner_id,
                "course_id": course_id,
                "week": week,
                "sessions_available": sessions_available,
                "sessions_attended": sessions_attended,
                "attendance_rate": attendance_rate,
                "login_count": logins,
                "active_minutes": active_min,
                "content_views": views,
                "assignment_submissions": submissions,
                "assessment_attempts": attempts,
                "average_score": score,
                "score_trend": score_trend,
                "help_requests": help_req,
                "forum_questions": forum_q,
                "mentor_contacts": mentor_c,
                "feedback_score": fb_score,
                "feedback_sentiment": round(float(fb_sentiment), 2),
                "support_needed": support_needed
            })
            
    df = pd.DataFrame(records)
    
    # Introduce realistic missing values (MCAR / MAR)
    # 1. feedback_score & feedback_sentiment (22% missing)
    mask_fb = np.random.rand(len(df)) < 0.22
    df.loc[mask_fb, "feedback_score"] = np.nan
    df.loc[mask_fb, "feedback_sentiment"] = np.nan
    
    # 2. help_seeking (12% missing due to unlinked channel)
    mask_help = np.random.rand(len(df)) < 0.12
    df.loc[mask_help, "help_requests"] = np.nan
    df.loc[mask_help, "forum_questions"] = np.nan
    df.loc[mask_help, "mentor_contacts"] = np.nan
    
    # 3. assessment average_score (7% missing when learner didn't sit quiz yet)
    mask_quiz = np.random.rand(len(df)) < 0.07
    df.loc[mask_quiz, "average_score"] = np.nan
    df.loc[mask_quiz, "score_trend"] = np.nan
    
    # 4. active_minutes & content_views (6% telemetry sync failure)
    mask_telemetry = np.random.rand(len(df)) < 0.06
    df.loc[mask_telemetry, "active_minutes"] = np.nan
    df.loc[mask_telemetry, "content_views"] = np.nan
    
    # 5. attendance_rate (4% missing instructor roster)
    mask_att = np.random.rand(len(df)) < 0.04
    df.loc[mask_att, "attendance_rate"] = np.nan
    
    return df


if __name__ == "__main__":
    df = generate_synthetic_data(n_learners=1200, n_weeks=5, random_seed=42)
    print(f"Generated synthetic dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Support needed rate: {df['support_needed'].mean():.2%}")
    print("Missing value counts:")
    print(df.isnull().sum()[df.isnull().sum() > 0])
