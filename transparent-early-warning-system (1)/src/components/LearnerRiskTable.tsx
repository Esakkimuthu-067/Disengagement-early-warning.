import React, { useState, useMemo } from 'react';
import { 
  Search, 
  Filter, 
  Download, 
  ArrowUpDown, 
  ChevronRight, 
  AlertCircle, 
  CheckCircle2, 
  Clock, 
  HelpCircle 
} from 'lucide-react';
import { LearnerRecord, Language, SupportTier } from '../types';
import { translations } from '../i18n';

interface LearnerRiskTableProps {
  learners: LearnerRecord[];
  language: Language;
  highContrast: boolean;
  onSelectLearner: (learner: LearnerRecord) => void;
  initialTierFilter?: string;
}

export const LearnerRiskTable: React.FC<LearnerRiskTableProps> = ({
  learners,
  language,
  highContrast,
  onSelectLearner,
  initialTierFilter
}) => {
  const t = translations[language];

  // Filters state
  const [searchQuery, setSearchQuery] = useState('');
  const [tierFilter, setTierFilter] = useState<string>(initialTierFilter || 'ALL');
  const [courseFilter, setCourseFilter] = useState<string>('ALL');
  const [minConfidence, setMinConfidence] = useState<number>(0);
  const [onlyMissing, setOnlyMissing] = useState<boolean>(false);

  // Sorting state
  const [sortField, setSortField] = useState<keyof LearnerRecord>('support_probability');
  const [sortAsc, setSortAsc] = useState<boolean>(false);

  // Pagination
  const [page, setPage] = useState<number>(1);
  const pageSize = 15;

  const courses = useMemo(() => {
    return Array.from(new Set(learners.map(l => l.course_id))).sort();
  }, [learners]);

  const filteredLearners = useMemo(() => {
    return learners.filter(l => {
      if (searchQuery && !l.learner_id.toLowerCase().includes(searchQuery.toLowerCase())) {
        return false;
      }
      if (tierFilter !== 'ALL' && l.risk_level !== tierFilter) {
        return false;
      }
      if (courseFilter !== 'ALL' && l.course_id !== courseFilter) {
        return false;
      }
      if (l.confidence_percentage < minConfidence) {
        return false;
      }
      if (onlyMissing && l.missing_feature_count === 0) {
        return false;
      }
      return true;
    }).sort((a, b) => {
      const valA = a[sortField];
      const valB = b[sortField];
      if (typeof valA === 'number' && typeof valB === 'number') {
        return sortAsc ? valA - valB : valB - valA;
      }
      return sortAsc
        ? String(valA).localeCompare(String(valB))
        : String(valB).localeCompare(String(valA));
    });
  }, [learners, searchQuery, tierFilter, courseFilter, minConfidence, onlyMissing, sortField, sortAsc]);

  const totalPages = Math.ceil(filteredLearners.length / pageSize) || 1;
  const paginatedLearners = filteredLearners.slice((page - 1) * pageSize, page * pageSize);

  const handleSort = (field: keyof LearnerRecord) => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(false);
    }
  };

  const exportCSV = () => {
    const headers = [
      "Learner ID", "Course", "Support Tier", "Support Probability", 
      "Confidence (%)", "Missing Signals", "Overall Engagement Score",
      "Attendance Rate", "Active Minutes", "Average Score"
    ];
    const rows = filteredLearners.map(l => [
      l.learner_id,
      l.course_id,
      l.risk_level,
      l.support_probability.toFixed(3),
      l.confidence_percentage.toFixed(1),
      l.missing_feature_count,
      l.overall_engagement_score.toFixed(1),
      l.attendance_rate.toFixed(2),
      l.active_minutes.toFixed(1),
      l.average_score.toFixed(1)
    ]);
    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map(e => e.join(","))].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `learner_prioritisation_roster.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const renderTierBadge = (tier: SupportTier) => {
    switch (tier) {
      case 'High Support Need':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-800 border border-red-200">
            <span className="w-2 h-2 rounded-full bg-red-600"></span>
            High Support Need
          </span>
        );
      case 'Moderate Support Need':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-200">
            <span className="w-2 h-2 rounded-full bg-amber-500"></span>
            Moderate Support Need
          </span>
        );
      case 'Low Support Need':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            Low Support Need
          </span>
        );
      case 'Insufficient Data':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-800 border border-slate-300">
            <HelpCircle className="w-3 h-3 text-slate-500" />
            Insufficient Data
          </span>
        );
    }
  };

  return (
    <div className="space-y-4">
      {/* Search & Filter Toolbar */}
      <div className={`p-4 rounded-xl border ${
        highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200'
      } flex flex-col md:flex-row items-center justify-between gap-3`}>
        {/* Search */}
        <div className="relative w-full md:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            id="learner-search-input"
            type="text"
            placeholder={t.search_placeholder}
            value={searchQuery}
            onChange={(e) => { setSearchQuery(e.target.value); setPage(1); }}
            className={`w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              highContrast ? 'bg-slate-900 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'
            }`}
          />
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          {/* Tier Filter */}
          <select
            id="tier-filter-select"
            value={tierFilter}
            onChange={(e) => { setTierFilter(e.target.value); setPage(1); }}
            className={`text-xs rounded-lg border px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              highContrast ? 'bg-slate-900 border-slate-700 text-white' : 'bg-white border-slate-200 text-slate-700'
            }`}
          >
            <option value="ALL">{t.all_tiers}</option>
            <option value="High Support Need">{t.high_support}</option>
            <option value="Moderate Support Need">{t.moderate_support}</option>
            <option value="Low Support Need">{t.low_support}</option>
            <option value="Insufficient Data">{t.insufficient_data}</option>
          </select>

          {/* Course Filter */}
          <select
            id="course-filter-select"
            value={courseFilter}
            onChange={(e) => { setCourseFilter(e.target.value); setPage(1); }}
            className={`text-xs rounded-lg border px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              highContrast ? 'bg-slate-900 border-slate-700 text-white' : 'bg-white border-slate-200 text-slate-700'
            }`}
          >
            <option value="ALL">{t.all_courses}</option>
            {courses.map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>

          {/* Missing Data Toggle */}
          <label className="flex items-center gap-1.5 text-xs cursor-pointer select-none text-slate-600 px-2 py-1 bg-slate-100 rounded-lg">
            <input
              type="checkbox"
              checked={onlyMissing}
              onChange={(e) => { setOnlyMissing(e.target.checked); setPage(1); }}
              className="rounded text-blue-600"
            />
            Missing Signals
          </label>

          {/* Export CSV */}
          <button
            id="export-csv-btn"
            onClick={exportCSV}
            className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-lg transition-colors ml-auto"
          >
            <Download className="w-3.5 h-3.5" />
            {t.export_csv}
          </button>
        </div>
      </div>

      {/* Roster Table */}
      <div className={`rounded-xl border overflow-hidden ${
        highContrast ? 'bg-black border-slate-700' : 'bg-white border-slate-200 shadow-sm'
      }`}>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className={`border-b ${
              highContrast ? 'bg-slate-900 border-slate-800 text-slate-300' : 'bg-slate-50 border-slate-200 text-slate-600 font-semibold'
            }`}>
              <tr>
                <th className="py-3 px-4 cursor-pointer hover:text-blue-600" onClick={() => handleSort('learner_id')}>
                  <div className="flex items-center gap-1">
                    Learner ID
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
                <th className="py-3 px-4 cursor-pointer hover:text-blue-600" onClick={() => handleSort('course_id')}>
                  <div className="flex items-center gap-1">
                    Course
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
                <th className="py-3 px-4 cursor-pointer hover:text-blue-600" onClick={() => handleSort('risk_level')}>
                  <div className="flex items-center gap-1">
                    Support Tier
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
                <th className="py-3 px-4 cursor-pointer hover:text-blue-600" onClick={() => handleSort('support_probability')}>
                  <div className="flex items-center gap-1">
                    Support Probability
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
                <th className="py-3 px-4 cursor-pointer hover:text-blue-600" onClick={() => handleSort('confidence_percentage')}>
                  <div className="flex items-center gap-1">
                    Confidence
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
                <th className="py-3 px-4 cursor-pointer hover:text-blue-600" onClick={() => handleSort('overall_engagement_score')}>
                  <div className="flex items-center gap-1">
                    Engagement (0-100)
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
                <th className="py-3 px-4 cursor-pointer hover:text-blue-600" onClick={() => handleSort('missing_feature_count')}>
                  <div className="flex items-center gap-1">
                    Missing Signals
                    <ArrowUpDown className="w-3 h-3" />
                  </div>
                </th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {paginatedLearners.length > 0 ? (
                paginatedLearners.map(learner => (
                  <tr 
                    key={learner.learner_id}
                    onClick={() => onSelectLearner(learner)}
                    className={`hover:bg-blue-50/40 transition-colors cursor-pointer ${
                      highContrast ? 'hover:bg-slate-900 text-white' : 'text-slate-800'
                    }`}
                  >
                    <td className="py-3 px-4 font-mono font-semibold text-blue-600">
                      {learner.learner_id}
                    </td>
                    <td className="py-3 px-4 font-medium text-slate-500">
                      {learner.course_id}
                    </td>
                    <td className="py-3 px-4">
                      {renderTierBadge(learner.risk_level)}
                    </td>
                    <td className="py-3 px-4 font-mono">
                      <div className="flex items-center gap-2">
                        <div className="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                          <div 
                            className={`h-full rounded-full ${
                              learner.support_probability > 0.65 ? 'bg-red-500' : learner.support_probability > 0.4 ? 'bg-amber-400' : 'bg-emerald-500'
                            }`}
                            style={{ width: `${learner.support_probability * 100}%` }}
                          />
                        </div>
                        {(learner.support_probability * 100).toFixed(1)}%
                      </div>
                    </td>
                    <td className="py-3 px-4 font-mono">
                      <span className={`px-2 py-0.5 rounded text-[11px] font-semibold ${
                        learner.confidence_percentage >= 75 ? 'bg-slate-100 text-slate-700' : 'bg-amber-50 text-amber-800'
                      }`}>
                        {learner.confidence_percentage.toFixed(0)}%
                      </span>
                    </td>
                    <td className="py-3 px-4 font-semibold">
                      {learner.overall_engagement_score.toFixed(1)}
                    </td>
                    <td className="py-3 px-4">
                      {learner.missing_feature_count > 0 ? (
                        <span className="px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-medium text-[11px]">
                          {learner.missing_feature_count} signal{learner.missing_feature_count > 1 ? 's' : ''} missing
                        </span>
                      ) : (
                        <span className="text-slate-400 text-[11px]">Complete</span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={(e) => { e.stopPropagation(); onSelectLearner(learner); }}
                        className="p-1 text-blue-600 hover:bg-blue-100 rounded transition-colors inline-flex items-center gap-1 font-semibold"
                        aria-label={`View deep dive for ${learner.learner_id}`}
                      >
                        Deep Dive
                        <ChevronRight className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={8} className="py-8 text-center text-slate-500">
                    {t.no_results}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Bar */}
        <div className={`py-3 px-4 border-t flex items-center justify-between text-xs ${
          highContrast ? 'bg-slate-900 border-slate-800 text-slate-400' : 'bg-slate-50 border-slate-200 text-slate-500'
        }`}>
          <div>
            Showing {(page - 1) * pageSize + 1} to {Math.min(page * pageSize, filteredLearners.length)} of {filteredLearners.length} learners
          </div>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-2.5 py-1 rounded border bg-white disabled:opacity-40 hover:bg-slate-50 transition-colors"
            >
              Previous
            </button>
            <span className="px-2">Page {page} of {totalPages}</span>
            <button
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="px-2.5 py-1 rounded border bg-white disabled:opacity-40 hover:bg-slate-50 transition-colors"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
