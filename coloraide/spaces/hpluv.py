"""
HPLuv.

Adapted to Python and ColorAide by Isaac Muse (2021)

--- License ---

Copyright (c) 2012-2021 Alexei Boronine
Copyright (c) 2016 Florian Dormont

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from ..spaces import Space, RE_DEFAULT_MATCH, FLG_ANGLE, FLG_PERCENT, GamutBound, Cylindrical
from .lch import ACHROMATIC_THRESHOLD
from .hsluv import max_safe_chroma_for_l
from .. import util
import re
from ..util import MutableVector
from typing import Tuple


def hpluv_to_lch(hpluv: MutableVector) -> MutableVector:
    """Convert HPLuv to Lch."""

    h, s, l = hpluv
    h = util.no_nan(h)
    c = 0.0
    if l > 100 - 1e-7:
        l = 100
    elif l < 1e-08:
        l = 0.0
    else:
        _hx_max = max_safe_chroma_for_l(l)
        c = _hx_max / 100 * s
        if c < ACHROMATIC_THRESHOLD:
            h = util.NaN
    return [l, c, util.constrain_hue(h)]


def lch_to_hpluv(lch: MutableVector) -> MutableVector:
    """Convert Lch to HPLuv."""

    l, c, h = lch
    h = util.no_nan(h)
    s = 0.0
    if l > 100 - 1e-7:
        l = 100
    elif l < 1e-08:
        l = 0.0
    else:
        _hx_max = max_safe_chroma_for_l(l)
        s = c / _hx_max * 100
    if s < 1e-08:
        h = util.NaN
    return [util.constrain_hue(h), s, l]


class HPLuv(Cylindrical, Space):
    """HPLuv class."""

    BASE = 'lchuv-d65'
    NAME = "hpluv"
    SERIALIZE = ("--hpluv",)
    CHANNEL_NAMES = ("h", "p", "l")
    CHANNEL_ALIASES = {
        "hue": "h",
        "perpendiculars": "p",
        "lightness": "l"
    }
    DEFAULT_MATCH = re.compile(RE_DEFAULT_MATCH.format(color_space='|'.join(SERIALIZE), channels=3))
    WHITE = "D65"
    GAMUT_CHECK = "srgb"

    BOUNDS = (
        GamutBound(0.0, 360.0, FLG_ANGLE),
        GamutBound(0.0, 100.0, FLG_PERCENT),
        GamutBound(0.0, 100.0, FLG_PERCENT)
    )

    @property
    def h(self) -> float:
        """Hue channel."""

        return self._coords[0]

    @h.setter
    def h(self, value: float) -> None:
        """Shift the hue."""

        self._coords[0] = self._handle_input(value)

    @property
    def p(self) -> float:
        """Perpendiculars channel."""

        return self._coords[1]

    @p.setter
    def p(self, value: float) -> None:
        """Use perpendiculars to unsaturate the color by the given factor."""

        self._coords[1] = self._handle_input(value)

    @property
    def l(self) -> float:
        """Lightness channel."""

        return self._coords[2]

    @l.setter
    def l(self, value: float) -> None:
        """Set lightness channel."""

        self._coords[2] = self._handle_input(value)

    @classmethod
    def null_adjust(cls, coords: MutableVector, alpha: float) -> Tuple[MutableVector, float]:
        """On color update."""

        if coords[1] == 0:
            coords[0] = util.NaN
        return coords, alpha

    @classmethod
    def to_base(cls, coords: MutableVector) -> MutableVector:
        """To LCHuv from HPLuv."""

        return hpluv_to_lch(coords)

    @classmethod
    def from_base(cls, coords: MutableVector) -> MutableVector:
        """From LCHuv to HPLuv."""

        return lch_to_hpluv(coords)
