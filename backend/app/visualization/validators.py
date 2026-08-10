from typing import List
from fastapi import HTTPException, status
from app.data.models import ColumnType, DatasetSchema
from app.visualization.models import ChartType, VisualizationSpec


class VisualizationValidator:
    @staticmethod
    def validate_spec(spec: VisualizationSpec, schema: DatasetSchema) -> None:
        if spec.type in [ChartType.LINE, ChartType.SCATTER, ChartType.BAR]:
            if not spec.x_column:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"code": "MISSING_X_COLUMN", "message": f"Chart type '{spec.type}' requires an 'x_column' specification."},
                )
            if spec.x_column not in schema.column_names:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"code": "INVALID_COLUMN", "message": f"Column '{spec.x_column}' does not exist in dataset."},
                )
            if not spec.y_columns:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"code": "MISSING_Y_COLUMNS", "message": f"Chart type '{spec.type}' requires at least one 'y_columns' entry."},
                )
            for y_col in spec.y_columns:
                if y_col not in schema.column_names:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={"code": "INVALID_COLUMN", "message": f"Column '{y_col}' does not exist in dataset."},
                    )

        elif spec.type == ChartType.HISTOGRAM:
            if not spec.x_column and not spec.y_columns:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"code": "MISSING_HISTOGRAM_COLUMN", "message": "Histogram requires a target numeric column in 'x_column' or 'y_columns'."},
                )

        elif spec.type == ChartType.HEATMAP:
            if not spec.x_column or not spec.y_columns:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"code": "MISSING_HEATMAP_AXES", "message": "Heatmap requires both 'x_column' and 'y_columns'."},
                )
