import json
import os
import tempfile
import pytest
from app.data.loaders.csv_loader import CSVDataLoader
from app.data.loaders.json_loader import JSONDataLoader
from app.data.models import TransformationOperation, TransformationPipeline, TransformationType
from app.data.processors.transformer import DataTransformer
from app.data.validators.validator import DatasetValidator
from app.visualization.models import ChartType, VisualizationOptions, VisualizationSpec
from app.visualization.service import VisualizationDataService


def test_csv_loader_and_statistics():
    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w+", delete=False, encoding="utf-8") as f:
        f.write("time,temperature,pressure\n1,25.5,101.3\n2,26.0,101.5\n3,,101.2\n4,28.1,\n")
        f_path = f.name

    try:
        loader = CSVDataLoader()
        schema = loader.inspect_schema(f_path)
        assert schema.format == "csv"
        assert schema.row_count == 4
        assert schema.column_count == 3
        assert "temperature" in schema.numeric_columns
        assert schema.missing_value_count == 2

        # Test Validation
        val_res = DatasetValidator.validate(schema)
        assert val_res.valid is True
        assert len(val_res.warnings) >= 1
    finally:
        if os.path.exists(f_path):
            os.remove(f_path)


def test_json_loader():
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w+", delete=False, encoding="utf-8") as f:
        f.write(json.dumps([
            {"time": 1, "voltage": 5.0},
            {"time": 2, "voltage": 5.1},
            {"time": 3, "voltage": 4.9},
        ]))
        f_path = f.name

    try:
        loader = JSONDataLoader()
        schema = loader.inspect_schema(f_path)
        assert schema.format == "json"
        assert schema.row_count == 3
        assert "voltage" in schema.numeric_columns
    finally:
        if os.path.exists(f_path):
            os.remove(f_path)


def test_data_transformations():
    rows = [
        {"x": 1, "y": 10.0},
        {"x": 2, "y": None},
        {"x": 3, "y": 30.0},
    ]

    pipeline = TransformationPipeline(operations=[
        TransformationOperation(type=TransformationType.DROP_MISSING),
        TransformationOperation(type=TransformationType.NORMALIZE_NUMERIC, params={"column": "y"}),
    ])

    res = DataTransformer.apply_pipeline(rows, pipeline)
    assert len(res) == 2
    assert res[0]["y"] == 0.0
    assert res[1]["y"] == 1.0


def test_chart_data_generation_5_types():
    rows = [
        {"time": 1, "temp": 20.0, "press": 100},
        {"time": 2, "temp": 25.0, "press": 102},
        {"time": 3, "temp": 30.0, "press": 105},
        {"time": 4, "temp": 35.0, "press": 108},
    ]

    # 1. Line Chart
    line_spec = VisualizationSpec(
        project_id="p1", dataset_id="d1", name="Line", type=ChartType.LINE, x_column="time", y_columns=["temp"]
    )
    line_res = VisualizationDataService.generate_chart_data(line_spec, rows)
    assert line_res.type == ChartType.LINE
    assert len(line_res.series[0].data) == 4

    # 2. Scatter Plot
    scatter_spec = VisualizationSpec(
        project_id="p1", dataset_id="d1", name="Scatter", type=ChartType.SCATTER, x_column="time", y_columns=["temp"]
    )
    scatter_res = VisualizationDataService.generate_chart_data(scatter_spec, rows)
    assert scatter_res.type == ChartType.SCATTER

    # 3. Bar Chart
    bar_spec = VisualizationSpec(
        project_id="p1", dataset_id="d1", name="Bar", type=ChartType.BAR, x_column="time", y_columns=["temp"]
    )
    bar_res = VisualizationDataService.generate_chart_data(bar_spec, rows)
    assert bar_res.type == ChartType.BAR

    # 4. Histogram
    hist_spec = VisualizationSpec(
        project_id="p1", dataset_id="d1", name="Hist", type=ChartType.HISTOGRAM, x_column="temp", y_columns=[]
    )
    hist_res = VisualizationDataService.generate_chart_data(hist_spec, rows)
    assert hist_res.type == ChartType.HISTOGRAM
    assert len(hist_res.series) >= 1

    # 5. Heatmap
    heat_spec = VisualizationSpec(
        project_id="p1", dataset_id="d1", name="Heat", type=ChartType.HEATMAP, x_column="time", y_columns=["temp", "press"]
    )
    heat_res = VisualizationDataService.generate_chart_data(heat_spec, rows)
    assert heat_res.type == ChartType.HEATMAP
    assert len(heat_res.series[0].data) == 8


def test_changed_dataset_detection():
    spec = VisualizationSpec(
        project_id="p1", dataset_id="d1", name="Line", type=ChartType.LINE, x_column="x", y_columns=["y"]
    )
    rows = [{"x": 1, "y": 2}]

    chart_res = VisualizationDataService.generate_chart_data(
        spec=spec,
        raw_rows=rows,
        current_hash="hash_v2",
        stored_hash="hash_v1",
    )
    assert chart_res.dataset_hash_changed is True
    assert "changed" in chart_res.warning
