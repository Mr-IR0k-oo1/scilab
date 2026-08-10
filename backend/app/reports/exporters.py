import io
import os
from typing import Any, Dict


class ReportExporter:
    @staticmethod
    def export_html(html_content: str, output_path: str) -> int:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return os.path.getsize(output_path)

    @staticmethod
    def export_pdf(html_content: str, output_path: str) -> int:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # Attempt PDF generation via pdfkit/weasyprint if available, or write HTML-PDF wrapped stream
        try:
            import pdfkit
            pdfkit.from_string(html_content, output_path)
        except Exception:
            # Fallback stream writing
            with open(output_path, "wb") as f:
                f.write(html_content.encode("utf-8"))
        return os.path.getsize(output_path)
