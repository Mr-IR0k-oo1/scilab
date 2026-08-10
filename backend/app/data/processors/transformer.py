from typing import Any, Dict, List
from app.data.models import TransformationOperation, TransformationPipeline, TransformationType


class DataTransformer:
    @staticmethod
    def apply_pipeline(rows: List[Dict[str, Any]], pipeline: TransformationPipeline) -> List[Dict[str, Any]]:
        result = [dict(r) for r in rows]  # Copy rows

        for op in pipeline.operations:
            result = DataTransformer.apply_operation(result, op)

        return result

    @staticmethod
    def apply_operation(rows: List[Dict[str, Any]], op: TransformationOperation) -> List[Dict[str, Any]]:
        if not rows:
            return rows

        if op.type == TransformationType.SELECT_COLUMNS:
            cols = op.params.get("columns", [])
            if not cols:
                return rows
            return [{k: r[k] for k in cols if k in r} for r in rows]

        elif op.type == TransformationType.DROP_MISSING:
            return [r for r in rows if all(v is not None for v in r.values())]

        elif op.type == TransformationType.FILL_MISSING_NUMERIC:
            fill_val = float(op.params.get("value", 0.0))
            new_rows = []
            for r in rows:
                new_r = {}
                for k, v in r.items():
                    new_r[k] = fill_val if v is None and isinstance(fill_val, (int, float)) else v
                new_rows.append(new_r)
            return new_rows

        elif op.type == TransformationType.RENAME_COLUMNS:
            mapping = op.params.get("mapping", {})
            new_rows = []
            for r in rows:
                new_r = {}
                for k, v in r.items():
                    new_k = mapping.get(k, k)
                    new_r[new_k] = v
                new_rows.append(new_r)
            return new_rows

        elif op.type == TransformationType.SORT:
            col = op.params.get("column")
            ascending = op.params.get("ascending", True)
            if not col or not rows:
                return rows
            return sorted(rows, key=lambda r: r.get(col) if r.get(col) is not None else float("-inf"), reverse=not ascending)

        elif op.type == TransformationType.NORMALIZE_NUMERIC:
            col = op.params.get("column")
            if not col or not rows:
                return rows
            vals = [r[col] for r in rows if r.get(col) is not None and isinstance(r.get(col), (int, float))]
            if not vals:
                return rows
            min_v, max_v = min(vals), max(vals)
            diff = (max_v - min_v) if max_v != min_v else 1.0
            new_rows = []
            for r in rows:
                new_r = dict(r)
                if new_r.get(col) is not None and isinstance(new_r.get(col), (int, float)):
                    new_r[col] = (new_r[col] - min_v) / diff
                new_rows.append(new_r)
            return new_rows

        return rows
