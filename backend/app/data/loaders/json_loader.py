import json
import os
import statistics
from typing import Any, Dict, List, Optional
from app.data.loaders.base import BaseDataLoader
from app.data.models import ColumnSummary, ColumnType, DatasetSchema, NumericStatistics


class JSONDataLoader(BaseDataLoader):
    def load_rows(self, file_path: str, max_rows: Optional[int] = 1000) -> List[Dict[str, Any]]:
        rows = []
        if not os.path.exists(file_path):
            return rows

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
            if isinstance(data, list):
                raw_rows = data
            elif isinstance(data, dict):
                raw_rows = data.get("data", [data])
            else:
                raw_rows = []

            for i, item in enumerate(raw_rows):
                if max_rows is not None and i >= max_rows:
                    break
                if isinstance(item, dict):
                    rows.append(item)
        except Exception:
            pass

        return rows

    def inspect_schema(self, file_path: str) -> DatasetSchema:
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        content_hash = self.calculate_file_hash(file_path) if file_size > 0 else ""

        rows = self.load_rows(file_path, max_rows=5000)
        if not rows:
            return DatasetSchema(
                filename=os.path.basename(file_path),
                format="json",
                size_bytes=file_size,
                row_count=0,
                column_count=0,
                content_hash=content_hash,
                column_names=[],
                columns=[],
                numeric_columns=[],
                categorical_columns=[],
                missing_value_count=0,
            )

        # Collect unique keys
        keys_set = []
        for r in rows:
            for k in r.keys():
                if k not in keys_set:
                    keys_set.append(k)

        column_names = keys_set
        total_missing = 0
        col_summaries = []
        numeric_cols = []
        categorical_cols = []

        for col in column_names:
            vals = [r.get(col) for r in rows]
            non_nulls = [v for v in vals if v is not None]
            missing_c = len(vals) - len(non_nulls)
            total_missing += missing_c

            num_vals = []
            for v in non_nulls:
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    num_vals.append(float(v))

            is_numeric = len(num_vals) > 0 and len(num_vals) == len(non_nulls)

            if is_numeric:
                col_type = ColumnType.NUMERIC
                numeric_cols.append(col)
                stat_obj = NumericStatistics(
                    count=len(num_vals),
                    min=min(num_vals) if num_vals else None,
                    max=max(num_vals) if num_vals else None,
                    mean=statistics.mean(num_vals) if num_vals else None,
                    median=statistics.median(num_vals) if num_vals else None,
                    std_dev=statistics.stdev(num_vals) if len(num_vals) > 1 else 0.0,
                )
            else:
                col_type = ColumnType.CATEGORICAL
                categorical_cols.append(col)
                stat_obj = None

            col_summaries.append(
                ColumnSummary(
                    name=col,
                    data_type=col_type,
                    missing_count=missing_c,
                    sample_values=vals[:5],
                    numeric_stats=stat_obj,
                )
            )

        return DatasetSchema(
            filename=os.path.basename(file_path),
            format="json",
            size_bytes=file_size,
            row_count=len(rows),
            column_count=len(column_names),
            content_hash=content_hash,
            column_names=column_names,
            columns=col_summaries,
            numeric_columns=numeric_cols,
            categorical_columns=categorical_cols,
            missing_value_count=total_missing,
        )
