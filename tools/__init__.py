from .convert_latex import convert_latex, return_latex_surface
from .differentiation import differentiate
from .eq_solver import solve
from .grapher import Plotter
from .integrator import integrate
from .max_min import find_extrema
from .parse_function import parse_function

__all__ = [
    "convert_latex",
    "return_latex_surface",
    "differentiate",
    "solve",
    "Plotter",
    "integrate",
    "find_extrema",
    "parse_function",
]
