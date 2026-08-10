import csv
import io
from typing import Any, Dict, List
from app.visualization.models import ChartDataResponse


class ChartExporter:
    @staticmethod
    def export_to_csv(chart_data: ChartDataResponse) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["series_name", "x", "y", "value"])

        for series in chart_data.series:
            for item in series.data:
                writer.writerow([
                    series.name,
                    item.get("x", ""),
                    item.get("y", ""),
                    item.get("value", ""),
                ])

        return output.getvalue()
