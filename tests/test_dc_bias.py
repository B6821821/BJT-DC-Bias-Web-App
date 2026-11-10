"""Unit tests for dc_bias.py — engineering logic only (no Flask)."""

import unittest

from dc_bias import parse_number, calculate_dc_bias, KILO, VCE_SAT_MAX


class TestDcBias(unittest.TestCase):
    """Forward-Active reference values (VCC=12, R1=100k, R2=22k, RC=2.2k,
    RE=1k, beta=100, VBE=0.70 → VB=1.9422 V, VE=1.2422 V, VC=9.2943 V,
    VCE=8.0522 V, IC=1.2299 mA, IB=12.299 µA)."""

    def test_reference_values_forward_active(self):
        result = calculate_dc_bias(12, 100, 22, 2.2, 1, 100, 0.70)
        self.assertAlmostEqual(result["vth"], 2.1639, places=4)
        self.assertAlmostEqual(result["rth_kohm"], 18.0328, places=4)
        self.assertAlmostEqual(result["ib"], 12.299e-6, places=7)
        self.assertAlmostEqual(result["ic"], 1.2299e-3, places=7)
        self.assertAlmostEqual(result["ie"], 1.2422e-3, places=7)
        self.assertAlmostEqual(result["vb"], 1.9422, places=4)
        self.assertAlmostEqual(result["ve"], 1.2422, places=4)
        self.assertAlmostEqual(result["vc"], 9.2943, places=4)
        self.assertAlmostEqual(result["vce"], 8.0522, places=4)
        self.assertEqual(result["region"], "Forward Active")
        self.assertEqual(result["warnings"], [])

    def test_thevenin_equivalents(self):
        result = calculate_dc_bias(12, 100, 22, 2.2, 1, 100, 0.70)
        self.assertAlmostEqual(result["vth"], 12 * 22 / (100 + 22), places=6)
        self.assertAlmostEqual(result["rth_kohm"], 100 * 22 / (100 + 22), places=6)

    def test_cutoff_when_vth_below_vbe(self):
        # R1=100k, R2=4.7k → VTH ≈ 0.54 V ≤ VBE=0.70 → Cutoff
        result = calculate_dc_bias(12, 100, 4.7, 2.2, 1, 100, 0.70)
        self.assertEqual(result["region"], "Cutoff")
        self.assertEqual(result["ic"], 0.0)
        self.assertEqual(result["ib"], 0.0)
        self.assertEqual(result["ie"], 0.0)
        self.assertAlmostEqual(result["vce"], 12.0, places=6)
        self.assertGreater(len(result["warnings"]), 0)
        self.assertIn("Cutoff", result["warnings"][0])

    def test_saturation_warns(self):
        # Large RC pulls VC down → VCE ≤ 0.3 V → Saturation warning
        result = calculate_dc_bias(12, 100, 22, 10, 1, 100, 0.70)
        self.assertEqual(result["region"], "Saturation")
        self.assertLessEqual(result["vce"], 0.3)
        self.assertGreater(len(result["warnings"]), 0)
        self.assertIn("Saturation", result["warnings"][0])

    def test_higher_beta_gives_higher_ic(self):
        low = calculate_dc_bias(12, 100, 22, 2.2, 1, 100, 0.70)["ic"]
        high = calculate_dc_bias(12, 100, 22, 2.2, 1, 200, 0.70)["ic"]
        self.assertGreater(high, low)

    def test_invalid_components_rejected(self):
        for kwargs in (
            dict(vcc=0, r1=100, r2=22, rc=2.2, re=1, beta=100, vbe=0.70),
            dict(vcc=12, r1=0, r2=22, rc=2.2, re=1, beta=100, vbe=0.70),
            dict(vcc=12, r1=100, r2=22, rc=0, re=1, beta=100, vbe=0.70),
            dict(vcc=12, r1=100, r2=22, rc=2.2, re=0, beta=100, vbe=0.70),
            dict(vcc=12, r1=100, r2=22, rc=2.2, re=1, beta=0, vbe=0.70),
            dict(vcc=12, r1=100, r2=22, rc=2.2, re=1, beta=100, vbe=12.0),
        ):
            with self.assertRaises(ValueError):
                calculate_dc_bias(**kwargs)

    def test_parse_number_rejects_text(self):
        with self.assertRaises(ValueError) as ctx:
            parse_number("abc", "R1")
        self.assertIn("R1", str(ctx.exception))

    def test_parse_number_rejects_empty_and_nan(self):
        with self.assertRaises(ValueError):
            parse_number("", "VBE")
        with self.assertRaises(ValueError):
            parse_number("nan", "VCC")


if __name__ == "__main__":
    unittest.main()
