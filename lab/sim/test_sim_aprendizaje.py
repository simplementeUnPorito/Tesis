"""Pruebas de contrato del simulador host del aprendizaje."""
import importlib.util
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(__file__)
RUNNER = os.path.join(HERE, "sim_aprendizaje.py")


class SimAprendizajeContract(unittest.TestCase):
    def test_campaign_reports_baseline_and_variants(self):
        """A campaign must expose the real-runtime baseline and both variants."""
        result = subprocess.run(
            [sys.executable, RUNNER, "--campaign", "--json"],
            cwd=HERE, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"baseline"', result.stdout)
        self.assertIn('"opa_sum"', result.stdout)
        self.assertIn('"coarse_fine"', result.stdout)

    def test_authority_fit_preserves_measured_topology(self):
        """The fitted plant must retain the four measured scaling relations."""
        spec = importlib.util.spec_from_file_location("sim_aprendizaje", RUNNER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        law = module.fit_authority()
        self.assertGreater(law["idac0"][50], law["idac0"][4] * 10)
        self.assertAlmostEqual(law["idac1_opa"][4], law["idac1_opa"][50], delta=0.5)
        self.assertAlmostEqual(law["idac2_opa"][4], law["idac2_opa"][50], delta=0.5)
        self.assertGreater(abs(law["idac2_sum"][50]), abs(law["idac2_sum"][4]) * 10)


if __name__ == "__main__":
    unittest.main()
