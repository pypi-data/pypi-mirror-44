# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Interpolation utilities"""
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from astropy import units as u


__all__ = ["ScaledRegularGridInterpolator", "interpolation_scale"]


class ScaledRegularGridInterpolator:
    """Thin wrapper around `scipy.interpolate.RegularGridInterpolator`.

    The values are scaled before the interpolation and back-scaled after the
    interpolation.

    Parameters
    ----------
    points : tuple of `~numpy.ndarray` or `~astropy.units.Quantity`
        Tuple of points passed to `RegularGridInterpolator`.
    values : `~numpy.ndarray`
        Values passed to `RegularGridInterpolator`.
    points_scale : tuple of str
        Interpolation scale used for the points.
    values_scale : {'lin', 'log', 'sqrt'}
        Interpolation scaling applied to values. If the values vary over many magnitudes
        a 'log' scaling is recommended.
    **kwargs : dict
        Keyword arguments passed to `RegularGridInterpolator`.
    """

    def __init__(
        self,
        points,
        values,
        points_scale=None,
        values_scale="lin",
        extrapolate=True,
        **kwargs
    ):

        if points_scale is None:
            points_scale = ["lin"] * len(points)

        self.scale_points = [interpolation_scale(scale) for scale in points_scale]
        self.scale = interpolation_scale(values_scale)

        points_scaled = tuple([scale(p) for p, scale in zip(points, self.scale_points)])
        values_scaled = self.scale(values)

        if extrapolate:
            kwargs.setdefault("bounds_error", False)
            kwargs.setdefault("fill_value", None)

        self._interpolate = RegularGridInterpolator(
            points=points_scaled, values=values_scaled, **kwargs
        )

    def __call__(self, points, method="linear", clip=True, **kwargs):
        """Interpolate data points.

        Parameters
        ----------
        points : tuple of `np.ndarray` or `~astropy.units.Quantity`
            Tuple of coordinate arrays of the form (x_1, x_2, x_3, ...). Arrays are
            broadcasted internally.
        method : {"linear", "nearest"}
            Linear or nearest neighbour interpolation.
        clip : bool
            Clip values at zero after interpolation.
        """
        points = tuple([scale(p) for scale, p in zip(self.scale_points, points)])

        points = np.broadcast_arrays(*points)
        points_interp = np.stack([_.flat for _ in points]).T

        values = self._interpolate(points_interp, method, **kwargs)
        values = self.scale.inverse(values.reshape(points[0].shape))

        if clip:
            values = np.clip(values, 0, np.inf)

        return values


def interpolation_scale(scale="lin"):
    """Interpolation scaling.

    Parameters
    ----------
    scale : {"lin", "log", "sqrt"}
        Choose interpolation scaling.
    """
    if scale in ["lin", "linear"]:
        return LinearScale()
    elif scale == "log":
        return LogScale()
    elif scale == "sqrt":
        return SqrtScale()
    else:
        raise ValueError("Not a valid value scaling mode: '{}'.".format(scale))


class InterpolationScale:
    """Interpolation scale base class."""

    def __call__(self, values):
        if hasattr(self, "_unit"):
            values = values.to_value(self._unit)
        else:
            if isinstance(values, u.Quantity):
                self._unit = values.unit
                values = values.value
        return self._scale(values)

    def inverse(self, values):
        values = self._inverse(values)
        if hasattr(self, "_unit"):
            return u.Quantity(values, self._unit, copy=False)
        else:
            return values


class LogScale(InterpolationScale):
    """Logarithmic scaling"""

    tiny = np.finfo(np.float32).tiny

    def _scale(self, values):
        values = np.clip(values, self.tiny, np.inf)
        return np.log(values)

    @staticmethod
    def _inverse(values):
        return np.exp(values)


class SqrtScale(InterpolationScale):
    """Sqrt scaling"""

    @staticmethod
    def _scale(values):
        sign = np.sign(values)
        return sign * np.sqrt(sign * values)

    @staticmethod
    def _inverse(values):
        return np.power(values, 2)


class LinearScale(InterpolationScale):
    """Linear scaling"""

    @staticmethod
    def _scale(values):
        return values

    @staticmethod
    def _inverse(values):
        return values
