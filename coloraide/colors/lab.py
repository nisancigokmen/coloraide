"""LAB class."""
from ._space import Space, RE_DEFAULT_MATCH
from ._gamut import GamutUnbound, GamutBound
from . import _convert as convert
from . import _parse as parse
from .. import util
import re


class LAB(Space):
    """LAB class."""

    SPACE = "lab"
    DEF_BG = "color(lab 0 0 0 / 1)"
    CHANNEL_NAMES = frozenset(["l", "a", "b", "alpha"])
    DEFAULT_MATCH = re.compile(RE_DEFAULT_MATCH.format(color_space=SPACE))

    _gamut = (
        (GamutBound(0), GamutUnbound(100.0)),  # Technically we could/should clamp the zero side.
        (GamutUnbound(-160), GamutUnbound(160)),  # No limit, but we could impose one +/-160?
        (GamutUnbound(-160), GamutUnbound(160))  # No limit, but we could impose one +/-160?
    )

    def __init__(self, color=DEF_BG):
        """Initialize."""

        super().__init__(color)

        if isinstance(color, Space):
            self.l, self.a, self.b = convert.convert(color.coords(), color.space(), self.space())
            self.alpha = color.alpha
        elif isinstance(color, str):
            values = self.match(color)[0]
            if values is None:
                raise ValueError("'{}' does not appear to be a valid color".format(color))
            self.l, self.a, self.b, self.alpha = values
        elif isinstance(color, (list, tuple)):
            if not (3 <= len(color) <= 4):
                raise ValueError("A list of channel values should be of length 3 or 4.")
            self.l = color[0]
            self.a = color[1]
            self.b = color[2]
            self.alpha = 1.0 if len(color) == 3 else color[3]
        else:
            raise TypeError("Unexpected type '{}' received".format(type(color)))

    def _is_achromatic(self, coords):
        """Is achromatic."""

        l, a, b = [util.round_half_up(c, scale=util.DEF_PREC) for c in coords]
        return abs(a) < util.ACHROMATIC_THRESHOLD and abs(b) < util.ACHROMATIC_THRESHOLD

    @property
    def l(self):
        """L channel."""

        return self._coords[0]

    @l.setter
    def l(self, value):
        """Get true luminance."""

        self._coords[0] = self.translate_channel(0, value) if isinstance(value, str) else float(value)

    @property
    def a(self):
        """A channel."""

        return self._coords[1]

    @a.setter
    def a(self, value):
        """A axis."""

        self._coords[1] = self.translate_channel(1, value) if isinstance(value, str) else float(value)

    @property
    def b(self):
        """B channel."""

        return self._coords[2]

    @b.setter
    def b(self, value):
        """B axis."""

        self._coords[2] = self.translate_channel(2, value) if isinstance(value, str) else float(value)

    @classmethod
    def translate_channel(cls, channel, value):
        """Translate channel string."""

        if 0 <= channel <= 2:
            return parse.norm_float(value)
        elif channel == -1:
            return parse.norm_alpha_channel(value)
        else:
            raise ValueError("Unexpected channel index of '{}'".format(channel))

    def to_string(self, *, alpha=None, precision=util.DEF_PREC, fit=None, **kwargs):
        """To string."""

        return super().to_string(alpha=alpha, precision=precision, fit=fit)
