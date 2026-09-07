import React from 'react';
import { Globe, Eye, ShieldCheck, HelpCircle } from 'lucide-react';
import { Language } from '../types';
import { translations } from '../i18n';

interface HeaderProps {
  language: Language;
  onLanguageChange: (lang: Language) => void;
  highContrast: boolean;
  onHighContrastToggle: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  language,
  onLanguageChange,
  highContrast,
  onHighContrastToggle,
}) => {
  const t = translations[language];

  return (
    <header
      id="app-header"
      className={`border-b ${
        highContrast
          ? 'bg-black text-white border-white'
          : 'bg-white text-slate-900 border-slate-200'
      } px-6 py-4 shadow-sm transition-colors`}
    >
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <span className="p-2 rounded-lg bg-blue-600 text-white font-bold text-lg flex items-center justify-center shadow">
              <ShieldCheck className="w-6 h-6" />
            </span>
            <div>
              <h1 className="text-xl md:text-2xl font-bold tracking-tight">
                {t.app_title}
              </h1>
              <p className={`text-xs md:text-sm font-medium ${highContrast ? 'text-slate-300' : 'text-slate-500'}`}>
                {t.app_subtitle}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 mt-2 text-xs">
            <span className="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-semibold border border-emerald-200 flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
              Non-Punitive Support Prioritisation
            </span>
            <span className="px-2 py-0.5 rounded-full bg-blue-100 text-blue-800 font-semibold border border-blue-200">
              5 Behavioral Signal Streams
            </span>
            <span className="px-2 py-0.5 rounded-full bg-purple-100 text-purple-800 font-semibold border border-purple-200">
              Uncertainty-Aware
            </span>
          </div>
        </div>

        <div className="flex items-center flex-wrap gap-2">
          {/* Language Switcher */}
          <div className="flex items-center rounded-lg border border-slate-300 p-0.5 bg-slate-50">
            <button
              id="lang-btn-en"
              onClick={() => onLanguageChange('en')}
              className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-all flex items-center gap-1.5 ${
                language === 'en'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-700 hover:text-black'
              }`}
              aria-label="Switch to English"
            >
              <Globe className="w-3.5 h-3.5" />
              English
            </button>
            <button
              id="lang-btn-ta"
              onClick={() => onLanguageChange('ta')}
              className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-all flex items-center gap-1.5 ${
                language === 'ta'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-700 hover:text-black'
              }`}
              aria-label="தமிழுக்கு மாறுக"
            >
              <Globe className="w-3.5 h-3.5" />
              தமிழ்
            </button>
          </div>

          {/* High Contrast Accessibility Toggle */}
          <button
            id="high-contrast-toggle"
            onClick={onHighContrastToggle}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg border flex items-center gap-1.5 transition-colors ${
              highContrast
                ? 'bg-yellow-400 text-black border-yellow-500 hover:bg-yellow-300'
                : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-100'
            }`}
            title="Toggle WCAG high contrast mode"
            aria-pressed={highContrast}
          >
            <Eye className="w-3.5 h-3.5" />
            {highContrast ? t.high_contrast_on : t.high_contrast_off}
          </button>
        </div>
      </div>
    </header>
  );
};
