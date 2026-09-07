import React from 'react';
import { HelpCircle, AlertTriangle, ShieldCheck, CheckCircle2, Info } from 'lucide-react';
import { PipelineResults, Language } from '../types';
import { translations } from '../i18n';

interface MissingDataUncertaintyProps {
  data: PipelineResults;
  language: Language;
  highContrast: boolean;
}

export const MissingDataUncertainty: React.FC<MissingDataUncertaintyProps> = ({
  data,
  language,
  highContrast
}) => {
  const t = translations[language];
  const { missing_data_summary, missing_data_performance } = data;

  return (
    <div className="space-y-6">
      {/* Principle Banner */}
      <div className={`p-4 rounded-xl border ${
        highContrast ? 'bg-slate-900 border-white text-white' : 'bg-slate-50 border-slate-200 text-slate-800'
      }`}>
        <div className="flex items-start gap-3">
          <Info className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
          <div className="text-xs md:text-sm leading-relaxed">
            <span className="font-bold">Transparent Uncertainty & Missing Data Policy: </span>
            <span>
              Real-world educational datasets have substantial missing values (e.g. optional sentiment surveys, 
              offline studying). Traditional algorithms force overconfident predictions on partial data. 
              Our architecture penalizes confidence proportional to missingness and explicitly categorizes 
              learners with ≥ 3 missing signals as <strong>"Insufficient Data"</strong> to prevent false accusations.
            </span>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className={`p-4 rounded-xl border ${
          highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200 shadow-sm'
        }`}>
          <div className="text-slate-500 text-xs font-semibold mb-1">Records with Partial Missingness</div>
          <div className="text-2xl font-bold text-slate-800">
            {missing_data_summary.records_with_any_missing.toLocaleString()}
          </div>
          <div className="text-xs text-slate-400 mt-1">
            {missing_data_summary.missing_rate_overall.toFixed(1)}% of all historical telemetry
          </div>
        </div>

        <div className={`p-4 rounded-xl border ${
          highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200 shadow-sm'
        }`}>
          <div className="text-slate-500 text-xs font-semibold mb-1">Insufficient Data Defenses Triggered</div>
          <div className="text-2xl font-bold text-amber-600">
            {missing_data_summary.insufficient_data_count.toLocaleString()}
          </div>
          <div className="text-xs text-amber-700 mt-1">
            {missing_data_summary.insufficient_data_rate.toFixed(1)}% automated flags deferred
          </div>
        </div>

        <div className={`p-4 rounded-xl border ${
          highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200 shadow-sm'
        }`}>
          <div className="text-slate-500 text-xs font-semibold mb-1">Cohort Performance Parity</div>
          <div className="text-2xl font-bold text-emerald-600">
            F1: {missing_data_performance.complete_cohort.metrics.f1.toFixed(3)} vs {missing_data_performance.missing_cohort.metrics.f1.toFixed(3)}
          </div>
          <div className="text-xs text-slate-400 mt-1">
            Robust imputation preserves discriminative ability
          </div>
        </div>
      </div>

      {/* Missingness by Feature Breakdown */}
      <div className={`p-5 rounded-xl border ${
        highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200 shadow-sm'
      }`}>
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-4">
          Telemetry Signal Missingness Rates
        </h4>

        <div className="space-y-3 text-xs">
          {Object.entries(missing_data_summary.feature_missing_percentages).map(([signal, rawPct]) => {
            const pct = Number(rawPct);
            return (
              <div key={signal}>
                <div className="flex justify-between text-slate-700 mb-1">
                  <span className="font-medium font-mono text-[11px] capitalize">{signal.replace('_', ' ')}</span>
                  <span className="font-bold text-slate-900">{pct.toFixed(1)}% missing</span>
                </div>
                <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div 
                    className={`h-full rounded-full ${pct > 15 ? 'bg-amber-500' : pct > 8 ? 'bg-blue-500' : 'bg-emerald-500'}`}
                    style={{ width: `${Math.min(100, pct * 3.5)}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Uncertainty Decision Rules */}
      <div className={`p-5 rounded-xl border ${
        highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200 shadow-sm'
      }`}>
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
          Uncertainty Calibration Framework
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
          <div className="p-3 bg-emerald-50 rounded-lg border border-emerald-200">
            <div className="font-bold text-emerald-800 mb-1">High Confidence (≥ 75%)</div>
            <p className="text-slate-600 text-[11px]">
              Complete or near-complete telemetry. Behavioral signals point coherently toward need or thriving status.
            </p>
          </div>
          <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
            <div className="font-bold text-blue-800 mb-1">Medium Confidence (55%–74%)</div>
            <p className="text-slate-600 text-[11px]">
              Mild signal conflicts (e.g. high test scores but low study minutes). Model alerts mentors to verify context.
            </p>
          </div>
          <div className="p-3 bg-amber-50 rounded-lg border border-amber-200">
            <div className="font-bold text-amber-800 mb-1">Low Confidence (&lt; 55%)</div>
            <p className="text-slate-600 text-[11px]">
              Probabilities near decision threshold (0.50). High model variance across trees indicates ambiguity.
            </p>
          </div>
          <div className="p-3 bg-slate-100 rounded-lg border border-slate-300">
            <div className="font-bold text-slate-800 mb-1">Insufficient Evidence</div>
            <p className="text-slate-600 text-[11px]">
              ≥ 3 critical behavioral channels absent. Automated prediction is deferred into "Insufficient Data" status.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
