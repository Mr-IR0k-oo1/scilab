from typing import List, Dict, Any

class ReportGenerator:
    @staticmethod
    def generate_html(title: str, blocks: List[Dict[str, Any]]) -> str:
        html = [
            "<!DOCTYPE html>",
            "<html><head>",
            "<meta charset='utf-8'/>",
            f"<title>{title}</title>",
            "<style>",
            "body { font-family: sans-serif; margin: 40px; color: #222; background: #fff; }",
            "h1, h2, h3 { color: #111; border-bottom: 1px solid #ddd; padding-bottom: 6px; }",
            "pre { background: #f4f4f4; padding: 12px; border-radius: 4px; overflow-x: auto; }",
            "table { border-collapse: collapse; width: 100%; margin: 16px 0; }",
            "th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: left; }",
            "th { background: #f8f8f8; }",
            ".report-block { margin-bottom: 24px; }",
            "</style>",
            "</head><body>",
            f"<h1>{title}</h1>"
        ]

        for block in blocks:
            btype = block.get("type", "paragraph")
            content = block.get("content", "")

            html.append("<div class='report-block'>")
            if btype == "heading":
                html.append(f"<h2>{content}</h2>")
            elif btype == "paragraph":
                html.append(f"<p>{content}</p>")
            elif btype == "code":
                html.append(f"<pre><code>{content}</code></pre>")
            elif btype == "table":
                # Render simple table if content structured as dict
                if isinstance(content, dict) and "headers" in content and "rows" in content:
                    html.append("<table><thead><tr>")
                    for h in content["headers"]:
                        html.append(f"<th>{h}</th>")
                    html.append("</tr></thead><tbody>")
                    for r in content["rows"]:
                        html.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in r) + "</tr>")
                    html.append("</tbody></table>")
                else:
                    html.append(f"<p>{content}</p>")
            elif btype == "image":
                html.append(f"<img src='{content}' style='max-width:100%; border-radius:4px;'/>")
            else:
                html.append(f"<div>{content}</div>")
            html.append("</div>")

        html.append("</body></html>")
        return "\n".join(html)

report_generator = ReportGenerator()
