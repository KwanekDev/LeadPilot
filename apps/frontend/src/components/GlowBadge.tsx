import React, { ReactNode } from 'react'

interface GlowBadgeProps {
  children: ReactNode
  variant?: 'blue' | 'purple' | 'cyan' | 'green' | 'red' | 'yellow'
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

const GlowBadge: React.FC<GlowBadgeProps> = ({
  children,
  variant = 'blue',
  size = 'md',
  className = '',
}) => {
  const variantClasses = {
    blue: 'bg-blue-500/20 text-blue-200 glow-blue',
    purple: 'bg-purple-500/20 text-purple-200 glow-purple',
    cyan: 'bg-cyan-500/20 text-cyan-200 glow-cyan',
    green: 'bg-green-500/20 text-green-200',
    red: 'bg-red-500/20 text-red-200',
    yellow: 'bg-yellow-500/20 text-yellow-200',
  }

  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1.5 text-sm',
    lg: 'px-4 py-2 text-base',
  }

  return (
    <div
      className={`
        inline-block
        rounded-full
        font-semibold
        border border-opacity-30
        ${variantClasses[variant]}
        ${sizeClasses[size]}
        ${className}
      `}
    >
      {children}
    </div>
  )
}

export default GlowBadge
