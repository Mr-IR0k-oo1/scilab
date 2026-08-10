import math
from typing import Any, Dict, List, Optional
from app.data.models import DatasetSchema, TransformationPipeline
from app.data.processors.transformer import DataTransformer
from app.visualization.models import ChartDataResponse, ChartSeries, ChartType, VisualizationSpec


class VisualizationDataService:
    MAX_POINTS = 5000

    @staticmethod
    def generate_chart_data(
        spec: VisualizationSpec,
        raw_rows: List[Dict[str, Any]],
        current_hash: str = "",
        stored_hash: str = "",
    ) -> ChartDataResponse:
        # Apply reproducible transformations first
        transformed_rows = DataTransformer.apply_pipeline(raw_rows, spec.transformations)

        sampled = False
        warning = None

        if current_hash and stored_hash and current_hash != stored_hash:
            warning = "Source dataset content hash has changed since this visualization was configured."

        total_rows = len(transformed_rows)
        if total_rows > VisualizationDataService.MAX_POINTS:
            step = math.ceil(total_rows / VisualizationDataService.MAX_POINTS)
            transformed_rows = transformed_rows[::step]
            sampled = True

        series_list: List[ChartSeries] = []

        if spec.type in [ChartType.LINE, ChartType.SCATTER, ChartType.BAR]:
            x_col = spec.x_column or "x"
            for y_col in spec.y_columns:
                series_data = []
                for row in transformed_rows:
                    if x_col in row and y_col in row:
                        series_data.append({
                            "x": row[x_col],
                            "y": row[y_col],
                        })
                series_list.append(ChartSeries(name=y_col, data=series_data))

        elif spec.type == ChartType.HISTOGRAM:
            target_col = spec.x_column or (spec.y_columns[0] if spec.y_columns else None)
            if target_col:
                vals = [float(r[target_col]) for r in transformed_rows if r.get(target_col) is not None and isinstance(r.get(target_col), (int, float))]
                if vals:
                    num_bins = spec.options.bins or 10
                    min_v, max_v = min(vals), max(vals)
                    bin_width = (max_v - min_v) / num_bins if max_v != min_v else 1.0
                    counts = [0] * num_bins
                    for v in vals:
                        idx = int((v - min_v) / bin_width) if bin_width > 0 else 0
                        if idx >= num_bins:
                            idx = num_bins - 1
                        counts[idx] += 1

                    bin_data = []
                    for i in range(num_bins):
                        start = min_v + i * bin_width
                        end = start + bin_width
                        bin_data.append({
                            "x": f"{start:.2f}-{end:.2f}",
                            "y": counts[i],
                        })
                    series_list.append(ChartSeries(name=f"Frequency ({target_col})", data=bin_data))

        elif spec.type == ChartType.HEATMAP:
            x_col = spec.x_column
            y_cols = spec.y_columns
            if x_col and y_cols:
                heatmap_data = []
                for row in transformed_rows:
                    if x_col in row:
                        for y_c in y_cols:
                            if y_c in row and isinstance(row[y_c], (int, float)):
                                heatmap_data.append({
                                    "x": str(row[x_col]),
                                    "y": y_c,
                                    "value": float(row[y_c]),
                                })
                series_list.append(ChartSeries(name="Heatmap Matrix", data=heatmap_data))

        return ChartDataResponse(
            visualization_id=spec.id or "preview",
            type=spec.type,
            series=series_list,
            sample_count=len(transformed_rows),
            sampled=sampled,
            dataset_hash_changed=(current_hash != stored_hash) if (current_hash and stored_hash) else False,
            warning=warning,
        )
