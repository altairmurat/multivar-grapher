import marimo

__generated_with = "0.25.2"
app = marimo.App(
    width="full",
    app_title="MultivarGrapher 3D — Clean Studio Edition",
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
    # Initialize reactive state, reading URL query parameters if present
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
        "show_flow_line": False,
        "toast": "",
    }

    get_cfg, set_cfg = mo.state(init_cfg, allow_self_loops=True)
    get_chat_log, set_chat_log = mo.state(
        [
            {
                "role": "assistant",
                "content": (
                    "**👋 Welcome to the AI Calculus Tutor!**\n\n"
                    "Type any request in the box **above** (and press **Enter** or click **🚀 Ask AI / Plot**), or click a quick button:\n"
                    "- *\"Create a flow line of gamma(t)\"*\n"
                    "- *\"Create a parabolic cylinder with x1^2/4 + x2 = 1\"*\n"
                    "- *\"Make me an ellipse\"* or *\"Show a 3x3 matrix in R3\"*"
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
                "show_flow_line": bool(p.get("show_flow_line", False)),
                "toast": f"Loaded: {p['label']}",
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
            if "show_flow_line" in action:
                nxt["show_flow_line"] = bool(action["show_flow_line"])
            toggles = action.get("toggles")
            if isinstance(toggles, dict) and "show_flow_line" in toggles:
                nxt["show_flow_line"] = bool(toggles["show_flow_line"])
            vm = action.get("view_mode") or action.get("mode")
            if vm:
                vm_l = str(vm).lower()
                if "2d" in vm_l:
                    nxt["view_mode"] = "2D Level Sets"
                elif "3d" in vm_l:
                    nxt["view_mode"] = "3D Surface"
                else:
                    nxt["view_mode"] = "Split Dual View"
            nxt["toast"] = summary or action.get("description") or f"Updated: f = {nxt['f']}"
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
def _(apply_preset, ce, get_cfg, mo, np, set_cfg):
    cfg = get_cfg()
    saved_key = ce.load_saved_api_key()

    # 1. Expression & Preset Controls (Short, crisp 1-line labels)
    preset_options = {p["label"]: k for k, p in ce.PRESETS.items()}
    preset_selector = mo.ui.dropdown(
        options=preset_options,
        value=None,
        label="📂 Load Preset Example",
        on_change=lambda val: apply_preset(val) if val else None,
        full_width=True,
    )

    function_input = mo.ui.text(
        value=cfg["f"],
        label="ƒ(x) Function, Matrix [a,b; c,d], or Vector [F₁; F₂; F₃]",
        on_change=lambda v: set_cfg(lambda prev: {**prev, "f": v, "toast": ""}),
        full_width=True,
    )

    constraint_input = mo.ui.text(
        value=cfg["constraint"],
        placeholder="e.g. x1^2/4 + x2 = 1  or  x1^2/4 + x2^2/9 = 1",
        label="🏛️ Domain / Cylinder Constraint (optional)",
        on_change=lambda v: set_cfg(
            lambda prev: {
                **prev,
                "constraint": v,
                "toast": f"Constraint: {v}" if v else "Cleared constraint",
            }
        ),
        full_width=True,
    )

    # Compact 1-click quick chips
    chip_flow_line = mo.ui.button(
        label="🌊 Flow Line γ(t)",
        on_click=lambda _: set_cfg(
            lambda prev: {
                **prev,
                "show_flow_line": not prev.get("show_flow_line", False),
                "a1": prev["a1"] if (abs(prev["a1"]) > 0.1 or abs(prev["a2"]) > 0.1) else 1.2,
                "a2": prev["a2"] if (abs(prev["a1"]) > 0.1 or abs(prev["a2"]) > 0.1) else 2.0,
                "toast": "Toggled Flow Line γ(t) of gradient field ∇f",
            }
        ),
    )
    chip_parab_cyl = mo.ui.button(
        label="🏛️ Parabolic Cyl",
        on_click=lambda _: set_cfg(
            lambda prev: {
                **prev,
                "f": "[x1; x2; x3]",
                "constraint": "x1^2 / 4 + x2 = 1",
                "view_mode": "3D Surface",
                "toast": "Parabolic Cylinder in ℝ³ (x₃ free)",
            }
        ),
    )
    chip_ellip_cyl = mo.ui.button(
        label="🏛️ Elliptic Cyl",
        on_click=lambda _: set_cfg(
            lambda prev: {
                **prev,
                "f": "[x1; x2; x3]",
                "constraint": "x1^2 / 4 + x2^2 / 9 = 1",
                "view_mode": "3D Surface",
                "toast": "Elliptic Cylinder in ℝ³ (x₃ free)",
            }
        ),
    )
    chip_circle_req = mo.ui.button(
        label="⭕ Circle c=4",
        on_click=lambda _: set_cfg(
            lambda prev: {
                **prev,
                "f": "x1^2 + x2^2",
                "constraint": "",
                "c": 4.0,
                "r": 2.0,
                "a1": 2.0,
                "a2": 0.0,
                "view_mode": "Split Dual View",
                "toast": "Circle x₁² + x₂² = 4",
            }
        ),
    )
    chip_clear_req = mo.ui.button(
        label="✖ Clear Constraint",
        on_click=lambda _: set_cfg(
            lambda prev: {**prev, "constraint": "", "toast": "Cleared constraint"}
        ),
    )

    # 2. Point a & Level Set c Sliders
    a1_slider = mo.ui.slider(
        start=-6.0,
        stop=6.0,
        step=0.05,
        value=float(np.clip(cfg["a1"], -6.0, 6.0)),
        label="Point a₁",
        on_change=lambda v: set_cfg(lambda prev: {**prev, "a1": float(v)}),
        full_width=True,
    )
    a2_slider = mo.ui.slider(
        start=-6.0,
        stop=6.0,
        step=0.05,
        value=float(np.clip(cfg["a2"], -6.0, 6.0)),
        label="Point a₂",
        on_change=lambda v: set_cfg(lambda prev: {**prev, "a2": float(v)}),
        full_width=True,
    )
    a3_slider = mo.ui.slider(
        start=-6.0,
        stop=6.0,
        step=0.05,
        value=float(np.clip(cfg["a3"], -6.0, 6.0)),
        label="Point a₃ (ℝ³)",
        on_change=lambda v: set_cfg(lambda prev: {**prev, "a3": float(v)}),
        full_width=True,
    )

    level_c_slider = mo.ui.slider(
        start=-10.0,
        stop=15.0,
        step=0.1,
        value=float(np.clip(cfg["c"], -10.0, 15.0)),
        label="Level Set c",
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
        label="Radius r (c = r²)",
        on_change=lambda v: set_cfg(
            lambda prev: {
                **prev,
                "r": float(v or 0.0),
                "c": round(float(v or 0.0) ** 2, 2),
                "a1": float(v or 0.0),
                "a2": 0.0,
                "toast": f"Radius r = {v} → c = {float(v or 0.0)**2:.2f}",
            }
        ),
    )

    # Test Point Sliders
    test_x_slider = mo.ui.slider(
        start=-6.0,
        stop=6.0,
        step=0.05,
        value=float(np.clip(cfg["test_x"], -6.0, 6.0)),
        label="Test x₁",
        on_change=lambda v: set_cfg(lambda prev: {**prev, "test_x": float(v)}),
        full_width=True,
    )
    test_y_slider = mo.ui.slider(
        start=-6.0,
        stop=6.0,
        step=0.05,
        value=float(np.clip(cfg["test_y"], -6.0, 6.0)),
        label="Test x₂",
        on_change=lambda v: set_cfg(lambda prev: {**prev, "test_y": float(v)}),
        full_width=True,
    )

    # Top Viewport & Animation Controls
    view_mode_radio = mo.ui.radio(
        options=["Split Dual View", "2D Level Sets", "3D Surface"],
        value=(
            cfg["view_mode"]
            if cfg["view_mode"] in ("Split Dual View", "2D Level Sets", "3D Surface")
            else "Split Dual View"
        ),
        label="View",
        inline=True,
        on_change=lambda v: set_cfg(lambda prev: {**prev, "view_mode": v}),
    )

    anim_mode_dropdown = mo.ui.dropdown(
        options={
            "Static (Interactive)": "none",
            "🎥 360° Camera Orbit": "orbit",
            "🌊 Slice Sweep c(t)": "slice",
            "✨ Glide Point a(t)": "glide",
        },
        value="Static (Interactive)",
        label="Animation",
    )

    theme_switch = mo.ui.dropdown(
        options={"☀️ Clean Light": "light", "🌙 Cosmic Dark": "dark"},
        value="☀️ Clean Light",
        label="Theme",
    )

    notation_switch = mo.ui.dropdown(
        options={"Subscript (x₁, x₂, x₃)": "x1x2", "Standard (x, y, z)": "xyz"},
        value="Subscript (x₁, x₂, x₃)",
        label="Notation",
    )

    colorscale_dropdown = mo.ui.dropdown(
        options=["Viridis", "Plasma", "Turbo", "Purples", "Spectral", "Cividis"],
        value="Viridis",
        label="Color Palette",
    )

    opacity_slider = mo.ui.slider(
        start=0.25, stop=1.0, step=0.05, value=0.85, label="3D Surface Opacity"
    )

    # Geometric Overlay Switches
    sw_flow_line = mo.ui.switch(
        value=bool(cfg.get("show_flow_line", False)),
        label="🌊 Flow Line γ(t) (γ' = ∇f)",
        on_change=lambda v: set_cfg(lambda prev: {**prev, "show_flow_line": bool(v)}),
    )
    sw_gradient = mo.ui.switch(value=True, label="🧭 Gradient Vector ∇f(a)")
    sw_tangent_line = mo.ui.switch(value=True, label="📏 2D Tangent Line")
    sw_normal_line = mo.ui.switch(value=True, label="📐 2D Normal Line (90°)")
    sw_right_angle = mo.ui.switch(value=True, label="⌞ 90° Right-Angle Marker")
    sw_affine_plane = mo.ui.switch(value=True, label="💠 3D Affine Plane g(x)")
    sw_3d_normal = mo.ui.switch(value=True, label="🚀 3D Surface Normal n₃D")
    sw_error_rod = mo.ui.switch(value=False, label="🔬 Error Rod at x_test")
    sw_all_contours = mo.ui.switch(value=True, label="🗺️ Background Contours")
    sw_constraint_surf = mo.ui.switch(value=True, label="🏛️ 3D Constraint Cylinder")
    sw_constraint_curve = mo.ui.switch(value=True, label="⭕ 2D Constraint Curve")

    # Parameter sliders a, b, c, d
    param_a = mo.ui.slider(-5.0, 5.0, 0.1, 1.0, label="a")
    param_b = mo.ui.slider(-5.0, 5.0, 0.1, 1.0, label="b")
    param_c = mo.ui.slider(-5.0, 5.0, 0.1, 1.0, label="c")
    param_d = mo.ui.slider(-5.0, 5.0, 0.1, 1.0, label="d")

    # Define api_key_input in THIS cell so its .value can be safely read in the AI Tutor cell!
    api_key_input = mo.ui.text(
        value=saved_key,
        kind="password",
        placeholder="Paste Gemini API key (auto-saved locally) or leave blank for Built-in Engine",
        label=f"🔑 Gemini API Key ({'🟢 Key Saved & Active' if saved_key else '⚡ Built-in Calculus Engine Active'})",
        on_change=lambda k: ce.save_api_key(k),
        full_width=True,
    )

    return (
        a1_slider,
        a2_slider,
        a3_slider,
        anim_mode_dropdown,
        api_key_input,
        cfg,
        chip_circle_req,
        chip_clear_req,
        chip_ellip_cyl,
        chip_flow_line,
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
        sw_flow_line,
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
):
    # Sync URL query params for link sharing
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

    return calc, params_dict


@app.cell
def _(calc, ce, cfg, mo, set_cfg):
    # Compact 1-line action buttons
    snap_curve_btn = mo.ui.button(
        label="🧲 Snap a to Curve",
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
        label="🎯 Critical Pt (∇f=0)",
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
        label="🔄 Reset",
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
                "show_flow_line": False,
                "toast": "Reset coordinates and view",
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
    set_cfg,
    sw_3d_normal,
    sw_affine_plane,
    sw_all_contours,
    sw_constraint_curve,
    sw_constraint_surf,
    sw_error_rod,
    sw_flow_line,
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
        show_flow_line=bool(sw_flow_line.value),
    )

    # Synchronized 2D & 3D Click Handler: clicking ANY point on 2D or 3D updates Point a in both views!
    def _on_plot_click(points):
        if not points or not isinstance(points, list):
            return
        pt = points[-1]
        if not isinstance(pt, dict):
            return
        raw_x = pt.get("x")
        raw_y = pt.get("y")
        raw_z = pt.get("z")
        if raw_x is None or raw_y is None:
            return
        try:
            cx = round(float(raw_x), 3)
            cy = round(float(raw_y), 3)
        except Exception:
            return

        # Compute exact value f(cx, cy) so toast shows the exact value immediately
        exact_val = calc["fa"]
        if calc["mode"] == "scalar_2d":
            try:
                exact_val = float(calc["f_fn_2d"](cx, cy))
            except Exception:
                if raw_z is not None:
                    try:
                        exact_val = float(raw_z)
                    except Exception:
                        pass
        elif raw_z is not None:
            try:
                exact_val = float(raw_z)
            except Exception:
                pass

        set_cfg(
            lambda prev: {
                **prev,
                "a1": cx,
                "a2": cy,
                "a3": round(float(raw_z), 3) if (raw_z is not None and calc["dim"] == 3) else prev["a3"],
                "toast": f"📍 Point a = ({cx:.2f}, {cy:.2f})  ⟹  Exact f(a) = {exact_val:.4f}",
            }
        )

    plotly_widget = mo.ui.plotly(fig, on_change=_on_plot_click)

    # Shadow-DOM Bridge so 3D Surface & 3D Scatter clicks also trigger mo.ui.plotly's onClick handler
    click_bridge_js = (
        "if(!window.__mvg3dBridge){window.__mvg3dBridge=setInterval(function(){"
        "document.querySelectorAll('marimo-plotly').forEach(function(mp){"
        "var r=mp.shadowRoot||mp;"
        "r.querySelectorAll('.js-plotly-plot').forEach(function(p){"
        "if(!p.__mvgHook&&typeof p.emit==='function'){"
        "p.__mvgHook=true;var orig=p.emit.bind(p);"
        "p.emit=function(ev,d){"
        "if(ev==='plotly_click'&&d&&Array.isArray(d.points)){"
        "d.points.forEach(function(pt){if(pt){"
        "pt.data=Object.assign({},pt.data||{},{type:'heatmap'});"
        "if(pt.fullData)pt.fullData=Object.assign({},pt.fullData,{type:'heatmap'});"
        "}});}"
        "return orig(ev,d);};}});});},350);}"
    )
    click_bridge_html = mo.Html(
        f'<img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" '
        f'onload="{click_bridge_js}" style="display:none;" />'
    )

    return click_bridge_html, fig, plotly_widget


@app.cell
def _(
    api_key_input,
    apply_action_dict,
    calc,
    ce,
    cfg,
    get_chat_log,
    mo,
    set_chat_log,
):
    # Ergonomic Top-Mounted AI Tutor (Input Box is at the VERY TOP — Zero Scrolling Required!)
    def _run_tutor_query(user_prompt):
        if not user_prompt or not str(user_prompt).strip():
            return
        q_clean = str(user_prompt).strip()
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
                {"role": "assistant", "content": f"*({model_label})*\n\n{reply_md}"},
            ]
        )

    # Top-mounted prompt form: press Enter or click "🚀 Ask AI / Plot" right at the top!
    ai_prompt_form = mo.ui.text(
        value="",
        placeholder="Ask AI or command a graph (e.g. 'flow line of gamma(t)', 'make an ellipse', 'parabolic cylinder')...",
        label="💬 Ask AI Calculus Tutor (Press Enter or Click Button)",
        full_width=True,
    ).form(
        submit_button_label="🚀 Ask AI / Plot",
        clear_on_submit=True,
        bordered=False,
        on_change=_run_tutor_query,
    )

    ai_btn_flow = mo.ui.button(
        label="🌊 Flow Line γ(t)",
        on_click=lambda _: _run_tutor_query("Create a flow line of gamma(t)"),
    )
    ai_btn_parab_cyl = mo.ui.button(
        label="🏛️ Parabolic Cylinder",
        on_click=lambda _: _run_tutor_query("Create a parabolic cylinder with x1^2/4 + x2 = 1"),
    )
    ai_btn_ellipse = mo.ui.button(
        label="🪐 Make an Ellipse",
        on_click=lambda _: _run_tutor_query("Make me an ellipse"),
    )
    ai_btn_matrix3d = mo.ui.button(
        label="🧊 3×3 Matrix in ℝ³",
        on_click=lambda _: _run_tutor_query("Show a 3x3 matrix in R3: [1, 2, 3; 4, 5, 6; 7, 8, 9]"),
    )
    ai_btn_hessian = mo.ui.button(
        label="🔍 Explain Hessian",
        on_click=lambda _: _run_tutor_query("Explain the Hessian matrix and 2nd derivative test"),
    )

    return (
        ai_btn_ellipse,
        ai_btn_flow,
        ai_btn_hessian,
        ai_btn_matrix3d,
        ai_btn_parab_cyl,
        ai_prompt_form,
        get_chat_log,
    )


@app.cell
def _(
    a1_slider,
    a2_slider,
    a3_slider,
    ai_btn_ellipse,
    ai_btn_flow,
    ai_btn_hessian,
    ai_btn_matrix3d,
    ai_btn_parab_cyl,
    ai_prompt_form,
    anim_mode_dropdown,
    api_key_input,
    calc,
    cfg,
    chip_circle_req,
    chip_clear_req,
    chip_ellip_cyl,
    chip_flow_line,
    chip_parab_cyl,
    click_bridge_html,
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
    sw_flow_line,
    sw_gradient,
    sw_normal_line,
    sw_right_angle,
    sw_tangent_line,
    test_x_slider,
    test_y_slider,
    theme_switch,
    view_mode_radio,
):
    # =========================================================================
    # CLEAN 2-COLUMN STUDIO LAYOUT (PURE MARKDOWN MATH SO KATEX RENDERS 100%)
    # =========================================================================

    a_coords_str = (
        f"({cfg['a1']:.2f}, {cfg['a2']:.2f}, {cfg['a3']:.2f})"
        if calc["dim"] == 3
        else f"({cfg['a1']:.2f}, {cfg['a2']:.2f})"
    )

    status_parts = [f"**{calc['extremum_label']}**"]
    if calc["constraint"]["active"]:
        status_parts.append(f"🏛️ `{calc['constraint']['status_text']}`")
    if cfg.get("toast"):
        status_parts.append(f"✨ `{cfg['toast']}`")
    status_line_md = " &nbsp;•&nbsp; ".join(status_parts)

    # Top Studio Header Bar (Pure Markdown inside mo.md so KaTeX renders f_latex!)
    top_header = mo.callout(
        mo.hstack(
            [
                mo.md(
                    f"### 🌌 MultivarGrapher 3D\n"
                    f"{status_line_md}"
                ),
                mo.md(
                    f"$${calc['f_latex']}$$\n"
                    f"**Selected Point:** $\\mathbf{{a}} = {a_coords_str} \\;\\Longrightarrow\\; f(\\mathbf{{a}}) = {calc['fa']:.4f}$"
                ),
            ],
            justify="space-between",
            align="center",
            wrap=True,
        ),
        kind="neutral",
    )

    # -------------------------------------------------------------------------
    # LEFT PANEL: Expression Card + Point Sliders + 4 Clean Tabs
    # -------------------------------------------------------------------------
    expr_card = mo.vstack(
        [
            preset_selector,
            function_input,
            constraint_input,
            mo.hstack(
                [chip_flow_line, chip_parab_cyl, chip_ellip_cyl, chip_circle_req, chip_clear_req],
                wrap=True,
                gap=0.35,
            ),
        ],
        gap=0.45,
    )

    point_card = mo.vstack(
        [
            mo.hstack([a1_slider, a2_slider], widths="equal"),
            mo.hstack([level_c_slider, a3_slider], widths="equal"),
            mo.hstack([snap_curve_btn, snap_critical_btn, reset_domain_btn], justify="start", gap=0.4),
        ],
        gap=0.4,
    )

    # TAB 1: Unified Calculus Sheet — Pure Markdown (NO <div> tags around LaTeX!)
    calculus_sheet_tab = mo.vstack(
        [
            mo.callout(
                mo.md(
                    f"#### 1. Derivative Row Matrix $\\mathbf{{D}}f(\\mathbf{{a}})$ & Gradient $\\nabla f(\\mathbf{{a}})$\n\n"
                    f"$${calc['df_symbolic_latex']} \\;\\Longrightarrow\\; {calc['df_numeric_latex']}$$\n\n"
                    f"- **Gradient Column Vector:** $${calc['grad_latex']}$$\n"
                    f"- **Magnitude & $90^\\circ$ Frame:** $\\|\\nabla f(\\mathbf{{a}})\\| = {calc['grad_mag']:.3f}$ &nbsp;|&nbsp; "
                    f"Unit Normal $\\mathbf{{n}} = \\langle {calc['unit_normal_2d'][0]:.2f}, {calc['unit_normal_2d'][1]:.2f} \\rangle \\perp$ "
                    f"Unit Tangent $\\mathbf{{T}} = \\langle {calc['unit_tangent_2d'][0]:.2f}, {calc['unit_tangent_2d'][1]:.2f} \\rangle$ ($90^\\circ$)"
                ),
                kind="info",
            ),
            mo.callout(
                mo.md(
                    f"#### 2. Affine Tangent Plane $g(\\mathbf{{x}})$ & 3D Surface Normal\n\n"
                    f"$${calc['affine_symbolic_latex']}$$\n\n"
                    f"$${calc['affine_numeric_latex']}$$\n\n"
                    f"- **3D Surface Normal Vector:** $\\mathbf{{n}}_{{3D}} = \\langle {-calc['fx1']:.3f}, {-calc['fx2']:.3f}, 1.000 \\rangle$"
                ),
                kind="success",
            ),
            mo.callout(
                mo.md(
                    f"#### 3. Hessian Matrix $\\mathbf{{H}}_f(\\mathbf{{a}})$ & Second Derivative Test\n\n"
                    f"$${calc['hessian_symbolic_latex']}$$\n\n"
                    f"$${calc['hessian_numeric_latex']}$$\n\n"
                    f"- **Invariants:** $\\det(\\mathbf{{H}}) = {calc['hessian_det']:.3f}$ &nbsp;|&nbsp; "
                    f"$\\operatorname{{tr}}(\\mathbf{{H}}) = {calc['hessian_trace']:.3f}$ &nbsp;|&nbsp; "
                    f"Eigenvalues: `{calc['eigenvalues_str']}`\n"
                    f"- **Classification Verdict:** **{calc['extremum_label']}**"
                ),
                kind="warn" if calc["extremum_type"] == "saddle" else "neutral",
            ),
            mo.accordion(
                {
                    "🔬 Linearization Error Calculator at x_test & Radius Helper": mo.vstack(
                        [
                            mo.hstack([test_x_slider, test_y_slider], widths="equal"),
                            sw_error_rod,
                            mo.md(
                                f"- **Exact Value:** $f(\\mathbf{{x}}_{{\\text{{test}}}}) = {calc['test_exact']:.4f}$\n"
                                f"- **Affine Approx:** $g(\\mathbf{{x}}_{{\\text{{test}}}}) = {calc['test_affine']:.4f}$\n"
                                f"- **First-Order Error:** $|f(\\mathbf{{x}}_{{\\text{{test}}}}) - g(\\mathbf{{x}}_{{\\text{{test}}}})| = {calc['test_error']:.4f}$"
                            ),
                            radius_r_input,
                        ]
                    ),
                    "🎚️ Formula Parameters (a, b, c, d)": mo.hstack(
                        [param_a, param_b, param_c, param_d], widths="equal"
                    ),
                }
            ),
        ],
        gap=0.45,
    )

    # TAB 2: AI Calculus Tutor — Input Form is AT THE TOP, Newest Reply First!
    recent_msgs = list(reversed(get_chat_log()[-6:]))
    log_md_blocks = "\n\n---\n\n".join(
        f"**{'🧑‍🎓 You' if m['role']=='user' else '🤖 AI Calculus Tutor'}:**\n\n{m['content']}"
        for m in recent_msgs
    )

    ai_tutor_tab = mo.vstack(
        [
            ai_prompt_form,
            mo.hstack(
                [ai_btn_flow, ai_btn_parab_cyl, ai_btn_ellipse, ai_btn_matrix3d, ai_btn_hessian],
                wrap=True,
                gap=0.35,
            ),
            mo.callout(mo.md(log_md_blocks), kind="neutral"),
            mo.accordion({"🔑 Gemini API Key Settings (Optional)": api_key_input}),
        ],
        gap=0.5,
    )

    # TAB 3: Complete Multivariable Calculus Theory Guide (Pure Markdown + KaTeX!)
    theory_tab = mo.vstack(
        [
            mo.callout(
                mo.md(
                    r"""
                    #### 1. Level Sets $f^{-1}(c)$ & Orthogonality ($90^\circ$)
                    For a scalar function $f: \mathbb{R}^2 \to \mathbb{R}$, the **level curve** at height $c$ is the set:
                    $$f^{-1}(c) = \{ (x_1, x_2) \in \mathbb{R}^2 \mid f(x_1, x_2) = c \}$$
                    - **Gradient Orthogonality Theorem:** At any non-critical point $\mathbf{a}$, the gradient $\nabla f(\mathbf{a})$ is **strictly perpendicular ($90^\circ$)** to the tangent line of the level curve passing through $\mathbf{a}$.
                    - **Flow Line $\gamma(t)$:** The trajectory solving $\gamma'(t) = \nabla f(\gamma(t))$ with $\gamma(0) = \mathbf{a}$ follows the path of **steepest ascent** and crosses every level curve at a $90^\circ$ angle.
                    """
                ),
                kind="info",
            ),
            mo.callout(
                mo.md(
                    r"""
                    #### 2. Total Derivative $\mathbf{D}f(\mathbf{a})$ & Affine Function $g(\mathbf{x})$
                    The **total derivative** at $\mathbf{a} = (a_1, a_2)$ is the $1 \times 2$ row matrix of partial derivatives:
                    $$\mathbf{D}f(\mathbf{a}) = \begin{bmatrix} \frac{\partial f}{\partial x_1}(\mathbf{a}) & \frac{\partial f}{\partial x_2}(\mathbf{a}) \end{bmatrix}_{1 \times 2}, \qquad \nabla f(\mathbf{a}) = \mathbf{D}f(\mathbf{a})^T$$
                    The **affine approximation** $g(\mathbf{x})$ defines the 3D **tangent plane** touching $z = f(\mathbf{x})$ at $\mathbf{a}$:
                    $$g(\mathbf{x}) = f(\mathbf{a}) + \mathbf{D}f(\mathbf{a})(\mathbf{x} - \mathbf{a}) = f(a_1, a_2) + f_{x_1}(\mathbf{a})(x_1 - a_1) + f_{x_2}(\mathbf{a})(x_2 - a_2)$$
                    """
                ),
                kind="success",
            ),
            mo.callout(
                mo.md(
                    r"""
                    #### 3. Hessian Matrix $\mathbf{H}_f(\mathbf{a})$ & Second Derivative Test
                    The **Hessian matrix** captures the second-order quadratic curvature of $f$ at $\mathbf{a}$:
                    $$\mathbf{H}_f(\mathbf{a}) = \begin{bmatrix} f_{11}(\mathbf{a}) & f_{12}(\mathbf{a}) \\ f_{21}(\mathbf{a}) & f_{22}(\mathbf{a}) \end{bmatrix}, \qquad D = \det(\mathbf{H}_f(\mathbf{a})) = f_{11}f_{22} - f_{12}^2$$
                    At a critical point ($\nabla f(\mathbf{a}) = \mathbf{0}$):
                    - $D > 0$ and $f_{11} > 0 \implies$ **Strict Local Minimum** (both eigenvalues $\lambda_1, \lambda_2 > 0$).
                    - $D > 0$ and $f_{11} < 0 \implies$ **Strict Local Maximum** (both eigenvalues $\lambda_1, \lambda_2 < 0$).
                    - $D < 0 \implies$ **Saddle Point** (eigenvalues have opposite signs).
                    """
                ),
                kind="warn",
            ),
            mo.callout(
                mo.md(
                    r"""
                    #### 4. Free-Variable 3D Cylinders & Linear Matrices in $\mathbb{R}^2 / \mathbb{R}^3$
                    - **3D Cylinders:** When $\mathbf{F}(x_1, x_2, x_3) = [x_1; x_2; x_3]$ is paired with a constraint like $\frac{x_1^2}{4} + x_2 = 1$, the variable $x_3$ is **free** ($x_3 \in (-\infty, \infty)$), extruding the 2D curve vertically into a **3D cylinder** parallel to the $x_3$-axis.
                    - **Matrices:** Entering `[a, b; c, d]` or a $3 \times 3$ matrix `[1, 2, 3; 4, 5, 6; 7, 8, 9]` visualizes the column basis vectors $\mathbf{A}\mathbf{e}_i$ and transformed vector $\mathbf{A}\mathbf{a}$.
                    """
                ),
                kind="neutral",
            ),
        ],
        gap=0.45,
    )

    # TAB 4: Layers & Visual Style
    layers_tab = mo.vstack(
        [
            mo.hstack([colorscale_dropdown, opacity_slider, notation_switch], widths="equal"),
            mo.hstack(
                [
                    mo.vstack([sw_flow_line, sw_gradient, sw_tangent_line, sw_normal_line, sw_right_angle]),
                    mo.vstack([sw_affine_plane, sw_3d_normal, sw_constraint_surf, sw_constraint_curve, sw_all_contours]),
                ],
                widths="equal",
            ),
        ],
        gap=0.6,
    )

    left_tabs = mo.ui.tabs(
        {
            "📐 Calculus Sheet": calculus_sheet_tab,
            "🤖 AI Tutor": ai_tutor_tab,
            "📖 Theory": theory_tab,
            "⚙️ Layers & Style": layers_tab,
        }
    )

    left_panel = mo.vstack(
        [
            expr_card,
            point_card,
            left_tabs,
        ],
        gap=0.6,
    )

    # -------------------------------------------------------------------------
    # RIGHT PANEL: Toolbar + Interactive 2D/3D Graph (Click to set Point a!) + KPIs
    # -------------------------------------------------------------------------
    kpi_row = mo.hstack(
        [
            mo.stat(value=f"{calc['fa']:.3f}", label="Exact Value f(a)", caption=f"At a = {a_coords_str}"),
            mo.stat(value=f"[{calc['fx1']:.2f}, {calc['fx2']:.2f}]", label="Derivative Df(a)", caption=f"‖∇f‖ = {calc['grad_mag']:.2f}"),
            mo.stat(value=f"c = {cfg['c']:.2f}", label="Level Set f = c", caption=f"|f(a)-c| = {calc['level_diff']:.2f}"),
            mo.stat(value=f"D = {calc['hessian_det']:.2f}", label="Hessian Det(H)", caption=f"λ: {calc['eigenvalues_str']}"),
        ],
        widths="equal",
        gap=0.6,
    )

    right_panel = mo.vstack(
        [
            mo.hstack(
                [
                    view_mode_radio,
                    anim_mode_dropdown,
                    theme_switch,
                ],
                justify="space-between",
                wrap=True,
            ),
            mo.md("💡 *Tip: Click anywhere on the **2D Map** or **3D Surface** to move Point $\\mathbf{a}$ synchronously in both views!*"),
            plotly_widget,
            kpi_row,
            click_bridge_html,
        ],
        gap=0.45,
    )

    studio_layout = mo.vstack(
        [
            top_header,
            mo.hstack([left_panel, right_panel], widths=[0.39, 0.61], gap=1.1, align="start"),
        ],
        gap=0.65,
    )

    studio_layout
    return (
        a_coords_str,
        ai_tutor_tab,
        calculus_sheet_tab,
        expr_card,
        kpi_row,
        layers_tab,
        left_panel,
        left_tabs,
        log_md_blocks,
        point_card,
        recent_msgs,
        right_panel,
        status_line_md,
        status_parts,
        studio_layout,
        theory_tab,
        top_header,
    )


if __name__ == "__main__":
    app.run()
