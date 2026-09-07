export type Language = 'en' | 'ta';

export type SupportTier = 
  | 'Low Support Need'
  | 'Moderate Support Need'
  | 'High Support Need'
  | 'Insufficient Data';

export type UncertaintyCategory =
  | 'High confidence'
  | 'Medium confidence'
  | 'Low confidence'
  | 'Insufficient evidence';

export interface LearnerRecord {
  learner_id: string;
  course_id: string;
  week: number;
  attendance_rate: number;
  sessions_attended: number;
  attendance_change: number;
  active_minutes: number;
  login_count: number;
  content_views: number;
  assignment_submissions: number;
  activity_change: number;
  submission_rate: number;
  average_score: number;
  assessment_attempts: number;
  score_trend: number;
  score_change: number;
  help_requests: number;
  forum_questions: number;
  mentor_contacts: number;
  help_seeking_frequency: number;
  feedback_score: number;
  feedback_sentiment: number;
  feedback_signal: number;
  overall_engagement_score: number;
  engagement_trend: number;
  missing_feature_count: number;
  support_probability: number;
  predicted_support: number;
  risk_level: SupportTier;
  confidence_percentage: number;
  uncertainty_category: UncertaintyCategory;
  uncertainty_warning: string;
  explanation_reasons: string[];
  explanation_strengths: string[];
  recommended_action: string;
  recommended_action_tamil: string;
}

export interface MetricComparisonRow {
  Metric: string;
  Baseline: string;
  "Improved Model": string;
  Improvement: string;
}

export interface ModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1: number;
  roc_auc: number;
  confusion_matrix: number[][];
  tn: number;
  fp: number;
  fn: number;
  tp: number;
}

export interface AblationRow {
  configuration: string;
  feature_count: number;
  f1: number;
  recall: number;
  precision: number;
  accuracy: number;
  roc_auc: number;
}

export interface WeeklyBacktestProgression {
  week: number;
  learner_count: number;
  actual_support_needed: number;
  baseline: {
    accuracy: number;
    precision: number;
    recall: number;
    f1: number;
    roc_auc: number;
    false_positives: number;
    false_negatives: number;
  };
  improved_model: {
    accuracy: number;
    precision: number;
    recall: number;
    f1: number;
    roc_auc: number;
    false_positives: number;
    false_negatives: number;
  };
  f1_improvement: number;
  recall_improvement: number;
}

export interface PipelineResults {
  execution_timestamp: string;
  dataset_statistics: {
    total_records: number;
    unique_learners: number;
    support_needed_rate: number;
    mean_overall_engagement: number;
  };
  baseline_metrics: ModelMetrics;
  improved_metrics: ModelMetrics;
  before_after_comparison: MetricComparisonRow[];
  cross_validation: Record<string, {
    f1_mean: number;
    f1_std: number;
    roc_auc_mean: number;
    roc_auc_std: number;
  }>;
  ablation_study: AblationRow[];
  backtest_results: {
    weekly_progression: WeeklyBacktestProgression[];
    earlier_identification_insight: string;
  };
  missing_data_summary: {
    total_records: number;
    records_with_any_missing: number;
    missing_rate_overall: number;
    feature_missing_percentages: Record<string, number>;
    insufficient_data_count: number;
    insufficient_data_rate: number;
  };
  missing_data_performance: {
    complete_cohort: { sample_size: number; metrics: ModelMetrics };
    missing_cohort: { sample_size: number; metrics: ModelMetrics };
  };
  error_analysis: {
    total_evaluated: number;
    false_positives: number;
    false_negatives: number;
    fp_drivers: string[];
    fn_drivers: string[];
  };
  feature_importances: Array<{
    feature: string;
    importance: number;
    percentage: number;
  }>;
  week_5_active_learners: LearnerRecord[];
}
