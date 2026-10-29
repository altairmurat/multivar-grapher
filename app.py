import marimo

__generated_with = "0.25.2"
app = marimo.App(
    width="full",
    app_title="MultivarGrapher 3D — Interactive Marimo Calculus Suite",
    css_file="custom.css",
)


@app.cell
def _():
    import os
    import urllib.parse
    import marimo as mo
    import numpy as np
    import calculus_engine as ce

    return ce, mo, np, os, urllib


@app.cell
def _(ce, mo):
    # Initialize reactive state, reading URL query parameters if present for instant link restoration
    qp = mo.query_params()

    def _safe_float(val, default: float) -> float:
        try:
            return float(val) if val is not None else default
        except Exception:
            return default

    init_cfg = {
        "f": str(qp.get("f") or "x1^2 + x2^2"),
        "constraint": str(qp.get("constraint") or ""),
        "c": _safe_float(qp.get("c"), 4.0),
        "r": _safe_float(qp.get("r"), 2.0),
        "a1": _safe_float(qp.get("a1"), 2.0),
        "a2": _safe_float(qp.get("a2"), 0.0),
        "a3": _safe_float(qp.get("a3"), 0.0),
        "test_x": _safe_float(qp.get("tx"), 2.1),
        "test_y": _safe_float(qp.get("ty"), 0.2),
        "xr_min": _safe_float(qp.get("xmin"), -6.0),
        "xr_max": _safe_float(qp.get("xmax"), 6.0),
        "yr_min": _safe_float(qp.get("ymin"), -6.0),
        "yr_max": _safe_float(qp.get("ymax"), 6.0),
        "view_mode": str(qp.get("mode") or "Split Dual View"),
        "toast": "",
    }

    get_cfg, set_cfg = mo.state(init_cfg, allow_self_loops=True)
    get_chat_log, set_chat_log = mo.state(
        [
            {
                "role": "assistant",
                "content": (
                    "### 👋 Welcome to the Marimo AI Calculus Tutor!\n"
                    "Ask me about **gradients**, **affine tangent planes**, **normal lines ($90^\\circ$)**, "
                    "**Hessian matrices**, **3D cylinders with free variables**, or ask me to graph any surface "
                    "(e.g. *\"Make me an ellipse\"*, *\"Create a parabolic cylinder with x1^2/4 + x2 = 1\"*, "
                    "or *\"Show a 3x3 matrix in R3\"*)!"
                ),
            }
        ],
        allow_self_loops=True,
    )

    def apply_preset(preset_key: str):
        if preset_key not in ce.PRESETS:
            return
        p = ce.PRESETS[preset_key]
        set_cfg(
            lambda prev: {
                **prev,
                "f": p["f"],
                "constraint": p["constraint"],
                "c": p["c"],
                "r": p["r"],
                "a1": p["a1"],
                "a2": p["a2"],
                "a3": p["a3"],
                "xr_min": p["xr"][0],
                "xr_max": p["xr"][1],
                "yr_min": p["yr"][0],
                "yr_max": p["yr"][1],
                "view_mode": p["view_mode"],
                "toast": f"Loaded preset: {p['label']}",
            }
        )

    def apply_action_dict(action: dict, summary: str = ""):
        if not action or not isinstance(action, dict):
            return

        def _updater(prev):
            nxt = dict(prev)
            if "f" in action and action["f"] is not None:
                nxt["f"] = str(action["f"])
            if "constraint" in action and action["constraint"] is not None:
                nxt["constraint"] = str(action["constraint"])
            if "c" in action and action["c"] is not None:
                nxt["c"] = float(action["c"])
                if nxt["c"] >= 0:
                    nxt["r"] = round(nxt["c"] ** 0.5, 2)
            if "r" in action and action["r"] is not None:
                nxt["r"] = float(action["r"])
            if "a1" in action and action["a1"] is not None:
                nxt["a1"] = float(action["a1"])
            if "a2" in action and action["a2"] is not None:
                nxt["a2"] = float(action["a2"])
            if "a3" in action and action["a3"] is not None:
                nxt["a3"] = float(action["a3"])
            if "point_a" in action and isinstance(action["point_a"], (list, tuple)):
                pa = action["point_a"]
                if len(pa) >= 2:
                    nxt["a1"], nxt["a2"] = float(pa[0]), float(pa[1])
                if len(pa) >= 3:
                    nxt["a3"] = float(pa[2])
            vm = action.get("view_mode") or action.get("mode")
            if vm:
                vm_l = str(vm).lower()
                if "2d" in vm_l:
                    nxt["view_mode"] = "2D Level Sets"
                elif "3d" in vm_l:
                    nxt["view_mode"] = "3D Surface"
                else:
                    nxt["view_mode"] = "Split Dual View"
            nxt["toast"] = summary or action.get("description") or f"Updated graph: f = {nxt['f']}"
            return nxt

        set_cfg(_updater)

    return (
        apply_action_dict,
        apply_preset,
        get_cfg,
        get_chat_log,
        qp,
        set_cfg,
        set_chat_log,
    )


@app.cell
def _(apply_preset, ce, get_cfg, mo, set_cfg):
    cfg = get_cfg()

    # Preset selector with on_change callback that updates reactive state
    preset_options = {p["label"]: k for k, p in ce.PRESETS.items()}
    preset_selector = mo.ui.dropdown(
        options=preset_options,
        value=None,
        label="🎯 Load Mathematical Preset (17 Built-in Examples)",
        on_change=lambda val: apply_preset(val) if val else None,
        full_width=True,
    )

    # Function & Constraint Inputs bound to reactive state
    function_input = mo.ui.text(
        value=cfg["f"],
        label="Function f(x₁, x₂), f(x₁, x₂, x₃), Vector [F₁; F₂; F₃], or Matrix [a, b; c, d]",
        on_change=lambda v: set_cfg(lambda prev: {**prev, "f": v, "toast": ""}),
        full_width=True,
    )

    constraint_input = mo.ui.text(
        value=cfg["constraint"],
        placeholder="e.g. x1^2/4 + x2 = 1  or  x1^2/4 + x2^2/9 = 1  or  x1^2 + x2^2 <= 4",
        label="Optional Requirement / Constraint (Domain or Cylinder Equation)",
        on_change=lambda v: set_cfg(lambda prev: {**prev, "constraint": v, "toast": f"Constraint: {v}" if v else "Cleared constraint"}),
        full_width=True,
    )

    # Quick 1-click constraint chips
    chip_parab_cyl = mo.ui.button(
        label="🏛️ Parabolic Cylinder: [x₁;x₂;x₃] s.t. x₁²/4 + x₂ = 1",
        on_click=lambda _: set_cfg(
            lambda prev: {
                **prev,
                "f": "[x1; x2; x3]",
                "constraint": "x1^2 / 4 + x2 = 1",
                "view_mode": "3D Surface",
                "toast": "Applied Parabolic Cylinder in ℝ³ (free variable x₃)",
            }
        ),
    )
    chip_ellip_cyl = mo.ui.button(
        label="🏛️ Elliptic Cylinder: [x₁;x₂;x₃] s.t. x₁²/4 + x₂²/9 = 1",
        on_click=lambda _: set_cfg(
            lambda prev: {
                **prev,
                "f": "[x1; x2; x3]",
                "constraint": "x1^2 / 4 + x2^2 / 9 = 1",
                "view_mode": "3D Surface",
                "toast": "Applied Elliptic Cylinder in ℝ³ (free variable x₃)",
            }
        ),
    )
    chip_circle_req = mo.ui.button(
        label="⭕ Circle Cylinder: x₁² + x₂² = 4",
        on_click=lambda _: set_cfg(
            lambda prev: {**prev, "constraint": "x1^2 + x2^2 = 4", "toast": "Applied constraint x₁² + x₂² = 4"}
        ),
    )
    chip_disk_ineq = mo.ui.button(
        label="🛡️ Disk Domain: x₁² + x₂² <= 4",
        on_click=lambda _: set_cfg(
            lambda prev: {**prev, "constraint": "x1^2 + x2^2 <= 4", "toast": "Applied inequality domain x₁² + x₂² <= 4"}
        ),
    )
    chip_clear_req = mo.ui.button(
        label="✖ Clear Requirement",
        on_click=lambda _: set_cfg(
            lambda prev: {**prev, "constraint": "", "toast": "Cleared requirement"}
        ),
    )

    # Evaluation Point a = (a1, a2, a3) & Level Set c controls
    a1_slider = mo.ui.slider(
        start=-6.0,
        stop=6.0,
        step=0.05,
        value=float(np.clip(cfg["a1"], -6.0, 6.0)),
        label="Point a₁ (x₁ coordinate)",
        on_change=lambda v: set_cfg(lambda prev: {**prev, "a1": float(v)}),
        full_width=True,
    )
    a2_slider = mo.ui.slider(
        start=-6.0,
        stop=6.0,
        step=0.05,
        value=float(np.clip(cfg["a2"], -6.0, 6.0)),
        label="Point a₂ (x₂ coordinate)",
        on_change=lambda v: set_cfg(lambda prev: {**prev, "a2": float(v)}),
        full_width=True,
    )
    a3_slider = mo.ui.slider(
        start=-6.0,
        stop=6.0,
        step=0.05,
        value=float(np.clip(cfg["a3"], -6.0, 6.0)),
        label="Point a₃ (x₃ coordinate for ℝ³)",
        on_change=lambda v: set_cfg(lambda prev: {**prev, "a3": float(v)}),
        full_width=True,
    )

    level_c_slider = mo.ui.slider(
        start=-10.0,
        stop=15.0,
        step=0.1,
        value=float(np.clip(cfg["c"], -10.0, 15.0)),
        label="Target Level Set Constant c (f = c)",
        on_change=lambda v: set_cfg(
            lambda prev: {
                **prev,
                "c": float(v),
                "r": round(max(0.0, float(v)) ** 0.5, 2),
            }
        ),
        full_width=True,
    )

    radius_r_input = mo.ui.number(
        start=0.0,
        stop=10.0,
        step=0.1,
        value=float(np.clip(cfg["r"], 0.0, 10.0)),
        label="Circle Radius Helper r (sets c = r²)",
        on_change=lambda v: set_cfg(
            lambda prev: {
                **prev,
                "r": float(v or 0.0),
                "c": round(float(v or 0.0) ** 2, 2),
                "a1": float(v or 0.0),
                "a2": 0.0,
                "toast": f"Set radius r = {v} → level c = {float(v or 0.0)**2:.2f}",
            }
        ),
    )

    # Linearization Test Point x_test = (test_x, test_y)
    test_x_slider = mo.ui.slider(
        start=-6.0,
        stop=6.0,
        step=0.05,
        value=float(np.clip(cfg["test_x"], -6.0, 6.0)),
        label="Test Point x₁ (for Affine Error |f - g|)",
        on_change=lambda v: set_cfg(lambda prev: {**prev, "test_x": float(v)}),
        full_width=True,
    )
    test_y_slider = mo.ui.slider(
        start=-6.0,
        stop=6.0,
        step=0.05,
        value=float(np.clip(cfg["test_y"], -6.0, 6.0)),
        label="Test Point x₂ (for Affine Error |f - g|)",
        on_change=lambda v: set_cfg(lambda prev: {**prev, "test_y": float(v)}),
        full_width=True,
    )

    # Viewport, Animation, Theme & Notation Controls
    view_mode_radio = mo.ui.radio(
        options=["Split Dual View", "2D Level Sets", "3D Surface"],
        value=cfg["view_mode"] if cfg["view_mode"] in ("Split Dual View", "2D Level Sets", "3D Surface") else "Split Dual View",
        label="🖥️ Viewport Mode",
        inline=True,
        on_change=lambda v: set_cfg(lambda prev: {**prev, "view_mode": v}),
    )

    anim_mode_dropdown = mo.ui.dropdown(
        options={
            "Static (Interactive Drag / Zoom)": "none",
            "🎥 3D Camera Orbit 360° Spin": "orbit",
            "🌊 Animated Level Slice Sweep c(t)": "slice",
            "✨ Glide Point a(t) Along Surface": "glide",
        },
        value="Static (Interactive Drag / Zoom)",
        label="🎬 Marimo Animation Studio",
    )

    theme_switch = mo.ui.dropdown(
        options={"☀️ Modern Violet-White (Light)": "light", "🌙 Cosmic Purple (Dark)": "dark"},
        value="☀️ Modern Violet-White (Light)",
        label="🎨 Theme",
    )

    notation_switch = mo.ui.dropdown(
        options={"Subscript (x₁, x₂, x₃)": "x1x2", "Standard (x, y, z)": "xyz"},
        value="Subscript (x₁, x₂, x₃)",
        label="🔤 Notation",
    )

    colorscale_dropdown = mo.ui.dropdown(
        options=["Turbo", "Viridis", "Plasma", "Magma", "Purples", "Spectral"],
        value="Turbo",
        label="🌈 Surface Colorscale",
    )

    opacity_slider = mo.ui.slider(
        start=0.25, stop=1.0, step=0.05, value=0.92, label="Surface Opacity"
    )

    # Geometric Overlay Switches
    sw_gradient = mo.ui.switch(value=True, label="Show Gradient Vector ∇f(a)")
    sw_tangent_line = mo.ui.switch(value=True, label="Show 2D Tangent Line")
    sw_normal_line = mo.ui.switch(value=True, label="Show 2D Normal Line")
    sw_right_angle = mo.ui.switch(value=True, label="Show 90° Orthogonality Marker")
    sw_affine_plane = mo.ui.switch(value=True, label="Show 3D Affine Tangent Plane g(x)")
    sw_3d_normal = mo.ui.switch(value=True, label="Show 3D Surface Normal Vector")
    sw_error_rod = mo.ui.switch(value=False, label="Show Linearization Error Rod at x_test")
    sw_all_contours = mo.ui.switch(value=True, label="Show All Iso-Contour Lines")
    sw_constraint_surf = mo.ui.switch(value=True, label="Show 3D Extruded Constraint Cylinder")
    sw_constraint_curve = mo.ui.switch(value=True, label="Show Constraint Curve")

    # Parameter sliders a, b, c, d for parametric formulas
    param_a = mo.ui.slider(-5.0, 5.0, 0.1, 1.0, label="Param a")
    param_b = mo.ui.slider(-5.0, 5.0, 0.1, 1.0, label="Param b")
    param_c = mo.ui.slider(-5.0, 5.0, 0.1, 1.0, label="Param c")
    param_d = mo.ui.slider(-5.0, 5.0, 0.1, 1.0, label="Param d")

    return (
        a1_slider,
        a2_slider,
        a3_slider,
        anim_mode_dropdown,
        cfg,
        chip_circle_req,
        chip_clear_req,
        chip_disk_ineq,
        chip_ellip_cyl,
        chip_parab_cyl,
        colorscale_dropdown,
        constraint_input,
        function_input,
        level_c_slider,
        notation_switch,
        opacity_slider,
        param_a,
        param_b,
        param_c,
        param_d,
        preset_selector,
        radius_r_input,
        sw_3d_normal,
        sw_affine_plane,
        sw_all_contours,
        sw_constraint_curve,
        sw_constraint_surf,
        sw_error_rod,
        sw_gradient,
        sw_normal_line,
        sw_right_angle,
        sw_tangent_line,
        test_x_slider,
        test_y_slider,
        theme_switch,
        view_mode_radio,
    )


@app.cell
def _(
    ce,
    cfg,
    notation_switch,
    param_a,
    param_b,
    param_c,
    param_d,
    qp,
    set_cfg,
):
    # Sync URL query params so copying the browser link preserves state
    try:
        qp["f"] = cfg["f"]
        if cfg["constraint"]:
            qp["constraint"] = cfg["constraint"]
        elif "constraint" in qp:
            del qp["constraint"]
        qp["c"] = str(round(cfg["c"], 2))
        qp["a1"] = str(round(cfg["a1"], 2))
        qp["a2"] = str(round(cfg["a2"], 2))
        qp["mode"] = cfg["view_mode"]
    except Exception:
        pass

    params_dict = {
        "a": float(param_a.value),
        "b": float(param_b.value),
        "c": float(param_c.value),
        "d": float(param_d.value),
    }

    calc = ce.analyze_calculus(
        raw_expr=cfg["f"],
        raw_constraint=cfg["constraint"],
        a1=cfg["a1"],
        a2=cfg["a2"],
        a3=cfg["a3"],
        level_c=cfg["c"],
        test_x=cfg["test_x"],
        test_y=cfg["test_y"],
        x_range=(cfg["xr_min"], cfg["xr_max"]),
        y_range=(cfg["yr_min"], cfg["yr_max"]),
        params=params_dict,
        notation=notation_switch.value,
    )

    def _do_snap_curve(_):
        nx1, nx2 = ce.snap_point_to_level_curve(calc, cfg["a1"], cfg["a2"], cfg["c"])
        set_cfg(
            lambda prev: {
                **prev,
                "a1": nx1,
                "a2": nx2,
                "toast": f"Snapped point a to ({nx1:.2f}, {nx2:.2f}) on level curve f = {cfg['c']:.2f}",
            }
        )

    def _do_snap_critical(_):
        cx1, cx2 = ce.snap_point_to_critical(calc, cfg["a1"], cfg["a2"])
        set_cfg(
            lambda prev: {
                **prev,
                "a1": cx1,
                "a2": cx2,
                "toast": f"Snapped point a to critical point ({cx1:.2f}, {cx2:.2f}) where ∇f = 0",
            }
        )

    return calc, params_dict


@app.cell
def _(calc, ce, cfg, mo, set_cfg):
    # Action buttons that depend on `calc`
    snap_curve_btn = mo.ui.button(
        label="🧲 Snap Point a to Level Curve f(a) = c",
        on_click=lambda _: (
            lambda nx1, nx2: set_cfg(
                lambda prev: {
                    **prev,
                    "a1": nx1,
                    "a2": nx2,
                    "toast": f"Snapped a = ({nx1:.2f}, {nx2:.2f}) onto f = {cfg['c']:.2f}",
                }
            )
        )(*ce.snap_point_to_level_curve(calc, cfg["a1"], cfg["a2"], cfg["c"])),
    )

    snap_critical_btn = mo.ui.button(
        label="🎯 Find & Snap to Critical Point (∇f = 0)",
        on_click=lambda _: (
            lambda cx1, cx2: set_cfg(
                lambda prev: {
                    **prev,
                    "a1": cx1,
                    "a2": cx2,
                    "toast": f"Snapped a = ({cx1:.2f}, {cx2:.2f}) to Critical Point",
                }
            )
        )(*ce.snap_point_to_critical(calc, cfg["a1"], cfg["a2"])),
    )

    reset_domain_btn = mo.ui.button(
        label="🔄 Reset View & Point a",
        on_click=lambda _: set_cfg(
            lambda prev: {
                **prev,
                "a1": 2.0,
                "a2": 0.0,
                "a3": 0.0,
                "xr_min": -6.0,
                "xr_max": 6.0,
                "yr_min": -6.0,
                "yr_max": 6.0,
                "toast": "Reset coordinates and domain range to [-6, 6]",
            }
        ),
    )

    return reset_domain_btn, snap_critical_btn, snap_curve_btn


@app.cell
def _(
    anim_mode_dropdown,
    calc,
    ce,
    cfg,
    colorscale_dropdown,
    mo,
    opacity_slider,
    sw_3d_normal,
    sw_affine_plane,
    sw_all_contours,
    sw_constraint_curve,
    sw_constraint_surf,
    sw_error_rod,
    sw_gradient,
    sw_normal_line,
    sw_right_angle,
    sw_tangent_line,
    theme_switch,
):
    # Build main 2D / 3D / Split Plotly Figure
    fig = ce.build_plotly_figure(
        calc=calc,
        a1=cfg["a1"],
        a2=cfg["a2"],
        a3=cfg["a3"],
        level_c=cfg["c"],
        test_x=cfg["test_x"],
        test_y=cfg["test_y"],
        x_range=(cfg["xr_min"], cfg["xr_max"]),
        y_range=(cfg["yr_min"], cfg["yr_max"]),
        view_mode=cfg["view_mode"],
        anim_mode=anim_mode_dropdown.value,
        color_scale=colorscale_dropdown.value,
        opacity=float(opacity_slider.value),
        theme=theme_switch.value,
        show_gradient=sw_gradient.value,
        show_tangent_line=sw_tangent_line.value,
        show_normal_line=sw_normal_line.value,
        show_right_angle=sw_right_angle.value,
        show_affine_plane=sw_affine_plane.value,
        show_3d_normal=sw_3d_normal.value,
        show_error_rod=sw_error_rod.value,
        show_all_contours=sw_all_contours.value,
        show_constraint_surface=sw_constraint_surf.value,
        show_constraint_curve=sw_constraint_curve.value,
    )

    plotly_widget = mo.ui.plotly(fig)
    return fig, plotly_widget


@app.cell
def _(apply_action_dict, calc, ce, cfg, get_chat_log, mo, os, set_chat_log):
    # Built-in AI Calculus Tutor (Gemini 3.5 Flash-Lite + Offline Engine + Auto Graph Actions)
    has_env_key = bool(os.environ.get("GEMINI_API_KEY", "").strip())

    api_key_input = mo.ui.text(
        value="",
        kind="password",
        placeholder="Optional if GEMINI_API_KEY is set on server (uses Offline Engine if blank)",
        label=f"🔑 Gemini API Key ({'🟢 Connected via Render Env' if has_env_key else '⚡ Offline Math Engine Ready'})",
        full_width=True,
    )

    def _run_tutor_query(user_prompt: str):
        if not user_prompt or not user_prompt.strip():
            return
        q_clean = user_prompt.strip()
        reply_md, action_dict, model_label = ce.ask_ai_tutor(
            message=q_clean,
            calc=calc,
            a1=cfg["a1"],
            a2=cfg["a2"],
            a3=cfg["a3"],
            custom_api_key=api_key_input.value,
        )
        if action_dict:
            apply_action_dict(action_dict, summary=f"AI Tutor ({model_label}) updated the graph!")

        set_chat_log(
            lambda prev: prev
            + [
                {"role": "user", "content": q_clean},
                {"role": "assistant", "content": f"*{model_label}*\n\n{reply_md}"},
            ]
        )

    # Chat Model Callable for mo.ui.chat
    def _marimo_chat_model(messages):
        user_msg = messages[-1].content if messages else "Explain this graph"
        reply_md, action_dict, model_label = ce.ask_ai_tutor(
            message=str(user_msg),
            calc=calc,
            a1=cfg["a1"],
            a2=cfg["a2"],
            a3=cfg["a3"],
            custom_api_key=api_key_input.value,
        )
        if action_dict:
            apply_action_dict(action_dict, summary=f"AI Tutor ({model_label}) updated the graph!")
        return f"*{model_label}*\n\n{reply_md}"

    chat_widget = mo.ui.chat(
        _marimo_chat_model,
        prompts=[
            "Make me an ellipse",
            "Create a parabolic cylinder with x1^2/4 + x2 = 1",
            "Create an elliptic cylinder in R3",
            "Show a 3x3 matrix in R3: [1, 2, 3; 4, 5, 6; 7, 8, 9]",
            "Show me a saddle surface",
            "Explain the Hessian matrix and 2nd derivative test at point a",
            "Explain the affine function g(x) and tangent plane",
            "Why is the normal line perpendicular at 90 degrees?",
        ],
    )

    # Quick-Action AI Buttons for 1-click tutoring + graph generation
    ai_btn_ellipse = mo.ui.button(
        label="🪐 Ask AI: Make an Ellipse",
        on_click=lambda _: _run_tutor_query("Make me an ellipse"),
    )
    ai_btn_parab_cyl = mo.ui.button(
        label="🏛️ Ask AI: Parabolic Cylinder (x₁²/4 + x₂ = 1)",
        on_click=lambda _: _run_tutor_query("Create a parabolic cylinder with x1^2/4 + x2 = 1"),
    )
    ai_btn_ellip_cyl = mo.ui.button(
        label="🏛️ Ask AI: Elliptic Cylinder in ℝ³",
        on_click=lambda _: _run_tutor_query("Create an elliptic cylinder in R3"),
    )
    ai_btn_matrix3d = mo.ui.button(
        label="🧊 Ask AI: 3×3 Matrix in ℝ³",
        on_click=lambda _: _run_tutor_query("Show a 3x3 matrix in R3: [1, 2, 3; 4, 5, 6; 7, 8, 9]"),
    )
    ai_btn_hessian = mo.ui.button(
        label="🔍 Ask AI: Explain Hessian & Extrema",
        on_click=lambda _: _run_tutor_query("Explain the Hessian matrix and 2nd derivative test"),
    )
    ai_btn_affine = mo.ui.button(
        label="📐 Ask AI: Explain Affine Plane g(x)",
        on_click=lambda _: _run_tutor_query("Explain the affine function g(x) and tangent plane"),
    )

    return (
        ai_btn_affine,
        ai_btn_ellip_cyl,
        ai_btn_ellipse,
        ai_btn_hessian,
        ai_btn_matrix3d,
        ai_btn_parab_cyl,
        api_key_input,
        chat_widget,
        get_chat_log,
    )


@app.cell
def _(
    a1_slider,
    a2_slider,
    a3_slider,
    ai_btn_affine,
    ai_btn_ellip_cyl,
    ai_btn_ellipse,
    ai_btn_hessian,
    ai_btn_matrix3d,
    ai_btn_parab_cyl,
    anim_mode_dropdown,
    api_key_input,
    calc,
    cfg,
    chat_widget,
    chip_circle_req,
    chip_clear_req,
    chip_disk_ineq,
    chip_ellip_cyl,
    chip_parab_cyl,
    colorscale_dropdown,
    constraint_input,
    function_input,
    get_chat_log,
    level_c_slider,
    mo,
    notation_switch,
    opacity_slider,
    param_a,
    param_b,
    param_c,
    param_d,
    plotly_widget,
    preset_selector,
    radius_r_input,
    reset_domain_btn,
    snap_critical_btn,
    snap_curve_btn,
    sw_3d_normal,
    sw_affine_plane,
    sw_all_contours,
    sw_constraint_curve,
    sw_constraint_surf,
    sw_error_rod,
    sw_gradient,
    sw_normal_line,
    sw_right_angle,
    sw_tangent_line,
    test_x_slider,
    test_y_slider,
    theme_switch,
    urllib,
    view_mode_radio,
):
    # =========================================================================
    # BUILD THE 5 INTERACTIVE TABS & MAIN WORKSPACE LAYOUT
    # =========================================================================

    # Shareable URL string
    share_params = urllib.parse.urlencode(
        {
            "f": cfg["f"],
            "constraint": cfg["constraint"],
            "c": round(cfg["c"], 2),
            "a1": round(cfg["a1"], 2),
            "a2": round(cfg["a2"], 2),
            "mode": cfg["view_mode"],
        }
    )

    # Top Hero & Equation Banner
    toast_html = (
        f'<span class="mvg-badge-emerald">✨ {cfg["toast"]}</span>' if cfg.get("toast") else ""
    )
    constraint_badge_html = (
        f'<span class="mvg-badge-cyan">🏛️ {calc["constraint"]["status_text"]}</span>'
        if calc["constraint"]["active"]
        else ""
    )

    hero_banner = mo.md(
        rf"""
        <div class="mvg-hero-banner">
          <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:10px;">
            <div>
              <span class="mvg-badge">⚡ Powered by Marimo</span>
              <span class="mvg-badge-{calc['extremum_badge']}">{calc['extremum_label']}</span>
              {constraint_badge_html}
              {toast_html}
            </div>
            <div style="font-size:0.8rem; opacity:0.85; font-family:monospace;">
              🔗 Share Query: <code>?{share_params}</code>
            </div>
          </div>
          <div style="margin-top:10px; font-size:1.05rem;">
            $${calc['f_latex']}$$
          </div>
        </div>
        """
    )

    # Top Quick KPI Row
    a_coords_str = (
        f"({cfg['a1']:.2f}, {cfg['a2']:.2f}, {cfg['a3']:.2f})"
        if calc["dim"] == 3
        else f"({cfg['a1']:.2f}, {cfg['a2']:.2f})"
    )
    kpi_row = mo.hstack(
        [
            mo.stat(
                value=f"{calc['fa']:.3f}",
                label="Value f(a)",
                caption=f"At a = {a_coords_str}",
            ),
            mo.stat(
                value=f"[{calc['fx1']:.2f}, {calc['fx2']:.2f}]",
                label="Derivative Df(a)",
                caption=f"‖∇f(a)‖ = {calc['grad_mag']:.3f}",
            ),
            mo.stat(
                value=f"c = {cfg['c']:.2f}",
                label="Level Set f⁻¹(c)",
                caption=f"|f(a) - c| = {calc['level_diff']:.3f} (r = {cfg['r']:.2f})",
            ),
            mo.stat(
                value=f"D = {calc['hessian_det']:.2f}",
                label="Hessian Det(H)",
                caption=f"{calc['eigenvalues_str']} • tr(H)={calc['hessian_trace']:.2f}",
            ),
        ],
        widths="equal",
        gap=1.0,
    )

    # -------------------------------------------------------------------------
    # TAB 1: Level Sets, Point a & Derivative Matrix Df(a)
    # -------------------------------------------------------------------------
    tab1_content = mo.vstack(
        [
            mo.md("### 🎯 Level Set $f(x_1, x_2) = c$ & Evaluation Point $\\mathbf{a}$"),
            mo.hstack([level_c_slider, radius_r_input], widths=[0.65, 0.35]),
            mo.hstack([snap_curve_btn, snap_critical_btn, reset_domain_btn], justify="start", gap=0.6),
            mo.hstack([a1_slider, a2_slider, a3_slider], widths="equal"),
            mo.callout(
                mo.md(
                    rf"""
                    #### 🔢 Total Derivative Row Matrix $\mathbf{{D}}f(\mathbf{{a}})$ & Gradient $\nabla f(\mathbf{{a}})$
                    - **Symbolic Derivative:** $${calc['df_symbolic_latex']}$$
                    - **Numeric Derivative at $\mathbf{{a}}$:** $${calc['df_numeric_latex']}$$
                    - **Gradient Vector (Transpose):** $${calc['grad_latex']}$$
                    - **2D Unit Normal & Tangent:** $\mathbf{{n}}_{{2D}} = \langle {calc['unit_normal_2d'][0]:.3f}, {calc['unit_normal_2d'][1]:.3f} \rangle$, $\quad \mathbf{{T}}_{{2D}} = \langle {calc['unit_tangent_2d'][0]:.3f}, {calc['unit_tangent_2d'][1]:.3f} \rangle$ ($\mathbf{{n}} \cdot \mathbf{{T}} = 0 \implies 90^\circ$)
                    """
                ),
                kind="info",
            ),
        ],
        gap=0.8,
    )

    # -------------------------------------------------------------------------
    # TAB 2: Affine Approximation g(x) & Normal Line (90°)
    # -------------------------------------------------------------------------
    tab2_content = mo.vstack(
        [
            mo.md("### 📐 Affine Function $g(\\mathbf{x})$ (Tangent Plane) & Normal Line"),
            mo.callout(
                mo.md(
                    rf"""
                    #### Best First-Order Linear Approximation near $\mathbf{{a}} = ({cfg['a1']:.2f}, {cfg['a2']:.2f})$
                    - **General Formula:** $${calc['affine_symbolic_latex']}$$
                    - **Evaluated Formula:** $${calc['affine_numeric_latex']}$$
                    - **3D Surface Normal Vector:** $$\mathbf{{n}}_{{3D}} = \left\langle -\frac{{\partial f}}{{\partial x_1}}, -\frac{{\partial f}}{{\partial x_2}}, 1 \right\rangle = \left\langle {-calc['fx1']:.3f}, {-calc['fx2']:.3f}, 1.000 \right\rangle$$
                    """
                ),
                kind="success",
            ),
            mo.md("#### 🔬 Linearization Error Calculator at Test Point $\\mathbf{x}_{\\text{test}}$"),
            mo.hstack([test_x_slider, test_y_slider, sw_error_rod], widths=[0.4, 0.4, 0.2]),
            mo.hstack(
                [
                    mo.stat(value=f"{calc['test_exact']:.4f}", label="Exact Value f(x_test)"),
                    mo.stat(value=f"{calc['test_affine']:.4f}", label="Affine Approx g(x_test)"),
                    mo.stat(
                        value=f"{calc['test_error']:.4f}",
                        label="Approximation Error |f - g|",
                        caption="First-order Taylor remainder",
                    ),
                ],
                widths="equal",
            ),
        ],
        gap=0.8,
    )

    # -------------------------------------------------------------------------
    # TAB 3: Hessian Matrix H_f(a) & Second Derivative Extremum Test
    # -------------------------------------------------------------------------
    tab3_content = mo.vstack(
        [
            mo.md("### 🔍 Hessian Matrix $\\mathbf{H}_f(\\mathbf{a})$ & Second Derivative Test"),
            mo.hstack([snap_critical_btn, a1_slider, a2_slider], widths=[0.34, 0.33, 0.33]),
            mo.callout(
                mo.md(
                    rf"""
                    #### Quadratic Curvature & Discriminant Analysis
                    - **Symbolic Hessian:** $${calc['hessian_symbolic_latex']}$$
                    - **Numeric Hessian at $\mathbf{{a}}$:** $${calc['hessian_numeric_latex']}$$
                    - **Second Partials:** $f_{{11}} = {calc['h11']:.3f}, \quad f_{{22}} = {calc['h22']:.3f}, \quad f_{{12}} = {calc['h12']:.3f}$
                    - **Discriminant & Trace:** $D = f_{{11}}f_{{22}} - f_{{12}}^2 = {calc['hessian_det']:.3f}, \quad \operatorname{{tr}}(\mathbf{{H}}) = {calc['hessian_trace']:.3f}, \quad \text{{Eigenvalues: }} {calc['eigenvalues_str']}$
                    - **Classification Verdict:** **{calc['extremum_label']}**
                    """
                ),
                kind="warn" if calc["extremum_type"] == "saddle" else "info",
            ),
        ],
        gap=0.8,
    )

    # -------------------------------------------------------------------------
    # TAB 4: Function Definition, Matrices, Constraints & Free-Variable Cylinders
    # -------------------------------------------------------------------------
    tab4_content = mo.vstack(
        [
            mo.md("### 🏛️ Function, Matrices in $\\mathbb{R}^2 / \\mathbb{R}^3$ & Optional Requirements"),
            preset_selector,
            function_input,
            constraint_input,
            mo.md("**Quick Constraint / Cylinder Chips (Click to Apply):**"),
            mo.hstack(
                [chip_parab_cyl, chip_ellip_cyl, chip_circle_req, chip_disk_ineq, chip_clear_req],
                wrap=True,
                gap=0.5,
            ),
            mo.hstack([sw_constraint_surf, sw_constraint_curve], justify="start", gap=1.5),
            mo.md("#### 🎚️ Optional Formula Parameters $(a, b, c, d)$"),
            mo.hstack([param_a, param_b, param_c, param_d], widths="equal"),
        ],
        gap=0.8,
    )

    # -------------------------------------------------------------------------
    # TAB 5: AI Calculus Tutor (Gemini 3.5 Flash-Lite + Auto Graph Action)
    # -------------------------------------------------------------------------
    recent_log = get_chat_log()[-4:]
    log_md_blocks = "\n\n---\n\n".join(
        f"**{'🧑‍🎓 You' if m['role']=='user' else '🤖 AI Calculus Tutor'}:**\n\n{m['content']}"
        for m in recent_log
    )

    tab5_content = mo.vstack(
        [
            mo.md("### 🤖 AI Calculus Tutor (`gemini-3.5-flash-lite` + Auto Graph Action Engine)"),
            api_key_input,
            mo.md("**⚡ 1-Click AI Graph Actions & Explanations:**"),
            mo.hstack(
                [
                    ai_btn_parab_cyl,
                    ai_btn_ellip_cyl,
                    ai_btn_ellipse,
                    ai_btn_matrix3d,
                    ai_btn_hessian,
                    ai_btn_affine,
                ],
                wrap=True,
                gap=0.5,
            ),
            mo.callout(mo.md(log_md_blocks), kind="neutral"),
            mo.md("#### 💬 Interactive Chat (Ask anything or request any 2D/3D surface):"),
            chat_widget,
        ],
        gap=0.8,
    )

    control_tabs = mo.ui.tabs(
        {
            "🏛️ 1. Function & Constraints": tab4_content,
            "🎯 2. Level Set & Point a": tab1_content,
            "📐 3. Affine Plane & Normal": tab2_content,
            "🔍 4. Hessian & Extrema": tab3_content,
            "🤖 5. AI Calculus Tutor": tab5_content,
        }
    )

    # Sidebar for Quick Global Controls & Overlays
    sidebar = mo.sidebar(
        [
            mo.md("## 🌌 MultivarGrapher 3D"),
            mo.md("*100% Marimo Reactive Calculus Suite*"),
            preset_selector,
            function_input,
            constraint_input,
            mo.md("---"),
            mo.md("### 📍 Quick Point $\\mathbf{a}$ & Level $c$"),
            a1_slider,
            a2_slider,
            a3_slider,
            level_c_slider,
            snap_curve_btn,
            mo.md("---"),
            mo.md("### 🎬 Animation & Display"),
            view_mode_radio,
            anim_mode_dropdown,
            theme_switch,
            notation_switch,
            colorscale_dropdown,
            opacity_slider,
            mo.md("---"),
            mo.md("### 👁️ Geometric Overlays"),
            sw_gradient,
            sw_tangent_line,
            sw_normal_line,
            sw_right_angle,
            sw_affine_plane,
            sw_3d_normal,
            sw_error_rod,
            sw_all_contours,
            sw_constraint_surf,
            sw_constraint_curve,
        ]
    )

    # Main Workspace Layout
    workspace = mo.vstack(
        [
            hero_banner,
            kpi_row,
            mo.hstack([view_mode_radio, anim_mode_dropdown, theme_switch, notation_switch], justify="space-between", wrap=True),
            plotly_widget,
            control_tabs,
        ],
        gap=1.0,
    )

    mo.vstack([sidebar, workspace])
    return control_tabs, hero_banner, kpi_row, sidebar, workspace


if __name__ == "__main__":
    app.run()
