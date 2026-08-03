import SubPage from './SubPage';

export default function ContactPage() {
  return (
    <SubPage title="Contact">
      <p>
        Have questions, suggestions, or need help? Reach out to the FOSSEE team.
      </p>

      <div className="grid gap-px bg-border mt-8">
        {[
          { label: 'General Inquiries', val: 'contact@fossee.in' },
          { label: 'Technical Support', val: 'support@fossee.in' },
          { label: 'Contributions', val: 'contribute@fossee.in' },
          { label: 'Address', val: 'IIT Bombay, Powai, Mumbai 400076' },
        ].map((s) => (
          <div key={s.label} className="bg-card p-6 flex items-center justify-between border-b border-border last:border-b-0">
            <span className="text-xs text-muted-foreground/70">{s.label}</span>
            <span className="text-xs font-semibold text-foreground/80">{s.val}</span>
          </div>
        ))}
      </div>
    </SubPage>
  );
}
