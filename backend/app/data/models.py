import hashlib
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict, Field


class ColumnType(str, Enum):
    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    TEXT = "text"
    UNKNOWN = "unknown"


class NumericStatistics(BaseModel):
    count: int
    min: Optional[float] = None
    max: Optional[float] = None
    mean: Optional[float] = None
    median: Optional[float] = None
    std_dev: Optional[float] = None


class ColumnSummary(BaseModel):
    name: str
    data_type: ColumnType
    missing_count: int
    sample_values: List[Any] = []
    numeric_stats: Optional[NumericStatistics] = None


class DatasetSchema(BaseModel):
    filename: str
    format: str
    size_bytes: int
    row_count: int
    column_count: int
    content_hash: str
    column_names: List[str]
    columns: List[ColumnSummary]
    numeric_columns: List[str]
    categorical_columns: List[str]
    missing_value_count: int


class DatasetValidationResult(BaseModel):
    valid: bool
    warnings: List[str] = []
    errors: List[str] = []
    statistics: Dict[str, Any] = {}


class TransformationType(str, Enum):
    SELECT_COLUMNS = "select_columns"
    FILTER_ROWS = "filter_rows"
    SORT = "sort"
    RENAME_COLUMNS = "rename_columns"
    DROP_MISSING = "drop_missing"
    FILL_MISSING_NUMERIC = "fill_missing_numeric"
    NORMALIZE_NUMERIC = "normalize_numeric"


class TransformationOperation(BaseModel):
    type: TransformationType
    params: Dict[str, Any] = {}


class TransformationPipeline(BaseModel):
    operations: List[TransformationOperation] = []
