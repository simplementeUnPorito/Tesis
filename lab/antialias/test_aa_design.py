"""Compile the C89 prototype and compare it against the Python reference."""

from __future__ import annotations

import pathlib
import subprocess
import tempfile
import unittest

import numpy as np
from scipy import signal

from reference import FACTORS, acquisition_fir_q23, kaiser_q23

HERE = pathlib.Path(__file__).resolve().parent


class CReferenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory()
        cls.exe = pathlib.Path(cls.temp.name) / "aa_design.exe"
        subprocess.run(
            ["gcc", "-std=c99", "-pedantic", "-Wall", "-Wextra", "-Werror",
             "-DAA_DESIGN_STANDALONE", str(HERE / "aa_design.c"), "-lm",
             "-o", str(cls.exe)], check=True, cwd=HERE,
        )
        cls.psoc_header_exe = pathlib.Path(cls.temp.name) / "test_psoc_aa_header.exe"
        subprocess.run(
            ["gcc", "-std=c99", "-pedantic", "-Wall", "-Wextra", "-Werror",
             "-I", str(HERE / "host"), str(HERE / "host" / "test_psoc_aa_header.c"),
             "-o", str(cls.psoc_header_exe)], check=True, cwd=HERE,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def c_coefficients(self, factor: int) -> np.ndarray:
        result = subprocess.run([str(self.exe), str(factor)], check=True,
                                text=True, capture_output=True)
        lines = result.stdout.splitlines()
        taps = int(lines[0])
        coeff = np.fromstring(lines[1], dtype=np.int32, sep=" ")
        self.assertEqual(taps, len(coeff))
        return coeff

    def test_coefficients_and_response(self) -> None:
        for factor in FACTORS:
            with self.subTest(factor=factor):
                c_q23 = self.c_coefficients(factor)
                py_q23 = kaiser_q23(factor)
                np.testing.assert_array_equal(c_q23, py_q23)
                self.assertEqual(int(c_q23.sum(dtype=np.int64)), 1 << 23)
                _, c_h = signal.freqz(c_q23.astype(float) / (1 << 23), worN=262144)
                _, py_h = signal.freqz(py_q23.astype(float) / (1 << 23), worN=262144)
                self.assertLess(float(np.max(np.abs(c_h - py_h))), 1e-14)
                stop = int(np.ceil((1.2 / factor) * 262144))
                rejection = -20 * np.log10(np.max(np.abs(c_h[stop:])))
                self.assertGreaterEqual(rejection, 85.0)

    def test_q23_avoids_the_q15_rejection_floor(self) -> None:
        factor = 16
        q23 = kaiser_q23(factor)
        q15 = np.rint(q23.astype(float) / (1 << 8)).astype(np.int16)
        q15[len(q15) // 2] += np.int16((1 << 15) - int(q15.sum(dtype=np.int64)))
        stop = int(np.ceil((1.2 / factor) * 1048576))
        _, h23 = signal.freqz(q23.astype(float) / (1 << 23), worN=1048576)
        _, h15 = signal.freqz(q15.astype(float) / (1 << 15), worN=1048576)
        rejection_q23 = -20 * np.log10(np.max(np.abs(h23[stop:])))
        rejection_q15 = -20 * np.log10(np.max(np.abs(h15[stop:])))
        self.assertGreater(rejection_q23, 85.0)
        self.assertLess(rejection_q15, 75.0)
        self.assertGreater(rejection_q23 - rejection_q15, 20.0)

    def test_decimator_keeps_input_sample_zero_then_every_n(self) -> None:
        result = subprocess.run([str(self.exe), "4", "13"], check=True,
                                text=True, capture_output=True)
        emitted = [tuple(map(int, line.split())) for line in result.stdout.splitlines()]
        self.assertEqual(emitted, [(0, 123456), (4, 123456),
                                   (8, 123456), (12, 123456)])

    def test_exact_psoc_header_on_host(self) -> None:
        result = subprocess.run([str(self.psoc_header_exe)], check=True,
                                text=True, capture_output=True)
        self.assertIn("N=16 taps=459 coef_bytes=2044", result.stdout)

        coefficients = subprocess.run(
            [str(self.psoc_header_exe), "--coeff"], check=True,
            text=True, capture_output=True,
        )
        q23 = np.fromstring(coefficients.stdout, dtype=np.int32, sep=" ")
        self.assertEqual(q23.size, 459)
        self.assertEqual(int(q23.sum(dtype=np.int64)), 1 << 23)
        _, response = signal.freqz(q23.astype(float) / (1 << 23), worN=1048576)
        stop = int(np.ceil((1.2 / 16) * 1048576))
        rejection = -20 * np.log10(np.max(np.abs(response[stop:])))
        self.assertGreater(rejection, 85.0)

    def test_2000_hz_acquisition_fir(self) -> None:
        coefficients = acquisition_fir_q23(2000.0)
        self.assertEqual(coefficients.size, 127)
        self.assertEqual(int(coefficients.sum()), 1 << 23)
        self.assertTrue(np.array_equal(coefficients, coefficients[::-1]))
        frequency, response = signal.freqz(
            coefficients.astype(float) / (1 << 23), worN=262144, fs=2000.0
        )
        magnitude_db = 20 * np.log10(np.maximum(np.abs(response), 1e-15))
        passband = magnitude_db[frequency <= 150.0]
        stopband = magnitude_db[frequency >= 250.0]
        self.assertLess(float(np.ptp(passband)), 0.02)
        self.assertGreaterEqual(float(-np.max(stopband)), 60.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
