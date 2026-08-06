import unittest
import asyncio
from fossee_backend.main import app
from fossee_backend.routers import charts, widgets, data, reports, learning, scilab
from fossee_backend.data_importer import data_importer
from fossee_backend.report_generator import report_generator

class TestBackendServices(unittest.TestCase):

    def test_data_importer_csv(self):
        csv_data = "Name,Age,Score\nAlice,25,95.5\nBob,30,88.0"
        columns, rows = data_importer.parse_csv(csv_data)
        self.assertEqual(len(columns), 3)
        self.assertEqual(columns[0]["name"], "Name")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][0], "Alice")

    def test_data_importer_json(self):
        json_data = '[{"name": "Alice", "score": 95}, {"name": "Bob", "score": 88}]'
        columns, rows = data_importer.parse_json(json_data)
        self.assertEqual(len(columns), 2)
        self.assertEqual(len(rows), 2)

    def test_report_generator_html(self):
        blocks = [
            {"type": "heading", "content": "Test Report"},
            {"type": "paragraph", "content": "Sample paragraph content."}
        ]
        html = report_generator.generate_html("Title", blocks)
        self.assertIn("<h1>Title</h1>", html)
        self.assertIn("<h2>Test Report</h2>", html)
        self.assertIn("Sample paragraph content.", html)

    def test_chart_types_async(self):
        types_res = asyncio.run(charts.get_supported_types())
        self.assertIn("line", types_res["types"])

    def test_widget_types_async(self):
        w_types = asyncio.run(widgets.get_all_widget_types())
        self.assertTrue(len(w_types) > 0)

    def test_learning_async(self):
        ex = asyncio.run(learning.get_examples())
        self.assertIn("examples", ex)
        self.assertTrue(len(ex["examples"]) > 0)

        tut = asyncio.run(learning.get_tutorials())
        self.assertIn("tutorials", tut)

        ref = asyncio.run(learning.get_reference())
        self.assertIn("reference", ref)

    def test_data_types_async(self):
        dt = asyncio.run(data.get_supported_import_types())
        self.assertIn("formats", dt)

    def test_reports_templates_async(self):
        tmpl = asyncio.run(reports.list_report_templates())
        self.assertIn("templates", tmpl)

if __name__ == "__main__":
    unittest.main()
