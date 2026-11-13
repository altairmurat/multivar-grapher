import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full")


@app.cell
def _():
    import json
    import math
    import os
    import re
    import anywidget
    from google import genai
    from google.genai import types
    import marimo as mo
    import numpy as np
    import traitlets

    return anywidget, genai, json, math, mo, np, os, re, traitlets, types


@app.cell
def _(anywidget, genai, json, math, mo, np, os, re, traitlets, types):
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
    # 2. ПРЕСЕТЫ ПО ТЕМЕ VECTOR FIELDS & F(gamma(t)) = [x(t); y(t); z(t)]
    # =========================================================================
    PRESET_STATES = {
        "preset_saddle_exp": {
            "preset_id": "preset_saddle_exp",
            "title": "F(γ(t)) = [x₀·e^(2t); y₀·e^(-t); t] — Седловой поток в 3D и 2D",
            "full_formula": "[x0*e^2t; y0*e^(-t); t]",
            "x_expr": "x0 * e^(2*t)",
            "y_expr": "y0 * e^(-t)",
            "z_expr": "t",
            "u_expr": "2*x",
            "v_expr": "-y",
            "w_expr": "1",
            "auto_field": True,
            "x0": 0.45,
            "y0": 1.35,
            "t_val": 0.55,
            "t_min": -1.2,
            "t_max": 1.2,
            "xy_range": [-2.6, 2.6],
            "show_2d_field": True,
            "show_3d_field": True,
            "show_curtain": True,
            "show_bundle": True,
            "show_velocity": True,
            "show_floor_curve": True,
            "show_surface": False,
            "split_2d": True,
            "show_box_grid": True,
            "anim_mode": "none",
            "cam_active": False,
            "status": "⚡ Готово: F(γ(t)) = [x₀·e^(2t); y₀·e^(-t); t], где γ(t) = [x(t); y(t)]",
        },
        "preset_spiral_sink": {
            "preset_id": "preset_spiral_sink",
            "title": "F(γ(t)) = [e^(-0.35t)·(x₀cos(2t)-y₀sin(2t)); e^(-0.35t)·(x₀sin(2t)+y₀cos(2t)); t] — Спиральный фокус",
            "full_formula": "[e^(-0.35*t)*(x0*cos(2*t) - y0*sin(2*t)); e^(-0.35*t)*(x0*sin(2*t) + y0*cos(2*t)); t]",
            "x_expr": "e^(-0.35*t)*(x0*cos(2*t) - y0*sin(2*t))",
            "y_expr": "e^(-0.35*t)*(x0*sin(2*t) + y0*cos(2*t))",
            "z_expr": "t",
            "u_expr": "-0.35*x - 2*y",
            "v_expr": "2*x - 0.35*y",
            "w_expr": "1",
            "auto_field": True,
            "x0": 1.60,
            "y0": 1.10,
            "t_val": 1.40,
            "t_min": -0.8,
            "t_max": 3.2,
            "xy_range": [-2.6, 2.6],
            "show_2d_field": True,
            "show_3d_field": True,
            "show_curtain": True,
            "show_bundle": True,
            "show_velocity": True,
            "show_floor_curve": True,
            "show_surface": False,
            "split_2d": True,
            "show_box_grid": True,
            "anim_mode": "none",
            "cam_active": False,
            "status": "🌀 Спиральный сток: в 2D закручивается к (0,0), в 3D образует коническую спираль вдоль оси t",
        },
        "preset_vortex_helix": {
            "preset_id": "preset_vortex_helix",
            "title": "F(γ(t)) = [x₀cos(t) - y₀sin(t); x₀sin(t) + y₀cos(t); t] — Вихревой поток и винтовая линия",
            "full_formula": "[x0*cos(t) - y0*sin(t); x0*sin(t) + y0*cos(t); t]",
            "x_expr": "x0*cos(t) - y0*sin(t)",
            "y_expr": "x0*sin(t) + y0*cos(t)",
            "z_expr": "t",
            "u_expr": "-y",
            "v_expr": "x",
            "w_expr": "1",
            "auto_field": True,
            "x0": 1.50,
            "y0": 0.50,
            "t_val": 1.80,
            "t_min": -2.0,
            "t_max": 3.5,
            "xy_range": [-2.5, 2.5],
            "show_2d_field": True,
            "show_3d_field": True,
            "show_curtain": True,
            "show_bundle": True,
            "show_velocity": True,
            "show_floor_curve": True,
            "show_surface": False,
            "split_2d": True,
            "show_box_grid": True,
            "anim_mode": "none",
            "cam_active": False,
            "status": "🎡 Вихревое поле V = [-y, x]: в 2D окружность γ(t), в 3D — винтовая спираль (геликоид)",
        },
        "preset_unstable_node": {
            "preset_id": "preset_unstable_node",
            "title": "F(γ(t)) = [x₀·e^t; y₀·e^(2t); t] — Неустойчивый узел (Источник)",
            "full_formula": "[x0*e^t; y0*e^2t; t]",
            "x_expr": "x0 * e^t",
            "y_expr": "y0 * e^(2*t)",
            "z_expr": "t",
            "u_expr": "x",
            "v_expr": "2*y",
            "w_expr": "1",
            "auto_field": True,
            "x0": 0.65,
            "y0": 0.35,
            "t_val": 0.50,
            "t_min": -1.5,
            "t_max": 1.1,
            "xy_range": [-2.6, 2.6],
            "show_2d_field": True,
            "show_3d_field": True,
            "show_curtain": True,
            "show_bundle": True,
            "show_velocity": True,
            "show_floor_curve": True,
            "show_surface": False,
            "split_2d": True,
            "show_box_grid": True,
            "anim_mode": "none",
            "cam_active": False,
            "status": "🚀 Источник V = [x, 2y]: в 2D параболический разлёт y = C·x², в 3D — подъём по t",
        },
        "preset_surface_lift": {
            "preset_id": "preset_surface_lift",
            "title": "F(γ(t)) = [x₀·e^(0.5t); y₀·e^(-0.5t); x² - y²] — Подъём траектории γ(t) на поверхность z = x² - y²",
            "full_formula": "[x0*e^(0.5*t); y0*e^(-0.5*t); x^2 - y^2]",
            "x_expr": "x0 * e^(0.5*t)",
            "y_expr": "y0 * e^(-0.5*t)",
            "z_expr": "x^2 - y^2",
            "u_expr": "0.5*x",
            "v_expr": "-0.5*y",
            "w_expr": "x^2 + y^2",
            "auto_field": True,
            "x0": 0.80,
            "y0": 1.30,
            "t_val": 0.60,
            "t_min": -1.6,
            "t_max": 1.6,
            "xy_range": [-2.4, 2.4],
            "show_2d_field": True,
            "show_3d_field": True,
            "show_curtain": True,
            "show_bundle": True,
            "show_velocity": True,
            "show_floor_curve": True,
            "show_surface": True,
            "split_2d": True,
            "show_box_grid": True,
            "anim_mode": "none",
            "cam_active": False,
            "status": "⛰️ Кривая γ(t) течёт по плоскости (x,y), а F(γ(t)) поднимает её на 3D поверхность z = x² - y²",
        },
    }

    # =========================================================================
    # 3. ПАРСЕР ВЕКТОР-ФУНКЦИЙ F(gamma(t)) = [x(t); y(t); z(t)] И КОМАНД
    # =========================================================================
    def normalize_math_expr(expr: str) -> str:
        s = (expr or "").strip()
        uni = {
            "⁰": "^0", "¹": "^1", "²": "^2", "³": "^3", "⁴": "^4",
            "⁵": "^5", "⁶": "^6", "⁷": "^7", "⁸": "^8", "⁹": "^9",
            "⁻": "-", "⁺": "+", "₀": "0", "₁": "1", "₂": "2", "₃": "3",
            "−": "-", "–": "-", "—": "-", "×": "*", "·": "*", "∙": "*", "÷": "/",
        }
        for k, v in uni.items():
            s = s.replace(k, v)
        s = re.sub(r"\bx_0\b", "x0", s, flags=re.IGNORECASE)
        s = re.sub(r"\by_0\b", "y0", s, flags=re.IGNORECASE)
        # Поддержка записи вида e^2t, e^-2t, e^(-t), e^(2t)
        s = re.sub(r"\be\s*\^\s*\(([^)]+)\)", r"exp(\1)", s)
        s = re.sub(r"\be\s*\^\s*([+\-]?\d+(?:\.\d+)?\s*\*?\s*[tTxXyY]\d*)", r"exp(\1)", s)
        s = re.sub(r"\be\s*\^\s*([+\-]?[a-zA-Z0-9_]+)", r"exp(\1)", s)
        return s.strip()

    def infer_velocity_expr(coord_expr: str, var_name: str) -> str:
        """Пытается красиво записать символьную производную для простых экспонент x0*e^(k*t)."""
        norm = normalize_math_expr(coord_expr).replace(" ", "")
        # Проверка на x0*exp(k*t) или y0*exp(k*t)
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

        # 1. Сброс к исходному примеру пользователя [x0*e^2t; y0*e^(-t); t]
        if any(w in low for w in ("сброс", "сначала", "reset", "седлов")):
            fresh = dict(PRESET_STATES["preset_saddle_exp"])
            fresh["status"] = "⚡ Сброшено к F(γ(t)) = [x₀·e^(2t); y₀·e^(-t); t]"
            return fresh, True

        # 2. Проверка на ввод вектор-функции в скобках: [x(t); y(t); z(t)] или [x(t), y(t), z(t)]
        bracket_m = re.search(r"\[\s*([^\]]+)\s*\]", norm)
        if bracket_m:
            inner = bracket_m.group(1)
            sep = ";" if ";" in inner else ","
            comps = [c.strip() for c in inner.split(sep) if c.strip()]
            if len(comps) >= 2:
                s["x_expr"] = comps[0]
                s["y_expr"] = comps[1]
                s["z_expr"] = comps[2] if len(comps) >= 3 else "t"
                s["full_formula"] = f"[{s['x_expr']}; {s['y_expr']}; {s['z_expr']}]"
                u_inf = infer_velocity_expr(s["x_expr"], "x")
                v_inf = infer_velocity_expr(s["y_expr"], "y")
                w_inf = infer_velocity_expr(s["z_expr"], "z")
                if u_inf:
                    s["u_expr"] = u_inf
                if v_inf:
                    s["v_expr"] = v_inf
                if w_inf:
                    s["w_expr"] = w_inf
                s["auto_field"] = True
                s["title"] = f"F(γ(t)) = [{s['x_expr']}; {s['y_expr']}; {s['z_expr']}]"
                parts.append(f"F(γ(t)) = {s['full_formula']}")
                handled = True

        # 3. Если введены 3 компоненты через точку с запятой без квадратных скобок: x0*e^2t; y0*e^(-t); t
        elif ";" in norm and len(norm.split(";")) >= 2:
            cleaned = re.sub(r"^.*?=\s*", "", norm).strip()
            comps = [c.strip() for c in cleaned.split(";") if c.strip()]
            if len(comps) >= 2:
                s["x_expr"] = comps[0]
                s["y_expr"] = comps[1]
                s["z_expr"] = comps[2] if len(comps) >= 3 else "t"
                s["full_formula"] = f"[{s['x_expr']}; {s['y_expr']}; {s['z_expr']}]"
                u_inf = infer_velocity_expr(s["x_expr"], "x")
                v_inf = infer_velocity_expr(s["y_expr"], "y")
                w_inf = infer_velocity_expr(s["z_expr"], "z")
                if u_inf:
                    s["u_expr"] = u_inf
                if v_inf:
                    s["v_expr"] = v_inf
                if w_inf:
                    s["w_expr"] = w_inf
                s["auto_field"] = True
                s["title"] = f"F(γ(t)) = [{s['x_expr']}; {s['y_expr']}; {s['z_expr']}]"
                parts.append(f"F(γ(t)) = {s['full_formula']}")
                handled = True

        # 4. Именованные типы векторных полей
        if not handled:
            if any(w in low for w in ("спирал", "фокус", "spiral", "sink")):
                p = dict(PRESET_STATES["preset_spiral_sink"])
                return p, True
            if any(w in low for w in ("вихр", "винтов", "окружност", "vortex", "helix")):
                p = dict(PRESET_STATES["preset_vortex_helix"])
                return p, True
            if any(w in low for w in ("источник", "узел", "node", "source")):
                p = dict(PRESET_STATES["preset_unstable_node"])
                return p, True
            if any(w in low for w in ("поверхност", "подъем", "подъём", "surface")):
                p = dict(PRESET_STATES["preset_surface_lift"])
                return p, True

        # 5. Начальные координаты x0, y0 и время t
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

        # 6. Управление анимацией (ТОЛЬКО по явному запросу)
        wants_stop = any(w in low for w in ("стоп", "останови", "пауза", "stop", "pause", "freeze"))
        wants_anim = any(w in low for w in ("анимир", "анимац", "двиг", "динамик", "запусти", "animate", "play"))
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
                s["anim_mode"] = "t"
            parts.append(f"🎬 запущена анимация ({s['anim_mode']})")
            handled = True

        if handled:
            s["status"] = "✅ Выполнено: " + (", ".join(parts) if parts else raw)

        return s, handled

    def ask_gemini_vector_ai(query: str, api_key: str, current_state: dict) -> tuple[dict, bool, str]:
        if not api_key:
            return current_state, False, "⚠️ Введите GEMINI_API_KEY в правом верхнем углу"
        try:
            client = genai.Client(api_key=api_key, http_options={"timeout": 6000})
            schema = {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "x_expr": {"type": "string", "description": "x(t) expression using t, x0, y0, e.g. 'x0*e^(2*t)'"},
                    "y_expr": {"type": "string", "description": "y(t) expression using t, x0, y0, e.g. 'y0*e^(-t)'"},
                    "z_expr": {"type": "string", "description": "z(t) expression using t, x0, y0, x, y, e.g. 't'"},
                    "u_expr": {"type": "string", "description": "dx/dt vector field component P(x,y), e.g. '2*x'"},
                    "v_expr": {"type": "string", "description": "dy/dt vector field component Q(x,y), e.g. '-y'"},
                    "w_expr": {"type": "string", "description": "dz/dt vector field component R(x,y,z), e.g. '1'"},
                    "x0": {"type": "number"},
                    "y0": {"type": "number"},
                    "t_val": {"type": "number"},
                    "t_min": {"type": "number"},
                    "t_max": {"type": "number"},
                    "show_curtain": {"type": "boolean"},
                    "show_bundle": {"type": "boolean"},
                    "show_surface": {"type": "boolean"},
                    "anim_mode": {"type": "string", "enum": ["none", "t", "x0", "y0", "orbit"]},
                },
                "required": [
                    "title", "x_expr", "y_expr", "z_expr", "u_expr", "v_expr", "w_expr",
                    "x0", "y0", "t_val", "t_min", "t_max", "show_curtain", "show_bundle", "show_surface", "anim_mode"
                ],
            }
            sys_prompt = (
                "You are an interactive 3D & 2D Vector Field and Parametric Flow F(gamma(t)) = [x(t); y(t); z(t)] studio controller.\n"
                "Parse the user's request into x_expr, y_expr, z_expr (functions of t, x0, y0) and vector field u_expr, v_expr, w_expr (functions of x, y, z).\n"
                "Set anim_mode to 'none' unless the user explicitly asks to animate."
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"User request: {query}\nCurrent state: {json.dumps(current_state, ensure_ascii=False)}",
                config=types.GenerateContentConfig(
                    system_instruction=sys_prompt,
                    temperature=0.1,
                    response_mime_type="application/json",
                    response_schema=schema,
                ),
            )
            data = json.loads(response.text or "{}")
            new_st = dict(current_state)
            for k in (
                "title", "x_expr", "y_expr", "z_expr", "u_expr", "v_expr", "w_expr",
                "x0", "y0", "t_val", "t_min", "t_max", "show_curtain", "show_bundle", "show_surface", "anim_mode"
            ):
                if k in data:
                    new_st[k] = data[k]
            new_st["full_formula"] = f"[{new_st['x_expr']}; {new_st['y_expr']}; {new_st['z_expr']}]"
            new_st["status"] = f"✨ Gemini AI настроил поток: {new_st['full_formula']}"
            return new_st, True, new_st["status"]
        except Exception as e:
            return current_state, False, f"⚠️ Ошибка Gemini API: {str(e)[:65]}"

    # =========================================================================
    # 4. ИНТЕРАКТИВНЫЙ 3D + 2D ВИДЖЕТ VECTOR FIELD & F(gamma(t)) STUDIO
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
        // Корректно парсит запись вида x0*e^2t, y0*e^(-t), e^-0.5t, x^2 - y^2 и т.д.
        function compileFlowExpr(exprStr, fallbackVal = 0) {
          let s = String(exprStr || "0").trim();
          const mapUni = {
            "⁰":"^0","¹":"^1","²":"^2","³":"^3","⁴":"^4","⁵":"^5","⁶":"^6","⁷":"^7","⁸":"^8","⁹":"^9",
            "⁻":"-","⁺":"+","₀":"0","₁":"1","₂":"2","₃":"3","−":"-","–":"-","—":"-","×":"*","·":"*","÷":"/","π":"pi"
          };
          for (const [k, v] of Object.entries(mapUni)) s = s.split(k).join(v);
          s = s.replace(/^[a-zA-Z0-9_]+\s*(\([^)]*\))?\s*=\s*/i, "");
          s = s.replace(/np\./g, "").replace(/Math\./g, "");
          s = s.replace(/\bx_0\b/gi, "x0").replace(/\by_0\b/gi, "y0");
          s = s.replace(/\bx_?1\b/gi, "x").replace(/\bx_?2\b/gi, "y");

          // Особая обработка экспонент: e^(2t), e^2t, e^-2t, e^(-t), e^t -> exp(...)
          s = s.replace(/\be\s*\^\s*\(([^)]+)\)/g, "exp($1)");
          s = s.replace(/\be\s*\^\s*([+\-]?\d+(?:\.\d+)?\s*\*?\s*[tTxXyYzZ]\d*)/g, "exp($1)");
          s = s.replace(/\be\s*\^\s*([+\-]?[a-zA-Z0-9_]+)/g, "exp($1)");

          // Неявное умножение: 2t -> 2*t, 2x -> 2*x, 2( -> 2*(, )x -> )*x, x0e -> x0*e
          s = s.replace(/(\d)\s*([a-zA-Z\(])/g, "$1*$2");
          s = s.replace(/(\))\s*([a-zA-Z\d\(])/g, "$1*$2");
          s = s.replace(/\b(x0|y0|t|x|y|z)\s+(x0|y0|t|x|y|z|exp|sin|cos|tan|sqrt|log|abs)\b/gi, "$1*$2");
          s = s.replace(/\b(x0|y0)\s*(exp|sin|cos|tan|sqrt|log|abs|\()/gi, "$1*$2");

          // Возведение в степень ^ -> **
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
          // x0*e^(2t) or x0*e^2t or x0*exp(2*t)
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

            el.innerHTML = `
              <style>
                .vf-studio {
                  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                  color: #0f172a;
                  background: #ffffff;
                  border: 1px solid #cbd5e1;
                  border-radius: 14px;
                  padding: 12px 16px;
                  box-shadow: 0 6px 24px rgba(15, 23, 42, 0.05);
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
                  font-size: 16px;
                  font-weight: 800;
                  color: #0f172a;
                  display: flex;
                  align-items: center;
                  gap: 8px;
                }
                .vf-badge {
                  background: linear-gradient(135deg, #2563eb 0%, #0d9488 100%);
                  color: #fff;
                  font-size: 11px;
                  font-weight: 700;
                  padding: 3px 9px;
                  border-radius: 999px;
                }
                .vf-voice-bar {
                  display: flex;
                  align-items: center;
                  gap: 8px;
                  background: linear-gradient(90deg, #f8fafc 0%, #eff6ff 100%);
                  border: 1px solid #cbd5e1;
                  border-radius: 10px;
                  padding: 7px 12px;
                  margin-top: 8px;
                  flex-wrap: wrap;
                }
                .vf-btn {
                  cursor: pointer;
                  border-radius: 8px;
                  border: 1px solid #cbd5e1;
                  background: #ffffff;
                  color: #1e293b;
                  font-size: 12px;
                  font-weight: 600;
                  padding: 6px 12px;
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
                .vf-btn-primary:hover {
                  background: #1d4ed8;
                }
                .vf-btn-ai {
                  background: #0f766e;
                  color: #ffffff;
                  border-color: #115e59;
                }
                .vf-btn-ai:hover {
                  background: #115e59;
                }
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
                .vf-grid-inputs {
                  display: grid;
                  grid-template-columns: 1.3fr 1.6fr 1.2fr;
                  gap: 10px;
                  margin-top: 10px;
                  background: #f8fafc;
                  border: 1px solid #e2e8f0;
                  border-radius: 10px;
                  padding: 10px 12px;
                }
                @media (max-width: 1100px) {
                  .vf-grid-inputs { grid-template-columns: 1fr; }
                }
                .vf-label {
                  font-size: 11.5px;
                  font-weight: 700;
                  color: #334155;
                  margin-bottom: 4px;
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                }
                .vf-input {
                  padding: 6px 9px;
                  border: 1px solid #cbd5e1;
                  border-radius: 7px;
                  font-size: 12.5px;
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
                  gap: 6px;
                }
                .vf-comp-box {
                  display: flex;
                  align-items: center;
                  background: #fff;
                  border: 1px solid #cbd5e1;
                  border-radius: 7px;
                  padding: 2px 6px;
                }
                .vf-comp-box span {
                  font-size: 11.5px;
                  font-weight: 700;
                  color: #2563eb;
                  margin-right: 4px;
                  white-space: nowrap;
                }
                .vf-comp-box input {
                  border: none;
                  outline: none;
                  width: 100%;
                  font-family: 'JetBrains Mono', Consolas, monospace;
                  font-size: 12px;
                  font-weight: 600;
                  color: #0f172a;
                }
                .vf-sliders-grid {
                  display: grid;
                  grid-template-columns: repeat(4, 1fr);
                  gap: 10px;
                  margin-top: 10px;
                }
                @media (max-width: 1000px) {
                  .vf-sliders-grid { grid-template-columns: repeat(2, 1fr); }
                }
                .vf-slider-card {
                  background: #f8fafc;
                  border: 1px solid #e2e8f0;
                  border-radius: 9px;
                  padding: 7px 10px;
                }
                .vf-slider-head {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  font-size: 12px;
                  margin-bottom: 4px;
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
                  font-size: 12px;
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
                  gap: 8px;
                  flex-wrap: wrap;
                  margin-top: 10px;
                  padding-bottom: 8px;
                  border-bottom: 1px solid #f1f5f9;
                }
                .vf-chips-group {
                  display: flex;
                  align-items: center;
                  gap: 6px;
                  flex-wrap: wrap;
                }
                .vf-chip {
                  cursor: pointer;
                  user-select: none;
                  font-size: 11.5px;
                  font-weight: 600;
                  padding: 5px 10px;
                  border-radius: 999px;
                  border: 1px solid #cbd5e1;
                  background: #f8fafc;
                  color: #475569;
                  transition: all 0.15s ease;
                }
                .vf-chip.active {
                  background: #eff6ff;
                  color: #1d4ed8;
                  border-color: #93c5fd;
                  box-shadow: 0 1px 3px rgba(37, 99, 235, 0.12);
                }
                .vf-status-banner {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  background: #f8fafc;
                  border-left: 4px solid #2563eb;
                  border-radius: 6px;
                  padding: 6px 12px;
                  margin-top: 8px;
                  font-size: 13px;
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
                  font-size: 12px;
                  line-height: 1.45;
                }
                .vf-step-card b {
                  color: #1e3a8a;
                  display: block;
                  margin-bottom: 2px;
                  font-size: 11.5px;
                  text-transform: uppercase;
                  letter-spacing: 0.3px;
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
                  cursor: grab;
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
                .vf-cam-icon-btn:hover {
                  background: rgba(56, 189, 248, 0.2);
                  border-color: #38bdf8;
                }
              </style>

              <div class="vf-studio">
                <!-- ШАПКА -->
                <div class="vf-topbar">
                  <div class="vf-brand">
                    <span class="vf-badge">VECTOR FIELD 3D + 2D</span>
                    <span>Поток векторного поля и построение кривой <b>F(γ(t)) = [x(t); y(t); z(t)]</b>, где <b>γ(t) = [x(t); y(t)]</b></span>
                  </div>
                  <div style="display:flex;align-items:center;gap:6px;">
                    <span style="font-size:11.5px;color:#64748b;font-weight:600;">🔑 Gemini API:</span>
                    <input id="vf-apikey" type="password" class="vf-input" style="width:170px;padding:4px 8px;font-size:11.5px;" placeholder="AI ключ (опционально)" />
                  </div>
                </div>

                <!-- СТРОКА БЫСТРОГО ВВОДА ФОРМУЛЫ, ГОЛОСА И КАМЕРЫ -->
                <div class="vf-voice-bar">
                  <button id="vf-mic-btn" class="vf-btn vf-mic-btn">🎙️ Голос</button>
                  <select id="vf-lang" class="vf-input" style="padding:4px 6px;font-size:11.5px;">
                    <option value="ru-RU">RU</option>
                    <option value="en-US">EN</option>
                  </select>
                  <button id="vf-cam-btn" class="vf-btn vf-cam-btn" title="Крутить 3D-сцену и двигать (x₀, y₀) жестами">📷 Камера 3D</button>
                  <input id="vf-nl-input" type="text" class="vf-input" style="flex:1;min-width:260px;font-weight:700;"
                    value="[x0*e^2t; y0*e^(-t); t]"
                    placeholder="Введите F(γ(t)): напр. [x0*e^2t; y0*e^(-t); t] или скажите голосом..." />
                  <button id="vf-nl-run" class="vf-btn vf-btn-primary">⚡ Построить F(γ(t))</button>
                  <button id="vf-nl-ai" class="vf-btn vf-btn-ai">🤖 Gemini AI</button>
                  <span id="vf-voice-live" style="font-size:11.5px;color:#2563eb;font-weight:600;"></span>
                </div>

                <!-- ПАНЕЛЬ ПАРАМЕТРИЧЕСКИХ КОМПОНЕНТ x(t), y(t), z(t) И ВЕКТОРНОГО ПОЛЯ V(x,y,z) -->
                <div class="vf-grid-inputs">
                  <!-- Выбор пресета -->
                  <div>
                    <div class="vf-label">
                      <span>📚 Примеры потоков <b>F(γ(t))</b>:</span>
                      <span style="color:#64748b;font-weight:400;">3D + 2D</span>
                    </div>
                    <select id="vf-preset" class="vf-input" style="width:100%;font-family:inherit;font-weight:600;">
                      <option value="preset_saddle_exp">1. Седловой поток: F(γ(t)) = [x₀·e^(2t); y₀·e^(-t); t]</option>
                      <option value="preset_spiral_sink">2. Спиральный фокус: затухающее вращение в 3D и 2D</option>
                      <option value="preset_vortex_helix">3. Вихрь и винтовая линия: [x₀cos t - y₀sin t; x₀sin t + y₀cos t; t]</option>
                      <option value="preset_unstable_node">4. Неустойчивый узел (Источник): [x₀·e^t; y₀·e^(2t); t]</option>
                      <option value="preset_surface_lift">5. Подъём γ(t) на поверхность: [x₀e^(0.5t); y₀e^(-0.5t); x²-y²]</option>
                    </select>
                  </div>

                  <!-- Компоненты кривой F(γ(t)) = [x(t); y(t); z(t)] -->
                  <div>
                    <div class="vf-label">
                      <span>📈 Кривая <b>γ(t) = [x(t); y(t)]</b> и подъём <b>F(γ(t)) = [x(t); y(t); z(t)]</b>:</span>
                      <span style="color:#0d9488;font-weight:600;">зависит от t, x₀, y₀</span>
                    </div>
                    <div class="vf-comp-row">
                      <div class="vf-comp-box">
                        <span>x(t)=</span>
                        <input id="vf-x-expr" type="text" value="x0 * e^(2*t)" title="Координата x(t) кривой γ(t)" />
                      </div>
                      <div class="vf-comp-box">
                        <span>y(t)=</span>
                        <input id="vf-y-expr" type="text" value="y0 * e^(-t)" title="Координата y(t) кривой γ(t)" />
                      </div>
                      <div class="vf-comp-box">
                        <span style="color:#dc2626;">z(t)=</span>
                        <input id="vf-z-expr" type="text" value="t" title="3-я координата z(t) для 3D графика F(γ(t))" />
                      </div>
                    </div>
                  </div>

                  <!-- Векторное поле V(x, y, z) = [P, Q, R] -->
                  <div>
                    <div class="vf-label">
                      <span>🧭 Векторное поле <b>V(x,y,z) = [x', y', z']</b>:</span>
                      <label style="font-weight:600;color:#2563eb;cursor:pointer;display:flex;align-items:center;gap:3px;">
                        <input id="vf-auto-field" type="checkbox" checked /> авто из γ'(t)
                      </label>
                    </div>
                    <div class="vf-comp-row">
                      <div class="vf-comp-box">
                        <span style="color:#0d9488;">P=</span>
                        <input id="vf-u-expr" type="text" value="2*x" title="Компонента поля по X (dx/dt)" />
                      </div>
                      <div class="vf-comp-box">
                        <span style="color:#0d9488;">Q=</span>
                        <input id="vf-v-expr" type="text" value="-y" title="Компонента поля по Y (dy/dt)" />
                      </div>
                      <div class="vf-comp-box">
                        <span style="color:#0d9488;">R=</span>
                        <input id="vf-w-expr" type="text" value="1" title="Компонента поля по Z (dz/dt)" />
                      </div>
                    </div>
                  </div>
                </div>

                <!-- ПОЛЗУНКИ ПАРАМЕТРОВ t, x0, y0, t_max -->
                <div class="vf-sliders-grid">
                  <!-- Ползунок времени t -->
                  <div class="vf-slider-card" style="border-color:#93c5fd;background:#f0f7ff;">
                    <div class="vf-slider-head">
                      <span>⏱️ Время <b>t</b> (точка на кривой):</span>
                      <div style="display:flex;align-items:center;gap:4px;">
                        <button id="vf-play-t" class="vf-play-btn" title="Анимировать построение по времени t">▶</button>
                        <span id="vf-val-t" class="vf-val-pill">0.55</span>
                      </div>
                    </div>
                    <input id="vf-sl-t" type="range" min="-1.2" max="1.2" step="0.02" value="0.55" style="width:100%;accent-color:#2563eb;" />
                  </div>

                  <!-- Ползунок начальной координаты x0 -->
                  <div class="vf-slider-card">
                    <div class="vf-slider-head">
                      <span>📍 Старт <b>x₀ = x(0)</b>:</span>
                      <div style="display:flex;align-items:center;gap:4px;">
                        <button id="vf-play-x0" class="vf-play-btn" title="Анимировать изменение начальной координаты x₀">▶</button>
                        <span id="vf-val-x0" class="vf-val-pill">0.45</span>
                      </div>
                    </div>
                    <input id="vf-sl-x0" type="range" min="-2.0" max="2.0" step="0.02" value="0.45" style="width:100%;accent-color:#0d9488;" />
                  </div>

                  <!-- Ползунок начальной координаты y0 -->
                  <div class="vf-slider-card">
                    <div class="vf-slider-head">
                      <span>📍 Старт <b>y₀ = y(0)</b>:</span>
                      <div style="display:flex;align-items:center;gap:4px;">
                        <button id="vf-play-y0" class="vf-play-btn" title="Анимировать изменение начальной координаты y₀">▶</button>
                        <span id="vf-val-y0" class="vf-val-pill">1.35</span>
                      </div>
                    </div>
                    <input id="vf-sl-y0" type="range" min="-2.0" max="2.0" step="0.02" value="1.35" style="width:100%;accent-color:#0d9488;" />
                  </div>

                  <!-- Ползунок интервала времени [t_min, t_max] -->
                  <div class="vf-slider-card">
                    <div class="vf-slider-head">
                      <span>📏 Охват времени <b>t ∈ [-T, +T]</b>:</span>
                      <div style="display:flex;align-items:center;gap:4px;">
                        <button id="vf-play-orbit" class="vf-play-btn" title="Вращать начальную точку (x₀, y₀) по кругу">🔄</button>
                        <span id="vf-val-tspan" class="vf-val-pill">±1.20</span>
                      </div>
                    </div>
                    <input id="vf-sl-tspan" type="range" min="0.4" max="3.5" step="0.05" value="1.20" style="width:100%;accent-color:#6366f1;" />
                  </div>
                </div>

                <!-- ЧИПЫ СЛОЕВ ПОСТРОЕНИЯ -->
                <div class="vf-chips-bar">
                  <div class="vf-chips-group">
                    <span style="font-size:11.5px;font-weight:700;color:#475569;">Слои построения:</span>
                    <div id="chip-curtain" class="vf-chip active" title="Показывает вертикальные линии подъёма от плоской кривой γ(t) на дне z=0 к 3D кривой F(γ(t))">📐 Шторка подъёма γ(t) → F(γ(t))</div>
                    <div id="chip-floor-curve" class="vf-chip active" title="Показывает плоскую кривую γ(t) = [x(t), y(t), 0] на плоскости z=0 в 3D">🟦 Тень γ(t) на плоскости z=0</div>
                    <div id="chip-2d-field" class="vf-chip active" title="Стрелки двумерного векторного поля V(x,y) = [x', y']">🧭 2D Поле стрелок</div>
                    <div id="chip-3d-field" class="vf-chip active" title="Трехмерные конусы и векторы поля V(x,y,z) в 3D пространстве">🚀 3D Векторное поле</div>
                    <div id="chip-bundle" class="vf-chip active" title="Семейство траекторий (фазовый портрет) для разных начальных точек (x₀, y₀)">🌊 Пучок траекторий (Фазовый портрет)</div>
                    <div id="chip-velocity" class="vf-chip active" title="Касательный вектор мгновенной скорости dF/dt в точке t">🎯 Вектор скорости F'(γ(t))</div>
                    <div id="chip-surface" class="vf-chip" title="Показать поверхность z = f(x,y), если z задана через x и y">🏔️ Поверхность z(x,y)</div>
                    <div id="chip-2d" class="vf-chip active" title="Показывать 2D фазовую плоскость рядом с 3D графиком">🗺️ 3D + 2D рядом</div>
                  </div>
                </div>

                <!-- СТАТУС И НАЗВАНИЕ -->
                <div class="vf-status-banner">
                  <div id="vf-title" style="font-weight:800;color:#0f172a;">
                    F(γ(t)) = [x₀·e^(2t); y₀·e^(-t); t] — Седловой поток в 3D и 2D
                  </div>
                  <div id="vf-status" style="font-size:12px;color:#1d4ed8;font-weight:600;">
                    ⚡ Кликните по любой точке 2D-графика справа, чтобы перенести старт (x₀, y₀)
                  </div>
                </div>

                <!-- ГЛАВНЫЙ ХОЛСТ PLOTLY (3D СЛЕВА + 2D ФАЗОВАЯ ПЛОСКОСТЬ СПРАВА) -->
                <div id="vf-plot-wrap" style="position:relative;width:100%;height:610px;margin-top:8px;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;background:#ffffff;">
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
                            <option value="point">📍 Точка старта (x₀, y₀)</option>
                            <option value="time_t">⏱️ Время t на кривой</option>
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

                <!-- ПОШАГОВОЕ ОБЪЯСНЕНИЕ "КАК ЭТО СТРОИТСЯ" С ЖИВЫМИ ЧИСЛАМИ -->
                <div id="vf-steps-bar" class="vf-step-cards"></div>
              </div>
            `;

            const dom = {
              apiKey: el.querySelector("#vf-apikey"),
              micBtn: el.querySelector("#vf-mic-btn"),
              lang: el.querySelector("#vf-lang"),
              camBtn: el.querySelector("#vf-cam-btn"),
              nlInput: el.querySelector("#vf-nl-input"),
              nlRun: el.querySelector("#vf-nl-run"),
              nlAi: el.querySelector("#vf-nl-ai"),
              voiceLive: el.querySelector("#vf-voice-live"),
              preset: el.querySelector("#vf-preset"),
              xExpr: el.querySelector("#vf-x-expr"),
              yExpr: el.querySelector("#vf-y-expr"),
              zExpr: el.querySelector("#vf-z-expr"),
              uExpr: el.querySelector("#vf-u-expr"),
              vExpr: el.querySelector("#vf-v-expr"),
              wExpr: el.querySelector("#vf-w-expr"),
              autoField: el.querySelector("#vf-auto-field"),
              slT: el.querySelector("#vf-sl-t"),
              slX0: el.querySelector("#vf-sl-x0"),
              slY0: el.querySelector("#vf-sl-y0"),
              slTspan: el.querySelector("#vf-sl-tspan"),
              valT: el.querySelector("#vf-val-t"),
              valX0: el.querySelector("#vf-val-x0"),
              valY0: el.querySelector("#vf-val-y0"),
              valTspan: el.querySelector("#vf-val-tspan"),
              playT: el.querySelector("#vf-play-t"),
              playX0: el.querySelector("#vf-play-x0"),
              playY0: el.querySelector("#vf-play-y0"),
              playOrbit: el.querySelector("#vf-play-orbit"),
              chipCurtain: el.querySelector("#chip-curtain"),
              chipFloorCurve: el.querySelector("#chip-floor-curve"),
              chip2dField: el.querySelector("#chip-2d-field"),
              chip3dField: el.querySelector("#chip-3d-field"),
              chipBundle: el.querySelector("#chip-bundle"),
              chipVelocity: el.querySelector("#chip-velocity"),
              chipSurface: el.querySelector("#chip-surface"),
              chip2d: el.querySelector("#chip-2d"),
              title: el.querySelector("#vf-title"),
              status: el.querySelector("#vf-status"),
              plot: el.querySelector("#vf-plot"),
              stepsBar: el.querySelector("#vf-steps-bar"),
              camPip: el.querySelector("#vf-cam-pip"),
              camHeader: el.querySelector("#vf-cam-header"),
              camVideo: el.querySelector("#vf-cam-video"),
              camCanvas: el.querySelector("#vf-cam-canvas"),
              camTarget: el.querySelector("#vf-cam-target"),
              camSpeed: el.querySelector("#vf-cam-speed"),
              camSpeedVal: el.querySelector("#vf-cam-speed-val"),
              camStatusMsg: el.querySelector("#vf-cam-status-msg"),
              camResetBtn: el.querySelector("#vf-cam-reset-btn"),
              camSnapBtn: el.querySelector("#vf-cam-snap-btn"),
              camCloseBtn: el.querySelector("#vf-cam-close-btn"),
            };

            const JS_PRESETS = {
              preset_saddle_exp: {
                preset_id: "preset_saddle_exp",
                title: "F(γ(t)) = [x₀·e^(2t); y₀·e^(-t); t] — Седловой поток в 3D и 2D",
                full_formula: "[x0*e^2t; y0*e^(-t); t]",
                x_expr: "x0 * e^(2*t)", y_expr: "y0 * e^(-t)", z_expr: "t",
                u_expr: "2*x", v_expr: "-y", w_expr: "1", auto_field: true,
                x0: 0.45, y0: 1.35, t_val: 0.55, t_min: -1.2, t_max: 1.2, xy_range: [-2.6, 2.6],
                show_2d_field: true, show_3d_field: true, show_curtain: true,
                show_bundle: true, show_velocity: true, show_floor_curve: true,
                show_surface: false, split_2d: true, show_box_grid: true, anim_mode: "none",
                status: "⚡ Седловой поток: по X растяжение e^(2t), по Y сжатие e^(-t), по Z подъём t"
              },
              preset_spiral_sink: {
                preset_id: "preset_spiral_sink",
                title: "F(γ(t)) = [e^(-0.35t)(x₀cos 2t - y₀sin 2t); e^(-0.35t)(x₀sin 2t + y₀cos 2t); t] — Спиральный фокус",
                full_formula: "[e^(-0.35*t)*(x0*cos(2*t) - y0*sin(2*t)); e^(-0.35*t)*(x0*sin(2*t) + y0*cos(2*t)); t]",
                x_expr: "e^(-0.35*t)*(x0*cos(2*t) - y0*sin(2*t))",
                y_expr: "e^(-0.35*t)*(x0*sin(2*t) + y0*cos(2*t))",
                z_expr: "t",
                u_expr: "-0.35*x - 2*y", v_expr: "2*x - 0.35*y", w_expr: "1", auto_field: true,
                x0: 1.60, y0: 1.10, t_val: 1.40, t_min: -0.8, t_max: 3.2, xy_range: [-2.6, 2.6],
                show_2d_field: true, show_3d_field: true, show_curtain: true,
                show_bundle: true, show_velocity: true, show_floor_curve: true,
                show_surface: false, split_2d: true, show_box_grid: true, anim_mode: "none",
                status: "🌀 Спиральный фокус: в 2D скручивается к (0,0), в 3D — коническая спираль вдоль t"
              },
              preset_vortex_helix: {
                preset_id: "preset_vortex_helix",
                title: "F(γ(t)) = [x₀cos(t) - y₀sin(t); x₀sin(t) + y₀cos(t); t] — Вихревой поток и винтовая линия",
                full_formula: "[x0*cos(t) - y0*sin(t); x0*sin(t) + y0*cos(t); t]",
                x_expr: "x0*cos(t) - y0*sin(t)", y_expr: "x0*sin(t) + y0*cos(t)", z_expr: "t",
                u_expr: "-y", v_expr: "x", w_expr: "1", auto_field: true,
                x0: 1.50, y0: 0.50, t_val: 1.80, t_min: -2.0, t_max: 3.5, xy_range: [-2.5, 2.5],
                show_2d_field: true, show_3d_field: true, show_curtain: true,
                show_bundle: true, show_velocity: true, show_floor_curve: true,
                show_surface: false, split_2d: true, show_box_grid: true, anim_mode: "none",
                status: "🎡 Вихревое поле V = [-y, x]: в 2D окружность γ(t), в 3D — классическая винтовая линия"
              },
              preset_unstable_node: {
                preset_id: "preset_unstable_node",
                title: "F(γ(t)) = [x₀·e^t; y₀·e^(2t); t] — Неустойчивый узел (Источник)",
                full_formula: "[x0*e^t; y0*e^2t; t]",
                x_expr: "x0 * e^t", y_expr: "y0 * e^(2*t)", z_expr: "t",
                u_expr: "x", v_expr: "2*y", w_expr: "1", auto_field: true,
                x0: 0.65, y0: 0.35, t_val: 0.50, t_min: -1.5, t_max: 1.1, xy_range: [-2.6, 2.6],
                show_2d_field: true, show_3d_field: true, show_curtain: true,
                show_bundle: true, show_velocity: true, show_floor_curve: true,
                show_surface: false, split_2d: true, show_box_grid: true, anim_mode: "none",
                status: "🚀 Источник V = [x, 2y]: в 2D параболический разлёт y = C·x², в 3D — подъём по t"
              },
              preset_surface_lift: {
                preset_id: "preset_surface_lift",
                title: "F(γ(t)) = [x₀·e^(0.5t); y₀·e^(-0.5t); x² - y²] — Подъём кривой γ(t) на поверхность z = x² - y²",
                full_formula: "[x0*e^(0.5*t); y0*e^(-0.5*t); x^2 - y^2]",
                x_expr: "x0 * e^(0.5*t)", y_expr: "y0 * e^(-0.5*t)", z_expr: "x^2 - y^2",
                u_expr: "0.5*x", v_expr: "-0.5*y", w_expr: "x^2 + y^2", auto_field: true,
                x0: 0.80, y0: 1.30, t_val: 0.60, t_min: -1.6, t_max: 1.6, xy_range: [-2.4, 2.4],
                show_2d_field: true, show_3d_field: true, show_curtain: true,
                show_bundle: true, show_velocity: true, show_floor_curve: true,
                show_surface: true, split_2d: true, show_box_grid: true, anim_mode: "none",
                status: "⛰️ Плоская траектория γ(t) поднимается на седловую поверхность z = x² - y²"
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
              const tSpan = Math.max(0.4, Math.max(Math.abs(tMin), Math.abs(tMax)));

              dom.slT.min = tMin.toFixed(2);
              dom.slT.max = tMax.toFixed(2);
              dom.slT.step = ((tMax - tMin) / 180).toFixed(4);
              dom.slT.value = Number(state.t_val ?? 0.55);

              dom.slX0.value = Number(state.x0 ?? 0.45);
              dom.slY0.value = Number(state.y0 ?? 1.35);
              dom.slTspan.value = tSpan;

              dom.valT.textContent = Number(state.t_val ?? 0.55).toFixed(2);
              dom.valX0.textContent = Number(state.x0 ?? 0.45).toFixed(2);
              dom.valY0.textContent = Number(state.y0 ?? 1.35).toFixed(2);
              dom.valTspan.textContent = `±${tSpan.toFixed(2)}`;
            }

            function syncControlsFromState() {
              if (state.preset_id && dom.preset.value !== state.preset_id) {
                dom.preset.value = state.preset_id;
              }
              dom.xExpr.value = state.x_expr || "x0 * e^(2*t)";
              dom.yExpr.value = state.y_expr || "y0 * e^(-t)";
              dom.zExpr.value = state.z_expr || "t";
              dom.uExpr.value = state.u_expr || "2*x";
              dom.vExpr.value = state.v_expr || "-y";
              dom.wExpr.value = state.w_expr || "1";
              dom.autoField.checked = state.auto_field !== false;
              dom.nlInput.value = state.full_formula || `[${dom.xExpr.value}; ${dom.yExpr.value}; ${dom.zExpr.value}]`;

              const setChip = (chip, on) => chip && chip.classList.toggle("active", !!on);
              setChip(dom.chipCurtain, state.show_curtain);
              setChip(dom.chipFloorCurve, state.show_floor_curve);
              setChip(dom.chip2dField, state.show_2d_field);
              setChip(dom.chip3dField, state.show_3d_field);
              setChip(dom.chipBundle, state.show_bundle);
              setChip(dom.chipVelocity, state.show_velocity);
              setChip(dom.chipSurface, state.show_surface);
              setChip(dom.chip2d, state.split_2d);

              const mode = state.anim_mode || "none";
              dom.playT.classList.toggle("playing", mode === "t");
              dom.playT.textContent = mode === "t" ? "⏸" : "▶";
              dom.playX0.classList.toggle("playing", mode === "x0");
              dom.playX0.textContent = mode === "x0" ? "⏸" : "▶";
              dom.playY0.classList.toggle("playing", mode === "y0");
              dom.playY0.textContent = mode === "y0" ? "⏸" : "▶";
              dom.playOrbit.classList.toggle("playing", mode === "orbit");
              dom.playOrbit.textContent = mode === "orbit" ? "⏸" : "🔄";

              dom.title.textContent = state.title || `F(γ(t)) = [${dom.xExpr.value}; ${dom.yExpr.value}; ${dom.zExpr.value}]`;
              dom.status.textContent = state.status || "⚡ Готово";

              syncSliderThumbsOnly();
              updateAnimationLoop();
            }

            // Плавный 60 FPS цикл анимации ползунков (включается только по кнопке ▶ или явному запросу)
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

                if (!userDraggingSlider) {
                  animPhase += dt * 1.15;
                  const tMin = Number(state.t_min ?? -1.2);
                  const tMax = Number(state.t_max ?? 1.2);
                  const tMid = 0.5 * (tMin + tMax);
                  const tAmp = 0.48 * (tMax - tMin);

                  if (curMode === "t") {
                    state.t_val = tMid + tAmp * Math.sin(animPhase);
                  } else if (curMode === "x0") {
                    state.x0 = 1.4 * Math.sin(animPhase);
                  } else if (curMode === "y0") {
                    state.y0 = 1.4 * Math.sin(animPhase);
                  } else if (curMode === "orbit") {
                    state.x0 = 1.2 * Math.cos(animPhase);
                    state.y0 = 1.2 * Math.sin(animPhase);
                  }
                  syncSliderThumbsOnly();
                  renderPlot();
                }
                animRaf = requestAnimationFrame(stepAnim);
              }
              animRaf = requestAnimationFrame(stepAnim);
            }

            // Парсинг строки вида [x0*e^2t; y0*e^(-t); t] на клиенте за < 0.2 мс
            function applyQuickInputCommand(rawStr) {
              const s = String(rawStr || "").trim();
              if (!s) return;

              // Если есть квадратные скобки [x(t); y(t); z(t)] или точка с запятой
              const br = s.match(/\[\s*([^\]]+)\s*\]/);
              let inner = br ? br[1] : (s.includes(";") ? s.replace(/^.*?=\s*/, "") : "");
              if (inner) {
                const sep = inner.includes(";") ? ";" : ",";
                const parts = inner.split(sep).map(p => p.trim()).filter(Boolean);
                if (parts.length >= 2) {
                  state.x_expr = parts[0];
                  state.y_expr = parts[1];
                  state.z_expr = parts[2] || "t";
                  state.full_formula = `[${state.x_expr}; ${state.y_expr}; ${state.z_expr}]`;
                  const uInf = inferSymbolicVelocity(state.x_expr, "x");
                  const vInf = inferSymbolicVelocity(state.y_expr, "y");
                  const wInf = inferSymbolicVelocity(state.z_expr, "z");
                  if (uInf) state.u_expr = uInf;
                  if (vInf) state.v_expr = vInf;
                  if (wInf) state.w_expr = wInf;
                  state.auto_field = true;
                  state.title = `F(γ(t)) = [${state.x_expr}; ${state.y_expr}; ${state.z_expr}]`;
                  state.status = `✅ Построен поток F(γ(t)) = ${state.full_formula}`;
                  syncControlsFromState();
                  renderPlot();
                }
              }
            }

            function sendToPython(cmdText, useAi = false, presetId = "") {
              if (presetId && JS_PRESETS[presetId]) {
                state = JSON.parse(JSON.stringify(JS_PRESETS[presetId]));
                syncControlsFromState();
                renderPlot();
              } else if (cmdText && !useAi) {
                applyQuickInputCommand(cmdText);
              }
              const seq = (model.get("cmd_seq") || 0) + 1;
              model.set("api_key", dom.apiKey.value.trim());
              model.set("cmd_request", {
                seq,
                command: cmdText,
                use_ai: useAi,
                preset_id: presetId,
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
              const txt = dom.nlInput.value.trim() || "покажи интересный 3D поток F(gamma(t))";
              dom.status.textContent = "🤖 Запрос к Gemini 2.5 Flash...";
              sendToPython(txt, true, "");
            });
            dom.preset.addEventListener("change", () => {
              sendToPython("", false, dom.preset.value);
            });

            function applyComponentInputs() {
              if (isApplyingModelUpdate) return;
              state.x_expr = dom.xExpr.value.trim() || "x0 * e^(2*t)";
              state.y_expr = dom.yExpr.value.trim() || "y0 * e^(-t)";
              state.z_expr = dom.zExpr.value.trim() || "t";
              state.auto_field = dom.autoField.checked;

              if (state.auto_field) {
                const uInf = inferSymbolicVelocity(state.x_expr, "x");
                const vInf = inferSymbolicVelocity(state.y_expr, "y");
                const wInf = inferSymbolicVelocity(state.z_expr, "z");
                if (uInf) { state.u_expr = uInf; dom.uExpr.value = uInf; }
                if (vInf) { state.v_expr = vInf; dom.vExpr.value = vInf; }
                if (wInf) { state.w_expr = wInf; dom.wExpr.value = wInf; }
              } else {
                state.u_expr = dom.uExpr.value.trim() || "2*x";
                state.v_expr = dom.vExpr.value.trim() || "-y";
                state.w_expr = dom.wExpr.value.trim() || "1";
              }

              state.full_formula = `[${state.x_expr}; ${state.y_expr}; ${state.z_expr}]`;
              dom.nlInput.value = state.full_formula;
              state.title = `F(γ(t)) = ${state.full_formula}`;
              state.status = `⚡ Обновлена вектор-функция: F(γ(t)) = ${state.full_formula}`;
              renderPlot();
            }

            [dom.xExpr, dom.yExpr, dom.zExpr, dom.uExpr, dom.vExpr, dom.wExpr].forEach((inp) => {
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

            // Ползунки
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

            dom.slTspan.addEventListener("input", () => {
              const span = parseFloat(dom.slTspan.value) || 1.2;
              state.t_min = -span;
              state.t_max = span;
              if (state.t_val < state.t_min) state.t_val = state.t_min;
              if (state.t_val > state.t_max) state.t_val = state.t_max;
              syncSliderThumbsOnly();
              renderPlot();
            });

            function toggleAnim(mode) {
              state.anim_mode = state.anim_mode === mode ? "none" : mode;
              syncControlsFromState();
            }
            dom.playT.addEventListener("click", () => toggleAnim("t"));
            dom.playX0.addEventListener("click", () => toggleAnim("x0"));
            dom.playY0.addEventListener("click", () => toggleAnim("y0"));
            dom.playOrbit.addEventListener("click", () => toggleAnim("orbit"));

            // Чипы слоёв
            [
              [dom.chipCurtain, "show_curtain"],
              [dom.chipFloorCurve, "show_floor_curve"],
              [dom.chip2dField, "show_2d_field"],
              [dom.chip3dField, "show_3d_field"],
              [dom.chipBundle, "show_bundle"],
              [dom.chipVelocity, "show_velocity"],
              [dom.chipSurface, "show_surface"],
              [dom.chip2d, "split_2d"],
            ].forEach(([chip, key]) => {
              chip.addEventListener("click", () => {
                state[key] = !state[key];
                syncControlsFromState();
                renderPlot();
              });
            });

            // Голосовое управление Web Speech API
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
            // ВЕБ-КАМЕРА: ТРЕКИНГ ЖЕСТОВ ДЛЯ 3D-СЦЕНЫ, ТОЧКИ (x0, y0) И ВРЕМЕНИ t
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
            let camTheta = -2.25;
            let camPhi = 0.42;
            let camDist = 2.25;
            let currentEye = { x: -1.42, y: -1.48, z: 1.05 };

            function syncSphericalFromEye(eye) {
              if (!eye) return;
              const x = Number(eye.x) || -1.42;
              const y = Number(eye.y) || -1.48;
              const z = Number(eye.z) || 1.05;
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
              camTheta = -2.25; camPhi = 0.42; camDist = 2.25;
              angVelTheta = 0; angVelPhi = 0;
              applyCameraEye();
            });
            dom.camSnapBtn.addEventListener("click", () => {
              if (window.Plotly && dom.plot) {
                Plotly.downloadImage(dom.plot, { format: "png", width: 1600, height: 1000, filename: "vector_field_flow" });
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
                      const targetT = tMin + (1 - (normY + 1) * 0.5) * (tMax - tMin);
                      state.t_val = Number((state.t_val * 0.84 + targetT * 0.16).toFixed(2));
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
            // ВЫСОКОСКОРОСТНОЙ РЕНДЕР 3D И 2D ВЕКТОРНОГО ПОЛЯ И КРИВОЙ F(gamma(t))
            // =========================================================================
            let plotInitialized = false;

            function renderPlot() {
              loadPlotly().then((Plotly) => {
                const xFn = compileFlowExpr(state.x_expr || "x0 * e^(2*t)", 0);
                const yFn = compileFlowExpr(state.y_expr || "y0 * e^(-t)", 0);
                const zFn = compileFlowExpr(state.z_expr || "t", 0);

                const uExplicit = compileFlowExpr(state.u_expr || "2*x", 0);
                const vExplicit = compileFlowExpr(state.v_expr || "-y", 0);
                const wExplicit = compileFlowExpr(state.w_expr || "1", 1);

                const useAutoField = state.auto_field !== false;

                // Функция вычисления точки кривой F(γ(t)) = [x(t), y(t), z(t)]
                function evalPoint(t, x0, y0) {
                  let xv = xFn(t, x0, y0, x0, y0, t);
                  let yv = yFn(t, x0, y0, xv, y0, t);
                  if (!isFinite(xv)) xv = 0;
                  if (!isFinite(yv)) yv = 0;
                  xv = Math.max(-15, Math.min(15, xv));
                  yv = Math.max(-15, Math.min(15, yv));
                  let zv = zFn(t, x0, y0, xv, yv, t);
                  if (!isFinite(zv)) zv = 0;
                  zv = Math.max(-15, Math.min(15, zv));
                  return [xv, yv, zv];
                }

                // Численная производная F'(γ(t)) = [x'(t), y'(t), z'(t)] вдоль траектории
                function evalCurveDerivative(t, x0, y0) {
                  const dt = 1e-4;
                  const p1 = evalPoint(t + dt, x0, y0);
                  const p0 = evalPoint(t - dt, x0, y0);
                  return [
                    (p1[0] - p0[0]) / (2 * dt),
                    (p1[1] - p0[1]) / (2 * dt),
                    (p1[2] - p0[2]) / (2 * dt),
                  ];
                }

                // Вычисление вектора поля V(x, y, z) в произвольной точке пространства (x, y, z)
                function evalVectorField(x, y, z) {
                  if (useAutoField) {
                    // Инфинитезимальный генератор потока при t = 0 из точки (x0=x, y0=y)
                    const p0 = evalPoint(0, x, y);
                    if (Math.hypot(p0[0] - x, p0[1] - y) < 0.25) {
                      return evalCurveDerivative(0, x, y);
                    }
                  }
                  const u = uExplicit(z, state.x0, state.y0, x, y, z);
                  const v = vExplicit(z, state.x0, state.y0, x, y, z);
                  const w = wExplicit(z, state.x0, state.y0, x, y, z);
                  return [
                    isFinite(u) ? u : 0,
                    isFinite(v) ? v : 0,
                    isFinite(w) ? w : 1,
                  ];
                }

                const x0 = Number(state.x0 ?? 0.45);
                const y0 = Number(state.y0 ?? 1.35);
                const tMin = Number(state.t_min ?? -1.2);
                const tMax = Number(state.t_max ?? 1.2);
                const tStar = Math.max(tMin, Math.min(tMax, Number(state.t_val ?? 0.55)));

                // 1. Вычисляем главную кривую γ(t) и F(γ(t)) на всем интервале [tMin, tMax]
                const M = 130;
                const fullX = [], fullY = [], fullZ = [], fullZero = [], fullT = [];
                // Активный участок от tMin до текущего t*
                const actX = [], actY = [], actZ = [], actZero = [];

                let maxAbsXY = 2.4;
                let zMinBound = Math.min(-0.5, tMin);
                let zMaxBound = Math.max(1.2, tMax);

                for (let i = 0; i <= M; i++) {
                  const ti = tMin + ((tMax - tMin) * i) / M;
                  const [px, py, pz] = evalPoint(ti, x0, y0);
                  fullX.push(px);
                  fullY.push(py);
                  fullZ.push(pz);
                  fullZero.push(0);
                  fullT.push(ti);

                  if (Math.abs(px) < 8 && Math.abs(py) < 8) {
                    maxAbsXY = Math.max(maxAbsXY, Math.abs(px) * 1.15, Math.abs(py) * 1.15);
                  }
                  if (Math.abs(pz) < 10) {
                    zMinBound = Math.min(zMinBound, pz);
                    zMaxBound = Math.max(zMaxBound, pz);
                  }

                  if (ti <= tStar + 1e-6) {
                    actX.push(px);
                    actY.push(py);
                    actZ.push(pz);
                    actZero.push(0);
                  }
                }
                maxAbsXY = Math.min(6.0, Math.max(2.4, maxAbsXY));
                const zSpan = Math.max(1.5, zMaxBound - zMinBound);

                // Точка при t = 0 (начальное условие) и при текущем t = t*
                const [startX, startY, startZ] = evalPoint(0, x0, y0);
                const [curX, curY, curZ] = evalPoint(tStar, x0, y0);
                const [velX, velY, velZ] = evalCurveDerivative(tStar, x0, y0);
                const velNorm = Math.hypot(velX, velY, velZ);

                const traces = [];
                const is2D = state.split_2d !== false;

                // =================================================================
                // СЛОЙ 1: БАЗОВАЯ ПЛОСКОСТЬ z = 0 В 3D (ДНО С КООРДИНАТНОЙ СЕТКОЙ)
                // =================================================================
                const R = maxAbsXY;
                traces.push({
                  type: "surface",
                  x: [[-R, R], [-R, R]],
                  y: [[-R, -R], [R, R]],
                  z: [[0, 0], [0, 0]],
                  colorscale: [[0, "#f1f5f9"], [1, "#e2e8f0"]],
                  showscale: false,
                  opacity: 0.42,
                  hoverinfo: "skip",
                  name: "Плоскость z = 0",
                });

                // Оси X и Y на плоскости z = 0
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

                // Опциональная поверхность z = f(x, y) (если включен чип Поверхность)
                if (state.show_surface) {
                  const Ns = 35;
                  const sX = [], sY = [], sZ = [];
                  for (let i = 0; i < Ns; i++) {
                    const vy = -R + (2 * R * i) / (Ns - 1);
                    const rX = [], rY = [], rZ = [];
                    for (let j = 0; j < Ns; j++) {
                      const vx = -R + (2 * R * j) / (Ns - 1);
                      let vz = zFn(tStar, x0, y0, vx, vy, 0);
                      if (!isFinite(vz)) vz = 0;
                      vz = Math.max(-10, Math.min(10, vz));
                      rX.push(vx); rY.push(vy); rZ.push(vz);
                    }
                    sX.push(rX); sY.push(rY); sZ.push(rZ);
                  }
                  traces.push({
                    type: "surface",
                    x: sX, y: sY, z: sZ,
                    colorscale: [[0, "#dbeafe"], [0.5, "#93c5fd"], [1, "#60a5fa"]],
                    showscale: false,
                    opacity: 0.48,
                    name: "z = f(x,y)",
                  });
                }

                // =================================================================
                // СЛОЙ 2: ПУЧОК ТРАЕКТОРИЙ (ФАЗОВЫЙ ПОРТРЕТ В 3D И НА ПЛОСКОСТИ)
                // =================================================================
                const bundleSeeds = [
                  [0.45, 1.4], [-0.45, 1.4], [-0.45, -1.4], [0.45, -1.4],
                  [0.22, 1.6], [-0.22, 1.6], [-0.22, -1.6], [0.22, -1.6],
                  [0.85, 0.9], [-0.85, 0.9], [-0.85, -0.9], [0.85, -0.9],
                ];
                if (state.show_bundle) {
                  const b3dX = [], b3dY = [], b3dZ = [];
                  const bFlX = [], bFlY = [], bFlZ = [];
                  const Mb = 45;
                  for (const [sx, sy] of bundleSeeds) {
                    for (let i = 0; i <= Mb; i++) {
                      const ti = tMin + ((tMax - tMin) * i) / Mb;
                      const [bx, by, bz] = evalPoint(ti, sx, sy);
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
                  // Соседние 3D траектории F(γ(t))
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: b3dX, y: b3dY, z: b3dZ,
                    line: { color: "rgba(99, 102, 241, 0.35)", width: 2.5 },
                    name: "Пучок F(γ(t))",
                    hoverinfo: "skip",
                  });
                  // Соседние 2D траектории на дне z = 0
                  if (state.show_floor_curve) {
                    traces.push({
                      type: "scatter3d",
                      mode: "lines",
                      x: bFlX, y: bFlY, z: bFlZ,
                      line: { color: "rgba(148, 163, 184, 0.42)", width: 1.5 },
                      showlegend: false,
                      hoverinfo: "skip",
                    });
                  }
                }

                // =================================================================
                // СЛОЙ 3: 2D И 3D СТРЕЛКИ ВЕКТОРНОГО ПОЛЯ V(x, y, z) В 3D СЦЕНЕ
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
                        const ux = (u / mag) * len;
                        const uy = (v / mag) * len;
                        const ex = gx + ux, ey = gy + uy;
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
                    line: { color: "rgba(13, 148, 136, 0.55)", width: 2.5 },
                    name: "2D поле на z=0",
                    hoverinfo: "skip",
                  });
                }

                if (state.show_3d_field) {
                  const cX = [], cY = [], cZ = [], cU = [], cV = [], cW = [];
                  const G3 = 4;
                  const zLevels = [zMinBound * 0.6, 0, zMaxBound * 0.6];
                  for (const gz of zLevels) {
                    for (let i = 0; i < G3; i++) {
                      for (let j = 0; j < G3; j++) {
                        const gx = -R * 0.72 + (2 * R * 0.72 * j) / (G3 - 1);
                        const gy = -R * 0.72 + (2 * R * 0.72 * i) / (G3 - 1);
                        const [u, v, w] = evalVectorField(gx, gy, gz);
                        const norm = Math.hypot(u, v, w) || 1;
                        cX.push(gx); cY.push(gy); cZ.push(gz);
                        cU.push((u / norm) * 0.35);
                        cV.push((v / norm) * 0.35);
                        cW.push((w / norm) * 0.35);
                      }
                    }
                  }
                  traces.push({
                    type: "cone",
                    x: cX, y: cY, z: cZ,
                    u: cU, v: cV, w: cW,
                    sizemode: "absolute",
                    sizeref: 0.28,
                    anchor: "tail",
                    colorscale: [[0, "#38bdf8"], [1, "#0284c7"]],
                    showscale: false,
                    opacity: 0.55,
                    name: "3D Поле V(x,y,z)",
                    hoverinfo: "skip",
                  });
                }

                // =================================================================
                // СЛОЙ 4: ВЕРТИКАЛЬНАЯ ШТОРКА ПОДЪЁМА γ(t) -> F(γ(t))
                // =================================================================
                if (state.show_curtain && actX.length >= 2) {
                  // Полупрозрачная лента-стенка между (x(t), y(t), 0) и (x(t), y(t), z(t))
                  traces.push({
                    type: "surface",
                    x: [actX, actX],
                    y: [actY, actY],
                    z: [actZero, actZ],
                    colorscale: [[0, "rgba(59, 130, 246, 0.18)"], [1, "rgba(239, 68, 68, 0.36)"]],
                    showscale: false,
                    opacity: 0.34,
                    hoverinfo: "skip",
                    name: "Подъём γ(t) → F(γ(t))",
                  });

                  // Вертикальные столбики (pillars) через равные шаги по t
                  const pilX = [], pilY = [], pilZ = [];
                  const stepP = Math.max(1, Math.floor(actX.length / 14));
                  for (let k = 0; k < actX.length; k += stepP) {
                    pilX.push(actX[k], actX[k], null);
                    pilY.push(actY[k], actY[k], null);
                    pilZ.push(0, actZ[k], null);
                  }
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: pilX, y: pilY, z: pilZ,
                    line: { color: "rgba(37, 99, 235, 0.52)", width: 2, dash: "dot" },
                    showlegend: false,
                    hoverinfo: "skip",
                  });
                }

                // =================================================================
                // СЛОЙ 5: ПЛОСКАЯ КРИВАЯ γ(t) = [x(t), y(t), 0] И 3D КРИВАЯ F(γ(t))
                // =================================================================
                if (state.show_floor_curve) {
                  // Полная траектория γ(t) на плоскости z = 0 (пунктир)
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: fullX, y: fullY, z: fullZero,
                    line: { color: "rgba(37, 99, 235, 0.35)", width: 3, dash: "dash" },
                    name: "γ(t) полная",
                    hoverinfo: "skip",
                  });
                  // Пройденная часть γ(t) до t*
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: actX, y: actY, z: actZero,
                    line: { color: "#2563eb", width: 5 },
                    name: "γ(t) = [x(t), y(t), 0]",
                  });
                }

                // Будущая часть 3D кривой F(γ(t)) (тонкий пунктир)
                traces.push({
                  type: "scatter3d",
                  mode: "lines",
                  x: fullX, y: fullY, z: fullZ,
                  line: { color: "rgba(220, 38, 38, 0.35)", width: 3, dash: "dot" },
                  name: "F(γ(t)) продолжение",
                });

                // Главная построенная 3D кривая F(γ(t)) от t_min до t*
                traces.push({
                  type: "scatter3d",
                  mode: "lines",
                  x: actX, y: actY, z: actZ,
                  line: {
                    color: actZ,
                    colorscale: [[0, "#2563eb"], [0.5, "#10b981"], [1, "#dc2626"]],
                    width: 8,
                  },
                  name: "F(γ(t)) = [x(t), y(t), z(t)]",
                });

                // =================================================================
                // СЛОЙ 6: КЛЮЧЕВЫЕ ТОЧКИ (СТАРТ t=0, ТЕКУЩАЯ t=t* И ПРОЕКЦИИ)
                // =================================================================
                // Вертикальный перпендикуляр от γ(t*) на дне к F(γ(t*)) в 3D и линии к осям
                traces.push({
                  type: "scatter3d",
                  mode: "lines",
                  x: [curX, curX, null, curX, curX, null, curX, 0],
                  y: [curY, curY, null, curY, 0, null, curY, curY],
                  z: [0, curZ, null, 0, 0, null, 0, 0],
                  line: { color: "#0f172a", width: 3.5, dash: "dash" },
                  showlegend: false,
                  hoverinfo: "skip",
                });

                // Маркеры: Старт (t=0), Точка на плоскости γ(t*), Точка в 3D F(γ(t*))
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
                    `t=0: (${startX.toFixed(2)}, ${startY.toFixed(2)}, ${startZ.toFixed(2)})`,
                    `γ(${tStar.toFixed(2)}) = (${curX.toFixed(2)}, ${curY.toFixed(2)})`,
                    `F(γ(${tStar.toFixed(2)})) = [${curX.toFixed(2)}, ${curY.toFixed(2)}, ${curZ.toFixed(2)}]`,
                  ],
                  textposition: ["bottom center", "bottom center", "top center"],
                  textfont: { size: 11, color: "#0f172a" },
                  showlegend: false,
                });

                // Касательный вектор скорости dF/dt в точке t*
                if (state.show_velocity && velNorm > 1e-5) {
                  const vScale = Math.min(1.0, 0.65 / Math.max(0.5, velNorm));
                  const vxEnd = curX + velX * vScale;
                  const vyEnd = curY + velY * vScale;
                  const vzEnd = curZ + velZ * vScale;

                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: [curX, vxEnd],
                    y: [curY, vyEnd],
                    z: [curZ, vzEnd],
                    line: { color: "#059669", width: 6 },
                    name: "F'(γ(t)) скорость",
                  });
                  traces.push({
                    type: "cone",
                    x: [vxEnd], y: [vyEnd], z: [vzEnd],
                    u: [velX * 0.22], v: [velY * 0.22], w: [velZ * 0.22],
                    sizemode: "absolute",
                    sizeref: 0.22,
                    anchor: "tail",
                    colorscale: [[0, "#059669"], [1, "#10b981"]],
                    showscale: false,
                    hoverinfo: "skip",
                  });
                }

                // =================================================================
                // СЛОЙ 7: 2D ФАЗОВАЯ ПЛОСКОСТЬ (x, y) СПРАВА — КРИВАЯ γ(t) И ПОЛЕ V(x,y)
                // =================================================================
                if (is2D) {
                  // 7.1 Сетка стрелок 2D векторного поля V(x, y) = [u, v]
                  if (state.show_2d_field) {
                    const arrX = [], arrY = [];
                    const N2 = 13;
                    const step2 = (2 * R * 0.9) / (N2 - 1);
                    for (let i = 0; i < N2; i++) {
                      for (let j = 0; j < N2; j++) {
                        const gx = -R * 0.9 + j * step2;
                        const gy = -R * 0.9 + i * step2;
                        const [u, v] = evalVectorField(gx, gy, 0);
                        const mag = Math.hypot(u, v);
                        if (mag > 1e-5) {
                          const len = Math.min(step2 * 0.44, 0.14 + 0.14 * Math.tanh(mag * 0.35));
                          const dx = (u / mag) * len;
                          const dy = (v / mag) * len;
                          const ex = gx + dx;
                          const ey = gy + dy;
                          // Наконечник стрелки (два уса под углом 28 градусов)
                          const headLen = len * 0.35;
                          const ang = Math.atan2(dy, dx);
                          const hx1 = ex - headLen * Math.cos(ang - 0.5);
                          const hy1 = ey - headLen * Math.sin(ang - 0.5);
                          const hx2 = ex - headLen * Math.cos(ang + 0.5);
                          const hy2 = ey - headLen * Math.sin(ang + 0.5);

                          arrX.push(gx, ex, null, hx1, ex, hx2, null);
                          arrY.push(gy, ey, null, hy1, ey, hy2, null);
                        }
                      }
                    }
                    traces.push({
                      type: "scatter",
                      mode: "lines",
                      x: arrX, y: arrY,
                      xaxis: "x", yaxis: "y",
                      line: { color: "rgba(13, 148, 136, 0.55)", width: 1.4 },
                      hoverinfo: "skip",
                      showlegend: false,
                    });
                  }

                  // 7.2 Семейство фазовых кривых γ_k(t) на 2D плоскости
                  if (state.show_bundle) {
                    const phX = [], phY = [];
                    const Mp = 55;
                    for (const [sx, sy] of bundleSeeds) {
                      for (let i = 0; i <= Mp; i++) {
                        const ti = tMin + ((tMax - tMin) * i) / Mp;
                        const [bx, by] = evalPoint(ti, sx, sy);
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
                      line: { color: "rgba(99, 102, 241, 0.32)", width: 1.5, dash: "dot" },
                      hoverinfo: "skip",
                      showlegend: false,
                    });
                  }

                  // 7.3 Полная кривая γ(t) = [x(t), y(t)] на 2D (пунктир)
                  traces.push({
                    type: "scatter",
                    mode: "lines",
                    x: fullX, y: fullY,
                    xaxis: "x", yaxis: "y",
                    line: { color: "rgba(37, 99, 235, 0.35)", width: 2, dash: "dash" },
                    hoverinfo: "skip",
                    showlegend: false,
                  });

                  // 7.4 Активная часть γ(t) от t_min до t*
                  traces.push({
                    type: "scatter",
                    mode: "lines",
                    x: actX, y: actY,
                    xaxis: "x", yaxis: "y",
                    line: { color: "#2563eb", width: 4 },
                    name: "γ(t) в 2D",
                    showlegend: false,
                  });

                  // 7.5 Вектор скорости γ'(t*) на 2D графике
                  if (state.show_velocity && Math.hypot(velX, velY) > 1e-5) {
                    const v2Norm = Math.hypot(velX, velY);
                    const s2 = Math.min(0.85, 0.55 / Math.max(0.4, v2Norm));
                    const vx2 = curX + velX * s2;
                    const vy2 = curY + velY * s2;
                    traces.push({
                      type: "scatter",
                      mode: "lines+markers",
                      x: [curX, vx2],
                      y: [curY, vy2],
                      xaxis: "x", yaxis: "y",
                      line: { color: "#059669", width: 3.5 },
                      marker: { size: [0, 8], symbol: ["circle", "triangle-up"], color: "#059669" },
                      showlegend: false,
                    });
                  }

                  // 7.6 Точки на 2D графике: старт (x0, y0) и текущая γ(t*)
                  traces.push({
                    type: "scatter",
                    mode: "markers+text",
                    x: [startX, curX],
                    y: [startY, curY],
                    xaxis: "x", yaxis: "y",
                    marker: {
                      size: [10, 12],
                      color: ["#16a34a", "#dc2626"],
                      line: { width: 2, color: "#ffffff" },
                    },
                    text: [
                      `γ(0)=(${startX.toFixed(2)}, ${startY.toFixed(2)})`,
                      `γ(${tStar.toFixed(2)})=(${curX.toFixed(2)}, ${curY.toFixed(2)})`,
                    ],
                    textposition: ["bottom right", "top left"],
                    textfont: { size: 11, color: "#0f172a" },
                    showlegend: false,
                  });
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
                      text: "<b>3D Пространство: F(γ(t)) = [x(t), y(t), z(t)]</b>",
                      x: 0.28, y: 1.03, xref: "paper", yref: "paper",
                      showarrow: false, font: { size: 13, color: "#0f172a" }
                    },
                    {
                      text: "<b>2D Фазовая плоскость (x, y): кривая γ(t) = [x(t), y(t)] и поле V(x,y)</b>",
                      x: 0.83, y: 1.03, xref: "paper", yref: "paper",
                      showarrow: false, font: { size: 13, color: "#0f172a" }
                    }
                  ] : [],
                  scene: {
                    domain: is2D ? { x: [0.0, 0.58], y: [0.0, 0.98] } : { x: [0.0, 1.0], y: [0.0, 0.98] },
                    xaxis: { range: [-R, R], title: "x(t)", gridcolor: "#e2e8f0", zerolineColor: "#64748b" },
                    yaxis: { range: [-R, R], title: "y(t)", gridcolor: "#e2e8f0", zerolineColor: "#64748b" },
                    zaxis: { range: [zMinBound - 0.15 * zSpan, zMaxBound + 0.15 * zSpan], title: "z(t) / t", gridcolor: "#e2e8f0", zerolineColor: "#64748b" },
                    aspectmode: "manual",
                    aspectratio: { x: 1.15, y: 1.15, z: 0.95 },
                    camera: { eye: currentEye, up: { x: 0, y: 0, z: 1 } },
                  },
                };

                if (is2D) {
                  layout.xaxis = {
                    domain: [0.64, 0.99],
                    range: [-R, R],
                    title: "x(t)",
                    gridcolor: "#e2e8f0",
                    zeroline: true,
                    zerolinecolor: "#94a3b8",
                    zerolinewidth: 1.5,
                  };
                  layout.yaxis = {
                    domain: [0.06, 0.94],
                    range: [-R, R],
                    title: "y(t)",
                    scaleanchor: "x",
                    scaleratio: 1,
                    gridcolor: "#e2e8f0",
                    zeroline: true,
                    zerolinecolor: "#94a3b8",
                    zerolinewidth: 1.5,
                  };
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
                      if (typeof pt.x === "number" && typeof pt.y === "number") {
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

                // Обновление пошаговой карточки "Как это строится"
                dom.stepsBar.innerHTML = `
                  <div class="vf-step-card">
                    <b>Шаг 1. Начальная точка (t = 0)</b>
                    Задаём старт <code>(x₀, y₀) = (${x0.toFixed(2)}, ${y0.toFixed(2)})</code>.<br/>
                    При <code>t = 0</code>: <code>γ(0) = [${startX.toFixed(2)}; ${startY.toFixed(2)}]</code>
                  </div>
                  <div class="vf-step-card">
                    <b>Шаг 2. Кривая γ(t) в 2D при t = ${tStar.toFixed(2)}</b>
                    <code>x(${tStar.toFixed(2)}) = ${state.x_expr} = ${curX.toFixed(3)}</code><br/>
                    <code>y(${tStar.toFixed(2)}) = ${state.y_expr} = ${curY.toFixed(3)}</code>
                  </div>
                  <div class="vf-step-card">
                    <b>Шаг 3. Подъём в 3D: F(γ(t))</b>
                    Поднимаем точку <code>γ(t)</code> на высоту <code>z(t) = ${state.z_expr} = ${curZ.toFixed(3)}</code>:<br/>
                    <code>F(γ(${tStar.toFixed(2)})) = [${curX.toFixed(2)}; ${curY.toFixed(2)}; ${curZ.toFixed(2)}]</code>
                  </div>
                  <div class="vf-step-card">
                    <b>Шаг 4. Вектор поля / скорости F'(γ(t))</b>
                    Производная по <code>t</code> даёт касательный вектор:<br/>
                    <code>[x', y', z'] = [${velX.toFixed(2)}; ${velY.toFixed(2)}; ${velZ.toFixed(2)}]</code> (‖v‖ = ${velNorm.toFixed(2)})
                  </div>
                `;
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
            cur_st = req.get("current_state") or json.loads(self.state_json)

            if preset_id and preset_id in PRESET_STATES:
                next_st = dict(PRESET_STATES[preset_id])
                self.state_json = json.dumps(next_st, ensure_ascii=False)
                return

            if not cmd_text:
                return

            next_st, handled = parse_vector_command(cmd_text, cur_st)

            key = (self.api_key or env_key or "").strip()
            if use_ai or (not handled and key):
                ai_st, ai_ok, _ = ask_gemini_vector_ai(cmd_text, key, next_st if handled else cur_st)
                if ai_ok:
                    next_st = ai_st
                    handled = True

            if not handled:
                next_st["status"] = (
                    f"💬 Не удалось распознать «{cmd_text}». Введите в формате [x0*e^2t; y0*e^(-t); t] или нажмите 🤖 Gemini AI."
                )

            self.state_json = json.dumps(next_st, ensure_ascii=False)

    studio_widget = mo.ui.anywidget(
        VectorFieldFlowStudio(
            initial_state=dict(PRESET_STATES["preset_saddle_exp"]),
            initial_key="",
        )
    )
    studio_widget
    return (
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
    app.run()
