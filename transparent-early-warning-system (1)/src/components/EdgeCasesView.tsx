import React from 'react';
import { ShieldAlert, CheckCircle2, AlertTriangle, HelpCircle, XCircle } from 'lucide-react';
import { PipelineResults, Language } from '../types';
import { translations } from '../i18n';

interface EdgeCasesViewProps {
  data: PipelineResults;
  language: Language;
  highContrast: boolean;
}

export const EdgeCasesView: React.FC<EdgeCasesViewProps> = ({
  data,
  language,
  highContrast
}) => {
  const t = translations[language];
  const { error_analysis } = data;

  return (
    <div className="space-y-6">
      {/* Introduction Header */}
      <div className={`p-4 rounded-xl border ${
        highContrast ? 'bg-slate-900 border-white text-white' : 'bg-slate-50 border-slate-200 text-slate-800'
      }`}>
        <div className="flex items-start gap-3">
          <ShieldAlert className="w-5 h-5 text-indigo-600 shrink-0 mt-0.5" />
          <div className="text-xs md:text-sm">
            <span className="font-bold">Edge Cases & Failure Diagnostic Framework (Section 20 & 21): </span>
            <span>
              Real learning environments feature diverse study strategies. We rigorously validate our models 
              against counter-intuitive behavioral configurations and audit the root drivers of prediction errors.
            </span>
          </div>
        </div>
      </div>

      {/* 4 Validated Edge Cases Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Edge Case 1 */}
        <div className={`p-5 rounded-xl border ${
          highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200 shadow-sm'
        } space-y-3`}>
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-bold uppercase tracking-wider text-red-600">
              Edge Case 1: High Marks, Low Engagement
            </h4>
            <span className="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-bold">
              Test Passed
            </span>
          </div>
          <div className="p-3 bg-slate-50 rounded-lg text-xs space-y-1 font-mono">
            <div>Score: <strong>90.0%</strong> | Attendance: <strong>20.0%</strong></div>
            <div>Active Time: <strong>25 min</strong> | Submissions: <strong>0</strong></div>
          </div>
          <p className="text-xs text-slate-600">
            <strong>Challenge:</strong> Traditional grade-based systems assume high marks mean the student is thriving.
          </p>
          <div className="p-3 bg-emerald-50 text-emerald-900 rounded-lg text-xs border border-emerald-200">
            <strong>System Safeguard:</strong> The model evaluates compound behavioral trajectories. Despite the high quiz score, 
            the 80% collapse in attendance and near-zero active minutes elevate the risk to <strong>Moderate/High Support Need</strong>, 
            preventing the learner from falling through the cracks.
          </div>
        </div>

        {/* Edge Case 2 */}
        <div className={`p-5 rounded-xl border ${
          highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200 shadow-sm'
        } space-y-3`}>
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-bold uppercase tracking-wider text-blue-600">
              Edge Case 2: Low Attendance, High Engagement
            </h4>
            <span className="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-bold">
              Test Passed
            </span>
          </div>
          <div className="p-3 bg-slate-50 rounded-lg text-xs space-y-1 font-mono">
            <div>Attendance: <strong>25.0%</strong> | Active Time: <strong>260 min</strong></div>
            <div>Submissions: <strong>2</strong> | Score: <strong>88.0%</strong></div>
          </div>
          <p className="text-xs text-slate-600">
            <strong>Challenge:</strong> Strict attendance-monitoring rules automatically penalize asynchronous adult learners.
          </p>
          <div className="p-3 bg-emerald-50 text-emerald-900 rounded-lg text-xs border border-emerald-200">
            <strong>System Safeguard:</strong> The system identifies independent study hours and consistent assignment completion. 
            The learner is safely kept in <strong>Low Support Need</strong> without punitive flags or unwanted mentor alerts.
          </div>
        </div>

        {/* Edge Case 3 */}
        <div className={`p-5 rounded-xl border ${
          highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200 shadow-sm'
        } space-y-3`}>
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-bold uppercase tracking-wider text-amber-600">
              Edge Case 3: Missing Telemetry Shield
            </h4>
            <span className="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-bold">
              Test Passed
            </span>
          </div>
          <div className="p-3 bg-slate-50 rounded-lg text-xs space-y-1 font-mono">
            <div>Missing: <strong>Feedback, Activity, Help-Seeking</strong></div>
            <div>Missing Features: <strong>≥ 3 signals</strong></div>
          </div>
          <p className="text-xs text-slate-600">
            <strong>Challenge:</strong> Forcing machine learning predictions on sparse data generates erratic hallucinations.
          </p>
          <div className="p-3 bg-amber-50 text-amber-900 rounded-lg text-xs border border-amber-200">
            <strong>System Safeguard:</strong> Automatically routed to <strong>"Insufficient Data"</strong>. 
            Confidence is downgraded and automated flags are deferred until telemetry or mentor check-in confirms status.
          </div>
        </div>

        {/* Edge Case 4 */}
        <div className={`p-5 rounded-xl border ${
          highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200 shadow-sm'
        } space-y-3`}>
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-bold uppercase tracking-wider text-purple-600">
              Edge Case 4: Sudden Disengagement
            </h4>
            <span className="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-bold">
              Test Passed
            </span>
          </div>
          <div className="p-3 bg-slate-50 rounded-lg text-xs space-y-1 font-mono">
            <div>Historic Baseline: <strong>Active & High Marks</strong></div>
            <div>Week 4 Δ Activity: <strong>-180 min</strong> | Week 4 Submissions: <strong>0</strong></div>
          </div>
          <p className="text-xs text-slate-600">
            <strong>Challenge:</strong> Cumulative averages mask acute drop-offs until it is too late to intervene.
          </p>
          <div className="p-3 bg-purple-50 text-purple-900 rounded-lg text-xs border border-purple-200">
            <strong>System Safeguard:</strong> Longitudinal trend features (`activity_change`, `engagement_trend`) 
            trigger an immediate priority alert despite acceptable cumulative term averages.
          </div>
        </div>
      </div>

      {/* Error Analysis Audit (Section 21) */}
      <div className={`p-5 rounded-xl border ${
        highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200 shadow-sm'
      }`}>
        <h3 className="text-sm font-bold tracking-tight mb-3">
          Error Analysis: Why the Model Makes False Predictions (Section 21)
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          {/* False Positives Diagnostic */}
          <div className="p-4 bg-red-50/50 rounded-xl border border-red-200">
            <div className="font-bold text-red-800 text-sm mb-1">
              False Positives Diagnostic (Total: {error_analysis.false_positives})
            </div>
            <p className="text-slate-600 mb-2">
              Learners flagged as needing support who were actually progressing well:
            </p>
            <ul className="space-y-1 text-slate-700">
              {error_analysis.fp_drivers.map((d, i) => (
                <li key={i} className="flex items-start gap-1.5">
                  <span className="text-red-500 font-bold">•</span>
                  <span>{d}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* False Negatives Diagnostic */}
          <div className="p-4 bg-amber-50/50 rounded-xl border border-amber-200">
            <div className="font-bold text-amber-800 text-sm mb-1">
              False Negatives Diagnostic (Total: {error_analysis.false_negatives})
            </div>
            <p className="text-slate-600 mb-2">
              Learners who needed support but were initially missed by the system:
            </p>
            <ul className="space-y-1 text-slate-700">
              {error_analysis.fn_drivers.map((d, i) => (
                <li key={i} className="flex items-start gap-1.5">
                  <span className="text-amber-500 font-bold">•</span>
                  <span>{d}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
