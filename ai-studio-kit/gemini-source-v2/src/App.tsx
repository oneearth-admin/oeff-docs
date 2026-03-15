import React, { useState, useEffect, useRef } from 'react';
import { RingDiagram } from './components/RingDiagram';
import { DataFlowView } from './components/DataFlowView';
import { EvolutionView } from './components/EvolutionView';
import { Entity, OEFF_DATA, PLATFORMS_DATA, TIMELINE_DATA, ROLES_DATA, DECISIONS_DATA } from './data';
import { motion, AnimatePresence } from 'motion/react';
import { X, ExternalLink, Shield, AlertTriangle, CheckCircle, Info, Quote } from 'lucide-react';

type Tab = 'DIAGRAM' | 'PLATFORMS' | 'TIMELINE' | 'ROLES' | 'RISK' | 'DECISIONS' | 'FLOW' | 'EVOLUTION';

export default function App() {
  const [activeTab, setActiveTab] = useState<Tab>('DIAGRAM');
  const [selectedEntity, setSelectedEntity] = useState<Entity | null>(null);
  const [hoveredEntity, setHoveredEntity] = useState<Entity | null>(null);
  const [hoveredCardRect, setHoveredCardRect] = useState<DOMRect | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const tabs: Tab[] = ['DIAGRAM', 'PLATFORMS', 'TIMELINE', 'ROLES', 'RISK', 'DECISIONS', 'FLOW', 'EVOLUTION'];
      if (e.key >= '1' && e.key <= '8') {
        setActiveTab(tabs[parseInt(e.key) - 1]);
      }
      if (e.key === 'Escape') {
        setSelectedEntity(null);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const renderBezierLine = () => {
    if (!hoveredEntity || !hoveredCardRect || activeTab !== 'DIAGRAM') return null;

    const ringRadii = [40, 80, 120, 160, 200];
    const targetRadius = ringRadii[hoveredEntity.ring] || 200;
    
    const svgElement = document.getElementById('ring-diagram-svg');
    if (!svgElement) return null;
    
    const svgRect = svgElement.getBoundingClientRect();
    const centerX = svgRect.left + svgRect.width / 2;
    const centerY = svgRect.top + svgRect.height / 2;
    
    // Target point on the ring (top of the arc)
    const tx = centerX;
    const ty = centerY - (targetRadius * (svgRect.width / 400)); 

    // Start point (center of the card)
    const sx = hoveredCardRect.left + hoveredCardRect.width / 2;
    const sy = hoveredCardRect.top + hoveredCardRect.height / 2;

    return (
      <svg className="fixed inset-0 pointer-events-none z-40 w-full h-full">
        <motion.path
          initial={{ pathLength: 0, opacity: 0 }}
          animate={{ pathLength: 1, opacity: 0.35 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
          d={`M ${sx} ${sy} Q ${(sx + tx) / 2} ${Math.min(sy, ty) - 100} ${tx} ${ty}`}
          stroke="#c8d9ce"
          strokeWidth="1.5"
          fill="none"
        />
      </svg>
    );
  };

  return (
    <div 
      ref={containerRef}
      className="min-h-screen bg-cream text-warm-ink font-sans selection:bg-sage/20 relative"
    >
      <div className="paper-grain" style={{ filter: 'url(#noiseFilter)' }} />
      
      <svg className="hidden">
        <filter id="noiseFilter">
          <feTurbulence 
            type="fractalNoise" 
            baseFrequency="0.5" 
            numOctaves="3" 
            stitchTiles="stitch" 
          />
        </filter>
      </svg>

      {/* Header */}
      <header className="pt-16 pb-8 text-center border-b border-forest-mist max-w-4xl mx-auto px-4">
        <h1 className="text-[36px] font-display font-bold text-ink leading-tight tracking-tight" style={{ fontOpticalSizing: 'auto' }}>
          OEFF Architecture
        </h1>
        <p className="font-mono text-[11px] font-semibold uppercase tracking-[0.3em] text-ink-muted mt-2">
          One Earth Film Festival
        </p>
      </header>

      {/* Tab Navigation */}
      <nav className="sticky-nav flex justify-center gap-6 py-4 mb-12">
        {(['DIAGRAM', 'PLATFORMS', 'TIMELINE', 'ROLES', 'RISK', 'DECISIONS', 'FLOW', 'EVOLUTION'] as Tab[]).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`font-mono text-[12px] font-semibold uppercase tracking-[0.15em] py-2 transition-all duration-200 border-b-2 cursor-pointer ${
              activeTab === tab 
                ? 'text-forest-sage border-forest-sage' 
                : 'text-ink-muted border-transparent hover:text-ink-soft'
            }`}
          >
            {tab}
          </button>
        ))}
      </nav>

      <main className="max-w-6xl mx-auto px-6 pb-24">
        <AnimatePresence mode="wait">
          {activeTab === 'DIAGRAM' && (
            <motion.div
              key="diagram"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="flex flex-col items-center"
            >
              <div className="text-center mb-12">
                <h3 className="font-serif italic text-[20px] text-forest-sage">Everything connects through Events</h3>
              </div>
              
              <RingDiagram className="mb-16" />

              {/* Layered Card List */}
              <div className="w-full space-y-12">
                {(['Core', 'Relational', 'Outputs', 'Resilience'] as const).map((type) => {
                  const entities = OEFF_DATA.filter(e => e.type === type);
                  const bgColors: Record<string, string> = {
                    Core: 'var(--color-layer-core)',
                    Relational: 'var(--color-layer-relational)',
                    Outputs: 'var(--color-layer-outputs)',
                    Resilience: 'var(--color-layer-resilience)'
                  };
                  const borderColors: Record<string, string> = {
                    Core: '#4a6a5a',
                    Relational: '#4b7c8c',
                    Outputs: '#b8863a',
                    Resilience: '#8a8580'
                  };
                  const labels: Record<string, string> = {
                    Core: 'Core',
                    Relational: 'Relational + Tracking',
                    Outputs: 'Stakeholder Outputs',
                    Resilience: 'Resilience'
                  };

                  return (
                    <section key={type} className="space-y-4">
                      <h4 className="font-serif italic text-[16px] text-ink-soft ml-2">
                        {labels[type]}
                      </h4>
                      <div 
                        className={`p-6 rounded-2xl flex flex-wrap gap-4 ${
                          type === 'Resilience' ? 'border-l-[3px] border-dashed border-ink-muted pl-8' : ''
                        }`}
                        style={{ backgroundColor: bgColors[type] }}
                      >
                        {entities.map((entity) => (
                          <button
                            key={entity.id}
                            onMouseEnter={(e) => {
                              setHoveredEntity(entity);
                              setHoveredCardRect(e.currentTarget.getBoundingClientRect());
                            }}
                            onMouseLeave={() => {
                              setHoveredEntity(null);
                              setHoveredCardRect(null);
                            }}
                            onClick={() => setSelectedEntity(entity)}
                            className="bg-paper border border-forest-mist rounded-xl p-[12px_16px] text-left group w-full max-w-[220px] flex flex-col gap-1 cursor-pointer shadow-warm hover:shadow-warm-hover hover:-translate-y-px transition-all"
                            style={{ borderLeftWidth: '3px', borderLeftColor: borderColors[type] }}
                          >
                            <div className="font-sans font-semibold text-[15px] text-ink leading-tight">
                              {entity.label}
                            </div>
                            <div className="font-serif text-[13px] text-ink-soft leading-snug">
                              {entity.description}
                            </div>
                          </button>
                        ))}
                      </div>
                    </section>
                  );
                })}
              </div>
            </motion.div>
          )}

          {activeTab === 'PLATFORMS' && (
            <motion.div
              key="platforms"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
            >
              {PLATFORMS_DATA.map((platform) => (
                <div key={platform.name} className="card-warm p-8 flex flex-col items-center text-center">
                  <h3 className="font-display font-bold text-xl text-ink mb-2">{platform.name}</h3>
                  <span className={`font-mono text-[11px] uppercase tracking-[0.15em] font-semibold ${
                    platform.access === 'centralized' ? 'text-forest-sage' : 
                    platform.access === 'shared' ? 'text-[#b8863a]' : 'text-[#a05050]'
                  }`}>
                    {platform.access}
                  </span>
                </div>
              ))}
            </motion.div>
          )}

          {activeTab === 'TIMELINE' && (
            <motion.div
              key="timeline"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex flex-col gap-4"
            >
              <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
                {TIMELINE_DATA.map((phase) => (
                  <div 
                    key={phase.phase} 
                    className={`p-6 rounded-xl border transition-all ${
                      phase.current 
                        ? 'bg-paper-raised border-forest-sage shadow-warm-lg ring-2 ring-forest-sage/10' 
                        : 'bg-paper/50 border-forest-mist opacity-60'
                    }`}
                  >
                    <div className="font-mono text-[10px] font-semibold uppercase tracking-widest text-forest-sage mb-2">
                      {phase.period}
                    </div>
                    <h3 className={`font-display font-bold text-lg ${phase.current ? 'text-ink' : 'text-ink-muted'}`}>
                      {phase.phase}
                    </h3>
                    {phase.current && (
                      <div className="mt-4 inline-block px-2 py-1 bg-forest-sage text-white font-mono text-[9px] font-semibold uppercase tracking-widest rounded">
                        Current
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          {activeTab === 'ROLES' && (
            <motion.div
              key="roles"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="grid grid-cols-1 md:grid-cols-2 gap-8"
            >
              {ROLES_DATA.map((role) => (
                <div key={role.role} className="card-warm p-8">
                  <h3 className="font-display font-bold text-2xl text-ink mb-6 border-b border-forest-mist pb-4 italic">{role.role}</h3>
                  <div className="space-y-6">
                    <div>
                      <h4 className="font-mono text-[11px] font-semibold uppercase tracking-[0.15em] text-forest-sage mb-2">Creates</h4>
                      <div className="flex flex-wrap gap-2">
                        {role.creates.map(c => <span key={c} className="text-[13px] font-sans bg-layer-core px-2 py-0.5 rounded">{c}</span>)}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-mono text-[11px] font-semibold uppercase tracking-[0.15em] text-forest-sage mb-2">Edits</h4>
                      <div className="flex flex-wrap gap-2">
                        {role.edits.map(c => <span key={c} className="text-[13px] font-sans bg-layer-relational px-2 py-0.5 rounded">{c}</span>)}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-mono text-[11px] font-semibold uppercase tracking-[0.15em] text-forest-sage mb-2">Reads</h4>
                      <div className="flex flex-wrap gap-2">
                        {role.reads.map(c => <span key={c} className="text-[13px] font-sans bg-layer-resilience px-2 py-0.5 rounded">{c}</span>)}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </motion.div>
          )}

          {activeTab === 'RISK' && (
            <motion.div
              key="risk"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="space-y-12"
            >
              <div className="max-w-2xl mx-auto text-center mb-12">
                <p className="text-xl font-serif italic text-ink leading-relaxed">
                  "Centralized platforms survive role changes. Personal infrastructure is the fragile layer."
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {(['High', 'Medium', 'Low'] as const).map((level) => (
                  <div key={level} className="space-y-4">
                    <h3 className={`font-display font-bold text-xl flex items-center gap-2 ${
                      level === 'High' ? 'text-[#a05050]' : level === 'Medium' ? 'text-[#b8863a]' : 'text-forest-sage'
                    }`}>
                      {level === 'High' ? <AlertTriangle size={20} /> : level === 'Medium' ? <Info size={20} /> : <CheckCircle size={20} />}
                      {level} Risk
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {OEFF_DATA.filter(e => e.risk === level).map(e => (
                        <button 
                          key={e.id} 
                          onClick={() => { setActiveTab('DIAGRAM'); setSelectedEntity(e); }}
                          className="px-4 py-1.5 bg-paper border border-forest-mist rounded-full text-[12px] font-medium text-ink-soft hover:border-forest-sage hover:text-ink transition-colors cursor-pointer shadow-warm"
                        >
                          {e.label}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          {activeTab === 'DECISIONS' && (
            <motion.div
              key="decisions"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-16"
            >
              <header className="max-w-3xl mx-auto text-center">
                <div className="font-mono text-[11px] font-semibold uppercase tracking-[0.3em] text-forest-sage mb-4">Architecture Decision Records</div>
                <h2 className="text-3xl font-display font-bold text-ink mb-6">The March 13, 2026 Strategy Session</h2>
                <p className="text-lg font-serif italic text-ink-soft leading-relaxed">
                  Kim and Garen met to finalize the load-bearing walls of the new data model. These decisions prioritize relational integrity over flat-file convenience.
                </p>
              </header>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {DECISIONS_DATA.map((decision) => (
                  <div key={decision.id} className="card-warm p-10 flex flex-col gap-6 relative overflow-hidden group">
                    <div className="absolute top-0 right-0 p-8 font-display text-8xl text-forest-sage/5 select-none group-hover:text-forest-sage/10 transition-colors">
                      {decision.id}
                    </div>
                    
                    <div className="space-y-4 relative z-10">
                      <div className="font-mono text-[11px] font-semibold uppercase tracking-widest text-forest-sage">Decision {decision.id}</div>
                      <h3 className="text-[20px] font-display font-semibold text-ink">{decision.title}</h3>
                      <p className="font-serif text-[15px] text-ink-soft leading-relaxed">
                        {decision.explanation}
                      </p>
                    </div>

                    {decision.quote && (
                      <div className="mt-auto pt-6 border-l-2 border-forest-sage pl-6 relative z-10">
                        <div className="flex gap-3">
                          <blockquote className="font-serif italic text-[15px] text-forest-sage leading-snug">
                            "{decision.quote}"
                          </blockquote>
                        </div>
                        <div className="mt-2 font-mono text-[10px] font-semibold uppercase tracking-widest text-ink-muted">
                          — Kim
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>

              <footer className="max-w-3xl mx-auto pt-16 border-t border-forest-mist">
                <div className="bg-ink text-paper-bg p-10 rounded-2xl shadow-warm-lg">
                  <div className="font-mono text-[11px] font-semibold uppercase tracking-[0.3em] text-forest-mist mb-4">Synthesis</div>
                  <p className="text-xl font-serif italic leading-relaxed">
                    "These 7 decisions reshaped every downstream tool. They're the load-bearing walls — change one, and the sync scripts, merge sheets, and host pages all need updating."
                  </p>
                </div>
              </footer>
            </motion.div>
          )}

          {activeTab === 'FLOW' && (
            <DataFlowView />
          )}

          {activeTab === 'EVOLUTION' && (
            <EvolutionView />
          )}
        </AnimatePresence>
      </main>

      {/* Detail Panel */}
      <AnimatePresence>
        {selectedEntity && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedEntity(null)}
              className="fixed inset-0 bg-[#2c2825]/20 backdrop-blur-sm z-50"
            />
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="fixed top-0 right-0 h-full w-full max-w-[480px] bg-paper z-[60] shadow-warm-lg overflow-y-auto p-12 flex flex-col"
            >
              <button 
                onClick={() => setSelectedEntity(null)}
                className="absolute top-8 right-8 p-2 hover:bg-linen rounded-full transition-colors cursor-pointer"
              >
                <X size={24} />
              </button>

              <div className="mb-8">
                <div className="flex items-center gap-2 text-[11px] font-mono font-semibold uppercase tracking-[0.15em] text-forest-sage mb-4">
                  <Shield size={12} />
                  {selectedEntity.type} Layer
                </div>
                <h2 className="text-3xl font-display font-bold text-ink mb-4">{selectedEntity.label}</h2>
                <p className="text-[15px] font-serif italic text-ink-soft leading-relaxed">
                  {selectedEntity.synthesis}
                </p>
              </div>

              <div className="flex flex-wrap gap-2 mb-10">
                <span className="px-[10px] py-[4px] bg-forest-mist text-ink font-mono font-semibold text-[10px] uppercase tracking-[0.1em] rounded-full">
                  {selectedEntity.type}
                </span>
                <span className="px-[10px] py-[4px] bg-linen text-ink font-mono font-semibold text-[10px] uppercase tracking-[0.1em] rounded-full">
                  {selectedEntity.platform}
                </span>
                <span className={`px-[10px] py-[4px] text-white font-mono font-semibold text-[10px] uppercase tracking-[0.1em] rounded-full ${
                  selectedEntity.risk === 'High' ? 'bg-[#a05050]' : selectedEntity.risk === 'Medium' ? 'bg-[#b8863a]' : 'bg-[#4a6a5a]'
                }`}>
                  Risk: {selectedEntity.risk}
                </span>
                {selectedEntity.fieldCount && (
                  <span className="px-[10px] py-[4px] bg-[#2d4a3a] text-white font-mono font-semibold text-[10px] uppercase tracking-[0.1em] rounded-full">
                    {selectedEntity.fieldCount} Fields
                  </span>
                )}
              </div>

              <div className="space-y-12 flex-1">
                {selectedEntity.ownership && (
                  <section>
                    <h3 className="font-mono text-[11px] font-semibold uppercase tracking-[0.15em] text-ink-muted mb-4">Ownership</h3>
                    <div className="grid grid-cols-3 gap-px bg-forest-mist border border-forest-mist rounded-xl overflow-hidden shadow-warm">
                      <div className="bg-paper-bg p-4 flex flex-col gap-1">
                        <div className="text-[9px] font-mono font-semibold uppercase tracking-tighter text-ink-muted">Creates</div>
                        <div className="text-[13px] font-sans font-semibold text-ink">{selectedEntity.ownership.creates}</div>
                      </div>
                      <div className="bg-paper-bg p-4 flex flex-col gap-1">
                        <div className="text-[9px] font-mono font-semibold uppercase tracking-tighter text-ink-muted">Edits</div>
                        <div className="text-[13px] font-sans font-semibold text-ink">{selectedEntity.ownership.edits}</div>
                      </div>
                      <div className="bg-paper-bg p-4 flex flex-col gap-1">
                        <div className="text-[9px] font-mono font-semibold uppercase tracking-tighter text-ink-muted">Reads</div>
                        <div className="text-[13px] font-sans font-semibold text-ink">{selectedEntity.ownership.reads}</div>
                      </div>
                    </div>
                    {selectedEntity.ownership.notes && (
                      <p className="mt-3 text-[12px] font-serif italic text-ink-muted leading-snug">
                        {selectedEntity.ownership.notes}
                      </p>
                    )}
                  </section>
                )}

                {selectedEntity.dataFlow && (
                  <section>
                    <h3 className="font-mono text-[11px] font-semibold uppercase tracking-[0.15em] text-ink-muted mb-4">Data Flow</h3>
                    <div className="flex items-center gap-4 bg-linen p-5 rounded-xl border border-forest-mist shadow-warm">
                      <div className="flex-1 text-right">
                        <div className="text-[9px] font-mono font-semibold uppercase tracking-tighter text-forest-sage mb-1">Inbound</div>
                        <div className="text-[12px] font-sans font-medium text-ink">{selectedEntity.dataFlow.inbound.join(', ')}</div>
                      </div>
                      <div className="text-forest-sage font-bold text-lg">→</div>
                      <div className="flex-1">
                        <div className="text-[9px] font-mono font-semibold uppercase tracking-tighter text-forest-sage mb-1">Outbound</div>
                        <div className="text-[12px] font-sans font-medium text-ink">{selectedEntity.dataFlow.outbound.join(', ')}</div>
                      </div>
                    </div>
                  </section>
                )}

                <section>
                  <details className="group" open>
                    <summary className="font-mono text-[11px] font-semibold uppercase tracking-[0.15em] text-ink-muted mb-4 cursor-pointer list-none flex items-center justify-between">
                      Field Schema
                      <span className="group-open:rotate-180 transition-transform text-forest-sage">▼</span>
                    </summary>
                    <div className="bg-linen p-6 rounded-xl border border-forest-mist mt-2 shadow-warm">
                      {Array.isArray(selectedEntity.schema) && typeof selectedEntity.schema[0] === 'string' ? (
                        <ul className="space-y-2">
                          {(selectedEntity.schema as string[]).map(field => (
                            <li key={field} className="flex items-center gap-3 text-[14px] font-mono text-ink-soft">
                              <div className="w-1.5 h-1.5 bg-forest-sage rounded-full opacity-40" />
                              {field}
                            </li>
                          ))}
                        </ul>
                      ) : (
                        <div className="space-y-8">
                          {(selectedEntity.schema as { group: string; fields: string[] }[]).map(group => (
                            <div key={group.group}>
                              <h4 className="text-[11px] font-mono font-semibold uppercase tracking-wider text-forest-sage mb-3 border-b border-forest-mist pb-1">
                                {group.group}
                              </h4>
                              <ul className="space-y-2">
                                {group.fields.map(field => (
                                  <li key={field} className="flex items-center gap-3 text-[13px] font-mono text-ink-soft">
                                    <div className="w-1.5 h-1.5 bg-forest-sage rounded-full opacity-30" />
                                    {field}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </details>
                </section>

                <section>
                  <h3 className="font-mono text-[11px] font-semibold uppercase tracking-[0.15em] text-ink-muted mb-4">Related Entities</h3>
                  <div className="flex flex-wrap gap-x-6 gap-y-3">
                    {selectedEntity.connections.map(id => {
                      const related = OEFF_DATA.find(e => e.id === id);
                      if (!related) return null;
                      return (
                        <button
                          key={id}
                          onClick={() => setSelectedEntity(related)}
                          className="text-[14px] text-forest-sage hover:text-ink font-medium underline underline-offset-4 decoration-forest-sage/30 transition-colors flex items-center gap-1 cursor-pointer"
                        >
                          {related.label}
                          <ExternalLink size={12} />
                        </button>
                      );
                    })}
                  </div>
                </section>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* Bezier Line Overlay */}
      <AnimatePresence>
        {renderBezierLine()}
      </AnimatePresence>
    </div>
  );
}
