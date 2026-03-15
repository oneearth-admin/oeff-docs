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
      <header className="pt-12 pb-6 text-center border-b-2 border-sage max-w-4xl mx-auto px-4">
        <h1 className="text-[32px] font-display font-bold text-forest-canopy leading-tight">OEFF Architecture</h1>
        <p className="font-mono text-[12px] uppercase tracking-[0.3em] text-[#8a8580] mt-1">One Earth Film Festival</p>
      </header>

      {/* Tab Navigation */}
      <nav className="flex justify-center gap-8 py-8">
        {(['DIAGRAM', 'PLATFORMS', 'TIMELINE', 'ROLES', 'RISK', 'DECISIONS', 'FLOW', 'EVOLUTION'] as Tab[]).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`font-mono text-[12px] uppercase tracking-widest pb-1 transition-all duration-200 border-b-2 cursor-pointer ${
              activeTab === tab 
                ? 'text-[#5c7c6b] border-[#5c7c6b]' 
                : 'text-[#2c2825]/40 border-transparent hover:text-[#2c2825]/60'
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
              <RingDiagram className="mb-16" />

              {/* Layered Card List */}
              <div className="w-full space-y-10">
                {(['Core', 'Relational', 'Outputs', 'Resilience'] as const).map((type) => {
                  const entities = OEFF_DATA.filter(e => e.type === type);
                  const bgColors: Record<string, string> = {
                    Core: '#dce8e0',
                    Relational: '#e8e3dd',
                    Outputs: '#f0ede8',
                    Resilience: '#f5f3f0'
                  };
                  const labels: Record<string, string> = {
                    Core: 'Core',
                    Relational: 'Relational + Tracking',
                    Outputs: 'Stakeholder Outputs',
                    Resilience: 'Resilience'
                  };

                  return (
                    <section key={type} className="space-y-3">
                      <h4 className="font-serif italic text-[14px] text-sage ml-2">
                        {labels[type]}
                      </h4>
                      <div 
                        className={`p-[1.25rem_1.5rem] rounded-xl flex flex-wrap gap-4 ${
                          type === 'Resilience' ? 'border-l-[3px] border-dashed border-[#8a8580] pl-8' : ''
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
                            className="bg-white border border-border-soft rounded-xl p-4 text-left group w-full max-w-[200px] flex flex-col gap-1 cursor-pointer hover:border-sage shadow-warm hover:shadow-warm-lg transition-all"
                          >
                            <div className="font-sans font-semibold text-[15px] text-[#1a2e22] leading-tight">
                              {entity.label}
                            </div>
                            <div className="font-serif text-[13px] text-[#2c2825]/50 leading-snug">
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
                  <h3 className="font-display text-xl mb-2">{platform.name}</h3>
                  <span className={`font-mono text-[10px] uppercase tracking-widest font-bold ${
                    platform.access === 'centralized' ? 'text-emerald-700' : 
                    platform.access === 'shared' ? 'text-amber-600' : 'text-rose-600'
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
                    className={`p-6 rounded-lg border transition-all ${
                      phase.current 
                        ? 'bg-white border-[#5c7c6b] shadow-md ring-2 ring-[#5c7c6b]/20' 
                        : 'bg-white/50 border-[#c8d9ce] opacity-60'
                    }`}
                  >
                    <div className="font-mono text-[10px] uppercase tracking-tighter text-[#5c7c6b] mb-2">
                      {phase.period}
                    </div>
                    <h3 className={`font-display text-lg ${phase.current ? 'text-[#1a2e22]' : 'text-[#2c2825]/40'}`}>
                      {phase.phase}
                    </h3>
                    {phase.current && (
                      <div className="mt-4 inline-block px-2 py-1 bg-[#5c7c6b] text-white font-mono text-[9px] uppercase tracking-widest rounded">
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
                  <h3 className="font-display text-2xl mb-6 border-b border-[#c8d9ce] pb-4 italic">{role.role}</h3>
                  <div className="space-y-6">
                    <div>
                      <h4 className="font-mono text-[10px] uppercase tracking-widest text-[#5c7c6b] mb-2">Creates</h4>
                      <div className="flex flex-wrap gap-2">
                        {role.creates.map(c => <span key={c} className="text-[13px] bg-[#dce8e0] px-2 py-0.5 rounded">{c}</span>)}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-mono text-[10px] uppercase tracking-widest text-[#5c7c6b] mb-2">Edits</h4>
                      <div className="flex flex-wrap gap-2">
                        {role.edits.map(c => <span key={c} className="text-[13px] bg-[#e8e3dd] px-2 py-0.5 rounded">{c}</span>)}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-mono text-[10px] uppercase tracking-widest text-[#5c7c6b] mb-2">Reads</h4>
                      <div className="flex flex-wrap gap-2">
                        {role.reads.map(c => <span key={c} className="text-[13px] bg-[#f5f3f0] px-2 py-0.5 rounded">{c}</span>)}
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
                <p className="text-xl font-serif italic text-[#1a2e22]/80 leading-relaxed">
                  "Centralized platforms survive role changes. Personal infrastructure is the fragile layer."
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {(['High', 'Medium', 'Low'] as const).map((level) => (
                  <div key={level} className="space-y-4">
                    <h3 className={`font-display text-xl flex items-center gap-2 ${
                      level === 'High' ? 'text-rose-700' : level === 'Medium' ? 'text-amber-700' : 'text-emerald-700'
                    }`}>
                      {level === 'High' ? <AlertTriangle size={20} /> : level === 'Medium' ? <Info size={20} /> : <CheckCircle size={20} />}
                      {level} Risk
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {OEFF_DATA.filter(e => e.risk === level).map(e => (
                        <button 
                          key={e.id} 
                          onClick={() => { setActiveTab('DIAGRAM'); setSelectedEntity(e); }}
                          className="px-3 py-1 bg-white border border-[#c8d9ce] rounded-full text-[12px] hover:border-[#5c7c6b] transition-colors cursor-pointer"
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
                <div className="font-mono text-[10px] uppercase tracking-[0.3em] text-[#5c7c6b] mb-4">Architecture Decision Records</div>
                <h2 className="text-3xl font-display font-bold text-[#1a2e22] mb-6">The March 13, 2026 Strategy Session</h2>
                <p className="text-lg font-serif italic text-[#2c2825]/70 leading-relaxed">
                  Kim and Garen met to finalize the load-bearing walls of the new data model. These decisions prioritize relational integrity over flat-file convenience.
                </p>
              </header>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {DECISIONS_DATA.map((decision) => (
                  <div key={decision.id} className="card-warm p-10 flex flex-col gap-6 relative overflow-hidden group">
                    <div className="absolute top-0 right-0 p-8 font-display text-8xl text-[#5c7c6b]/5 select-none group-hover:text-[#5c7c6b]/10 transition-colors">
                      {decision.id}
                    </div>
                    
                    <div className="space-y-4 relative z-10">
                      <div className="font-mono text-[10px] uppercase tracking-widest text-[#5c7c6b]">Decision {decision.id}</div>
                      <h3 className="text-2xl font-display font-bold text-[#1a2e22]">{decision.title}</h3>
                      <p className="font-serif text-[15px] text-[#2c2825]/80 leading-relaxed">
                        {decision.explanation}
                      </p>
                    </div>

                    {decision.quote && (
                      <div className="mt-auto pt-6 border-t border-[#c8d9ce]/50 relative z-10">
                        <div className="flex gap-3">
                          <Quote size={16} className="text-[#5c7c6b] shrink-0 mt-1" />
                          <blockquote className="font-serif italic text-[14px] text-[#5c7c6b] leading-snug">
                            "{decision.quote}"
                          </blockquote>
                        </div>
                        <div className="mt-2 ml-7 font-mono text-[9px] uppercase tracking-widest text-[#8a8580]">
                          — Kim
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>

              <footer className="max-w-3xl mx-auto pt-16 border-t border-[#5c7c6b]/20">
                <div className="bg-[#1a2e22] text-[#f7f5f2] p-10 rounded-2xl shadow-xl">
                  <div className="font-mono text-[10px] uppercase tracking-[0.3em] text-[#c8d9ce] mb-4">Synthesis</div>
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
              className="fixed top-0 right-0 h-full w-full max-w-[480px] bg-white z-[60] shadow-2xl overflow-y-auto p-12 flex flex-col"
            >
              <button 
                onClick={() => setSelectedEntity(null)}
                className="absolute top-8 right-8 p-2 hover:bg-[#f7f5f2] rounded-full transition-colors cursor-pointer"
              >
                <X size={24} />
              </button>

              <div className="mb-8">
                <div className="flex items-center gap-2 text-[10px] font-mono uppercase tracking-widest text-[#5c7c6b] mb-4">
                  <Shield size={12} />
                  {selectedEntity.type} Layer
                </div>
                <h2 className="text-4xl font-display font-bold italic text-[#1a2e22] mb-4">{selectedEntity.label}</h2>
                <p className="text-xl font-serif italic text-[#5c7c6b] leading-relaxed">
                  {selectedEntity.synthesis}
                </p>
              </div>

              <div className="flex flex-wrap gap-2 mb-8">
                <span className="px-3 py-1 bg-[#dce8e0] text-[#1a2e22] text-[10px] font-mono uppercase tracking-wider rounded font-bold">
                  {selectedEntity.type}
                </span>
                <span className="px-3 py-1 bg-[#e8e3dd] text-[#1a2e22] text-[10px] font-mono uppercase tracking-wider rounded font-bold">
                  {selectedEntity.platform}
                </span>
                <span className="px-3 py-1 bg-[#f0ede8] text-[#1a2e22] text-[10px] font-mono uppercase tracking-wider rounded font-bold">
                  {selectedEntity.lifecycle}
                </span>
                <span className={`px-3 py-1 text-white text-[10px] font-mono uppercase tracking-wider rounded font-bold ${
                  selectedEntity.risk === 'High' ? 'bg-rose-600' : selectedEntity.risk === 'Medium' ? 'bg-amber-600' : 'bg-emerald-600'
                }`}>
                  Risk: {selectedEntity.risk}
                </span>
                {selectedEntity.fieldCount && (
                  <span className="px-3 py-1 bg-[#1a2e22] text-white text-[10px] font-mono uppercase tracking-wider rounded font-bold">
                    {selectedEntity.fieldCount} Fields
                  </span>
                )}
              </div>

              <div className="space-y-10 flex-1">
                {selectedEntity.ownership && (
                  <section>
                    <h3 className="font-mono text-[10px] uppercase tracking-widest text-[#2c2825]/40 mb-4 font-bold">Ownership</h3>
                    <div className="grid grid-cols-3 gap-4 bg-[#f7f5f2] p-4 rounded-lg border border-[#c8d9ce]">
                      <div>
                        <div className="text-[9px] uppercase tracking-tighter text-[#5c7c6b] mb-1">Creates</div>
                        <div className="text-[13px] font-sans font-medium">{selectedEntity.ownership.creates}</div>
                      </div>
                      <div>
                        <div className="text-[9px] uppercase tracking-tighter text-[#5c7c6b] mb-1">Edits</div>
                        <div className="text-[13px] font-sans font-medium">{selectedEntity.ownership.edits}</div>
                      </div>
                      <div>
                        <div className="text-[9px] uppercase tracking-tighter text-[#5c7c6b] mb-1">Reads</div>
                        <div className="text-[13px] font-sans font-medium">{selectedEntity.ownership.reads}</div>
                      </div>
                    </div>
                    {selectedEntity.ownership.notes && (
                      <p className="mt-3 text-[12px] font-serif italic text-[#2c2825]/60 leading-snug">
                        {selectedEntity.ownership.notes}
                      </p>
                    )}
                  </section>
                )}

                {selectedEntity.dataFlow && (
                  <section>
                    <h3 className="font-mono text-[10px] uppercase tracking-widest text-[#2c2825]/40 mb-4 font-bold">Data Flow</h3>
                    <div className="flex items-center gap-4 bg-[#f7f5f2] p-4 rounded-lg border border-[#c8d9ce]">
                      <div className="flex-1 text-right">
                        <div className="text-[9px] uppercase tracking-tighter text-[#5c7c6b] mb-1">Inbound</div>
                        <div className="text-[12px] font-sans">{selectedEntity.dataFlow.inbound.join(', ')}</div>
                      </div>
                      <div className="text-[#5c7c6b] font-bold">→</div>
                      <div className="flex-1">
                        <div className="text-[9px] uppercase tracking-tighter text-[#5c7c6b] mb-1">Outbound</div>
                        <div className="text-[12px] font-sans">{selectedEntity.dataFlow.outbound.join(', ')}</div>
                      </div>
                    </div>
                  </section>
                )}

                <section>
                  <details className="group" open>
                    <summary className="font-mono text-[10px] uppercase tracking-widest text-[#2c2825]/40 mb-4 font-bold cursor-pointer list-none flex items-center justify-between">
                      Field Schema
                      <span className="group-open:rotate-180 transition-transform">▼</span>
                    </summary>
                    <div className="bg-[#f7f5f2] p-6 rounded-lg border border-[#c8d9ce] mt-2">
                      {Array.isArray(selectedEntity.schema) && typeof selectedEntity.schema[0] === 'string' ? (
                        <ul className="space-y-2">
                          {(selectedEntity.schema as string[]).map(field => (
                            <li key={field} className="flex items-center gap-3 text-[14px] font-mono text-[#2c2825]/70">
                              <div className="w-1.5 h-1.5 bg-[#5c7c6b] rounded-full" />
                              {field}
                            </li>
                          ))}
                        </ul>
                      ) : (
                        <div className="space-y-6">
                          {(selectedEntity.schema as { group: string; fields: string[] }[]).map(group => (
                            <div key={group.group}>
                              <h4 className="text-[11px] font-mono uppercase tracking-wider text-[#5c7c6b] mb-3 font-bold border-b border-[#c8d9ce] pb-1">
                                {group.group}
                              </h4>
                              <ul className="space-y-2">
                                {group.fields.map(field => (
                                  <li key={field} className="flex items-center gap-3 text-[13px] font-mono text-[#2c2825]/70">
                                    <div className="w-1.5 h-1.5 bg-[#5c7c6b] rounded-full opacity-50" />
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
                  <h3 className="font-mono text-[10px] uppercase tracking-widest text-[#2c2825]/40 mb-4 font-bold">Related Entities</h3>
                  <div className="flex flex-wrap gap-x-6 gap-y-3">
                    {selectedEntity.connections.map(id => {
                      const related = OEFF_DATA.find(e => e.id === id);
                      if (!related) return null;
                      return (
                        <button
                          key={id}
                          onClick={() => setSelectedEntity(related)}
                          className="text-[14px] text-[#5c7c6b] hover:text-[#1a2e22] underline underline-offset-4 decoration-[#5c7c6b]/30 transition-colors flex items-center gap-1 cursor-pointer"
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
