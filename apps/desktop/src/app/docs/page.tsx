import SubPage from '@/components/SubPage';

export default function DocsPage() {
  return (
    <SubPage title="Documentation">
      <p>
        Comprehensive guides for every tool in the FOSSEE ecosystem. Whether you&apos;re a student setting up
        your first simulation or an instructor designing a lab curriculum, you&apos;ll find everything you need here.
      </p>

      <div className="grid md:grid-cols-2 gap-px bg-border mt-8 mb-8">
        {[
          { title: 'Scilab', desc: 'Getting started, numerical analysis, signal processing, and control systems.' },
          { title: 'Xcos', desc: 'Block diagram modeling, hybrid dynamic systems, and simulation workflows.' },
          { title: 'eSim', desc: 'Circuit design, schematic capture, PCB layout, and SPICE simulation.' },
          { title: 'OpenModelica', desc: 'Modelica language, physical system modeling, and optimization.' },
        ].map((s) => (
          <div key={s.title} className="bg-card p-6">
            <h3 className="text-sm font-bold mb-1.5">{s.title}</h3>
            <p className="text-xs text-muted-foreground/70">{s.desc}</p>
          </div>
        ))}
      </div>

      <h2 className="text-base font-bold mt-8 mb-3">API Reference</h2>
      <p>Complete API documentation for Scilab functions, Xcos blocks, eSim components, and OpenModelica libraries. All endpoints, parameters, and return types are documented with examples.</p>

      <h2 className="text-base font-bold mt-8 mb-3">Tutorials &amp; Guides</h2>
      <p>Step-by-step tutorials covering common engineering workflows: control system design, circuit simulation, data analysis, and report generation. Each tutorial includes sample code and expected output.</p>
    </SubPage>
  );
}
