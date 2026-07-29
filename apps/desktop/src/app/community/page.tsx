import SubPage from '@/components/SubPage';

export default function CommunityPage() {
  return (
    <SubPage title="Community Forum">
      <p>
        Join thousands of educators, engineers, and students using FOSSEE tools. Ask questions,
        share projects, contribute examples, and help shape the future of open engineering education.
      </p>

      <div className="grid gap-px bg-border mt-8">
        {[
          { title: 'Q&A', desc: 'Get help with Scilab scripts, Xcos models, eSim circuits, and OpenModelica simulations.' },
          { title: 'Show & Tell', desc: 'Share your projects, lab exercises, and curriculum materials with the community.' },
          { title: 'Feature Requests', desc: 'Suggest improvements and vote on upcoming features for all FOSSEE tools.' },
          { title: 'Contributors', desc: 'Meet the contributors building and maintaining the FOSSEE ecosystem.' },
        ].map((s) => (
          <div key={s.title} className="bg-card p-6 border-b border-border last:border-b-0">
            <h3 className="text-sm font-bold mb-1.5">{s.title}</h3>
            <p className="text-xs text-muted-foreground/70">{s.desc}</p>
          </div>
        ))}
      </div>
    </SubPage>
  );
}
