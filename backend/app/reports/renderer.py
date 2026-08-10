import os
from datetime import datetime, timezone
from typing import Any, Dict
from jinja2 import Environment, FileSystemLoader, select_autoescape


class ReportRenderer:
    @staticmethod
    def render_html(template_name: str, context: Dict[str, Any]) -> str:
        templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates", template_name))
        if not os.path.exists(templates_dir):
            # Fallback to default
            templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates", "default_engineering_report"))

        env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
        template = env.get_template("template.html")
        return template.render(**context)
