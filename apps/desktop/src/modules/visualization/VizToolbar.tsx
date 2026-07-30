interface VizToolbarProps {
  chartType: string;
  onChartTypeChange: (type: string) => void;
  chartTypes: { id: string; label: string; icon: string }[];
}

export default function VizToolbar({ chartType, onChartTypeChange, chartTypes }: VizToolbarProps) {
  return (
    <div className="viz-toolbar">
      {chartTypes.map((ct) => (
        <button
          key={ct.id}
          className={`viz-chart-btn ${chartType === ct.id ? 'active' : ''}`}
          onClick={() => onChartTypeChange(ct.id)}
        >
          <span className="viz-chart-icon">{ct.icon}</span>
          <span className="viz-chart-label">{ct.label}</span>
        </button>
      ))}
    </div>
  );
}
