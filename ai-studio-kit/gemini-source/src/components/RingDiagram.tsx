import React, { useRef, useEffect } from 'react';

interface RingDiagramProps {
  className?: string;
}

export const RingDiagram: React.FC<RingDiagramProps> = ({ className }) => {
  const svgRef = useRef<SVGSVGElement>(null);

  const ringColors = [
    '#c8d9ce', // Center (Events)
    '#dce8e0', // Core
    '#e8e3dd', // Relational
    '#f0ede8', // Outputs
    '#f5f3f0', // Resilience
  ];

  const ringRadii = [40, 80, 120, 160, 200];

  return (
    <div className={`relative flex flex-col items-center ${className}`}>
      <div className="relative w-[380px] h-[380px]">
        <svg
          viewBox="0 0 400 400"
          className="w-full h-full"
          id="ring-diagram-svg"
        >
          {/* Rings from outside in */}
          {[4, 3, 2, 1, 0].map((i) => (
            <circle
              key={i}
              cx="200"
              cy="200"
              r={ringRadii[i]}
              fill={ringColors[i]}
              stroke="#1a3a32"
              strokeWidth="0.5"
              strokeOpacity="0.1"
              className={i === 4 ? "animate-breathe origin-center" : ""}
            />
          ))}
          
          {/* Center Text */}
          <text
            x="200"
            y="205"
            textAnchor="middle"
            className="font-sans font-bold text-[14px] fill-[#1a2e22]"
          >
            Events
          </text>

          {/* Band Labels - Top centered, decreasing opacity */}
          <g className="font-mono text-[9px] uppercase tracking-[0.2em] font-bold">
            <text x="200" y="155" textAnchor="middle" fill="#1a2e22" fillOpacity="0.6">Core</text>
            <text x="200" y="115" textAnchor="middle" fill="#1a2e22" fillOpacity="0.5">Relational</text>
            <text x="200" y="75" textAnchor="middle" fill="#1a2e22" fillOpacity="0.4">Outputs</text>
            <text x="200" y="35" textAnchor="middle" fill="#1a2e22" fillOpacity="0.35">Resilience</text>
          </g>
        </svg>
      </div>

      <div className="mt-6 text-center">
        <h3 className="font-display italic text-xl text-[#1a2e22]">Everything connects through Events</h3>
      </div>

      <div className="mt-8 flex gap-6">
        {[
          { label: 'Core', color: '#dce8e0' },
          { label: 'Relational', color: '#e8e3dd' },
          { label: 'Outputs', color: '#f0ede8' },
          { label: 'Resilience', color: '#f5f3f0' },
        ].map((item) => (
          <div key={item.label} className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color, border: '1px solid #c8d9ce' }} />
            <span className="font-mono text-[10px] uppercase tracking-wider text-[#2c2825]/60">{item.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
