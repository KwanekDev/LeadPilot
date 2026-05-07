import React from 'react'
import { useTranslation } from 'i18next-react'

const LanguageSwitcher: React.FC = () => {
  const { i18n } = useTranslation()

  const toggleLanguage = () => {
    const newLanguage = i18n.language === 'pl' ? 'en' : 'pl'
    i18n.changeLanguage(newLanguage)
  }

  return (
    <button
      onClick={toggleLanguage}
      className="px-3 py-1.5 text-sm font-medium rounded-lg glass-panel hover:bg-slate-700/30 transition text-light-secondary hover:text-light-primary"
      title={`Switch to ${i18n.language === 'pl' ? 'English' : 'Polski'}`}
    >
      {i18n.language === 'pl' ? '🇬🇧 English' : '🇵🇱 Polski'}
    </button>
  )
}

export default LanguageSwitcher
