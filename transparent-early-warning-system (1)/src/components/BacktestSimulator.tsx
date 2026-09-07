import React from 'react';
import { Clock, TrendingUp, AlertCircle, ShieldCheck, CheckCircle2 } from 'lucide-react';
import { PipelineResults, Language } from '../types';
import { translations } from '../i18n';

interface BacktestSimulatorProps {
  data: PipelineResults;
  language: Language;
  highContrast: boolean;
}

export const BacktestSimulator: React.FC<BacktestSimulatorProps> = ({
  data,
  language,
  highContrast
}) => {
  const t = translations[language];
  const { weekly_progression, earlier_identification_insight } = data.backtest_results;

  return (
    <div className="space-y-6">
      {/* Insight Highlight Banner */}
      <div className={`p-4 rounded-xl border ${
        highContrast ? 'bg-slate-900 border-white text-white' : 'bg-blue-50 border-blue-200 text-blue-900'
      }`}>
        <div className="flex items-start gap-3">
          <Clock className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
          <div className="text-xs md:text-sm">
            <span className="font-bold">Proactive Intervention Advantage: </span>
            <span>{earlier_identification_insight}</span>
          </div>
        </div>
      </div>

      {/* Week-by-Week Progression Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
        {weekly_progression.map(wk => (
          <div 
            key={wk.week}
            className={`p-4 rounded-xl border ${
              highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200 shadow-sm'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Week {wk.week}
              </span>
              <span className="text-[11px] px-2 py-0.5 rounded-full bg-blue-100 text-blue-800 font-semibold">
                +{((wk.recall_improvement) * 100).toFixed(0)}% Recall
              </span>
            </div>

            <div className="space-y-2 text-xs">
              <div className="p-2 rounded bg-slate-50 border border-slate-100">
                <div className="text-slate-400 text-[10px]">Baseline F1-Score</div>
                <div className="text-sm font-bold text-slate-600 font-mono">
                  {wk.baseline.f1.toFixed(3)}
                </div>
                <div className="text-[10px] text-slate-400">
                  FP: {wk.baseline.false_positives} | FN: {wk.baseline.false_negatives}
                </div>
              </div>

              <div className="p-2 rounded bg-blue-50 border border-blue-100">
                <div className="text-blue-600 text-[10px] font-semibold">Improved ML F1</div>
                <div className="text-sm font-bold text-blue-700 font-mono">
                  {wk.improved_model.f1.toFixed(3)}
                </div>
                <div className="text-[10px] text-blue-600 font-medium">
                  FP: {wk.improved_model.false_positives} | FN: {wk.improved_model.false_negatives}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Detailed Chronological Progression Table */}
      <div className={`p-5 rounded-xl border ${
        highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200 shadow-sm'
      }`}>
        <h3 className="text-sm font-bold tracking-tight mb-3">
          Chronological Back-Testing Performance Audit
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="border-b border-slate-200 bg-slate-50 font-semibold text-slate-600">
              <tr>
                <th className="py-2.5 px-4">Course Week</th>
                <th className="py-2.5 px-4">Learner Telemetry</th>
                <th className="py-2.5 px-4">Baseline Accuracy</th>
                <th className="py-2.5 px-4">Baseline F1</th>
                <th className="py-2.5 px-4 text-blue-600 font-bold">Improved Accuracy</th>
                <th className="py-2.5 px-4 text-blue-600 font-bold">Improved F1</th>
                <th className="py-2.5 px-4 text-emerald-600 font-bold">Early Recall Gain</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {weekly_progression.map(wk => (
                <tr key={wk.week} className="hover:bg-slate-50/60">
                  <td className="py-3 px-4 font-bold text-slate-900">Week {wk.week}</td>
                  <td className="py-3 px-4 font-mono text-slate-500">{wk.learner_count} learners</td>
                  <td className="py-3 px-4 font-mono text-slate-500">{wk.baseline.accuracy.toFixed(3)}</td>
                  <td className="py-3 px-4 font-mono text-slate-500">{wk.baseline.f1.toFixed(3)}</td>
                  <td className="py-3 px-4 font-mono font-bold text-blue-600">{wk.improved_model.accuracy.toFixed(3)}</td>
                  <td className="py-3 px-4 font-mono font-bold text-blue-600">{wk.improved_model.f1.toFixed(3)}</td>
                  <td className="py-3 px-4 font-mono font-bold text-emerald-600">
                    +{(wk.recall_improvement * 100).toFixed(1)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
