"""Regression checks for multiple advisors and unknown historical degrees."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('genealogy_fetch', Path(__file__).resolve().parents[1] / 'genealogy-fetch.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ParserTests(unittest.TestCase):
    def test_all_advisors_but_not_students(self):
        page = '''Mathematics Genealogy Project
        <h2>A &amp; B</h2><div style="line-height: 30px; text-align:center">Ph.D. <span>Example University</span> 2000</div>
        Dissertation: <span id="thesisTitle">A thesis</span>
        <p style="text-align:center">Advisor 1: <a href="id.php?id=1">First</a><br />Advisor 2: <a href="id.php?id=2">Second</a></p>
        <p>Students: <a href="id.php?id=3">Third</a></p>'''
        record = module.parse(page, '4')
        self.assertEqual(record['name'], 'A & B')
        self.assertEqual(record['advisors'], ['1', '2'])
        self.assertEqual(record['degree'], 'Ph.D. Example University 2000')

    def test_terminal_record_is_not_invented(self):
        record = module.parse('Mathematics Genealogy Project <h2>Old Scholar</h2> Dissertation:', '5')
        self.assertEqual(record['advisors'], [])
        self.assertEqual(record['degree'], '')

    def test_error_page_is_not_a_terminal_ancestor(self):
        with self.assertRaises(ValueError):
            module.parse('<h2>Service unavailable</h2>', '5')


if __name__ == '__main__':
    unittest.main()
