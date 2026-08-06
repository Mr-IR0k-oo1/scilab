import csv
import json
import io
from typing import List, Dict, Any, Tuple

class DataImporter:
    @staticmethod
    def parse_csv(content: str) -> Tuple[List[Dict[str, str]], List[List[Any]]]:
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        if not rows:
            return [], []
        
        headers = rows[0]
        columns = [{"name": h if h.strip() else f"Col_{i+1}", "type": "string"} for i, h in enumerate(headers)]
        data_rows = rows[1:]
        
        # Infer type for first row of data
        if data_rows:
            sample = data_rows[0]
            for i, val in enumerate(sample):
                if i < len(columns):
                    try:
                        float(val)
                        columns[i]["type"] = "number"
                    except ValueError:
                        columns[i]["type"] = "string"
                        
        return columns, data_rows

    @staticmethod
    def parse_json(content: str) -> Tuple[List[Dict[str, str]], List[List[Any]]]:
        data = json.loads(content)
        if isinstance(data, list) and data:
            if isinstance(data[0], dict):
                headers = list(data[0].keys())
                columns = [{"name": h, "type": "number" if isinstance(data[0][h], (int, float)) else "string"} for h in headers]
                rows = [[item.get(h) for h in headers] for item in data]
                return columns, rows
            elif isinstance(data[0], list):
                headers = [f"Col_{i+1}" for i in range(len(data[0]))]
                columns = [{"name": h, "type": "string"} for h in headers]
                return columns, data
        return [], []

data_importer = DataImporter()
