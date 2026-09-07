import React from 'react';
import { 
  Users, 
  AlertTriangle, 
  Clock, 
  CheckCircle2, 
  HelpCircle, 
  Sparkles, 
  ShieldAlert,
  BarChart3,
  BookOpen,
  MessageSquare,
  Award
} from 'lucide-react';
import { PipelineResults, Language } from '../types';
import { translations } from '../i18n';

interface DashboardOverviewProps {
  data: PipelineResults;
  language: Language;
  highContrast: boolean;
  onNavigateToLearners: (tierFilter?: string) => void;
}

export const DashboardOverview: React.FC<DashboardOverviewProps> = ({
  data,
  language,
  highContrast,
  onNavigateToLearners
}) => {
  const t = translations[language];
  const active = data.week_5_active_learners;
  const total = active.length;

  const highCount = active.filter(l => l.risk_level === 'High Support Need').length;
  const modCount = active.filter(l => l.risk_level === 'Moderate Support Need').length;
  const lowCount = active.filter(l => l.risk_level === 'Low Support Need').length;
  const insufCount = active.filter(l => l.risk_level === 'Insufficient Data').length;

  const avgEng = (active.reduce((acc, l) => acc + l.overall_engagement_score, 0) / total).toFixed(1);
  const avgConf = (active.reduce((acc, l) => acc + l.confidence_percentage, 0) / total).toFixed(1);

  return (
    <div className="space-y-6">
      {/* Ethical Charter Banner */}
      <div className={`p-4 rounded-xl border ${
        highContrast 
          ? 'bg-slate-900 border-white text-white' 
          : 'bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200 text-blue-950'
      }`}>
        <div className="flex items-start gap-3">
          <Sparkles className="w-5 h-5 text-blue-600 mt-0.5 shrink-0" />
          <div className="text-sm">
            <span className="font-bold">Transparent Support Architecture: </span>
            <span>
              This system does not rank or discipline students. It synthesizes 5 behavioral streams—attendance, 
              learning activity, assessments, help-seeking, and learner feedback—to highlight learners who 
              may benefit from empathetic mentor check-ins, while actively communicating confidence and missing-data limits.
            </span>
          </div>
        </div>
      </div>

      {/* KPI Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <div className={`p-4 rounded-xl border shadow-sm transition-all ${
          highContrast ? 'bg-black border-white text-white' : 'bg-white border-slate-200 text-slate-900'
        }`}>
          <div className="flex items-center justify-between text-slate-500 mb-1">
            <span className="text-xs font-medium">{t.total_learners}</span>
            <Users className="w-4 h-4 text-slate-400" />
          </div>
          <div className="text-2xl font-bold">{total.toLocaleString()}</div>
          <div className="text-xs text-slate-400 mt-1">Week 5 Telemetry</div>
        </div>

        {/* High Support Need */}
        <button
          onClick={() => onNavigateToLearners('High Support Need')}
          className={`p-4 rounded-xl border text-left transition-all hover:scale-[1.02] shadow-sm cursor-pointer ${
            highContrast ? 'bg-red-950 border-red-500 text-white' : 'bg-red-50/70 border-red-200 text-red-950 hover:bg-red-50'
          }`}
        >
          <div className="flex items-center justify-between text-red-600 mb-1">
            <span className="text-xs font-semibold flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-red-600"></span>
              {t.high_support}
            </span>
            <AlertTriangle className="w-4 h-4 text-red-500" />
          </div>
          <div className="text-2xl font-bold text-red-700">{highCount}</div>
          <div className="text-xs text-red-600 mt-1 font-medium">{((highCount / total) * 100).toFixed(1)}% of cohort</div>
        </button>

        {/* Moderate Support Need */}
        <button
          onClick={() => onNavigateToLearners('Moderate Support Need')}
          className={`p-4 rounded-xl border text-left transition-all hover:scale-[1.02] shadow-sm cursor-pointer ${
            highContrast ? 'bg-amber-950 border-amber-500 text-white' : 'bg-amber-50/70 border-amber-200 text-amber-950 hover:bg-amber-50'
          }`}
        >
          <div className="flex items-center justify-between text-amber-600 mb-1">
            <span className="text-xs font-semibold flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-amber-500"></span>
              {t.moderate_support}
            </span>
            <Clock className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-bold text-amber-700">{modCount}</div>
          <div className="text-xs text-amber-600 mt-1 font-medium">{((modCount / total) * 100).toFixed(1)}% of cohort</div>
        </button>

        {/* Low Support Need */}
        <button
          onClick={() => onNavigateToLearners('Low Support Need')}
          className={`p-4 rounded-xl border text-left transition-all hover:scale-[1.02] shadow-sm cursor-pointer ${
            highContrast ? 'bg-emerald-950 border-emerald-500 text-white' : 'bg-emerald-50/70 border-emerald-200 text-emerald-950 hover:bg-emerald-50'
          }`}
        >
          <div className="flex items-center justify-between text-emerald-600 mb-1">
            <span className="text-xs font-semibold flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              {t.low_support}
            </span>
            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="text-2xl font-bold text-emerald-700">{lowCount}</div>
          <div className="text-xs text-emerald-600 mt-1 font-medium">{((lowCount / total) * 100).toFixed(1)}% thriving</div>
        </button>

        {/* Insufficient Data */}
        <button
          onClick={() => onNavigateToLearners('Insufficient Data')}
          className={`p-4 rounded-xl border text-left transition-all hover:scale-[1.02] shadow-sm cursor-pointer ${
            highContrast ? 'bg-slate-900 border-slate-400 text-white' : 'bg-slate-50 border-slate-300 text-slate-800 hover:bg-slate-100'
          }`}
        >
          <div className="flex items-center justify-between text-slate-500 mb-1">
            <span className="text-xs font-semibold flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-slate-400"></span>
              {t.insufficient_data}
            </span>
            <HelpCircle className="w-4 h-4 text-slate-400" />
          </div>
          <div className="text-2xl font-bold text-slate-700">{insufCount}</div>
          <div className="text-xs text-slate-500 mt-1 font-medium">Overconfident flags deferred</div>
        </button>

        {/* Avg Evidence Confidence */}
        <div className={`p-4 rounded-xl border shadow-sm ${
          highContrast ? 'bg-black border-white text-white' : 'bg-white border-slate-200 text-slate-900'
        }`}>
          <div className="flex items-center justify-between text-slate-500 mb-1">
            <span className="text-xs font-medium">{t.avg_confidence}</span>
            <BarChart3 className="w-4 h-4 text-blue-500" />
          </div>
          <div className="text-2xl font-bold text-blue-600">{avgConf}%</div>
          <div className="text-xs text-slate-400 mt-1">Calibrated margin</div>
        </div>
      </div>

      {/* 5-Signal Breakdown Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div className={`p-4 rounded-xl border ${highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200'}`}>
          <div className="flex items-center gap-2 mb-2 text-blue-600 font-semibold text-sm">
            <BookOpen className="w-4 h-4" />
            1. Attendance
          </div>
          <p className="text-xs text-slate-500 leading-relaxed">
            Live lectures, session consistency, and week-over-week attendance velocity.
          </p>
        </div>

        <div className={`p-4 rounded-xl border ${highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200'}`}>
          <div className="flex items-center gap-2 mb-2 text-indigo-600 font-semibold text-sm">
            <Clock className="w-4 h-4" />
            2. Study Activity
          </div>
          <p className="text-xs text-slate-500 leading-relaxed">
            Active platform minutes, login frequency, content views, and assignment submissions.
          </p>
        </div>

        <div className={`p-4 rounded-xl border ${highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200'}`}>
          <div className="flex items-center gap-2 mb-2 text-emerald-600 font-semibold text-sm">
            <Award className="w-4 h-4" />
            3. Assessment
          </div>
          <p className="text-xs text-slate-500 leading-relaxed">
            Quiz scores, submission timeliness, grade trajectory, and attempt persistence.
          </p>
        </div>

        <div className={`p-4 rounded-xl border ${highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200'}`}>
          <div className="flex items-center gap-2 mb-2 text-purple-600 font-semibold text-sm">
            <HelpCircle className="w-4 h-4" />
            4. Help-Seeking
          </div>
          <p className="text-xs text-slate-500 leading-relaxed">
            Forum participation, mentor inquiries, question posting, and office-hour visits.
          </p>
        </div>

        <div className={`p-4 rounded-xl border ${highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200'}`}>
          <div className="flex items-center gap-2 mb-2 text-amber-600 font-semibold text-sm">
            <MessageSquare className="w-4 h-4" />
            5. Learner Feedback
          </div>
          <p className="text-xs text-slate-500 leading-relaxed">
            Self-reported pacing comfort, weekly sentiment surveys, and course satisfaction.
          </p>
        </div>
      </div>

      {/* Cohort Distribution Visualizer */}
      <div className={`p-5 rounded-xl border ${highContrast ? 'bg-black border-slate-800' : 'bg-white border-slate-200'} space-y-4`}>
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500">
            Active Cohort Support Prioritisation Spectrum
          </h3>
          <span className="text-xs text-slate-400">Total N = {total.toLocaleString()}</span>
        </div>

        {/* Stacked Progress Bar */}
        <div className="h-4 w-full bg-slate-100 rounded-full overflow-hidden flex shadow-inner">
          <div 
            style={{ width: `${(lowCount / total) * 100}%` }} 
            className="bg-emerald-500 transition-all hover:opacity-90" 
            title={`Low Support: ${lowCount} (${((lowCount/total)*100).toFixed(1)}%)`}
          />
          <div 
            style={{ width: `${(modCount / total) * 100}%` }} 
            className="bg-amber-400 transition-all hover:opacity-90" 
            title={`Moderate Support: ${modCount} (${((modCount/total)*100).toFixed(1)}%)`}
          />
          <div 
            style={{ width: `${(highCount / total) * 100}%` }} 
            className="bg-red-500 transition-all hover:opacity-90" 
            title={`High Support: ${highCount} (${((highCount/total)*100).toFixed(1)}%)`}
          />
          <div 
            style={{ width: `${(insufCount / total) * 100}%` }} 
            className="bg-slate-400 transition-all hover:opacity-90" 
            title={`Insufficient Data: ${insufCount} (${((insufCount/total)*100).toFixed(1)}%)`}
          />
        </div>

        <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-medium pt-1">
          <div className="flex items-center gap-1.5 text-emerald-700">
            <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
            Low Support Need ({((lowCount / total) * 100).toFixed(1)}%)
          </div>
          <div className="flex items-center gap-1.5 text-amber-700">
            <span className="w-3 h-3 rounded-full bg-amber-400"></span>
            Moderate Support Need ({((modCount / total) * 100).toFixed(1)}%)
          </div>
          <div className="flex items-center gap-1.5 text-red-700">
            <span className="w-3 h-3 rounded-full bg-red-500"></span>
            High Support Need ({((highCount / total) * 100).toFixed(1)}%)
          </div>
          <div className="flex items-center gap-1.5 text-slate-600">
            <span className="w-3 h-3 rounded-full bg-slate-400"></span>
            Insufficient Data ({((insufCount / total) * 100).toFixed(1)}%)
          </div>
        </div>
      </div>
    </div>
  );
};
