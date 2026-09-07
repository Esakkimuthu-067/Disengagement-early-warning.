import React, { useState } from 'react';
import pipelineData from './pipeline_results.json';
import { PipelineResults, Language, LearnerRecord } from './types';
import { translations } from './i18n';
import { Header } from './components/Header';
import { DashboardOverview } from './components/DashboardOverview';
import { LearnerRiskTable } from './components/LearnerRiskTable';
import { LearnerDetailModal } from './components/LearnerDetailModal';
import { ModelPerformance } from './components/ModelPerformance';
import { BacktestSimulator } from './components/BacktestSimulator';
import { MissingDataUncertainty } from './components/MissingDataUncertainty';
import { EdgeCasesView } from './components/EdgeCasesView';
import { 
  LayoutDashboard, 
  Users, 
  LineChart, 
  History, 
  ShieldAlert, 
  AlertOctagon,
  Terminal,
  ExternalLink
} from 'lucide-react';

const data = pipelineData as unknown as PipelineResults;

export default function App() {
  const [language, setLanguage] = useState<Language>('en');
  const [highContrast, setHighContrast] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<
    'dashboard' | 'learners' | 'performance' | 'backtest' | 'missing' | 'failures'
  >('dashboard');
  const [selectedLearner, setSelectedLearner] = useState<LearnerRecord | null>(null);
  const [initialTierFilter, setInitialTierFilter] = useState<string>('ALL');

  const t = translations[language];

  const handleNavigateToLearners = (tierFilter?: string) => {
    if (tierFilter) {
      setInitialTierFilter(tierFilter);
    }
    setActiveTab('learners');
  };

  return (
    <div className={`min-h-screen transition-colors ${
      highContrast ? 'bg-black text-white' : 'bg-slate-50 text-slate-900'
    }`}>
      {/* Header */}
      <Header
        language={language}
        onLanguageChange={setLanguage}
        highContrast={highContrast}
        onHighContrastToggle={() => setHighContrast(!highContrast)}
      />

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        {/* Navigation Tabs Bar */}
        <div className={`flex items-center gap-1 border-b overflow-x-auto pb-1 scrollbar-none ${
          highContrast ? 'border-slate-800' : 'border-slate-200'
        }`}>
          <button
            id="nav-tab-dashboard"
            onClick={() => setActiveTab('dashboard')}
            className={`flex items-center gap-2 px-4 py-2 text-xs md:text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
              activeTab === 'dashboard'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            <LayoutDashboard className="w-4 h-4" />
            {t.tab_dashboard}
          </button>

          <button
            id="nav-tab-learners"
            onClick={() => setActiveTab('learners')}
            className={`flex items-center gap-2 px-4 py-2 text-xs md:text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
              activeTab === 'learners'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            <Users className="w-4 h-4" />
            {t.tab_learners}
          </button>

          <button
            id="nav-tab-performance"
            onClick={() => setActiveTab('performance')}
            className={`flex items-center gap-2 px-4 py-2 text-xs md:text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
              activeTab === 'performance'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            <LineChart className="w-4 h-4" />
            {t.tab_performance}
          </button>

          <button
            id="nav-tab-backtest"
            onClick={() => setActiveTab('backtest')}
            className={`flex items-center gap-2 px-4 py-2 text-xs md:text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
              activeTab === 'backtest'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            <History className="w-4 h-4" />
            {t.tab_backtest}
          </button>

          <button
            id="nav-tab-missing"
            onClick={() => setActiveTab('missing')}
            className={`flex items-center gap-2 px-4 py-2 text-xs md:text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
              activeTab === 'missing'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            <ShieldAlert className="w-4 h-4" />
            {t.tab_missing}
          </button>

          <button
            id="nav-tab-failures"
            onClick={() => setActiveTab('failures')}
            className={`flex items-center gap-2 px-4 py-2 text-xs md:text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
              activeTab === 'failures'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            <AlertOctagon className="w-4 h-4" />
            {t.tab_failures}
          </button>
        </div>

        {/* Tab Content Views */}
        {activeTab === 'dashboard' && (
          <DashboardOverview
            data={data}
            language={language}
            highContrast={highContrast}
            onNavigateToLearners={handleNavigateToLearners}
          />
        )}

        {activeTab === 'learners' && (
          <LearnerRiskTable
            learners={data.week_5_active_learners}
            language={language}
            highContrast={highContrast}
            onSelectLearner={setSelectedLearner}
            initialTierFilter={initialTierFilter}
          />
        )}

        {activeTab === 'performance' && (
          <ModelPerformance
            data={data}
            language={language}
            highContrast={highContrast}
          />
        )}

        {activeTab === 'backtest' && (
          <BacktestSimulator
            data={data}
            language={language}
            highContrast={highContrast}
          />
        )}

        {activeTab === 'missing' && (
          <MissingDataUncertainty
            data={data}
            language={language}
            highContrast={highContrast}
          />
        )}

        {activeTab === 'failures' && (
          <EdgeCasesView
            data={data}
            language={language}
            highContrast={highContrast}
          />
        )}

        {/* Streamlit CLI Run Instructions Drawer */}
        <div className={`p-4 rounded-xl border flex flex-col md:flex-row items-center justify-between gap-3 text-xs ${
          highContrast ? 'bg-slate-900 border-slate-700 text-slate-300' : 'bg-slate-100 border-slate-200 text-slate-600'
        }`}>
          <div className="flex items-center gap-2 font-mono">
            <Terminal className="w-4 h-4 text-blue-600" />
            <span>Streamlit Dashboard Also Available: <code>streamlit run app.py</code></span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-slate-500">Includes Python ML Pipeline, Pytest Suite & Bilingual Support</span>
          </div>
        </div>
      </main>

      {/* Selected Learner Deep Dive Modal */}
      {selectedLearner && (
        <LearnerDetailModal
          learner={selectedLearner}
          language={language}
          highContrast={highContrast}
          onClose={() => setSelectedLearner(null)}
        />
      )}
    </div>
  );
}
