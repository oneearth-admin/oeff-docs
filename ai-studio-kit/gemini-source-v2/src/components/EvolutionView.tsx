import React from 'react';
import { motion } from 'motion/react';
import { History, Zap, Info } from 'lucide-react';

export const EvolutionView: React.FC = () => {
  const comparisons = [
    {
      label: "Organizing principle",
      v1: "Venues",
      v2: "Events"
    },
    {
      label: "Host Helper Access",
      v1: "Per-venue shared grid views (24)",
      v2: "Per-event Interface Designer pages"
    },
    {
      label: "Data chain",
      v1: "3-layer rollup (link → LKP → Host formula)",
      v2: "Flat text fields, script-assembled"
    },
    {
      label: "Kim's edit model",
      v1: "Cannot edit rollups or formulas",
      v2: "Team edits flat fields directly"
    },
    {
      label: "Multi-event venues",
      v1: "Concatenated values with commas",
      v2: "One row per event — no ambiguity"
    },
    {
      label: "Contacts",
      v1: "Separate Host + Film Contact tables",
      v2: "Unified Directory with role + priority"
    },
    {
      label: "Debuggability",
      v1: "Trace link → rollup → formula",
      v2: "What you see is what's stored"
    },
    {
      label: "Table Complexity",
      v1: "Venues table: 69 fields (29 rollup/formula debt)",
      v2: "Host Helper: 28 fields, all text/date/URL"
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-12 pb-24 max-w-5xl mx-auto"
    >
      <header className="text-center">
        <div className="font-mono text-[11px] font-semibold uppercase tracking-[0.3em] text-forest-sage mb-4">Architecture Evolution</div>
        <h2 className="text-3xl font-display font-bold text-ink mb-6">v1 (Venue-Centric) vs v2 (Event-Centric)</h2>
        <p className="text-lg font-serif italic text-ink-soft leading-relaxed max-w-3xl mx-auto">
          Shifting from a relational rollup model to a flattened event-centric model to prioritize editability and operational clarity.
        </p>
      </header>

      <div className="grid grid-cols-[1fr_2fr_2fr] gap-px bg-forest-mist border border-forest-mist rounded-xl overflow-hidden shadow-warm">
        {/* Header Row */}
        <div className="bg-paper p-4 font-mono text-[10px] font-semibold uppercase tracking-widest text-ink-muted flex items-center">Dimension</div>
        <div className="bg-layer-outputs/30 p-4 font-display font-bold text-ink flex items-center gap-2">
          <History size={16} className="text-ink-muted" />
          v1 — Venue-Centric
        </div>
        <div className="bg-layer-core/30 p-4 font-display font-bold text-ink flex items-center gap-2">
          <Zap size={16} className="text-forest-sage" />
          v2 — Event-Centric
        </div>

        {/* Comparison Rows */}
        {comparisons.map((row, idx) => (
          <React.Fragment key={idx}>
            <div className="bg-paper p-6 font-mono text-[11px] font-semibold uppercase tracking-wider text-forest-sage flex items-center border-t border-forest-mist">
              {row.label}
            </div>
            <div className="bg-paper/50 p-6 font-serif text-[15px] text-ink-soft border-t border-forest-mist">
              {row.v1}
            </div>
            <div className="bg-layer-core/10 p-6 font-serif text-[15px] text-ink border-t border-forest-mist font-medium">
              {row.v2}
            </div>
          </React.Fragment>
        ))}
      </div>

      {/* Synthesis Callout */}
      <div className="bg-ink text-paper-bg p-10 rounded-2xl shadow-warm-lg relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-10">
          <Zap size={120} />
        </div>
        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-6">
            <Info className="text-forest-mist" size={20} />
            <div className="font-mono text-[10px] font-semibold uppercase tracking-[0.2em] text-forest-mist">Core Tradeoff Synthesis</div>
          </div>
          <p className="text-xl font-serif italic leading-relaxed">
            "v2 duplicates data (every event row has its own copy of the venue address) in exchange for editability and clarity. The assemble-host-helper.py script can re-flatten at any time without breaking Kim's manual edits in the 7 protected fields."
          </p>
        </div>
      </div>
    </motion.div>
  );
};
