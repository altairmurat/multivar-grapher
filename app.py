import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full")


@app.cell
def _():
    import base64
    import json
    import math
    import os
    import re
    import warnings
    warnings.filterwarnings("ignore", category=SyntaxWarning)
    import anywidget
    from google import genai
    from google.genai import types
    import marimo as mo
    import numpy as np
    import traitlets

    return anywidget, base64, genai, json, math, mo, np, os, re, traitlets, types


@app.cell
def _(anywidget, base64, genai, json, math, mo, np, os, re, traitlets, types):
    # =========================================================================
    # 1. ЧТЕНИЕ API КЛЮЧА GEMINI (ИЗ ОКРУЖЕНИЯ ИЛИ .gemini_key)
    # =========================================================================
    env_key = os.environ.get("GEMINI_API_KEY", "").strip()
    key_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".gemini_key")
    if not env_key and os.path.exists(key_file):
        try:
            with open(key_file, "r", encoding="utf-8") as _f:
                env_key = _f.read().strip()
        except Exception:
            pass

    # =========================================================================
    # 2. ПРЕСЕТЫ ПО ВСЕМ 5 ТЕМАМ:
    #    1) Path (Параметрический путь γ(t) и длина дуги)
    #    2) Flow Line (Линия тока γ'(t) = F(γ(t)) и фазовый поток)
    #    3) Path Integral (Криволинейный интеграл I рода ∫_γ f ds)
    #    4) Line Integral (Криволинейный интеграл II рода ∫_γ F · dγ)
    #    5) Work (Работа силового поля W = ∫_γ F · dr)
    # =========================================================================
    PRESET_STATES = {
        "preset_flow_saddle": {
            "preset_id": "preset_flow_saddle",
            "topic_mode": "flow_line",
            "title": "Flow Line: F(γ(t)) = [x₀·e^(2t); y₀·e^(-t); t] — Седловая линия тока в 3D и 2D",
            "full_formula": "[x0*e^2t; y0*e^(-t); t]",
            "x_expr": "x0 * e^(2*t)",
            "y_expr": "y0 * e^(-t)",
            "z_expr": "t",
            "f_expr": "x^2 + y^2",
            "u_expr": "2*x",
            "v_expr": "-y",
            "w_expr": "1",
            "auto_field": True,
            "use_rk4": False,
            "x0": 0.45,
            "y0": 1.35,
            "t_val": 0.55,
            "t_min": -1.2,
            "t_max": 1.2,
            "riemann_n": 18,
            "build_stage": 4,
            "progressive_draw": True,
            "show_2d_field": True,
            "show_3d_field": True,
            "show_curtain": True,
            "show_bundle": True,
            "show_velocity": True,
            "show_floor_curve": True,
            "show_surface": False,
            "show_path_vectors": True,
            "show_integrand_chart": True,
            "split_2d": True,
            "anim_mode": "none",
            "anim_speed": 1.0,
            "problem_solution": None,
            "status": "🌊 Flow Line: γ'(t) = F(γ(t)), где γ(t) = [x₀·e^(2t); y₀·e^(-t)] и F = [2x, -y, 1]",
        },
        "preset_flow_spiral": {
            "preset_id": "preset_flow_spiral",
            "topic_mode": "flow_line",
            "title": "Flow Line: Спиральная линия тока γ'(t) = [-0.35x - 2y, 2x - 0.35y, 1]",
            "full_formula": "[e^(-0.35*t)*(x0*cos(2*t) - y0*sin(2*t)); e^(-0.35*t)*(x0*sin(2*t) + y0*cos(2*t)); t]",
            "x_expr": "e^(-0.35*t)*(x0*cos(2*t) - y0*sin(2*t))",
            "y_expr": "e^(-0.35*t)*(x0*sin(2*t) + y0*cos(2*t))",
            "z_expr": "t",
            "f_expr": "x^2 + y^2",
            "u_expr": "-0.35*x - 2*y",
            "v_expr": "2*x - 0.35*y",
            "w_expr": "1",
            "auto_field": False,
            "use_rk4": False,
            "x0": 1.60,
            "y0": 1.10,
            "t_val": 1.60,
            "t_min": -0.6,
            "t_max": 3.2,
            "riemann_n": 20,
            "build_stage": 4,
            "progressive_draw": True,
            "show_2d_field": True,
            "show_3d_field": True,
            "show_curtain": True,
            "show_bundle": True,
            "show_velocity": True,
            "show_floor_curve": True,
            "show_surface": False,
            "show_path_vectors": True,
            "show_integrand_chart": True,
            "split_2d": True,
            "anim_mode": "none",
            "anim_speed": 1.0,
            "problem_solution": None,
            "status": "🌀 Спиральная линия тока: в каждой точке вектор скорости γ'(t) совпадает с полем F(γ(t))",
        },
        "preset_path_helix": {
            "preset_id": "preset_path_helix",
            "topic_mode": "path",
            "title": "Path γ(t): Винтовая траектория γ(t) = [1.5·cos(t); 1.5·sin(t); 0.45·t] и длина дуги s(t)",
            "full_formula": "[1.5*cos(t); 1.5*sin(t); 0.45*t]",
            "x_expr": "1.5 * cos(t)",
            "y_expr": "1.5 * sin(t)",
            "z_expr": "0.45 * t",
            "f_expr": "1",
            "u_expr": "-y",
            "v_expr": "x",
            "w_expr": "0.45",
            "auto_field": False,
            "use_rk4": False,
            "x0": 1.50,
            "y0": 0.00,
            "t_val": 3.80,
            "t_min": 0.0,
            "t_max": 6.2832,
            "riemann_n": 20,
            "build_stage": 4,
            "progressive_draw": True,
            "show_2d_field": False,
            "show_3d_field": False,
            "show_curtain": True,
            "show_bundle": False,
            "show_velocity": True,
            "show_floor_curve": True,
            "show_surface": False,
            "show_path_vectors": True,
            "show_integrand_chart": True,
            "split_2d": True,
            "anim_mode": "none",
            "anim_speed": 1.0,
            "problem_solution": None,
            "status": "🛤️ Path γ(t): исследование пути, касательного вектора скорости γ'(t) и длины дуги L = ∫ ‖γ'(t)‖ dt",
        },
        "preset_path_twisted": {
            "preset_id": "preset_path_twisted",
            "topic_mode": "path",
            "title": "Path γ(t): Кубическо-параболический 3D путь γ(t) = [t; 0.7·t² - 1; 0.35·t³]",
            "full_formula": "[t; 0.7*t^2 - 1; 0.35*t^3]",
            "x_expr": "t",
            "y_expr": "0.7 * t^2 - 1",
            "z_expr": "0.35 * t^3",
            "f_expr": "1 + x^2",
            "u_expr": "1",
            "v_expr": "1.4*x",
            "w_expr": "1.05*x^2",
            "auto_field": False,
            "use_rk4": False,
            "x0": 0.0,
            "y0": -1.0,
            "t_val": 1.10,
            "t_min": -1.8,
            "t_max": 1.8,
            "riemann_n": 18,
            "build_stage": 4,
            "progressive_draw": True,
            "show_2d_field": False,
            "show_3d_field": False,
            "show_curtain": True,
            "show_bundle": False,
            "show_velocity": True,
            "show_floor_curve": True,
            "show_surface": False,
            "show_path_vectors": True,
            "show_integrand_chart": True,
            "split_2d": True,
            "anim_mode": "none",
            "anim_speed": 1.0,
            "problem_solution": None,
            "status": "🛤️ 3D путь γ(t) = [t, 0.7t²-1, 0.35t³]: тень на плоскости z=0 и подъём в 3D",
        },
        "preset_path_int_circle": {
            "preset_id": "preset_path_int_circle",
            "topic_mode": "path_integral",
            "title": "Path Integral ∫_γ f ds: Забор Римана f(x,y) = 1.2 + 0.4·x² + 0.6·y вдоль дуги окружности",
            "full_formula": "[1.6*cos(t); 1.6*sin(t); 1.2 + 0.4*x^2 + 0.6*y]",
            "x_expr": "1.6 * cos(t)",
            "y_expr": "1.6 * sin(t)",
            "z_expr": "1.2 + 0.4*x^2 + 0.6*y",
            "f_expr": "1.2 + 0.4*x^2 + 0.6*y",
            "u_expr": "-y",
            "v_expr": "x",
            "w_expr": "0",
            "auto_field": False,
            "use_rk4": False,
            "x0": 1.6,
            "y0": 0.0,
            "t_val": 2.40,
            "t_min": 0.0,
            "t_max": 3.1416,
            "riemann_n": 18,
            "build_stage": 4,
            "progressive_draw": True,
            "show_2d_field": False,
            "show_3d_field": False,
            "show_curtain": True,
            "show_bundle": False,
            "show_velocity": True,
            "show_floor_curve": True,
            "show_surface": True,
            "show_path_vectors": True,
            "show_integrand_chart": True,
            "split_2d": True,
            "anim_mode": "none",
            "anim_speed": 1.0,
            "problem_solution": None,
            "status": "🧱 Path Integral ∫_γ f(x,y) ds = ∫ f(γ(t))·‖γ'(t)‖ dt — площадь криволинейного забора под z = f(x,y)",
        },
        "preset_path_int_parabola": {
            "preset_id": "preset_path_int_parabola",
            "topic_mode": "path_integral",
            "title": "Path Integral ∫_γ f ds: Интеграл от f(x,y) = 0.8 + 0.5·x² + 0.4·y² вдоль параболы y = 0.5·x² - 1",
            "full_formula": "[t; 0.5*t^2 - 1; 0.8 + 0.5*x^2 + 0.4*y^2]",
            "x_expr": "t",
            "y_expr": "0.5 * t^2 - 1",
            "z_expr": "0.8 + 0.5*x^2 + 0.4*y^2",
            "f_expr": "0.8 + 0.5*x^2 + 0.4*y^2",
            "u_expr": "1",
            "v_expr": "x",
            "w_expr": "0",
            "auto_field": False,
            "use_rk4": False,
            "x0": -1.6,
            "y0": 0.28,
            "t_val": 0.85,
            "t_min": -1.6,
            "t_max": 1.6,
            "riemann_n": 16,
            "build_stage": 4,
            "progressive_draw": True,
            "show_2d_field": False,
            "show_3d_field": False,
            "show_curtain": True,
            "show_bundle": False,
            "show_velocity": True,
            "show_floor_curve": True,
            "show_surface": True,
            "show_path_vectors": True,
            "show_integrand_chart": True,
            "split_2d": True,
            "anim_mode": "none",
            "anim_speed": 1.0,
            "problem_solution": None,
            "status": "🧱 Path Integral: столбики Римана f(γ(t_k))·Δs_k вдоль параболического пути γ(t) = [t, 0.5t²-1]",
        },
        "preset_line_int_vortex": {
            "preset_id": "preset_line_int_vortex",
            "topic_mode": "line_integral",
            "title": "Line Integral ∫_γ F·dγ: Интеграл вихревого поля F = [-y, x, 0] вдоль окружности r = 1.5",
            "full_formula": "[1.5*cos(t); 1.5*sin(t); 0]",
            "x_expr": "1.5 * cos(t)",
            "y_expr": "1.5 * sin(t)",
            "z_expr": "0",
            "f_expr": "x^2 + y^2",
            "u_expr": "-y",
            "v_expr": "x",
            "w_expr": "0",
            "auto_field": False,
            "use_rk4": False,
            "x0": 1.5,
            "y0": 0.0,
            "t_val": 4.20,
            "t_min": 0.0,
            "t_max": 6.2832,
            "riemann_n": 16,
            "build_stage": 4,
            "progressive_draw": True,
            "show_2d_field": True,
            "show_3d_field": False,
            "show_curtain": True,
            "show_bundle": False,
            "show_velocity": True,
            "show_floor_curve": True,
            "show_surface": False,
            "show_path_vectors": True,
            "show_integrand_chart": True,
            "split_2d": True,
            "anim_mode": "none",
            "anim_speed": 1.0,
            "problem_solution": None,
            "status": "🧭 Line Integral ∫_γ F·dγ = ∫ (P dx + Q dy): поле F = [-y, x] сонаправлено с γ'(t), вклад везде > 0",
        },
        "preset_line_int_3d": {
            "preset_id": "preset_line_int_3d",
            "topic_mode": "line_integral",
            "title": "Line Integral 3D ∫_γ F·dγ: Поле F = [y, z, x] вдоль винтовой линии γ(t) = [cos t, sin t, 0.5t]",
            "full_formula": "[1.4*cos(t); 1.4*sin(t); 0.4*t]",
            "x_expr": "1.4 * cos(t)",
            "y_expr": "1.4 * sin(t)",
            "z_expr": "0.4 * t",
            "f_expr": "x + y + z",
            "u_expr": "y",
            "v_expr": "z",
            "w_expr": "x",
            "auto_field": False,
            "use_rk4": False,
            "x0": 1.4,
            "y0": 0.0,
            "t_val": 3.60,
            "t_min": 0.0,
            "t_max": 6.2832,
            "riemann_n": 18,
            "build_stage": 4,
            "progressive_draw": True,
            "show_2d_field": True,
            "show_3d_field": True,
            "show_curtain": True,
            "show_bundle": False,
            "show_velocity": True,
            "show_floor_curve": True,
            "show_surface": False,
            "show_path_vectors": True,
            "show_integrand_chart": True,
            "split_2d": True,
            "anim_mode": "none",
            "anim_speed": 1.0,
            "problem_solution": None,
            "status": "🧭 3D Line Integral ∫_γ (P dx + Q dy + R dz): зелёные участки F·γ' > 0, красные F·γ' < 0",
        },
        "preset_work_parabola": {
            "preset_id": "preset_work_parabola",
            "topic_mode": "work",
            "title": "Work W = ∫_γ F·dr: Работа силы F = [y + 0.5x, x², 0.4] вдоль пути γ(t) = [t, 0.6t² - 0.8, 0.4t]",
            "full_formula": "[t; 0.6*t^2 - 0.8; 0.4*t]",
            "x_expr": "t",
            "y_expr": "0.6 * t^2 - 0.8",
            "z_expr": "0.4 * t",
            "f_expr": "x*y",
            "u_expr": "y + 0.5*x",
            "v_expr": "x^2",
            "w_expr": "0.4",
            "auto_field": False,
            "use_rk4": False,
            "x0": -1.2,
            "y0": 0.06,
            "t_val": 0.90,
            "t_min": -1.2,
            "t_max": 1.6,
            "riemann_n": 16,
            "build_stage": 4,
            "progressive_draw": True,
            "show_2d_field": True,
            "show_3d_field": True,
            "show_curtain": True,
            "show_bundle": False,
            "show_velocity": True,
            "show_floor_curve": True,
            "show_surface": False,
            "show_path_vectors": True,
            "show_integrand_chart": True,
            "split_2d": True,
            "anim_mode": "none",
            "anim_speed": 1.0,
            "problem_solution": None,
            "status": "⚡ Work W = ∫_γ F·dr: разложение силы F на полезную касательную F_∥ (совершает работу) и нормальную F_⊥",
        },
        "preset_work_mixed": {
            "preset_id": "preset_work_mixed",
            "topic_mode": "work",
            "title": "Work W = ∫_γ F·dr: Знакопеременная работа седлового поля F = [x, -y, 0] вдоль полуокружности",
            "full_formula": "[1.6*cos(t); 1.6*sin(t); 0]",
            "x_expr": "1.6 * cos(t)",
            "y_expr": "1.6 * sin(t)",
            "z_expr": "0",
            "f_expr": "0.5*(x^2 - y^2)",
            "u_expr": "x",
            "v_expr": "-y",
            "w_expr": "0",
            "auto_field": False,
            "use_rk4": False,
            "x0": 1.6,
            "y0": 0.0,
            "t_val": 2.10,
            "t_min": 0.0,
            "t_max": 3.1416,
            "riemann_n": 18,
            "build_stage": 4,
            "progressive_draw": True,
            "show_2d_field": True,
            "show_3d_field": False,
            "show_curtain": True,
            "show_bundle": False,
            "show_velocity": True,
            "show_floor_curve": True,
            "show_surface": False,
            "show_path_vectors": True,
            "show_integrand_chart": True,
            "split_2d": True,
            "anim_mode": "none",
            "anim_speed": 1.0,
            "problem_solution": None,
            "status": "⚡ Знакопеременная работа: сначала сила тормозит частицу (dW < 0, красный), затем разгоняет (dW > 0)",
        },
    }

    # =========================================================================
    # 3. НОРМАЛИЗАТОР И ЛОКАЛЬНЫЙ ПАРСЕР КОМАНД ПО ВСЕМ 5 ТЕМАМ
    # =========================================================================
    def normalize_math_expr(expr: str) -> str:
        s = (expr or "").strip()
        uni = {
            "⁰": "^0", "¹": "^1", "²": "^2", "³": "^3", "⁴": "^4",
            "⁵": "^5", "⁶": "^6", "⁷": "^7", "⁸": "^8", "⁹": "^9",
            "⁻": "-", "⁺": "+", "₀": "0", "₁": "1", "₂": "2", "₃": "3",
            "−": "-", "–": "-", "—": "-", "×": "*", "·": "*", "∙": "*", "÷": "/", "π": "pi",
        }
        for k, v in uni.items():
            s = s.replace(k, v)
        s = re.sub(r"\bx_0\b", "x0", s, flags=re.IGNORECASE)
        s = re.sub(r"\by_0\b", "y0", s, flags=re.IGNORECASE)
        s = re.sub(r"\be\s*\^\s*\(([^)]+)\)", r"exp(\1)", s)
        s = re.sub(r"\be\s*\^\s*([+\-]?\d+(?:\.\d+)?\s*\*?\s*[tTxXyYzZ]\d*)", r"exp(\1)", s)
        s = re.sub(r"\be\s*\^\s*([+\-]?[a-zA-Z0-9_]+)", r"exp(\1)", s)
        return s.strip()

    def infer_velocity_expr(coord_expr: str, var_name: str) -> str:
        norm = normalize_math_expr(coord_expr).replace(" ", "")
        m = re.match(r"^(?:x0|y0)\*?exp\(([+\-]?\d*(?:\.\d+)?)\*?t\)$", norm, flags=re.IGNORECASE)
        if m:
            k_str = m.group(1)
            if k_str in ("", "+"):
                return var_name
            if k_str == "-":
                return f"-{var_name}"
            return f"{k_str}*{var_name}"
        if norm == "t":
            return "1"
        m_lin = re.match(r"^([+\-]?\d+(?:\.\d+)?)\*?t$", norm)
        if m_lin:
            return m_lin.group(1)
        return ""

    def parse_vector_command(raw_cmd: str, current_state: dict) -> tuple[dict, bool]:
        s = dict(current_state)
        raw = (raw_cmd or "").strip()
        if not raw:
            return s, False

        norm = normalize_math_expr(raw)
        low = norm.lower()
        handled = False
        parts = []

        # 1. Переключение темы по ключевым словам
        if any(w in low for w in ("path integral", "интеграл 1", "интеграл первого", "скалярный интеграл", "забор римана", "f ds")):
            s["topic_mode"] = "path_integral"
            s["show_curtain"] = True
            s["show_surface"] = True
            parts.append("тема: Path Integral (∫_γ f ds)")
            handled = True
        elif any(w in low for w in ("line integral", "интеграл 2", "интеграл второго", "векторный интеграл", "циркуляц")):
            s["topic_mode"] = "line_integral"
            s["show_2d_field"] = True
            s["show_path_vectors"] = True
            parts.append("тема: Line Integral (∫_γ F·dγ)")
            handled = True
        elif any(w in low for w in ("work", "работ", "сил")):
            s["topic_mode"] = "work"
            s["show_2d_field"] = True
            s["show_path_vectors"] = True
            parts.append("тема: Work (W = ∫_γ F·dr)")
            handled = True
        elif any(w in low for w in ("flow line", "линия тока", "линии тока", "поток", "фазов")):
            s["topic_mode"] = "flow_line"
            s["show_2d_field"] = True
            s["show_bundle"] = True
            parts.append("тема: Flow Line (γ'(t) = F(γ(t)))")
            handled = True
        elif any(w in low for w in ("длина дуги", "arc length", "просто путь", "траектори")):
            s["topic_mode"] = "path"
            parts.append("тема: Path γ(t)")
            handled = True

        # 2. Сброс к исходному примеру
        if any(w in low for w in ("сброс", "сначала", "reset", "седлов")):
            fresh = dict(PRESET_STATES["preset_flow_saddle"])
            fresh["status"] = "⚡ Сброшено к F(γ(t)) = [x₀·e^(2t); y₀·e^(-t); t]"
            return fresh, True

        # 3. Ввод формулы кривой [x(t); y(t); z(t)]
        bracket_m = re.search(r"\[\s*([^\]]+)\s*\]", norm)
        if bracket_m:
            inner = bracket_m.group(1)
            sep = ";" if ";" in inner else ","
            comps = [c.strip() for c in inner.split(sep) if c.strip()]
            if len(comps) >= 2:
                # Проверяем, зависят ли компоненты от t или только от x,y (поле F)
                has_t = any(re.search(r"\bt\b", c) for c in comps)
                if has_t or "f(" in low or "gamma" in low or "γ" in low or ";" in inner:
                    s["x_expr"] = comps[0]
                    s["y_expr"] = comps[1]
                    s["z_expr"] = comps[2] if len(comps) >= 3 else "0"
                    s["full_formula"] = f"[{s['x_expr']}; {s['y_expr']}; {s['z_expr']}]"
                    u_inf = infer_velocity_expr(s["x_expr"], "x")
                    v_inf = infer_velocity_expr(s["y_expr"], "y")
                    w_inf = infer_velocity_expr(s["z_expr"], "z")
                    if u_inf and s.get("topic_mode") == "flow_line":
                        s["u_expr"] = u_inf
                    if v_inf and s.get("topic_mode") == "flow_line":
                        s["v_expr"] = v_inf
                    if w_inf and s.get("topic_mode") == "flow_line":
                        s["w_expr"] = w_inf
                    s["title"] = f"γ(t) = [{s['x_expr']}; {s['y_expr']}; {s['z_expr']}]"
                    parts.append(f"γ(t) = {s['full_formula']}")
                    handled = True
                else:
                    s["u_expr"] = comps[0]
                    s["v_expr"] = comps[1]
                    s["w_expr"] = comps[2] if len(comps) >= 3 else "0"
                    s["auto_field"] = False
                    parts.append(f"F = [{s['u_expr']}, {s['v_expr']}, {s['w_expr']}]")
                    handled = True
        elif ";" in norm and len(norm.split(";")) >= 2:
            cleaned = re.sub(r"^.*?=\s*", "", norm).strip()
            comps = [c.strip() for c in cleaned.split(";") if c.strip()]
            if len(comps) >= 2:
                s["x_expr"] = comps[0]
                s["y_expr"] = comps[1]
                s["z_expr"] = comps[2] if len(comps) >= 3 else "0"
                s["full_formula"] = f"[{s['x_expr']}; {s['y_expr']}; {s['z_expr']}]"
                s["title"] = f"γ(t) = [{s['x_expr']}; {s['y_expr']}; {s['z_expr']}]"
                parts.append(f"γ(t) = {s['full_formula']}")
                handled = True

        # 4. Параметры x0, y0, t
        x0_m = re.search(r"\bx0\s*=\s*(-?\d+(?:\.\d+)?)", low)
        if x0_m:
            s["x0"] = float(x0_m.group(1))
            parts.append(f"x₀ = {s['x0']:g}")
            handled = True

        y0_m = re.search(r"\by0\s*=\s*(-?\d+(?:\.\d+)?)", low)
        if y0_m:
            s["y0"] = float(y0_m.group(1))
            parts.append(f"y₀ = {s['y0']:g}")
            handled = True

        t_m = re.search(r"\bt\s*=\s*(-?\d+(?:\.\d+)?)", low)
        if t_m:
            s["t_val"] = float(t_m.group(1))
            parts.append(f"t = {s['t_val']:g}")
            handled = True

        # 5. Управление анимацией построения
        wants_stop = any(w in low for w in ("стоп", "останови", "пауза", "stop", "pause", "freeze"))
        wants_anim = any(w in low for w in ("анимир", "анимац", "построй вживую", "покажи построение", "двиг", "запусти", "animate", "play", "build"))
        if wants_stop:
            s["anim_mode"] = "none"
            parts.append("⏸️ анимация остановлена")
            handled = True
        elif wants_anim:
            if "x0" in low:
                s["anim_mode"] = "x0"
            elif "y0" in low:
                s["anim_mode"] = "y0"
            elif "круг" in low or "orbit" in low:
                s["anim_mode"] = "orbit"
            else:
                s["anim_mode"] = "build"
                s["progressive_draw"] = True
            parts.append(f"🎬 анимация построения ({s['anim_mode']})")
            handled = True

        if handled:
            s["status"] = "✅ Выполнено: " + (", ".join(parts) if parts else raw)

        return s, handled

    # =========================================================================
    # 4. GEMINI 2.5 FLASH AI (ТЕКСТОВЫЕ ЗАДАЧИ + РЕШЕНИЕ ПО СКРИНШОТУ VISION)
    # =========================================================================
    AI_PROBLEM_SCHEMA = {
        "type": "object",
        "properties": {
            "topic_mode": {
                "type": "string",
                "enum": ["path", "flow_line", "path_integral", "line_integral", "work"],
                "description": "Best matching topic mode for the problem",
            },
            "title": {"type": "string", "description": "Clear title of the problem and what is being visualized"},
            "x_expr": {"type": "string", "description": "x(t) parametric expression using t, x0, y0, e.g. '2*cos(t)' or 'x0*e^(2*t)'"},
            "y_expr": {"type": "string", "description": "y(t) parametric expression using t, x0, y0, e.g. '2*sin(t)' or 'y0*e^(-t)'"},
            "z_expr": {"type": "string", "description": "z(t) parametric expression using t, x0, y0, x, y, e.g. '0' or 't'"},
            "f_expr": {"type": "string", "description": "Scalar function f(x,y,z) for path_integral, e.g. 'x^2 + y'"},
            "u_expr": {"type": "string", "description": "Vector field X-component P(x,y,z), e.g. '-y' or '2*x'"},
            "v_expr": {"type": "string", "description": "Vector field Y-component Q(x,y,z), e.g. 'x' or '-y'"},
            "w_expr": {"type": "string", "description": "Vector field Z-component R(x,y,z), e.g. '0' or '1'"},
            "auto_field": {"type": "boolean"},
            "use_rk4": {"type": "boolean"},
            "x0": {"type": "number"},
            "y0": {"type": "number"},
            "t_min": {"type": "number"},
            "t_max": {"type": "number"},
            "t_val": {"type": "number"},
            "show_curtain": {"type": "boolean"},
            "show_bundle": {"type": "boolean"},
            "show_surface": {"type": "boolean"},
            "show_2d_field": {"type": "boolean"},
            "show_3d_field": {"type": "boolean"},
            "anim_mode": {"type": "string", "enum": ["none", "build", "t", "orbit"]},
            "problem_statement": {"type": "string", "description": "Extracted problem statement in Russian"},
            "step1_param": {"type": "string", "description": "Step 1: Parameterization of path gamma(t) and bounds [t_min, t_max]"},
            "step2_deriv": {"type": "string", "description": "Step 2: Velocity vector gamma'(t), speed ||gamma'(t)|| or field F(gamma(t))"},
            "step3_integrand": {"type": "string", "description": "Step 3: Simplified integrand f(gamma(t))||gamma'(t)|| or F(gamma(t))*gamma'(t)"},
            "step4_answer": {"type": "string", "description": "Step 4: Analytical evaluation and final exact/decimal answer"},
        },
        "required": [
            "topic_mode", "title", "x_expr", "y_expr", "z_expr", "f_expr",
            "u_expr", "v_expr", "w_expr", "auto_field", "use_rk4",
            "x0", "y0", "t_min", "t_max", "t_val",
            "show_curtain", "show_bundle", "show_surface", "show_2d_field", "show_3d_field", "anim_mode",
            "problem_statement", "step1_param", "step2_deriv", "step3_integrand", "step4_answer",
        ],
    }

    def ask_gemini_vector_ai(
        query: str,
        api_key: str,
        current_state: dict,
        image_b64: str = "",
        image_mime: str = "image/png",
    ) -> tuple[dict, bool, str]:
        if not api_key:
            return current_state, False, "⚠️ Введите GEMINI_API_KEY в верхнем правом углу для AI-разбора"
        try:
            client = genai.Client(api_key=api_key, http_options={"timeout": 18000})
            sys_prompt = (
                "You are an expert Multivariable Calculus & Vector Field 3D/2D Studio solver.\n"
                "You support 5 topics:\n"
                "1. 'path': Parameterized path gamma(t) = [x(t), y(t), z(t)], tangent velocity gamma'(t), arc length L = int ||gamma'(t)|| dt.\n"
                "2. 'flow_line': Flow line of a vector field F = [P, Q, R] satisfying gamma'(t) = F(gamma(t)) from (x0, y0).\n"
                "3. 'path_integral': Scalar path integral (1st kind) int_gamma f(x,y,z) ds = int_{t_min}^{t_max} f(gamma(t)) ||gamma'(t)|| dt.\n"
                "   For 2D path integrals, set z_expr equal to f_expr so the 3D curve lifts to the top of the Riemann curtain z = f(x,y)!\n"
                "4. 'line_integral': Vector line integral (2nd kind) int_gamma F * d(gamma) = int (P dx + Q dy + R dz).\n"
                "5. 'work': Work done by force field F along path gamma: W = int_gamma F * dr.\n\n"
                "IMPORTANT RULES FOR EXPRESSIONS:\n"
                "- Use standard math syntax compatible with JS Math: sin(t), cos(t), tan(t), exp(t), sqrt(t), log(t), pi, e, x^2, etc.\n"
                "- x_expr and y_expr must be functions of t (and optionally x0, y0).\n"
                "- If the problem gives a geometric curve (e.g., 'circle x^2+y^2=4', 'segment from (1,0) to (0,2)', 'parabola y=x^2 from x=0 to x=2'), parameterize it explicitly in terms of t!\n"
                "- Always provide a thorough 4-step explanation in Russian (problem_statement, step1_param, step2_deriv, step3_integrand, step4_answer).\n"
                "- When solving a problem or screenshot, set anim_mode='build' so the user watches the animated construction!"
            )

            contents = []
            if image_b64:
                raw_b64 = image_b64.split(",", 1)[-1] if "," in image_b64 else image_b64
                img_bytes = base64.b64decode(raw_b64)
                contents.append(types.Part.from_bytes(data=img_bytes, mime_type=image_mime or "image/png"))
                prompt_text = (
                    "Распознай задачу на этом скриншоте, определи тему (path, flow_line, path_integral, line_integral, work), "
                    "составь параметризацию кривой gamma(t) = [x(t), y(t), z(t)], пределы t_min..t_max, поле F или функцию f, "
                    "и дай полный пошаговый разбор задачи и ответ на русском языке.\n"
                )
                if query:
                    prompt_text += f"Дополнительный комментарий пользователя: {query}\n"
                contents.append(prompt_text)
            else:
                contents.append(
                    f"Запрос пользователя: {query}\nТекущее состояние: {json.dumps(current_state, ensure_ascii=False)}"
                )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=sys_prompt,
                    temperature=0.1,
                    response_mime_type="application/json",
                    response_schema=AI_PROBLEM_SCHEMA,
                ),
            )
            data = json.loads(response.text or "{}")
            new_st = dict(current_state)
            for k in (
                "topic_mode", "title", "x_expr", "y_expr", "z_expr", "f_expr",
                "u_expr", "v_expr", "w_expr", "auto_field", "use_rk4",
                "x0", "y0", "t_min", "t_max", "t_val",
                "show_curtain", "show_bundle", "show_surface", "show_2d_field", "show_3d_field", "anim_mode",
            ):
                if k in data and data[k] is not None:
                    new_st[k] = data[k]

            new_st["progressive_draw"] = True
            new_st["build_stage"] = 4
            new_st["full_formula"] = f"[{new_st['x_expr']}; {new_st['y_expr']}; {new_st['z_expr']}]"
            new_st["problem_solution"] = {
                "problem_statement": data.get("problem_statement", ""),
                "step1_param": data.get("step1_param", ""),
                "step2_deriv": data.get("step2_deriv", ""),
                "step3_integrand": data.get("step3_integrand", ""),
                "step4_answer": data.get("step4_answer", ""),
            }
            prefix = "📸 Скриншот задачи разобран!" if image_b64 else "✨ Gemini AI построил решение:"
            new_st["status"] = f"{prefix} {new_st['title']}"
            return new_st, True, new_st["status"]
        except Exception as e:
            return current_state, False, f"⚠️ Ошибка Gemini AI: {str(e)[:80]}"

    # =========================================================================
    # 5. ИНТЕРАКТИВНЫЙ 3D + 2D ВИДЖЕТ: PATH, FLOW LINE, PATH/LINE INTEGRALS, WORK
    # =========================================================================
    class VectorFieldFlowStudio(anywidget.AnyWidget):
        _esm = r"""
        function loadPlotly() {
          if (window.Plotly) return Promise.resolve(window.Plotly);
          if (window._plotlyLoadingPromise) return window._plotlyLoadingPromise;
          window._plotlyLoadingPromise = new Promise((resolve, reject) => {
            const sc = document.createElement("script");
            sc.src = "https://cdn.plot.ly/plotly-2.35.2.min.js";
            sc.onload = () => resolve(window.Plotly);
            sc.onerror = reject;
            document.head.appendChild(sc);
          });
          return window._plotlyLoadingPromise;
        }

        // Компилятор математических выражений от (t, x0, y0, x, y, z)
        function compileFlowExpr(exprStr, fallbackVal = 0) {
          let s = String(exprStr ?? "0").trim();
          if (!s) return () => fallbackVal;
          const mapUni = {
            "⁰":"^0","¹":"^1","²":"^2","³":"^3","⁴":"^4","⁵":"^5","⁶":"^6","⁷":"^7","⁸":"^8","⁹":"^9",
            "⁻":"-","⁺":"+","₀":"0","₁":"1","₂":"2","₃":"3","−":"-","–":"-","—":"-","×":"*","·":"*","÷":"/","π":"pi"
          };
          for (const [k, v] of Object.entries(mapUni)) s = s.split(k).join(v);
          s = s.replace(/^[a-zA-Z0-9_]+\s*(\([^)]*\))?\s*=\s*/i, "");
          s = s.replace(/np\./g, "").replace(/Math\./g, "");
          s = s.replace(/\bx_0\b/gi, "x0").replace(/\by_0\b/gi, "y0");
          s = s.replace(/\bx_?1\b/gi, "x").replace(/\bx_?2\b/gi, "y").replace(/\bx_?3\b/gi, "z");

          // Поддержка e^(2t), e^2t, e^-t, e^t
          s = s.replace(/\be\s*\^\s*\(([^)]+)\)/g, "exp($1)");
          s = s.replace(/\be\s*\^\s*([+\-]?\d+(?:\.\d+)?\s*\*?\s*[tTxXyYzZ]\d*)/g, "exp($1)");
          s = s.replace(/\be\s*\^\s*([+\-]?[a-zA-Z0-9_]+)/g, "exp($1)");

          // Неявное умножение
          s = s.replace(/(\d)\s*([a-zA-Z\(])/g, "$1*$2");
          s = s.replace(/(\))\s*([a-zA-Z\d\(])/g, "$1*$2");
          s = s.replace(/\b(x0|y0|t|x|y|z|pi)\s+(x0|y0|t|x|y|z|pi|exp|sin|cos|tan|sqrt|log|abs)\b/gi, "$1*$2");
          s = s.replace(/\b(x0|y0)\s*(exp|sin|cos|tan|sqrt|log|abs|\()/gi, "$1*$2");

          s = s.replace(/\^/g, "**");
          s = s.replace(/\bln\b/gi, "log");

          try {
            const fn = new Function(
              "t", "x0", "y0", "x", "y", "z",
              "const {sin,cos,tan,exp,sqrt,log,abs,atan2,asin,acos,pow,min,max,PI,E} = Math; const pi = PI, e = E; return (" + s + ");"
            );
            const test = fn(0.5, 1.0, 1.0, 1.0, 1.0, 0.5);
            if (typeof test === "number" && !isNaN(test)) return fn;
          } catch (err) {}
          return () => fallbackVal;
        }

        function inferSymbolicVelocity(exprStr, varName) {
          let s = String(exprStr || "").replace(/\s+/g, "");
          s = s.replace(/⁰/g,"^0").replace(/¹/g,"^1").replace(/²/g,"^2").replace(/³/g,"^3").replace(/⁻/g,"-");
          let m = s.match(/^(?:x0|y0)\*?(?:e\^|exp)\(?([+\-]?\d*(?:\.\d+)?)\*?t\)?$/i);
          if (m) {
            const k = m[1];
            if (k === "" || k === "+") return varName;
            if (k === "-") return "-" + varName;
            return k + "*" + varName;
          }
          if (s === "t") return "1";
          let mLin = s.match(/^([+\-]?\d+(?:\.\d+)?)\*?t$/i);
          if (mLin) return mLin[1];
          return "";
        }

        const TOPIC_META = {
          path: {
            badge: "🛤️ PATH γ(t)",
            name: "Параметрический путь γ(t) и длина дуги",
            formula: "γ(t) = [x(t), y(t), z(t)],   ds = ‖γ'(t)‖ dt,   L = ∫ ‖γ'(t)‖ dt",
            color: "#2563eb",
            integrandLabel: "Скорость ‖γ'(t)‖ (элемент дуги ds/dt)",
            integralSymbol: "L(t) = ∫ ‖γ'(τ)‖ dτ",
          },
          flow_line: {
            badge: "🌊 FLOW LINE",
            name: "Линия тока векторного поля γ'(t) = F(γ(t))",
            formula: "dγ/dt = F(γ(t)),   γ(0) = (x₀, y₀, z₀)",
            color: "#0d9488",
            integrandLabel: "Модуль скорости потока ‖F(γ(t))‖",
            integralSymbol: "s(t) = ∫ ‖F(γ(τ))‖ dτ",
          },
          path_integral: {
            badge: "🧱 PATH INTEGRAL",
            name: "Криволинейный интеграл I рода (по длине дуги)",
            formula: "∫_γ f(x,y,z) ds = ∫_a^b f(γ(t)) · ‖γ'(t)‖ dt",
            color: "#7c3aed",
            integrandLabel: "Подынтегральная f(γ(t))·‖γ'(t)‖",
            integralSymbol: "∫_γ f ds",
          },
          line_integral: {
            badge: "🧭 LINE INTEGRAL",
            name: "Криволинейный интеграл II рода (по координатам)",
            formula: "∫_γ F · dγ = ∫_a^b (P dx + Q dy + R dz) = ∫_a^b F(γ(t)) · γ'(t) dt",
            color: "#ea580c",
            integrandLabel: "Скалярное произведение F(γ(t)) · γ'(t)",
            integralSymbol: "∫_γ F · dγ",
          },
          work: {
            badge: "⚡ WORK (РАБОТА ПОЛЯ)",
            name: "Работа силового поля F вдоль пути γ(t)",
            formula: "W = ∫_γ F · dr = ∫_a^b ‖F‖·‖γ'‖·cos θ dt = ∫_a^b F_∥ ds",
            color: "#dc2626",
            integrandLabel: "Мгновенная мощность dW/dt = F(γ(t)) · γ'(t)",
            integralSymbol: "W(t) = ∫ F · dr",
          }
        };

        export default {
          render({ model, el }) {
            let state = {};
            try {
              state = JSON.parse(model.get("state_json") || "{}");
            } catch (e) {}

            let animRaf = null;
            let lastFrameTs = 0;
            let animPhase = 0;
            let userDraggingSlider = false;
            let isApplyingModelUpdate = false;
            let pendingScreenshotB64 = "";
            let pendingScreenshotMime = "image/png";

            el.innerHTML = `
              <style>
                .vf-studio {
                  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                  color: #0f172a;
                  background: #ffffff;
                  border: 1px solid #cbd5e1;
                  border-radius: 14px;
                  padding: 12px 16px;
                  box-shadow: 0 8px 28px rgba(15, 23, 42, 0.06);
                }
                .vf-topbar {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  gap: 12px;
                  flex-wrap: wrap;
                  padding-bottom: 10px;
                  border-bottom: 1px solid #e2e8f0;
                }
                .vf-brand {
                  font-size: 15.5px;
                  font-weight: 800;
                  color: #0f172a;
                  display: flex;
                  align-items: center;
                  gap: 8px;
                  flex-wrap: wrap;
                }
                .vf-badge {
                  background: linear-gradient(135deg, #2563eb 0%, #0d9488 100%);
                  color: #fff;
                  font-size: 11px;
                  font-weight: 800;
                  padding: 4px 10px;
                  border-radius: 999px;
                  letter-spacing: 0.3px;
                }
                /* ПАНЕЛЬ ВЫБОРА ИЗ 5 ТЕМ */
                .vf-topic-tabs {
                  display: grid;
                  grid-template-columns: repeat(5, 1fr);
                  gap: 7px;
                  margin-top: 10px;
                }
                @media (max-width: 1050px) {
                  .vf-topic-tabs { grid-template-columns: repeat(2, 1fr); }
                }
                .vf-topic-tab {
                  cursor: pointer;
                  border: 1.5px solid #cbd5e1;
                  background: #f8fafc;
                  border-radius: 10px;
                  padding: 7px 10px;
                  text-align: left;
                  transition: all 0.16s ease;
                }
                .vf-topic-tab:hover {
                  background: #f1f5f9;
                  border-color: #94a3b8;
                }
                .vf-topic-tab.active {
                  background: #eff6ff;
                  border-color: #2563eb;
                  box-shadow: 0 3px 10px rgba(37, 99, 235, 0.14);
                }
                .vf-topic-tab-title {
                  font-size: 12.5px;
                  font-weight: 800;
                  color: #0f172a;
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                }
                .vf-topic-tab-sub {
                  font-size: 10.5px;
                  color: #475569;
                  margin-top: 2px;
                  font-family: 'JetBrains Mono', monospace;
                }
                .vf-voice-bar {
                  display: flex;
                  align-items: center;
                  gap: 7px;
                  background: linear-gradient(90deg, #f8fafc 0%, #eff6ff 100%);
                  border: 1px solid #cbd5e1;
                  border-radius: 10px;
                  padding: 7px 11px;
                  margin-top: 9px;
                  flex-wrap: wrap;
                }
                .vf-btn {
                  cursor: pointer;
                  border-radius: 8px;
                  border: 1px solid #cbd5e1;
                  background: #ffffff;
                  color: #1e293b;
                  font-size: 12px;
                  font-weight: 700;
                  padding: 6px 11px;
                  transition: all 0.15s ease;
                }
                .vf-btn:hover {
                  background: #f1f5f9;
                  border-color: #94a3b8;
                }
                .vf-btn-primary {
                  background: #2563eb;
                  color: #ffffff;
                  border-color: #1d4ed8;
                }
                .vf-btn-primary:hover { background: #1d4ed8; }
                .vf-btn-ai {
                  background: #0f766e;
                  color: #ffffff;
                  border-color: #115e59;
                }
                .vf-btn-ai:hover { background: #115e59; }
                .vf-btn-snap-mode {
                  background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%);
                  color: #ffffff;
                  border: none;
                }
                .vf-btn-snap-mode:hover { opacity: 0.93; }
                .vf-mic-btn.active {
                  background: #dc2626 !important;
                  color: #fff !important;
                  border-color: #b91c1c !important;
                }
                .vf-cam-btn.active {
                  background: #0d9488 !important;
                  color: #fff !important;
                  border-color: #0f766e !important;
                }
                /* МОДАЛКА / ДРОПЗОНА СКРИНШОТА ЗАДАЧИ */
                .vf-snap-drawer {
                  display: none;
                  margin-top: 9px;
                  background: linear-gradient(135deg, #faf5ff 0%, #fdf2f8 100%);
                  border: 2px dashed #a855f7;
                  border-radius: 12px;
                  padding: 12px 14px;
                }
                .vf-snap-drawer.open { display: block; }
                .vf-snap-grid {
                  display: grid;
                  grid-template-columns: 240px 1fr;
                  gap: 14px;
                  align-items: center;
                }
                @media (max-width: 850px) {
                  .vf-snap-grid { grid-template-columns: 1fr; }
                }
                .vf-snap-preview-box {
                  width: 100%;
                  height: 130px;
                  background: #ffffff;
                  border: 1px solid #d8b4fe;
                  border-radius: 9px;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  overflow: hidden;
                  cursor: pointer;
                  position: relative;
                }
                .vf-snap-preview-box img {
                  max-width: 100%;
                  max-height: 100%;
                  object-fit: contain;
                }
                /* КАРТОЧКА РЕШЕНИЯ ЗАДАЧИ СО СКРИНШОТА */
                .vf-solution-panel {
                  display: none;
                  margin-top: 9px;
                  background: #f0fdf4;
                  border: 1.5px solid #86efac;
                  border-radius: 11px;
                  padding: 10px 14px;
                }
                .vf-solution-panel.visible { display: block; }
                .vf-sol-steps {
                  display: grid;
                  grid-template-columns: repeat(4, 1fr);
                  gap: 8px;
                  margin-top: 8px;
                }
                @media (max-width: 1050px) {
                  .vf-sol-steps { grid-template-columns: repeat(2, 1fr); }
                }
                .vf-sol-card {
                  background: #ffffff;
                  border: 1px solid #bbf7d0;
                  border-radius: 8px;
                  padding: 7px 9px;
                  font-size: 11.5px;
                  line-height: 1.45;
                }
                .vf-sol-card b {
                  display: block;
                  color: #166534;
                  font-size: 11px;
                  text-transform: uppercase;
                  margin-bottom: 3px;
                }
                /* СЕТКА ВВОДА ФОРМУЛ */
                .vf-grid-inputs {
                  display: grid;
                  grid-template-columns: 1.15fr 1.45fr 0.9fr 1.25fr;
                  gap: 9px;
                  margin-top: 9px;
                  background: #f8fafc;
                  border: 1px solid #e2e8f0;
                  border-radius: 10px;
                  padding: 9px 11px;
                }
                @media (max-width: 1150px) {
                  .vf-grid-inputs { grid-template-columns: 1fr 1fr; }
                }
                .vf-label {
                  font-size: 11px;
                  font-weight: 700;
                  color: #334155;
                  margin-bottom: 4px;
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                }
                .vf-input {
                  padding: 5px 8px;
                  border: 1px solid #cbd5e1;
                  border-radius: 7px;
                  font-size: 12px;
                  color: #0f172a;
                  background: #fff;
                  outline: none;
                  box-sizing: border-box;
                  font-family: 'JetBrains Mono', Consolas, monospace;
                }
                .vf-input:focus {
                  border-color: #2563eb;
                  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
                }
                .vf-comp-row {
                  display: grid;
                  grid-template-columns: repeat(3, 1fr);
                  gap: 5px;
                }
                .vf-comp-box {
                  display: flex;
                  align-items: center;
                  background: #fff;
                  border: 1px solid #cbd5e1;
                  border-radius: 7px;
                  padding: 2px 5px;
                }
                .vf-comp-box span {
                  font-size: 11px;
                  font-weight: 700;
                  color: #2563eb;
                  margin-right: 3px;
                  white-space: nowrap;
                }
                .vf-comp-box input {
                  border: none;
                  outline: none;
                  width: 100%;
                  font-family: 'JetBrains Mono', Consolas, monospace;
                  font-size: 11.5px;
                  font-weight: 600;
                  color: #0f172a;
                }
                /* КОНСТРУКТОР АНИМАЦИИ ПОСТРОЕНИЯ (ШАГ ЗА ШАГОМ) */
                .vf-builder-bar {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  gap: 8px;
                  flex-wrap: wrap;
                  margin-top: 9px;
                  padding: 7px 11px;
                  background: linear-gradient(90deg, #eff6ff 0%, #f0fdfa 100%);
                  border: 1px solid #bfdbfe;
                  border-radius: 10px;
                }
                .vf-stage-btn {
                  cursor: pointer;
                  border: 1px solid #93c5fd;
                  background: #ffffff;
                  color: #1e3a8a;
                  border-radius: 7px;
                  padding: 4px 9px;
                  font-size: 11.5px;
                  font-weight: 700;
                  transition: all 0.14s;
                }
                .vf-stage-btn.active {
                  background: #2563eb;
                  color: #ffffff;
                  border-color: #1d4ed8;
                }
                .vf-build-play-btn {
                  cursor: pointer;
                  border: none;
                  background: linear-gradient(135deg, #059669 0%, #0d9488 100%);
                  color: #ffffff;
                  border-radius: 8px;
                  padding: 5px 13px;
                  font-size: 12px;
                  font-weight: 800;
                  box-shadow: 0 2px 8px rgba(5, 150, 105, 0.25);
                }
                .vf-build-play-btn.playing {
                  background: linear-gradient(135deg, #dc2626 0%, #ea580c 100%);
                }
                /* ПОЛЗУНКИ */
                .vf-sliders-grid {
                  display: grid;
                  grid-template-columns: 1.3fr 1fr 1fr 1fr;
                  gap: 9px;
                  margin-top: 9px;
                }
                @media (max-width: 1000px) {
                  .vf-sliders-grid { grid-template-columns: repeat(2, 1fr); }
                }
                .vf-slider-card {
                  background: #f8fafc;
                  border: 1px solid #e2e8f0;
                  border-radius: 9px;
                  padding: 6px 9px;
                }
                .vf-slider-head {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  font-size: 11.5px;
                  margin-bottom: 3px;
                }
                .vf-play-btn {
                  cursor: pointer;
                  border: 1px solid #cbd5e1;
                  background: #fff;
                  border-radius: 6px;
                  padding: 1px 7px;
                  font-size: 11px;
                  font-weight: 700;
                  color: #2563eb;
                }
                .vf-play-btn.playing {
                  background: #2563eb;
                  color: #fff;
                  border-color: #1d4ed8;
                }
                .vf-val-pill {
                  font-family: 'JetBrains Mono', monospace;
                  font-size: 11.5px;
                  font-weight: 700;
                  color: #0f172a;
                  background: #e2e8f0;
                  padding: 1px 6px;
                  border-radius: 5px;
                }
                .vf-chips-bar {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  gap: 6px;
                  flex-wrap: wrap;
                  margin-top: 8px;
                  padding-bottom: 6px;
                  border-bottom: 1px solid #f1f5f9;
                }
                .vf-chips-group {
                  display: flex;
                  align-items: center;
                  gap: 5px;
                  flex-wrap: wrap;
                }
                .vf-chip {
                  cursor: pointer;
                  user-select: none;
                  font-size: 11px;
                  font-weight: 600;
                  padding: 4px 9px;
                  border-radius: 999px;
                  border: 1px solid #cbd5e1;
                  background: #f8fafc;
                  color: #475569;
                  transition: all 0.14s ease;
                }
                .vf-chip.active {
                  background: #eff6ff;
                  color: #1d4ed8;
                  border-color: #93c5fd;
                }
                .vf-status-banner {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  flex-wrap: wrap;
                  gap: 8px;
                  background: #f8fafc;
                  border-left: 4px solid #2563eb;
                  border-radius: 6px;
                  padding: 6px 12px;
                  margin-top: 7px;
                  font-size: 12.5px;
                }
                .vf-live-integral-pill {
                  background: #0f172a;
                  color: #f8fafc;
                  font-family: 'JetBrains Mono', monospace;
                  font-size: 12px;
                  font-weight: 700;
                  padding: 4px 10px;
                  border-radius: 7px;
                  display: flex;
                  align-items: center;
                  gap: 10px;
                }
                .vf-step-cards {
                  display: grid;
                  grid-template-columns: repeat(4, 1fr);
                  gap: 8px;
                  margin-top: 8px;
                }
                @media (max-width: 1050px) {
                  .vf-step-cards { grid-template-columns: repeat(2, 1fr); }
                }
                .vf-step-card {
                  background: #f8fafc;
                  border: 1px solid #e2e8f0;
                  border-radius: 8px;
                  padding: 8px 10px;
                  font-size: 11.5px;
                  line-height: 1.45;
                }
                .vf-step-card b {
                  color: #1e3a8a;
                  display: block;
                  margin-bottom: 2px;
                  font-size: 11px;
                  text-transform: uppercase;
                }
                .vf-step-card code {
                  font-family: 'JetBrains Mono', monospace;
                  font-weight: 700;
                  color: #0f172a;
                  background: #e2e8f0;
                  padding: 1px 4px;
                  border-radius: 4px;
                }
                .vf-cam-pip {
                  position: absolute;
                  bottom: 16px;
                  left: 16px;
                  width: 256px;
                  background: rgba(15, 23, 42, 0.92);
                  border: 1px solid #38bdf8;
                  border-radius: 12px;
                  color: #f8fafc;
                  z-index: 50;
                  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
                  overflow: hidden;
                  backdrop-filter: blur(8px);
                }
                .vf-cam-header {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  padding: 6px 10px;
                  background: rgba(30, 41, 59, 0.95);
                  border-bottom: 1px solid rgba(56, 189, 248, 0.3);
                  font-size: 11.5px;
                  font-weight: 700;
                }
                .vf-cam-icon-btn {
                  cursor: pointer;
                  background: transparent;
                  border: 1px solid rgba(148, 163, 184, 0.4);
                  color: #e2e8f0;
                  border-radius: 5px;
                  padding: 1px 6px;
                  font-size: 11px;
                }
              </style>

              <div class="vf-studio">
                <!-- ШАПКА -->
                <div class="vf-topbar">
                  <div class="vf-brand">
                    <span id="vf-mode-badge" class="vf-badge">🌊 FLOW LINE</span>
                    <span id="vf-mode-header">Поток векторного поля, Путь γ(t), Криволинейные интегралы I/II рода и Работа силы</span>
                  </div>
                  <div style="display:flex;align-items:center;gap:6px;">
                    <span style="font-size:11.5px;color:#64748b;font-weight:600;">🔑 Gemini API:</span>
                    <input id="vf-apikey" type="password" class="vf-input" style="width:165px;padding:4px 8px;font-size:11.5px;" placeholder="AI ключ для скриншотов" />
                  </div>
                </div>

                <!-- 5 ВКЛАДОК ТЕМ: PATH / FLOW LINE / PATH INTEGRAL / LINE INTEGRAL / WORK -->
                <div class="vf-topic-tabs">
                  <div class="vf-topic-tab" data-topic="path">
                    <div class="vf-topic-tab-title"><span>🛤️ 1. Path (Путь γ)</span><span>3D+2D</span></div>
                    <div class="vf-topic-tab-sub">γ(t)=[x(t),y(t),z(t)], L=∫‖γ'‖dt</div>
                  </div>
                  <div class="vf-topic-tab active" data-topic="flow_line">
                    <div class="vf-topic-tab-title"><span>🌊 2. Flow Line</span><span>Поток</span></div>
                    <div class="vf-topic-tab-sub">γ'(t) = F(γ(t)), фазовый портрет</div>
                  </div>
                  <div class="vf-topic-tab" data-topic="path_integral">
                    <div class="vf-topic-tab-title"><span>🧱 3. Path Integral</span><span>I род</span></div>
                    <div class="vf-topic-tab-sub">∫_γ f(x,y,z) ds = ∫ f(γ(t))‖γ'‖dt</div>
                  </div>
                  <div class="vf-topic-tab" data-topic="line_integral">
                    <div class="vf-topic-tab-title"><span>🧭 4. Line Integral</span><span>II род</span></div>
                    <div class="vf-topic-tab-sub">∫_γ F·dγ = ∫ (Pdx + Qdy + Rdz)</div>
                  </div>
                  <div class="vf-topic-tab" data-topic="work">
                    <div class="vf-topic-tab-title"><span>⚡ 5. Work (Работа)</span><span>Физика</span></div>
                    <div class="vf-topic-tab-sub">W = ∫_γ F·dr = ∫ ‖F‖‖γ'‖cosθ dt</div>
                  </div>
                </div>

                <!-- СТРОКА БЫСТРОГО ВВОДА, ГОЛОСА, КАМЕРЫ И КНОПКИ СКРИНШОТА ЗАДАЧИ -->
                <div class="vf-voice-bar">
                  <button id="vf-mic-btn" class="vf-btn vf-mic-btn">🎙️ Голос</button>
                  <select id="vf-lang" class="vf-input" style="padding:4px 6px;font-size:11.5px;">
                    <option value="ru-RU">RU</option>
                    <option value="en-US">EN</option>
                  </select>
                  <button id="vf-cam-btn" class="vf-btn vf-cam-btn" title="Управление 3D-сценой и параметрами жестами руки">📷 Камера 3D</button>
                  <button id="vf-snap-toggle-btn" class="vf-btn vf-btn-snap-mode" title="Вставить скриншот задачи (Ctrl+V) и получить полное 3D/2D построение и решение">📸 Скриншот задачи (Ctrl+V)</button>
                  <input id="vf-nl-input" type="text" class="vf-input" style="flex:1;min-width:220px;font-weight:700;"
                    value="[x0*e^2t; y0*e^(-t); t]"
                    placeholder="Введите формулу [x(t); y(t); z(t)] или условие задачи текстом..." />
                  <button id="vf-nl-run" class="vf-btn vf-btn-primary">⚡ Построить</button>
                  <button id="vf-nl-ai" class="vf-btn vf-btn-ai">🤖 Решить с AI</button>
                  <span id="vf-voice-live" style="font-size:11.5px;color:#2563eb;font-weight:600;"></span>
                </div>

                <!-- ПАНЕЛЬ ЗАГРУЗКИ / ВСТАВКИ СКРИНШОТА ЗАДАЧИ (CTRL+V / DRAG & DROP) -->
                <div id="vf-snap-drawer" class="vf-snap-drawer">
                  <div class="vf-snap-grid">
                    <div>
                      <div id="vf-snap-dropzone" class="vf-snap-preview-box" title="Кликните для выбора картинки или нажмите Ctrl+V">
                        <span id="vf-snap-placeholder" style="font-size:11.5px;color:#7e22ce;font-weight:700;text-align:center;padding:8px;">
                          📋 Нажмите <b>Ctrl + V</b> чтобы вставить скриншот<br/>или кликните для выбора файла
                        </span>
                        <img id="vf-snap-img" style="display:none;" alt="Screenshot preview" />
                      </div>
                      <input id="vf-snap-file" type="file" accept="image/*" style="display:none;" />
                    </div>
                    <div style="display:flex;flex-direction:column;gap:7px;">
                      <div style="font-size:13px;font-weight:800;color:#581c87;">
                        📸 Режим «Скриншот задачи → Полный разбор + 3D/2D Анимация построения»
                      </div>
                      <div style="font-size:11.5px;color:#475569;">
                        Сделайте скриншот любого задания по темам <b>Path, Flow Line, Path Integral (∫ f ds), Line Integral (∫ F·dγ) или Work (Работа поля)</b>, нажмите <b>Ctrl+V</b> — ИИ автоматически параметризует кривую γ(t), построит 3D/2D график и запустит пошаговую анимацию!
                      </div>
                      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
                        <input id="vf-snap-note" type="text" class="vf-input" style="flex:1;min-width:200px;" placeholder="Доп. комментарий к скриншоту (необязательно)..." />
                        <button id="vf-snap-solve-btn" class="vf-btn vf-btn-snap-mode">🚀 Распознать и построить график</button>
                        <button id="vf-snap-close-btn" class="vf-btn">Скрыть</button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- КАРТОЧКА ПОШАГОВОГО РЕШЕНИЯ ЗАДАЧИ СО СКРИНШОТА / AI -->
                <div id="vf-solution-panel" class="vf-solution-panel">
                  <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;">
                    <div id="vf-sol-statement" style="font-size:12.5px;font-weight:800;color:#14532d;"></div>
                    <button id="vf-sol-hide-btn" class="vf-btn" style="padding:2px 8px;font-size:11px;">✕ Скрыть разбор</button>
                  </div>
                  <div class="vf-sol-steps">
                    <div class="vf-sol-card"><b>Шаг 1. Параметризация γ(t)</b><span id="vf-sol-s1"></span></div>
                    <div class="vf-sol-card"><b>Шаг 2. Производная γ'(t) и ds</b><span id="vf-sol-s2"></span></div>
                    <div class="vf-sol-card"><b>Шаг 3. Подынтегральное выражение</b><span id="vf-sol-s3"></span></div>
                    <div class="vf-sol-card"><b>Шаг 4. Итоговый ответ</b><span id="vf-sol-s4"></span></div>
                  </div>
                </div>

                <!-- ПАНЕЛЬ ПАРАМЕТРИЧЕСКИХ КОМПОНЕНТ x(t), y(t), z(t), СКАЛЯРНОЙ f(x,y,z) И ПОЛЯ F(x,y,z) -->
                <div class="vf-grid-inputs">
                  <!-- 1. Готовые примеры по всем 5 темам -->
                  <div>
                    <div class="vf-label">
                      <span>📚 Примеры по 5 темам:</span>
                      <span style="color:#2563eb;font-weight:600;">10 пресетов</span>
                    </div>
                    <select id="vf-preset" class="vf-input" style="width:100%;font-family:inherit;font-weight:600;">
                      <optgroup label="🌊 Flow Line (Линии тока)">
                        <option value="preset_flow_saddle">1. Flow Line: [x₀·e^(2t); y₀·e^(-t); t] (Седловой поток)</option>
                        <option value="preset_flow_spiral">2. Flow Line: Спиральный фокус в 3D и 2D</option>
                      </optgroup>
                      <optgroup label="🛤️ Path (Путь γ(t) и длина дуги)">
                        <option value="preset_path_helix">3. Path: Винтовая линия [1.5cos t; 1.5sin t; 0.45t]</option>
                        <option value="preset_path_twisted">4. Path: 3D кубическая дуга [t; 0.7t²-1; 0.35t³]</option>
                      </optgroup>
                      <optgroup label="🧱 Path Integral (Интеграл I рода ∫_γ f ds)">
                        <option value="preset_path_int_circle">5. Path Integral: ∫_γ (1.2 + 0.4x² + 0.6y) ds по дуге</option>
                        <option value="preset_path_int_parabola">6. Path Integral: ∫_γ (0.8 + 0.5x² + 0.4y²) ds по параболе</option>
                      </optgroup>
                      <optgroup label="🧭 Line Integral (Интеграл II рода ∫_γ F·dγ)">
                        <option value="preset_line_int_vortex">7. Line Integral: Циркуляция F=[-y, x, 0] по окружности</option>
                        <option value="preset_line_int_3d">8. Line Integral 3D: ∫_γ (y dx + z dy + x dz) по спирали</option>
                      </optgroup>
                      <optgroup label="⚡ Work (Работа силы W = ∫_γ F·dr)">
                        <option value="preset_work_parabola">9. Work: Работа силы F=[y+0.5x, x², 0.4] вдоль параболы</option>
                        <option value="preset_work_mixed">10. Work: Знакопеременная работа F=[x, -y, 0] по дуге</option>
                      </optgroup>
                    </select>
                  </div>

                  <!-- 2. Кривая γ(t) = [x(t); y(t); z(t)] -->
                  <div>
                    <div class="vf-label">
                      <span>📈 Путь <b>γ(t) = [x(t); y(t); z(t)]</b>:</span>
                      <label style="color:#0d9488;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:3px;" title="Численно строить линию тока RK4 напрямую из векторного поля F=[P,Q,R] от точки (x₀, y₀)">
                        <input id="vf-use-rk4" type="checkbox" /> RK4 из поля F
                      </label>
                    </div>
                    <div class="vf-comp-row">
                      <div class="vf-comp-box">
                        <span>x(t)=</span>
                        <input id="vf-x-expr" type="text" value="x0 * e^(2*t)" />
                      </div>
                      <div class="vf-comp-box">
                        <span>y(t)=</span>
                        <input id="vf-y-expr" type="text" value="y0 * e^(-t)" />
                      </div>
                      <div class="vf-comp-box">
                        <span style="color:#dc2626;">z(t)=</span>
                        <input id="vf-z-expr" type="text" value="t" />
                      </div>
                    </div>
                  </div>

                  <!-- 3. Скалярная функция f(x,y,z) для Path Integral -->
                  <div>
                    <div class="vf-label">
                      <span>🧱 Скалярная <b>f(x,y,z)</b>:</span>
                      <span style="color:#7c3aed;font-weight:600;">для ∫_γ f ds</span>
                    </div>
                    <div class="vf-comp-box" style="padding:4px 7px;">
                      <span style="color:#7c3aed;">f =</span>
                      <input id="vf-f-expr" type="text" value="x^2 + y^2" title="Скалярная функция высоты забора Римана f(x,y,z) для Path Integral" />
                    </div>
                  </div>

                  <!-- 4. Векторное поле / Сила F(x,y,z) = [P, Q, R] -->
                  <div>
                    <div class="vf-label">
                      <span>🧭 Векторное поле <b>F = [P, Q, R]</b>:</span>
                      <label style="font-weight:600;color:#2563eb;cursor:pointer;display:flex;align-items:center;gap:3px;">
                        <input id="vf-auto-field" type="checkbox" checked /> авто из γ'
                      </label>
                    </div>
                    <div class="vf-comp-row">
                      <div class="vf-comp-box">
                        <span style="color:#0d9488;">P=</span>
                        <input id="vf-u-expr" type="text" value="2*x" />
                      </div>
                      <div class="vf-comp-box">
                        <span style="color:#0d9488;">Q=</span>
                        <input id="vf-v-expr" type="text" value="-y" />
                      </div>
                      <div class="vf-comp-box">
                        <span style="color:#0d9488;">R=</span>
                        <input id="vf-w-expr" type="text" value="1" />
                      </div>
                    </div>
                  </div>
                </div>

                <!-- ПАНЕЛЬ ПОШАГОВОЙ АНИМАЦИИ ПОСТРОЕНИЯ ГРАФИКА ("КАК СТРОИТСЯ") -->
                <div class="vf-builder-bar">
                  <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
                    <button id="vf-build-play" class="vf-build-play-btn">🎬 Анимация построения с нуля (Play)</button>
                    <span style="font-size:11.5px;font-weight:800;color:#1e3a8a;margin-left:4px;">Этапы построения:</span>
                    <button class="vf-stage-btn" data-stage="1">Шаг 1: 2D Путь γ(t)</button>
                    <button class="vf-stage-btn" data-stage="2">Шаг 2: Подъём в 3D и γ'(t)</button>
                    <button class="vf-stage-btn" data-stage="3">Шаг 3: Поле F / Поверхность f</button>
                    <button class="vf-stage-btn active" data-stage="4">Шаг 4: Интеграл / Работа (Все слои)</button>
                  </div>
                  <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                    <label style="font-size:11.5px;font-weight:700;color:#0f172a;cursor:pointer;display:flex;align-items:center;gap:4px;">
                      <input id="vf-prog-draw" type="checkbox" checked />
                      ✏️ Рисовать кривую по росту t
                    </label>
                    <div style="display:flex;align-items:center;gap:4px;font-size:11.5px;font-weight:700;color:#475569;">
                      <span>Скорость:</span>
                      <select id="vf-anim-speed" class="vf-input" style="padding:2px 6px;font-size:11px;">
                        <option value="0.5">0.5x (Медленно)</option>
                        <option value="1.0" selected>1.0x (Норм)</option>
                        <option value="1.8">1.8x (Быстро)</option>
                      </select>
                    </div>
                  </div>
                </div>

                <!-- ПОЛЗУНКИ ПАРАМЕТРОВ t, [t_min, t_max], x0, y0 -->
                <div class="vf-sliders-grid">
                  <!-- Ползунок времени t -->
                  <div class="vf-slider-card" style="border-color:#93c5fd;background:#f0f7ff;">
                    <div class="vf-slider-head">
                      <span>⏱️ Параметр <b>t</b> (построение):</span>
                      <div style="display:flex;align-items:center;gap:4px;">
                        <button id="vf-play-t" class="vf-play-btn" title="Анимировать параметр t">▶</button>
                        <span id="vf-val-t" class="vf-val-pill">0.55</span>
                      </div>
                    </div>
                    <input id="vf-sl-t" type="range" min="-1.2" max="1.2" step="0.01" value="0.55" style="width:100%;accent-color:#2563eb;" />
                  </div>

                  <!-- Интервал t ∈ [t_min, t_max] -->
                  <div class="vf-slider-card">
                    <div class="vf-slider-head">
                      <span>📏 Пределы <b>t ∈ [a, b]</b>:</span>
                      <span id="vf-val-tspan" class="vf-val-pill">[-1.2, 1.2]</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:5px;margin-top:2px;">
                      <input id="vf-tmin-inp" type="number" step="0.2" class="vf-input" style="width:100%;padding:3px 5px;" value="-1.2" title="Нижний предел t_min (a)" />
                      <span style="font-weight:700;color:#64748b;">..</span>
                      <input id="vf-tmax-inp" type="number" step="0.2" class="vf-input" style="width:100%;padding:3px 5px;" value="1.2" title="Верхний предел t_max (b)" />
                    </div>
                  </div>

                  <!-- Начальная координата x0 -->
                  <div class="vf-slider-card">
                    <div class="vf-slider-head">
                      <span>📍 Старт <b>x₀</b> (клик на 2D):</span>
                      <div style="display:flex;align-items:center;gap:4px;">
                        <button id="vf-play-x0" class="vf-play-btn" title="Анимировать x₀">▶</button>
                        <span id="vf-val-x0" class="vf-val-pill">0.45</span>
                      </div>
                    </div>
                    <input id="vf-sl-x0" type="range" min="-2.4" max="2.4" step="0.02" value="0.45" style="width:100%;accent-color:#0d9488;" />
                  </div>

                  <!-- Начальная координата y0 + вращение (x0, y0) -->
                  <div class="vf-slider-card">
                    <div class="vf-slider-head">
                      <span>📍 Старт <b>y₀</b> / Орбита:</span>
                      <div style="display:flex;align-items:center;gap:4px;">
                        <button id="vf-play-y0" class="vf-play-btn" title="Анимировать y₀">▶</button>
                        <button id="vf-play-orbit" class="vf-play-btn" title="Вращать точку (x₀, y₀) по кругу">🔄</button>
                        <span id="vf-val-y0" class="vf-val-pill">1.35</span>
                      </div>
                    </div>
                    <input id="vf-sl-y0" type="range" min="-2.4" max="2.4" step="0.02" value="1.35" style="width:100%;accent-color:#0d9488;" />
                  </div>
                </div>

                <!-- ЧИПЫ СЛОЕВ ВИЗУАЛИЗАЦИИ -->
                <div class="vf-chips-bar">
                  <div class="vf-chips-group">
                    <span style="font-size:11px;font-weight:700;color:#475569;">Слои:</span>
                    <div id="chip-curtain" class="vf-chip active" title="Вертикальная шторка подъёма / забор Римана от z=0 к кривой">🧱 Шторка / Забор Римана</div>
                    <div id="chip-floor-curve" class="vf-chip active" title="Проекция пути γ(t) = [x(t), y(t), 0] на плоскость z=0">🟦 Тень γ(t) на z=0</div>
                    <div id="chip-velocity" class="vf-chip active" title="Вектор скорости γ'(t), сила F(γ(t)) и касательная проекция F_∥">🎯 Векторы γ'(t) и F(γ(t))</div>
                    <div id="chip-path-vectors" class="vf-chip active" title="Векторы поля F(γ(t_k)) или столбики Римана вдоль самой кривой">🦔 Векторы / столбики вдоль γ(t)</div>
                    <div id="chip-2d-field" class="vf-chip active" title="Сетка стрелок векторного поля F(x,y) на плоскости">🧭 2D Поле F(x,y)</div>
                    <div id="chip-3d-field" class="vf-chip active" title="Трехмерные конусы поля F(x,y,z) в 3D">🚀 3D Конусы поля</div>
                    <div id="chip-bundle" class="vf-chip active" title="Семейство соседних линий тока (фазовый портрет)">🌊 Пучок траекторий</div>
                    <div id="chip-surface" class="vf-chip" title="Поверхность z = f(x,y) над плоскостью">🏔️ Поверхность z=f(x,y)</div>
                    <div id="chip-integrand" class="vf-chip active" title="Показывать справа снизу график накопления интеграла по t">📈 График интеграла по t</div>
                    <div id="chip-2d" class="vf-chip active" title="Показывать 2D плоскость и график интеграла справа от 3D">🗺️ 3D + 2D панель</div>
                  </div>
                </div>

                <!-- БАННЕР СТАТУСА И ЖИВОГО ЗНАЧЕНИЯ ИНТЕГРАЛА / РАБОТЫ / ДЛИНЫ ДУГИ -->
                <div class="vf-status-banner">
                  <div>
                    <div id="vf-title" style="font-weight:800;color:#0f172a;">
                      Flow Line: F(γ(t)) = [x₀·e^(2t); y₀·e^(-t); t]
                    </div>
                    <div id="vf-status" style="font-size:11.5px;color:#1d4ed8;font-weight:600;margin-top:1px;">
                      ⚡ Кликните по 2D-графику справа для выбора (x₀, y₀) или нажмите «🎬 Анимация построения с нуля»
                    </div>
                  </div>
                  <div id="vf-live-metrics" class="vf-live-integral-pill">
                    <span id="vf-metric-main">∫ = 0.000</span>
                    <span style="color:#94a3b8;">|</span>
                    <span id="vf-metric-arc" style="color:#38bdf8;">Дуга s(t) = 0.000</span>
                  </div>
                </div>

                <!-- ГЛАВНЫЙ ХОЛСТ PLOTLY (3D СЛЕВА + 2D ПЛОСКОСТЬ И ГРАФИК ИНТЕГРАЛА СПРАВА) -->
                <div id="vf-plot-wrap" style="position:relative;width:100%;height:630px;margin-top:8px;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;background:#ffffff;">
                  <div id="vf-plot" style="width:100%;height:100%;"></div>

                  <!-- ПЛАВАЮЩИЙ HUD ВЕБ-КАМЕРЫ -->
                  <div id="vf-cam-pip" class="vf-cam-pip" style="display:none;">
                    <div id="vf-cam-header" class="vf-cam-header">
                      <span>📷 3D Gesture Control</span>
                      <div style="display:flex;gap:4px;">
                        <button id="vf-cam-reset-btn" class="vf-cam-icon-btn" title="Сбросить ракурс">🎯</button>
                        <button id="vf-cam-snap-btn" class="vf-cam-icon-btn" title="Скачать PNG">📸</button>
                        <button id="vf-cam-close-btn" class="vf-cam-icon-btn" title="Закрыть камеру">✕</button>
                      </div>
                    </div>
                    <div style="padding:8px;">
                      <div style="position:relative;width:240px;height:150px;border-radius:8px;overflow:hidden;background:#000;border:1px solid #334155;">
                        <video id="vf-cam-video" autoplay playsinline muted style="display:none;"></video>
                        <canvas id="vf-cam-canvas" width="240" height="150" style="width:100%;height:100%;display:block;"></canvas>
                      </div>
                      <div style="margin-top:6px;display:flex;flex-direction:column;gap:5px;font-size:11px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                          <span style="color:#94a3b8;">Жест управляет:</span>
                          <select id="vf-cam-target" style="background:#1e293b;color:#f8fafc;border:1px solid #475569;border-radius:5px;padding:2px 5px;font-size:11px;">
                            <option value="orbit">🔄 Вращение 3D сцены</option>
                            <option value="time_t">⏱️ Построение по времени t</option>
                            <option value="point">📍 Точка старта (x₀, y₀)</option>
                          </select>
                        </div>
                        <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;">
                          <span style="color:#94a3b8;">Чувств:</span>
                          <input id="vf-cam-speed" type="range" min="0.3" max="2.5" step="0.1" value="1.1" style="flex:1;height:4px;accent-color:#38bdf8;" />
                          <span id="vf-cam-speed-val" style="color:#38bdf8;font-family:monospace;">1.1x</span>
                        </div>
                        <div id="vf-cam-status-msg" style="text-align:center;color:#38bdf8;font-weight:600;font-size:10.5px;">
                          👋 Помашите рукой перед камерой
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- ПОШАГОВЫЕ МАТЕМАТИЧЕСКИЕ КАРТОЧКИ ВНИЗУ (АДАПТИРУЮТСЯ ПОД ВЫБРАННУЮ ТЕМУ) -->
                <div id="vf-steps-bar" class="vf-step-cards"></div>
              </div>
            `;

            const dom = {
              modeBadge: el.querySelector("#vf-mode-badge"),
              modeHeader: el.querySelector("#vf-mode-header"),
              apiKey: el.querySelector("#vf-apikey"),
              topicTabs: Array.from(el.querySelectorAll(".vf-topic-tab")),
              micBtn: el.querySelector("#vf-mic-btn"),
              lang: el.querySelector("#vf-lang"),
              camBtn: el.querySelector("#vf-cam-btn"),
              snapToggleBtn: el.querySelector("#vf-snap-toggle-btn"),
              nlInput: el.querySelector("#vf-nl-input"),
              nlRun: el.querySelector("#vf-nl-run"),
              nlAi: el.querySelector("#vf-nl-ai"),
              voiceLive: el.querySelector("#vf-voice-live"),
              snapDrawer: el.querySelector("#vf-snap-drawer"),
              snapDropzone: el.querySelector("#vf-snap-dropzone"),
              snapPlaceholder: el.querySelector("#vf-snap-placeholder"),
              snapImg: el.querySelector("#vf-snap-img"),
              snapFile: el.querySelector("#vf-snap-file"),
              snapNote: el.querySelector("#vf-snap-note"),
              snapSolveBtn: el.querySelector("#vf-snap-solve-btn"),
              snapCloseBtn: el.querySelector("#vf-snap-close-btn"),
              solPanel: el.querySelector("#vf-solution-panel"),
              solStatement: el.querySelector("#vf-sol-statement"),
              solS1: el.querySelector("#vf-sol-s1"),
              solS2: el.querySelector("#vf-sol-s2"),
              solS3: el.querySelector("#vf-sol-s3"),
              solS4: el.querySelector("#vf-sol-s4"),
              solHideBtn: el.querySelector("#vf-sol-hide-btn"),
              preset: el.querySelector("#vf-preset"),
              useRk4: el.querySelector("#vf-use-rk4"),
              xExpr: el.querySelector("#vf-x-expr"),
              yExpr: el.querySelector("#vf-y-expr"),
              zExpr: el.querySelector("#vf-z-expr"),
              fExpr: el.querySelector("#vf-f-expr"),
              uExpr: el.querySelector("#vf-u-expr"),
              vExpr: el.querySelector("#vf-v-expr"),
              wExpr: el.querySelector("#vf-w-expr"),
              autoField: el.querySelector("#vf-auto-field"),
              buildPlay: el.querySelector("#vf-build-play"),
              stageBtns: Array.from(el.querySelectorAll(".vf-stage-btn")),
              progDraw: el.querySelector("#vf-prog-draw"),
              animSpeed: el.querySelector("#vf-anim-speed"),
              slT: el.querySelector("#vf-sl-t"),
              tMinInp: el.querySelector("#vf-tmin-inp"),
              tMaxInp: el.querySelector("#vf-tmax-inp"),
              slX0: el.querySelector("#vf-sl-x0"),
              slY0: el.querySelector("#vf-sl-y0"),
              valT: el.querySelector("#vf-val-t"),
              valTspan: el.querySelector("#vf-val-tspan"),
              valX0: el.querySelector("#vf-val-x0"),
              valY0: el.querySelector("#vf-val-y0"),
              playT: el.querySelector("#vf-play-t"),
              playX0: el.querySelector("#vf-play-x0"),
              playY0: el.querySelector("#vf-play-y0"),
              playOrbit: el.querySelector("#vf-play-orbit"),
              chipCurtain: el.querySelector("#chip-curtain"),
              chipFloorCurve: el.querySelector("#chip-floor-curve"),
              chipVelocity: el.querySelector("#chip-velocity"),
              chipPathVectors: el.querySelector("#chip-path-vectors"),
              chip2dField: el.querySelector("#chip-2d-field"),
              chip3dField: el.querySelector("#chip-3d-field"),
              chipBundle: el.querySelector("#chip-bundle"),
              chipSurface: el.querySelector("#chip-surface"),
              chipIntegrand: el.querySelector("#chip-integrand"),
              chip2d: el.querySelector("#chip-2d"),
              title: el.querySelector("#vf-title"),
              status: el.querySelector("#vf-status"),
              metricMain: el.querySelector("#vf-metric-main"),
              metricArc: el.querySelector("#vf-metric-arc"),
              plot: el.querySelector("#vf-plot"),
              stepsBar: el.querySelector("#vf-steps-bar"),
              camPip: el.querySelector("#vf-cam-pip"),
              camVideo: el.querySelector("#vf-cam-video"),
              camCanvas: el.querySelector("#vf-cam-canvas"),
              camTarget: el.querySelector("#vf-cam-target"),
              camSpeed: el.querySelector("#vf-cam-speed"),
              camSpeedVal: el.querySelector("#vf-cam-speed-val"),
              camResetBtn: el.querySelector("#vf-cam-reset-btn"),
              camSnapBtn: el.querySelector("#vf-cam-snap-btn"),
              camCloseBtn: el.querySelector("#vf-cam-close-btn"),
            };

            const JS_PRESETS = {
              preset_flow_saddle: {
                preset_id: "preset_flow_saddle", topic_mode: "flow_line",
                title: "Flow Line: F(γ(t)) = [x₀·e^(2t); y₀·e^(-t); t] — Седловая линия тока в 3D и 2D",
                full_formula: "[x0*e^2t; y0*e^(-t); t]",
                x_expr: "x0 * e^(2*t)", y_expr: "y0 * e^(-t)", z_expr: "t",
                f_expr: "x^2 + y^2", u_expr: "2*x", v_expr: "-y", w_expr: "1",
                auto_field: true, use_rk4: false,
                x0: 0.45, y0: 1.35, t_val: 0.55, t_min: -1.2, t_max: 1.2,
                build_stage: 4, progressive_draw: true,
                show_2d_field: true, show_3d_field: true, show_curtain: true,
                show_bundle: true, show_velocity: true, show_floor_curve: true,
                show_surface: false, show_path_vectors: true, show_integrand_chart: true,
                split_2d: true, anim_mode: "none", problem_solution: null,
                status: "🌊 Flow Line: γ'(t) = F(γ(t)), где γ(t) = [x₀·e^(2t); y₀·e^(-t)] и F = [2x, -y, 1]"
              },
              preset_flow_spiral: {
                preset_id: "preset_flow_spiral", topic_mode: "flow_line",
                title: "Flow Line: Спиральная линия тока γ'(t) = [-0.35x - 2y, 2x - 0.35y, 1]",
                full_formula: "[e^(-0.35*t)*(x0*cos(2*t) - y0*sin(2*t)); e^(-0.35*t)*(x0*sin(2*t) + y0*cos(2*t)); t]",
                x_expr: "e^(-0.35*t)*(x0*cos(2*t) - y0*sin(2*t))",
                y_expr: "e^(-0.35*t)*(x0*sin(2*t) + y0*cos(2*t))",
                z_expr: "t", f_expr: "x^2 + y^2",
                u_expr: "-0.35*x - 2*y", v_expr: "2*x - 0.35*y", w_expr: "1",
                auto_field: false, use_rk4: false,
                x0: 1.60, y0: 1.10, t_val: 1.60, t_min: -0.6, t_max: 3.2,
                build_stage: 4, progressive_draw: true,
                show_2d_field: true, show_3d_field: true, show_curtain: true,
                show_bundle: true, show_velocity: true, show_floor_curve: true,
                show_surface: false, show_path_vectors: true, show_integrand_chart: true,
                split_2d: true, anim_mode: "none", problem_solution: null,
                status: "🌀 Спиральная линия тока: в каждой точке вектор скорости γ'(t) равен полю F(γ(t))"
              },
              preset_path_helix: {
                preset_id: "preset_path_helix", topic_mode: "path",
                title: "Path γ(t): Винтовая траектория γ(t) = [1.5·cos(t); 1.5·sin(t); 0.45·t] и длина дуги s(t)",
                full_formula: "[1.5*cos(t); 1.5*sin(t); 0.45*t]",
                x_expr: "1.5 * cos(t)", y_expr: "1.5 * sin(t)", z_expr: "0.45 * t",
                f_expr: "1", u_expr: "-y", v_expr: "x", w_expr: "0.45",
                auto_field: false, use_rk4: false,
                x0: 1.50, y0: 0.00, t_val: 3.80, t_min: 0.0, t_max: 6.2832,
                build_stage: 4, progressive_draw: true,
                show_2d_field: false, show_3d_field: false, show_curtain: true,
                show_bundle: false, show_velocity: true, show_floor_curve: true,
                show_surface: false, show_path_vectors: true, show_integrand_chart: true,
                split_2d: true, anim_mode: "none", problem_solution: null,
                status: "🛤️ Path γ(t): исследование пути, касательного вектора скорости γ'(t) и длины дуги L = ∫ ‖γ'(t)‖ dt"
              },
              preset_path_twisted: {
                preset_id: "preset_path_twisted", topic_mode: "path",
                title: "Path γ(t): Кубическо-параболический 3D путь γ(t) = [t; 0.7·t² - 1; 0.35·t³]",
                full_formula: "[t; 0.7*t^2 - 1; 0.35*t^3]",
                x_expr: "t", y_expr: "0.7 * t^2 - 1", z_expr: "0.35 * t^3",
                f_expr: "1 + x^2", u_expr: "1", v_expr: "1.4*x", w_expr: "1.05*x^2",
                auto_field: false, use_rk4: false,
                x0: 0.0, y0: -1.0, t_val: 1.10, t_min: -1.8, t_max: 1.8,
                build_stage: 4, progressive_draw: true,
                show_2d_field: false, show_3d_field: false, show_curtain: true,
                show_bundle: false, show_velocity: true, show_floor_curve: true,
                show_surface: false, show_path_vectors: true, show_integrand_chart: true,
                split_2d: true, anim_mode: "none", problem_solution: null,
                status: "🛤️ 3D путь γ(t) = [t, 0.7t²-1, 0.35t³]: тень на плоскости z=0 и подъём в 3D"
              },
              preset_path_int_circle: {
                preset_id: "preset_path_int_circle", topic_mode: "path_integral",
                title: "Path Integral ∫_γ f ds: Забор Римана f(x,y) = 1.2 + 0.4·x² + 0.6·y вдоль дуги окружности",
                full_formula: "[1.6*cos(t); 1.6*sin(t); 1.2 + 0.4*x^2 + 0.6*y]",
                x_expr: "1.6 * cos(t)", y_expr: "1.6 * sin(t)", z_expr: "1.2 + 0.4*x^2 + 0.6*y",
                f_expr: "1.2 + 0.4*x^2 + 0.6*y", u_expr: "-y", v_expr: "x", w_expr: "0",
                auto_field: false, use_rk4: false,
                x0: 1.6, y0: 0.0, t_val: 2.40, t_min: 0.0, t_max: 3.1416,
                build_stage: 4, progressive_draw: true,
                show_2d_field: false, show_3d_field: false, show_curtain: true,
                show_bundle: false, show_velocity: true, show_floor_curve: true,
                show_surface: true, show_path_vectors: true, show_integrand_chart: true,
                split_2d: true, anim_mode: "none", problem_solution: null,
                status: "🧱 Path Integral ∫_γ f(x,y) ds = ∫ f(γ(t))·‖γ'(t)‖ dt — площадь криволинейного забора под z = f(x,y)"
              },
              preset_path_int_parabola: {
                preset_id: "preset_path_int_parabola", topic_mode: "path_integral",
                title: "Path Integral ∫_γ f ds: Интеграл от f(x,y) = 0.8 + 0.5·x² + 0.4·y² вдоль параболы y = 0.5·x² - 1",
                full_formula: "[t; 0.5*t^2 - 1; 0.8 + 0.5*x^2 + 0.4*y^2]",
                x_expr: "t", y_expr: "0.5 * t^2 - 1", z_expr: "0.8 + 0.5*x^2 + 0.4*y^2",
                f_expr: "0.8 + 0.5*x^2 + 0.4*y^2", u_expr: "1", v_expr: "x", w_expr: "0",
                auto_field: false, use_rk4: false,
                x0: -1.6, y0: 0.28, t_val: 0.85, t_min: -1.6, t_max: 1.6,
                build_stage: 4, progressive_draw: true,
                show_2d_field: false, show_3d_field: false, show_curtain: true,
                show_bundle: false, show_velocity: true, show_floor_curve: true,
                show_surface: true, show_path_vectors: true, show_integrand_chart: true,
                split_2d: true, anim_mode: "none", problem_solution: null,
                status: "🧱 Path Integral: столбики Римана f(γ(t_k))·Δs_k вдоль параболического пути γ(t)"
              },
              preset_line_int_vortex: {
                preset_id: "preset_line_int_vortex", topic_mode: "line_integral",
                title: "Line Integral ∫_γ F·dγ: Интеграл вихревого поля F = [-y, x, 0] вдоль окружности r = 1.5",
                full_formula: "[1.5*cos(t); 1.5*sin(t); 0]",
                x_expr: "1.5 * cos(t)", y_expr: "1.5 * sin(t)", z_expr: "0",
                f_expr: "x^2 + y^2", u_expr: "-y", v_expr: "x", w_expr: "0",
                auto_field: false, use_rk4: false,
                x0: 1.5, y0: 0.0, t_val: 4.20, t_min: 0.0, t_max: 6.2832,
                build_stage: 4, progressive_draw: true,
                show_2d_field: true, show_3d_field: false, show_curtain: true,
                show_bundle: false, show_velocity: true, show_floor_curve: true,
                show_surface: false, show_path_vectors: true, show_integrand_chart: true,
                split_2d: true, anim_mode: "none", problem_solution: null,
                status: "🧭 Line Integral ∫_γ F·dγ = ∫ (P dx + Q dy): поле F = [-y, x] сонаправлено с γ'(t), вклад везде > 0"
              },
              preset_line_int_3d: {
                preset_id: "preset_line_int_3d", topic_mode: "line_integral",
                title: "Line Integral 3D ∫_γ F·dγ: Поле F = [y, z, x] вдоль винтовой линии γ(t) = [1.4cos t, 1.4sin t, 0.4t]",
                full_formula: "[1.4*cos(t); 1.4*sin(t); 0.4*t]",
                x_expr: "1.4 * cos(t)", y_expr: "1.4 * sin(t)", z_expr: "0.4 * t",
                f_expr: "x + y + z", u_expr: "y", v_expr: "z", w_expr: "x",
                auto_field: false, use_rk4: false,
                x0: 1.4, y0: 0.0, t_val: 3.60, t_min: 0.0, t_max: 6.2832,
                build_stage: 4, progressive_draw: true,
                show_2d_field: true, show_3d_field: true, show_curtain: true,
                show_bundle: false, show_velocity: true, show_floor_curve: true,
                show_surface: false, show_path_vectors: true, show_integrand_chart: true,
                split_2d: true, anim_mode: "none", problem_solution: null,
                status: "🧭 3D Line Integral ∫_γ (P dx + Q dy + R dz): зелёные участки F·γ' > 0, красные F·γ' < 0"
              },
              preset_work_parabola: {
                preset_id: "preset_work_parabola", topic_mode: "work",
                title: "Work W = ∫_γ F·dr: Работа силы F = [y + 0.5x, x², 0.4] вдоль пути γ(t) = [t, 0.6t² - 0.8, 0.4t]",
                full_formula: "[t; 0.6*t^2 - 0.8; 0.4*t]",
                x_expr: "t", y_expr: "0.6 * t^2 - 0.8", z_expr: "0.4 * t",
                f_expr: "x*y", u_expr: "y + 0.5*x", v_expr: "x^2", w_expr: "0.4",
                auto_field: false, use_rk4: false,
                x0: -1.2, y0: 0.06, t_val: 0.90, t_min: -1.2, t_max: 1.6,
                build_stage: 4, progressive_draw: true,
                show_2d_field: true, show_3d_field: true, show_curtain: true,
                show_bundle: false, show_velocity: true, show_floor_curve: true,
                show_surface: false, show_path_vectors: true, show_integrand_chart: true,
                split_2d: true, anim_mode: "none", problem_solution: null,
                status: "⚡ Work W = ∫_γ F·dr: разложение силы F на касательную F_∥ (совершает работу) и нормальную F_⊥ (работа = 0)"
              },
              preset_work_mixed: {
                preset_id: "preset_work_mixed", topic_mode: "work",
                title: "Work W = ∫_γ F·dr: Знакопеременная работа седлового поля F = [x, -y, 0] вдоль полуокружности",
                full_formula: "[1.6*cos(t); 1.6*sin(t); 0]",
                x_expr: "1.6 * cos(t)", y_expr: "1.6 * sin(t)", z_expr: "0",
                f_expr: "0.5*(x^2 - y^2)", u_expr: "x", v_expr: "-y", w_expr: "0",
                auto_field: false, use_rk4: false,
                x0: 1.6, y0: 0.0, t_val: 2.10, t_min: 0.0, t_max: 3.1416,
                build_stage: 4, progressive_draw: true,
                show_2d_field: true, show_3d_field: false, show_curtain: true,
                show_bundle: false, show_velocity: true, show_floor_curve: true,
                show_surface: false, show_path_vectors: true, show_integrand_chart: true,
                split_2d: true, anim_mode: "none", problem_solution: null,
                status: "⚡ Знакопеременная работа: сначала сила тормозит частицу (dW < 0, красный), затем разгоняет (dW > 0)"
              }
            };

            dom.apiKey.value = model.get("api_key") || "";
            dom.apiKey.addEventListener("change", () => {
              model.set("api_key", dom.apiKey.value.trim());
              model.save_changes();
            });

            function syncSliderThumbsOnly() {
              const tMin = Number(state.t_min ?? -1.2);
              const tMax = Number(state.t_max ?? 1.2);
              dom.slT.min = tMin.toFixed(3);
              dom.slT.max = tMax.toFixed(3);
              dom.slT.step = (Math.max(0.05, tMax - tMin) / 220).toFixed(4);
              dom.slT.value = Number(state.t_val ?? tMax);

              dom.tMinInp.value = Number(tMin.toFixed(2));
              dom.tMaxInp.value = Number(tMax.toFixed(2));

              dom.slX0.value = Number(state.x0 ?? 0.45);
              dom.slY0.value = Number(state.y0 ?? 1.35);

              dom.valT.textContent = Number(state.t_val ?? 0.55).toFixed(2);
              dom.valTspan.textContent = `[${tMin.toFixed(1)}, ${tMax.toFixed(1)}]`;
              dom.valX0.textContent = Number(state.x0 ?? 0.45).toFixed(2);
              dom.valY0.textContent = Number(state.y0 ?? 1.35).toFixed(2);
            }

            function syncControlsFromState() {
              const topic = state.topic_mode || "flow_line";
              const meta = TOPIC_META[topic] || TOPIC_META.flow_line;

              dom.modeBadge.textContent = meta.badge;
              dom.modeBadge.style.background = meta.color;
              dom.modeHeader.innerHTML = `<b>${meta.name}:</b> <code style="background:#f1f5f9;padding:2px 6px;border-radius:5px;font-size:12.5px;">${meta.formula}</code>`;

              dom.topicTabs.forEach((tab) => {
                tab.classList.toggle("active", tab.dataset.topic === topic);
              });

              if (state.preset_id && dom.preset.value !== state.preset_id) {
                dom.preset.value = state.preset_id;
              }
              dom.xExpr.value = state.x_expr || "x0 * e^(2*t)";
              dom.yExpr.value = state.y_expr || "y0 * e^(-t)";
              dom.zExpr.value = state.z_expr ?? "t";
              dom.fExpr.value = state.f_expr || "x^2 + y^2";
              dom.uExpr.value = state.u_expr || "2*x";
              dom.vExpr.value = state.v_expr || "-y";
              dom.wExpr.value = state.w_expr ?? "1";
              dom.autoField.checked = !!state.auto_field;
              dom.useRk4.checked = !!state.use_rk4;
              dom.progDraw.checked = state.progressive_draw !== false;
              dom.nlInput.value = state.full_formula || `[${dom.xExpr.value}; ${dom.yExpr.value}; ${dom.zExpr.value}]`;

              const stage = Number(state.build_stage || 4);
              dom.stageBtns.forEach((b) => {
                b.classList.toggle("active", Number(b.dataset.stage) === stage);
              });

              const setChip = (chip, on) => chip && chip.classList.toggle("active", !!on);
              setChip(dom.chipCurtain, state.show_curtain);
              setChip(dom.chipFloorCurve, state.show_floor_curve);
              setChip(dom.chipVelocity, state.show_velocity);
              setChip(dom.chipPathVectors, state.show_path_vectors !== false);
              setChip(dom.chip2dField, state.show_2d_field);
              setChip(dom.chip3dField, state.show_3d_field);
              setChip(dom.chipBundle, state.show_bundle);
              setChip(dom.chipSurface, state.show_surface);
              setChip(dom.chipIntegrand, state.show_integrand_chart !== false);
              setChip(dom.chip2d, state.split_2d !== false);

              const mode = state.anim_mode || "none";
              const isBuilding = mode === "build" || mode === "t";
              dom.buildPlay.classList.toggle("playing", isBuilding);
              dom.buildPlay.textContent = isBuilding
                ? "⏸ Пауза построения"
                : "🎬 Анимация построения с нуля (Play)";
              dom.playT.classList.toggle("playing", isBuilding);
              dom.playT.textContent = isBuilding ? "⏸" : "▶";
              dom.playX0.classList.toggle("playing", mode === "x0");
              dom.playX0.textContent = mode === "x0" ? "⏸" : "▶";
              dom.playY0.classList.toggle("playing", mode === "y0");
              dom.playY0.textContent = mode === "y0" ? "⏸" : "▶";
              dom.playOrbit.classList.toggle("playing", mode === "orbit");
              dom.playOrbit.textContent = mode === "orbit" ? "⏸" : "🔄";

              dom.title.textContent = state.title || `${meta.name}: [${dom.xExpr.value}; ${dom.yExpr.value}; ${dom.zExpr.value}]`;
              dom.status.textContent = state.status || "⚡ Готово";

              // Панель разбора задачи со скриншота / AI
              if (state.problem_solution && state.problem_solution.problem_statement) {
                const sol = state.problem_solution;
                dom.solPanel.classList.add("visible");
                dom.solStatement.textContent = "📘 Условие задачи: " + sol.problem_statement;
                dom.solS1.textContent = sol.step1_param || "";
                dom.solS2.textContent = sol.step2_deriv || "";
                dom.solS3.textContent = sol.step3_integrand || "";
                dom.solS4.textContent = sol.step4_answer || "";
              } else {
                dom.solPanel.classList.remove("visible");
              }

              syncSliderThumbsOnly();
              updateAnimationLoop();
            }

            // =========================================================================
            // 60 FPS ДВИЖОК ПОШАГОВОЙ АНИМАЦИИ ПОСТРОЕНИЯ ГРАФИКА
            // =========================================================================
            function updateAnimationLoop() {
              const mode = state.anim_mode || "none";
              if (mode === "none") {
                if (animRaf) {
                  cancelAnimationFrame(animRaf);
                  animRaf = null;
                }
                return;
              }
              if (animRaf) return;
              lastFrameTs = performance.now();

              function stepAnim(now) {
                const curMode = state.anim_mode || "none";
                if (curMode === "none") {
                  animRaf = null;
                  return;
                }
                const dt = Math.min(0.05, (now - lastFrameTs) / 1000);
                lastFrameTs = now;
                const spd = parseFloat(dom.animSpeed.value) || 1.0;

                if (!userDraggingSlider) {
                  const tMin = Number(state.t_min ?? -1.2);
                  const tMax = Number(state.t_max ?? 1.2);
                  const span = Math.max(0.1, tMax - tMin);

                  if (curMode === "build" || curMode === "t") {
                    // Плавное наращивание параметра t от t_min до t_max (рисование графика вживую!)
                    let nextT = Number(state.t_val ?? tMin) + dt * span * 0.28 * spd;
                    if (nextT > tMax) {
                      nextT = tMin + 0.02 * span;
                    }
                    state.t_val = nextT;
                  } else if (curMode === "x0") {
                    animPhase += dt * 1.2 * spd;
                    state.x0 = 1.45 * Math.sin(animPhase);
                  } else if (curMode === "y0") {
                    animPhase += dt * 1.2 * spd;
                    state.y0 = 1.45 * Math.sin(animPhase);
                  } else if (curMode === "orbit") {
                    animPhase += dt * 1.1 * spd;
                    state.x0 = 1.25 * Math.cos(animPhase);
                    state.y0 = 1.25 * Math.sin(animPhase);
                  }
                  syncSliderThumbsOnly();
                  renderPlot();
                }
                animRaf = requestAnimationFrame(stepAnim);
              }
              animRaf = requestAnimationFrame(stepAnim);
            }

            // Применение этапов построения (Шаг 1 -> Шаг 2 -> Шаг 3 -> Шаг 4)
            function applyBuildStage(stageNum) {
              state.build_stage = stageNum;
              if (stageNum === 1) {
                state.show_floor_curve = true;
                state.show_curtain = false;
                state.show_velocity = false;
                state.show_path_vectors = false;
                state.show_2d_field = false;
                state.show_3d_field = false;
                state.status = "🏗️ Этап 1 из 4: Строим плоскую траекторию γ(t) = [x(t), y(t)] на базовой плоскости z = 0";
              } else if (stageNum === 2) {
                state.show_floor_curve = true;
                state.show_curtain = true;
                state.show_velocity = true;
                state.show_path_vectors = false;
                state.show_2d_field = false;
                state.show_3d_field = false;
                state.status = "🏗️ Этап 2 из 4: Поднимаем кривую в 3D [x(t), y(t), z(t)] и строим вектор скорости γ'(t)";
              } else if (stageNum === 3) {
                state.show_floor_curve = true;
                state.show_curtain = true;
                state.show_velocity = true;
                state.show_path_vectors = true;
                state.show_2d_field = state.topic_mode !== "path" && state.topic_mode !== "path_integral";
                state.show_3d_field = state.topic_mode === "flow_line" || state.topic_mode === "line_integral" || state.topic_mode === "work";
                state.show_surface = state.topic_mode === "path_integral";
                state.status = "🏗️ Этап 3 из 4: Накладываем векторное поле F(x,y,z) / скалярную функцию высоты f(x,y,z)";
              } else {
                state.show_floor_curve = true;
                state.show_curtain = true;
                state.show_velocity = true;
                state.show_path_vectors = true;
                state.show_2d_field = state.topic_mode !== "path" && state.topic_mode !== "path_integral";
                state.show_3d_field = state.topic_mode === "flow_line";
                state.show_surface = state.topic_mode === "path_integral";
                state.show_integrand_chart = true;
                state.status = "🏗️ Этап 4 из 4: Полная картина — накопление интеграла, забор Римана и разложение векторов";
              }
              syncControlsFromState();
              renderPlot();
            }

            dom.stageBtns.forEach((btn) => {
              btn.addEventListener("click", () => {
                applyBuildStage(Number(btn.dataset.stage || 4));
              });
            });

            dom.buildPlay.addEventListener("click", () => {
              if (state.anim_mode === "build" || state.anim_mode === "t") {
                state.anim_mode = "none";
              } else {
                const tMin = Number(state.t_min ?? -1.2);
                const tMax = Number(state.t_max ?? 1.2);
                if (state.t_val >= tMax - 0.05 * (tMax - tMin)) {
                  state.t_val = tMin;
                }
                state.progressive_draw = true;
                state.anim_mode = "build";
              }
              syncControlsFromState();
            });

            dom.progDraw.addEventListener("change", () => {
              state.progressive_draw = dom.progDraw.checked;
              renderPlot();
            });

            // Переключение 5 вкладок тем
            dom.topicTabs.forEach((tab) => {
              tab.addEventListener("click", () => {
                const newTopic = tab.dataset.topic;
                state.topic_mode = newTopic;
                if (newTopic === "path") {
                  state.show_2d_field = false;
                  state.show_3d_field = false;
                  state.show_bundle = false;
                  state.show_surface = false;
                  state.show_curtain = true;
                  state.show_velocity = true;
                } else if (newTopic === "flow_line") {
                  state.show_2d_field = true;
                  state.show_3d_field = true;
                  state.show_bundle = true;
                  state.show_surface = false;
                  state.show_curtain = true;
                } else if (newTopic === "path_integral") {
                  state.show_2d_field = false;
                  state.show_3d_field = false;
                  state.show_bundle = false;
                  state.show_surface = true;
                  state.show_curtain = true;
                  state.show_path_vectors = true;
                } else if (newTopic === "line_integral" || newTopic === "work") {
                  state.show_2d_field = true;
                  state.show_3d_field = false;
                  state.show_bundle = false;
                  state.show_surface = false;
                  state.show_curtain = true;
                  state.show_path_vectors = true;
                  state.show_velocity = true;
                }
                state.status = `✨ Выбрана тема: ${(TOPIC_META[newTopic] || {}).name || newTopic}`;
                syncControlsFromState();
                renderPlot();
              });
            });

            // =========================================================================
            // ОБРАБОТКА СКРИНШОТА ЗАДАЧИ (CTRL+V / DRAG & DROP / ВЫБОР ФАЙЛА)
            // =========================================================================
            function loadScreenshotFile(file) {
              if (!file || !file.type.startsWith("image/")) return;
              const reader = new FileReader();
              reader.onload = (ev) => {
                pendingScreenshotB64 = String(ev.target.result || "");
                pendingScreenshotMime = file.type || "image/png";
                dom.snapImg.src = pendingScreenshotB64;
                dom.snapImg.style.display = "block";
                dom.snapPlaceholder.style.display = "none";
                dom.snapDrawer.classList.add("open");
                dom.status.textContent = "📸 Скриншот загружен! Нажмите «🚀 Распознать и построить график»";
              };
              reader.readAsDataURL(file);
            }

            dom.snapToggleBtn.addEventListener("click", () => {
              dom.snapDrawer.classList.toggle("open");
            });
            dom.snapCloseBtn.addEventListener("click", () => {
              dom.snapDrawer.classList.remove("open");
            });
            dom.solHideBtn.addEventListener("click", () => {
              dom.solPanel.classList.remove("visible");
            });
            dom.snapDropzone.addEventListener("click", () => {
              dom.snapFile.click();
            });
            dom.snapFile.addEventListener("change", () => {
              if (dom.snapFile.files && dom.snapFile.files[0]) {
                loadScreenshotFile(dom.snapFile.files[0]);
              }
            });
            dom.snapDropzone.addEventListener("dragover", (e) => {
              e.preventDefault();
              dom.snapDropzone.style.borderColor = "#db2777";
            });
            dom.snapDropzone.addEventListener("dragleave", () => {
              dom.snapDropzone.style.borderColor = "#d8b4fe";
            });
            dom.snapDropzone.addEventListener("drop", (e) => {
              e.preventDefault();
              dom.snapDropzone.style.borderColor = "#d8b4fe";
              if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
                loadScreenshotFile(e.dataTransfer.files[0]);
              }
            });

            // Глобальный перехват Ctrl+V для мгновенной вставки скриншота задачи
            window.addEventListener("paste", (e) => {
              const items = (e.clipboardData || window.clipboardData || {}).items;
              if (!items) return;
              for (let i = 0; i < items.length; i++) {
                if (items[i].type && items[i].type.indexOf("image") !== -1) {
                  const blob = items[i].getAsFile();
                  if (blob) {
                    loadScreenshotFile(blob);
                    e.preventDefault();
                    break;
                  }
                }
              }
            });

            dom.snapSolveBtn.addEventListener("click", () => {
              if (!pendingScreenshotB64) {
                dom.status.textContent = "⚠️ Сначала вставьте скриншот (Ctrl+V) или выберите файл картинки";
                return;
              }
              dom.status.textContent = "🤖 Gemini Vision читает скриншот задачи и строит 3D/2D модель...";
              sendToPython(dom.snapNote.value.trim(), true, "", pendingScreenshotB64, pendingScreenshotMime);
            });

            // Быстрый клиентский парсер формулы [x(t); y(t); z(t)]
            function applyQuickInputCommand(rawStr) {
              const s = String(rawStr || "").trim();
              if (!s) return;
              const br = s.match(/\[\s*([^\]]+)\s*\]/);
              let inner = br ? br[1] : (s.includes(";") ? s.replace(/^.*?=\s*/, "") : "");
              if (inner) {
                const sep = inner.includes(";") ? ";" : ",";
                const parts = inner.split(sep).map(p => p.trim()).filter(Boolean);
                if (parts.length >= 2) {
                  state.x_expr = parts[0];
                  state.y_expr = parts[1];
                  state.z_expr = parts[2] || "0";
                  state.full_formula = `[${state.x_expr}; ${state.y_expr}; ${state.z_expr}]`;
                  if (state.topic_mode === "flow_line" && state.auto_field) {
                    const uInf = inferSymbolicVelocity(state.x_expr, "x");
                    const vInf = inferSymbolicVelocity(state.y_expr, "y");
                    const wInf = inferSymbolicVelocity(state.z_expr, "z");
                    if (uInf) state.u_expr = uInf;
                    if (vInf) state.v_expr = vInf;
                    if (wInf) state.w_expr = wInf;
                  }
                  state.title = `γ(t) = [${state.x_expr}; ${state.y_expr}; ${state.z_expr}]`;
                  state.status = `✅ Построен график для γ(t) = ${state.full_formula}`;
                  syncControlsFromState();
                  renderPlot();
                }
              }
            }

            function sendToPython(cmdText, useAi = false, presetId = "", imgB64 = "", imgMime = "image/png") {
              if (presetId && JS_PRESETS[presetId]) {
                state = JSON.parse(JSON.stringify(JS_PRESETS[presetId]));
                syncControlsFromState();
                renderPlot();
              } else if (cmdText && !useAi && !imgB64) {
                applyQuickInputCommand(cmdText);
              }
              const seq = (model.get("cmd_seq") || 0) + 1;
              model.set("api_key", dom.apiKey.value.trim());
              model.set("cmd_request", {
                seq,
                command: cmdText,
                use_ai: useAi,
                preset_id: presetId,
                image_b64: imgB64,
                image_mime: imgMime,
                current_state: state,
              });
              model.set("cmd_seq", seq);
              model.save_changes();
            }

            model.on("change:state_json", () => {
              try {
                const next = JSON.parse(model.get("state_json") || "{}");
                isApplyingModelUpdate = true;
                state = next;
                syncControlsFromState();
                renderPlot();
                isApplyingModelUpdate = false;
              } catch (e) {}
            });

            dom.nlRun.addEventListener("click", () => {
              const txt = dom.nlInput.value.trim();
              if (txt) sendToPython(txt, false, "");
            });
            dom.nlInput.addEventListener("keydown", (e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                dom.nlRun.click();
              }
            });
            dom.nlAi.addEventListener("click", () => {
              const txt = dom.nlInput.value.trim() || "покажи пример вычисления работы поля вдоль кривой";
              dom.status.textContent = "🤖 Gemini 2.5 Flash решает задачу и настраивает 3D/2D график...";
              sendToPython(txt, true, "");
            });
            dom.preset.addEventListener("change", () => {
              sendToPython("", false, dom.preset.value);
            });

            function applyComponentInputs() {
              if (isApplyingModelUpdate) return;
              state.x_expr = dom.xExpr.value.trim() || "t";
              state.y_expr = dom.yExpr.value.trim() || "t";
              state.z_expr = dom.zExpr.value.trim() || "0";
              state.f_expr = dom.fExpr.value.trim() || "1";
              state.auto_field = dom.autoField.checked;
              state.use_rk4 = dom.useRk4.checked;

              if (state.auto_field && state.topic_mode === "flow_line") {
                const uInf = inferSymbolicVelocity(state.x_expr, "x");
                const vInf = inferSymbolicVelocity(state.y_expr, "y");
                const wInf = inferSymbolicVelocity(state.z_expr, "z");
                if (uInf) { state.u_expr = uInf; dom.uExpr.value = uInf; }
                if (vInf) { state.v_expr = vInf; dom.vExpr.value = vInf; }
                if (wInf) { state.w_expr = wInf; dom.wExpr.value = wInf; }
              } else {
                state.u_expr = dom.uExpr.value.trim() || "0";
                state.v_expr = dom.vExpr.value.trim() || "0";
                state.w_expr = dom.wExpr.value.trim() || "0";
              }

              state.full_formula = `[${state.x_expr}; ${state.y_expr}; ${state.z_expr}]`;
              dom.nlInput.value = state.full_formula;
              state.status = `⚡ Обновлено: γ(t)=${state.full_formula}, F=[${state.u_expr}, ${state.v_expr}, ${state.w_expr}], f=${state.f_expr}`;
              renderPlot();
            }

            [dom.xExpr, dom.yExpr, dom.zExpr, dom.fExpr, dom.uExpr, dom.vExpr, dom.wExpr].forEach((inp) => {
              inp.addEventListener("change", applyComponentInputs);
              inp.addEventListener("keydown", (e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  applyComponentInputs();
                }
              });
            });
            dom.uExpr.addEventListener("input", () => { dom.autoField.checked = false; state.auto_field = false; });
            dom.vExpr.addEventListener("input", () => { dom.autoField.checked = false; state.auto_field = false; });
            dom.wExpr.addEventListener("input", () => { dom.autoField.checked = false; state.auto_field = false; });
            dom.autoField.addEventListener("change", applyComponentInputs);
            dom.useRk4.addEventListener("change", () => {
              state.use_rk4 = dom.useRk4.checked;
              if (state.use_rk4) {
                state.auto_field = false;
                dom.autoField.checked = false;
              }
              renderPlot();
            });

            // Ползунки и пределы интегрирования
            window.addEventListener("pointerup", () => {
              userDraggingSlider = false;
            });
            [
              [dom.slT, "t_val"],
              [dom.slX0, "x0"],
              [dom.slY0, "y0"],
            ].forEach(([sl, key]) => {
              sl.addEventListener("pointerdown", () => { userDraggingSlider = true; });
              sl.addEventListener("pointerup", () => { userDraggingSlider = false; });
              sl.addEventListener("input", () => {
                state[key] = parseFloat(sl.value);
                syncSliderThumbsOnly();
                renderPlot();
              });
            });

            function applyTBounds() {
              let a = parseFloat(dom.tMinInp.value);
              let b = parseFloat(dom.tMaxInp.value);
              if (isNaN(a)) a = -1.2;
              if (isNaN(b)) b = 1.2;
              if (b <= a + 0.05) b = a + 0.5;
              state.t_min = a;
              state.t_max = b;
              if (state.t_val < a) state.t_val = a;
              if (state.t_val > b) state.t_val = b;
              syncSliderThumbsOnly();
              renderPlot();
            }
            dom.tMinInp.addEventListener("change", applyTBounds);
            dom.tMaxInp.addEventListener("change", applyTBounds);

            function toggleAnim(mode) {
              state.anim_mode = state.anim_mode === mode ? "none" : mode;
              syncControlsFromState();
            }
            dom.playT.addEventListener("click", () => toggleAnim("build"));
            dom.playX0.addEventListener("click", () => toggleAnim("x0"));
            dom.playY0.addEventListener("click", () => toggleAnim("y0"));
            dom.playOrbit.addEventListener("click", () => toggleAnim("orbit"));

            [
              [dom.chipCurtain, "show_curtain"],
              [dom.chipFloorCurve, "show_floor_curve"],
              [dom.chipVelocity, "show_velocity"],
              [dom.chipPathVectors, "show_path_vectors"],
              [dom.chip2dField, "show_2d_field"],
              [dom.chip3dField, "show_3d_field"],
              [dom.chipBundle, "show_bundle"],
              [dom.chipSurface, "show_surface"],
              [dom.chipIntegrand, "show_integrand_chart"],
              [dom.chip2d, "split_2d"],
            ].forEach(([chip, key]) => {
              chip.addEventListener("click", () => {
                state[key] = !state[key];
                syncControlsFromState();
                renderPlot();
              });
            });

            // Голосовое управление
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            let recognition = null;
            let isListening = false;
            if (SpeechRecognition) {
              recognition = new SpeechRecognition();
              recognition.continuous = true;
              recognition.interimResults = true;
              let debounceTimer = null;
              let lastSpeech = "";

              const runSpeech = (txt) => {
                const clean = String(txt || "").trim();
                if (!clean || clean.toLowerCase() === lastSpeech.toLowerCase()) return;
                lastSpeech = clean;
                dom.nlInput.value = clean;
                dom.voiceLive.textContent = `🎙️ «${clean}»`;
                sendToPython(clean, false, "");
              };

              recognition.onresult = (ev) => {
                let interim = "", finalCmd = "";
                for (let i = ev.resultIndex; i < ev.results.length; ++i) {
                  const tr = ev.results[i][0].transcript;
                  if (ev.results[i].isFinal) finalCmd += tr;
                  else interim += tr;
                }
                if (finalCmd.trim()) {
                  if (debounceTimer) clearTimeout(debounceTimer);
                  runSpeech(finalCmd.trim());
                } else if (interim.trim()) {
                  dom.voiceLive.textContent = `🗣️ «${interim.trim()}...»`;
                  if (debounceTimer) clearTimeout(debounceTimer);
                  debounceTimer = setTimeout(() => runSpeech(interim.trim()), 420);
                }
              };
              recognition.onend = () => {
                if (isListening) {
                  try { recognition.start(); } catch (e) {}
                }
              };
              dom.micBtn.addEventListener("click", () => {
                isListening = !isListening;
                if (isListening) {
                  recognition.lang = dom.lang.value;
                  try { recognition.start(); } catch (e) {}
                  dom.micBtn.classList.add("active");
                  dom.micBtn.textContent = "🔴 Слушаю...";
                } else {
                  try { recognition.stop(); } catch (e) {}
                  dom.micBtn.classList.remove("active");
                  dom.micBtn.textContent = "🎙️ Голос";
                  dom.voiceLive.textContent = "";
                }
              });
            }

            // =========================================================================
            // ВЕБ-КАМЕРА: ТРЕКИНГ ЖЕСТОВ
            // =========================================================================
            let camStream = null;
            let camRaf = null;
            let camActive = false;
            let prevFrameData = null;
            let smoothCentroidX = 80;
            let smoothCentroidY = 60;
            let lastCentroidX = 80;
            let lastCentroidY = 60;
            let angVelTheta = 0;
            let angVelPhi = 0;
            let camTheta = -2.22;
            let camPhi = 0.44;
            let camDist = 2.25;
            let currentEye = { x: -1.40, y: -1.48, z: 1.08 };

            function syncSphericalFromEye(eye) {
              if (!eye) return;
              const x = Number(eye.x) || -1.40;
              const y = Number(eye.y) || -1.48;
              const z = Number(eye.z) || 1.08;
              camDist = Math.max(0.8, Math.min(6.0, Math.hypot(x, y, z)));
              camTheta = Math.atan2(y, x);
              camPhi = Math.atan2(z, Math.max(1e-4, Math.hypot(x, y)));
            }

            function applyCameraEye() {
              const cosPhi = Math.cos(camPhi);
              currentEye = {
                x: Number((camDist * Math.cos(camTheta) * cosPhi).toFixed(3)),
                y: Number((camDist * Math.sin(camTheta) * cosPhi).toFixed(3)),
                z: Number((camDist * Math.sin(camPhi)).toFixed(3)),
              };
              if (window.Plotly && dom.plot && dom.plot._fullLayout) {
                Plotly.relayout(dom.plot, {
                  "scene.camera.eye": currentEye,
                  "scene.camera.up": { x: 0, y: 0, z: 1 },
                });
              }
            }

            const procCanvas = document.createElement("canvas");
            procCanvas.width = 160;
            procCanvas.height = 120;
            const procCtx = procCanvas.getContext("2d", { willReadFrequently: true });
            const dispCtx = dom.camCanvas ? dom.camCanvas.getContext("2d") : null;

            async function startWebcam() {
              if (camActive) return;
              try {
                const stream = await navigator.mediaDevices.getUserMedia({
                  video: { width: { ideal: 320 }, height: { ideal: 240 }, facingMode: "user" },
                  audio: false,
                });
                camStream = stream;
                dom.camVideo.srcObject = stream;
                await dom.camVideo.play();
                camActive = true;
                dom.camBtn.classList.add("active");
                dom.camPip.style.display = "block";
                prevFrameData = null;
                startCamLoop();
              } catch (err) {
                dom.status.textContent = "⚠️ Доступ к камере отклонен браузером";
              }
            }

            function stopWebcam() {
              camActive = false;
              if (camRaf) {
                cancelAnimationFrame(camRaf);
                camRaf = null;
              }
              if (camStream) {
                camStream.getTracks().forEach(t => t.stop());
                camStream = null;
              }
              dom.camBtn.classList.remove("active");
              dom.camPip.style.display = "none";
            }

            dom.camBtn.addEventListener("click", () => {
              if (camActive) stopWebcam();
              else startWebcam();
            });
            dom.camCloseBtn.addEventListener("click", stopWebcam);
            dom.camResetBtn.addEventListener("click", () => {
              camTheta = -2.22; camPhi = 0.44; camDist = 2.25;
              angVelTheta = 0; angVelPhi = 0;
              applyCameraEye();
            });
            dom.camSnapBtn.addEventListener("click", () => {
              if (window.Plotly && dom.plot) {
                Plotly.downloadImage(dom.plot, { format: "png", width: 1600, height: 1000, filename: "vector_calculus_studio" });
              }
            });
            dom.camSpeed.addEventListener("input", () => {
              dom.camSpeedVal.textContent = parseFloat(dom.camSpeed.value).toFixed(1) + "x";
            });

            function startCamLoop() {
              function camStep() {
                if (!camActive) return;
                if (dom.camVideo && dom.camVideo.readyState >= 2) {
                  procCtx.save();
                  procCtx.scale(-1, 1);
                  procCtx.drawImage(dom.camVideo, -160, 0, 160, 120);
                  procCtx.restore();
                  const frame = procCtx.getImageData(0, 0, 160, 120);
                  const d = frame.data;

                  let sumX = 0, sumY = 0, totalMotion = 0;
                  if (prevFrameData) {
                    for (let y = 6; y < 114; y += 2) {
                      for (let x = 6; x < 154; x += 2) {
                        const idx = (y * 160 + x) * 4;
                        const diff = Math.abs(d[idx] - prevFrameData[idx]) +
                                     Math.abs(d[idx+1] - prevFrameData[idx+1]) +
                                     Math.abs(d[idx+2] - prevFrameData[idx+2]);
                        if (diff > 34) {
                          sumX += x * diff;
                          sumY += y * diff;
                          totalMotion += diff;
                        }
                      }
                    }
                  } else {
                    prevFrameData = new Uint8ClampedArray(d.length);
                  }
                  prevFrameData.set(d);

                  const motionDetected = totalMotion > 1700;
                  const sens = parseFloat(dom.camSpeed.value) || 1.1;
                  const target = dom.camTarget.value;

                  if (motionDetected) {
                    const rawX = sumX / totalMotion;
                    const rawY = sumY / totalMotion;
                    smoothCentroidX = smoothCentroidX * 0.68 + rawX * 0.32;
                    smoothCentroidY = smoothCentroidY * 0.68 + rawY * 0.32;
                    const dx = smoothCentroidX - lastCentroidX;
                    const dy = smoothCentroidY - lastCentroidY;
                    lastCentroidX = smoothCentroidX;
                    lastCentroidY = smoothCentroidY;

                    const normX = (smoothCentroidX - 80) / 80;
                    const normY = (smoothCentroidY - 60) / 60;

                    if (target === "orbit") {
                      if (Math.abs(dx) > 0.7) angVelTheta = Math.max(-0.05, Math.min(0.05, angVelTheta - dx * 0.0024 * sens));
                      if (Math.abs(dy) > 0.7) angVelPhi = Math.max(-0.04, Math.min(0.04, angVelPhi - dy * 0.0018 * sens));
                    } else if (target === "point") {
                      const tX0 = normX * 2.0;
                      const tY0 = -normY * 2.0;
                      state.x0 = Number((state.x0 * 0.84 + tX0 * 0.16).toFixed(2));
                      state.y0 = Number((state.y0 * 0.84 + tY0 * 0.16).toFixed(2));
                      syncSliderThumbsOnly();
                      renderPlot();
                    } else if (target === "time_t") {
                      const tMin = Number(state.t_min ?? -1.2);
                      const tMax = Number(state.t_max ?? 1.2);
                      const targetT = tMin + Math.max(0, Math.min(1, (normX + 1) * 0.5)) * (tMax - tMin);
                      state.t_val = Number((state.t_val * 0.82 + targetT * 0.18).toFixed(2));
                      syncSliderThumbsOnly();
                      renderPlot();
                    }
                  } else {
                    lastCentroidX = smoothCentroidX;
                    lastCentroidY = smoothCentroidY;
                  }

                  if (target === "orbit") {
                    camTheta += angVelTheta;
                    camPhi = Math.max(-1.38, Math.min(1.38, camPhi + angVelPhi));
                    angVelTheta *= 0.86;
                    angVelPhi *= 0.86;
                    if (Math.abs(angVelTheta) > 1e-4 || Math.abs(angVelPhi) > 1e-4) {
                      applyCameraEye();
                    }
                  }

                  if (dispCtx) {
                    dispCtx.save();
                    dispCtx.scale(-1, 1);
                    dispCtx.filter = "contrast(160%) brightness(108%) saturate(140%)";
                    dispCtx.drawImage(dom.camVideo, -240, 0, 240, 150);
                    dispCtx.restore();
                    if (motionDetected) {
                      const hx = smoothCentroidX * (240 / 160);
                      const hy = smoothCentroidY * (150 / 120);
                      dispCtx.beginPath();
                      dispCtx.arc(hx, hy, 14, 0, 2 * Math.PI);
                      dispCtx.strokeStyle = "#38bdf8";
                      dispCtx.lineWidth = 2.5;
                      dispCtx.stroke();
                    }
                  }
                }
                camRaf = requestAnimationFrame(camStep);
              }
              camRaf = requestAnimationFrame(camStep);
            }

            // =========================================================================
            // МАТЕМАТИЧЕСКОЕ ЯДРО И 3D/2D РЕНДЕР ВСЕХ 5 ТЕМ
            // =========================================================================
            let plotInitialized = false;

            function renderPlot() {
              loadPlotly().then((Plotly) => {
                const topic = state.topic_mode || "flow_line";
                const meta = TOPIC_META[topic] || TOPIC_META.flow_line;

                const xFn = compileFlowExpr(state.x_expr || "t", 0);
                const yFn = compileFlowExpr(state.y_expr || "t", 0);
                const zFn = compileFlowExpr(state.z_expr ?? "0", 0);
                const fFn = compileFlowExpr(state.f_expr || "1", 1);

                const uExplicit = compileFlowExpr(state.u_expr || "0", 0);
                const vExplicit = compileFlowExpr(state.v_expr || "0", 0);
                const wExplicit = compileFlowExpr(state.w_expr ?? "0", 0);

                const useAutoField = !!state.auto_field && topic === "flow_line" && !state.use_rk4;
                const useRk4 = !!state.use_rk4;

                const x0 = Number(state.x0 ?? 0.45);
                const y0 = Number(state.y0 ?? 1.35);
                const tMin = Number(state.t_min ?? -1.2);
                const tMax = Math.max(tMin + 0.05, Number(state.t_max ?? 1.2));
                const tStar = Math.max(tMin, Math.min(tMax, Number(state.t_val ?? tMax)));
                const progDraw = state.progressive_draw !== false;

                function evalScalarF(x, y, z, t = 0) {
                  let val = fFn(t, x0, y0, x, y, z);
                  if (!isFinite(val)) val = 0;
                  return Math.max(-15, Math.min(15, val));
                }

                function evalAnalyticPoint(t, sx0, sy0) {
                  let xv = xFn(t, sx0, sy0, sx0, sy0, t);
                  let yv = yFn(t, sx0, sy0, xv, sy0, t);
                  if (!isFinite(xv)) xv = 0;
                  if (!isFinite(yv)) yv = 0;
                  xv = Math.max(-15, Math.min(15, xv));
                  yv = Math.max(-15, Math.min(15, yv));
                  let zv = zFn(t, sx0, sy0, xv, yv, t);
                  if (topic === "path_integral" && (String(state.z_expr).trim() === "0" || String(state.z_expr).trim() === "")) {
                    zv = evalScalarF(xv, yv, 0, t);
                  }
                  if (!isFinite(zv)) zv = 0;
                  zv = Math.max(-15, Math.min(15, zv));
                  return [xv, yv, zv];
                }

                function evalAnalyticDeriv(t, sx0, sy0) {
                  const dt = 1e-4;
                  const p1 = evalAnalyticPoint(t + dt, sx0, sy0);
                  const p0 = evalAnalyticPoint(t - dt, sx0, sy0);
                  return [
                    (p1[0] - p0[0]) / (2 * dt),
                    (p1[1] - p0[1]) / (2 * dt),
                    (p1[2] - p0[2]) / (2 * dt),
                  ];
                }

                function evalVectorField(x, y, z) {
                  if (useAutoField) {
                    const p0 = evalAnalyticPoint(0, x, y);
                    if (Math.hypot(p0[0] - x, p0[1] - y) < 0.25) {
                      return evalAnalyticDeriv(0, x, y);
                    }
                  }
                  const u = uExplicit(z, x0, y0, x, y, z);
                  const v = vExplicit(z, x0, y0, x, y, z);
                  const w = wExplicit(z, x0, y0, x, y, z);
                  return [
                    isFinite(u) ? Math.max(-20, Math.min(20, u)) : 0,
                    isFinite(v) ? Math.max(-20, Math.min(20, v)) : 0,
                    isFinite(w) ? Math.max(-20, Math.min(20, w)) : 0,
                  ];
                }

                // Численный интегратор Рунге-Кутты 4-го порядка (RK4) для построения Flow Line любого поля F=[P,Q,R]
                function buildTrajectorySamples(sx0, sy0, Msteps) {
                  const pts = [];
                  if (!useRk4) {
                    for (let i = 0; i <= Msteps; i++) {
                      const ti = tMin + ((tMax - tMin) * i) / Msteps;
                      pts.push({ t: ti, p: evalAnalyticPoint(ti, sx0, sy0) });
                    }
                    return pts;
                  }
                  // Если включен RK4: интегрируем dγ/dt = F(γ) от t=0 вперед и назад
                  const dtStep = (tMax - tMin) / Msteps;
                  const tGrid = [];
                  for (let i = 0; i <= Msteps; i++) tGrid.push(tMin + i * dtStep);
                  // Находим индекс ближайший к t=0 (или началу интервала)
                  let zeroIdx = 0;
                  let bestDist = Infinity;
                  for (let i = 0; i <= Msteps; i++) {
                    if (Math.abs(tGrid[i]) < bestDist) {
                      bestDist = Math.abs(tGrid[i]);
                      zeroIdx = i;
                    }
                  }
                  const out = new Array(Msteps + 1);
                  out[zeroIdx] = [sx0, sy0, 0];

                  const rk4Step = (p, h) => {
                    const k1 = evalVectorField(p[0], p[1], p[2]);
                    const k2 = evalVectorField(p[0] + 0.5*h*k1[0], p[1] + 0.5*h*k1[1], p[2] + 0.5*h*k1[2]);
                    const k3 = evalVectorField(p[0] + 0.5*h*k2[0], p[1] + 0.5*h*k2[1], p[2] + 0.5*h*k2[2]);
                    const k4 = evalVectorField(p[0] + h*k3[0], p[1] + h*k3[1], p[2] + h*k3[2]);
                    return [
                      Math.max(-12, Math.min(12, p[0] + (h/6)*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0]))),
                      Math.max(-12, Math.min(12, p[1] + (h/6)*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1]))),
                      Math.max(-12, Math.min(12, p[2] + (h/6)*(k1[2] + 2*k2[2] + 2*k3[2] + k4[2]))),
                    ];
                  };

                  for (let i = zeroIdx + 1; i <= Msteps; i++) {
                    out[i] = rk4Step(out[i - 1], dtStep);
                  }
                  for (let i = zeroIdx - 1; i >= 0; i--) {
                    out[i] = rk4Step(out[i + 1], -dtStep);
                  }
                  for (let i = 0; i <= Msteps; i++) {
                    pts.push({ t: tGrid[i], p: out[i] });
                  }
                  return pts;
                }

                // 1. Вычисляем массив точек главной кривой и численно считаем интегралы
                const M = 140;
                const mainSamples = buildTrajectorySamples(x0, y0, M);
                const fullX = [], fullY = [], fullZ = [], fullZero = [], fullT = [];
                const actX = [], actY = [], actZ = [], actZero = [], actT = [];
                const integrandArr = [], cumIntArr = [], actIntegrandArr = [];

                let maxAbsXY = 2.4;
                let zMinBound = -0.5;
                let zMaxBound = 1.4;

                let totalIntegral = 0;
                let accumIntegral = 0;
                let totalArcLen = 0;
                let accumArcLen = 0;

                let curIdx = 0;

                for (let i = 0; i <= M; i++) {
                  const ti = mainSamples[i].t;
                  const [px, py, pz] = mainSamples[i].p;

                  // Численная производная γ'(t_i)
                  let dx_dt, dy_dt, dz_dt;
                  if (useRk4) {
                    [dx_dt, dy_dt, dz_dt] = evalVectorField(px, py, pz);
                  } else {
                    [dx_dt, dy_dt, dz_dt] = evalAnalyticDeriv(ti, x0, y0);
                  }
                  const speed2D = Math.hypot(dx_dt, dy_dt);
                  const speed3D = Math.hypot(dx_dt, dy_dt, dz_dt);
                  const fVal = evalScalarF(px, py, pz, ti);
                  const [fx, fy, fz] = evalVectorField(px, py, pz);
                  const dotProd = fx * dx_dt + fy * dy_dt + fz * dz_dt;

                  // Высота 3D точки в зависимости от темы
                  let displayZ = pz;
                  if (topic === "path_integral") {
                    displayZ = fVal;
                  }

                  // Подынтегральная функция I(t) для выбранной темы
                  let instIntegrand = speed3D;
                  if (topic === "path") {
                    instIntegrand = speed3D;
                  } else if (topic === "flow_line") {
                    instIntegrand = speed3D;
                  } else if (topic === "path_integral") {
                    // Для плоского криволинейного интеграла I рода ds = sqrt(x'^2 + y'^2) dt
                    const dsRate = (String(state.z_expr).trim() === "0" || String(state.z_expr).trim() === String(state.f_expr).trim())
                      ? speed2D
                      : speed3D;
                    instIntegrand = fVal * dsRate;
                  } else if (topic === "line_integral" || topic === "work") {
                    instIntegrand = dotProd;
                  }

                  fullX.push(px);
                  fullY.push(py);
                  fullZ.push(displayZ);
                  fullZero.push(0);
                  fullT.push(ti);
                  integrandArr.push(instIntegrand);

                  if (i > 0) {
                    const dt = fullT[i] - fullT[i - 1];
                    const dInt = 0.5 * (integrandArr[i - 1] + integrandArr[i]) * dt;
                    const prevSpd = Math.hypot(
                      (fullX[i] - fullX[i - 1]) / (dt || 1),
                      (fullY[i] - fullY[i - 1]) / (dt || 1),
                      ( (topic === "path_integral" ? 0 : (fullZ[i] - fullZ[i - 1])) ) / (dt || 1)
                    );
                    const dArc = prevSpd * dt;
                    totalIntegral += dInt;
                    totalArcLen += dArc;
                    if (ti <= tStar + 1e-6) {
                      accumIntegral += dInt;
                      accumArcLen += dArc;
                    }
                  }
                  cumIntArr.push(totalIntegral);

                  if (Math.abs(px) < 9 && Math.abs(py) < 9) {
                    maxAbsXY = Math.max(maxAbsXY, Math.abs(px) * 1.18, Math.abs(py) * 1.18);
                  }
                  if (Math.abs(displayZ) < 12) {
                    zMinBound = Math.min(zMinBound, displayZ, 0);
                    zMaxBound = Math.max(zMaxBound, displayZ, 0.8);
                  }

                  if (ti <= tStar + 1e-6) {
                    actX.push(px);
                    actY.push(py);
                    actZ.push(displayZ);
                    actZero.push(0);
                    actT.push(ti);
                    actIntegrandArr.push(instIntegrand);
                    curIdx = i;
                  }
                }

                maxAbsXY = Math.min(6.5, Math.max(2.3, maxAbsXY));
                const R = maxAbsXY;
                const zSpan = Math.max(1.5, zMaxBound - zMinBound);

                // Точка старта и текущая точка t*
                const startX = fullX[0] ?? x0;
                const startY = fullY[0] ?? y0;
                const startZ = fullZ[0] ?? 0;

                const curX = fullX[curIdx] ?? x0;
                const curY = fullY[curIdx] ?? y0;
                const curZ = fullZ[curIdx] ?? 0;

                let [velX, velY, velZ] = useRk4
                  ? evalVectorField(curX, curY, curZ)
                  : evalAnalyticDeriv(tStar, x0, y0);
                if (topic === "path_integral") velZ = 0;
                const velNorm = Math.hypot(velX, velY, velZ);

                const [fldX, fldY, fldZ] = evalVectorField(curX, curY, curZ);
                const fldNorm = Math.hypot(fldX, fldY, fldZ);
                const curFVal = evalScalarF(curX, curY, curZ, tStar);
                const curDot = fldX * velX + fldY * velY + fldZ * velZ;
                const cosTheta = (velNorm > 1e-5 && fldNorm > 1e-5)
                  ? Math.max(-1, Math.min(1, curDot / (velNorm * fldNorm)))
                  : 0;
                const thetaDeg = (Math.acos(cosTheta) * 180) / Math.PI;

                // Численный ротор curl F = ∇ × F в текущей точке (проверка потенциальности поля для Work / Line Integral)
                const eps = 1e-3;
                const [u_y1, v_y1, w_y1] = evalVectorField(curX, curY + eps, curZ);
                const [u_y0, v_y0, w_y0] = evalVectorField(curX, curY - eps, curZ);
                const [u_x1, v_x1, w_x1] = evalVectorField(curX + eps, curY, curZ);
                const [u_x0, v_x0, w_x0] = evalVectorField(curX - eps, curY, curZ);
                const curlZ = (v_x1 - v_x0) / (2 * eps) - (u_y1 - u_y0) / (2 * eps);

                // Обновляем верхний индикатор живого интеграла и длины дуги
                dom.metricMain.textContent = `${meta.integralSymbol} = ${(progDraw ? accumIntegral : totalIntegral).toFixed(3)} (полный: ${totalIntegral.toFixed(3)})`;
                dom.metricArc.textContent = `Дуга s(t) = ${(progDraw ? accumArcLen : totalArcLen).toFixed(3)}`;

                const traces = [];
                const is2D = state.split_2d !== false;
                const showIntChart = state.show_integrand_chart !== false && is2D;

                // Выбираем массив для отрисовки (прогрессивное построение до t* или вся кривая)
                const drawX = progDraw ? actX : fullX;
                const drawY = progDraw ? actY : fullY;
                const drawZ = progDraw ? actZ : fullZ;
                const drawZero = progDraw ? actZero : fullZero;

                // =================================================================
                // СЛОЙ 1: БАЗОВАЯ ПЛОСКОСТЬ z = 0 И ПОВЕРХНОСТЬ z = f(x,y)
                // =================================================================
                traces.push({
                  type: "surface",
                  x: [[-R, R], [-R, R]],
                  y: [[-R, -R], [R, R]],
                  z: [[0, 0], [0, 0]],
                  colorscale: [[0, "#f8fafc"], [1, "#e2e8f0"]],
                  showscale: false,
                  opacity: 0.40,
                  hoverinfo: "skip",
                  name: "Плоскость z = 0",
                });

                traces.push({
                  type: "scatter3d",
                  mode: "lines",
                  x: [-R, R, null, 0, 0],
                  y: [0, 0, null, -R, R],
                  z: [0, 0, null, 0, 0],
                  line: { color: "#64748b", width: 3 },
                  showlegend: false,
                  hoverinfo: "skip",
                });

                if (state.show_surface) {
                  const Ns = 32;
                  const sX = [], sY = [], sZ = [];
                  for (let i = 0; i < Ns; i++) {
                    const vy = -R + (2 * R * i) / (Ns - 1);
                    const rX = [], rY = [], rZ = [];
                    for (let j = 0; j < Ns; j++) {
                      const vx = -R + (2 * R * j) / (Ns - 1);
                      let vz = topic === "path_integral"
                        ? evalScalarF(vx, vy, 0, tStar)
                        : zFn(tStar, x0, y0, vx, vy, 0);
                      if (!isFinite(vz)) vz = 0;
                      vz = Math.max(-10, Math.min(10, vz));
                      rX.push(vx); rY.push(vy); rZ.push(vz);
                    }
                    sX.push(rX); sY.push(rY); sZ.push(rZ);
                  }
                  traces.push({
                    type: "surface",
                    x: sX, y: sY, z: sZ,
                    colorscale: [[0, "#ede9fe"], [0.5, "#c4b5fd"], [1, "#8b5cf6"]],
                    showscale: false,
                    opacity: 0.36,
                    hoverinfo: "skip",
                    name: "z = f(x,y)",
                  });
                }

                // =================================================================
                // СЛОЙ 2: ПУЧОК ТРАЕКТОРИЙ (ДЛЯ FLOW LINE)
                // =================================================================
                const bundleSeeds = [
                  [0.45, 1.4], [-0.45, 1.4], [-0.45, -1.4], [0.45, -1.4],
                  [0.22, 1.6], [-0.22, 1.6], [-0.22, -1.6], [0.22, -1.6],
                  [0.85, 0.9], [-0.85, 0.9], [-0.85, -0.9], [0.85, -0.9],
                ];
                if (state.show_bundle && topic === "flow_line") {
                  const b3dX = [], b3dY = [], b3dZ = [];
                  const bFlX = [], bFlY = [], bFlZ = [];
                  const Mb = 40;
                  for (const [sx, sy] of bundleSeeds) {
                    const bPts = buildTrajectorySamples(sx, sy, Mb);
                    for (let i = 0; i <= Mb; i++) {
                      const [bx, by, bz] = bPts[i].p;
                      if (Math.abs(bx) <= R * 1.15 && Math.abs(by) <= R * 1.15) {
                        b3dX.push(bx); b3dY.push(by); b3dZ.push(bz);
                        bFlX.push(bx); bFlY.push(by); bFlZ.push(0);
                      } else {
                        b3dX.push(null); b3dY.push(null); b3dZ.push(null);
                        bFlX.push(null); bFlY.push(null); bFlZ.push(null);
                      }
                    }
                    b3dX.push(null); b3dY.push(null); b3dZ.push(null);
                    bFlX.push(null); bFlY.push(null); bFlZ.push(null);
                  }
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: b3dX, y: b3dY, z: b3dZ,
                    line: { color: "rgba(99, 102, 241, 0.32)", width: 2.2 },
                    hoverinfo: "skip",
                  });
                  if (state.show_floor_curve) {
                    traces.push({
                      type: "scatter3d",
                      mode: "lines",
                      x: bFlX, y: bFlY, z: bFlZ,
                      line: { color: "rgba(148, 163, 184, 0.38)", width: 1.4 },
                      hoverinfo: "skip",
                    });
                  }
                }

                // =================================================================
                // СЛОЙ 3: ВЕКТОРНОЕ ПОЛЕ F В 3D И НА ПЛОСКОСТИ z=0
                // =================================================================
                if (state.show_2d_field) {
                  const vfX = [], vfY = [], vfZ = [];
                  const G = 7;
                  const step = (2 * R * 0.85) / (G - 1);
                  for (let i = 0; i < G; i++) {
                    for (let j = 0; j < G; j++) {
                      const gx = -R * 0.85 + j * step;
                      const gy = -R * 0.85 + i * step;
                      const [u, v] = evalVectorField(gx, gy, 0);
                      const mag = Math.hypot(u, v);
                      if (mag > 1e-5) {
                        const len = Math.min(step * 0.42, 0.14 + 0.12 * Math.tanh(mag * 0.4));
                        const ex = gx + (u / mag) * len;
                        const ey = gy + (v / mag) * len;
                        vfX.push(gx, ex, null);
                        vfY.push(gy, ey, null);
                        vfZ.push(0, 0, null);
                      }
                    }
                  }
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: vfX, y: vfY, z: vfZ,
                    line: { color: "rgba(13, 148, 136, 0.50)", width: 2.2 },
                    hoverinfo: "skip",
                  });
                }

                if (state.show_3d_field) {
                  const cX = [], cY = [], cZ = [], cU = [], cV = [], cW = [];
                  const G3 = 4;
                  const zLevels = [zMinBound * 0.5, 0, zMaxBound * 0.6];
                  for (const gz of zLevels) {
                    for (let i = 0; i < G3; i++) {
                      for (let j = 0; j < G3; j++) {
                        const gx = -R * 0.72 + (2 * R * 0.72 * j) / (G3 - 1);
                        const gy = -R * 0.72 + (2 * R * 0.72 * i) / (G3 - 1);
                        const [u, v, w] = evalVectorField(gx, gy, gz);
                        const norm = Math.hypot(u, v, w) || 1;
                        cX.push(gx); cY.push(gy); cZ.push(gz);
                        cU.push((u / norm) * 0.34);
                        cV.push((v / norm) * 0.34);
                        cW.push((w / norm) * 0.34);
                      }
                    }
                  }
                  traces.push({
                    type: "cone",
                    x: cX, y: cY, z: cZ,
                    u: cU, v: cV, w: cW,
                    sizemode: "absolute",
                    sizeref: 0.26,
                    anchor: "tail",
                    colorscale: [[0, "#38bdf8"], [1, "#0284c7"]],
                    showscale: false,
                    opacity: 0.50,
                    hoverinfo: "skip",
                  });
                }

                // =================================================================
                // СЛОЙ 4: ШТОРКА ПОДЪЁМА / ЗАБОР РИМАНА ВДОЛЬ КРИВОЙ γ(t)
                // =================================================================
                if (state.show_curtain && drawX.length >= 2) {
                  const curtainColors = topic === "path_integral"
                    ? [[0, "rgba(124, 58, 237, 0.25)"], [1, "rgba(219, 39, 119, 0.52)"]]
                    : (topic === "work" || topic === "line_integral")
                      ? [[0, "rgba(220, 38, 38, 0.35)"], [0.5, "rgba(250, 204, 21, 0.25)"], [1, "rgba(16, 185, 129, 0.45)"]]
                      : [[0, "rgba(59, 130, 246, 0.18)"], [1, "rgba(239, 68, 68, 0.36)"]];

                  traces.push({
                    type: "surface",
                    x: [drawX, drawX],
                    y: [drawY, drawY],
                    z: [drawZero, drawZ],
                    colorscale: curtainColors,
                    showscale: false,
                    opacity: topic === "path_integral" ? 0.55 : 0.35,
                    hoverinfo: "skip",
                  });

                  // Вертикальные столбики Римана (для Path Integral — густая сетка панелей Δs_k)
                  const pilX = [], pilY = [], pilZ = [];
                  const topBarX = [], topBarY = [], topBarZ = [];
                  const nPillars = topic === "path_integral" ? 22 : 14;
                  const stepP = Math.max(1, Math.floor(drawX.length / nPillars));
                  for (let k = 0; k < drawX.length; k += stepP) {
                    pilX.push(drawX[k], drawX[k], null);
                    pilY.push(drawY[k], drawY[k], null);
                    pilZ.push(0, drawZ[k], null);
                    if (topic === "path_integral" && k + stepP < drawX.length) {
                      // Верхняя ступенька прямоугольника Римана f(γ(t_k))
                      const kNext = Math.min(drawX.length - 1, k + stepP);
                      topBarX.push(drawX[k], drawX[kNext], drawX[kNext], null);
                      topBarY.push(drawY[k], drawY[kNext], drawY[kNext], null);
                      topBarZ.push(drawZ[k], drawZ[k], 0, null);
                    }
                  }
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: pilX, y: pilY, z: pilZ,
                    line: {
                      color: topic === "path_integral" ? "rgba(124, 58, 237, 0.75)" : "rgba(37, 99, 235, 0.52)",
                      width: topic === "path_integral" ? 3 : 2,
                      dash: topic === "path_integral" ? "solid" : "dot",
                    },
                    hoverinfo: "skip",
                  });
                  if (topBarX.length > 0) {
                    traces.push({
                      type: "scatter3d",
                      mode: "lines",
                      x: topBarX, y: topBarY, z: topBarZ,
                      line: { color: "rgba(109, 40, 217, 0.85)", width: 2.5 },
                      hoverinfo: "skip",
                    });
                  }
                }

                // =================================================================
                // СЛОЙ 5: ВЕКТОРЫ ПОЛЯ F(γ(t_k)) ВДОЛЬ САМОЙ КРИВОЙ (ДЛЯ LINE INTEGRAL & WORK)
                // =================================================================
                if (state.show_path_vectors !== false && (topic === "line_integral" || topic === "work" || topic === "flow_line")) {
                  const posVecX = [], posVecY = [], posVecZ = [];
                  const negVecX = [], negVecY = [], negVecZ = [];
                  const stepV = Math.max(1, Math.floor(drawX.length / 14));
                  for (let k = 0; k < drawX.length; k += stepV) {
                    const px = drawX[k], py = drawY[k], pz = drawZ[k];
                    const [fx, fy, fz] = evalVectorField(px, py, pz);
                    const fMag = Math.hypot(fx, fy, fz);
                    if (fMag > 1e-5) {
                      const scale = Math.min(0.55, 0.22 + 0.18 * Math.tanh(fMag * 0.35));
                      const ex = px + (fx / fMag) * scale;
                      const ey = py + (fy / fMag) * scale;
                      const ez = pz + (fz / fMag) * scale;
                      const dVal = integrandArr[k] ?? 0;
                      if (dVal >= 0) {
                        posVecX.push(px, ex, null);
                        posVecY.push(py, ey, null);
                        posVecZ.push(pz, ez, null);
                      } else {
                        negVecX.push(px, ex, null);
                        negVecY.push(py, ey, null);
                        negVecZ.push(pz, ez, null);
                      }
                    }
                  }
                  if (posVecX.length > 0) {
                    traces.push({
                      type: "scatter3d",
                      mode: "lines",
                      x: posVecX, y: posVecY, z: posVecZ,
                      line: { color: "#16a34a", width: 4 },
                      name: "F(γ(t)) где F·γ' > 0",
                      hoverinfo: "skip",
                    });
                  }
                  if (negVecX.length > 0) {
                    traces.push({
                      type: "scatter3d",
                      mode: "lines",
                      x: negVecX, y: negVecY, z: negVecZ,
                      line: { color: "#dc2626", width: 4 },
                      name: "F(γ(t)) где F·γ' < 0",
                      hoverinfo: "skip",
                    });
                  }
                }

                // =================================================================
                // СЛОЙ 6: КРИВАЯ НА ПЛОСКОСТИ z=0 И 3D ТРАЕКТОРИЯ γ(t)
                // =================================================================
                if (state.show_floor_curve) {
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: fullX, y: fullY, z: fullZero,
                    line: { color: "rgba(37, 99, 235, 0.28)", width: 2.5, dash: "dash" },
                    hoverinfo: "skip",
                  });
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: drawX, y: drawY, z: drawZero,
                    line: { color: "#2563eb", width: 5 },
                    name: "γ(t) на z=0",
                  });
                }

                // Будущая часть 3D кривой (пунктир-призрак)
                traces.push({
                  type: "scatter3d",
                  mode: "lines",
                  x: fullX, y: fullY, z: fullZ,
                  line: { color: "rgba(148, 163, 184, 0.40)", width: 3, dash: "dot" },
                  hoverinfo: "skip",
                });

                // Активно построенная 3D кривая
                traces.push({
                  type: "scatter3d",
                  mode: "lines",
                  x: drawX, y: drawY, z: drawZ,
                  line: {
                    color: (topic === "line_integral" || topic === "work")
                      ? (progDraw ? actIntegrandArr : integrandArr)
                      : drawZ,
                    colorscale: (topic === "line_integral" || topic === "work")
                      ? [[0, "#dc2626"], [0.5, "#f59e0b"], [1, "#16a34a"]]
                      : [[0, "#2563eb"], [0.5, "#10b981"], [1, "#dc2626"]],
                    width: 8,
                  },
                  name: "3D Кривая",
                });

                // =================================================================
                // СЛОЙ 7: ТОЧКА t*, СКОРОСТЬ γ'(t*), СИЛА F(γ(t*)) И ПРОЕКЦИЯ F_∥
                // =================================================================
                traces.push({
                  type: "scatter3d",
                  mode: "lines",
                  x: [curX, curX, null, curX, curX, null, curX, 0],
                  y: [curY, curY, null, curY, 0, null, curY, curY],
                  z: [0, curZ, null, 0, 0, null, 0, 0],
                  line: { color: "#0f172a", width: 3, dash: "dash" },
                  hoverinfo: "skip",
                });

                traces.push({
                  type: "scatter3d",
                  mode: "markers+text",
                  x: [startX, curX, curX],
                  y: [startY, curY, curY],
                  z: [startZ, 0, curZ],
                  marker: {
                    size: [6, 6, 8],
                    color: ["#16a34a", "#2563eb", "#dc2626"],
                    line: { width: 2, color: "#ffffff" },
                  },
                  text: [
                    `A: t=${tMin.toFixed(1)}`,
                    `γ(${tStar.toFixed(2)})`,
                    topic === "path_integral"
                      ? `f(γ(${tStar.toFixed(2)})) = ${curFVal.toFixed(2)}`
                      : `r(${tStar.toFixed(2)}) = [${curX.toFixed(2)}, ${curY.toFixed(2)}, ${curZ.toFixed(2)}]`,
                  ],
                  textposition: ["bottom center", "bottom center", "top center"],
                  textfont: { size: 11, color: "#0f172a" },
                });

                if (state.show_velocity) {
                  // 1. Вектор скорости γ'(t*) (сине-изумрудный)
                  if (velNorm > 1e-5) {
                    const vScale = Math.min(0.95, 0.65 / Math.max(0.5, velNorm));
                    const vxEnd = curX + velX * vScale;
                    const vyEnd = curY + velY * vScale;
                    const vzEnd = curZ + velZ * vScale;
                    traces.push({
                      type: "scatter3d",
                      mode: "lines",
                      x: [curX, vxEnd], y: [curY, vyEnd], z: [curZ, vzEnd],
                      line: { color: "#2563eb", width: 6 },
                      name: "γ'(t) скорость",
                    });
                    traces.push({
                      type: "cone",
                      x: [vxEnd], y: [vyEnd], z: [vzEnd],
                      u: [velX * 0.2], v: [velY * 0.2], w: [velZ * 0.2],
                      sizemode: "absolute", sizeref: 0.20, anchor: "tail",
                      colorscale: [[0, "#2563eb"], [1, "#1d4ed8"]],
                      showscale: false, hoverinfo: "skip",
                    });
                  }

                  // 2. Вектор поля / силы F(γ(t*)) и его проекция F_∥ на касательную (для Line Integral и Work)
                  if ((topic === "line_integral" || topic === "work") && fldNorm > 1e-5) {
                    const fScale = Math.min(0.95, 0.65 / Math.max(0.5, fldNorm));
                    const fxEnd = curX + fldX * fScale;
                    const fyEnd = curY + fldY * fScale;
                    const fzEnd = curZ + fldZ * fScale;

                    traces.push({
                      type: "scatter3d",
                      mode: "lines",
                      x: [curX, fxEnd], y: [curY, fyEnd], z: [curZ, fzEnd],
                      line: { color: "#ea580c", width: 6 },
                      name: "Сила F(γ(t))",
                    });
                    traces.push({
                      type: "cone",
                      x: [fxEnd], y: [fyEnd], z: [fzEnd],
                      u: [fldX * 0.2], v: [fldY * 0.2], w: [fldZ * 0.2],
                      sizemode: "absolute", sizeref: 0.20, anchor: "tail",
                      colorscale: [[0, "#ea580c"], [1, "#f97316"]],
                      showscale: false, hoverinfo: "skip",
                    });

                    // Касательная проекция F_∥ = ((F·v)/|v|^2) * v
                    if (velNorm > 1e-5) {
                      const projCoef = curDot / (velNorm * velNorm);
                      const pxEnd = curX + velX * projCoef * fScale;
                      const pyEnd = curY + velY * projCoef * fScale;
                      const pzEnd = curZ + velZ * projCoef * fScale;
                      const projColor = curDot >= 0 ? "#16a34a" : "#dc2626";

                      traces.push({
                        type: "scatter3d",
                        mode: "lines",
                        x: [curX, pxEnd, null, fxEnd, pxEnd],
                        y: [curY, pyEnd, null, fyEnd, pyEnd],
                        z: [curZ, pzEnd, null, fzEnd, pzEnd],
                        line: { color: projColor, width: 5, dash: "solid" },
                        name: "Проекция F_∥",
                      });
                    }
                  }
                }

                // =================================================================
                // СЛОЙ 8: ПРАВАЯ ПАНЕЛЬ — 2D ФАЗОВАЯ ПЛОСКОСТЬ (x,y) И ГРАФИК ИНТЕГРАЛА ПО t
                // =================================================================
                if (is2D) {
                  // 8.1 Стрелки 2D векторного поля F(x,y)
                  if (state.show_2d_field) {
                    const arrX = [], arrY = [];
                    const N2 = 12;
                    const step2 = (2 * R * 0.9) / (N2 - 1);
                    for (let i = 0; i < N2; i++) {
                      for (let j = 0; j < N2; j++) {
                        const gx = -R * 0.9 + j * step2;
                        const gy = -R * 0.9 + i * step2;
                        const [u, v] = evalVectorField(gx, gy, 0);
                        const mag = Math.hypot(u, v);
                        if (mag > 1e-5) {
                          const len = Math.min(step2 * 0.42, 0.13 + 0.13 * Math.tanh(mag * 0.35));
                          const dx = (u / mag) * len;
                          const dy = (v / mag) * len;
                          const ex = gx + dx, ey = gy + dy;
                          const headLen = len * 0.35;
                          const ang = Math.atan2(dy, dx);
                          arrX.push(
                            gx, ex, null,
                            ex - headLen * Math.cos(ang - 0.5), ex, ex - headLen * Math.cos(ang + 0.5), null
                          );
                          arrY.push(
                            gy, ey, null,
                            ey - headLen * Math.sin(ang - 0.5), ey, ey - headLen * Math.sin(ang + 0.5), null
                          );
                        }
                      }
                    }
                    traces.push({
                      type: "scatter",
                      mode: "lines",
                      x: arrX, y: arrY,
                      xaxis: "x", yaxis: "y",
                      line: { color: "rgba(13, 148, 136, 0.52)", width: 1.35 },
                      hoverinfo: "skip",
                    });
                  }

                  // 8.2 Пучок фазовых кривых в 2D (для Flow Line)
                  if (state.show_bundle && topic === "flow_line") {
                    const phX = [], phY = [];
                    const Mp = 45;
                    for (const [sx, sy] of bundleSeeds) {
                      const bPts = buildTrajectorySamples(sx, sy, Mp);
                      for (let i = 0; i <= Mp; i++) {
                        const [bx, by] = bPts[i].p;
                        if (Math.abs(bx) <= R * 1.15 && Math.abs(by) <= R * 1.15) {
                          phX.push(bx); phY.push(by);
                        } else {
                          phX.push(null); phY.push(null);
                        }
                      }
                      phX.push(null); phY.push(null);
                    }
                    traces.push({
                      type: "scatter",
                      mode: "lines",
                      x: phX, y: phY,
                      xaxis: "x", yaxis: "y",
                      line: { color: "rgba(99, 102, 241, 0.30)", width: 1.4, dash: "dot" },
                      hoverinfo: "skip",
                    });
                  }

                  // 8.3 Полная и построенная 2D кривая γ(t) = [x(t), y(t)]
                  traces.push({
                    type: "scatter",
                    mode: "lines",
                    x: fullX, y: fullY,
                    xaxis: "x", yaxis: "y",
                    line: { color: "rgba(148, 163, 184, 0.45)", width: 2, dash: "dash" },
                    hoverinfo: "skip",
                  });

                  traces.push({
                    type: "scatter",
                    mode: "lines",
                    x: drawX, y: drawY,
                    xaxis: "x", yaxis: "y",
                    line: { color: "#2563eb", width: 4 },
                  });

                  // 8.4 Векторы γ'(t*) и F(γ(t*)) на 2D плоскости
                  if (state.show_velocity) {
                    const v2Norm = Math.hypot(velX, velY);
                    if (v2Norm > 1e-5) {
                      const s2 = Math.min(0.8, 0.52 / Math.max(0.4, v2Norm));
                      traces.push({
                        type: "scatter",
                        mode: "lines+markers",
                        x: [curX, curX + velX * s2],
                        y: [curY, curY + velY * s2],
                        xaxis: "x", yaxis: "y",
                        line: { color: "#2563eb", width: 3.5 },
                        marker: { size: [0, 8], symbol: ["circle", "triangle-up"], color: "#2563eb" },
                      });
                    }
                    const f2Norm = Math.hypot(fldX, fldY);
                    if ((topic === "line_integral" || topic === "work") && f2Norm > 1e-5) {
                      const sf2 = Math.min(0.8, 0.52 / Math.max(0.4, f2Norm));
                      traces.push({
                        type: "scatter",
                        mode: "lines+markers",
                        x: [curX, curX + fldX * sf2],
                        y: [curY, curY + fldY * sf2],
                        xaxis: "x", yaxis: "y",
                        line: { color: "#ea580c", width: 3.5 },
                        marker: { size: [0, 8], symbol: ["circle", "triangle-up"], color: "#ea580c" },
                      });
                    }
                  }

                  // 8.5 Маркеры старта A и текущей точки γ(t*) на 2D
                  traces.push({
                    type: "scatter",
                    mode: "markers+text",
                    x: [startX, curX],
                    y: [startY, curY],
                    xaxis: "x", yaxis: "y",
                    marker: {
                      size: [9, 11],
                      color: ["#16a34a", "#dc2626"],
                      line: { width: 2, color: "#ffffff" },
                    },
                    text: [`A(${startX.toFixed(1)},${startY.toFixed(1)})`, `γ(${tStar.toFixed(2)})`],
                    textposition: ["bottom right", "top left"],
                    textfont: { size: 10.5, color: "#0f172a" },
                  });

                  // ===============================================================
                  // 8.6 НИЖНИЙ ПРАВЫЙ ГРАФИК: НАКОПЛЕНИЕ ИНТЕГРАЛА ПО ПАРАМЕТРУ t
                  // ===============================================================
                  if (showIntChart) {
                    // Полная кривая подынтегральной функции I(t)
                    traces.push({
                      type: "scatter",
                      mode: "lines",
                      x: fullT,
                      y: integrandArr,
                      xaxis: "x2",
                      yaxis: "y2",
                      line: { color: "#64748b", width: 2, dash: "dot" },
                      hoverinfo: "skip",
                    });

                    // Закрашенная площадь ∫_{t_min}^{t*} I(τ) dτ
                    const fillColor = (progDraw ? accumIntegral : totalIntegral) >= 0
                      ? "rgba(16, 185, 129, 0.30)"
                      : "rgba(239, 68, 68, 0.30)";
                    const lineColor = (progDraw ? accumIntegral : totalIntegral) >= 0
                      ? "#059669"
                      : "#dc2626";

                    traces.push({
                      type: "scatter",
                      mode: "lines",
                      x: progDraw ? actT : fullT,
                      y: progDraw ? actIntegrandArr : integrandArr,
                      xaxis: "x2",
                      yaxis: "y2",
                      fill: "tozeroy",
                      fillcolor: fillColor,
                      line: { color: lineColor, width: 3 },
                    });

                    // Текущий маркер на графике подынтегральной функции
                    const curIntegrandVal = integrandArr[curIdx] ?? 0;
                    traces.push({
                      type: "scatter",
                      mode: "markers+text",
                      x: [tStar],
                      y: [curIntegrandVal],
                      xaxis: "x2",
                      yaxis: "y2",
                      marker: { size: 9, color: "#dc2626", line: { width: 2, color: "#fff" } },
                      text: [`I(${tStar.toFixed(2)})=${curIntegrandVal.toFixed(2)}`],
                      textposition: "top center",
                      textfont: { size: 10, color: "#0f172a" },
                    });
                  }
                }

                const layout = {
                  template: "plotly_white",
                  paper_bgcolor: "#ffffff",
                  plot_bgcolor: "#f8fafc",
                  margin: { l: 8, r: 8, t: 28, b: 8 },
                  showlegend: false,
                  uirevision: "keep_vf_camera",
                  annotations: is2D ? [
                    {
                      text: `<b>3D Пространство: ${meta.name}</b>`,
                      x: 0.28, y: 1.03, xref: "paper", yref: "paper",
                      showarrow: false, font: { size: 12.5, color: "#0f172a" }
                    },
                    {
                      text: "<b>2D Плоскость (x, y): путь γ(t) и поле F(x,y)</b>",
                      x: 0.82, y: 1.03, xref: "paper", yref: "paper",
                      showarrow: false, font: { size: 12, color: "#0f172a" }
                    },
                    ...(showIntChart ? [{
                      text: `<b>Накопление интеграла: ${meta.integrandLabel} (Площадь = ${(progDraw ? accumIntegral : totalIntegral).toFixed(3)})</b>`,
                      x: 0.82, y: 0.37, xref: "paper", yref: "paper",
                      showarrow: false, font: { size: 11.5, color: "#0f172a" }
                    }] : [])
                  ] : [],
                  scene: {
                    domain: is2D ? { x: [0.0, 0.59], y: [0.0, 0.98] } : { x: [0.0, 1.0], y: [0.0, 0.98] },
                    xaxis: { range: [-R, R], title: "x(t)", gridcolor: "#e2e8f0", zerolineColor: "#64748b" },
                    yaxis: { range: [-R, R], title: "y(t)", gridcolor: "#e2e8f0", zerolineColor: "#64748b" },
                    zaxis: {
                      range: [zMinBound - 0.15 * zSpan, zMaxBound + 0.15 * zSpan],
                      title: topic === "path_integral" ? "Высота f(x,y)" : "z(t)",
                      gridcolor: "#e2e8f0",
                      zerolineColor: "#64748b",
                    },
                    aspectmode: "manual",
                    aspectratio: { x: 1.15, y: 1.15, z: 0.95 },
                    camera: { eye: currentEye, up: { x: 0, y: 0, z: 1 } },
                  },
                };

                if (is2D) {
                  layout.xaxis = {
                    domain: [0.64, 0.99],
                    range: [-R, R],
                    title: showIntChart ? "" : "x(t)",
                    gridcolor: "#e2e8f0",
                    zeroline: true,
                    zerolinecolor: "#94a3b8",
                  };
                  layout.yaxis = {
                    domain: showIntChart ? [0.43, 0.97] : [0.06, 0.96],
                    range: [-R, R],
                    title: "y(t)",
                    scaleanchor: "x",
                    scaleratio: 1,
                    gridcolor: "#e2e8f0",
                    zeroline: true,
                    zerolinecolor: "#94a3b8",
                  };
                  if (showIntChart) {
                    layout.xaxis2 = {
                      domain: [0.64, 0.99],
                      range: [tMin, tMax],
                      title: "Параметр t ∈ [a, b]",
                      gridcolor: "#e2e8f0",
                      zeroline: true,
                      zerolinecolor: "#94a3b8",
                    };
                    layout.yaxis2 = {
                      domain: [0.05, 0.34],
                      title: "I(t)",
                      gridcolor: "#e2e8f0",
                      zeroline: true,
                      zerolinecolor: "#475569",
                      zerolinewidth: 1.5,
                    };
                  }
                }

                Plotly.react(dom.plot, traces, layout, {
                  displayModeBar: true,
                  displaylogo: false,
                  responsive: true,
                });

                if (!plotInitialized) {
                  plotInitialized = true;
                  dom.plot.on("plotly_click", (ev) => {
                    if (ev && ev.points && ev.points.length > 0) {
                      const pt = ev.points[0];
                      if (pt.xaxis && pt.xaxis._id === "x2") {
                        // Клик по графику интеграла меняет время t*
                        state.t_val = Number(pt.x.toFixed(2));
                        syncSliderThumbsOnly();
                        renderPlot();
                      } else if (typeof pt.x === "number" && typeof pt.y === "number") {
                        state.x0 = Number(pt.x.toFixed(2));
                        state.y0 = Number(pt.y.toFixed(2));
                        state.status = `📍 Новая стартовая точка: (x₀, y₀) = (${state.x0}, ${state.y0})`;
                        syncSliderThumbsOnly();
                        renderPlot();
                      }
                    }
                  });
                  dom.plot.on("plotly_relayout", (ed) => {
                    const eye = (ed && ed["scene.camera"] && ed["scene.camera"].eye) || (ed && ed["scene.camera.eye"]);
                    if (eye) {
                      currentEye = { x: Number(eye.x), y: Number(eye.y), z: Number(eye.z) };
                      syncSphericalFromEye(currentEye);
                    }
                  });
                }

                // =================================================================
                // ПОШАГОВЫЕ ОБРАЗОВАТЕЛЬНЫЕ КАРТОЧКИ ВНИЗУ ДЛЯ ВЫБРАННОЙ ТЕМЫ
                // =================================================================
                if (topic === "path") {
                  dom.stepsBar.innerHTML = `
                    <div class="vf-step-card">
                      <b>Шаг 1. Параметризация пути γ(t)</b>
                      При <code>t = ${tStar.toFixed(2)}</code> из <code>[${tMin.toFixed(1)}, ${tMax.toFixed(1)}]</code>:<br/>
                      <code>γ(t) = [${curX.toFixed(2)}; ${curY.toFixed(2)}; ${curZ.toFixed(2)}]</code>
                    </div>
                    <div class="vf-step-card">
                      <b>Шаг 2. Вектор скорости γ'(t)</b>
                      Касательный вектор к траектории:<br/>
                      <code>γ'(t) = [${velX.toFixed(2)}; ${velY.toFixed(2)}; ${velZ.toFixed(2)}]</code>
                    </div>
                    <div class="vf-step-card">
                      <b>Шаг 3. Дифференциал дуги ds</b>
                      Мгновенная скорость точки:<br/>
                      <code>ds = ‖γ'(t)‖ dt = ${velNorm.toFixed(3)} dt</code>
                    </div>
                    <div class="vf-step-card">
                      <b>Шаг 4. Длина дуги кривой L(t)</b>
                      Накопленная длина от <code>a</code> до <code>t</code>: <code>${accumArcLen.toFixed(3)}</code><br/>
                      Полная длина на <code>[a, b]</code>: <code>L = ${totalArcLen.toFixed(3)}</code>
                    </div>
                  `;
                } else if (topic === "flow_line") {
                  dom.stepsBar.innerHTML = `
                    <div class="vf-step-card">
                      <b>Шаг 1. Задача Коши (Начальная точка)</b>
                      Старт <code>(x₀, y₀) = (${x0.toFixed(2)}, ${y0.toFixed(2)})</code>.<br/>
                      Векторное поле: <code>F = [${state.u_expr}, ${state.v_expr}, ${state.w_expr}]</code>
                    </div>
                    <div class="vf-step-card">
                      <b>Шаг 2. Движение вдоль поля при t = ${tStar.toFixed(2)}</b>
                      Точка на линии тока:<br/>
                      <code>γ(${tStar.toFixed(2)}) = [${curX.toFixed(2)}; ${curY.toFixed(2)}; ${curZ.toFixed(2)}]</code>
                    </div>
                    <div class="vf-step-card">
                      <b>Шаг 3. Условие линии тока γ'(t) = F(γ(t))</b>
                      Скорость кривой: <code>[${velX.toFixed(2)}, ${velY.toFixed(2)}, ${velZ.toFixed(2)}]</code><br/>
                      Вектор поля F: <code>[${fldX.toFixed(2)}, ${fldY.toFixed(2)}, ${fldZ.toFixed(2)}]</code>
                    </div>
                    <div class="vf-step-card">
                      <b>Шаг 4. Длина пройденной линии тока</b>
                      Пройденный путь до <code>t=${tStar.toFixed(2)}</code>: <code>s = ${accumArcLen.toFixed(3)}</code><br/>
                      Полная длина на <code>[${tMin.toFixed(1)}, ${tMax.toFixed(1)}]</code>: <code>${totalArcLen.toFixed(3)}</code>
                    </div>
                  `;
                } else if (topic === "path_integral") {
                  const dsCur = Math.hypot(velX, velY);
                  dom.stepsBar.innerHTML = `
                    <div class="vf-step-card">
                      <b>Шаг 1. Кривая γ(t) и функция высоты f(x,y)</b>
                      Путь: <code>γ(${tStar.toFixed(2)}) = (${curX.toFixed(2)}, ${curY.toFixed(2)})</code><br/>
                      Высота забора: <code>f(γ(t)) = ${state.f_expr} = ${curFVal.toFixed(3)}</code>
                    </div>
                    <div class="vf-step-card">
                      <b>Шаг 2. Элемент длины дуги ds</b>
                      Множитель растяжения дуги:<br/>
                      <code>ds = √(x'(t)² + y'(t)²) dt = ${dsCur.toFixed(3)} dt</code>
                    </div>
                    <div class="vf-step-card">
                      <b>Шаг 3. Площадь элементарной полоски</b>
                      Высота × ширина основания:<br/>
                      <code>dI = f(γ(t))·‖γ'(t)‖ dt = ${(curFVal * dsCur).toFixed(3)} dt</code>
                    </div>
                    <div class="vf-step-card">
                      <b>Шаг 4. Интеграл I рода ∫_γ f ds</b>
                      Накоплено до <code>t=${tStar.toFixed(2)}</code>: <code>${accumIntegral.toFixed(3)}</code><br/>
                      Полная площадь забора: <code>∫_γ f ds = ${totalIntegral.toFixed(3)}</code>
                    </div>
                  `;
                } else if (topic === "line_integral") {
                  dom.stepsBar.innerHTML = `
                    <div class="vf-step-card">
                      <b>Шаг 1. Вектор поля F на кривой γ(t)</b>
                      В точке <code>γ(${tStar.toFixed(2)}) = [${curX.toFixed(2)}, ${curY.toFixed(2)}, ${curZ.toFixed(2)}]</code>:<br/>
                      <code>F(γ(t)) = [${fldX.toFixed(2)}, ${fldY.toFixed(2)}, ${fldZ.toFixed(2)}]</code>
                    </div>
                    <div class="vf-step-card">
                      <b>Шаг 2. Дифференциал пути dγ = γ'(t)dt</b>
                      Касательный вектор скорости:<br/>
                      <code>γ'(t) = [${velX.toFixed(2)}, ${velY.toFixed(2)}, ${velZ.toFixed(2)}]</code>
                    </div>
                    <div class="vf-step-card">
                      <b>Шаг 3. Скалярное произведение F · γ'(t)</b>
                      <code>P·x' + Q·y' + R·z' = ${curDot.toFixed(3)}</code><br/>
                      Угол между F и γ': <code>θ = ${thetaDeg.toFixed(1)}° (cos θ = ${cosTheta.toFixed(2)})</code>
                    </div>
                    <div class="vf-step-card">
                      <b>Шаг 4. Интеграл II рода ∫_γ F · dγ</b>
                      Накоплено до <code>t=${tStar.toFixed(2)}</code>: <code>${accumIntegral.toFixed(3)}</code><br/>
                      Полный интеграл: <code>∫_γ F·dγ = ${totalIntegral.toFixed(3)}</code>
                    </div>
                  `;
                } else {
                  const isConserv = Math.abs(curlZ) < 1e-2;
                  dom.stepsBar.innerHTML = `
                    <div class="vf-step-card">
                      <b>Шаг 1. Сила F и перемещение dr</b>
                      Сила в точке: <code>F = [${fldX.toFixed(2)}, ${fldY.toFixed(2)}, ${fldZ.toFixed(2)}]</code><br/>
                      Скорость: <code>v = dr/dt = [${velX.toFixed(2)}, ${velY.toFixed(2)}, ${velZ.toFixed(2)}]</code>
                    </div>
                    <div class="vf-step-card">
                      <b>Шаг 2. Разложение силы: F = F_∥ + F_⊥</b>
                      Угол <code>θ = ${thetaDeg.toFixed(1)}°</code> (<code>cos θ = ${cosTheta.toFixed(2)}</code>).<br/>
                      Ротор <code>(∇×F)_z = ${curlZ.toFixed(2)}</code> (${isConserv ? "Консервативно ✅" : "Вихревое 🌀"})
                    </div>
                    <div class="vf-step-card">
                      <b>Шаг 3. Элементарная работа dW = F · dr</b>
                      Мощность: <code>dW/dt = F·v = ${curDot.toFixed(3)}</code><br/>
                      ${curDot >= 0 ? "🟢 Сила разгоняет частицу (dW > 0)" : "🔴 Сила тормозит частицу (dW < 0)"}
                    </div>
                    <div class="vf-step-card">
                      <b>Шаг 4. Полная работа поля W = ∫_γ F · dr</b>
                      Работа от старта до <code>t=${tStar.toFixed(2)}</code>: <code>W(t) = ${accumIntegral.toFixed(3)}</code><br/>
                      Полная работа на всём пути: <code>W = ${totalIntegral.toFixed(3)}</code>
                    </div>
                  `;
                }
              });
            }

            syncControlsFromState();
            renderPlot();
          }
        };
        """

        state_json = traitlets.Unicode("{}").tag(sync=True)
        api_key = traitlets.Unicode("").tag(sync=True)
        cmd_seq = traitlets.Int(0).tag(sync=True)
        cmd_request = traitlets.Dict({}).tag(sync=True)

        def __init__(self, initial_state: dict, initial_key: str = "", **kwargs):
            super().__init__(
                state_json=json.dumps(initial_state, ensure_ascii=False),
                api_key=initial_key,
                cmd_seq=0,
                cmd_request={},
                **kwargs,
            )
            self.observe(self._handle_cmd_request, names=["cmd_request"])

        def _handle_cmd_request(self, change):
            req = change.get("new") or {}
            if not req:
                return
            cmd_text = str(req.get("command") or "").strip()
            use_ai = bool(req.get("use_ai", False))
            preset_id = str(req.get("preset_id") or "").strip()
            img_b64 = str(req.get("image_b64") or "").strip()
            img_mime = str(req.get("image_mime") or "image/png").strip()
            cur_st = req.get("current_state") or json.loads(self.state_json)

            if preset_id and preset_id in PRESET_STATES:
                next_st = dict(PRESET_STATES[preset_id])
                self.state_json = json.dumps(next_st, ensure_ascii=False)
                return

            key = (self.api_key or env_key or "").strip()

            # Если прислан скриншот задачи — сразу отправляем в Gemini Vision
            if img_b64:
                ai_st, ai_ok, msg = ask_gemini_vector_ai(cmd_text, key, cur_st, image_b64=img_b64, image_mime=img_mime)
                if not ai_ok:
                    ai_st = dict(cur_st)
                    ai_st["status"] = msg
                self.state_json = json.dumps(ai_st, ensure_ascii=False)
                return

            if not cmd_text:
                return

            next_st, handled = parse_vector_command(cmd_text, cur_st)

            if use_ai or (not handled and key):
                ai_st, ai_ok, msg = ask_gemini_vector_ai(cmd_text, key, next_st if handled else cur_st)
                if ai_ok:
                    next_st = ai_st
                    handled = True
                elif use_ai:
                    next_st["status"] = msg
                    handled = True

            if not handled:
                next_st["status"] = (
                    f"💬 Не удалось распознать «{cmd_text}». Введите [x(t); y(t); z(t)], выберите тему или нажмите 🤖 Решить с AI."
                )

            self.state_json = json.dumps(next_st, ensure_ascii=False)

    studio_widget = mo.ui.anywidget(
        VectorFieldFlowStudio(
            initial_state=dict(PRESET_STATES["preset_flow_saddle"]),
            initial_key="",
        )
    )
    studio_widget
    return (
        AI_PROBLEM_SCHEMA,
        PRESET_STATES,
        VectorFieldFlowStudio,
        ask_gemini_vector_ai,
        env_key,
        infer_velocity_expr,
        normalize_math_expr,
        parse_vector_command,
        studio_widget,
    )


if __name__ == "__main__":
    import argparse
    import os
    import subprocess
    import sys

    parser = argparse.ArgumentParser(description="Vector Field, Paths & Line Integrals 3D/2D Studio")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface")
    parser.add_argument("--port", type=int, default=8000, help="Port number")
    parser.add_argument("--no-browser", action="store_true", help="Do not open browser")
    parser.add_argument("--marimo-edit", action="store_true", help="Open in Marimo edit mode")
    args, _ = parser.parse_known_args()

    actual_port = int(os.environ.get("PORT", args.port))
    mode = "edit" if args.marimo_edit else "run"
    cmd = [
        sys.executable,
        "-m",
        "marimo",
        mode,
        os.path.abspath(__file__),
        "--host",
        args.host,
        "--port",
        str(actual_port),
    ]
    if args.no_browser or os.environ.get("PORT"):
        cmd.append("--headless")
    if not args.marimo_edit:
        cmd.append("--no-token")

    raise SystemExit(subprocess.call(cmd))
