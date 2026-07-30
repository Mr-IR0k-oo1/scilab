interface ExampleCardProps {
  example: {
    id: string;
    title: string;
    category: string;
    difficulty: string;
    duration: string;
    description: string;
  };
  onOpen: () => void;
}

const DIFFICULTY_COLORS: Record<string, string> = {
  Beginner: '#81c784',
  Intermediate: '#ffb74d',
  Advanced: '#ef5350',
};

export default function ExampleCard({ example, onOpen }: ExampleCardProps) {
  return (
    <div className="lc-card">
      <div className="lc-card-header">
        <span className="lc-card-category">{example.category}</span>
        <span className="lc-card-duration">{example.duration}</span>
      </div>
      <h3 className="lc-card-title">{example.title}</h3>
      <p className="lc-card-desc">{example.description}</p>
      <div className="lc-card-footer">
        <span className="lc-card-difficulty" style={{ color: DIFFICULTY_COLORS[example.difficulty] }}>
          {example.difficulty}
        </span>
        <button className="lc-card-btn" onClick={(e) => { e.stopPropagation(); onOpen(); }}>Open</button>
      </div>
    </div>
  );
}
