"""Test Okhsv library."""
import unittest
from . import util
from coloraide import Color, NaN


class TestOkhsvInputOutput(util.ColorAsserts, unittest.TestCase):
    """Test Okhsv."""

    def test_input_raw(self):
        """Test raw input."""

        self.assertColorEqual(Color("okhsv", [20, 100, 75]), Color('color(--okhsv 20 100% 75%)'))

    def test_color_class(self):
        """Test raw input."""

        self.assertColorEqual(Color(Color("okhsv", [20, 100, 75])), Color('color(--okhsv 20 100% 75%)'))

    def test_color(self):
        """Test color input/output format."""

        args = {"color": True}
        color = "color(--okhsv 20 100% 75%)"

        self.assertEqual(Color(color).to_string(**args), 'color(--okhsv 20 100% 75%)')

        color = "color(--okhsv 20 100% 75% / 0.5)"
        self.assertEqual(Color(color).to_string(**args), 'color(--okhsv 20 100% 75% / 0.5)')

        color = "color(--okhsv 20 100% 75% / 50%)"
        self.assertEqual(Color(color).to_string(**args), 'color(--okhsv 20 100% 75% / 0.5)')

    def test_no_alpha(self):
        """Test no alpha."""

        args = {"alpha": False}

        color = "color(--okhsv 20 100% 75% 0.2)"
        okhsv = Color(color)
        self.assertEqual("color(--okhsv 20 100% 75%)", okhsv.to_string(**args))

    def test_force_alpha(self):
        """Test force alpha."""

        args = {"alpha": True}

        color = "color(--okhsv 20 100% 75% / 1)"
        okhsv = Color(color)
        self.assertEqual("color(--okhsv 20 100% 75% / 1)", okhsv.to_string(**args))

    def test_precision(self):
        """Test precision."""

        color = 'color(--okhsv 20.1234567 50.1234567% 50.1234567%)'
        self.assertEqual(Color(color).to_string(), 'color(--okhsv 20.123 50.123% 50.123%)')
        self.assertEqual(Color(color).to_string(precision=3), 'color(--okhsv 20.1 50.1% 50.1%)')
        self.assertEqual(Color(color).to_string(precision=0), 'color(--okhsv 20 50% 50%)')
        self.assertEqual(
            Color(color).to_string(precision=-1),
            'color(--okhsv 20.12345669999999842048055143095552921295166015625 50.12345669999999842048055143095552921295166015625% 50.12345669999999842048055143095552921295166015625%)'  # noqa:  E501
        )

    def test_fit(self):
        """Test fit."""

        self.assertEqual(
            Color('color(--okhsv 20 150% 75%)').to_string(),
            'color(--okhsv 23.806 100% 57.454%)'
        )

        self.assertEqual(
            Color('color(--okhsv 20 150% 75%)').to_string(fit="clip"),
            'color(--okhsv 20 100% 75%)'
        )

        self.assertEqual(
            Color('color(--okhsv 20 150% 75%)').to_string(fit=False),
            'color(--okhsv 20 150% 75%)'
        )


class TestOkhsvProperties(util.ColorAsserts, unittest.TestCase):
    """Test Okhsv."""

    def test_hue(self):
        """Test `hue`."""

        c = Color('color(--okhsv 120 50% 50% / 1)')
        self.assertEqual(c.hue, 120)
        c.hue = 110
        self.assertEqual(c.hue, 110)

    def test_saturation(self):
        """Test `saturation`."""

        c = Color('color(--okhsv 120 50% 50% / 1)')
        self.assertEqual(c.saturation, 50)
        c.saturation = 60
        self.assertEqual(c.saturation, 60)

    def test_value(self):
        """Test `value`."""

        c = Color('color(--okhsv 120 50% 50% / 1)')
        self.assertEqual(c.value, 50)
        c.value = 40
        self.assertEqual(c.value, 40)

    def test_alpha(self):
        """Test `alpha`."""

        c = Color('color(--okhsv 120 50% 50% / 1)')
        self.assertEqual(c.alpha, 1)
        c.alpha = 0.5
        self.assertEqual(c.alpha, 0.5)


class TestNull(util.ColorAsserts, unittest.TestCase):
    """Test Null cases."""

    def test_null_input(self):
        """Test null input."""

        c = Color('okhsv', [NaN, 50, 75], 1)
        self.assertTrue(c.is_nan('hue'))

    def test_auto_null(self):
        """Test auto null."""

        c = Color('color(--okhsv 120 0% 75% / 1)')
        self.assertTrue(c.is_nan('hue'))