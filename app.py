import marimo

__generated_with = "0.25.2"
app = marimo.App(width="full", app_title="MultivarGrapher 3D | Reactive Marimo Calculus Suite")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import sympy as sp
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    return go, make_subplots, mo, np, sp


@app.cell
def _(mo):
    header = mo.md(
        r"""
        # 🪐 MultivarGrapher 3D — Reactive Calculus Suite
        **Powered by [marimo](https://github.com/marimo-team/marimo) & Plotly**  
        *Real-time multivariable calculus, 3D affine tangent planes, gradients, Hessian classification, and animations.*
        """
    )
    return (header,)


@app.cell
def _(mo):
    # Sidebar Controls: Presets, Function, Evaluation Point, Toggles, and Animation
    preset_dropdown = mo.ui.dropdown(
        options={
            "Circular Paraboloid (Bowl)": "x1**2 + x2**2",
            "Hyperbolic Paraboloid (Saddle)": "x1**2 - x2**2",
            "Elliptic Cone": "sqrt(x1**2 + x2**2 + 0.01)",
            "Monkey Saddle": "x1**3 - 3*x1*x2**2",
            "Ripple Wave": "sin(sqrt(x1**2 + x2**2))",
            "Rosenbrock Banana Valley": "(1 - x1)**2 + 10*(x2 - x1**2)**2",
            "Parabolic Cylinder in R3": "CYL_PARABOLA",
            "Elliptic Cylinder in R3": "CYL_ELLIPSE",
            "Lagrange Optimization": "LAGRANGE",
            "Custom Expression": "CUSTOM",
        },
        value="Circular Paraboloid (Bowl)",
        label="🎯 Mathematical Preset",
    )

    func_input = mo.ui.text(
        value="x1**2 + x2**2",
        label="Formula f(x1, x2) or [x1; x2; x3]",
    )

    constraint_input = mo.ui.text(
        value="",
        label="Optional Constraint / Requirement (e.g. x1**2/4 + x2 == 1)",
    )

    a1_slider = mo.ui.slider(
        start=-4.0, stop=4.0, step=0.1, value=1.0, label="Point a1 (x-coordinate)"
    )
    a2_slider = mo.ui.slider(
        start=-4.0, stop=4.0, step=0.1, value=1.0, label="Point a2 (y-coordinate)"
    )
    level_slider = mo.ui.slider(
        start=-8.0, stop=10.0, step=0.25, value=2.0, label="Level Set Constant (c)"
    )

    view_mode = mo.ui.radio(
        options=["3D Surface", "2D Level Sets", "Split Dual View"],
        value="Split Dual View",
        label="Viewport Layout",
    )

    anim_mode = mo.ui.dropdown(
        options={
            "Static (No Animation)": "none",
            "🌊 Slicing Plane Animation c(t)": "slice",
            "🎥 3D Camera Orbit Spin": "orbit",
            "✨ Glide Point a(t) along Surface": "glide",
        },
        value="Static (No Animation)",
        label="🎬 Animation Mode",
    )

    color_scheme = mo.ui.dropdown(
        options=["Viridis", "Plasma", "Magma", "Purples", "Spectral", "Turbo"],
        value="Viridis",
        label="🎨 Colorscale",
    )

    toggle_tangent = mo.ui.switch(value=True, label="Show Affine Tangent Plane g(x)")
    toggle_gradient = mo.ui.switch(value=True, label="Show Gradient Vector ∇f(a)")
    toggle_normal = mo.ui.switch(value=True, label="Show Normal Line")
    toggle_hessian = mo.ui.switch(value=True, label="Second Derivative Test (Hessian)")
    toggle_contours = mo.ui.switch(value=True, label="Show 3D Contour Rings")

    sidebar = mo.sidebar(
        [
            mo.md("### ⚙️ Function & Geometry Controls"),
            preset_dropdown,
            func_input,
            constraint_input,
            mo.md("---"),
            mo.md("### 📍 Evaluation Point & Level Set"),
            a1_slider,
            a2_slider,
            level_slider,
            mo.md("---"),
            mo.md("### 🎬 Animation & Visualization"),
            anim_mode,
            view_mode,
            color_scheme,
            mo.md("---"),
            mo.md("### 🔍 Mathematical Overlays"),
            toggle_tangent,
            toggle_gradient,
            toggle_normal,
            toggle_hessian,
            toggle_contours,
        ]
    )

    return (
        a1_slider,
        a2_slider,
        anim_mode,
        color_scheme,
        constraint_input,
        func_input,
        level_slider,
        preset_dropdown,
        sidebar,
        toggle_contours,
        toggle_gradient,
        toggle_hessian,
        toggle_normal,
        toggle_tangent,
        view_mode,
    )


@app.cell
def _(
    a1_slider,
    a2_slider,
    constraint_input,
    func_input,
    level_slider,
    np,
    preset_dropdown,
    sp,
):
    # Determine active formula and constraint from preset or custom input
    preset_val = preset_dropdown.value
    raw_expr = func_input.value.strip()
    raw_constraint = constraint_input.value.strip()

    is_cylinder_mode = False
    is_lagrange_mode = False

    if preset_val == "CYL_PARABOLA":
        raw_expr = "[x1, x2, x3]"
        raw_constraint = "x1**2 / 4 + x2 == 1"
        is_cylinder_mode = True
    elif preset_val == "CYL_ELLIPSE":
        raw_expr = "[x1, x2, x3]"
        raw_constraint = "x1**2 / 4 + x2**2 / 9 == 1"
        is_cylinder_mode = True
    elif preset_val == "LAGRANGE":
        raw_expr = "x1 * x2"
        raw_constraint = "x1**2 + x2**2 == 4"
        is_lagrange_mode = True
    elif preset_val != "CUSTOM":
        raw_expr = preset_val

    # SymPy symbols
    x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)

    # Check if vector identity [x1, x2, x3]
    if "[" in raw_expr and "x3" in raw_expr:
        is_cylinder_mode = True

    # Parse main scalar function
    parse_expr = raw_expr
    if is_cylinder_mode:
        # Default scalar visualization for identity cylinder is distance or x1^2/4 + x2
        parse_expr = "x1**2 / 4 + x2" if "x2**2" not in raw_constraint else "x1**2 / 4 + x2**2 / 9"

    try:
        f_sym = sp.sympify(parse_expr.replace("^", "**"))
    except Exception:
        f_sym = x1**2 + x2**2

    # Symbolic partial derivatives
    df_dx1_sym = sp.diff(f_sym, x1)
    df_dx2_sym = sp.diff(f_sym, x2)

    # Second order partial derivatives
    f11_sym = sp.diff(df_dx1_sym, x1)
    f22_sym = sp.diff(df_dx2_sym, x2)
    f12_sym = sp.diff(df_dx1_sym, x2)
    hessian_det_sym = f11_sym * f22_sym - f12_sym**2

    # Lambdify for fast numpy evaluation
    f_num = sp.lambdify((x1, x2), f_sym, "numpy")
    df_dx1_num = sp.lambdify((x1, x2), df_dx1_sym, "numpy")
    df_dx2_num = sp.lambdify((x1, x2), df_dx2_sym, "numpy")
    f11_num = sp.lambdify((x1, x2), f11_sym, "numpy")
    f22_num = sp.lambdify((x1, x2), f22_sym, "numpy")
    f12_num = sp.lambdify((x1, x2), f12_sym, "numpy")

    # Evaluation point values
    a1_val = float(a1_slider.value)
    a2_val = float(a2_slider.value)
    c_val = float(level_slider.value)

    try:
        fa_val = float(f_num(a1_val, a2_val))
    except Exception:
        fa_val = 0.0

    try:
        fx1_val = float(df_dx1_num(a1_val, a2_val))
        fx2_val = float(df_dx2_num(a1_val, a2_val))
    except Exception:
        fx1_val, fx2_val = 0.0, 0.0

    grad_mag = np.sqrt(fx1_val**2 + fx2_val**2)

    # Hessian numerical values at a
    try:
        h11 = float(f11_num(a1_val, a2_val))
        h22 = float(f22_num(a1_val, a2_val))
        h12 = float(f12_num(a1_val, a2_val))
        hess_det = h11 * h22 - h12**2
    except Exception:
        h11, h22, h12, hess_det = 0.0, 0.0, 0.0, 0.0

    # Second derivative test classification
    if grad_mag < 1e-3:
        if hess_det > 1e-4 and h11 > 0:
            verdict_text = "🟢 Local Minimum (Cup / Basin)"
            verdict_badge = "success"
        elif hess_det > 1e-4 and h11 < 0:
            verdict_text = "🔴 Local Maximum (Hilltop Peak)"
            verdict_badge = "danger"
        elif hess_det < -1e-4:
            verdict_text = "🟡 Saddle Point (Min in one dir, Max in other)"
            verdict_badge = "warn"
        else:
            verdict_text = "⚪ Inconclusive (D ≈ 0, higher order terms needed)"
            verdict_badge = "info"
    else:
        verdict_text = f"⚪ Not a Critical Point (∇f ≠ 0, Magnitude = {grad_mag:.3f})"
        verdict_badge = "info"

    return (
        a1_val,
        a2_val,
        c_val,
        df_dx1_num,
        df_dx1_sym,
        df_dx2_num,
        df_dx2_sym,
        f11_num,
        f11_sym,
        f12_num,
        f12_sym,
        f22_num,
        f22_sym,
        f_num,
        f_sym,
        fa_val,
        fx1_val,
        fx2_val,
        grad_mag,
        h11,
        h12,
        h22,
        hess_det,
        is_cylinder_mode,
        is_lagrange_mode,
        raw_constraint,
        raw_expr,
        verdict_badge,
        verdict_text,
        x1,
        x2,
        x3,
    )


@app.cell
def _(
    a1_val,
    a2_val,
    c_val,
    df_dx1_sym,
    df_dx2_sym,
    f_sym,
    fa_val,
    fx1_val,
    fx2_val,
    grad_mag,
    h11,
    h12,
    h22,
    hess_det,
    is_cylinder_mode,
    mo,
    raw_constraint,
    raw_expr,
    verdict_text,
):
    # Metric cards & LaTeX summaries
    stat_fa = mo.stat(
        value=f"{fa_val:.3f}",
        label="f(a)",
        caption=f"Evaluated at ({a1_val:.2f}, {a2_val:.2f})",
    )
    stat_grad = mo.stat(
        value=f"[{fx1_val:.2f}, {fx2_val:.2f}]",
        label="∇f(a)",
        caption=f"Magnitude ‖∇f‖ = {grad_mag:.3f}",
    )
    stat_hess = mo.stat(
        value=f"D = {hess_det:.3f}",
        label="Hessian Det",
        caption=f"f₁₁={h11:.2f}, f₂₂={h22:.2f}, f₁₂={h12:.2f}",
    )
    stat_verdict = mo.stat(
        value=verdict_text.split(" ")[0] + " " + verdict_text.split(" ")[1],
        label="Extremum Test",
        caption=verdict_text,
    )

    stats_row = mo.hstack([stat_fa, stat_grad, stat_hess, stat_verdict], justify="space-between")

    # Math card with KaTeX
    sign_x1 = f"- {a1_val:.2f}" if a1_val >= 0 else f"+ {abs(a1_val):.2f}"
    sign_x2 = f"- {a2_val:.2f}" if a2_val >= 0 else f"+ {abs(a2_val):.2f}"
    constraint_str = f"\\quad \\text{{s.t. }} {raw_constraint}" if raw_constraint else ""

    math_card = mo.callout(
        mo.md(
            rf"""
            ### 📐 Live Mathematical Formulation
            - **Function:** $$f(x_1, x_2) = {raw_expr} {constraint_str}$$
            - **Total Derivative Row Matrix:** $$\mathbf{{D}}f(\mathbf{{a}}) = \begin{{bmatrix}} \frac{{\partial f}}{{\partial x_1}} & \frac{{\partial f}}{{\partial x_2}} \end{{bmatrix}} = \begin{{bmatrix}} {fx1_val:.3f} & {fx2_val:.3f} \end{{bmatrix}}_{{1 \times 2}}$$
            - **Gradient Column Vector:** $$\nabla f(\mathbf{{a}}) = (\mathbf{{D}}f(\mathbf{{a}}))^T = \begin{{bmatrix}} {fx1_val:.3f} \\ {fx2_val:.3f} \end{{bmatrix}}_{{2 \times 1}} \quad (\|\nabla f\| = {grad_mag:.3f})$$
            - **Affine Tangent Plane:** $$g(x_1, x_2) = {fa_val:.3f} + {fx1_val:.3f}(x_1 {sign_x1}) + {fx2_val:.3f}(x_2 {sign_x2})$$
            - **Hessian Matrix:** $$\mathbf{{H}} = \begin{{bmatrix}} {h11:.3f} & {h12:.3f} \\ {h12:.3f} & {h22:.3f} \end{{bmatrix}}, \quad D = \det(\mathbf{{H}}) = {hess_det:.3f}$$
            """
        ),
        kind="info",
    )

    return math_card, stats_row


@app.cell
def _(
    a1_val,
    a2_val,
    anim_mode,
    c_val,
    color_scheme,
    f_num,
    fa_val,
    fx1_val,
    fx2_val,
    go,
    is_cylinder_mode,
    make_subplots,
    mo,
    np,
    raw_constraint,
    toggle_contours,
    toggle_gradient,
    toggle_normal,
    toggle_tangent,
    view_mode,
):
    # Construct 3D and 2D Plotly Visualizations
    resolution = 40
    xr = np.linspace(-4, 4, resolution)
    yr = np.linspace(-4, 4, resolution)
    X, Y = np.meshgrid(xr, yr)

    try:
        Z = f_num(X, Y)
        if np.isscalar(Z):
            Z = np.full_like(X, float(Z))
        Z = np.nan_to_num(Z, nan=np.nan, posinf=np.nan, neginf=np.nan)
    except Exception:
        Z = X**2 + Y**2

    # Tangent plane grid
    px = np.linspace(a1_val - 1.8, a1_val + 1.8, 15)
    py = np.linspace(a2_val - 1.8, a2_val + 1.8, 15)
    PX, PY = np.meshgrid(px, py)
    PZ = fa_val + fx1_val * (PX - a1_val) + fx2_val * (PY - a2_val)

    # 3D Normal line segment
    n_len = 2.0
    norm_x = [a1_val, a1_val - fx1_val * 0.5]
    norm_y = [a2_val, a2_val - fx2_val * 0.5]
    norm_z = [fa_val, fa_val + n_len * 0.5]

    # Check if cylinder extrusion mode
    is_extrude = is_cylinder_mode or ("x1**2 / 4" in raw_constraint or "x1^2/4" in raw_constraint)
    cylinder_trace = None

    if is_extrude:
        # Generate 3D cylindrical surface by extruding 2D curve along z
        theta_cyl = np.linspace(0, 2 * np.pi, 60)
        # Parabolic or elliptic cross section
        if "x2**2" in raw_constraint or "x2^2" in raw_constraint:
            # Ellipse: x1^2/4 + x2^2/9 = 1
            cx = 2.0 * np.cos(theta_cyl)
            cy = 3.0 * np.sin(theta_cyl)
        else:
            # Parabola: x1^2/4 + x2 = 1 -> x2 = 1 - x1^2/4
            cx = np.linspace(-2.2, 2.2, 50)
            cy = 1.0 - (cx**2) / 4.0

        cz = np.linspace(-4, 4, 25)
        CX = np.outer(cx, np.ones_like(cz))
        CY = np.outer(cy, np.ones_like(cz))
        CZ = np.outer(np.ones_like(cx), cz)

        cylinder_trace = go.Surface(
            x=CX,
            y=CY,
            z=CZ,
            colorscale="Purples",
            opacity=0.75,
            name="3D Extruded Cylinder (Free x3)",
            showscale=False,
            contours_z=dict(show=True, usecolormap=True, highlightcolor="#00ffff", project_z=False),
        )

    # -------------------------------------------------------------
    # Build 3D Traces
    # -------------------------------------------------------------
    traces_3d = []

    # Main surface
    if cylinder_trace is not None and is_cylinder_mode:
        traces_3d.append(cylinder_trace)
    else:
        surf_trace = go.Surface(
            x=X,
            y=Y,
            z=Z,
            colorscale=color_scheme.value,
            opacity=0.92,
            name="Surface z = f(x1, x2)",
            contours_z=dict(
                show=toggle_contours.value,
                usecolormap=True,
                highlightcolor="#ffffff",
                project_z=True,
            ),
        )
        traces_3d.append(surf_trace)

        if cylinder_trace is not None:
            traces_3d.append(cylinder_trace)

    # Affine Tangent Plane
    if toggle_tangent.value and not is_cylinder_mode:
        tangent_trace = go.Surface(
            x=PX,
            y=PY,
            z=PZ,
            colorscale=[[0, "rgba(236,72,153,0.7)"], [1, "rgba(168,85,247,0.7)"]],
            showscale=False,
            name="Tangent Plane g(x)",
            opacity=0.7,
        )
        traces_3d.append(tangent_trace)

    # Point a marker
    point_trace = go.Scatter3d(
        x=[a1_val],
        y=[a2_val],
        z=[fa_val],
        mode="markers+text",
        marker=dict(size=8, color="#00ffff", symbol="diamond", line=dict(color="#ffffff", width=2)),
        text=["a = (a1, a2, f(a))"],
        textposition="top center",
        name="Point a",
    )
    traces_3d.append(point_trace)

    # Normal Line
    if toggle_normal.value and not is_cylinder_mode:
        norm_trace = go.Scatter3d(
            x=norm_x,
            y=norm_y,
            z=norm_z,
            mode="lines+markers",
            line=dict(color="#22c55e", width=6),
            marker=dict(size=4),
            name="Normal Line (90°)",
        )
        traces_3d.append(norm_trace)

    # Gradient Vector in 3D (projected at base level)
    if toggle_gradient.value:
        grad_3d = go.Scatter3d(
            x=[a1_val, a1_val + fx1_val * 0.4],
            y=[a2_val, a2_val + fx2_val * 0.4],
            z=[fa_val, fa_val],
            mode="lines+markers",
            line=dict(color="#f59e0b", width=7),
            marker=dict(size=[0, 6], symbol="diamond"),
            name="Gradient ∇f(a)",
        )
        traces_3d.append(grad_3d)

    # Slicing Plane at z = c
    slice_plane_z = np.full_like(X, c_val)
    slice_trace = go.Surface(
        x=X,
        y=Y,
        z=slice_plane_z,
        colorscale=[[0, "rgba(14,165,233,0.3)"], [1, "rgba(14,165,233,0.3)"]],
        showscale=False,
        name=f"Level Slice z = {c_val:.2f}",
        opacity=0.35,
    )
    traces_3d.append(slice_trace)

    # -------------------------------------------------------------
    # Build 2D Traces
    # -------------------------------------------------------------
    contour_2d = go.Contour(
        x=xr,
        y=yr,
        z=Z,
        colorscale=color_scheme.value,
        contours=dict(coloring="heatmap", showlabels=True),
        name="Level Sets",
    )

    # Point a on 2D
    point_2d = go.Scatter(
        x=[a1_val],
        y=[a2_val],
        mode="markers+text",
        marker=dict(size=12, color="#00ffff", line=dict(color="#000000", width=2)),
        text=["a"],
        textposition="top right",
        name="Point a",
    )

    # Gradient vector arrow on 2D
    grad_2d = go.Scatter(
        x=[a1_val, a1_val + fx1_val * 0.4],
        y=[a2_val, a2_val + fx2_val * 0.4],
        mode="lines+markers",
        line=dict(color="#f59e0b", width=4),
        marker=dict(size=[0, 8]),
        name="∇f(a)",
    )

    # Tangent line in 2D (orthogonal to gradient)
    tangent_2d = go.Scatter(
        x=[a1_val - fx2_val * 0.4, a1_val + fx2_val * 0.4],
        y=[a2_val + fx1_val * 0.4, a2_val - fx1_val * 0.4],
        mode="lines",
        line=dict(color="#ec4899", width=3, dash="dash"),
        name="Tangent Line (Level Set)",
    )

    # Active level curve highlight at c
    level_curve_highlight = go.Contour(
        x=xr,
        y=yr,
        z=Z,
        contours=dict(
            start=c_val,
            end=c_val,
            size=1,
            coloring="none",
            showlabels=True,
        ),
        line=dict(color="#ffffff", width=4),
        name=f"Level Curve f = {c_val:.2f}",
    )

    # -------------------------------------------------------------
    # Assemble Layout based on View Mode
    # -------------------------------------------------------------
    vm = view_mode.value
    anim = anim_mode.value

    # Animation frames configuration
    frames = []
    updatemenus = []

    if anim == "slice":
        # Slicing animation frames across range of c
        c_steps = np.linspace(-4, 6, 25)
        for idx, ct in enumerate(c_steps):
            f_slice = go.Surface(
                x=X,
                y=Y,
                z=np.full_like(X, ct),
                colorscale=[[0, "rgba(14,165,233,0.35)"], [1, "rgba(14,165,233,0.35)"]],
                showscale=False,
                opacity=0.35,
            )
            frames.append(
                go.Frame(
                    data=[None, None, None, None, None, f_slice],
                    name=f"c={ct:.2f}",
                )
            )
        updatemenus = [
            dict(
                type="buttons",
                buttons=[
                    dict(label="▶ Play Slicing", method="animate", args=[None, dict(frame=dict(duration=80, redraw=True), fromcurrent=True)]),
                    dict(label="⏸ Pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")]),
                ],
                direction="left",
                pad=dict(r=10, t=10),
                showactive=True,
                x=0.05,
                y=1.12,
            )
        ]
    elif anim == "orbit":
        # 3D Camera Orbit frames
        angles = np.linspace(0, 2 * np.pi, 30)
        for idx, ang in enumerate(angles):
            eye_x = 1.8 * np.cos(ang)
            eye_y = 1.8 * np.sin(ang)
            frames.append(
                go.Frame(
                    layout=dict(
                        scene=dict(
                            camera=dict(
                                eye=dict(x=eye_x, y=eye_y, z=1.2)
                            )
                        )
                    ),
                    name=f"ang={idx}",
                )
            )
        updatemenus = [
            dict(
                type="buttons",
                buttons=[
                    dict(label="🔄 Orbit 360°", method="animate", args=[None, dict(frame=dict(duration=60, redraw=True), fromcurrent=True)]),
                    dict(label="⏸ Pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")]),
                ],
                direction="left",
                pad=dict(r=10, t=10),
                showactive=True,
                x=0.05,
                y=1.12,
            )
        ]
    elif anim == "glide":
        # Gliding point a(t) in an ellipse orbit
        t_orbit = np.linspace(0, 2 * np.pi, 24)
        for idx, t_val in enumerate(t_orbit):
            ga1 = 2.0 * np.cos(t_val)
            ga2 = 2.0 * np.sin(t_val)
            try:
                gfa = float(f_num(ga1, ga2))
            except Exception:
                gfa = 0.0

            f_pt = go.Scatter3d(
                x=[ga1],
                y=[ga2],
                z=[gfa],
                mode="markers",
                marker=dict(size=9, color="#00ffff", line=dict(color="#ffffff", width=2)),
            )
            frames.append(go.Frame(data=[None, None, f_pt], name=f"t={idx}"))

        updatemenus = [
            dict(
                type="buttons",
                buttons=[
                    dict(label="✨ Glide Point a(t)", method="animate", args=[None, dict(frame=dict(duration=80, redraw=True), fromcurrent=True)]),
                    dict(label="⏸ Pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")]),
                ],
                direction="left",
                pad=dict(r=10, t=10),
                showactive=True,
                x=0.05,
                y=1.12,
            )
        ]

    # Create figure
    if vm == "3D Surface":
        fig = go.Figure(data=traces_3d, frames=frames)
        fig.update_layout(
            title=dict(text="🌌 3D Surface View with Tangent Geometry", font=dict(size=16)),
            scene=dict(
                xaxis=dict(title="x1", backgroundcolor="rgba(15,23,42,0.6)", gridcolor="rgba(148,163,184,0.2)"),
                yaxis=dict(title="x2", backgroundcolor="rgba(15,23,42,0.6)", gridcolor="rgba(148,163,184,0.2)"),
                zaxis=dict(title="z = f(x1, x2)", backgroundcolor="rgba(15,23,42,0.6)", gridcolor="rgba(148,163,184,0.2)"),
                camera=dict(eye=dict(x=1.6, y=1.6, z=1.2)),
            ),
            margin=dict(l=0, r=0, b=0, t=40),
            height=650,
            updatemenus=updatemenus,
        )
    elif vm == "2D Level Sets":
        fig = go.Figure(data=[contour_2d, level_curve_highlight, point_2d, grad_2d, tangent_2d])
        fig.update_layout(
            title=dict(text="🎯 2D Level Sets f⁻¹(c) with Gradient & Tangent", font=dict(size=16)),
            xaxis=dict(title="x1", range=[-4, 4], scaleanchor="y", scaleratio=1),
            yaxis=dict(title="x2", range=[-4, 4]),
            margin=dict(l=20, r=20, b=20, t=40),
            height=650,
        )
    else:
        # Split dual view
        fig = make_subplots(
            rows=1,
            cols=2,
            specs=[[{"type": "scene"}, {"type": "xy"}]],
            subplot_titles=["3D Surface & Affine Plane", "2D Level Curves & ∇f(a)"],
            column_widths=[0.58, 0.42],
        )
        for t in traces_3d:
            fig.add_trace(t, row=1, col=1)

        fig.add_trace(contour_2d, row=1, col=2)
        fig.add_trace(level_curve_highlight, row=1, col=2)
        fig.add_trace(point_2d, row=1, col=2)
        fig.add_trace(grad_2d, row=1, col=2)
        fig.add_trace(tangent_2d, row=1, col=2)

        fig.update_layout(
            scene=dict(
                xaxis=dict(title="x1"),
                yaxis=dict(title="x2"),
                zaxis=dict(title="z"),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
            ),
            margin=dict(l=0, r=0, b=0, t=40),
            height=650,
            updatemenus=updatemenus,
        )

    # Plotly theme matching marimo dark/light
    fig.update_layout(
        template="plotly_dark",
        font=dict(family="system-ui, -apple-system, sans-serif"),
    )

    plot_ui = mo.ui.plotly(fig)
    return (plot_ui,)


@app.cell
def _(mo):
    accordion_help = mo.accordion(
        {
            "💡 Why does marimo make multivariable calculus cooler?": mo.md(
                r"""
                - **Reactive Dataflow DAG:** Every widget (sliders for $\mathbf{a}$, level constant $c$, preset dropdown) updates the exact downstream calculus calculations in memory without reloading the page.
                - **Interactive Animations:** You can run smooth client-side Plotly animations (3D camera orbit, slicing plane sweeps, gliding point paths) or scrub them manually with Marimo reactive sliders.
                - **Pure Python & Reproducible:** The entire notebook is stored as clean Python code (`app.py`), executable as a web app with `marimo run app.py` or editable in the notebook editor with `marimo edit app.py`.
                """
            ),
            "📐 Affine Linearization & Tangent Plane": mo.md(
                r"""
                The **affine function** $g(\mathbf{x})$ is the best first-order linear approximation of $f$ near point $\mathbf{a}$:
                $$g(\mathbf{x}) = f(\mathbf{a}) + \mathbf{D}f(\mathbf{a})(\mathbf{x} - \mathbf{a})$$
                In 3D, the graph of $z = g(x_1, x_2)$ is the **tangent plane** kissing the surface $z = f(x_1, x_2)$ at $(\mathbf{a}, f(\mathbf{a}))$.
                """
            ),
            "🧭 Gradient & 90° Orthogonality to Level Curves": mo.md(
                r"""
                Along any level curve $f(x_1, x_2) = c$, the directional derivative along the tangent vector $\mathbf{T}$ is zero:
                $$\frac{df}{ds} = \nabla f(\mathbf{a}) \cdot \mathbf{T} = 0$$
                This proves that the gradient vector $\nabla f(\mathbf{a})$ is **strictly perpendicular ($90^\circ$)** to the tangent line of the level curve, pointing in the direction of steepest ascent!
                """
            ),
            "🏛️ Cylindrical Manifolds & Free Variables in R3": mo.md(
                r"""
                When an equation in $\mathbb{R}^3$ involves only two variables (like $x_1^2/4 + x_2 = 1$):
                - The variable $x_3$ is **free** ($-\infty < x_3 < \infty$).
                - The 2D curve in the $(x_1, x_2)$ plane is extruded vertically along the $x_3$ axis, forming a **cylinder**.
                - With $\mathbf{F}(x_1, x_2, x_3) = [x_1, x_2, x_3]^T$, the 3D viewport renders this continuous cylindrical manifold with horizontal contour rings.
                """
            ),
        }
    )
    return (accordion_help,)


@app.cell
def _(accordion_help, header, math_card, mo, plot_ui, sidebar, stats_row):
    # Main page layout combining header, stats, plots, and educational accordions
    main_layout = mo.vstack(
        [
            header,
            stats_row,
            plot_ui,
            math_card,
            accordion_help,
        ],
        gap=1.2,
    )
    return (main_layout,)


if __name__ == "__main__":
    app.run()
