import React, { ReactNode } from 'react'

interface GlassCardProps {
  children: ReactNode
  className?: string
  glow?: 'blue' | 'purple' | 'cyan' | 'none'
  hover?: boolean
  onClick?: () => void
}

const GlassCard: React.FC<GlassCardProps> = ({
  children,
  className = '',
  glow = 'none',
  hover = false,
  onClick,
}) => {
  const glowClasses = {
    blue: 'glow-blue',
    purple: 'glow-purple',
    cyan: 'glow-cyan',
    none: '',
  }

  return (
    <div
      onClick={onClick}
      className={`
        glass-panel
        ${glowClasses[glow]}
        ${hover ? 'smooth-transition cursor-pointer hover:shadow-lg hover:scale-105' : ''}
        ${className}
      `}
    >
      {children}
    </div>
  )
}

export default GlassCard
