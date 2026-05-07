import React, { ReactNode } from 'react'

interface AnimatedButtonProps {
  children: ReactNode
  onClick?: () => void
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  type?: 'button' | 'submit' | 'reset'
  className?: string
}

const AnimatedButton: React.FC<AnimatedButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  type = 'button',
  className = '',
}) => {
  const variantClasses = {
    primary: 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white glow-blue hover:shadow-lg hover:glow-blue',
    secondary: 'bg-slate-700/50 text-slate-200 border border-slate-600 hover:bg-slate-700/70',
    ghost: 'bg-transparent text-slate-300 border border-slate-600 hover:bg-slate-700/30',
    danger: 'bg-gradient-to-r from-red-500 to-pink-500 text-white hover:shadow-lg',
  }

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={`
        inline-flex items-center justify-center
        rounded-lg
        font-semibold
        transition-all
        duration-300
        ease-out
        disabled:opacity-50 disabled:cursor-not-allowed
        active:scale-95
        hover:scale-105
        ${variantClasses[variant]}
        ${sizeClasses[size]}
        ${className}
      `}
    >
      {loading ? (
        <>
          <span className="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
          Loading...
        </>
      ) : (
        children
      )}
    </button>
  )
}

export default AnimatedButton
