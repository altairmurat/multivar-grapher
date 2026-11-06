"""
MultivarGrapher 3D — Core Mathematical, Plotting, Constraint & AI Engine for Marimo
===================================================================================
Supports:
- Scalar functions in R2: f(x1, x2)
- Scalar functions in R3 (3D Level Surfaces): f(x1, x2, x3) = c
- Vector fields in R2 & R3: [-x2, x1], [x1; x2; x3]
- Matrices in R2 (2x2) & R3 (3x3): [2, 1; 1, 2], [1, 2, 3; 4, 5, 6; 7, 8, 9]
- Equality & Inequality Constraints + 3D Cylindrical Extrusion along free variables (x3)
- Affine Tangent Plane g(x), 2D/3D Normal Lines, 90° Right-Angle Marker, Error Rod
- Hessian Matrix, Eigenvalues, Discriminant D, and 2nd Derivative Extremum Test
- Interactive Plotly 2D / 3D / Split Figures with 3D Orbit, Level Slice, and Gliding Point Animations
- Gemini 3.5 Flash-Lite AI Tutor + Offline Calculus Intelligence + Automatic Graph Action execution
"""

import json
import math
import os
import re
import ssl
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sympy as sp


# =============================================================================
# 1. MATHEMATICAL PRESETS CATALOG
# =============================================================================
PRESETS: Dict[str, Dict[str, Any]] = {
    "circle_example": {
        "label": "⭕ Circle Level Set: x₁² + x₂² (c = 4, r = 2)",
        "f": "x1^2 + x2^2",
        "constraint": "",
        "c": 4.0,
        "r": 2.0,
        "a1": 2.0,
        "a2": 0.0,
        "a3": 0.0,
        "xr": [-6.0, 6.0],
        "yr": [-6.0, 6.0],
        "view_mode": "Split Dual View",
    },
    "ellipse": {
        "label": "🪐 Elliptic Paraboloid: x₁²/4 + x₂²/9 (c = 1)",
        "f": "x1^2 / 4 + x2^2 / 9",
        "constraint": "",
        "c": 1.0,
        "r": 1.0,
        "a1": 1.2,
        "a2": 2.4,
        "a3": 0.0,
        "xr": [-6.0, 6.0],
        "yr": [-6.0, 6.0],
        "view_mode": "Split Dual View",
    },
    "saddle": {
        "label": "🐎 Hyperbolic Saddle: x₁² - x₂² (c = 1)",
        "f": "x1^2 - x2^2",
        "constraint": "",
        "c": 1.0,
        "r": 1.0,
        "a1": 1.41,
        "a2": 1.0,
        "a3": 0.0,
        "xr": [-5.0, 5.0],
        "yr": [-5.0, 5.0],
        "view_mode": "Split Dual View",
    },
    "cylindrical_parabola": {
        "label": "🏛️ Parabolic Cylinder in ℝ³: [x₁; x₂; x₃] s.t. x₁²/4 + x₂ = 1",
        "f": "[x1; x2; x3]",
        "constraint": "x1^2 / 4 + x2 = 1",
        "c": 1.0,
        "r": 1.0,
        "a1": 2.0,
        "a2": 0.0,
        "a3": 1.0,
        "xr": [-5.0, 5.0],
        "yr": [-5.0, 5.0],
        "view_mode": "3D Surface",
    },
    "cylindrical_ellipse": {
        "label": "🏛️ Elliptic Cylinder in ℝ³: [x₁; x₂; x₃] s.t. x₁²/4 + x₂²/9 = 1",
        "f": "[x1; x2; x3]",
        "constraint": "x1^2 / 4 + x2^2 / 9 = 1",
        "c": 1.0,
        "r": 1.0,
        "a1": 2.0,
        "a2": 0.0,
        "a3": 1.0,
        "xr": [-5.0, 5.0],
        "yr": [-5.0, 5.0],
        "view_mode": "3D Surface",
    },
    "lagrange_opt": {
        "label": "🎯 Constrained Extrema (Lagrange): x₁² + x₂² s.t. x₁ + 2x₂ = 4",
        "f": "x1^2 + x2^2",
        "constraint": "x1 + 2*x2 = 4",
        "c": 3.2,
        "r": 1.79,
        "a1": 0.8,
        "a2": 1.6,
        "a3": 0.0,
        "xr": [-5.0, 5.0],
        "yr": [-5.0, 5.0],
        "view_mode": "Split Dual View",
    },
    "r2_matrix": {
        "label": "🔢 2×2 Matrix in ℝ²: [2, 1; 1, 2]",
        "f": "[2, 1; 1, 2]",
        "constraint": "",
        "c": 1.0,
        "r": 1.0,
        "a1": 1.0,
        "a2": 1.0,
        "a3": 0.0,
        "xr": [-5.0, 5.0],
        "yr": [-5.0, 5.0],
        "view_mode": "Split Dual View",
    },
    "r3_matrix": {
        "label": "🧊 3×3 Matrix in ℝ³: [1, 2, 3; 4, 5, 6; 7, 8, 9]",
        "f": "[1, 2, 3; 4, 5, 6; 7, 8, 9]",
        "constraint": "",
        "c": 1.0,
        "r": 1.0,
        "a1": 1.0,
        "a2": 0.5,
        "a3": 0.5,
        "xr": [-6.0, 6.0],
        "yr": [-6.0, 6.0],
        "view_mode": "3D Surface",
    },
    "r2_vector": {
        "label": "🌀 2D Rotational Vector Field: [-x₂, x₁]",
        "f": "[-x2, x1]",
        "constraint": "",
        "c": 2.0,
        "r": 1.41,
        "a1": 1.5,
        "a2": 1.0,
        "a3": 0.0,
        "xr": [-5.0, 5.0],
        "yr": [-5.0, 5.0],
        "view_mode": "Split Dual View",
    },
    "vortex_irrotational": {
        "label": "🌪️ Irrotational Swirl (Curl = 0 outside origin): [-x₂/(x₁²+x₂²+0.05), x₁/(x₁²+x₂²+0.05)]",
        "f": "[-x2/(x1^2 + x2^2 + 0.05), x1/(x1^2 + x2^2 + 0.05)]",
        "constraint": "",
        "c": 1.0,
        "r": 1.0,
        "a1": 1.5,
        "a2": 1.0,
        "a3": 0.0,
        "xr": [-4.0, 4.0],
        "yr": [-4.0, 4.0],
        "view_mode": "Split Dual View",
    },
    "conservative_grad": {
        "label": "⚡ Conservative Gradient Field: [2*x₁*x₂, x₁²] (φ = x₁²x₂)",
        "f": "[2*x1*x2, x1^2]",
        "constraint": "",
        "c": 4.0,
        "r": 2.0,
        "a1": 1.5,
        "a2": 1.5,
        "a3": 0.0,
        "xr": [-4.0, 4.0],
        "yr": [-4.0, 4.0],
        "view_mode": "Split Dual View",
    },
    "source_radial": {
        "label": "🌋 Radial Source Field (div = +2): [x₁, x₂]",
        "f": "[x1, x2]",
        "constraint": "",
        "c": 2.0,
        "r": 1.41,
        "a1": 1.5,
        "a2": 1.0,
        "a3": 0.0,
        "xr": [-5.0, 5.0],
        "yr": [-5.0, 5.0],
        "view_mode": "Split Dual View",
    },
    "saddle_field": {
        "label": "🧲 Hyperbolic Saddle Field (div = 0, curl = 0): [x₁, -x₂]",
        "f": "[x1, -x2]",
        "constraint": "",
        "c": 1.0,
        "r": 1.0,
        "a1": 1.5,
        "a2": 1.0,
        "a3": 0.0,
        "xr": [-4.0, 4.0],
        "yr": [-4.0, 4.0],
        "view_mode": "Split Dual View",
    },
    "shear_flow": {
        "label": "🌊 Shear Flow (Parallel with Non-Zero Curl): [x₂², 0]",
        "f": "[x2^2, 0]",
        "constraint": "",
        "c": 2.0,
        "r": 1.41,
        "a1": 1.0,
        "a2": 1.5,
        "a3": 0.0,
        "xr": [-4.0, 4.0],
        "yr": [-4.0, 4.0],
        "view_mode": "Split Dual View",
    },
    "line_integral_loop": {
        "label": "∮ Circulation & Green's Theorem: ∮_C [-x₂, x₁]·dr = 2πR²",
        "f": "[-x2, x1]",
        "constraint": "",
        "c": 2.0,
        "r": 1.5,
        "a1": 0.0,
        "a2": 0.0,
        "a3": 0.0,
        "xr": [-4.0, 4.0],
        "yr": [-4.0, 4.0],
        "view_mode": "Split Dual View",
    },
    "tornado_3d": {
        "label": "🌪️ 3D Helical Swirl & Updraft: [-x₂; x₁; 1.5]",
        "f": "[-x2; x1; 1.5]",
        "constraint": "",
        "c": 2.0,
        "r": 1.41,
        "a1": 1.5,
        "a2": 1.0,
        "a3": 1.0,
        "xr": [-4.0, 4.0],
        "yr": [-4.0, 4.0],
        "view_mode": "3D Surface",
    },
    "r3_vector": {
        "label": "🧭 3D Radial Vector Field in ℝ³: [x₁; x₂; x₃]",
        "f": "[x1; x2; x3]",
        "constraint": "",
        "c": 3.0,
        "r": 1.73,
        "a1": 1.5,
        "a2": 1.5,
        "a3": 1.5,
        "xr": [-5.0, 5.0],
        "yr": [-5.0, 5.0],
        "view_mode": "3D Surface",
    },
    "r3_sphere": {
        "label": "🌐 3D Level Surface (Sphere in ℝ³): x₁² + x₂² + x₃² = 4",
        "f": "x1^2 + x2^2 + x3^2",
        "constraint": "",
        "c": 4.0,
        "r": 2.0,
        "a1": 1.0,
        "a2": 1.0,
        "a3": 1.414,
        "xr": [-4.0, 4.0],
        "yr": [-4.0, 4.0],
        "view_mode": "3D Surface",
    },
    "monkey": {
        "label": "🐒 Monkey Saddle: x₁³ - 3x₁x₂²",
        "f": "x1^3 - 3*x1*x2^2",
        "constraint": "",
        "c": 0.0,
        "r": 1.0,
        "a1": 1.0,
        "a2": 0.5,
        "a3": 0.0,
        "xr": [-3.5, 3.5],
        "yr": [-3.5, 3.5],
        "view_mode": "Split Dual View",
    },
    "cone": {
        "label": "🍦 Elliptic Cone: sqrt(x₁² + x₂² + 0.01)",
        "f": "sqrt(x1^2 + x2^2 + 0.01)",
        "constraint": "",
        "c": 2.0,
        "r": 2.0,
        "a1": 1.2,
        "a2": 1.6,
        "a3": 0.0,
        "xr": [-5.0, 5.0],
        "yr": [-5.0, 5.0],
        "view_mode": "Split Dual View",
    },
    "ripple": {
        "label": "💧 Water Droplet Ripple: sin(2*sqrt(x₁² + x₂²))",
        "f": "sin(2 * sqrt(x1^2 + x2^2 + 0.01))",
        "constraint": "",
        "c": 0.5,
        "r": 1.0,
        "a1": 1.0,
        "a2": 1.0,
        "a3": 0.0,
        "xr": [-6.0, 6.0],
        "yr": [-6.0, 6.0],
        "view_mode": "Split Dual View",
    },
    "gaussian": {
        "label": "🔔 Gaussian Wave Packet: 4*exp(-(x₁² + x₂²)/3)*cos(1.5*x₁)",
        "f": "4 * exp(-(x1^2 + x2^2)/3) * cos(1.5*x1)",
        "constraint": "",
        "c": 1.5,
        "r": 1.2,
        "a1": 0.5,
        "a2": 0.5,
        "a3": 0.0,
        "xr": [-5.0, 5.0],
        "yr": [-5.0, 5.0],
        "view_mode": "Split Dual View",
    },
    "egg_carton": {
        "label": "🥚 Egg Carton Periodic Surface: 2*sin(x₁)*cos(x₂)",
        "f": "2 * sin(x1) * cos(x2)",
        "constraint": "",
        "c": 1.0,
        "r": 1.0,
        "a1": 0.8,
        "a2": 0.5,
        "a3": 0.0,
        "xr": [-6.0, 6.0],
        "yr": [-6.0, 6.0],
        "view_mode": "Split Dual View",
    },
    "rosenbrock": {
        "label": "🍌 Rosenbrock Valley: (1 - x₁)² + 2*(x₂ - x₁²)²",
        "f": "(1 - x1)^2 + 2 * (x2 - x1^2)^2",
        "constraint": "",
        "c": 2.0,
        "r": 1.4,
        "a1": 0.5,
        "a2": 0.5,
        "a3": 0.0,
        "xr": [-3.0, 3.0],
        "yr": [-2.0, 4.0],
        "view_mode": "Split Dual View",
    },
    "flow_line": {
        "label": "🌊 Flow Line γ(t) of Gradient Field: γ'(t) = ∇f(γ(t))",
        "f": "x1^2 / 4 + x2^2 / 9",
        "constraint": "",
        "c": 1.0,
        "r": 1.0,
        "a1": 1.2,
        "a2": 2.4,
        "a3": 0.0,
        "xr": [-6.0, 6.0],
        "yr": [-6.0, 6.0],
        "view_mode": "Split Dual View",
        "show_flow_line": True,
    },
}


# =============================================================================
# 2. EXPRESSION NORMALIZATION & PARSING
# =============================================================================
def normalize_math_expr(expr_str: str, params: Optional[Dict[str, float]] = None) -> str:
    """Normalizes user math string for SymPy parsing."""
    if not expr_str or not expr_str.strip():
        return "0"
    s = expr_str.strip()
    s = s.replace("^", "**")
    # Convert standalone x, y, z into x1, x2, x3
    s = re.sub(r"\bx\b", "x1", s)
    s = re.sub(r"\by\b", "x2", s)
    s = re.sub(r"\bz\b", "x3", s)
    # Implicit multiplication: e.g. 2x1 -> 2*x1, 3(x1) -> 3*(x1), )( -> )*(
    s = re.sub(r"(\d)\s*(x[123]\b|[a-d]\b|\()", r"\1*\2", s)
    s = re.sub(r"(\))\s*(\d|x[123]\b|[a-d]\b|\()", r"\1*\2", s)
    s = re.sub(r"(x[123])\s*(\()", r"\1*\2", s)

    if params:
        for k, v in params.items():
            s = re.sub(rf"\b{k}\b", f"({float(v)})", s)
    return s


def split_top_level(text: str, delimiters: str = ",;") -> List[str]:
    """Splits a mathematical string by delimiters only at the top level of parentheses/brackets."""
    parts = []
    current: List[str] = []
    depth = 0
    for char in text:
        if char in "([{":
            depth += 1
            current.append(char)
        elif char in ")]}":
            depth = max(0, depth - 1)
            current.append(char)
        elif depth == 0 and char in delimiters:
            p_str = "".join(current).strip()
            if p_str:
                parts.append(p_str)
            current = []
        else:
            current.append(char)
    last = "".join(current).strip()
    if last:
        parts.append(last)
    return parts


def parse_matrix_or_vector(raw_expr: str) -> Dict[str, Any]:
    """
    Detects whether `raw_expr` is:
    - a constant 2x2 or 3x3 matrix: `[2, 1; 1, 2]` or `[1, 2, 3; 4, 5, 6; 7, 8, 9]`
    - a 2D or 3D vector field: `[-x2, x1]`, `<-y, x>`, `[x1; x2; x3]`, or `F(x,y) = <P, Q>`
    - or a scalar expression.
    """
    s = (raw_expr or "").strip()
    # Remove common vector prefixes like F = , F(x1, x2) = , F(x, y) = , \mathbf{F} = 
    s = re.sub(r"^(?:\\mathbf\{F\}|F)\s*(?:\([^)]*\))?\s*=\s*", "", s).strip()

    is_bracketed = False
    inner = s
    if (s.startswith("[") and s.endswith("]")) or (s.startswith("<") and s.endswith(">")):
        is_bracketed = True
        inner = s[1:-1].strip()
    elif s.startswith("(") and s.endswith(")"):
        # Check if there is a top-level comma inside, indicating a vector rather than a grouped scalar
        top_parts = split_top_level(s[1:-1].strip(), ",")
        if len(top_parts) in (2, 3):
            is_bracketed = True
            inner = s[1:-1].strip()

    if not is_bracketed or not inner:
        return {"is_bracketed": False}

    # Check if semicolon-separated rows (matrices or column vectors)
    if ";" in inner:
        rows_raw = split_top_level(inner, ";")
        grid_cells = []
        for r_str in rows_raw:
            cols = split_top_level(r_str, ",")
            grid_cells.append(cols)

        # Case A: Multi-row matrix (2x2 or 3x3) where each row has >1 element
        if len(grid_cells) in (2, 3) and all(len(r) == len(grid_cells) for r in grid_cells):
            try:
                mat_vals = [[float(sp.sympify(normalize_math_expr(c))) for c in r] for r in grid_cells]
                dim = len(grid_cells)
                return {
                    "is_bracketed": True,
                    "kind": f"matrix_{dim}d",
                    "dim": dim,
                    "matrix": np.array(mat_vals, dtype=float),
                }
            except Exception:
                pass

        # Case B: Column vector written as [f1; f2] or [f1; f2; f3]
        if all(len(r) == 1 for r in grid_cells) and len(grid_cells) in (2, 3):
            comps = [r[0] for r in grid_cells]
            return {
                "is_bracketed": True,
                "kind": f"vector_{len(comps)}d",
                "dim": len(comps),
                "components": comps,
            }

    # Comma-separated vector [f1, f2], <f1, f2>, or [f1, f2, f3]
    comps = split_top_level(inner, ",")
    if len(comps) in (2, 3):
        return {
            "is_bracketed": True,
            "kind": f"vector_{len(comps)}d",
            "dim": len(comps),
            "components": comps,
        }

    return {"is_bracketed": False}


def find_potential_function(
    comp_syms: List[sp.Expr],
    vars_tuple: Tuple[sp.Symbol, ...],
) -> Dict[str, Any]:
    """
    Symbolically tests if a 2D or 3D vector field is conservative (curl = 0),
    and if so, finds the scalar potential function φ such that F = ∇φ.
    Returns full step-by-step LaTeX derivations and a fast callable NumPy function.
    """
    dim = len(comp_syms)
    x1 = vars_tuple[0]
    x2 = vars_tuple[1]
    x3 = vars_tuple[2] if dim == 3 else sp.Symbol("x3")

    if dim == 2:
        P, Q = comp_syms[0], comp_syms[1]
        curl = sp.simplify(sp.diff(Q, x1) - sp.diff(P, x2))
        is_conservative = bool(curl == 0)

        if is_conservative:
            try:
                phi1 = sp.integrate(P, x1)
                rem = sp.simplify(Q - sp.diff(phi1, x2))
                g = sp.integrate(rem, x2)
                phi = sp.simplify(phi1 + g)
                phi_fn = sp.lambdify((x1, x2), phi, "numpy")
                latex_derivation = (
                    rf"\begin{{aligned}}"
                    rf"\text{{1. Curl Test: }} & \operatorname{{curl}}\mathbf{{F}} = \frac{{\partial Q}}{{\partial x_1}} - \frac{{\partial P}}{{\partial x_2}} = 0 \implies \mathbf{{F}} \text{{ is conservative!}} \\"
                    rf"\text{{2. Integrate }} F_1: & \phi(x_1, x_2) = \int ({sp.latex(P)})\,dx_1 = {sp.latex(phi1)} + g(x_2) \\"
                    rf"\text{{3. Match }} F_2: & \frac{{\partial \phi}}{{\partial x_2}} = {sp.latex(sp.diff(phi1, x2))} + g'(x_2) = {sp.latex(Q)} \implies g'(x_2) = {sp.latex(rem)} \\"
                    rf"\text{{4. Integrate }} g'(x_2): & g(x_2) = \int ({sp.latex(rem)})\,dx_2 = {sp.latex(g)} \\"
                    rf"\text{{5. Potential: }} & \phi(x_1, x_2) = {sp.latex(phi)}"
                    rf"\end{{aligned}}"
                )
                return {
                    "is_conservative": True,
                    "curl_sym": curl,
                    "phi_sym": phi,
                    "phi_latex": sp.latex(phi),
                    "derivation_latex": latex_derivation,
                    "phi_fn": phi_fn,
                }
            except Exception:
                pass

        return {
            "is_conservative": False,
            "curl_sym": curl,
            "phi_sym": None,
            "phi_latex": r"\text{None (Non-conservative, } \operatorname{curl}\mathbf{F} \neq 0)",
            "derivation_latex": rf"\operatorname{{curl}}\mathbf{{F}} = \frac{{\partial Q}}{{\partial x_1}} - \frac{{\partial P}}{{\partial x_2}} = {sp.latex(curl)} \neq 0 \implies \text{{Line integrals depend on path!}}",
            "phi_fn": None,
        }

    elif dim == 3:
        P, Q, R = comp_syms[0], comp_syms[1], comp_syms[2]
        cx = sp.simplify(sp.diff(R, x2) - sp.diff(Q, x3))
        cy = sp.simplify(sp.diff(P, x3) - sp.diff(R, x1))
        cz = sp.simplify(sp.diff(Q, x1) - sp.diff(P, x2))
        is_conservative = bool(cx == 0 and cy == 0 and cz == 0)

        if is_conservative:
            try:
                phi1 = sp.integrate(P, x1)
                rem2 = sp.simplify(Q - sp.diff(phi1, x2))
                phi2 = sp.integrate(rem2, x2)
                rem3 = sp.simplify(R - sp.diff(phi1 + phi2, x3))
                phi3 = sp.integrate(rem3, x3)
                phi = sp.simplify(phi1 + phi2 + phi3)
                phi_fn = sp.lambdify((x1, x2, x3), phi, "numpy")
                latex_derivation = (
                    rf"\begin{{aligned}}"
                    rf"\text{{1. Curl Test: }} & \nabla \times \mathbf{{F}} = \mathbf{{0}} \implies \mathbf{{F}} \text{{ is conservative!}} \\"
                    rf"\text{{2. Potential: }} & \phi(x_1, x_2, x_3) = {sp.latex(phi)}"
                    rf"\end{{aligned}}"
                )
                return {
                    "is_conservative": True,
                    "curl_sym": [cx, cy, cz],
                    "phi_sym": phi,
                    "phi_latex": sp.latex(phi),
                    "derivation_latex": latex_derivation,
                    "phi_fn": phi_fn,
                }
            except Exception:
                pass

        return {
            "is_conservative": False,
            "curl_sym": [cx, cy, cz],
            "phi_sym": None,
            "phi_latex": r"\text{None (Non-conservative, } \nabla \times \mathbf{F} \neq \mathbf{0})",
            "derivation_latex": rf"\nabla \times \mathbf{{F}} \neq \mathbf{{0}} \implies \text{{Circulation exists, line integrals depend on path!}}",
            "phi_fn": None,
        }

    return {"is_conservative": False, "phi_fn": None}


def compute_line_integral(
    comp_fns: List[Any],
    dim: int,
    curve_type: str = "circle",
    center: Tuple[float, float] = (0.0, 0.0),
    radius: float = 1.5,
    p0: Tuple[float, float] = (0.0, 0.0),
    p1: Tuple[float, float] = (2.0, 1.0),
    a3: float = 0.0,
    num_samples: int = 150,
    potential_fn: Optional[Any] = None,
    is_conservative: bool = False,
    curl_val: float = 0.0,
) -> Dict[str, Any]:
    """
    Computes numerical and analytical line integral W = ∫_C F · dr along standard paths
    (closed circle loop, straight line segment, parabolic curve), comparing with
    Green's Theorem circulation and potential difference Δφ.
    """
    c1, c2 = center
    if curve_type == "circle":
        ts = np.linspace(0, 2 * np.pi, num_samples)
        dt = ts[1] - ts[0]
        xs = c1 + radius * np.cos(ts)
        ys = c2 + radius * np.sin(ts)
        zs = np.full_like(xs, a3)
        dx_dt = -radius * np.sin(ts)
        dy_dt = radius * np.cos(ts)
        dz_dt = np.zeros_like(ts)
        curve_name = f"Closed Circle Loop (R = {radius:.2f} at ({c1:.1f}, {c2:.1f}))"
        is_closed = True
    elif curve_type == "parabola":
        ts = np.linspace(0, 1.0, num_samples)
        dt = ts[1] - ts[0]
        xs = p0[0] + ts * (p1[0] - p0[0])
        ys = p0[1] + (ts**2) * (p1[1] - p0[1])
        zs = np.full_like(xs, a3)
        dx_dt = np.full_like(ts, p1[0] - p0[0])
        dy_dt = 2 * ts * (p1[1] - p0[1])
        dz_dt = np.zeros_like(ts)
        curve_name = f"Parabolic Path from ({p0[0]:.1f},{p0[1]:.1f}) to ({p1[0]:.1f},{p1[1]:.1f})"
        is_closed = False
    else:
        ts = np.linspace(0, 1.0, num_samples)
        dt = ts[1] - ts[0]
        xs = p0[0] + ts * (p1[0] - p0[0])
        ys = p0[1] + ts * (p1[1] - p0[1])
        zs = np.full_like(xs, a3)
        dx_dt = np.full_like(ts, p1[0] - p0[0])
        dy_dt = np.full_like(ts, p1[1] - p0[1])
        dz_dt = np.zeros_like(ts)
        curve_name = f"Straight Segment from ({p0[0]:.1f},{p0[1]:.1f}) to ({p1[0]:.1f},{p1[1]:.1f})"
        is_closed = False

    us = np.zeros_like(xs)
    vs = np.zeros_like(ys)
    ws = np.zeros_like(zs)
    try:
        if dim == 2:
            us = np.asarray(comp_fns[0](xs, ys), dtype=float)
            vs = np.asarray(comp_fns[1](xs, ys), dtype=float)
        else:
            us = np.asarray(comp_fns[0](xs, ys, zs), dtype=float)
            vs = np.asarray(comp_fns[1](xs, ys, zs), dtype=float)
            ws = np.asarray(comp_fns[2](xs, ys, zs), dtype=float)
    except Exception:
        for i in range(len(xs)):
            try:
                if dim == 2:
                    us[i] = float(comp_fns[0](xs[i], ys[i]))
                    vs[i] = float(comp_fns[1](xs[i], ys[i]))
                else:
                    us[i] = float(comp_fns[0](xs[i], ys[i], zs[i]))
                    vs[i] = float(comp_fns[1](xs[i], ys[i], zs[i]))
                    ws[i] = float(comp_fns[2](xs[i], ys[i], zs[i]))
            except Exception:
                pass

    integrand = us * dx_dt + vs * dy_dt + ws * dz_dt
    trap_fn = getattr(np, "trapezoid", getattr(np, "trapz", None))
    work_val = float(trap_fn(integrand, ts)) if trap_fn is not None else float(np.sum(integrand[:-1]) * dt)

    greens_circulation = float(curl_val * np.pi * (radius**2)) if is_closed else None

    delta_phi = None
    if is_conservative and potential_fn is not None:
        try:
            val_start = potential_fn(xs[0], ys[0]) if dim == 2 else potential_fn(xs[0], ys[0], zs[0])
            val_end = potential_fn(xs[-1], ys[-1]) if dim == 2 else potential_fn(xs[-1], ys[-1], zs[-1])
            phi_start = float(np.real(complex(val_start)))
            phi_end = float(np.real(complex(val_end)))
            delta_phi = phi_end - phi_start
        except Exception:
            delta_phi = None

    return {
        "curve_type": curve_type,
        "curve_name": curve_name,
        "is_closed": is_closed,
        "xs": xs.tolist(),
        "ys": ys.tolist(),
        "zs": zs.tolist(),
        "us": us.tolist(),
        "vs": vs.tolist(),
        "ws": ws.tolist(),
        "integrand": integrand.tolist(),
        "work": work_val,
        "greens_circulation": greens_circulation,
        "delta_phi": delta_phi,
    }


# =============================================================================
# 3. MARCHING SQUARES 2D CONTOUR POLYLINE EXTRACTOR
# =============================================================================
def extract_contour_polylines(
    eval_fn,
    x_range: Tuple[float, float],
    y_range: Tuple[float, float],
    nx: int = 75,
    ny: int = 75,
) -> List[Tuple[np.ndarray, np.ndarray]]:
    """
    High-speed 2D Marching Squares contour extractor for g(x1, x2) = 0.
    Returns a list of continuous (X_poly, Y_poly) numpy arrays.
    """
    xs = np.linspace(x_range[0], x_range[1], nx)
    ys = np.linspace(y_range[0], y_range[1], ny)
    X, Y = np.meshgrid(xs, ys)

    try:
        Z = eval_fn(X, Y)
        if np.isscalar(Z):
            return []
        Z = np.asarray(Z, dtype=float)
    except Exception:
        return []

    segments = []
    for j in range(ny - 1):
        y0, y1 = ys[j], ys[j + 1]
        for i in range(nx - 1):
            x0, x1 = xs[i], xs[i + 1]
            v00 = Z[j, i]
            v10 = Z[j, i + 1]
            v11 = Z[j + 1, i + 1]
            v01 = Z[j + 1, i]
            if not (np.isfinite(v00) and np.isfinite(v10) and np.isfinite(v11) and np.isfinite(v01)):
                continue

            idx = 0
            if v00 >= 0:
                idx |= 1
            if v10 >= 0:
                idx |= 2
            if v11 >= 0:
                idx |= 4
            if v01 >= 0:
                idx |= 8
            if idx == 0 or idx == 15:
                continue

            def interp(va, vb, pa, pb):
                denom = vb - va
                t = 0.5 if abs(denom) < 1e-12 else np.clip(-va / denom, 0.0, 1.0)
                return (pa[0] + t * (pb[0] - pa[0]), pa[1] + t * (pb[1] - pa[1]))

            p_bottom = interp(v00, v10, (x0, y0), (x1, y0))
            p_right = interp(v10, v11, (x1, y0), (x1, y1))
            p_top = interp(v01, v11, (x0, y1), (x1, y1))
            p_left = interp(v00, v01, (x0, y0), (x0, y1))

            if idx in (1, 14):
                segments.append((p_left, p_bottom))
            elif idx in (2, 13):
                segments.append((p_bottom, p_right))
            elif idx in (3, 12):
                segments.append((p_left, p_right))
            elif idx in (4, 11):
                segments.append((p_right, p_top))
            elif idx == 5:
                segments.append((p_left, p_top))
                segments.append((p_bottom, p_right))
            elif idx in (6, 9):
                segments.append((p_bottom, p_top))
            elif idx in (7, 8):
                segments.append((p_left, p_top))
            elif idx == 10:
                segments.append((p_left, p_bottom))
                segments.append((p_right, p_top))

    if not segments:
        return []

    # Chain adjacent segments into continuous polylines
    used = [False] * len(segments)
    polylines: List[Tuple[np.ndarray, np.ndarray]] = []
    eps2 = ((x_range[1] - x_range[0]) / nx * 0.35) ** 2

    def dist2(p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

    for i in range(len(segments)):
        if used[i]:
            continue
        used[i] = True
        chain = [segments[i][0], segments[i][1]]

        changed = True
        while changed:
            changed = False
            for j in range(len(segments)):
                if used[j]:
                    continue
                s0, s1 = segments[j]
                if dist2(chain[-1], s0) < eps2:
                    chain.append(s1)
                    used[j] = True
                    changed = True
                elif dist2(chain[-1], s1) < eps2:
                    chain.append(s0)
                    used[j] = True
                    changed = True
                elif dist2(chain[0], s1) < eps2:
                    chain.insert(0, s0)
                    used[j] = True
                    changed = True
                elif dist2(chain[0], s0) < eps2:
                    chain.insert(0, s1)
                    used[j] = True
                    changed = True

        if len(chain) >= 2:
            px = np.array([p[0] for p in chain], dtype=float)
            py = np.array([p[1] for p in chain], dtype=float)
            polylines.append((px, py))

    return polylines


def parse_constraint(
    raw_constraint: str,
    x_range: Tuple[float, float] = (-6.0, 6.0),
    y_range: Tuple[float, float] = (-6.0, 6.0),
    params: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """
    Parses optional requirement/constraint (e.g. `x1^2/4 + x2 = 1` or `x1^2 + x2^2 <= 4`),
    identifies free variables (such as `x3`), compiles difference function `lhs - rhs`,
    and extracts 2D contour polylines.
    """
    raw = (raw_constraint or "").strip()
    if not raw:
        return {
            "active": False,
            "raw": "",
            "status_text": "No constraint (full ℝⁿ domain)",
            "polylines": [],
            "free_vars": [],
            "is_equality": True,
        }

    op_match = re.search(r"(<=|>=|==|<|>|=)", raw)
    if op_match:
        op = op_match.group(1)
        parts = raw.split(op, 1)
        lhs_str, rhs_str = parts[0].strip(), parts[1].strip()
    else:
        op = "="
        lhs_str, rhs_str = raw, "0"

    is_equality = op in ("=", "==")
    norm_lhs = normalize_math_expr(lhs_str, params)
    norm_rhs = normalize_math_expr(rhs_str, params)

    x1, x2, x3 = sp.symbols("x1 x2 x3")
    try:
        lhs_sym = sp.sympify(norm_lhs)
        rhs_sym = sp.sympify(norm_rhs)
        diff_sym = lhs_sym - rhs_sym
    except Exception as e:
        return {
            "active": False,
            "raw": raw,
            "status_text": f"Invalid constraint syntax: {e}",
            "polylines": [],
            "free_vars": [],
            "is_equality": True,
        }

    used_syms = diff_sym.free_symbols
    free_vars = []
    if x1 not in used_syms:
        free_vars.append("x₁")
    if x2 not in used_syms:
        free_vars.append("x₂")
    if x3 not in used_syms:
        free_vars.append("x₃")

    diff_fn = sp.lambdify((x1, x2), diff_sym.subs(x3, 0), "numpy")
    polylines = extract_contour_polylines(diff_fn, x_range, y_range, nx=75, ny=75)

    if is_equality and "x₃" in free_vars:
        status_text = f"Active Cylinder Requirement ({raw}) • Free variable: x₃ ∈ (-∞, ∞)"
    elif is_equality:
        status_text = f"Active Equality Constraint: {raw}"
    else:
        status_text = f"Active Domain Inequality: {raw}"

    return {
        "active": True,
        "raw": raw,
        "op": op,
        "is_equality": is_equality,
        "diff_sym": diff_sym,
        "diff_fn": diff_fn,
        "free_vars": free_vars,
        "polylines": polylines,
        "status_text": status_text,
        "latex": f"{sp.latex(lhs_sym)} {op if op != '==' else '='} {sp.latex(rhs_sym)}",
    }


# =============================================================================
# 4. COMPLETE SYMBOLIC & NUMERIC CALCULUS ENGINE
# =============================================================================
def analyze_calculus(
    raw_expr: str,
    raw_constraint: str = "",
    a1: float = 2.0,
    a2: float = 0.0,
    a3: float = 0.0,
    level_c: float = 4.0,
    test_x: float = 2.1,
    test_y: float = 0.2,
    x_range: Tuple[float, float] = (-6.0, 6.0),
    y_range: Tuple[float, float] = (-6.0, 6.0),
    params: Optional[Dict[str, float]] = None,
    notation: str = "x1x2",
) -> Dict[str, Any]:
    """
    Performs full symbolic and numerical multivariable calculus analysis.
    """
    x1, x2, x3 = sp.symbols("x1 x2 x3")
    v1_tex = "x_1" if notation == "x1x2" else "x"
    v2_tex = "x_2" if notation == "x1x2" else "y"
    v3_tex = "x_3" if notation == "x1x2" else "z"

    constraint_info = parse_constraint(raw_constraint, x_range, y_range, params)
    parsed_vec = parse_matrix_or_vector(raw_expr)

    # Check if identity vector [x1; x2; x3]
    is_identity_vector = False
    if parsed_vec.get("is_bracketed") and parsed_vec.get("kind") == "vector_3d":
        comps_clean = [normalize_math_expr(c, params).strip() for c in parsed_vec["components"]]
        if comps_clean == ["x1", "x2", "x3"]:
            is_identity_vector = True

    # -------------------------------------------------------------------------
    # CASE 1: 2x2 or 3x3 Constant Matrix [2, 1; 1, 2] or [1,2,3; 4,5,6; 7,8,9]
    # -------------------------------------------------------------------------
    if parsed_vec.get("is_bracketed") and parsed_vec.get("kind") in ("matrix_2d", "matrix_3d"):
        mat = parsed_vec["matrix"]
        dim = parsed_vec["dim"]
        det_val = float(np.linalg.det(mat))
        trace_val = float(np.trace(mat))
        eig_vals = np.linalg.eigvals(mat)
        eig_str = ", ".join(
            f"{ev.real:.2f}" if abs(ev.imag) < 1e-6 else f"{ev.real:.2f}{ev.imag:+.2f}i"
            for ev in eig_vals
        )

        if dim == 2:
            vec_a = np.array([a1, a2], dtype=float)
            ta = mat @ vec_a
            f_sym = mat[0, 0] * x1 + mat[0, 1] * x2
            fa_val = float(np.linalg.norm(ta))
            fx1_val, fx2_val, fx3_val = float(ta[0]), float(ta[1]), 0.0
        else:
            vec_a = np.array([a1, a2, a3], dtype=float)
            ta = mat @ vec_a
            f_sym = mat[0, 0] * x1 + mat[0, 1] * x2 + mat[0, 2] * x3
            fa_val = float(np.linalg.norm(ta))
            fx1_val, fx2_val, fx3_val = float(ta[0]), float(ta[1]), float(ta[2])

        mat_rows_tex = " \\\\ ".join(" & ".join(f"{val:g}" for val in row) for row in mat)
        mat_tex = rf"\mathbf{{A}} = \begin{{bmatrix}} {mat_rows_tex} \end{{bmatrix}}_{{{dim} \times {dim}}}"
        ta_rows_tex = " \\\\ ".join(f"{v:.2f}" for v in ta)

        return {
            "mode": f"matrix_{dim}d",
            "dim": dim,
            "matrix": mat,
            "transformed_a": ta,
            "is_identity_vector": False,
            "raw_expr": raw_expr,
            "f_latex": mat_tex,
            "df_symbolic_latex": rf"\mathbf{{D}}(A\mathbf{{x}}) = \mathbf{{A}}",
            "df_numeric_latex": mat_tex,
            "grad_latex": rf"T(\mathbf{{a}}) = \mathbf{{A}}\mathbf{{a}} = \begin{{bmatrix}} {ta_rows_tex} \end{{bmatrix}}",
            "affine_symbolic_latex": r"g(\mathbf{x}) = \mathbf{A}\mathbf{x}",
            "affine_numeric_latex": rf"g(\mathbf{{x}}) = \mathbf{{A}}\mathbf{{x}}, \quad \|T(\mathbf{{a}})\|_2 = {fa_val:.3f}",
            "hessian_symbolic_latex": r"\mathbf{H} = \mathbf{0} \text{ (Linear Map)}",
            "hessian_numeric_latex": rf"\det(\mathbf{{A}}) = {det_val:.3f}, \quad \operatorname{{tr}}(\mathbf{{A}}) = {trace_val:.3f}",
            "fa": fa_val,
            "fx1": fx1_val,
            "fx2": fx2_val,
            "fx3": fx3_val,
            "grad_mag": fa_val,
            "unit_normal_2d": (1.0, 0.0),
            "unit_tangent_2d": (0.0, 1.0),
            "surface_normal_3d": (0.0, 0.0, 1.0),
            "level_c": level_c,
            "radius_r": math.sqrt(max(0.0, level_c)),
            "level_diff": abs(fa_val - level_c),
            "test_x": test_x,
            "test_y": test_y,
            "test_exact": fa_val,
            "test_affine": fa_val,
            "test_error": 0.0,
            "h11": mat[0, 0],
            "h22": mat[1, 1],
            "h12": mat[0, 1],
            "hessian_det": det_val,
            "hessian_trace": trace_val,
            "eigenvalues_str": eig_str,
            "extremum_type": "linear_matrix",
            "extremum_label": f"Linear Transformation ({dim}×{dim} Matrix) • det(A) = {det_val:.2f}",
            "extremum_badge": "cyan",
            "constraint": constraint_info,
            "v1_tex": v1_tex,
            "v2_tex": v2_tex,
            "v3_tex": v3_tex,
        }

    # -------------------------------------------------------------------------
    # CASE 2: 2D or 3D Vector Field [-x2, x1] or [x1; x2; x3]
    # -------------------------------------------------------------------------
    if parsed_vec.get("is_bracketed") and parsed_vec.get("kind") in ("vector_2d", "vector_3d"):
        dim = parsed_vec["dim"]
        comps_raw = parsed_vec["components"]
        vars_tuple = (x1, x2) if dim == 2 else (x1, x2, x3)
        pt_subs = {x1: a1, x2: a2, x3: a3}

        comp_syms = []
        for c_str in comps_raw:
            try:
                comp_syms.append(sp.sympify(normalize_math_expr(c_str, params)))
            except Exception:
                comp_syms.append(sp.Integer(0))

        comp_fns = [sp.lambdify(vars_tuple, cs, "numpy") for cs in comp_syms]
        f_at_a = [float(cs.subs(pt_subs).evalf()) for cs in comp_syms]
        mag_fa = float(np.linalg.norm(f_at_a))

        # Jacobian Matrix J_F
        jac_sym = sp.Matrix([[sp.diff(cs, v) for v in vars_tuple] for cs in comp_syms])
        jac_num = np.array([[float(jac_sym[r, c].subs(pt_subs).evalf()) for c in range(dim)] for r in range(dim)])
        det_j = float(np.linalg.det(jac_num))

        # Divergence: div(F) = trace(J_F)
        div_sym = sp.simplify(sum(jac_sym[i, i] for i in range(dim)))
        div_val = float(np.trace(jac_num))
        div_latex = rf"\operatorname{{div}}\mathbf{{F}} = \nabla \cdot \mathbf{{F}} = {sp.latex(div_sym)} \quad \Longrightarrow \quad \operatorname{{div}}\mathbf{{F}}(\mathbf{{a}}) = {div_val:.3f}"
        if div_val > 0.02:
            div_meaning = f"🌋 Source / Expanding Fluid (div = +{div_val:.2f} > 0): Fluid expands and diverges outward from point a like a spring or positive charge."
        elif div_val < -0.02:
            div_meaning = f"🕳️ Sink / Compressing Fluid (div = {div_val:.2f} < 0): Fluid converges inward and is drained at point a like a sinkhole or negative charge."
        else:
            div_meaning = f"🌊 Incompressible / Solenoidal (div = {div_val:.2f} ≈ 0): Fluid flows continuously without volume change. Net flux into any small volume enclosing point a is zero."

        # Curl: curl(F) in 2D (scalar / z-component) or 3D (vector)
        if dim == 2:
            curl_sym = sp.simplify(sp.diff(comp_syms[1], x1) - sp.diff(comp_syms[0], x2))
            curl_val = float(jac_num[1, 0] - jac_num[0, 1])
            curl_vec = [0.0, 0.0, curl_val]
            curl_mag = abs(curl_val)
            curl_latex = rf"\operatorname{{curl}}\mathbf{{F}} = \frac{{\partial F_2}}{{\partial x_1}} - \frac{{\partial F_1}}{{\partial x_2}} = {sp.latex(curl_sym)} \quad \Longrightarrow \quad \operatorname{{curl}}\mathbf{{F}}(\mathbf{{a}}) = {curl_val:.3f}"
            if curl_val > 0.02:
                curl_meaning = f"🔄 Counter-Clockwise (CCW) Rotation: A microscopic paddle wheel placed at point a will spin CCW with vorticity curl = +{curl_val:.2f} (angular velocity ω ≈ {curl_val/2:.2f} rad/s)."
            elif curl_val < -0.02:
                curl_meaning = f"🔄 Clockwise (CW) Rotation: A microscopic paddle wheel placed at point a will spin CW with vorticity curl = {curl_val:.2f} (angular velocity ω ≈ {abs(curl_val)/2:.2f} rad/s)."
            else:
                curl_meaning = f"⚪ Irrotational / Curl-Free: Paddle wheel remains stationary! (curl = {curl_val:.2f} ≈ 0). There is no local rotational circulation around point a."
        else:
            cx_sym = sp.simplify(sp.diff(comp_syms[2], x2) - sp.diff(comp_syms[1], x3))
            cy_sym = sp.simplify(sp.diff(comp_syms[0], x3) - sp.diff(comp_syms[2], x1))
            cz_sym = sp.simplify(sp.diff(comp_syms[1], x1) - sp.diff(comp_syms[0], x2))
            cx_val = float(jac_num[2, 1] - jac_num[1, 2])
            cy_val = float(jac_num[0, 2] - jac_num[2, 0])
            cz_val = float(jac_num[1, 0] - jac_num[0, 1])
            curl_vec = [cx_val, cy_val, cz_val]
            curl_mag = float(np.linalg.norm(curl_vec))
            curl_val = cz_val
            curl_latex = rf"\nabla \times \mathbf{{F}} = \begin{{bmatrix}} {sp.latex(cx_sym)} \\ {sp.latex(cy_sym)} \\ {sp.latex(cz_sym)} \end{{bmatrix}} \quad \Longrightarrow \quad \nabla \times \mathbf{{F}}(\mathbf{{a}}) = \begin{{bmatrix}} {cx_val:.2f} \\ {cy_val:.2f} \\ {cz_val:.2f} \end{{bmatrix}}, \; \|\nabla \times \mathbf{{F}}\| = {curl_mag:.3f}"
            if curl_mag > 0.02:
                curl_meaning = f"🔄 3D Rotation along axis ⟨{cx_val:.2f}, {cy_val:.2f}, {cz_val:.2f}⟩ with vorticity magnitude {curl_mag:.2f}. Thumb points along curl vector, fingers curl with rotation."
            else:
                curl_meaning = "⚪ Irrotational in ℝ³: ∇ × F ≈ 0. Zero microscopic rotation around any axis."

        # Potential Function & Conservative Field test
        pot_info = find_potential_function(comp_syms, vars_tuple)
        is_conservative = pot_info["is_conservative"]
        if is_conservative:
            potential_meaning = "⚡ Conservative Vector Field (F = ∇φ): Path Independent! Any line integral between two points depends ONLY on endpoints: ∫_C F·dr = φ(b) - φ(a). Circulation along any closed loop is strictly zero!"
        else:
            potential_meaning = "🚫 Non-Conservative Field: Circulation exists! Curl ≠ 0, so work depends on the chosen path, and closed loop line integrals can be non-zero (Green's Theorem circulation)."

        # Line Integral Analysis along closed loop (default radius 1.5 at center (a1, a2) or origin)
        line_int_center = (0.0, 0.0) if (abs(a1) < 0.1 and abs(a2) < 0.1) else (a1, a2)
        line_int_info = compute_line_integral(
            comp_fns=comp_fns,
            dim=dim,
            curve_type="circle",
            center=line_int_center,
            radius=1.5,
            p0=(0.0, 0.0),
            p1=(a1, a2),
            a3=a3,
            potential_fn=pot_info.get("phi_fn"),
            is_conservative=is_conservative,
            curl_val=curl_val,
        )

        vec_tex_rows = " \\\\ ".join(sp.latex(cs) for cs in comp_syms)
        f_latex = rf"\mathbf{{F}}({v1_tex}, {v2_tex}{', ' + v3_tex if dim == 3 else ''}) = \begin{{bmatrix}} {vec_tex_rows} \end{{bmatrix}}"
        if constraint_info["active"]:
            f_latex += rf" \quad \left[\text{{s.t. }} {constraint_info['latex']}\right]"

        jac_sym_rows = " \\\\ ".join(" & ".join(sp.latex(jac_sym[r, c]) for c in range(dim)) for r in range(dim))
        jac_num_rows = " \\\\ ".join(" & ".join(f"{jac_num[r, c]:.2f}" for c in range(dim)) for r in range(dim))
        fa_vec_rows = " \\\\ ".join(f"{v:.2f}" for v in f_at_a)

        return {
            "mode": f"vector_{dim}d",
            "dim": dim,
            "comp_syms": comp_syms,
            "comp_fns": comp_fns,
            "f_at_a_vec": f_at_a,
            "jacobian_num": jac_num,
            "is_identity_vector": is_identity_vector,
            "raw_expr": raw_expr,
            "f_latex": f_latex,
            "df_symbolic_latex": rf"\mathbf{{J}}_F = \begin{{bmatrix}} {jac_sym_rows} \end{{bmatrix}}_{{{dim} \times {dim}}}",
            "df_numeric_latex": rf"\mathbf{{J}}_F(\mathbf{{a}}) = \begin{{bmatrix}} {jac_num_rows} \end{{bmatrix}}_{{{dim} \times {dim}}}",
            "grad_latex": rf"\mathbf{{F}}(\mathbf{{a}}) = \begin{{bmatrix}} {fa_vec_rows} \end{{bmatrix}}, \quad \|\mathbf{{F}}(\mathbf{{a}})\| = {mag_fa:.3f}",
            "affine_symbolic_latex": r"\mathbf{g}(\mathbf{x}) = \mathbf{F}(\mathbf{a}) + \mathbf{J}_F(\mathbf{a})(\mathbf{x} - \mathbf{a})",
            "affine_numeric_latex": rf"\operatorname{{div}}\mathbf{{F}}(\mathbf{{a}}) = {div_val:.3f}, \quad \operatorname{{curl}}\mathbf{{F}}(\mathbf{{a}}) = {curl_val:.3f}",
            "hessian_symbolic_latex": rf"\mathbf{{J}}_F = \begin{{bmatrix}} {jac_sym_rows} \end{{bmatrix}}",
            "hessian_numeric_latex": rf"\det(\mathbf{{J}}_F) = {det_j:.3f}, \quad \operatorname{{tr}}(\mathbf{{J}}_F) = {div_val:.3f}",
            "fa": mag_fa,
            "fx1": f_at_a[0],
            "fx2": f_at_a[1],
            "fx3": f_at_a[2] if dim == 3 else 0.0,
            "grad_mag": mag_fa,
            "unit_normal_2d": (1.0, 0.0),
            "unit_tangent_2d": (0.0, 1.0),
            "surface_normal_3d": (0.0, 0.0, 1.0),
            "level_c": level_c,
            "radius_r": math.sqrt(max(0.0, level_c)),
            "level_diff": abs(mag_fa - level_c),
            "test_x": test_x,
            "test_y": test_y,
            "test_exact": mag_fa,
            "test_affine": mag_fa,
            "test_error": 0.0,
            "h11": jac_num[0, 0],
            "h22": jac_num[1, 1],
            "h12": jac_num[0, 1],
            "hessian_det": det_j,
            "hessian_trace": div_val,
            "eigenvalues_str": f"div = {div_val:.2f}, curl = {curl_val:.2f}",
            "extremum_type": "vector_field",
            "extremum_label": (
                f"3D Cylindrical Surface (Free Variable {','.join(constraint_info['free_vars'])})"
                if (is_identity_vector and constraint_info["active"])
                else f"{dim}D Vector Field • det(J)={det_j:.2f}, div(F)={div_val:.2f}, curl={curl_val:.2f}"
            ),
            "extremum_badge": "emerald" if (is_identity_vector and constraint_info["active"]) else "cyan",
            "constraint": constraint_info,
            "v1_tex": v1_tex,
            "v2_tex": v2_tex,
            "v3_tex": v3_tex,
            # Dedicated Vector Calculus derivations & values:
            "is_vector_field": True,
            "vars_tuple": vars_tuple,
            "comp_funcs": comp_fns,
            "div_val": div_val,
            "div_latex": div_latex,
            "div_meaning": div_meaning,
            "div_interpretation": div_meaning,
            "curl_val": curl_val,
            "curl_scalar_val": curl_val,
            "curl_vec": curl_vec,
            "curl_vector_vals": curl_vec,
            "curl_mag": curl_mag,
            "curl_latex": curl_latex,
            "curl_meaning": curl_meaning,
            "curl_interpretation": curl_meaning,
            "is_conservative": is_conservative,
            "potential": pot_info,
            "potential_fn": pot_info.get("phi_fn"),
            "potential_func": pot_info.get("phi_fn"),
            "potential_latex": pot_info.get("phi_latex"),
            "potential_derivation_latex": pot_info.get("derivation_latex"),
            "potential_meaning": potential_meaning,
            "line_integral": line_int_info,
        }

    # -------------------------------------------------------------------------
    # CASE 3: Scalar Function in R2 or R3: f(x1, x2) or f(x1, x2, x3)
    # -------------------------------------------------------------------------
    norm_f = normalize_math_expr(raw_expr, params)
    try:
        f_sym = sp.sympify(norm_f)
    except Exception:
        f_sym = x1**2 + x2**2

    has_x3 = x3 in f_sym.free_symbols
    dim = 3 if has_x3 else 2

    df_dx1 = sp.diff(f_sym, x1)
    df_dx2 = sp.diff(f_sym, x2)
    df_dx3 = sp.diff(f_sym, x3) if has_x3 else sp.Integer(0)

    f11_sym = sp.diff(df_dx1, x1)
    f22_sym = sp.diff(df_dx2, x2)
    f12_sym = sp.diff(df_dx1, x2)

    pt_subs = {x1: a1, x2: a2, x3: a3}

    def safe_eval(sym_expr, subs_dict) -> float:
        try:
            val = complex(sym_expr.subs(subs_dict).evalf())
            return float(val.real) if abs(val.imag) < 1e-7 else 0.0
        except Exception:
            return 0.0

    fa_val = safe_eval(f_sym, pt_subs)
    fx1_val = safe_eval(df_dx1, pt_subs)
    fx2_val = safe_eval(df_dx2, pt_subs)
    fx3_val = safe_eval(df_dx3, pt_subs) if has_x3 else 0.0

    grad_mag = math.sqrt(fx1_val**2 + fx2_val**2 + fx3_val**2)
    mag_2d = math.sqrt(fx1_val**2 + fx2_val**2)
    unit_normal_2d = (fx1_val / mag_2d, fx2_val / mag_2d) if mag_2d > 1e-6 else (0.0, 0.0)
    unit_tangent_2d = (-fx2_val / mag_2d, fx1_val / mag_2d) if mag_2d > 1e-6 else (0.0, 0.0)
    surface_normal_3d = (-fx1_val, -fx2_val, 1.0)

    # Hessian 2x2 (or 3x3)
    h11 = safe_eval(f11_sym, pt_subs)
    h22 = safe_eval(f22_sym, pt_subs)
    h12 = safe_eval(f12_sym, pt_subs)
    hess_det = h11 * h22 - h12**2
    hess_trace = h11 + h22

    try:
        eig_vals = np.linalg.eigvalsh(np.array([[h11, h12], [h12, h22]], dtype=float))
        eig_str = f"λ₁ = {eig_vals[0]:.2f}, λ₂ = {eig_vals[1]:.2f}"
    except Exception:
        eig_str = "N/A"

    # Second Derivative Test Classification
    if grad_mag < 1e-2:
        if hess_det > 1e-4 and h11 > 0:
            extremum_type = "local_min"
            extremum_label = "🟢 Local Minimum (∇f = 0, D > 0, f₁₁ > 0)"
            extremum_badge = "emerald"
        elif hess_det > 1e-4 and h11 < 0:
            extremum_type = "local_max"
            extremum_label = "🔴 Local Maximum (∇f = 0, D > 0, f₁₁ < 0)"
            extremum_badge = "rose"
        elif hess_det < -1e-4:
            extremum_type = "saddle"
            extremum_label = "🟡 Saddle Point (∇f = 0, D < 0)"
            extremum_badge = "amber"
        else:
            extremum_type = "inconclusive"
            extremum_label = "⚪ Critical Point — Inconclusive (D ≈ 0)"
            extremum_badge = "cyan"
    else:
        extremum_type = "not_critical"
        extremum_label = f"⚪ Sloping Surface (‖∇f(a)‖ = {grad_mag:.3f} ≠ 0)"
        extremum_badge = "violet"

    # Linearization / Affine Approximation at test point
    test_exact = safe_eval(f_sym, {x1: test_x, x2: test_y, x3: a3})
    test_affine = fa_val + fx1_val * (test_x - a1) + fx2_val * (test_y - a2)
    test_error = abs(test_exact - test_affine)

    # Fast numpy lambdified function
    f_fn_2d = sp.lambdify((x1, x2), f_sym.subs(x3, a3), "numpy")
    f_fn_3d = sp.lambdify((x1, x2, x3), f_sym, "numpy") if has_x3 else None

    # LaTeX formatting
    f_tex_body = sp.latex(f_sym)
    if notation == "xyz":
        f_tex_body = f_tex_body.replace("x_{1}", "x").replace("x_{2}", "y").replace("x_{3}", "z")

    vars_header = f"{v1_tex}, {v2_tex}, {v3_tex}" if has_x3 else f"{v1_tex}, {v2_tex}"
    f_latex = rf"f({vars_header}) = {f_tex_body}"
    if constraint_info["active"]:
        f_latex += rf" \quad \left[\text{{s.t. }} {constraint_info['latex']}\right]"

    if has_x3:
        df_sym_tex = rf"\mathbf{{D}}f = \begin{{bmatrix}} {sp.latex(df_dx1)} & {sp.latex(df_dx2)} & {sp.latex(df_dx3)} \end{{bmatrix}}_{{1 \times 3}}"
        df_num_tex = rf"\mathbf{{D}}f(\mathbf{{a}}) = \begin{{bmatrix}} {fx1_val:.3f} & {fx2_val:.3f} & {fx3_val:.3f} \end{{bmatrix}}_{{1 \times 3}}"
        grad_tex = rf"\nabla f(\mathbf{{a}}) = \begin{{bmatrix}} {fx1_val:.3f} \\ {fx2_val:.3f} \\ {fx3_val:.3f} \end{{bmatrix}}_{{3 \times 1}}"
    else:
        df_sym_tex = rf"\mathbf{{D}}f = \begin{{bmatrix}} {sp.latex(df_dx1)} & {sp.latex(df_dx2)} \end{{bmatrix}}_{{1 \times 2}}"
        df_num_tex = rf"\mathbf{{D}}f(\mathbf{{a}}) = \begin{{bmatrix}} {fx1_val:.3f} & {fx2_val:.3f} \end{{bmatrix}}_{{1 \times 2}}"
        grad_tex = rf"\nabla f(\mathbf{{a}}) = (\mathbf{{D}}f(\mathbf{{a}}))^T = \begin{{bmatrix}} {fx1_val:.3f} \\ {fx2_val:.3f} \end{{bmatrix}}_{{2 \times 1}}"

    sign_a1 = f"- {a1:.2f}" if a1 >= 0 else f"+ {abs(a1):.2f}"
    sign_a2 = f"- {a2:.2f}" if a2 >= 0 else f"+ {abs(a2):.2f}"
    affine_sym_tex = r"g(\mathbf{x}) = f(\mathbf{a}) + \mathbf{D}f(\mathbf{a})(\mathbf{x} - \mathbf{a})"
    affine_num_tex = rf"g({v1_tex}, {v2_tex}) = {fa_val:.3f} + ({fx1_val:.3f})({v1_tex} {sign_a1}) + ({fx2_val:.3f})({v2_tex} {sign_a2})"

    hess_sym_tex = rf"\mathbf{{H}}_f = \begin{{bmatrix}} {sp.latex(f11_sym)} & {sp.latex(f12_sym)} \\ {sp.latex(f12_sym)} & {sp.latex(f22_sym)} \end{{bmatrix}}_{{2 \times 2}}"
    hess_num_tex = rf"\mathbf{{H}}_f(\mathbf{{a}}) = \begin{{bmatrix}} {h11:.3f} & {h12:.3f} \\ {h12:.3f} & {h22:.3f} \end{{bmatrix}}, \quad D = {hess_det:.3f}"

    return {
        "mode": "scalar_3d" if has_x3 else "scalar_2d",
        "dim": dim,
        "f_sym": f_sym,
        "f_fn_2d": f_fn_2d,
        "f_fn_3d": f_fn_3d,
        "is_identity_vector": False,
        "raw_expr": raw_expr,
        "f_latex": f_latex,
        "df_symbolic_latex": df_sym_tex,
        "df_numeric_latex": df_num_tex,
        "grad_latex": grad_tex,
        "affine_symbolic_latex": affine_sym_tex,
        "affine_numeric_latex": affine_num_tex,
        "hessian_symbolic_latex": hess_sym_tex,
        "hessian_numeric_latex": hess_num_tex,
        "fa": fa_val,
        "fx1": fx1_val,
        "fx2": fx2_val,
        "fx3": fx3_val,
        "grad_mag": grad_mag,
        "unit_normal_2d": unit_normal_2d,
        "unit_tangent_2d": unit_tangent_2d,
        "surface_normal_3d": surface_normal_3d,
        "level_c": level_c,
        "radius_r": math.sqrt(max(0.0, level_c)),
        "level_diff": abs(fa_val - level_c),
        "test_x": test_x,
        "test_y": test_y,
        "test_exact": test_exact,
        "test_affine": test_affine,
        "test_error": test_error,
        "h11": h11,
        "h22": h22,
        "h12": h12,
        "hessian_det": hess_det,
        "hessian_trace": hess_trace,
        "eigenvalues_str": eig_str,
        "extremum_type": extremum_type,
        "extremum_label": extremum_label,
        "extremum_badge": extremum_badge,
        "constraint": constraint_info,
        "v1_tex": v1_tex,
        "v2_tex": v2_tex,
        "v3_tex": v3_tex,
    }


def snap_point_to_level_curve(
    calc: Dict[str, Any], a1: float, a2: float, level_c: float
) -> Tuple[float, float]:
    """Projects (a1, a2) onto the level curve f(x1, x2) = c using damped Newton-Gradient steps."""
    if calc["mode"] != "scalar_2d":
        return a1, a2
    f_sym = calc["f_sym"]
    x1, x2, x3 = sp.symbols("x1 x2 x3")
    df1 = sp.diff(f_sym, x1)
    df2 = sp.diff(f_sym, x2)

    cur_x, cur_y = float(a1), float(a2)
    if abs(cur_x) < 1e-4 and abs(cur_y) < 1e-4:
        cur_x = 1.0

    for _ in range(12):
        subs = {x1: cur_x, x2: cur_y, x3: 0.0}
        try:
            f_val = float(f_sym.subs(subs).evalf())
            gx = float(df1.subs(subs).evalf())
            gy = float(df2.subs(subs).evalf())
        except Exception:
            break
        err = f_val - level_c
        if abs(err) < 1e-5:
            break
        g_norm2 = gx * gx + gy * gy
        if g_norm2 < 1e-8:
            break
        cur_x -= (err / g_norm2) * gx
        cur_y -= (err / g_norm2) * gy

    return round(cur_x, 3), round(cur_y, 3)


def snap_point_to_critical(calc: Dict[str, Any], a1: float, a2: float) -> Tuple[float, float]:
    """Finds nearest critical point (∇f = 0) via Newton's method on the gradient."""
    if calc["mode"] != "scalar_2d":
        return 0.0, 0.0
    f_sym = calc["f_sym"]
    x1, x2, x3 = sp.symbols("x1 x2 x3")
    df1 = sp.diff(f_sym, x1)
    df2 = sp.diff(f_sym, x2)
    f11 = sp.diff(df1, x1)
    f12 = sp.diff(df1, x2)
    f22 = sp.diff(df2, x2)

    cur_x, cur_y = float(a1), float(a2)
    for _ in range(15):
        subs = {x1: cur_x, x2: cur_y, x3: 0.0}
        try:
            gx = float(df1.subs(subs).evalf())
            gy = float(df2.subs(subs).evalf())
            if math.hypot(gx, gy) < 1e-5:
                return round(cur_x, 3), round(cur_y, 3)
            h11 = float(f11.subs(subs).evalf())
            h12 = float(f12.subs(subs).evalf())
            h22 = float(f22.subs(subs).evalf())
            det = h11 * h22 - h12 * h12
            if abs(det) < 1e-8:
                break
            dx = (h22 * gx - h12 * gy) / det
            dy = (-h12 * gx + h11 * gy) / det
            cur_x -= dx
            cur_y -= dy
        except Exception:
            break
    return 0.0, 0.0


def compute_flow_line(
    calc: Dict[str, Any],
    a1: float,
    a2: float,
    a3: float = 0.0,
    x_range: Tuple[float, float] = (-6.0, 6.0),
    y_range: Tuple[float, float] = (-6.0, 6.0),
    steps: int = 85,
) -> Tuple[List[float], List[float], List[float]]:
    """
    Computes the integral curve / flow line γ(t) passing through γ(0) = a = (a1, a2)
    by solving γ'(t) = V(γ(t)) forward (t >= 0) and backward (t <= 0) using RK4:
    - For scalar functions f(x1, x2): V(x) = ∇f(x) (steepest ascent/descent curve, orthogonal to level sets)
    - For vector fields F(x): V(x) = F(x)
    - For matrices A: V(x) = A x
    Returns (xs_flow, ys_flow, zs_flow).
    """
    mode = calc["mode"]
    x1_sym, x2_sym, x3_sym = sp.symbols("x1 x2 x3")

    if mode == "scalar_2d":
        f_sym = calc["f_sym"]
        df1_fn = sp.lambdify((x1_sym, x2_sym), sp.diff(f_sym, x1_sym).subs(x3_sym, 0), "numpy")
        df2_fn = sp.lambdify((x1_sym, x2_sym), sp.diff(f_sym, x2_sym).subs(x3_sym, 0), "numpy")

        def _vec(px: float, py: float) -> Tuple[float, float]:
            try:
                vx = float(df1_fn(px, py))
                vy = float(df2_fn(px, py))
                return vx, vy
            except Exception:
                return 0.0, 0.0

    elif mode in ("vector_2d", "vector_3d"):
        c0 = calc["comp_fns"][0]
        c1 = calc["comp_fns"][1]

        def _vec(px: float, py: float) -> Tuple[float, float]:
            try:
                if mode == "vector_2d":
                    return float(c0(px, py)), float(c1(px, py))
                return float(c0(px, py, a3)), float(c1(px, py, a3))
            except Exception:
                return 0.0, 0.0

    elif mode in ("matrix_2d", "matrix_3d"):
        mat = calc["matrix"]

        def _vec(px: float, py: float) -> Tuple[float, float]:
            return float(mat[0, 0] * px + mat[0, 1] * py), float(mat[1, 0] * px + mat[1, 1] * py)

    else:
        return [a1], [a2], [a3]

    dt = (x_range[1] - x_range[0]) * 0.012

    def _trace_dir(sign: float) -> List[Tuple[float, float]]:
        pts: List[Tuple[float, float]] = []
        cx, cy = float(a1), float(a2)
        if abs(cx) < 1e-4 and abs(cy) < 1e-4:
            cx, cy = 0.25, 0.25
        for _ in range(steps):
            if not (x_range[0] <= cx <= x_range[1] and y_range[0] <= cy <= y_range[1]):
                break
            vx1, vy1 = _vec(cx, cy)
            m1 = math.hypot(vx1, vy1)
            if m1 < 1e-5:
                break
            ux1, uy1 = (vx1 / m1) * sign, (vy1 / m1) * sign

            vx2, vy2 = _vec(cx + 0.5 * dt * ux1, cy + 0.5 * dt * uy1)
            m2 = math.hypot(vx2, vy2) or 1.0
            ux2, uy2 = (vx2 / m2) * sign, (vy2 / m2) * sign

            cx += dt * ux2
            cy += dt * uy2
            pts.append((cx, cy))
        return pts

    back_pts = list(reversed(_trace_dir(-1.0)))
    fwd_pts = _trace_dir(1.0)
    full_xy = back_pts + [(float(a1), float(a2))] + fwd_pts

    fx_list = [p[0] for p in full_xy]
    fy_list = [p[1] for p in full_xy]
    fz_list = []
    for px, py in full_xy:
        if mode == "scalar_2d":
            try:
                fz_list.append(float(calc["f_fn_2d"](px, py)))
            except Exception:
                fz_list.append(0.0)
        else:
            fz_list.append(float(a3))

    return fx_list, fy_list, fz_list


# =============================================================================
# 5. INTERACTIVE PLOTLY 2D & 3D FIGURE BUILDER (WITH ANIMATIONS)
# =============================================================================
def build_plotly_figure(
    calc: Dict[str, Any],
    a1: float = 2.0,
    a2: float = 0.0,
    a3: float = 0.0,
    level_c: float = 4.0,
    test_x: float = 2.1,
    test_y: float = 0.2,
    x_range: Tuple[float, float] = (-6.0, 6.0),
    y_range: Tuple[float, float] = (-6.0, 6.0),
    view_mode: str = "Split Dual View",
    anim_mode: str = "none",
    color_scale: str = "Viridis",
    opacity: float = 0.85,
    theme: str = "light",
    show_gradient: bool = True,
    show_tangent_line: bool = True,
    show_normal_line: bool = True,
    show_right_angle: bool = True,
    show_affine_plane: bool = True,
    show_3d_normal: bool = True,
    show_error_rod: bool = False,
    show_all_contours: bool = True,
    show_constraint_surface: bool = True,
    show_constraint_curve: bool = True,
    show_flow_line: bool = False,
    show_curl_wheel: bool = True,
    show_div_bubble: bool = True,
    show_equipotential: bool = True,
    show_line_integral: bool = True,
    grid_res: int = 48,
) -> go.Figure:
    """
    Builds the complete 2D, 3D, or Split Dual View Plotly figure with all geometric overlays
    and client-side animation frames.
    """
    is_dark = theme == "dark"
    template_name = "plotly_dark" if is_dark else "plotly_white"
    bg_2d = "#090418" if is_dark else "#ffffff"
    paper_bg = "#070314" if is_dark else "#f8f6fc"
    grid_col = "rgba(168,85,247,0.18)" if is_dark else "rgba(124,58,237,0.12)"
    text_col = "#f3e8ff" if is_dark else "#1e1b4b"

    mode = calc["mode"]
    constraint_info = calc["constraint"]
    xs = np.linspace(x_range[0], x_range[1], grid_res)
    ys = np.linspace(y_range[0], y_range[1], grid_res)
    X, Y = np.meshgrid(xs, ys)

    # Evaluate scalar surface Z if applicable
    Z = np.zeros_like(X)
    if mode == "scalar_2d":
        try:
            Z_raw = calc["f_fn_2d"](X, Y)
            if np.isscalar(Z_raw):
                Z = np.full_like(X, float(Z_raw))
            else:
                Z = np.array(Z_raw, dtype=float)
        except Exception:
            Z = X**2 + Y**2
    elif mode in ("vector_2d", "vector_3d"):
        try:
            if mode == "vector_2d":
                U = np.asarray(calc["comp_fns"][0](X, Y), dtype=float)
                V = np.asarray(calc["comp_fns"][1](X, Y), dtype=float)
                Z = np.sqrt(U**2 + V**2)
            else:
                U = np.asarray(calc["comp_fns"][0](X, Y, a3), dtype=float)
                V = np.asarray(calc["comp_fns"][1](X, Y, a3), dtype=float)
                W = np.asarray(calc["comp_fns"][2](X, Y, a3), dtype=float)
                Z = np.sqrt(U**2 + V**2 + W**2)
        except Exception:
            Z = np.sqrt(X**2 + Y**2)
    elif mode in ("matrix_2d", "matrix_3d"):
        mat = calc["matrix"]
        U = mat[0, 0] * X + mat[0, 1] * Y
        V = mat[1, 0] * X + mat[1, 1] * Y
        Z = np.sqrt(U**2 + V**2)

    # Mask inequality constraints on Z
    if constraint_info["active"] and not constraint_info["is_equality"]:
        try:
            diff_grid = np.asarray(constraint_info["diff_fn"](X, Y), dtype=float)
            op = constraint_info["op"]
            if op == "<=":
                mask = diff_grid <= 1e-6
            elif op == "<":
                mask = diff_grid < 0
            elif op == ">=":
                mask = diff_grid >= -1e-6
            else:
                mask = diff_grid > 0
            Z = np.where(mask, Z, np.nan)
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # A. BUILD 2D TRACES
    # -------------------------------------------------------------------------
    traces_2d: List[Any] = []

    # 1. Interactive Clickable 2D Heatmap + Iso-Contour Lines
    traces_2d.append(
        go.Heatmap(
            x=xs,
            y=ys,
            z=Z,
            colorscale=color_scale,
            zsmooth="best",
            opacity=0.84,
            colorbar=(
                dict(title="f(x)", len=0.85, thickness=14)
                if view_mode == "2D Level Sets"
                else dict(len=0.75, thickness=12, x=1.02)
            ),
            hovertemplate="x₁ = %{x:.3f}<br>x₂ = %{y:.3f}<br>Exact f = %{z:.4f}<extra>Click to set Point a</extra>",
            name="Surface Field (Click to set a)",
        )
    )
    if show_all_contours:
        traces_2d.append(
            go.Contour(
                x=xs,
                y=ys,
                z=Z,
                contours=dict(
                    coloring="none",
                    showlabels=True,
                    labelfont=dict(size=10, color="#ffffff"),
                ),
                line=dict(color="rgba(255,255,255,0.42)", width=1.1),
                showscale=False,
                hoverinfo="skip",
                showlegend=False,
                name="Iso-Contours",
            )
        )

    # 2. Highlighted Level Curve f(x1, x2) = c
    if mode in ("scalar_2d", "scalar_3d"):
        traces_2d.append(
            go.Contour(
                x=xs,
                y=ys,
                z=Z,
                contours=dict(
                    start=level_c,
                    end=level_c,
                    size=1.0,
                    coloring="none",
                    showlabels=True,
                    labelfont=dict(size=12, color="#00ffff" if is_dark else "#4c1d95"),
                ),
                line=dict(color="#00ffff" if is_dark else "#6d28d9", width=4),
                showscale=False,
                name=f"Level Set f = {level_c:.2f}",
            )
        )

    # 3. 2D Vector Field: Quiver Arrows, F(a) Vector, Paddle Wheel, Flux Bubble, Equipotential Contours & Line Integral
    if mode in ("vector_2d", "vector_3d"):
        # 3A. Quiver Arrows
        q_xs = np.linspace(x_range[0] * 0.88, x_range[1] * 0.88, 13)
        q_ys = np.linspace(y_range[0] * 0.88, y_range[1] * 0.88, 13)
        qx_lines, qy_lines = [], []
        scale = (x_range[1] - x_range[0]) / 20.0
        for qx in q_xs:
            for qy in q_ys:
                try:
                    u = float(calc["comp_fns"][0](qx, qy)) if mode == "vector_2d" else float(calc["comp_fns"][0](qx, qy, a3))
                    v = float(calc["comp_fns"][1](qx, qy)) if mode == "vector_2d" else float(calc["comp_fns"][1](qx, qy, a3))
                    m = math.hypot(u, v)
                    if m > 1e-6:
                        ux, uy = (u / m) * scale, (v / m) * scale
                        ex, ey = qx + ux, qy + uy
                        px, py = -uy * 0.28, ux * 0.28
                        qx_lines.extend([qx, ex, None, ex - ux * 0.32 + px, ex, ex - ux * 0.32 - px, None])
                        qy_lines.extend([qy, ey, None, ey - uy * 0.32 + py, ey, ey - uy * 0.32 - py, None])
                except Exception:
                    pass
        traces_2d.append(
            go.Scatter(
                x=qx_lines,
                y=qy_lines,
                mode="lines",
                line=dict(color="#06b6d4" if is_dark else "#4f46e5", width=1.8),
                name="Vector Field Flow F",
            )
        )

        # 3B. Vector F(a) at Point a
        fa_u, fa_v = calc["fx1"], calc["fx2"]
        fa_m = math.hypot(fa_u, fa_v)
        if fa_m > 1e-6:
            vec_scale = (x_range[1] - x_range[0]) * 0.2 / max(fa_m, 1.0)
            end_x = a1 + fa_u * vec_scale
            end_y = a2 + fa_v * vec_scale
            traces_2d.append(
                go.Scatter(
                    x=[a1, end_x],
                    y=[a2, end_y],
                    mode="lines+markers+text",
                    line=dict(color="#f59e0b", width=4.5),
                    marker=dict(size=[0, 10], symbol="triangle-up"),
                    text=["", f"F(a) ‖F‖={fa_m:.2f}"],
                    textposition="top right",
                    name="Vector F(a)",
                )
            )

        # 3C. Equipotential Contours (when Conservative)
        if show_equipotential and calc.get("is_conservative") and calc.get("potential_fn"):
            try:
                Z_phi = np.asarray(calc["potential_fn"](X, Y), dtype=float)
                traces_2d.append(
                    go.Contour(
                        x=xs,
                        y=ys,
                        z=Z_phi,
                        contours=dict(coloring="none", showlabels=True, labelfont=dict(size=10, color="#a855f7")),
                        line=dict(color="#a855f7" if is_dark else "#7c3aed", width=1.8, dash="dot"),
                        showscale=False,
                        name="Equipotential φ(x)=c (F ⊥ Level Sets)",
                    )
                )
            except Exception:
                pass

        # 3D. Paddle Wheel (Rotational Curl Visualizer at Point a)
        curl_v = calc.get("curl_val", 0.0)
        if show_curl_wheel:
            wheel_r = (x_range[1] - x_range[0]) * 0.075
            th_wheel = np.linspace(0, 2 * np.pi, 48)
            wx = a1 + wheel_r * np.cos(th_wheel)
            wy = a2 + wheel_r * np.sin(th_wheel)

            wheel_color = "#f59e0b" if curl_v > 0.02 else ("#ec4899" if curl_v < -0.02 else "#94a3b8")
            wheel_dash = "solid" if abs(curl_v) > 0.02 else "dash"
            spin_label = "CCW" if curl_v > 0.02 else ("CW" if curl_v < -0.02 else "Still")

            # Rim
            traces_2d.append(
                go.Scatter(
                    x=wx.tolist(),
                    y=wy.tolist(),
                    mode="lines",
                    line=dict(color=wheel_color, width=2.5, dash=wheel_dash),
                    name=f"Paddle Wheel (Curl = {curl_v:.2f}, {spin_label})",
                    hovertemplate=f"<b>Paddle Wheel at a</b><br>Curl = {curl_v:.3f}<br>Spin: {spin_label} (ω ≈ {abs(curl_v)/2:.2f} rad/s)<extra></extra>",
                )
            )
            # 4 Spokes (+)
            spoke_x = [a1 - wheel_r, a1 + wheel_r, None, a1, a1, None]
            spoke_y = [a2, a2, None, a2 - wheel_r, a2 + wheel_r, None]
            traces_2d.append(
                go.Scatter(
                    x=spoke_x,
                    y=spoke_y,
                    mode="lines",
                    line=dict(color=wheel_color, width=1.5),
                    showlegend=False,
                    hoverinfo="skip",
                )
            )
            # Tangential arrows on rim
            if abs(curl_v) > 0.02:
                arrow_angles = [0.0, np.pi / 2, np.pi, 3 * np.pi / 2]
                tang_x, tang_y = [], []
                arrow_len = wheel_r * 0.4
                sign_rot = 1.0 if curl_v > 0 else -1.0
                for ang in arrow_angles:
                    bx = a1 + wheel_r * math.cos(ang)
                    by = a2 + wheel_r * math.sin(ang)
                    tx_dir = -math.sin(ang) * sign_rot
                    ty_dir = math.cos(ang) * sign_rot
                    ex = bx + tx_dir * arrow_len
                    ey = by + ty_dir * arrow_len
                    px = -ty_dir * 0.28 * arrow_len
                    py = tx_dir * 0.28 * arrow_len
                    tang_x.extend([bx, ex, None, ex - tx_dir * 0.35 * arrow_len + px, ex, ex - tx_dir * 0.35 * arrow_len - px, None])
                    tang_y.extend([by, ey, None, ey - ty_dir * 0.35 * arrow_len + py, ey, ey - ty_dir * 0.35 * arrow_len - py, None])
                traces_2d.append(
                    go.Scatter(
                        x=tang_x,
                        y=tang_y,
                        mode="lines",
                        line=dict(color=wheel_color, width=2.5),
                        showlegend=False,
                        hoverinfo="skip",
                    )
                )

        # 3E. Divergence Flux Ring at Point a
        div_v = calc.get("div_val", 0.0)
        if show_div_bubble and abs(div_v) > 0.02:
            bub_r = (x_range[1] - x_range[0]) * 0.05
            bub_col = "#10b981" if div_v > 0 else "#ef4444"
            div_label = "Source (Expanding)" if div_v > 0 else "Sink (Compressing)"
            rad_x, rad_y = [], []
            r_angles = [0.0, np.pi / 2, np.pi, 3 * np.pi / 2]
            arrow_len = bub_r * 0.6
            dir_sign = 1.0 if div_v > 0 else -1.0
            for ang in r_angles:
                rx = math.cos(ang)
                ry = math.sin(ang)
                bx = a1 + bub_r * rx
                by = a2 + bub_r * ry
                ex = bx + rx * arrow_len * dir_sign
                ey = by + ry * arrow_len * dir_sign
                px = -ry * 0.28 * arrow_len
                py = rx * 0.28 * arrow_len
                rad_x.extend([bx, ex, None, ex - rx * 0.35 * arrow_len * dir_sign + px, ex, ex - rx * 0.35 * arrow_len * dir_sign - px, None])
                rad_y.extend([by, ey, None, ey - ry * 0.35 * arrow_len * dir_sign + py, ey, ey - ry * 0.35 * arrow_len * dir_sign - py, None])
            traces_2d.append(
                go.Scatter(
                    x=rad_x,
                    y=rad_y,
                    mode="lines",
                    line=dict(color=bub_col, width=2.2),
                    name=f"Flux Ring (Div = {div_v:.2f}, {div_label})",
                    hovertemplate=f"<b>Flux Ring at a</b><br>Div = {div_v:.3f}<br>{div_label}<extra></extra>",
                )
            )

        # 3F. Line Integral Curve C
        if show_line_integral and "line_integral" in calc:
            li = calc["line_integral"]
            traces_2d.append(
                go.Scatter(
                    x=li["xs"],
                    y=li["ys"],
                    mode="lines",
                    line=dict(color="#d946ef" if is_dark else "#9333ea", width=3.5, dash="dash" if not li["is_closed"] else "solid"),
                    name=f"Path C: W = {li['work']:.2f}",
                    hovertemplate=(
                        f"<b>Line Integral Path C</b><br>"
                        f"Curve: {li['curve_name']}<br>"
                        f"Work W = ∫_C F·dr = <b>{li['work']:.3f}</b>"
                        + (f"<br>Green's Thm ∬ curl dA = {li['greens_circulation']:.3f}" if li.get("greens_circulation") is not None else "")
                        + (f"<br>Potential Δφ = {li['delta_phi']:.3f}" if li.get("delta_phi") is not None else "")
                        + "<extra></extra>"
                    ),
                )
            )
            # Start and End markers on curve
            traces_2d.append(
                go.Scatter(
                    x=[li["xs"][0], li["xs"][-1]],
                    y=[li["ys"][0], li["ys"][-1]],
                    mode="markers+text",
                    marker=dict(size=[9, 9], color=["#10b981", "#ef4444"], symbol=["circle", "square"]),
                    text=["r(0)", "r(1)"] if not li["is_closed"] else ["r(0)=r(2π)", ""],
                    textposition="bottom right",
                    showlegend=False,
                    name="Curve Endpoints",
                )
            )

    if mode in ("matrix_2d", "matrix_3d"):
        mat = calc["matrix"]
        # Transformed unit circle
        th = np.linspace(0, 2 * np.pi, 100)
        uc_x, uc_y = np.cos(th), np.sin(th)
        tc_x = mat[0, 0] * uc_x + mat[0, 1] * uc_y
        tc_y = mat[1, 0] * uc_x + mat[1, 1] * uc_y
        traces_2d.append(
            go.Scatter(
                x=uc_x, y=uc_y, mode="lines",
                line=dict(color="#94a3b8", width=2, dash="dot"),
                name="Unit Circle ‖x‖=1",
            )
        )
        traces_2d.append(
            go.Scatter(
                x=tc_x, y=tc_y, mode="lines",
                line=dict(color="#ec4899", width=3.5),
                name="Transformed Ellipse A(Unit Circle)",
            )
        )
        # Column basis vectors c1, c2
        traces_2d.append(
            go.Scatter(
                x=[0, mat[0, 0]], y=[0, mat[1, 0]],
                mode="lines+markers+text",
                line=dict(color="#ef4444", width=4),
                marker=dict(size=[4, 10]),
                text=["", f"c₁=({mat[0,0]:g},{mat[1,0]:g})"],
                textposition="top right",
                name="Column 1 (A·e₁)",
            )
        )
        traces_2d.append(
            go.Scatter(
                x=[0, mat[0, 1]], y=[0, mat[1, 1]],
                mode="lines+markers+text",
                line=dict(color="#10b981", width=4),
                marker=dict(size=[4, 10]),
                text=["", f"c₂=({mat[0,1]:g},{mat[1,1]:g})"],
                textposition="top right",
                name="Column 2 (A·e₂)",
            )
        )

    # 4. Constraint 2D Curve
    if constraint_info["active"] and show_constraint_curve and constraint_info["polylines"]:
        cx_all, cy_all = [], []
        for px, py in constraint_info["polylines"]:
            cx_all.extend(px.tolist() + [None])
            cy_all.extend(py.tolist() + [None])
        traces_2d.append(
            go.Scatter(
                x=cx_all,
                y=cy_all,
                mode="lines",
                line=dict(color="#06b6d4", width=4, dash="solid" if constraint_info["is_equality"] else "dash"),
                name=f"Constraint ({constraint_info['raw']})",
            )
        )

    # 5. Tangent Line, Normal Line, 90° Right-Angle Symbol, and Gradient Vector at Point a
    nx_u, ny_u = calc["unit_normal_2d"]
    tx_u, ty_u = calc["unit_tangent_2d"]
    span = (x_range[1] - x_range[0]) * 0.45

    if show_tangent_line and ( abs(tx_u) > 1e-6 or abs(ty_u) > 1e-6 ):
        traces_2d.append(
            go.Scatter(
                x=[a1 - tx_u * span, a1 + tx_u * span],
                y=[a2 - ty_u * span, a2 + ty_u * span],
                mode="lines",
                line=dict(color="#ec4899", width=3, dash="dash"),
                name="Tangent Line",
            )
        )

    if show_normal_line and (abs(nx_u) > 1e-6 or abs(ny_u) > 1e-6):
        traces_2d.append(
            go.Scatter(
                x=[a1 - nx_u * span, a1 + nx_u * span],
                y=[a2 - ny_u * span, a2 + ny_u * span],
                mode="lines",
                line=dict(color="#10b981", width=3),
                name="Normal Line (90°)",
            )
        )

    # 90-degree orthogonality square marker
    if show_right_angle and show_tangent_line and show_normal_line and (abs(nx_u) > 1e-6 or abs(ny_u) > 1e-6):
        sq_sz = (x_range[1] - x_range[0]) * 0.038
        p1 = (a1 + tx_u * sq_sz, a2 + ty_u * sq_sz)
        p2 = (a1 + (tx_u + nx_u) * sq_sz, a2 + (ty_u + ny_u) * sq_sz)
        p3 = (a1 + nx_u * sq_sz, a2 + ny_u * sq_sz)
        traces_2d.append(
            go.Scatter(
                x=[p1[0], p2[0], p3[0]],
                y=[p1[1], p2[1], p3[1]],
                mode="lines",
                line=dict(color="#facc15", width=2.5),
                name="90° Right Angle (∇f ⊥ Tangent)",
            )
        )

    # Gradient Vector Arrow in 2D
    if show_gradient and calc["grad_mag"] > 1e-6:
        g_scale = min(1.0, (x_range[1] - x_range[0]) * 0.22 / max(calc["grad_mag"], 1e-4))
        gx_end = a1 + calc["fx1"] * g_scale
        gy_end = a2 + calc["fx2"] * g_scale
        traces_2d.append(
            go.Scatter(
                x=[a1, gx_end],
                y=[a2, gy_end],
                mode="lines+markers+text",
                line=dict(color="#f59e0b", width=4.5),
                marker=dict(size=[0, 10], symbol="triangle-up"),
                text=["", "∇f(a)"],
                textposition="top right",
                name="Gradient ∇f(a)",
            )
        )

    # Evaluation Point a & Test Point x_test in 2D (Shows exact value f(a))
    traces_2d.append(
        go.Scatter(
            x=[a1],
            y=[a2],
            mode="markers+text",
            marker=dict(size=13, color="#00ffff", line=dict(color="#1e1b4b", width=2.5)),
            text=[f"a=({a1:.2f}, {a2:.2f}) | f={calc['fa']:.3f}"],
            textfont=dict(size=11, color="#0f172a" if not is_dark else "#f8fafc"),
            textposition="bottom right",
            hovertemplate=f"<b>Point a</b><br>x₁ = {a1:.4f}<br>x₂ = {a2:.4f}<br>Exact f(a) = {calc['fa']:.4f}<extra></extra>",
            name="Point a",
        )
    )
    if show_error_rod:
        traces_2d.append(
            go.Scatter(
                x=[a1, test_x],
                y=[a2, test_y],
                mode="lines+markers+text",
                line=dict(color="#a855f7", width=2.5, dash="dot"),
                marker=dict(size=[0, 9], color="#a855f7"),
                text=["", "x_test"],
                textposition="top left",
                name="Displacement Δx = x - a",
            )
        )

    # Flow Line γ(t) in 2D
    flow_xs, flow_ys, flow_zs = [], [], []
    if show_flow_line:
        flow_xs, flow_ys, flow_zs = compute_flow_line(calc, a1, a2, a3, x_range, y_range)
        if len(flow_xs) > 1:
            traces_2d.append(
                go.Scatter(
                    x=flow_xs,
                    y=flow_ys,
                    mode="lines",
                    line=dict(color="#f43f5e", width=3.8),
                    name="Flow Line γ(t)",
                )
            )

    # -------------------------------------------------------------------------
    # B. BUILD 3D TRACES
    # -------------------------------------------------------------------------
    traces_3d: List[Any] = []
    z_min_plot = float(np.nanmin(Z)) if np.any(np.isfinite(Z)) else -5.0
    z_max_plot = float(np.nanmax(Z)) if np.any(np.isfinite(Z)) else 5.0
    if abs(z_max_plot - z_min_plot) < 1e-3:
        z_min_plot, z_max_plot = -5.0, 5.0

    is_cyl_only = calc["is_identity_vector"] and constraint_info["active"]

    # 1. 3D Matrix Visualization (for 3x3 matrix in R3 or 2x2 matrix lifted to R3)
    if mode == "matrix_3d":
        mat = calc["matrix"]
        cols_colors = [("#ef4444", "c₁ = A·e₁"), ("#10b981", "c₂ = A·e₂"), ("#3b82f6", "c₃ = A·e₃")]
        for c_idx, (col_hex, col_lbl) in enumerate(cols_colors):
            vx, vy, vz = float(mat[0, c_idx]), float(mat[1, c_idx]), float(mat[2, c_idx])
            traces_3d.append(
                go.Scatter3d(
                    x=[0, vx],
                    y=[0, vy],
                    z=[0, vz],
                    mode="lines+markers+text",
                    line=dict(color=col_hex, width=8),
                    marker=dict(size=[3, 7], color=col_hex),
                    text=["", f"{col_lbl}=({vx:g},{vy:g},{vz:g})"],
                    name=col_lbl,
                )
            )
        # Transformed point T(a) = A * a
        ta = calc["transformed_a"]
        traces_3d.append(
            go.Scatter3d(
                x=[0, a1], y=[0, a2], z=[0, a3],
                mode="lines+markers+text",
                line=dict(color="#00ffff", width=5, dash="dash"),
                marker=dict(size=[2, 6], color="#00ffff"),
                text=["", f"a=({a1:.1f},{a2:.1f},{a3:.1f})"],
                name="Input Vector a",
            )
        )
        traces_3d.append(
            go.Scatter3d(
                x=[0, float(ta[0])], y=[0, float(ta[1])], z=[0, float(ta[2])],
                mode="lines+markers+text",
                line=dict(color="#f59e0b", width=8),
                marker=dict(size=[3, 8], color="#f59e0b", symbol="diamond"),
                text=["", f"A·a=({ta[0]:.1f},{ta[1]:.1f},{ta[2]:.1f})"],
                name="Transformed Vector A·a",
            )
        )

    # 2. 3D Implicit Level Surface f(x1, x2, x3) = c
    elif mode == "scalar_3d" and calc["f_fn_3d"] is not None:
        iso_res = 22
        ix = np.linspace(x_range[0], x_range[1], iso_res)
        iy = np.linspace(y_range[0], y_range[1], iso_res)
        iz = np.linspace(x_range[0], x_range[1], iso_res)
        IX, IY, IZ = np.meshgrid(ix, iy, iz)
        try:
            IV = np.asarray(calc["f_fn_3d"](IX, IY, IZ), dtype=float)
            traces_3d.append(
                go.Isosurface(
                    x=IX.flatten(),
                    y=IY.flatten(),
                    z=IZ.flatten(),
                    value=IV.flatten(),
                    isomin=level_c,
                    isomax=level_c,
                    surface_count=1,
                    colorscale=color_scale,
                    opacity=opacity,
                    showscale=False,
                    name=f"3D Level Surface f = {level_c:.2f}",
                )
            )
        except Exception:
            pass

    # 3. Standard 3D Surface z = f(x1, x2) (skipped when identity vector + constraint cylinder is primary)
    elif not is_cyl_only:
        traces_3d.append(
            go.Surface(
                x=X,
                y=Y,
                z=Z,
                colorscale=color_scale,
                opacity=opacity,
                showscale=False,
                contours_z=dict(
                    show=show_all_contours,
                    usecolormap=True,
                    highlightcolor="#ffffff",
                    project_z=True,
                ),
                name="Surface z = f(x₁, x₂)",
            )
        )

    # 4. 3D Extruded Cylinder Surface & 3D Restricted Constraint Curve
    if constraint_info["active"] and constraint_info["polylines"]:
        c_zmin = -5.0 if is_cyl_only else z_min_plot
        c_zmax = 5.0 if is_cyl_only else z_max_plot
        z_levels = np.linspace(c_zmin, c_zmax, 26)

        if show_constraint_surface or is_cyl_only:
            for idx_p, (px, py) in enumerate(constraint_info["polylines"]):
                if len(px) < 2:
                    continue
                CX = np.outer(px, np.ones_like(z_levels))
                CY = np.outer(py, np.ones_like(z_levels))
                CZ = np.outer(np.ones_like(px), z_levels)
                traces_3d.append(
                    go.Surface(
                        x=CX,
                        y=CY,
                        z=CZ,
                        colorscale=[[0, "#06b6d4"], [0.5, "#6366f1"], [1, "#a855f7"]],
                        opacity=0.88 if is_cyl_only else 0.45,
                        showscale=False,
                        contours_z=dict(show=True, width=2, color="#ffffff"),
                        name="3D Cylindrical Surface (Free x₃)" if idx_p == 0 else f"Cylinder Branch {idx_p+1}",
                    )
                )

        if show_constraint_curve and mode == "scalar_2d":
            rx_all, ry_all, rz_all = [], [], []
            for px, py in constraint_info["polylines"]:
                try:
                    pz = np.asarray(calc["f_fn_2d"](px, py), dtype=float)
                    if np.isscalar(pz):
                        pz = np.full_like(px, float(pz))
                    rx_all.extend(px.tolist() + [None])
                    ry_all.extend(py.tolist() + [None])
                    rz_all.extend(pz.tolist() + [None])
                except Exception:
                    pass
            if rx_all:
                traces_3d.append(
                    go.Scatter3d(
                        x=rx_all,
                        y=ry_all,
                        z=rz_all,
                        mode="lines",
                        line=dict(color="#00ffff", width=8),
                        name="Restricted 3D Curve f(Constraint)",
                    )
                )

    # 5. 3D Vector Field Cones (when in vector_3d mode without constraint cylinder)
    if mode == "vector_3d" and not is_cyl_only:
        c_pts = np.linspace(-3.5, 3.5, 4)
        VX, VY, VZ = np.meshgrid(c_pts, c_pts, c_pts)
        try:
            U3 = np.asarray(calc["comp_fns"][0](VX, VY, VZ), dtype=float)
            V3 = np.asarray(calc["comp_fns"][1](VX, VY, VZ), dtype=float)
            W3 = np.asarray(calc["comp_fns"][2](VX, VY, VZ), dtype=float)
            traces_3d.append(
                go.Cone(
                    x=VX.flatten(),
                    y=VY.flatten(),
                    z=VZ.flatten(),
                    u=U3.flatten(),
                    v=V3.flatten(),
                    w=W3.flatten(),
                    sizemode="scaled",
                    sizeref=0.45,
                    colorscale="Viridis",
                    showscale=False,
                    name="3D Vector Field F(x₁,x₂,x₃)",
                )
            )
        except Exception:
            pass

        # 5B. 3D Curl Vector ∇ × F(a) & Perpendicular Rotation Disc
        curl_v3 = calc.get("curl_vec", [0.0, 0.0, 0.0])
        curl_m3 = calc.get("curl_mag", 0.0)
        if curl_m3 > 0.02:
            c_scale = (x_range[1] - x_range[0]) * 0.28 / max(curl_m3, 1.0)
            cx_end = a1 + curl_v3[0] * c_scale
            cy_end = a2 + curl_v3[1] * c_scale
            cz_end = a3 + curl_v3[2] * c_scale
            traces_3d.append(
                go.Scatter3d(
                    x=[a1, cx_end],
                    y=[a2, cy_end],
                    z=[a3, cz_end],
                    mode="lines+markers+text",
                    line=dict(color="#f59e0b", width=8),
                    marker=dict(size=[3, 7], color="#f59e0b", symbol="diamond"),
                    text=["", f"∇×F(a) ‖curl‖={curl_m3:.2f}"],
                    textposition="top center",
                    name="3D Curl Vector ∇×F(a)",
                )
            )

        # 5C. 3D Line Integral Curve
        if show_line_integral and "line_integral" in calc:
            li = calc["line_integral"]
            traces_3d.append(
                go.Scatter3d(
                    x=li["xs"],
                    y=li["ys"],
                    z=li["zs"],
                    mode="lines",
                    line=dict(color="#d946ef", width=6),
                    name=f"3D Path C (W = {li['work']:.2f})",
                )
            )

    # 5D. 3D Vector Field Cones, Curl Vector, Paddle Wheel, Divergence Bubble & Line Integral for 2D Vector Fields
    if mode == "vector_2d":
        # Surface: Potential landscape if conservative, or subtle base plane if general
        if calc.get("is_conservative") and calc.get("potential_fn") and show_equipotential:
            try:
                Z_pot = np.asarray(calc["potential_fn"](X, Y), dtype=float)
                traces_3d.append(
                    go.Surface(
                        x=X,
                        y=Y,
                        z=Z_pot,
                        colorscale=[[0, "#06b6d4"], [0.5, "#8b5cf6"], [1, "#ec4899"]],
                        opacity=0.75,
                        showscale=False,
                        contours_z=dict(show=True, width=1.5, color="#ffffff"),
                        name="3D Potential Landscape z = φ(x₁, x₂)",
                    )
                )
            except Exception:
                pass
        else:
            # Subtle semi-transparent xy reference plane
            traces_3d.append(
                go.Surface(
                    x=X,
                    y=Y,
                    z=np.zeros_like(X),
                    colorscale=[[0, "rgba(71, 85, 105, 0.15)"], [1, "rgba(71, 85, 105, 0.15)"]],
                    opacity=0.2,
                    showscale=False,
                    name="xy-Plane (z = 0)",
                    hoverinfo="skip",
                )
            )

        # 3D Vector Cones on xy-plane (or on potential surface if conservative)
        c_pts = np.linspace(x_range[0] * 0.75, x_range[1] * 0.75, 7)
        c_ypts = np.linspace(y_range[0] * 0.75, y_range[1] * 0.75, 7)
        VX, VY = np.meshgrid(c_pts, c_ypts)
        if calc.get("is_conservative") and calc.get("potential_fn"):
            try:
                VZ = np.asarray(calc["potential_fn"](VX, VY), dtype=float)
            except Exception:
                VZ = np.zeros_like(VX)
        else:
            VZ = np.zeros_like(VX)

        try:
            U2 = np.asarray(calc["comp_fns"][0](VX, VY), dtype=float)
            V2 = np.asarray(calc["comp_fns"][1](VX, VY), dtype=float)
            W2 = np.zeros_like(U2)
            traces_3d.append(
                go.Cone(
                    x=VX.flatten(),
                    y=VY.flatten(),
                    z=VZ.flatten(),
                    u=U2.flatten(),
                    v=V2.flatten(),
                    w=W2.flatten(),
                    sizemode="scaled",
                    sizeref=0.35,
                    colorscale="Viridis",
                    showscale=False,
                    name="2D Vector Field in 3D F(x₁, x₂)",
                )
            )
        except Exception:
            pass

        # 3D Vertical Curl Vector ∇ × F = ⟨0, 0, curl⟩ at point a
        curl_v2 = calc.get("curl_val", 0.0)
        pt_base_z = 0.0
        if calc.get("is_conservative") and calc.get("potential_fn"):
            try:
                pt_base_z = float(np.real(complex(calc["potential_fn"](a1, a2))))
            except Exception:
                pt_base_z = 0.0

        if abs(curl_v2) > 0.02 and show_curl_wheel:
            c_scale = (x_range[1] - x_range[0]) * 0.35 / max(abs(curl_v2), 1.0)
            cz_end = pt_base_z + curl_v2 * c_scale
            traces_3d.append(
                go.Scatter3d(
                    x=[a1, a1],
                    y=[a2, a2],
                    z=[pt_base_z, cz_end],
                    mode="lines+markers+text",
                    line=dict(color="#f59e0b", width=9),
                    marker=dict(size=[3, 8], color="#f59e0b", symbol="diamond"),
                    text=["", f"∇×F (Curl={curl_v2:.2f})"],
                    textposition="top center",
                    name="3D Curl Vector ∇×F (Z-Axis)",
                )
            )
            # 3D Horizontal Paddle Wheel Rim at point a
            th_w = np.linspace(0, 2 * np.pi, 36)
            w_rad = (x_range[1] - x_range[0]) * 0.09
            traces_3d.append(
                go.Scatter3d(
                    x=a1 + w_rad * np.cos(th_w),
                    y=a2 + w_rad * np.sin(th_w),
                    z=np.full_like(th_w, pt_base_z),
                    mode="lines",
                    line=dict(color="#f59e0b", width=4),
                    name=f"Paddle Wheel Rim (ω={abs(curl_v2)/2:.2f} rad/s)",
                )
            )

        # 3D Divergence Bubble at point a
        div_v2 = calc.get("div_val", 0.0)
        if abs(div_v2) > 0.02 and show_div_bubble:
            b_rad = (x_range[1] - x_range[0]) * 0.07
            th_b = np.linspace(0, 2 * np.pi, 32)
            bub_col = "#10b981" if div_v2 > 0 else "#ef4444"
            traces_3d.append(
                go.Scatter3d(
                    x=a1 + b_rad * np.cos(th_b),
                    y=a2 + b_rad * np.sin(th_b),
                    z=np.full_like(th_b, pt_base_z),
                    mode="lines",
                    line=dict(color=bub_col, width=3),
                    name=f"Div Bubble ({'Source' if div_v2 > 0 else 'Sink'})",
                )
            )
            traces_3d.append(
                go.Scatter3d(
                    x=a1 + b_rad * np.cos(th_b),
                    y=np.full_like(th_b, a2),
                    z=pt_base_z + b_rad * np.sin(th_b),
                    mode="lines",
                    line=dict(color=bub_col, width=2, dash="dash"),
                    showlegend=False,
                )
            )

        # 3D Line Integral Curve
        if show_line_integral and "line_integral" in calc:
            li = calc["line_integral"]
            lx = np.array(li["xs"], dtype=float)
            ly = np.array(li["ys"], dtype=float)
            if calc.get("is_conservative") and calc.get("potential_fn"):
                try:
                    lz = np.asarray(calc["potential_fn"](lx, ly), dtype=float) + 0.04
                except Exception:
                    lz = np.full_like(lx, 0.06)
            else:
                lz = np.full_like(lx, 0.06)
            traces_3d.append(
                go.Scatter3d(
                    x=lx,
                    y=ly,
                    z=lz,
                    mode="lines",
                    line=dict(color="#d946ef", width=7),
                    name=f"3D Path C (W = {li['work']:.2f})",
                )
            )

        # 3D Evaluation Force Vector F(a)
        f1_val = calc.get("fx1", 0.0)
        f2_val = calc.get("fx2", 0.0)
        f_norm = math.sqrt(f1_val**2 + f2_val**2)
        if f_norm > 1e-4 and show_gradient:
            f_scale = (x_range[1] - x_range[0]) * 0.22 / max(f_norm, 1.0)
            traces_3d.append(
                go.Scatter3d(
                    x=[a1, a1 + f1_val * f_scale],
                    y=[a2, a2 + f2_val * f_scale],
                    z=[pt_base_z, pt_base_z],
                    mode="lines+markers+text",
                    line=dict(color="#38bdf8", width=7),
                    marker=dict(size=[2, 7], color="#38bdf8", symbol="diamond"),
                    text=["", f"F(a) ‖F‖={f_norm:.2f}"],
                    textposition="top center",
                    name="Force Vector F(a)",
                )
            )

    # 6. Affine Tangent Plane z = g(x1, x2)
    fa_val = calc["fa"]
    fx1_val, fx2_val = calc["fx1"], calc["fx2"]
    if show_affine_plane and mode == "scalar_2d":
        p_span = (x_range[1] - x_range[0]) * 0.24
        px_grid = np.linspace(a1 - p_span, a1 + p_span, 15)
        py_grid = np.linspace(a2 - p_span, a2 + p_span, 15)
        PX, PY = np.meshgrid(px_grid, py_grid)
        PZ = fa_val + fx1_val * (PX - a1) + fx2_val * (PY - a2)
        traces_3d.append(
            go.Surface(
                x=PX,
                y=PY,
                z=PZ,
                colorscale=[[0, "rgba(236,72,153,0.72)"], [1, "rgba(139,92,246,0.72)"]],
                showscale=False,
                opacity=0.72,
                name="Affine Tangent Plane g(x)",
            )
        )

    # 7. Point a, Vertical 2D<->3D Projection Stem, 3D Surface Normal Line, 3D Gradient, Flow Line γ(t), and Error Rod
    if mode == "vector_2d":
        if calc.get("is_conservative") and calc.get("potential_fn"):
            try:
                pt_z = float(np.real(complex(calc["potential_fn"](a1, a2))))
            except Exception:
                pt_z = 0.0
        else:
            pt_z = 0.0
    elif mode in ("scalar_3d", "vector_3d", "matrix_3d") or is_cyl_only:
        pt_z = a3
    else:
        pt_z = fa_val
    traces_3d.append(
        go.Scatter3d(
            x=[a1, a1],
            y=[a2, a2],
            z=[z_min_plot, pt_z],
            mode="lines+markers",
            line=dict(color="#00ffff", width=3, dash="dot"),
            marker=dict(size=[4, 0], color="#00ffff"),
            showlegend=False,
            hoverinfo="skip",
            name="2D↔3D Link",
        )
    )
    traces_3d.append(
        go.Scatter3d(
            x=[a1],
            y=[a2],
            z=[pt_z],
            mode="markers+text",
            marker=dict(size=8, color="#00ffff", symbol="diamond", line=dict(color="#ffffff", width=2)),
            text=[f"a=({a1:.2f},{a2:.2f}) • f={pt_z:.3f}"],
            textposition="top center",
            hovertemplate=f"<b>Point a (3D)</b><br>x₁ = {a1:.4f}<br>x₂ = {a2:.4f}<br>Exact f(a) = {pt_z:.4f}<extra></extra>",
            name="Point a",
            showlegend=(view_mode == "3D Surface"),
        )
    )

    if show_flow_line and len(flow_xs) > 1:
        traces_3d.append(
            go.Scatter3d(
                x=flow_xs,
                y=flow_ys,
                z=flow_zs,
                mode="lines",
                line=dict(color="#f43f5e", width=6),
                name="Flow Line γ(t)",
                showlegend=(view_mode == "3D Surface"),
            )
        )

    if show_3d_normal and mode == "scalar_2d":
        nx3, ny3, nz3 = calc["surface_normal_3d"]
        n_norm = math.sqrt(nx3**2 + ny3**2 + nz3**2)
        n_scale = (x_range[1] - x_range[0]) * 0.22 / max(n_norm, 1e-4)
        traces_3d.append(
            go.Scatter3d(
                x=[a1 - nx3 * n_scale * 0.5, a1 + nx3 * n_scale],
                y=[a2 - ny3 * n_scale * 0.5, a2 + ny3 * n_scale],
                z=[fa_val - nz3 * n_scale * 0.5, fa_val + nz3 * n_scale],
                mode="lines+markers",
                line=dict(color="#10b981", width=6),
                marker=dict(size=[3, 6], color="#10b981"),
                name="3D Surface Normal n₃D",
            )
        )

    if show_gradient and calc["grad_mag"] > 1e-6 and mode == "scalar_2d":
        g_scale3 = min(1.0, (x_range[1] - x_range[0]) * 0.2 / max(calc["grad_mag"], 1e-4))
        traces_3d.append(
            go.Scatter3d(
                x=[a1, a1 + fx1_val * g_scale3],
                y=[a2, a2 + fx2_val * g_scale3],
                z=[fa_val, fa_val],
                mode="lines+markers",
                line=dict(color="#f59e0b", width=7),
                marker=dict(size=[0, 6], symbol="diamond", color="#f59e0b"),
                name="Gradient ∇f(a)",
                showlegend=(view_mode == "3D Surface"),
            )
        )

    if show_error_rod and mode == "scalar_2d":
        traces_3d.append(
            go.Scatter3d(
                x=[test_x, test_x],
                y=[test_y, test_y],
                z=[calc["test_affine"], calc["test_exact"]],
                mode="lines+markers+text",
                line=dict(color="#ef4444", width=6),
                marker=dict(size=5, color=["#ec4899", "#ef4444"]),
                text=["g(x_test)", f"f(x_test) (|err|={calc['test_error']:.3f})"],
                name="Approximation Error |f - g|",
            )
        )

    # 8. Horizontal Level Slice Plane z = c
    if mode == "scalar_2d" and not is_cyl_only:
        traces_3d.append(
            go.Surface(
                x=X,
                y=Y,
                z=np.full_like(X, level_c),
                colorscale=[[0, "rgba(6,182,212,0.28)"], [1, "rgba(6,182,212,0.28)"]],
                showscale=False,
                opacity=0.30,
                name=f"Level Slice Plane z = {level_c:.2f}",
            )
        )

    # -------------------------------------------------------------------------
    # C. BUILD ANIMATION FRAMES (SLICE / ORBIT / GLIDE)
    # -------------------------------------------------------------------------
    frames: List[go.Frame] = []
    updatemenus: List[Dict[str, Any]] = []

    if anim_mode == "orbit":
        angles = np.linspace(0, 2 * np.pi, 36, endpoint=False)
        for idx, ang in enumerate(angles):
            eye_x = 1.9 * math.cos(ang)
            eye_y = 1.9 * math.sin(ang)
            eye_z = 1.15 + 0.25 * math.sin(ang * 2)
            frames.append(
                go.Frame(
                    layout=dict(scene=dict(camera=dict(eye=dict(x=eye_x, y=eye_y, z=eye_z)))),
                    name=f"orbit_{idx}",
                )
            )
        updatemenus = [
            dict(
                type="buttons",
                direction="left",
                x=0.02,
                y=1.08,
                showactive=True,
                buttons=[
                    dict(
                        label="▶ Play 360° Orbit",
                        method="animate",
                        args=[None, dict(frame=dict(duration=55, redraw=True), fromcurrent=True)],
                    ),
                    dict(
                        label="⏸ Pause",
                        method="animate",
                        args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")],
                    ),
                ],
            )
        ]

    elif anim_mode == "slice" and mode == "scalar_2d" and len(traces_3d) >= 1:
        c_vals = np.linspace(z_min_plot * 0.8, z_max_plot * 0.85, 24)
        slice_idx = len(traces_3d) - 1
        for idx, cv in enumerate(c_vals):
            frames.append(
                go.Frame(
                    data=[
                        go.Surface(
                            x=X,
                            y=Y,
                            z=np.full_like(X, float(cv)),
                            colorscale=[[0, "rgba(6,182,212,0.38)"], [1, "rgba(6,182,212,0.38)"]],
                            showscale=False,
                            opacity=0.38,
                        )
                    ],
                    traces=[slice_idx],
                    name=f"slice_{idx}",
                )
            )
        updatemenus = [
            dict(
                type="buttons",
                direction="left",
                x=0.02,
                y=1.08,
                showactive=True,
                buttons=[
                    dict(
                        label="🌊 Animate Level Slice c(t)",
                        method="animate",
                        args=[None, dict(frame=dict(duration=75, redraw=True), fromcurrent=True)],
                    ),
                    dict(
                        label="⏸ Pause",
                        method="animate",
                        args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")],
                    ),
                ],
            )
        ]

    elif anim_mode == "glide" and mode == "scalar_2d":
        t_vals = np.linspace(0, 2 * np.pi, 24, endpoint=False)
        r_orb = max(0.8, math.hypot(a1, a2) if math.hypot(a1, a2) > 0.3 else 1.8)
        # Find trace index of Point a in traces_3d
        pt_trace_idx = next((i for i, tr in enumerate(traces_3d) if getattr(tr, "name", "") == "Point a"), None)
        if pt_trace_idx is not None:
            for idx, tv in enumerate(t_vals):
                gx = r_orb * math.cos(tv)
                gy = r_orb * math.sin(tv)
                try:
                    gz = float(calc["f_fn_2d"](gx, gy))
                except Exception:
                    gz = 0.0
                frames.append(
                    go.Frame(
                        data=[
                            go.Scatter3d(
                                x=[gx],
                                y=[gy],
                                z=[gz],
                                mode="markers+text",
                                marker=dict(size=8, color="#00ffff", symbol="diamond", line=dict(color="#ffffff", width=2)),
                                text=[f"a(t)=({gx:.1f},{gy:.1f},{gz:.1f})"],
                            )
                        ],
                        traces=[pt_trace_idx],
                        name=f"glide_{idx}",
                    )
                )
            updatemenus = [
                dict(
                    type="buttons",
                    direction="left",
                    x=0.02,
                    y=1.08,
                    showactive=True,
                    buttons=[
                        dict(
                            label="✨ Glide Point a(t)",
                            method="animate",
                            args=[None, dict(frame=dict(duration=75, redraw=True), fromcurrent=True)],
                        ),
                        dict(
                            label="⏸ Pause",
                            method="animate",
                            args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")],
                        ),
                    ],
                )
            ]

    # -------------------------------------------------------------------------
    # D. ASSEMBLE FINAL FIGURE BY VIEW MODE
    # -------------------------------------------------------------------------
    v1_lbl = "x₁" if calc["v1_tex"] == "x_1" else "x"
    v2_lbl = "x₂" if calc["v2_tex"] == "x_2" else "y"
    v3_lbl = "x₃" if calc["v3_tex"] == "x_3" else "z"

    scene_cfg = dict(
        xaxis=dict(title=v1_lbl, gridcolor=grid_col, backgroundcolor=bg_2d, showbackground=True),
        yaxis=dict(title=v2_lbl, gridcolor=grid_col, backgroundcolor=bg_2d, showbackground=True),
        zaxis=dict(title=f"{v3_lbl} / f(x)", gridcolor=grid_col, backgroundcolor=bg_2d, showbackground=True),
        camera=dict(eye=dict(x=1.55, y=1.55, z=1.18)),
        aspectmode="cube",
    )

    if view_mode == "2D Level Sets":
        fig = go.Figure(data=traces_2d)
        fig.update_layout(
            template=template_name,
            dragmode="pan",
            clickmode="event+select",
            paper_bgcolor=paper_bg,
            plot_bgcolor=bg_2d,
            font=dict(color=text_col, family="Plus Jakarta Sans, Inter, system-ui, sans-serif"),
            xaxis=dict(title=v1_lbl, range=list(x_range), gridcolor=grid_col, scaleanchor="y", scaleratio=1),
            yaxis=dict(title=v2_lbl, range=list(y_range), gridcolor=grid_col),
            height=620,
            margin=dict(l=40, r=20, t=45, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0),
        )
    elif view_mode == "3D Surface":
        fig = go.Figure(data=traces_3d, frames=frames)
        fig.update_layout(
            template=template_name,
            dragmode="turntable",
            clickmode="event+select",
            paper_bgcolor=paper_bg,
            font=dict(color=text_col, family="Plus Jakarta Sans, Inter, system-ui, sans-serif"),
            scene=scene_cfg,
            height=620,
            margin=dict(l=10, r=10, t=45, b=10),
            updatemenus=updatemenus,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0),
        )
    else:
        # Split Dual View (3D + 2D side-by-side)
        fig = make_subplots(
            rows=1,
            cols=2,
            specs=[[{"type": "scene"}, {"type": "xy"}]],
            subplot_titles=("🌌 3D Manifold (Click Surface to Set Point a)", "🎯 2D Level Sets (Click Map to Set Point a)"),
            column_widths=[0.54, 0.46],
            horizontal_spacing=0.06,
        )
        for tr3 in traces_3d:
            fig.add_trace(tr3, row=1, col=1)
        for tr2 in traces_2d:
            fig.add_trace(tr2, row=1, col=2)

        if frames:
            fig.frames = frames

        fig.update_layout(
            template=template_name,
            dragmode="pan",
            clickmode="event+select",
            paper_bgcolor=paper_bg,
            plot_bgcolor=bg_2d,
            font=dict(color=text_col, family="Plus Jakarta Sans, Inter, system-ui, sans-serif"),
            scene=scene_cfg,
            xaxis=dict(title=v1_lbl, range=list(x_range), gridcolor=grid_col, scaleanchor="y", scaleratio=1),
            yaxis=dict(title=v2_lbl, range=list(y_range), gridcolor=grid_col),
            height=620,
            margin=dict(l=15, r=15, t=50, b=30),
            updatemenus=updatemenus,
            legend=dict(orientation="h", yanchor="bottom", y=-0.12, xanchor="center", x=0.5),
        )

    return fig


# =============================================================================
# 6. AI CALCULUS TUTOR ENGINE (GEMINI 3.5 FLASH-LITE + OFFLINE FALLBACK)
# =============================================================================
def extract_graph_action(raw_text: str) -> Tuple[str, Optional[Dict[str, Any]]]:
    """
    Extracts any `graph_action` JSON block from the AI response and strips all raw
    JSON/code blocks so the user only sees clean Markdown & LaTeX.
    """
    if not raw_text:
        return "", None

    matched_action = None
    m1 = re.search(r"```graph_action\s*([\s\S]*?)(?:```|$)", raw_text, flags=re.IGNORECASE)
    if m1:
        try:
            matched_action = json.loads(m1.group(1).strip().rstrip("`").strip())
        except Exception:
            pass

    if not matched_action:
        m2 = re.search(
            r"```(?:json)?\s*(\{[\s\S]*?(?:\"action\"|\"f\"|\"constraint\"|\"point_a\")[\s\S]*?\})(?:```|$)",
            raw_text,
            flags=re.IGNORECASE,
        )
        if m2:
            try:
                matched_action = json.loads(m2.group(1).strip())
            except Exception:
                pass

    clean_text = re.sub(r"```graph_action[\s\S]*?(?:```|$)", "", raw_text, flags=re.IGNORECASE)
    clean_text = re.sub(
        r"```(?:json)?\s*\{[\s\S]*?(?:\"action\"|\"update_graph\"|\"point_a\"|\"f\"\s*:)[\s\S]*?\}(?:```|$)",
        "",
        clean_text,
        flags=re.IGNORECASE,
    ).strip()

    return clean_text, matched_action


def load_saved_api_key() -> str:
    """Loads Gemini API key from environment variable, .env file, or local .gemini_key file."""
    env_k = (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or "").strip()
    if env_k:
        return env_k
    base_dir = os.path.dirname(os.path.abspath(__file__))
    key_file = os.path.join(base_dir, ".gemini_key")
    if os.path.exists(key_file):
        try:
            with open(key_file, "r", encoding="utf-8") as fh:
                k = fh.read().strip()
                if k:
                    return k
        except Exception:
            pass
    env_file = os.path.join(base_dir, ".env")
    if os.path.exists(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as fh:
                for line in fh:
                    if "=" in line and not line.strip().startswith("#"):
                        k_name, k_val = line.split("=", 1)
                        if k_name.strip() in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
                            return k_val.strip().strip('"').strip("'")
        except Exception:
            pass
    return ""


def save_api_key(key: str) -> None:
    """Persists a user-entered Gemini API key locally in .gemini_key (gitignored)."""
    k = (key or "").strip()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    key_file = os.path.join(base_dir, ".gemini_key")
    try:
        if k:
            with open(key_file, "w", encoding="utf-8") as fh:
                fh.write(k)
        elif os.path.exists(key_file):
            os.remove(key_file)
    except Exception:
        pass


def generate_offline_tutor_response(query: str, calc: Dict[str, Any], a1: float, a2: float, a3: float) -> Tuple[str, Optional[Dict[str, Any]]]:
    """
    Intelligent built-in multivariable calculus tutor & action generator.
    Works 100% offline and can automatically configure any shape, flow line γ(t), cylinder, matrix, or surface!
    """
    q = (query or "").lower()
    v1, v2 = calc["v1_tex"], calc["v2_tex"]
    fa, fx1, fx2, mag = calc["fa"], calc["fx1"], calc["fx2"], calc["grad_mag"]

    # -1. Curl / Rotor / Paddle Wheel / Circulation requests
    if any(k in q for k in ("curl", "ротор", "rotor", "paddle wheel", "circulation", "вихрь", "vorticity")):
        reply = (
            f"### 🔄 Curl $\\nabla \\times \\mathbf{{F}}$ & The Microscopic Paddle Wheel\n\n"
            f"**Curl** measures the **rotational tendency (circulation density)** of a vector field $\\mathbf{{F}}$ at a point $\\mathbf{{a}}$:\n"
            f"- **In 2D:** $\\operatorname{{curl}}\\mathbf{{F}} = \\frac{{\\partial F_2}}{{\\partial x_1}} - \\frac{{\\partial F_1}}{{\\partial x_2}} = Q_x - P_y$\n"
            f"- **Physical Intuition:** Drop a tiny microscopic paddle wheel into the flow at point $\\mathbf{{a}}$:\n"
            f"  - **$\\operatorname{{curl}} > 0$:** Spins **Counter-Clockwise (CCW)** with angular speed $\\omega = \\frac{{1}}{{2}}\\operatorname{{curl}}\\mathbf{{F}}$.\n"
            f"  - **$\\operatorname{{curl}} < 0$:** Spins **Clockwise (CW)**.\n"
            f"  - **$\\operatorname{{curl}} = 0$:** **Irrotational / Curl-Free!** The paddle wheel does NOT rotate at all!\n\n"
            f"✅ *I have loaded the classic **Rotational Vortex Field $\\mathbf{{F}} = [-x_2, x_1]$** with the interactive Paddle Wheel enabled!*"
        )
        return reply, {"f": "[-x2, x1]", "a1": 1.5, "a2": 1.0, "view_mode": "Split Dual View"}

    # -2. Potential Function & Conservative Fields (F = ∇φ)
    if any(k in q for k in ("potential", "потенциал", "conservative", "консервативн", "path independent", "gradient field")):
        reply = (
            r"### ⚡ Conservative Vector Fields & Scalar Potential $\phi(\mathbf{x})$" "\n\n"
            r"A vector field $\mathbf{F}$ is **conservative** if and only if it is the gradient of a scalar potential landscape:" "\n"
            r"$$\mathbf{F} = \nabla \phi = \left\langle \frac{\partial \phi}{\partial x_1}, \frac{\partial \phi}{\partial x_2} \right\rangle$$" "\n"
            r"- **The Curl Test:** On a simply connected domain, $\mathbf{F}$ is conservative $\iff \operatorname{curl}\mathbf{F} = \mathbf{0}$." "\n"
            r"- **Fundamental Theorem of Line Integrals:** Work is strictly **path-independent**!" "\n"
            r"  $$\int_C \mathbf{F} \cdot d\mathbf{r} = \phi(\mathbf{r}(b)) - \phi(\mathbf{r}(a))$$" "\n"
            r"- **Closed Loops:** Circulation along any closed loop is strictly zero: $\oint_C \mathbf{F} \cdot d\mathbf{r} = 0$!" "\n\n"
            r"✅ *I have loaded the conservative field $\mathbf{F} = [2x_1 x_2, x_1^2]$ whose potential is $\phi(x_1, x_2) = x_1^2 x_2$! Notice the 3D potential surface in the 3D view.*"
        )
        return reply, {"f": "[2*x1*x2, x1^2]", "a1": 1.5, "a2": 1.5, "view_mode": "Split Dual View"}

    # -3. Line Integrals & Green's Theorem
    if any(k in q for k in ("line integral", "интеграл", "криволинейн", "green", "грине", "circulation loop", "work", "работа")):
        reply = (
            r"### ➰ Line Integrals $\int_C \mathbf{F} \cdot d\mathbf{r}$ & Green's Theorem" "\n\n"
            r"The **line integral** calculates the total work done by force field $\mathbf{F}$ moving a particle along curve $C$:" "\n"
            r"$$W = \int_C \mathbf{F} \cdot d\mathbf{r} = \int_{t_0}^{t_1} \mathbf{F}(\mathbf{r}(t)) \cdot \mathbf{r}'(t) \, dt$$" "\n"
            r"- **Green's Theorem:** For a positively oriented simple closed curve $C = \partial D$:" "\n"
            r"  $$\oint_C (P\,dx_1 + Q\,dx_2) = \iint_D \left( \frac{\partial Q}{\partial x_1} - \frac{\partial P}{\partial x_2} \right) dA = \iint_D (\operatorname{curl}\mathbf{F}) \, dA$$" "\n"
            r"- For constant curl (e.g. $\mathbf{F} = [-x_2, x_1]$ with $\operatorname{curl}=2$): Circulation $= 2 \times (\pi R^2) = 2\pi R^2$!" "\n\n"
            r"✅ *I have loaded the Closed Loop Line Integral preset! Check the path and work value.*"
        )
        return reply, {"f": "[-x2, x1]", "a1": 0.0, "a2": 0.0, "view_mode": "Split Dual View"}

    # -4. Divergence & Flux (Sources / Sinks)
    if any(k in q for k in ("divergence", "дивергенция", "div", "source", "sink", "flux", "поток", "источник", "сток")):
        reply = (
            r"### 💥 Divergence $\nabla \cdot \mathbf{F}$ & Fluid Flux" "\n\n"
            r"**Divergence** measures the net outward flux of a vector field per unit volume from an infinitesimal region around $\mathbf{a}$:" "\n"
            r"$$\operatorname{div}\mathbf{F} = \nabla \cdot \mathbf{F} = \frac{\partial F_1}{\partial x_1} + \frac{\partial F_2}{\partial x_2} \left(+ \frac{\partial F_3}{\partial x_3}\right)$$" "\n"
            r"- **$\operatorname{div} > 0$ (Source):** Fluid or electric flux spreads outward (expansion)." "\n"
            r"- **$\operatorname{div} < 0$ (Sink):** Fluid or flux converges inward and drains." "\n"
            r"- **$\operatorname{div} = 0$ (Incompressible / Solenoidal):** Ideal fluid flow without volume change." "\n\n"
            r"✅ *I have loaded the Radial Source field $\mathbf{F} = [x_1, x_2]$ (div = +2) with the expanding Flux Ring!*"
        )
        return reply, {"f": "[x1, x2]", "a1": 1.5, "a2": 1.0, "view_mode": "Split Dual View"}

    # 0. Flow Line γ(t) / Integral Curve / Trajectory requests (e.g. "bro create me pls flow line of gamma t")
    if any(k in q for k in ("flow line", "flowline", "gamma", "γ(t)", "integral curve", "trajectory", "steepest")):
        cur_f = calc["raw_expr"] if calc["mode"] == "scalar_2d" else "x1^2 / 4 + x2^2 / 9"
        pt_a1 = a1 if (abs(a1) > 0.1 or abs(a2) > 0.1) else 1.2
        pt_a2 = a2 if (abs(a1) > 0.1 or abs(a2) > 0.1) else 2.4
        reply = (
            f"### 🌊 Flow Line $\\gamma(t)$ (Integral Curve of the Gradient Field)\n\n"
            f"A **flow line** (or **integral curve**) $\\gamma: \\mathbb{{R}} \\to \\mathbb{{R}}^2$ starting at point $\\mathbf{{a}} = ({pt_a1:.2f}, {pt_a2:.2f})$ is the curve satisfying the initial value problem:\n"
            f"$$\\gamma'(t) = \\nabla f(\\gamma(t)), \\qquad \\gamma(0) = \\mathbf{{a}}$$\n"
            f"- **Tangent to the Gradient:** At every point along $\\gamma(t)$, the velocity vector $\\gamma'(t)$ equals the gradient $\\nabla f(\\gamma(t)) = \\langle {fx1:.2f}, {fx2:.2f} \\rangle$.\n"
            f"- **Orthogonal to Level Sets ($90^\\circ$):** Because $\\nabla f$ is perpendicular to every level curve $f({v1}, {v2}) = c$, the flow line $\\gamma(t)$ crosses every contour ring at a strict **$90^\\circ$ right angle** — following the path of **steepest ascent** up the 3D surface!\n\n"
            f"✅ *I have enabled the **Flow Line $\\gamma(t)$** trajectory (in crimson red) on both the 2D Level Set plot and the 3D Surface!*"
        )
        return reply, {
            "f": cur_f,
            "a1": pt_a1,
            "a2": pt_a2,
            "show_flow_line": True,
            "view_mode": "Split Dual View",
        }

    # 1. Cylinder / Free Variable / Requirement requests
    if any(k in q for k in ("cylinder", "цилиндр", "constraint", "requirement", "free variable", "x1^2/4")):
        is_parab = any(k in q for k in ("parabol", "парабол", "+ x2 =", "+x2="))
        req = "x1^2 / 4 + x2 = 1" if is_parab else "x1^2 / 4 + x2^2 / 9 = 1"
        name = "Parabolic Cylinder" if is_parab else "Elliptic Cylinder"
        eq_tex = r"\frac{x_1^2}{4} + x_2 = 1" if is_parab else r"\frac{x_1^2}{4} + \frac{x_2^2}{9} = 1"
        reply = (
            f"### 🏛️ {name} in $\\mathbb{{R}}^3$ via Free Variable $x_3$\n\n"
            f"When we define the identity vector $\\mathbf{{F}}(x_1, x_2, x_3) = [x_1; x_2; x_3]$ with requirement:\n"
            f"$${eq_tex}$$\n"
            f"- **Free Variable $x_3$:** Since $x_3$ does not appear in the constraint equation, $x_3$ can take **any real value** ($-\\infty < x_3 < \\infty$).\n"
            f"- **3D Extrusion:** The 2D curve in the $(x_1, x_2)$ plane is extruded vertically parallel to the $x_3$-axis to form a continuous **3D cylindrical surface**!\n\n"
            f"✅ *I have automatically updated the Function and Constraint inputs for you!*"
        )
        action = {
            "f": "[x1; x2; x3]",
            "constraint": req,
            "a1": 2.0,
            "a2": 0.0,
            "a3": 1.0,
            "view_mode": "3D Surface",
        }
        return reply, action

    # 2. Ellipse request
    if any(k in q for k in ("ellipse", "эллипс", "еллипс")):
        reply = (
            f"### 🪐 Ellipse Level Set & Quadratic Form\n\n"
            f"An **ellipse** with semi-axes $A = 2$ and $B = 3$ is given by:\n"
            f"$$f({v1}, {v2}) = \\frac{{{v1}^2}}{{4}} + \\frac{{{v2}^2}}{{9}} = 1$$\n"
            f"- **Total Derivative Row Matrix:** $\\mathbf{{D}}f({v1}, {v2}) = \\begin{{bmatrix}} \\frac{{{v1}}}{{2}} & \\frac{{2{v2}}}{{9}} \\end{{bmatrix}}_{{1 \\times 2}}$\n"
            f"- **Gradient Orthogonality:** $\\nabla f(\\mathbf{{a}})$ points outward along the normal line at strictly $90^\\circ$ to the ellipse tangent!\n\n"
            f"✅ *Applied $f = x_1^2/4 + x_2^2/9$ with $c = 1.0$ to your graph!*"
        )
        return reply, {"f": "x1^2 / 4 + x2^2 / 9", "constraint": "", "c": 1.0, "a1": 1.2, "a2": 2.4, "view_mode": "Split Dual View"}

    # 3. Saddle request
    if any(k in q for k in ("saddle", "седло", "hyperbolic", "гипербол")):
        reply = (
            f"### 🐎 Hyperbolic Paraboloid (Saddle Surface)\n\n"
            f"$$f({v1}, {v2}) = {v1}^2 - {v2}^2$$\n"
            f"- At the origin $(0,0)$, $\\nabla f(0,0) = \\mathbf{{0}}$ and the Hessian matrix is $\\mathbf{{H}} = \\begin{{bmatrix}} 2 & 0 \\\\ 0 & -2 \\end{{bmatrix}}$.\n"
            f"- Because the Hessian determinant is $D = (2)(-2) - 0 = -4 < 0$, $(0,0)$ is a **Saddle Point**!\n\n"
            f"✅ *Applied the saddle surface to your graph!*"
        )
        return reply, {"f": "x1^2 - x2^2", "constraint": "", "c": 1.0, "a1": 1.41, "a2": 1.0, "view_mode": "Split Dual View"}

    # 4. 3x3 or 2x2 Matrix request
    if any(k in q for k in ("3x3", "r3 matrix", "matrix in r3", "[1, 2, 3")):
        reply = (
            r"### 🧊 $3 \times 3$ Linear Transformation Matrix in $\mathbb{R}^3$" "\n\n"
            r"$$\mathbf{A} = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix}_{3 \times 3}$$" "\n"
            r"- The columns $\mathbf{c}_1, \mathbf{c}_2, \mathbf{c}_3$ represent the images of the standard basis vectors $\mathbf{e}_1, \mathbf{e}_2, \mathbf{e}_3$ in $\mathbb{R}^3$." "\n"
            r"- They are rendered as 3D basis arrows alongside the transformed vector $\mathbf{A}\mathbf{a}$!" "\n\n"
            r"✅ *Applied the $3 \times 3$ matrix in 3D view!*"
        )
        return reply, {"f": "[1, 2, 3; 4, 5, 6; 7, 8, 9]", "constraint": "", "a1": 1.0, "a2": 0.5, "a3": 0.5, "view_mode": "3D Surface"}

    # 5. Hessian / Extremum / Second Derivative Test
    if any(k in q for k in ("hessian", "heissian", "гессиан", "extrem", "minimum", "maximum", "critical")):
        reply = (
            f"### 🔍 Hessian Matrix & Second Derivative Test at $\\mathbf{{a}} = ({a1:.2f}, {a2:.2f})$\n\n"
            f"- **Gradient:** $\\nabla f(\\mathbf{{a}}) = \\langle {fx1:.3f}, {fx2:.3f} \\rangle$, $\\|\\nabla f\\| = {mag:.3f}$\n"
            f"- **Hessian Matrix:**\n"
            f"  $${calc['hessian_numeric_latex']}$$\n"
            f"- **Eigenvalues:** `{calc['eigenvalues_str']}`\n"
            f"- **Verdict:** **{calc['extremum_label']}**"
        )
        return reply, None

    # 6. Affine / Tangent Plane
    if any(k in q for k in ("affine", "tangent plane", "linearization", "approximation", "g(x)", "аффин", "касательн")):
        reply = (
            f"### 📐 Affine Approximation $g(\\mathbf{{x}})$ & Tangent Plane\n\n"
            f"The **affine function** is the best first-order linear approximation of $f$ near $\\mathbf{{a}} = ({a1:.2f}, {a2:.2f})$:\n"
            f"$${calc['affine_symbolic_latex']}$$\n"
            f"Evaluated at your current point:\n"
            f"$${calc['affine_numeric_latex']}$$\n"
            f"- At test point $\\mathbf{{x}}_{{\\text{{test}}}} = ({calc['test_x']:.2f}, {calc['test_y']:.2f})$:\n"
            f"  - Exact: $f(\\mathbf{{x}}_{{\\text{{test}}}}) = {calc['test_exact']:.4f}$\n"
            f"  - Affine: $g(\\mathbf{{x}}_{{\\text{{test}}}}) = {calc['test_affine']:.4f}$\n"
            f"  - Error: $|f - g| = {calc['test_error']:.4f}$"
        )
        return reply, None

    # 7. Default Live Graph Summary
    reply = (
        f"### 🤖 Live Calculus Analysis for ${calc['f_latex']}$\n\n"
        f"- **Evaluation Point:** $\\mathbf{{a}} = ({a1:.2f}, {a2:.2f})$, where $f(\\mathbf{{a}}) = {fa:.3f}$\n"
        f"- **Total Derivative Matrix:** $${calc['df_numeric_latex']}$$\n"
        f"- **Gradient Vector:** $${calc['grad_latex']}$$ (magnitude $\\|\\nabla f\\| = {mag:.3f}$)\n"
        f"- **Affine Tangent Plane:** $${calc['affine_numeric_latex']}$$\n"
        f"- **Hessian & Extremum Test:** {calc['extremum_label']}\n\n"
        f"💡 *Try asking me:*\n"
        f"- *\"Create a flow line of gamma(t)\"*\n"
        f"- *\"Create a parabolic cylinder with x1^2/4 + x2 = 1\"*\n"
        f"- *\"Make me an ellipse\"* or *\"Show me a saddle surface\"*\n"
        f"- *\"Explain the Hessian matrix and 2nd derivative test\"*"
    )
    return reply, None


def ask_ai_tutor(
    message: str,
    calc: Dict[str, Any],
    a1: float,
    a2: float,
    a3: float,
    custom_api_key: str = "",
) -> Tuple[str, Optional[Dict[str, Any]], str]:
    """
    Calls Gemini API (gemini-2.5-flash-lite / gemini-2.0-flash) if a valid API key is available,
    otherwise instantly falls back to the deterministic Built-in Calculus & Action Engine.
    Returns (clean_reply_markdown, graph_action_dict_or_None, model_used).
    """
    if custom_api_key and custom_api_key.strip():
        save_api_key(custom_api_key.strip())
    api_key = (custom_api_key or load_saved_api_key()).strip()
    
    # If key is empty or not formatted as a Gemini API key (which begins with AIza), use Built-in Engine
    if not api_key or not api_key.startswith("AIza"):
        reply, action = generate_offline_tutor_response(message, calc, a1, a2, a3)
        return reply, action, "Built-in Calculus Engine"

    system_prompt = f"""You are an expert Multivariable Calculus AI Tutor in the Marimo MultivarGrapher 3D suite.
IMPORTANT: ALWAYS RESPOND IN ENGLISH.
Use clear, pedagogical explanations with formatted LaTeX math: $...$ for inline and \\[ ... \\] for block display equations. Never output unrendered dollar blocks.

Current live graph state:
- Function: {calc['raw_expr']}
- Optional Requirement / Constraint: {calc['constraint']['raw'] or 'None'}
- Evaluation Point a = ({a1}, {a2}, {a3})
- Value f(a) = {calc['fa']:.4f}
- Partial derivatives: fx1 = {calc['fx1']:.4f}, fx2 = {calc['fx2']:.4f}, fx3 = {calc['fx3']:.4f}
- Gradient magnitude: {calc['grad_mag']:.4f}
- Level set constant c = {calc['level_c']}
- Hessian: f11 = {calc['h11']:.4f}, f22 = {calc['h22']:.4f}, f12 = {calc['h12']:.4f}, det(H) = {calc['hessian_det']:.4f}
- Extremum classification: {calc['extremum_label']}

Instructions:
1. Answer the user's question directly in English using LaTeX math ($...$ and \\[ ... \\]).
2. If the user asks to create, graph, or change a function, flow line gamma(t) / integral curve, shape (ellipse, circle, saddle, paraboloid, cylinder, matrix, vector field), constraint, level c, or point a:
   Explain the math first, and at the very end output a ```graph_action block with valid JSON:
   - For cylinders in R3 (e.g. x1^2/4 + x2 = 1), set "f": "[x1; x2; x3]" and "constraint": "x1^2 / 4 + x2 = 1".
   - For flow lines gamma(t), set "show_flow_line": true.
   ```graph_action
   {{
     "f": "[x1; x2; x3]",
     "constraint": "x1^2 / 4 + x2 = 1",
     "c": 1.0,
     "a1": 2.0,
     "a2": 0.0,
     "a3": 1.0,
     "show_flow_line": false,
     "view_mode": "3D Surface"
   }}
   ```
"""
    fallback_reply, fallback_action = generate_offline_tutor_response(message, calc, a1, a2, a3)

    candidate_models = [
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
    ]
    payload_bytes = json.dumps(
        {"contents": [{"role": "user", "parts": [{"text": f"{system_prompt}\n\nUser Question: {message}"}]}]}
    ).encode("utf-8")
    ssl_ctx = ssl.create_default_context()

    for model in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=payload_bytes, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, context=ssl_ctx, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    raw_reply = "".join(p.get("text", "") for p in parts).strip()
                    if raw_reply:
                        clean_reply, action = extract_graph_action(raw_reply)
                        if fallback_action:
                            merged = dict(fallback_action)
                            if isinstance(action, dict):
                                for k, v in action.items():
                                    if v not in (None, ""):
                                        merged[k] = v
                            action = merged
                        return clean_reply, action, model
        except Exception:
            continue

    return fallback_reply, fallback_action, "Built-in Calculus Engine"
