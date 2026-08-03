from typing import Dict, Optional, List
from .models import Chart, DataDescriptor, ChartOptions

charts: Dict[str, Chart] = {}
next_id: int = 1

def generate_id() -> str:
    global next_id
    id_str = f"chart-{next_id}"
    next_id += 1
    return id_str

def create_chart(chart_type: str, data: DataDescriptor, options: ChartOptions) -> Chart:
    chart_id = generate_id()
    chart = Chart(id=chart_id, type=chart_type, data=data, options=options)
    charts[chart_id] = chart
    return chart

def get_chart(chart_id: str) -> Optional[Chart]:
    return charts.get(chart_id)

def update_chart(chart_id: str, options: ChartOptions) -> bool:
    if chart_id in charts:
        charts[chart_id].options = options
        return True
    return False

def update_chart_data(chart_id: str, data: DataDescriptor) -> bool:
    if chart_id in charts:
        charts[chart_id].data = data
        return True
    return False

def destroy_chart(chart_id: str) -> bool:
    if chart_id in charts:
        del charts[chart_id]
        return True
    return False

def get_supported_types() -> List[str]:
    return [
        "line", "scatter", "bar", "heatmap", "pie", 
        "histogram", "boxplot", "surface", "mesh", "contour"
    ]
