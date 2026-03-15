import React from 'react';
import { motion } from 'motion/react';
import { ArrowDown, Database, Cpu, Share2 } from 'lucide-react';

export const DataFlowView: React.FC = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-16 pb-24"
    >
      <header className="max-w-3xl mx-auto text-center">
        <div className="font-mono text-[11px] font-semibold uppercase tracking-[0.3em] text-forest-sage mb-4">Pipeline Architecture</div>
        <h2 className="text-3xl font-display font-bold text-ink mb-6">The Downhill Data Flow</h2>
        <p className="text-lg font-serif italic text-ink-soft leading-relaxed">
          The OEFF pipeline is strictly unidirectional. Canonical sources feed master tables, which feed assembly scripts, which produce flat outputs.
        </p>
      </header>

      <div className="flex flex-col items-center gap-12 max-w-4xl mx-auto">
        
        {/* INPUTS SECTION */}
        <section className="w-full space-y-8">
          <div className="flex items-center gap-4 mb-6">
            <div className="h-[1px] flex-1 bg-forest-mist" />
            <h3 className="font-mono text-[11px] font-semibold uppercase tracking-[0.4em] text-forest-sage">Inputs (Canonical Sources)</h3>
            <div className="h-[1px] flex-1 bg-forest-mist" />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <FlowCard 
              title="Kim's Tracker Sheets" 
              subtitle="5 tabs" 
              description="Validated contacts, venues, AV, films"
              target="Directory + Venues + Films"
              color="green"
            />
            <FlowCard 
              title="OEC Active Roadmap" 
              subtitle="Project Management" 
              description="Scheduling, film assignments, confirmations"
              target="Events table"
              color="green"
            />
            <FlowCard 
              title="Kim's Comms Tracker" 
              subtitle="2 tabs" 
              description="Outreach history, RACI, engagement"
              target="Comms Log + Deliverables"
              color="green"
            />
          </div>
        </section>

        <ArrowDown className="text-forest-mist" size={32} />

        {/* ASSEMBLY SECTION */}
        <section className="w-full space-y-8">
          <div className="flex items-center gap-4 mb-6">
            <div className="h-[1px] flex-1 bg-forest-mist" />
            <h3 className="font-mono text-[11px] font-semibold uppercase tracking-[0.4em] text-forest-sage">Assembly</h3>
            <div className="h-[1px] flex-1 bg-forest-mist" />
          </div>
          
          <div className="flex justify-center">
            <FlowCard 
              title="assemble-host-helper.py" 
              subtitle="Python Script" 
              description="Events + Venues + Films + Directory"
              target="Host Helper 2026 (28 flat rows)"
              color="blue"
              className="max-w-md w-full"
            />
          </div>
        </section>

        <ArrowDown className="text-forest-mist" size={32} />

        {/* OUTPUTS SECTION */}
        <section className="w-full space-y-8">
          <div className="flex items-center gap-4 mb-6">
            <div className="h-[1px] flex-1 bg-forest-mist" />
            <h3 className="font-mono text-[11px] font-semibold uppercase tracking-[0.4em] text-forest-sage">Outputs</h3>
            <div className="h-[1px] flex-1 bg-forest-mist" />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-3xl mx-auto w-full">
            <FlowCard 
              title="Interface Designer" 
              subtitle="Airtable Native" 
              description="Host-facing pages"
              target="hosts.oneearthfilmfest.org"
              color="gray"
            />
            <FlowCard 
              title="oeff-airtable-sync.py" 
              subtitle="Python Script" 
              description="Syncs Host Helper to outreach tools"
              target="Mailmeteor campaigns"
              color="gray"
            />
          </div>
        </section>
      </div>

      {/* CALLOUTS */}
      <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8 mt-16">
        <div className="bg-ink text-paper-bg p-8 rounded-2xl shadow-warm-lg">
          <div className="flex items-center gap-3 mb-4">
            <Cpu className="text-forest-mist" size={20} />
            <div className="font-mono text-[10px] font-semibold uppercase tracking-[0.2em] text-forest-mist">Key Insight</div>
          </div>
          <p className="text-lg font-serif italic leading-relaxed">
            "Data flows downhill. Master tables feed Events. Events feed the assembly script. The script produces flat rows. No data flows upstream — that's what makes the system debuggable."
          </p>
        </div>

        <div className="bg-paper border border-forest-mist p-8 rounded-2xl shadow-warm">
          <div className="flex items-center gap-3 mb-4">
            <Database className="text-forest-sage" size={20} />
            <div className="font-mono text-[10px] font-semibold uppercase tracking-[0.2em] text-forest-sage">Dual-Canonical Principle</div>
          </div>
          <p className="text-[15px] font-serif text-ink-soft leading-relaxed">
            Tracker sheets for validated operational data. Roadmap for team-facing planning. Airtable for relational structure. Sync scripts bridge them.
          </p>
        </div>
      </div>
    </motion.div>
  );
};

interface FlowCardProps {
  title: string;
  subtitle: string;
  description: string;
  target: string;
  color: 'green' | 'blue' | 'gray';
  className?: string;
}

const FlowCard: React.FC<FlowCardProps> = ({ title, subtitle, description, target, color, className = '' }) => {
  const colorClasses = {
    green: 'border-forest-mist bg-layer-core text-ink',
    blue: 'border-forest-mist bg-layer-relational text-ink',
    gray: 'border-forest-mist bg-paper text-ink'
  };

  const iconClasses = {
    green: 'text-forest-sage',
    blue: 'text-forest-sage',
    gray: 'text-ink-muted'
  };

  return (
    <div className={`p-6 rounded-xl border shadow-warm flex flex-col gap-3 transition-all hover:shadow-warm-hover hover:-translate-y-px ${colorClasses[color]} ${className}`}>
      <div className="flex items-start justify-between">
        <div>
          <div className="font-mono text-[10px] font-semibold uppercase tracking-widest text-ink-muted mb-1">{subtitle}</div>
          <h4 className="text-lg font-display font-bold leading-tight">{title}</h4>
        </div>
        {color === 'green' ? <Database size={18} className={iconClasses[color]} /> : 
         color === 'blue' ? <Cpu size={18} className={iconClasses[color]} /> : 
         <Share2 size={18} className={iconClasses[color]} />}
      </div>
      
      <p className="text-[14px] font-serif italic text-ink-soft leading-snug">
        {description}
      </p>
      
      <div className="mt-2 pt-3 border-t border-current/10 flex items-center gap-2">
        <div className="text-[10px] font-mono font-semibold uppercase tracking-tighter text-ink-muted">Feeds →</div>
        <div className="text-[12px] font-sans font-semibold">{target}</div>
      </div>
    </div>
  );
};
