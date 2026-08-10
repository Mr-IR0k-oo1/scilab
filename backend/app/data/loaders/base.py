import hashlib
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from app.data.models import DatasetSchema


class BaseDataLoader(ABC):
    @staticmethod
    def calculate_file_hash(file_path: str) -> str:
        sha = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                sha.update(chunk)
        return sha.hexdigest()

    @abstractmethod
    def load_rows(self, file_path: str, max_rows: Optional[int] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def inspect_schema(self, file_path: str) -> DatasetSchema:
        pass
