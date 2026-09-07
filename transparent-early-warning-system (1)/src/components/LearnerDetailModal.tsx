import React, { useState } from 'react';
import { 
  X, 
  AlertTriangle, 
  CheckCircle2, 
  Clock, 
  HelpCircle, 
  Award, 
  MessageSquare, 
  BookOpen, 
  TrendingUp, 
  TrendingDown, 
  Sparkles, 
  Send,
  ShieldAlert,
  ArrowRight
} from 'lucide-react';
import { LearnerRecord, Language } from '../types';
import { translations } from '../i18n';

interface LearnerDetailModalProps {
  learner: LearnerRecord | null;
  language: Language;
  highContrast: boolean;
  onClose: () => void;
}

export const LearnerDetailModal: React.FC<LearnerDetailModalProps> = ({
  learner,
  language,
  highContrast,
  onClose
}) => {
  const [actionLogged, setActionLogged] = useState<boolean>(false);
  if (!learner) return null;

  const t = translations[language];

  const handleLogAction = () => {
    setActionLogged(true);
    setTimeout(() => {
      setActionLogged(false);
    }, 4000);
  };

  const renderTierIcon = () => {
    switch (learner.risk_level) {
      case 'High Support Need':
        return <span className="w-3 h-3 rounded-full bg-red-600 inline-block"></span>;
      case 'Moderate Support Need':
        return <span className="w-3 h-3 rounded-full bg-amber-500 inline-block"></span>;
      case 'Low Support Need':
        return <span className="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span>;
      case 'Insufficient Data':
        return <HelpCircle className="w-3.5 h-3.5 text-slate-500 inline-block" />;
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs overflow-y-auto">
      <div 
        className={`w-full max-w-4xl rounded-2xl border shadow-2xl overflow-hidden my-8 transition-all ${
          highContrast ? 'bg-black text-white border-white' : 'bg-white text-slate-900 border-slate-200'
        }`}
        role="dialog"
        aria-modal="true"
      >
        {/* Modal Header */}
        <div className={`p-6 border-b flex items-start justify-between ${
          highContrast ? 'border-slate-800 bg-slate-900' : 'border-slate-200 bg-slate-50/80'
        }`}>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="font-mono text-xl font-bold tracking-tight text-blue-600">
                {learner.learner_id}
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-slate-200 text-slate-700 font-semibold">
                {learner.course_id}
              </span>
              <span className="text-xs text-slate-400">Week {learner.week}</span>
            </div>
            <div className="flex items-center gap-3 text-xs">
              <span className="inline-flex items-center gap-1.5 font-bold">
                {renderTierIcon()}
                {learner.risk_level}
              </span>
              <span className="text-slate-400">•</span>
              <span>Evidence Confidence: <strong>{learner.confidence_percentage.toFixed(0)}%</strong> ({learner.uncertainty_category})</span>
              <span className="text-slate-400">•</span>
              <span>Support Probability: <strong>{(learner.support_probability * 100).toFixed(1)}%</strong></span>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-200 transition-colors"
            aria-label={t.close}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Content */}
        <div className="p-6 space-y-6 max-h-[75vh] overflow-y-auto">
          {/* Missing Data / Uncertainty Banner */}
          {learner.missing_feature_count > 0 && (
            <div className="p-3.5 rounded-xl border border-amber-300 bg-amber-50 text-amber-900 text-xs flex items-start gap-2.5">
              <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
              <div>
                <span className="font-bold">Missing Telemetry Warning: </span>
                <span>{learner.uncertainty_warning}</span>
                <div className="mt-1 text-[11px] text-amber-800">
                  {t.missing_notice} Always check in with the learner directly before assuming disengagement.
                </div>
              </div>
            </div>
          )}

          {/* 5-Signal Breakdown Grid */}
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
              {t.signals_profile}
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3 text-xs">
              {/* 1. Attendance */}
              <div className="p-3 rounded-xl border border-slate-200 bg-slate-50/50">
                <div className="flex items-center justify-between text-blue-600 mb-1 font-semibold">
                  <span className="flex items-center gap-1"><BookOpen className="w-3.5 h-3.5" /> {t.attendance}</span>
                  {learner.attendance_change >= 0 ? (
                    <span className="text-emerald-600 flex items-center text-[10px]"><TrendingUp className="w-3 h-3" /> +{(learner.attendance_change * 100).toFixed(0)}%</span>
                  ) : (
                    <span className="text-red-600 flex items-center text-[10px]"><TrendingDown className="w-3 h-3" /> {(learner.attendance_change * 100).toFixed(0)}%</span>
                  )}
                </div>
                <div className="text-lg font-bold">{(learner.attendance_rate * 100).toFixed(0)}%</div>
                <div className="text-[11px] text-slate-500 mt-1">{learner.sessions_attended} sessions attended</div>
              </div>

              {/* 2. Activity */}
              <div className="p-3 rounded-xl border border-slate-200 bg-slate-50/50">
                <div className="flex items-center justify-between text-indigo-600 mb-1 font-semibold">
                  <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> {t.activity}</span>
                  {learner.activity_change >= 0 ? (
                    <span className="text-emerald-600 flex items-center text-[10px]"><TrendingUp className="w-3 h-3" /> +{learner.activity_change.toFixed(0)}m</span>
                  ) : (
                    <span className="text-red-600 flex items-center text-[10px]"><TrendingDown className="w-3 h-3" /> {learner.activity_change.toFixed(0)}m</span>
                  )}
                </div>
                <div className="text-lg font-bold">{learner.active_minutes.toFixed(0)} min</div>
                <div className="text-[11px] text-slate-500 mt-1">{learner.login_count} logins • {learner.assignment_submissions} submissions</div>
              </div>

              {/* 3. Assessment */}
              <div className="p-3 rounded-xl border border-slate-200 bg-slate-50/50">
                <div className="flex items-center justify-between text-emerald-600 mb-1 font-semibold">
                  <span className="flex items-center gap-1"><Award className="w-3.5 h-3.5" /> {t.assessment}</span>
                  {learner.score_change >= 0 ? (
                    <span className="text-emerald-600 flex items-center text-[10px]"><TrendingUp className="w-3 h-3" /> +{learner.score_change.toFixed(0)}%</span>
                  ) : (
                    <span className="text-red-600 flex items-center text-[10px]"><TrendingDown className="w-3 h-3" /> {learner.score_change.toFixed(0)}%</span>
                  )}
                </div>
                <div className="text-lg font-bold">{learner.average_score.toFixed(1)}%</div>
                <div className="text-[11px] text-slate-500 mt-1">{learner.assessment_attempts} attempt(s) logged</div>
              </div>

              {/* 4. Help Seeking */}
              <div className="p-3 rounded-xl border border-slate-200 bg-slate-50/50">
                <div className="flex items-center justify-between text-purple-600 mb-1 font-semibold">
                  <span className="flex items-center gap-1"><HelpCircle className="w-3.5 h-3.5" /> {t.help_seeking}</span>
                </div>
                <div className="text-lg font-bold">{learner.help_seeking_frequency} inquiries</div>
                <div className="text-[11px] text-slate-500 mt-1">{learner.forum_questions} forums • {learner.mentor_contacts} mentor chats</div>
              </div>

              {/* 5. Feedback */}
              <div className="p-3 rounded-xl border border-slate-200 bg-slate-50/50">
                <div className="flex items-center justify-between text-amber-600 mb-1 font-semibold">
                  <span className="flex items-center gap-1"><MessageSquare className="w-3.5 h-3.5" /> {t.feedback}</span>
                </div>
                <div className="text-lg font-bold">{learner.feedback_score.toFixed(1)} / 5.0</div>
                <div className="text-[11px] text-slate-500 mt-1">Sentiment: {learner.feedback_sentiment >= 0 ? 'Positive' : 'Concerned'}</div>
              </div>
            </div>
          </div>

          {/* Explainability Section: Reasons vs Strengths */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Reasons */}
            <div className={`p-4 rounded-xl border ${
              highContrast ? 'bg-slate-950 border-red-800' : 'bg-red-50/40 border-red-200'
            }`}>
              <h4 className="text-xs font-bold text-red-700 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <AlertTriangle className="w-4 h-4" />
                {t.reasons_title}
              </h4>
              <ul className="space-y-1.5 text-xs text-slate-700">
                {learner.explanation_reasons.length > 0 ? (
                  learner.explanation_reasons.map((r, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="text-red-500 font-bold">•</span>
                      <span>{r}</span>
                    </li>
                  ))
                ) : (
                  <li className="text-slate-500 italic">No adverse behavioral warning flags detected.</li>
                )}
              </ul>
            </div>

            {/* Strengths */}
            <div className={`p-4 rounded-xl border ${
              highContrast ? 'bg-slate-950 border-emerald-800' : 'bg-emerald-50/40 border-emerald-200'
            }`}>
              <h4 className="text-xs font-bold text-emerald-700 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                {t.strengths_title}
              </h4>
              <ul className="space-y-1.5 text-xs text-slate-700">
                {learner.explanation_strengths.length > 0 ? (
                  learner.explanation_strengths.map((s, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="text-emerald-500 font-bold">★</span>
                      <span>{s}</span>
                    </li>
                  ))
                ) : (
                  <li className="text-slate-500 italic">Historical baseline being established.</li>
                )}
              </ul>
            </div>
          </div>

          {/* Recommended Mentor Action (English & Tamil) */}
          <div className={`p-5 rounded-xl border ${
            highContrast ? 'bg-blue-950 border-blue-600' : 'bg-blue-50/60 border-blue-200'
          }`}>
            <h4 className="text-xs font-bold text-blue-800 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <Sparkles className="w-4 h-4 text-blue-600" />
              {t.action_title}
            </h4>

            {/* English Action */}
            <div className="text-sm font-semibold text-blue-950 mb-2">
              🤝 {learner.recommended_action}
            </div>

            {/* Tamil Action */}
            <div className="text-xs text-blue-800 italic bg-blue-100/50 p-2.5 rounded-lg border border-blue-200">
              🇮🇳 <strong>தமிழ் வழிகாட்டுதல்: </strong>
              {learner.recommended_action_tamil}
            </div>

            {/* Log Action Button */}
            <div className="mt-4 flex items-center justify-between pt-2 border-t border-blue-200/60">
              <span className="text-xs text-slate-500">
                Record outreach in student support log:
              </span>
              <button
                id="log-mentor-action-btn"
                onClick={handleLogAction}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold shadow flex items-center gap-1.5 transition-colors"
              >
                <Send className="w-3.5 h-3.5" />
                Log Outreach Completed
              </button>
            </div>

            {actionLogged && (
              <div className="mt-2 text-xs text-emerald-700 font-medium flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                Support outreach logged successfully for {learner.learner_id}!
              </div>
            )}
          </div>
        </div>

        {/* Modal Footer */}
        <div className={`p-4 border-t flex items-center justify-end ${
          highContrast ? 'border-slate-800 bg-slate-900' : 'border-slate-200 bg-slate-50'
        }`}>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-800 rounded-lg text-xs font-semibold transition-colors"
          >
            {t.close}
          </button>
        </div>
      </div>
    </div>
  );
};
