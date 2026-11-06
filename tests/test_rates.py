import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    # ------------------------------------------------------------------
    # Standard service (preserved behaviour)
    # ------------------------------------------------------------------
    def test_standard_rates(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_standard_explicit_keyword(self):
        self.assertEqual(shipping_quote(2, "local", service="standard"), 8.0)

    def test_invalid_weight(self):
        with self.assertRaises(ValueError):
            shipping_quote(0, "local")

    # ------------------------------------------------------------------
    # Express service
    # ------------------------------------------------------------------
    def test_express_local(self):
        # standard local = 5 + 1.5*2 = 8; express adds 7 → 15
        self.assertEqual(shipping_quote(2, "local", service="express"), 15.0)

    def test_express_regional(self):
        # standard regional = 8 + 1.5*2 = 11; express adds 7 → 18
        self.assertEqual(shipping_quote(2, "regional", service="express"), 18.0)

    def test_express_fractional_weight(self):
        # 8 + 1.5*1.5 + 7 = 17.25
        self.assertAlmostEqual(
            shipping_quote(1.5, "regional", service="express"), 17.25, places=2
        )

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def test_invalid_zone(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "intergalactic")

    def test_invalid_service(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "local", service="overnight")
