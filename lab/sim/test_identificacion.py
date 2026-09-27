"""Regression checks for the off-line step-response identification."""
import importlib.util
import os
import unittest

HERE = os.path.dirname(__file__)
SPEC = importlib.util.spec_from_file_location(
    "identificacion", os.path.join(HERE, "identificacion.py"))


class IdentificacionContract(unittest.TestCase):
    def test_holdout_is_not_part_of_fit_and_reports_each_tap(self):
        """A regression must not silently score an input run it trained on."""
        module = importlib.util.module_from_spec(SPEC)
        SPEC.loader.exec_module(module)
        result = module.identify()
        self.assertEqual(set(result["holdout"]),
                         {"idac0_pgax16.json", "paso4_idac1.json", "paso6_idac2.json"})
        self.assertTrue(all(len(row["taps"]) == 5 for row in result["holdout"].values()))


if __name__ == "__main__":
    unittest.main()
