import React from 'react';

interface RingDiagramProps {
  className?: string;
}

export const RingDiagram: React.FC<RingDiagramProps> = ({ className = '' }) => {
  const rings = [
    { label: 'CORE', radius: 40, color: '#4a6a5a' },
    { label: 'RELATIONAL', radius: 80, color: '#4b7c8c' },
    { label: 'TRACKING', radius: 120, color: '#4b7c8c' },
    { label: 'OUTPUTS', radius: 160, color: '#b8863a' },
    { label: 'RESILIENCE', radius: 200, color: '#8a8580' },
  ];

  return (
    <div className={`relative flex flex-col items-center justify-center ${className}`}>
      <div className="relative w-[380px] h-[380px] flex items-center justify-center">
        <svg 
          id="ring-diagram-svg"
          viewBox="0 0 440 440" 
          className="w-full h-full"
        >
          {/* Background Rings */}
          {rings.map((ring, i) => (
            <g key={ring.label}>
              <circle
                cx="220"
                cy="220"
                r={ring.radius}
                fill="none"
                stroke={ring.color}
                strokeWidth="1"
                strokeDasharray="4 4"
                className="opacity-20"
              />
              {/* Outermost ring breathing animation */}
              <circle
                cx="220"
                cy="220"
                r={ring.radius}
                fill="none"
                stroke={ring.color}
                strokeWidth={i === rings.length - 1 ? "2" : "1.5"}
                strokeDasharray={i === rings.length - 1 ? "none" : "8 4"}
                className={`opacity-40 ${i === rings.length - 1 ? 'animate-breathe origin-center' : ''}`}
              />
              {/* Ring Label */}
              <text
                x="220"
                y={220 - ring.radius - 6}
                textAnchor="middle"
                className="font-mono text-[10px] font-semibold fill-ink-muted uppercase tracking-[0.1em]"
              >
                {ring.label}
              </text>
            </g>
          ))}

          {/* Center Node */}
          <g>
            <circle
              cx="220"
              cy="220"
              r="30"
              className="fill-forest-sage"
            />
            <text
              x="220"
              y="225"
              textAnchor="middle"
              className="font-display font-bold text-[18px] fill-white"
            >
              Events
            </text>
          </g>
        </svg>
      </div>
    </div>
  );
};
