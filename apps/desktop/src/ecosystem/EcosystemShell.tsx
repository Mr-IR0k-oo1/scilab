'use client';

import { useState, useRef, useEffect } from 'react';
import type { FOSSEEToolId, FOSSEEProject } from '@/ecosystem/types';
import { FOSSEE_TOOLS } from '@/ecosystem/ToolRegistry';
import { createProject } from '@/ecosystem/ProjectFormat';
import { Button } from '@/components/ui/button';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

function RevealChars({ text }: { text: string }) {
  return Array.from(text).map((char, i) => (
    <span key={i} className="reveal-char inline" style={{ opacity: 0.08 }}>{char}</span>
  ));
}

interface EcosystemShellProps {
  onEnterProject: (project: FOSSEEProject) => void;
}

const RECENT_PROJECTS: { name: string; tools: FOSSEEToolId[]; date: string }[] = [
  { name: 'CampusEnergy', tools: ['scilab', 'xcos'], date: '2026-07-28' },
  { name: 'ControlLab', tools: ['scilab', 'openmodelica'], date: '2026-07-25' },
  { name: 'CircuitSim', tools: ['esim', 'scilab'], date: '2026-07-20' },
];

const TOOLS_LIST = Object.values(FOSSEE_TOOLS);

const TESTIMONIALS = [
  { text: 'FOSSEE transformed how our lab teaches control systems. The Scilab integration is seamless.', author: 'Dr. Anjali Mehta', role: 'Professor, IIT Bombay' },
  { text: 'We migrated our entire circuit design curriculum to eSim. Zero licensing costs, better outcomes.', author: 'Rajesh Kumar', role: 'HoD, NIT Trichy' },
  { text: 'Xcos replaced Simulink for our dynamic systems course. Students adapt within a week.', author: 'Prof. S. Venkatesh', role: 'IISc Bangalore' },
];

const WORKFLOW_STEPS = [
  { num: '01', title: 'Choose Your Tools', desc: 'Select from Scilab, Xcos, eSim, or OpenModelica. Combine them in a single project workspace.', img: 'tools' },
  { num: '02', title: 'Build or Import', desc: 'Write scripts in the editor, drag-and-drop block diagrams in Xcos, or import existing circuit schematics into eSim.', img: 'build' },
  { num: '03', title: 'Simulate & Analyze', desc: 'Run simulations with the Scilab backend. Visualize results with charts, data tables, and interactive plots.', img: 'analyze' },
  { num: '04', title: 'Share & Export', desc: 'Export reports with embedded charts, publish GUI apps, or share your project as a .fossee bundle.', img: 'share' },
];

const FEATURES = [
  { icon: '+', title: 'Multi-Tool Projects', desc: 'Combine Scilab, Xcos, eSim, and OpenModelica in a single project. Each tool gets its own module space.' },
  { icon: '#', title: 'Script Editor', desc: 'Full-featured code editor with syntax highlighting, inline execution, and Scilab output in the console panel.' },
  { icon: '~', title: 'Data Pipeline', desc: 'Import CSV, Excel, or JSON. Clean, transform, and analyze data with a visual pipeline builder.' },
  { icon: '^', title: 'Visualization Studio', desc: 'Line charts, bar graphs, scatter plots, histograms, gauges, and donut charts. Export to PNG or SVG.' },
  { icon: '=', title: 'GUI Builder', desc: 'Drag-and-drop interface for building Scilab GUI applications with buttons, sliders, plots, and labels.' },
  { icon: '/', title: 'Report Generator', desc: 'Assemble reports with live headings, paragraphs, embedded charts, tables, and code blocks.' },
];

const PARTNERS = ['IIT Bombay', 'IIT Delhi', 'IIT Madras', 'NIT Trichy', 'NIT Surathkal', 'IISc Bangalore', 'DTU Delhi', 'COEP Pune', 'VNIT Nagpur', 'IIIT Hyderabad'];

export default function EcosystemShell({ onEnterProject }: EcosystemShellProps) {
  const router = useRouter();
  const [newName, setNewName] = useState('');
  const [selectedTools, setSelectedTools] = useState<FOSSEEToolId[]>(['scilab']);
  const [activeTestimonial, setActiveTestimonial] = useState(0);
  const [partnerPos, setPartnerPos] = useState(0);
  const [recentList] = useState(RECENT_PROJECTS);
  const [showNewProject, setShowNewProject] = useState(false);
  const [countVals, setCountVals] = useState({ tools: 0, partners: 0, students: 0, labs: 0 });
  const nameInputRef = useRef<HTMLInputElement>(null);
  const heroRef = useRef<HTMLDivElement>(null);
  const ctaRef = useRef<HTMLDivElement>(null);
  const ctaTitleRef = useRef<HTMLHeadingElement>(null);
  const cardsRef = useRef<HTMLDivElement>(null);
  const workflowRef = useRef<HTMLDivElement>(null);
  const featuresRef = useRef<HTMLDivElement>(null);
  const statsRef = useRef<HTMLDivElement>(null);
  const partnerScrollRef = useRef<HTMLDivElement>(null);
  const stepsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    document.body.style.overflow = 'auto';
    document.documentElement.style.overflow = 'auto';
    document.documentElement.style.scrollBehavior = 'smooth';
    return () => {
      document.body.style.overflow = '';
      document.documentElement.style.overflow = '';
      document.documentElement.style.scrollBehavior = '';
    };
  }, []);

  useEffect(() => {
    const ctx = gsap.context(() => {
      document.querySelectorAll('.reveal-title').forEach((el) => {
        const chars = el.querySelectorAll('.reveal-char');
        if (!chars.length) return;
        ScrollTrigger.create({
          trigger: el,
          start: 'top 78%',
          end: 'bottom 22%',
          onUpdate: (self) => {
            chars.forEach((c, i) => {
              const progress = (self.progress - i / chars.length) * chars.length;
              (c as HTMLElement).style.opacity = String(Math.min(1, Math.max(0.08, progress)));
            });
          },
        });
      });

      if (ctaTitleRef.current) {
        const chars = ctaTitleRef.current.querySelectorAll('.reveal-char');
        ScrollTrigger.create({
          trigger: ctaTitleRef.current,
          start: 'top 85%',
          end: 'top 60%',
          onUpdate: (self) => {
            chars.forEach((c, i) => {
              const progress = (self.progress - i / chars.length) * chars.length;
              (c as HTMLElement).style.opacity = String(Math.min(1, Math.max(0.08, progress)));
            });
          },
        });
      }

      if (cardsRef.current) {
        const cards = cardsRef.current.querySelectorAll('.stack-card');
        cards.forEach((card, i) => {
          if (i === 0) return;
          gsap.set(card, { y: 40 * i, scale: 1 - i * 0.03, opacity: 1 - i * 0.15 });
          ScrollTrigger.create({
            trigger: cardsRef.current,
            start: `top+=${i * 300} 80%`,
            end: `top+=${i * 300 + 200} 60%`,
            onUpdate: (self) => {
              const p = self.progress;
              gsap.to(card, { y: 40 * i * (1 - p), scale: (1 - i * 0.03) + p * i * 0.03, opacity: (1 - i * 0.15) + p * i * 0.15, duration: 0.1, overwrite: 'auto' });
            },
          });
        });
      }

      if (heroRef.current) {
        gsap.from(heroRef.current.querySelectorAll('.hero-anim'), { y: 60, opacity: 0, duration: 1, stagger: 0.15, ease: 'power3.out' });
      }

      if (ctaRef.current) {
        gsap.from(ctaRef.current.querySelectorAll('.cta-anim'), { y: 40, opacity: 0, duration: 0.8, stagger: 0.1, scrollTrigger: { trigger: ctaRef.current, start: 'top 80%' } });
      }

      if (featuresRef.current) {
        gsap.from(featuresRef.current.querySelectorAll('.feat-card'), { y: 60, opacity: 0, duration: 0.7, stagger: 0.08, scrollTrigger: { trigger: featuresRef.current, start: 'top 75%' } });
      }

      if (workflowRef.current) {
        gsap.from(workflowRef.current.querySelectorAll('.step-card'), { x: -60, opacity: 0, duration: 0.6, stagger: 0.15, scrollTrigger: { trigger: workflowRef.current, start: 'top 70%' } });
      }
    });
    return () => ctx.revert();
  }, []);

  useEffect(() => {
    const t = setInterval(() => setActiveTestimonial((prev) => (prev + 1) % TESTIMONIALS.length), 5000);
    return () => clearInterval(t);
  }, []);

  useEffect(() => {
    let frame: number;
    const animate = () => {
      setPartnerPos((prev) => (prev < -50 ? 0 : prev - 0.04));
      frame = requestAnimationFrame(animate);
    };
    frame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frame);
  }, []);

  useEffect(() => {
    if (showNewProject && nameInputRef.current) nameInputRef.current.focus();
  }, [showNewProject]);

  useEffect(() => {
    if (!statsRef.current) return;
    const targets = { tools: 4, partners: 100, students: 500, labs: 2000 };
    ScrollTrigger.create({
      trigger: statsRef.current,
      start: 'top 80%',
      onEnter: () => {
        gsap.to(countVals, {
          ...targets, duration: 2, ease: 'power2.out', overwrite: 'auto',
          onUpdate: () => setCountVals({
            tools: Math.floor(countVals.tools + (targets.tools - countVals.tools) * 0.1),
            partners: Math.floor(countVals.partners + (targets.partners - countVals.partners) * 0.1),
            students: Math.floor(countVals.students + (targets.students - countVals.students) * 0.1),
            labs: Math.floor(countVals.labs + (targets.labs - countVals.labs) * 0.1),
          }),
        });
      },
      once: true,
    });
  }, []);

  const toggleTool = (id: FOSSEEToolId) => setSelectedTools((prev) => prev.includes(id) ? prev.filter((t) => t !== id) : [...prev, id]);
  const handleCreate = () => { if (newName.trim()) onEnterProject(createProject(newName.trim(), selectedTools)); };
  const handleOpen = (name: string) => { const p = recentList.find((rp) => rp.name === name); onEnterProject(createProject(name, p?.tools ?? ['scilab'])); };

  return (
    <main className="overflow-x-hidden w-full max-w-full bg-background text-foreground min-h-screen font-sans">
      {/* Navigation */}
      <nav className="fixed top-4 left-1/2 -translate-x-1/2 z-50 flex items-center gap-5 px-5 py-2.5 bg-card/80 backdrop-blur-xl border border-border rounded-full">
        <span className="text-sm font-semibold tracking-[0.15em]">FOSSEE</span>
        <span className="w-px h-3.5 bg-border" />
        <a href="#tools" className="text-xs text-muted-foreground hover:text-foreground transition-colors tracking-wide">Tools</a>
        <a href="#workflow" className="text-xs text-muted-foreground hover:text-foreground transition-colors tracking-wide">Workflow</a>
        <a href="#features" className="text-xs text-muted-foreground hover:text-foreground transition-colors tracking-wide">Features</a>
        <a href="#partners" className="text-xs text-muted-foreground hover:text-foreground transition-colors tracking-wide">Partners</a>
        <Button size="sm" className="rounded-full h-7 px-4 text-xs" onClick={() => setShowNewProject(true)}>+ New</Button>
      </nav>

      {/* HERO: Editorial Split */}
      <section ref={heroRef} className="relative min-h-screen flex items-center border-b border-border">
        <div className="max-w-7xl mx-auto w-full px-6 grid md:grid-cols-2 gap-12 md:gap-0 items-center">
          <div className="relative z-10 md:pr-12">
            <p className="text-xs text-muted-foreground tracking-[0.15em] mb-6 hero-anim">FOSSEE PLATFORM</p>
            <h1 className="text-[clamp(2.5rem,4vw,4.5rem)] font-bold leading-[1.1] tracking-tight hero-anim max-w-6xl">
              Engineering{' '}
              <span className="inline-block w-20 h-8 md:w-28 md:h-10 rounded-full align-middle mx-2 bg-cover bg-center opacity-90 contrast-125 grayscale"
                    style={{ backgroundImage: 'url(https://picsum.photos/seed/engineering/400/200)' }} />
              {' '}simulation{' '}
              <span className="inline-block w-16 h-8 md:w-24 md:h-10 rounded-full align-middle mx-2 bg-cover bg-center opacity-90 contrast-125 grayscale"
                    style={{ backgroundImage: 'url(https://picsum.photos/seed/circuit/400/200)' }} />
              {' '}for everyone.
            </h1>
            <p className="text-sm md:text-base text-muted-foreground/70 mt-6 max-w-md leading-relaxed hero-anim">
              Free and Open Source Software in Education. A unified platform for simulation, modeling, and analysis across Scilab, Xcos, eSim, and OpenModelica.
            </p>
            <div className="flex gap-3 mt-8 hero-anim">
              <Button size="lg" className="rounded-full px-8" onClick={() => setShowNewProject(true)}>Start Building</Button>
              <Button variant="outline" size="lg" className="rounded-full px-8 text-foreground border-border hover:border-primary" onClick={() => document.querySelector('main')?.scrollTo({ top: 99999, behavior: 'smooth' })}>Recent Work</Button>
            </div>
          </div>
          <div className="relative md:h-[70vh] hero-anim overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-l from-transparent via-background/60 to-background z-[1]" />
            <div className="w-full h-full min-h-[50vh] md:min-h-full bg-cover bg-center grayscale contrast-125"
                 style={{ backgroundImage: 'url(https://picsum.photos/seed/lab/1200/1600)' }} />
          </div>
        </div>
      </section>

      {/* HOW IT WORKS: Pinned horizontal workflow */}
      <section id="workflow" ref={workflowRef} className="py-32 md:py-48 px-6 border-b border-border">
        <div className="max-w-7xl mx-auto w-full">
          <div className="mb-16">
            <p className="text-xs text-muted-foreground tracking-[0.15em] mb-4">FROM START TO SIMULATION</p>
            <h2 className="reveal-title text-[clamp(2rem,3.5vw,3.5rem)] font-bold leading-[1.15] tracking-tight max-w-3xl">
              <RevealChars text="Four steps to your first engineering project." />
            </h2>
          </div>

          <div ref={stepsRef} className="grid md:grid-cols-4 gap-px bg-border">
            {WORKFLOW_STEPS.map((step) => (
              <div key={step.num} className="step-card bg-card p-8 md:p-10 flex flex-col relative overflow-hidden group min-h-[320px]">
                <div className="absolute inset-0 bg-cover bg-center opacity-15 grayscale transition-all duration-700 group-hover:scale-105 group-hover:opacity-30"
                     style={{ backgroundImage: `url(https://picsum.photos/seed/${step.img}/600/800)` }} />
                <div className="absolute inset-0 bg-gradient-to-t from-card via-card/80 to-card/40" />
                <div className="relative z-[1] mt-auto">
                  <span className="text-4xl font-bold text-primary/20 block mb-3 font-mono">{step.num}</span>
                  <h3 className="text-lg font-bold mb-2">{step.title}</h3>
                  <p className="text-sm text-muted-foreground/70 leading-relaxed">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* TOOLS BENTO: Detailed tool showcase */}
      <section id="tools" className="py-32 md:py-48 px-6 border-b border-border">
        <div className="max-w-7xl mx-auto w-full">
          <div className="mb-16 max-w-3xl">
            <p className="text-xs text-muted-foreground tracking-[0.15em] mb-4">FOUR TOOLS. ONE WORKSPACE.</p>
            <h2 className="reveal-title text-[clamp(2rem,3.5vw,3.5rem)] font-bold leading-[1.15] tracking-tight">
              {Array.from('Everything you need to model, simulate, and analyze.').map((char, i) => (
                <span key={i} className="reveal-char inline" style={{ opacity: 0.08 }}>{char}</span>
              ))}
            </h2>
          </div>

          <div className="grid grid-cols-3 grid-flow-dense gap-px bg-border auto-rows-[240px]">
            <div onClick={() => { setSelectedTools(['scilab']); setShowNewProject(true); }}
              className="col-span-3 md:col-span-2 md:row-span-2 bg-card p-8 flex flex-col justify-end relative overflow-hidden group cursor-pointer">
              <div className="absolute inset-0 bg-cover bg-center opacity-30 grayscale transition-all duration-700 group-hover:scale-105 group-hover:opacity-50"
                   style={{ backgroundImage: 'url(https://picsum.photos/seed/scilab/800/600)' }} />
              <div className="absolute inset-0 bg-gradient-to-t from-card via-card/60 to-transparent" />
              <div className="relative z-[1]">
                <p className="text-3xl mb-2 font-mono text-muted-foreground/50">{FOSSEE_TOOLS.scilab.icon}</p>
                <h3 className="text-xl font-bold mb-1">{FOSSEE_TOOLS.scilab.name}</h3>
                <p className="text-sm text-muted-foreground/70 max-w-md">{FOSSEE_TOOLS.scilab.description}</p>
              </div>
            </div>
            <div onClick={() => { setSelectedTools(['xcos']); setShowNewProject(true); }}
              className="col-span-3 md:col-span-1 md:row-span-1 bg-card p-6 flex flex-col justify-end relative overflow-hidden group cursor-pointer">
              <div className="absolute inset-0 bg-cover bg-center opacity-20 grayscale transition-all duration-700 group-hover:scale-105 group-hover:opacity-40"
                   style={{ backgroundImage: 'url(https://picsum.photos/seed/dynamics/400/300)' }} />
              <div className="absolute inset-0 bg-gradient-to-t from-card via-card/60 to-transparent" />
              <div className="relative z-[1]">
                <p className="text-xl mb-1 font-mono text-muted-foreground/50">{FOSSEE_TOOLS.xcos.icon}</p>
                <h3 className="text-base font-bold">{FOSSEE_TOOLS.xcos.name}</h3>
                <p className="text-xs text-muted-foreground/70 mt-1">{FOSSEE_TOOLS.xcos.tagline}</p>
              </div>
            </div>
            <div onClick={() => { setSelectedTools(['esim', 'openmodelica']); setShowNewProject(true); }}
              className="col-span-3 md:col-span-1 md:row-span-1 bg-card p-6 flex flex-col relative overflow-hidden group cursor-pointer">
              <div className="absolute inset-0 bg-cover bg-center opacity-20 grayscale transition-all duration-700 group-hover:scale-105 group-hover:opacity-40"
                   style={{ backgroundImage: 'url(https://picsum.photos/seed/circuits/400/300)' }} />
              <div className="absolute inset-0 bg-gradient-to-t from-card via-card/60 to-transparent" />
              <div className="relative z-[1] mt-auto">
                <div className="flex gap-3 mb-2">
                  <span className="font-mono text-lg text-muted-foreground/50">{FOSSEE_TOOLS.esim.icon}</span>
                  <span className="font-mono text-lg text-muted-foreground/50">{FOSSEE_TOOLS.openmodelica.icon}</span>
                </div>
                <h3 className="text-base font-bold">eSim + OpenModelica</h3>
                <p className="text-xs text-muted-foreground/70 mt-1">Circuit design & physical system modeling</p>
              </div>
            </div>
            <div className="col-span-3 bg-card p-8 relative overflow-hidden">
              <p className="text-[10px] text-muted-foreground/40 tracking-[0.15em] mb-6 font-semibold">INTEGRATED TOOLS</p>
              <div className="grid grid-cols-4 gap-px bg-border">
                {Object.values(FOSSEE_TOOLS).map((tool) => (
                  <div key={tool.id} onClick={() => { setSelectedTools([tool.id]); setShowNewProject(true); }}
                    className="bg-card p-5 flex flex-col items-center justify-center gap-3 relative overflow-hidden group/tool min-h-[110px] cursor-pointer">
                    <div className="absolute inset-0 bg-gradient-to-b from-transparent to-card pointer-events-none" />
                    <span className="text-2xl font-mono transition-all duration-500 group-hover/tool:scale-125 group-hover/tool:opacity-100 relative z-[1]"
                          style={{ color: tool.color, opacity: 0.7 }}>
                      {tool.icon}
                    </span>
                    <span className="text-[11px] text-muted-foreground/40 font-semibold tracking-wide relative z-[1] group-hover/tool:text-foreground/70 transition-colors duration-300">{tool.name}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-3 grid-flow-dense gap-px bg-border mt-px auto-rows-[140px]">
            {[
              { value: '4', label: 'Open Tools', img: 'tools', wide: false },
              { value: '100+', label: 'University Partners', img: 'campus', wide: true },
              { value: 'Zero', label: 'Licensing Cost', img: 'zero', wide: false },
            ].map((s, i) => (
              <div key={i} className={`bg-card p-6 flex items-center justify-center relative overflow-hidden group ${s.wide ? 'col-span-2' : 'col-span-1'}`}>
                <div className="absolute inset-0 bg-cover bg-center opacity-10 grayscale transition-all duration-700 group-hover:scale-105 group-hover:opacity-20"
                     style={{ backgroundImage: `url(https://picsum.photos/seed/${s.img}/400/200)` }} />
                <div className="absolute inset-0 bg-gradient-to-r from-card/60 via-card/30 to-card/60" />
                <div className="relative z-[1] text-center">
                  <p className="text-2xl font-bold text-primary">{s.value}</p>
                  <p className="text-xs text-muted-foreground/70 mt-1 tracking-wide">{s.label}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FEATURES: Gapless bento capabilities grid */}
      <section id="features" ref={featuresRef} className="py-32 md:py-48 px-6 border-b border-border">
        <div className="max-w-7xl mx-auto w-full">
          <div className="mb-16 max-w-3xl">
            <p className="text-xs text-muted-foreground tracking-[0.15em] mb-4">CAPABILITIES</p>
            <h2 className="reveal-title text-[clamp(2rem,3.5vw,3.5rem)] font-bold leading-[1.15] tracking-tight">
              <RevealChars text="Everything you need, nothing you do not." />
            </h2>
            <p className="text-sm text-muted-foreground/70 mt-4 max-w-xl leading-relaxed">
              Six integrated modules that work together across all four tools. No plugins, no separate installs.
            </p>
          </div>

          <div className="grid grid-cols-3 grid-flow-dense gap-px bg-border auto-rows-[220px]">
            {FEATURES.map((feat, i) => {
              const isWide = i === 0 || i === 5;
              const isTall = i === 2;
              return (
                <div key={i} className={`feat-card bg-card p-8 flex flex-col justify-end relative overflow-hidden group cursor-default ${
                  isWide ? 'col-span-2' : 'col-span-1'
                } ${isTall ? 'row-span-2' : 'row-span-1'}`}>
                  <div className="absolute inset-0 bg-cover bg-center opacity-15 grayscale transition-all duration-700 group-hover:scale-105 group-hover:opacity-30"
                       style={{ backgroundImage: `url(https://picsum.photos/seed/feat${i}/600/500)` }} />
                  <div className="absolute inset-0 bg-gradient-to-t from-card via-card/80 to-card/30" />
                  <div className="relative z-[1]">
                    <span className="text-xl font-mono text-primary mb-3 block">{feat.icon}</span>
                    <h3 className="text-base font-bold mb-1.5">{feat.title}</h3>
                    <p className="text-sm text-muted-foreground/70 leading-relaxed">{feat.desc}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* IMPACT STATS: Animated counters in bento layout */}
      <section ref={statsRef} className="py-32 md:py-48 px-6 border-b border-border">
        <div className="max-w-7xl mx-auto w-full">
          <div className="mb-16 text-center">
            <p className="text-xs text-muted-foreground tracking-[0.15em] mb-4">OUR REACH</p>
            <h2 className="reveal-title text-[clamp(2rem,3.5vw,3.5rem)] font-bold leading-[1.15] tracking-tight">
              <RevealChars text="Growing the open engineering community." />
            </h2>
          </div>

          <div className="grid grid-cols-4 grid-flow-dense gap-px bg-border auto-rows-[180px]">
            {[
              { val: countVals.tools, suffix: '', label: 'Open Source Tools', wide: false, tall: false },
              { val: countVals.partners, suffix: '+', label: 'University Partners', wide: true, tall: false },
              { val: countVals.students, suffix: 'K+', label: 'Students Reached', wide: false, tall: false },
              { val: countVals.labs, suffix: '+', label: 'Lab Installations', wide: true, tall: false },
            ].map((s, i) => (
              <div key={i} className={`bg-card p-10 flex flex-col items-center justify-center relative overflow-hidden group ${
                s.wide ? 'col-span-2' : 'col-span-1'
              } ${s.tall ? 'row-span-2' : 'row-span-1'}`}>
                <div className="absolute inset-0 bg-gradient-to-br from-primary/[0.02] to-transparent group-hover:from-primary/[0.04] transition-all duration-700" />
                <p className="text-4xl md:text-5xl font-bold text-primary tabular-nums relative z-[1]">
                  {s.val}{s.suffix}
                </p>
                <p className="text-xs text-muted-foreground/70 mt-3 tracking-wide relative z-[1]">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* UNIVERSITY PARTNERS: Infinite marquee */}
      <section id="partners" className="py-24 md:py-32 px-6 border-b border-border">
        <div className="max-w-7xl mx-auto w-full">
          <div className="mb-12 text-center">
            <p className="text-xs text-muted-foreground tracking-[0.15em] mb-4">TRUSTED BY</p>
            <h2 className="reveal-title text-[clamp(1.5rem,2.5vw,2.5rem)] font-bold leading-[1.15] tracking-tight">
              <RevealChars text="India's top engineering institutions use FOSSEE." />
            </h2>
          </div>

          <div className="overflow-hidden">
            <div className="flex gap-16 items-center" style={{ transform: `translateX(${partnerPos}%)`, whiteSpace: 'nowrap' }}>
              {[...PARTNERS, ...PARTNERS, ...PARTNERS].map((name, i) => (
                <span key={i} className="inline-block text-sm text-muted-foreground/30 font-semibold tracking-wide">{name}</span>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CARD STACKING + TESTIMONIALS: Desire section */}
      <section className="py-32 md:py-48 px-6 border-b border-border">
        <div className="max-w-7xl mx-auto w-full">
          <div className="mb-16">
            <p className="text-xs text-muted-foreground tracking-[0.15em] mb-4">TRUSTED BY ENGINEERS</p>
            <h2 className="reveal-title text-[clamp(2rem,3.5vw,3.5rem)] font-bold leading-[1.15] tracking-tight max-w-3xl">
              <RevealChars text="Used in classrooms and labs across India." />
            </h2>
          </div>

          <div ref={cardsRef} className="relative min-h-[600px] mb-32">
            {[
              { title: 'Curriculum Aligned', desc: 'Covers B.Tech and M.Tech lab syllabi for electrical, electronics, and mechanical engineering.', img: 'curriculum' },
              { title: 'Zero License Cost', desc: 'Every tool is fully open source. No per-seat fees, no vendor lock-in, no renewal surprises.', img: 'opensource' },
              { title: 'Active Community', desc: 'Backed by IIT Bombay and a growing community of educators contributing examples and modules.', img: 'community' },
            ].map((item, i) => (
              <div key={i} className="stack-card relative bg-card border border-border p-8 md:p-12 flex items-center gap-8 md:gap-16 mb-4"
                   style={{ zIndex: 3 - i }}>
                <div className="flex-1 min-w-0">
                  <span className="text-2xl font-mono text-muted-foreground/20 mb-2 block">0{i + 1}</span>
                  <h3 className="text-xl font-bold mb-3">{item.title}</h3>
                  <p className="text-sm text-muted-foreground/70 leading-relaxed max-w-md">{item.desc}</p>
                </div>
                <div className="w-40 h-40 md:w-56 md:h-56 shrink-0 bg-cover bg-center grayscale contrast-125 rounded-sm opacity-80"
                     style={{ backgroundImage: `url(https://picsum.photos/seed/${item.img}/400/400)` }} />
              </div>
            ))}
          </div>

          {/* Testimonial Carousel */}
          <div className="bg-card border border-border p-8 md:p-12">
            <div className="max-w-2xl mx-auto text-center">
              <div className="flex justify-center -space-x-2 mb-8">
                {TESTIMONIALS.map((_, i) => (
                  <div key={i} className={`w-12 h-12 rounded-full bg-cover bg-center grayscale border-2 border-background transition-all duration-500 ${
                    i === activeTestimonial ? 'opacity-100 scale-110' : 'opacity-50 scale-90'
                  }`}
                       style={{ backgroundImage: `url(https://picsum.photos/seed/person${i}/200/200)` }} />
                ))}
              </div>
              <p className="text-base md:text-lg text-foreground/80 leading-relaxed mb-6 min-h-[80px] transition-opacity duration-500">
                &ldquo;{TESTIMONIALS[activeTestimonial].text}&rdquo;
              </p>
              <p className="text-sm font-semibold">{TESTIMONIALS[activeTestimonial].author}</p>
              <p className="text-xs text-muted-foreground/70">{TESTIMONIALS[activeTestimonial].role}</p>
              <div className="flex justify-center gap-2 mt-6">
                {TESTIMONIALS.map((_, i) => (
                  <button key={i} onClick={() => setActiveTestimonial(i)}
                          className={`w-2 h-2 rounded-full transition-all duration-300 ${
                            i === activeTestimonial ? 'bg-primary w-6' : 'bg-border'
                          }`} />
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* RECENT PROJECTS */}
      <section className="py-32 md:py-48 px-6 border-b border-border">
        <div className="max-w-7xl mx-auto w-full">
          <div className="mb-12">
            <p className="text-xs text-muted-foreground tracking-[0.15em] mb-4">YOUR WORK</p>
            <h2 className="reveal-title text-[clamp(2rem,3.5vw,3.5rem)] font-bold leading-[1.15] tracking-tight max-w-3xl">
              <RevealChars text="Recent projects." />
            </h2>
          </div>

          <div className="grid grid-cols-3 grid-flow-dense gap-px bg-border auto-rows-[240px]">
            {recentList.map((p, i) => (
              <div key={p.name} onClick={() => handleOpen(p.name)}
                className={`bg-card p-8 flex flex-col relative overflow-hidden group cursor-pointer ${
                  i === 0 ? 'col-span-2 row-span-2' : 'col-span-1 row-span-1'
                }`}>
                <div className="absolute inset-0 bg-cover bg-center opacity-20 grayscale transition-all duration-700 group-hover:scale-105 group-hover:opacity-35"
                     style={{ backgroundImage: `url(https://picsum.photos/seed/project${i}/600/600)` }} />
                <div className="absolute inset-0 bg-gradient-to-t from-card via-card/70 to-card/20" />
                <div className="relative z-[1] mt-auto">
                  <div className="flex gap-2 text-lg mb-3 font-mono text-muted-foreground/40">
                    {p.tools.slice(0, 2).map((t) => <span key={t}>{FOSSEE_TOOLS[t].icon}</span>)}
                  </div>
                  <h3 className="text-lg font-bold mb-1 group-hover:text-primary transition-colors">{p.name}</h3>
                  <div className="flex gap-1.5 flex-wrap mt-3">
                    {p.tools.map((t) => (
                      <span key={t} className="text-[10px] text-muted-foreground/50 border border-border px-2 py-0.5">{FOSSEE_TOOLS[t].name}</span>
                    ))}
                  </div>
                  <p className="text-[10px] text-muted-foreground/30 mt-3">{p.date}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* RESOURCES / COMMUNITY */}
      <section className="py-32 md:py-48 px-6 border-b border-border">
        <div className="max-w-7xl mx-auto w-full">
          <div className="mb-16 max-w-3xl">
            <p className="text-xs text-muted-foreground tracking-[0.15em] mb-4">RESOURCES</p>
            <h2 className="reveal-title text-[clamp(2rem,3.5vw,3.5rem)] font-bold leading-[1.15] tracking-tight">
              <RevealChars text="Everything you need to get started." />
            </h2>
          </div>

          <div className="grid grid-cols-3 grid-flow-dense gap-px bg-border auto-rows-[280px]">
            {[
              { icon: '/', title: 'Documentation', desc: 'Comprehensive guides for every tool. API references, tutorials, and example projects.', cta: 'Read Docs', img: 'docs', href: '/docs' },
              { icon: '<', title: 'Community Forum', desc: 'Join thousands of educators and engineers. Ask questions, share projects, contribute.', cta: 'Join Forum', img: 'forum', href: '/community' },
              { icon: '>', title: 'GitHub Repository', desc: 'All tools are open source. Fork, contribute, or report issues on GitHub.', cta: 'View on GitHub', img: 'github', href: 'https://github.com/fossee' },
            ].map((res, i) => (
              <div key={i} onClick={() => {
                if (res.href.startsWith('http')) window.open(res.href, '_blank');
                else router.push(res.href);
              }} className={`bg-card p-8 md:p-10 flex flex-col relative overflow-hidden group cursor-pointer ${
                i === 1 ? 'col-span-1 row-span-2' : 'col-span-1 row-span-1'
              }`}>
                <div className="absolute inset-0 bg-cover bg-center opacity-15 grayscale transition-all duration-700 group-hover:scale-105 group-hover:opacity-30"
                     style={{ backgroundImage: `url(https://picsum.photos/seed/${res.img}/600/700)` }} />
                <div className="absolute inset-0 bg-gradient-to-t from-card via-card/80 to-card/30" />
                <div className="relative z-[1] mt-auto">
                  <span className="text-xl font-mono text-muted-foreground/30 mb-3 block">{res.icon}</span>
                  <h3 className="text-lg font-bold mb-2">{res.title}</h3>
                  <p className="text-sm text-muted-foreground/70 leading-relaxed mb-4">{res.desc}</p>
                  <span className="text-xs text-primary group-hover:opacity-100 opacity-70 transition-opacity">{res.cta} &rarr;</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ACTION: High-contrast CTA */}
      <section ref={ctaRef} className="py-32 md:py-48 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <p className="text-xs text-primary tracking-[0.15em] mb-6 cta-anim">GET STARTED</p>
          <h2 ref={ctaTitleRef} className="text-[clamp(2rem,4vw,4rem)] font-bold leading-[1.1] tracking-tight cta-anim">
            <RevealChars text="Ready to build something?" />
          </h2>
          <p className="text-sm md:text-base text-muted-foreground/70 mt-4 max-w-lg mx-auto leading-relaxed cta-anim">
            Create your first project and start simulating circuits, systems, and signals. No license keys required. No credit card.
          </p>
          <div className="flex gap-3 justify-center mt-8 cta-anim">
            <Button size="lg" className="rounded-full px-10 text-base h-12" onClick={() => setShowNewProject(true)}>Create a Project</Button>
            <Button variant="outline" size="lg" className="rounded-full px-10 text-base h-12 border-border text-foreground hover:border-primary" onClick={() => router.push('/community')}>Browse Examples</Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border relative">
        <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent" />

        <div className="pt-24 pb-6 px-6">
          <div className="max-w-7xl mx-auto w-full">

            {/* Top row: brand + columns */}
            <div className="grid md:grid-cols-12 gap-px bg-border mb-16">
              <div className="md:col-span-4 bg-card p-10 md:p-12 flex flex-col relative overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-br from-primary/[0.02] to-transparent pointer-events-none" />
                <span className="text-lg font-bold tracking-[0.15em] mb-5 relative z-[1]">FOSSEE</span>
                <p className="text-xs text-muted-foreground/50 leading-relaxed max-w-xs mb-8 relative z-[1]">
                  Free and Open Source Software in Education. A unified platform for simulation, modeling, and analysis, backed by IIT Bombay.
                </p>
                <div className="flex gap-2 mt-auto relative z-[1]">
                  {[
                    { s: '𝕏', label: 'X', href: 'https://x.com/fossee' },
                    { s: 'in', label: 'LinkedIn', href: 'https://linkedin.com/company/fossee' },
                    { s: '⟨⟩', label: 'GitHub', href: 'https://github.com/fossee' },
                    { s: '✉', label: 'Email', href: 'mailto:contact@fossee.in' },
                  ].map((item) => (
                    <span key={item.label} title={item.label} onClick={() => window.open(item.href, '_blank')}
                      className="w-8 h-8 flex items-center justify-center border border-border text-[11px] text-muted-foreground/40 hover:text-primary hover:border-primary/40 transition-all duration-300 cursor-pointer font-mono">
                      {item.s}
                    </span>
                  ))}
                </div>
              </div>
              <div className="md:col-span-2 bg-card p-10 md:p-12">
                <p className="text-[10px] text-muted-foreground/40 tracking-[0.15em] mb-6 font-semibold">TOOLS</p>
                <div className="flex flex-col gap-2.5">
                  {Object.values(FOSSEE_TOOLS).map((t) => (
                    <span key={t.id} onClick={() => router.push('/docs#' + t.id.toLowerCase())}
                      className="text-xs text-muted-foreground/60 hover:text-foreground transition-all duration-200 cursor-pointer border-l border-transparent hover:border-primary hover:pl-2 pl-0">
                      {t.name}
                    </span>
                  ))}
                </div>
              </div>
              <div className="md:col-span-3 bg-card p-10 md:p-12">
                <p className="text-[10px] text-muted-foreground/40 tracking-[0.15em] mb-6 font-semibold">RESOURCES</p>
                <div className="flex flex-col gap-2.5">
                  {[
                    { label: 'Documentation', meta: 'docs', href: '/docs' },
                    { label: 'API Reference', meta: 'api', href: '/docs#api' },
                    { label: 'Tutorials', meta: 'guides', href: '/docs#tutorials' },
                    { label: 'Example Projects', meta: 'examples', href: '/docs#examples' },
                    { label: 'Community Forum', meta: 'forum', href: '/community' },
                    { label: 'GitHub', meta: 'source', href: 'https://github.com/fossee' },
                  ].map((r) => (
                    <div key={r.label} onClick={() => {
                      if (r.href.startsWith('http')) window.open(r.href, '_blank');
                      else router.push(r.href);
                    }}
                      className="group/link flex items-center justify-between text-xs text-muted-foreground/60 hover:text-foreground transition-all duration-200 cursor-pointer border-l border-transparent hover:border-primary hover:pl-2 pl-0">
                      <span>{r.label}</span>
                      <span className="text-[8px] text-muted-foreground/20 group-hover/link:text-primary/40 transition-colors font-mono">{r.meta}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="md:col-span-3 bg-card p-10 md:p-12">
                <p className="text-[10px] text-muted-foreground/40 tracking-[0.15em] mb-6 font-semibold">COMPANY</p>
                <div className="flex flex-col gap-2.5">
                  {[
                    { label: 'About FOSSEE', meta: 'about', href: '/about' },
                    { label: 'IIT Bombay', meta: '.ac.in', href: 'https://www.iitb.ac.in' },
                    { label: 'Privacy Policy', meta: 'legal', href: '/privacy' },
                    { label: 'Terms of Use', meta: 'legal', href: '/terms' },
                    { label: 'License', meta: 'MIT', href: '/terms#license' },
                    { label: 'Contact', meta: 'email', href: '/contact' },
                  ].map((c) => (
                    <div key={c.label} onClick={() => {
                      if (c.href.startsWith('http')) window.open(c.href, '_blank');
                      else router.push(c.href);
                    }}
                      className="group/link flex items-center justify-between text-xs text-muted-foreground/60 hover:text-foreground transition-all duration-200 cursor-pointer border-l border-transparent hover:border-primary hover:pl-2 pl-0">
                      <span>{c.label}</span>
                      <span className="text-[8px] text-muted-foreground/20 group-hover/link:text-primary/40 transition-colors font-mono">{c.meta}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Divider with decorative dot */}
            <div className="flex items-center gap-3 mb-8">
              <div className="flex-1 h-px bg-border" />
              <div className="w-1.5 h-1.5 rounded-full bg-primary/30" />
              <div className="flex-1 h-px bg-border" />
            </div>

            {/* Bottom bar */}
            <div className="flex flex-col md:flex-row items-center justify-between gap-4">
              <p className="text-[10px] text-muted-foreground/25 tracking-wide">
                &copy; {new Date().getFullYear()} FOSSEE &mdash; Free and Open Source Software in Education
              </p>
              <div className="flex items-center gap-4 text-[10px] text-muted-foreground/25">
                <span onClick={() => router.push('/privacy')} className="hover:text-muted-foreground/60 transition-colors cursor-pointer tracking-wide">Privacy</span>
                <span className="w-px h-3 bg-border" />
                <span onClick={() => router.push('/terms')} className="hover:text-muted-foreground/60 transition-colors cursor-pointer tracking-wide">Terms</span>
                <span className="w-px h-3 bg-border" />
                <span onClick={() => router.push('/terms#license')} className="hover:text-muted-foreground/60 transition-colors cursor-pointer tracking-wide">License</span>
                <span className="w-px h-3 bg-border" />
                <span onClick={() => router.push('/docs')} className="hover:text-muted-foreground/60 transition-colors cursor-pointer tracking-wide">Sitemap</span>
              </div>
            </div>
          </div>
        </div>
      </footer>

      {/* New Project Dialog */}
      {showNewProject && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm" onClick={() => setShowNewProject(false)}>
          <div className="bg-card border border-border p-8 w-full max-w-[400px]" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-lg font-bold mb-6">New Project</h2>
            <div className="space-y-2 mb-5">
              <label className="text-xs text-muted-foreground tracking-wide">Project Name</label>
              <input ref={nameInputRef}
                className="w-full px-3 py-2 bg-background border border-border text-sm text-foreground outline-none focus:border-primary transition-colors"
                placeholder="e.g. CampusEnergy" value={newName}
                onChange={(e) => setNewName(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') handleCreate(); }} maxLength={64} />
              <p className="text-[10px] text-muted-foreground/50 text-right">{newName.length}/64</p>
            </div>
            <div className="space-y-2 mb-6">
              <label className="text-xs text-muted-foreground tracking-wide">Tools</label>
              <div className="flex flex-wrap gap-1.5">
                {Object.values(FOSSEE_TOOLS).map((tool) => {
                  const active = selectedTools.includes(tool.id);
                  return (
                    <button key={tool.id} type="button" onClick={() => toggleTool(tool.id)}
                      className={`inline-flex items-center gap-1.5 px-3 py-1.5 text-xs border transition-colors ${
                        active ? 'bg-primary text-primary-foreground border-primary' : 'bg-transparent text-muted-foreground border-border hover:border-muted-foreground/30'
                      }`}>
                      <span>{tool.icon}</span><span>{tool.name}</span>
                    </button>
                  );
                })}
              </div>
            </div>
            <div className="flex gap-2">
              <Button size="sm" onClick={handleCreate} disabled={!newName.trim()}>Create</Button>
              <Button variant="outline" size="sm" onClick={() => setShowNewProject(false)}>Cancel</Button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
