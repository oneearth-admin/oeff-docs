export interface Entity {
  id: string;
  label: string;
  ring: number; // 0 (center), 1, 2, 3, 4
  description: string;
  synthesis: string;
  connections: string[];
  type: 'Core' | 'Relational' | 'Outputs' | 'Resilience';
  platform: string;
  lifecycle: 'Year-over-year' | 'Seasonal';
  risk: 'Low' | 'Medium' | 'High';
  schema?: string[] | { group: string; fields: string[] }[];
  fieldCount?: number;
  ownership?: {
    creates: string;
    edits: string;
    reads: string;
    notes?: string;
  };
  dataFlow?: {
    inbound: string[];
    outbound: string[];
  };
}

export interface Decision {
  id: number;
  title: string;
  explanation: string;
  quote?: string;
}

export const DECISIONS_DATA: Decision[] = [
  {
    id: 1,
    title: "Events as relational key",
    explanation: "Events and screenings represent the most granular and specific level of data in the system. They link to master tables rather than the reverse, ensuring all logistical data is anchored to a specific point in time and space.",
    quote: "The most specific our data will ever get is by event."
  },
  {
    id: 2,
    title: "Unified Directory",
    explanation: "All people-data in one table with a Contact Type field, replacing scattered host, venue, and filmmaker contact lists with a single source of truth for institutional memory.",
    quote: "What if we just called this table a directory?"
  },
  {
    id: 3,
    title: "Partnership categorization",
    explanation: "Establishing a clear distinction between mission-oriented collaborators and transactional contacts. Collaborators are partners in the festival's mission, while transactional contacts are engaged for specific deliverables where money changes hands.",
  },
  {
    id: 4,
    title: "Members vs Partners",
    explanation: "Defining the 14k email list as 'members' (who we work for) and active stakeholders as 'partners' (who we work with). This clarifies the intent of every communication.",
    quote: "Distinguish who we work with and who we work for."
  },
  {
    id: 5,
    title: "Per-event interface pages",
    explanation: "Replacing 24 shared grid views with record-parameter deep links in Interface Designer. This provides direct, focused edit access for each specific event, reducing cognitive load.",
    quote: "I don't want to see 200 rows if I'm only working on one venue."
  },
  {
    id: 6,
    title: "Dual venue classification",
    explanation: "Implementing a non-competing classification system: Flagship/Community (based on team presence) and T1–T4 (based on technical needs).",
  },
  {
    id: 7,
    title: "'Events' umbrella term",
    explanation: "Redefining 'Screenings' as a subtype of the broader 'Events' category, future-proofs the model to include action fairs, concerts, and panels.",
  }
];

export const OEFF_DATA: Entity[] = [
  // CORE
  {
    id: 'events',
    label: 'Events',
    ring: 0,
    type: 'Core',
    description: 'The relational hub',
    synthesis: 'Every other table points here. Lose Events, lose the spine of the entire system.',
    connections: ['directory', 'venues', 'films', 'sponsors', 'members', 'merged_timeline'],
    platform: 'Airtable',
    lifecycle: 'Seasonal',
    risk: 'Low',
    fieldCount: 52,
    ownership: {
      creates: 'scripts',
      edits: 'Technical Coordinator',
      reads: 'all'
    },
    dataFlow: {
      inbound: ['OEC Active Roadmap'],
      outbound: ['Host Helper 2026', 'Deliverables', 'Email Campaigns']
    },
    schema: ['Event Name', 'Date', 'Time', 'Venue (link)', 'Film (link)', 'Directory Contacts (link)', 'Event Type', 'Status', 'Eventbrite URL', 'Access Code']
  },
  {
    id: 'directory',
    label: 'Directory',
    ring: 1,
    type: 'Core',
    description: 'All people in one place',
    synthesis: 'The festival\'s institutional memory. Centralized contact management prevents fragmented outreach.',
    connections: ['events', 'sponsors', 'members'],
    platform: 'Airtable',
    lifecycle: 'Year-over-year',
    risk: 'Low',
    ownership: {
      creates: 'Kim (tracker)',
      edits: 'Kim + scripts',
      reads: 'all'
    },
    schema: ['Name', 'Email', 'Role', 'Organization', 'Tags']
  },
  {
    id: 'venues',
    label: 'Venues',
    ring: 1,
    type: 'Core',
    description: 'Physical spaces and their capabilities',
    synthesis: 'Maps physical footprint to digital schedule. Essential for logistical planning.',
    connections: ['events', 'host_confirmations', 'host_intake'],
    platform: 'Airtable',
    lifecycle: 'Year-over-year',
    risk: 'Low',
    fieldCount: 69,
    schema: ['Venue Name', 'Address', 'Capacity', 'Tech Specs', 'Contact']
  },
  {
    id: 'films',
    label: 'Films',
    ring: 1,
    type: 'Core',
    description: 'Titles, runtimes, licensing terms',
    synthesis: 'The creative core. Tracks content from submission to screening.',
    connections: ['events', 'assets', 'filmmaker_kits'],
    platform: 'Airtable',
    lifecycle: 'Seasonal',
    risk: 'Low',
    fieldCount: 30,
    schema: ['Title', 'Director', 'Runtime', 'License Status', 'File Link']
  },
  {
    id: 'sponsors',
    label: 'Sponsors',
    ring: 1,
    type: 'Core',
    description: 'Organizations, tiers, financial commitments',
    synthesis: 'Ensures contractual obligations are met. Vital for financial sustainability.',
    connections: ['events', 'directory'],
    platform: 'Airtable',
    lifecycle: 'Seasonal',
    risk: 'Low',
    fieldCount: 39,
    schema: ['Sponsor Name', 'Tier', 'Amount', 'Logo Link', 'Contract Status']
  },
  {
    id: 'members',
    label: 'Members',
    ring: 1,
    type: 'Core',
    description: '14k email list',
    synthesis: 'Our primary audience engine. Connects individual support to festival access.',
    connections: ['events', 'directory', 'email_campaigns'],
    platform: 'Mailchimp',
    lifecycle: 'Year-over-year',
    risk: 'Low',
    schema: ['Email', 'Name', 'Member Level', 'Join Date', 'Last Active']
  },

  // RELATIONAL
  {
    id: 'host_helper_2026',
    label: 'Host Helper 2026',
    ring: 2,
    type: 'Relational',
    description: 'Script-assembled, team-editable',
    synthesis: 'The workhorse. 28 flat rows, one per event. Replaced the 3-layer rollup chain Kim couldn\'t touch.',
    connections: ['host_helper_pages', 'host_confirmations', 'host_intake'],
    platform: 'Airtable',
    lifecycle: 'Seasonal',
    risk: 'Medium',
    fieldCount: 28,
    ownership: {
      creates: 'assemble-host-helper.py',
      edits: 'Kim (7 protected fields)',
      reads: 'hosts via Interface Designer',
      notes: '21 script-owned fields (overwritten on re-run) and 7 team-editable fields (preserved): Parking, Transit, WiFi, AV Notes, Volunteer Needs, Screening Packet URL, Notes'
    },
    dataFlow: {
      inbound: ['Events', 'Venues', 'Films', 'Directory (via script)'],
      outbound: ['Host Helper Pages', 'Mailmeteor']
    },
    schema: [
      {
        group: 'Script-owned',
        fields: ['Event Name', 'Event ID', 'Film Title', 'Film Runtime', 'Filmmaker Name', 'Filmmaker Email', 'Screening Date', 'Start Time', 'Doors Open', 'Venue Name', 'Venue Address', 'Venue Capacity', 'Contact Name/Email/Phone/Role', 'Ticket URL', 'Ticket Price', 'OEFF Rep', 'Webinar Recording', 'Host Guide Link']
      },
      {
        group: 'Team-editable',
        fields: ['Parking', 'Transit', 'WiFi', 'AV Notes', 'Volunteer Needs', 'Screening Packet URL', 'Notes']
      }
    ]
  },
  {
    id: 'assets',
    label: 'Assets',
    ring: 2,
    type: 'Relational',
    description: 'Master index of all files',
    synthesis: 'Every inbound film copy, every outbound screening packet. The file ledger that prevents "where did that poster go?"',
    connections: ['asset_versions', 'films', 'event_media'],
    platform: 'Google Drive',
    lifecycle: 'Year-over-year',
    risk: 'Low',
    dataFlow: {
      inbound: ['Films', 'Events', 'Venues'],
      outbound: ['Asset Versions', 'Deliverables', 'Packet QA']
    },
    schema: ['File Name', 'Path', 'Type', 'Owner', 'Size']
  },
  {
    id: 'asset_versions',
    label: 'Asset Versions',
    ring: 2,
    type: 'Relational',
    description: 'QC history per file version',
    synthesis: 'Ensures we don\'t screen a draft. Tracks the lifecycle of every trailer and film.',
    connections: ['assets', 'deliverables'],
    platform: 'Airtable',
    lifecycle: 'Seasonal',
    risk: 'Low',
    schema: ['Asset ID', 'Version Number', 'QC Status', 'Timestamp']
  },
  {
    id: 'deliverables',
    label: 'Deliverables',
    ring: 2,
    type: 'Relational',
    description: 'Packaged outputs for stakeholders',
    synthesis: 'The specific files that must be in the booth on opening night.',
    connections: ['asset_versions', 'delivery_log', 'screening_packets'],
    platform: 'Airtable',
    lifecycle: 'Seasonal',
    risk: 'Low',
    schema: ['Deliverable Name', 'Target Venue', 'Format', 'Status']
  },
  {
    id: 'delivery_log',
    label: 'Delivery Log',
    ring: 2,
    type: 'Relational',
    description: 'Who got what, when',
    synthesis: 'Without this table, post-festival filmmaker reports require manual email archaeology.',
    connections: ['deliverables'],
    platform: 'Airtable',
    lifecycle: 'Seasonal',
    risk: 'Low',
    schema: ['Recipient', 'Deliverable ID', 'Method', 'Timestamp']
  },
  {
    id: 'comms_log',
    label: 'Comms Log',
    ring: 2,
    type: 'Relational',
    description: 'Outreach tracking',
    synthesis: 'The paper trail of promises. Ensures we don\'t ask the same host the same question twice.',
    connections: ['directory', 'host_intake'],
    platform: 'Airtable',
    lifecycle: 'Seasonal',
    risk: 'Low',
    schema: ['Contact ID', 'Date', 'Subject', 'Notes']
  },
  {
    id: 'host_confirmations',
    label: 'Host Confirmations',
    ring: 2,
    type: 'Relational',
    description: 'Host response tracking',
    synthesis: 'The green light for every event. Turns a "maybe" venue into a "confirmed" screening.',
    connections: ['venues', 'host_helper_2026'],
    platform: 'Airtable',
    lifecycle: 'Seasonal',
    risk: 'Low',
    fieldCount: 13,
    schema: ['Venue ID', 'Confirmation Date', 'Signed Agreement', 'Status']
  },
  {
    id: 'host_intake',
    label: 'Host Intake',
    ring: 2,
    type: 'Relational',
    description: 'Form responses from venue intake',
    synthesis: 'The front door for new partners. Captures technical and logistical needs.',
    connections: ['host_helper_2026', 'comms_log', 'venues'],
    platform: 'Google Forms',
    lifecycle: 'Year-over-year',
    risk: 'Low',
    schema: ['Timestamp', 'Venue Name', 'Contact Info', 'Capacity', 'Tech Needs']
  },
  {
    id: 'event_media',
    label: 'Event Media Assets',
    ring: 2,
    type: 'Relational',
    description: 'Posters, stills, press photos',
    synthesis: 'The visual identity of the program. Connects abstract events to actual photos.',
    connections: ['events', 'assets'],
    platform: 'Airtable',
    lifecycle: 'Seasonal',
    risk: 'Low',
    fieldCount: 22,
    schema: ['Event ID', 'Asset Link', 'Type', 'Credit']
  },
  {
    id: 'packet_qa',
    label: 'Packet QA',
    ring: 2,
    type: 'Relational',
    description: 'Quality checks on screening packets',
    synthesis: 'The safety net. Ensures every packet is complete and functional before opening night.',
    connections: ['screening_packets'],
    platform: 'Airtable',
    lifecycle: 'Seasonal',
    risk: 'Low',
    fieldCount: 20,
    schema: ['Packet ID', 'QA Date', 'Checker', 'Pass/Fail']
  },
  {
    id: 'webinar_content',
    label: 'Webinar Content',
    ring: 2,
    type: 'Relational',
    description: 'Recorded sessions for host training',
    synthesis: 'The digital program. Ensures our hosts have the training and slides they need.',
    connections: ['recordings'],
    platform: 'Airtable',
    lifecycle: 'Seasonal',
    risk: 'Low',
    fieldCount: 20,
    schema: ['Session Name', 'Video Link', 'Presentation Link', 'Date']
  },
  {
    id: 'participants',
    label: 'Participants',
    ring: 2,
    type: 'Relational',
    description: 'Event attendees',
    synthesis: 'The human element. Tracks travel, tech needs, and bios of everyone on stage.',
    connections: ['events', 'recordings'],
    platform: 'Airtable',
    lifecycle: 'Seasonal',
    risk: 'Low',
    schema: ['Name', 'Role', 'Bio', 'Travel Status', 'Tech Needs']
  },
  {
    id: 'recordings',
    label: 'Recordings',
    ring: 2,
    type: 'Relational',
    description: 'Session recordings linked to events',
    synthesis: 'The festival\'s legacy. Captures discussions for future audiences.',
    connections: ['webinar_content', 'participants', 'events'],
    platform: 'Vimeo',
    lifecycle: 'Year-over-year',
    risk: 'Low',
    schema: ['Event ID', 'Vimeo Link', 'Duration', 'Publish Date']
  },
  {
    id: 'merged_timeline',
    label: 'Merged Timeline',
    ring: 2,
    type: 'Relational',
    description: 'Cross-event calendar view',
    synthesis: 'The heartbeat of the festival. Merges programming, logistics, and marketing.',
    connections: ['events', 'seasons'],
    platform: 'Airtable',
    lifecycle: 'Seasonal',
    risk: 'Medium',
    schema: ['Date', 'Event ID', 'Type', 'Milestone']
  },

  // OUTPUTS
  {
    id: 'host_helper_pages',
    label: 'Host Helper Pages',
    ring: 3,
    type: 'Outputs',
    description: 'Per-event pages for host venues',
    synthesis: 'The host\'s manual. Distills complex database records into simple, actionable instructions.',
    connections: ['host_helper_2026'],
    platform: 'Cloudflare Pages',
    lifecycle: 'Seasonal',
    risk: 'Medium',
    schema: ['URL', 'Event ID', 'Last Updated', 'Access Key']
  },
  {
    id: 'screening_packets',
    label: 'Screening Packets',
    ring: 3,
    type: 'Outputs',
    description: 'Bundled deliverables for day-of operations',
    synthesis: 'The festival in a box. Everything a venue needs to run a successful screening.',
    connections: ['deliverables', 'packet_qa'],
    platform: 'Google Drive',
    lifecycle: 'Seasonal',
    risk: 'Medium',
    schema: ['Packet ID', 'Venue ID', 'Download Link', 'Size']
  },
  {
    id: 'filmmaker_kits',
    label: 'Filmmaker Kits',
    ring: 3,
    type: 'Outputs',
    description: 'License docs, reports, press assets',
    synthesis: 'Our service to creators. Provides filmmakers with laurels, schedules, and assets.',
    connections: ['films'],
    platform: 'Airtable',
    lifecycle: 'Seasonal',
    risk: 'Medium',
    schema: ['Filmmaker Name', 'Film ID', 'Kit Link', 'Status']
  },
  {
    id: 'email_campaigns',
    label: 'Email Campaigns',
    ring: 3,
    type: 'Outputs',
    description: 'Mailmeteor merge data for outreach',
    synthesis: 'The megaphone. Connects our database segments to the actual people who attend.',
    connections: ['members'],
    platform: 'Mailmeteor',
    lifecycle: 'Seasonal',
    risk: 'Low',
    schema: ['Campaign Name', 'Segment', 'Send Date', 'Open Rate']
  },

  // RESILIENCE
  {
    id: 'routing_rules',
    label: 'Routing Rules',
    ring: 4,
    type: 'Resilience',
    description: 'Where does this go?',
    synthesis: 'Encodes routing knowledge in data, not in someone\'s head. Replaces "ask Garen" as the routing table.',
    connections: ['integration_registry'],
    platform: 'GitHub',
    lifecycle: 'Year-over-year',
    risk: 'Low',
    schema: ['Rule ID', 'Source', 'Destination', 'Logic']
  },
  {
    id: 'integration_registry',
    label: 'Integration Registry',
    ring: 4,
    type: 'Resilience',
    description: 'Every script and sync documented',
    synthesis: 'Owner, schedule, failure mode, last successful run. The map of the plumbing.',
    connections: ['routing_rules'],
    platform: 'Airtable',
    lifecycle: 'Year-over-year',
    risk: 'Low',
    schema: ['Integration Name', 'Owner', 'Schedule', 'Last Run']
  },
  {
    id: 'seasons',
    label: 'Seasons',
    ring: 4,
    type: 'Resilience',
    description: 'Year/edition records for cross-season reporting',
    synthesis: 'The long view. Allows us to compare performance across different festival editions.',
    connections: ['merged_timeline'],
    platform: 'Airtable',
    lifecycle: 'Year-over-year',
    risk: 'Low',
    schema: ['Season Year', 'Start Date', 'End Date', 'Budget']
  },
  {
    id: 'decision_log',
    label: 'Decision Log',
    ring: 4,
    type: 'Resilience',
    description: 'Architecture decisions captured in git',
    synthesis: 'Why things are the way they are. When someone asks "why did we do it this way?" — this answers.',
    connections: ['routing_rules'],
    platform: 'GitHub',
    lifecycle: 'Year-over-year',
    risk: 'Medium',
    schema: ['Decision ID', 'Date', 'Author', 'Context', 'Outcome']
  },
];

export const PLATFORMS_DATA = [
  { name: 'Airtable', access: 'centralized' },
  { name: 'Google Sheets', access: 'shared' },
  { name: 'Google Drive', access: 'centralized' },
  { name: 'Eventbrite', access: 'centralized' },
  { name: 'Google Forms', access: 'centralized' },
  { name: 'Mailchimp/Mailmeteor', access: 'centralized' },
  { name: 'Cloudflare Pages', access: 'personal' },
  { name: 'GitHub', access: 'personal' },
  { name: 'Vimeo', access: 'centralized' },
];

export const TIMELINE_DATA = [
  { phase: 'Off-season', period: 'May-Oct', current: false },
  { phase: 'Planning', period: 'Nov-Jan', current: false },
  { phase: 'Build-out', period: 'Feb-Mar', current: true },
  { phase: 'Crunch', period: 'Apr 1-21', current: false },
  { phase: 'Festival', period: 'Apr 22-27', current: false },
  { phase: 'Wind-down', period: 'Apr 28-May', current: false },
];

export const ROLES_DATA = [
  {
    role: 'Executive Director',
    creates: ['Seasons', 'Decision Log'],
    edits: ['Sponsors', 'Directory'],
    reads: ['All']
  },
  {
    role: 'Technical Coordinator',
    creates: ['Host Helper 2026', 'Integration Registry', 'Routing Rules'],
    edits: ['Assets', 'Deliverables', 'Packet QA'],
    reads: ['All']
  },
  {
    role: 'Host Comms Coordinator',
    creates: ['Host Confirmations', 'Comms Log'],
    edits: ['Host Intake', 'Venues'],
    reads: ['Events', 'Directory']
  },
  {
    role: 'Digital Communications',
    creates: ['Email Campaigns', 'Host Helper Pages'],
    edits: ['Event Media Assets'],
    reads: ['Members', 'Events']
  },
  {
    role: 'Creative Assets',
    creates: ['Event Media Assets'],
    edits: ['Assets', 'Asset Versions'],
    reads: ['Films', 'Events']
  },
  {
    role: 'Development',
    creates: ['Sponsors'],
    edits: ['Directory'],
    reads: ['Events']
  },
  {
    role: 'Marketing/Creative',
    creates: ['Email Campaigns'],
    edits: ['Event Media Assets'],
    reads: ['All']
  }
];
