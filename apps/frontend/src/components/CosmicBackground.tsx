import React, { useEffect, useRef } from 'react'

interface CosmicBackgroundProps {
  className?: string
  intensity?: 'low' | 'medium' | 'high'
}

const CosmicBackground: React.FC<CosmicBackgroundProps> = ({
  className = '',
  intensity = 'medium',
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    // Star count based on intensity
    const starCounts = { low: 50, medium: 100, high: 150 }
    const starCount = starCounts[intensity]

    // Generate stars
    const stars: Array<{ x: number; y: number; radius: number; opacity: number; opacityChange: number }> = []
    for (let i = 0; i < starCount; i++) {
      stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 1.5,
        opacity: Math.random() * 0.5 + 0.5,
        opacityChange: (Math.random() - 0.5) * 0.05,
      })
    }

    // Animation loop
    const animate = () => {
      // Clear canvas with dark background
      ctx.fillStyle = '#0f172a'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // Add gradient overlay
      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height)
      gradient.addColorStop(0, 'rgba(15, 23, 42, 0.8)')
      gradient.addColorStop(0.5, 'rgba(30, 41, 59, 0.4)')
      gradient.addColorStop(1, 'rgba(10, 14, 39, 0.8)')
      ctx.fillStyle = gradient
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // Draw stars
      stars.forEach((star) => {
        star.opacity += star.opacityChange
        if (star.opacity > 1) {
          star.opacity = 1
          star.opacityChange = -Math.abs(star.opacityChange)
        } else if (star.opacity < 0.2) {
          star.opacity = 0.2
          star.opacityChange = Math.abs(star.opacityChange)
        }

        ctx.fillStyle = `rgba(226, 232, 240, ${star.opacity})`
        ctx.beginPath()
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2)
        ctx.fill()
      })

      requestAnimationFrame(animate)
    }

    animate()

    return () => {
      window.removeEventListener('resize', resizeCanvas)
    }
  }, [intensity])

  return (
    <canvas
      ref={canvasRef}
      className={`fixed top-0 left-0 w-full h-full pointer-events-none ${className}`}
      style={{ zIndex: -1 }}
    />
  )
}

export default CosmicBackground
