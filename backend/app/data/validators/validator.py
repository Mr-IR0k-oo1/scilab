import os
from typing import Any, Dict, List
from app.data.models import DatasetSchema, DatasetValidationResult


class DatasetValidator:
    @staticmethod
    def validate(schema: DatasetSchema) -> DatasetValidationResult:
        warnings: List[str] = []
        errors: List[str] = []
        valid = True

        if schema.row_count == 0:
            errors.append("Dataset contains 0 data rows.")
            valid = False

        if schema.column_count == 0:
            errors.append("Dataset contains 0 columns.")
            valid = False

        if schema.missing_value_count > 0:
            warnings.append(f"Dataset contains {schema.missing_value_count} total missing values.")

        for col in schema.columns:
            if col.missing_count == schema.row_count and schema.row_count > 0:
                warnings.append(f"Column '{col.name}' is completely empty.")

        stats = {
            "filename": schema.filename,
            "format": schema.format,
            "size_bytes": schema.size_bytes,
            "row_count": schema.row_count,
            "column_count": schema.column_count,
            "numeric_columns_count": len(schema.numeric_columns),
            "categorical_columns_count": len(schema.categorical_columns),
            "missing_values_count": schema.missing_value_count,
        }

        return DatasetValidationResult(
            valid=valid,
            warnings=warnings,
            errors=errors,
            statistics=stats,
        )
