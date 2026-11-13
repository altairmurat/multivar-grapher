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
    # 2. ПРЕСЕТЫ ТЕМ (LECTURE 14 & MULTIVARIABLE CALCULUS)
    # =========================================================================
    PRESET_STATES = {
        "preset_lecture14": {
            "preset_id": "preset_lecture14",
            "title": "Lecture 14: Сечение поверхности y = x₁² - x₂² плоскостью y = c",
            "formula": "x1^2 - x2^2",
            "eval_z": "X1**2 - X2**2",
            "vector_u": "-x2",
            "vector_v": "x1",
            "x1_range": [-1.8, 1.8],
            "x2_range": [-1.8, 1.8],
            "a1": 0.55,
            "a2": 0.85,
            "c_val": -0.50,
            "extra_val": 0.90,
            "show_level_plane": True,
            "show_xy_traces": False,
            "show_tangent": False,
            "show_ball": False,
            "show_riemann": False,
            "show_vector_field": False,
            "circular_domain": True,
            "split_2d": False,
            "show_box_grid": False,
            "anim_mode": "none",
            "cam_active": False,
            "status": "⚡ Готово: Lecture 14 (все ползунки, поля и анимации активны)",
        },
        "preset_trace": {
            "preset_id": "preset_trace",
            "title": "Slices & Traces: Срезы z = sin(x₁)·cos(x₂) плоскостями x₁ = a₁ и x₂ = a₂",
            "formula": "sin(x1) * cos(x2)",
            "eval_z": "np.sin(X1) * np.cos(X2)",
            "vector_u": "-x2",
            "vector_v": "x1",
            "x1_range": [-3.2, 3.2],
            "x2_range": [-3.2, 3.2],
            "a1": 1.0,
            "a2": 0.6,
            "c_val": 0.0,
            "extra_val": 1.0,
            "show_level_plane": False,
            "show_xy_traces": True,
            "show_tangent": False,
            "show_ball": False,
            "show_riemann": False,
            "show_vector_field": False,
            "circular_domain": False,
            "split_2d": True,
            "show_box_grid": False,
            "anim_mode": "a2",
            "cam_active": False,
            "status": "🎬 Авто-анимация среза x₂ = a₂ запущена",
        },
        "preset_tangent": {
            "preset_id": "preset_tangent",
            "title": "Касательная плоскость, нормаль и градиент ∇f(a) к y = x₁² - x₂²",
            "formula": "x1^2 - x2^2",
            "eval_z": "X1**2 - X2**2",
            "vector_u": "-x2",
            "vector_v": "x1",
            "x1_range": [-1.8, 1.8],
            "x2_range": [-1.8, 1.8],
            "a1": 0.80,
            "a2": 0.45,
            "c_val": 0.44,
            "extra_val": 0.90,
            "show_level_plane": True,
            "show_xy_traces": False,
            "show_tangent": True,
            "show_ball": False,
            "show_riemann": False,
            "show_vector_field": False,
            "circular_domain": True,
            "split_2d": True,
            "show_box_grid": False,
            "anim_mode": "orbit",
            "cam_active": False,
            "status": "🎬 Авто-анимация точки a=(a₁, a₂) и касательной плоскости",
        },
        "preset_flow": {
            "preset_id": "preset_flow",
            "title": "Векторное поле F(x₁, x₂) = [-x₂, x₁] и линия тока r(t)",
            "formula": "0.15 * (x1^2 + x2^2)",
            "eval_z": "0.15 * (X1**2 + X2**2)",
            "vector_u": "-x2",
            "vector_v": "x1",
            "x1_range": [-2.8, 2.8],
            "x2_range": [-2.8, 2.8],
            "a1": 1.6,
            "a2": 0.3,
            "c_val": 0.4,
            "extra_val": 5.5,
            "show_level_plane": False,
            "show_xy_traces": False,
            "show_tangent": False,
            "show_ball": False,
            "show_riemann": False,
            "show_vector_field": True,
            "circular_domain": False,
            "split_2d": True,
            "show_box_grid": False,
            "anim_mode": "rnt",
            "cam_active": False,
            "status": "🎬 Авто-анимация потока векторного поля r(t)",
        },
        "preset_riemann": {
            "preset_id": "preset_riemann",
            "title": "Двойной интеграл и 3D суммы Римана: f(x₁, x₂) = 4 - x₁² - x₂²",
            "formula": "4 - x1^2 - x2^2",
            "eval_z": "4 - X1**2 - X2**2",
            "vector_u": "-x2",
            "vector_v": "x1",
            "x1_range": [-1.6, 1.6],
            "x2_range": [-1.6, 1.6],
            "a1": 0.7,
            "a2": 0.7,
            "c_val": 1.5,
            "extra_val": 7.0,
            "show_level_plane": False,
            "show_xy_traces": False,
            "show_tangent": False,
            "show_ball": False,
            "show_riemann": True,
            "show_vector_field": False,
            "circular_domain": False,
            "split_2d": False,
            "show_box_grid": False,
            "anim_mode": "rnt",
            "cam_active": False,
            "status": "🎬 Авто-анимация числа разбиений Римана N",
        },
        "preset_ball": {
            "preset_id": "preset_ball",
            "title": "Открытая окрестность B_r(a) и граница ∂B_r(a) вокруг точки a=(a₁, a₂)",
            "formula": "x1^2 + x2^2 - 1",
            "eval_z": "X1**2 + X2**2 - 1",
            "vector_u": "-x2",
            "vector_v": "x1",
            "x1_range": [-2.0, 2.0],
            "x2_range": [-2.0, 2.0],
            "a1": 0.55,
            "a2": 0.45,
            "c_val": -0.50,
            "extra_val": 0.85,
            "show_level_plane": True,
            "show_xy_traces": False,
            "show_tangent": False,
            "show_ball": True,
            "show_riemann": False,
            "show_vector_field": False,
            "circular_domain": True,
            "split_2d": True,
            "show_box_grid": False,
            "anim_mode": "rnt",
            "cam_active": False,
            "status": "🎬 Авто-анимация радиуса окрестности B_r(a)",
        },
    }

    # =========================================================================
    # 3. УНИВЕРСАЛЬНЫЙ ПАРСЕР МАТЕМАТИКИ, ДАННЫХ, ДИАПАЗОНОВ И АНИМАЦИЙ (RU/EN)
    # =========================================================================
    def normalize_spoken_math(text: str) -> str:
        """
        Переводит русскую и английскую устную/текстовую речь (включая Unicode-степени x1³ - x2²,
        индексы x₁, x₂, кириллические х1, х2, числительные и функции) в чистую запись.
        """
        s = (text or "").strip()
        unicode_replacements = {
            "⁰": "^0",
            "¹": "^1",
            "²": "^2",
            "³": "^3",
            "⁴": "^4",
            "⁵": "^5",
            "⁶": "^6",
            "⁷": "^7",
            "⁸": "^8",
            "⁹": "^9",
            "⁻": "-",
            "₁": "1",
            "₂": "2",
            "₃": "3",
            "−": "-",
            "–": "-",
            "—": "-",
            "×": "*",
            "·": "*",
            "∙": "*",
            "÷": "/",
            "π": "pi",
        }
        for u_ch, ascii_rep in unicode_replacements.items():
            s = s.replace(u_ch, ascii_rep)

        s = re.sub(r"√\s*\(([^)]+)\)", r"sqrt(\1)", s)
        s = re.sub(r"√\s*([a-zA-Z0-9_]+)", r"sqrt(\1)", s)
        s = re.sub(r"(\d),(\d)", r"\1.\2", s)

        spoken_nums = [
            (r"\bминус\s+полтора\b", "-1.5"),
            (r"\bполтора\b", "1.5"),
            (r"\bноль\s+целых\s+пять\s+десятых\b", "0.5"),
            (r"\bноль\s+пять\b", "0.5"),
            (r"\bноль\s+два\b", "0.2"),
            (r"\bноль\s+восемь\b", "0.8"),
            (r"\bноль\b", "0"),
            (r"\bнулю\b", "0"),
            (r"\bнуля\b", "0"),
            (r"\bzero\b", "0"),
            (r"\bединиц[аеыу]\b", "1"),
            (r"\bодин\b", "1"),
            (r"\bодной\b", "1"),
            (r"\bодного\b", "1"),
            (r"\bone\b", "1"),
            (r"\bдва\b", "2"),
            (r"\bдвух\b", "2"),
            (r"\btwo\b", "2"),
            (r"\bтри\b", "3"),
            (r"\bтрех\b", "3"),
            (r"\bтрёх\b", "3"),
            (r"\bthree\b", "3"),
            (r"\bчетыре\b", "4"),
            (r"\bчетырех\b", "4"),
            (r"\bfour\b", "4"),
            (r"\bпять\b", "5"),
            (r"\bпяти\b", "5"),
            (r"\bfive\b", "5"),
            (r"\bшесть\b", "6"),
            (r"\bшести\b", "6"),
            (r"\bsix\b", "6"),
            (r"\bсемь\b", "7"),
            (r"\bсеми\b", "7"),
            (r"\bseven\b", "7"),
            (r"\bвосемь\b", "8"),
            (r"\bвосьми\b", "8"),
            (r"\beight\b", "8"),
            (r"\bдевять\b", "9"),
            (r"\bдевяти\b", "9"),
            (r"\bnine\b", "9"),
            (r"\bдесять\b", "10"),
            (r"\bдесяти\b", "10"),
            (r"\bten\b", "10"),
            (r"\bдвенадцать\b", "12"),
            (r"\btwelve\b", "12"),
            (r"\bпятнадцать\b", "15"),
            (r"\bшестнадцать\b", "16"),
            (r"\bдвадцать\b", "20"),
        ]
        for pat, repl in spoken_nums:
            s = re.sub(pat, repl, s, flags=re.IGNORECASE)

        spoken_ops = [
            (r"(?<![a-zA-Zа-яА-Я])(?:а|a)\s*_?\s*1(?![a-zA-Zа-яА-Я0-9])", "a1"),
            (r"(?<![a-zA-Zа-яА-Я])(?:а|a)\s*_?\s*2(?![a-zA-Zа-яА-Я0-9])", "a2"),
            (r"(?<![a-zA-Zа-яА-Я])(?:икс|х|x)\s*_?\s*1(?![a-zA-Zа-яА-Я0-9])", "x1"),
            (r"(?<![a-zA-Zа-яА-Я])(?:икс|х|x)\s*_?\s*2(?![a-zA-Zа-яА-Я0-9])", "x2"),
            (r"\bигрек\b", "x2"),
            (r"\bикс\b", "x1"),
            (r"\bto\s+the\s+power\s+of\s*(\d+)\b", r"^\1"),
            (r"\bpower\s+of\s*(\d+)\b", r"^\1"),
            (r"\bpower\s*(\d+)\b", r"^\1"),
            (r"\bв\s+квадрате\b", "^2"),
            (r"\bквадрат\b", "^2"),
            (r"\bsquared\b", "^2"),
            (r"\bв\s+кубе\b", "^3"),
            (r"\bкуб\b", "^3"),
            (r"\bcubed\b", "^3"),
            (r"\bв\s+четвертой\s+степени\b", "^4"),
            (r"\bв\s+пятой\s+степени\b", "^5"),
            (r"\bв\s+степени\s*(\d+)\b", r"^\1"),
            (r"\bв\s+степени\b", "^"),
            (r"\bкорень\s+(?:из\s+)?([a-zA-Z0-9_\^\+\-\*]+)", r"sqrt(\1)"),
            (r"\bsquare\s+root\s+(?:of\s+)?([a-zA-Z0-9_\^\+\-\*]+)", r"sqrt(\1)"),
            (r"\b(?:синус(?:\s+от)?|sine\s+of|sine|sin\s+of|sin)\s*\(?\s*([a-zA-Z0-9_]+)\s*\)?", r"sin(\1)"),
            (r"\b(?:косинус(?:\s+от)?|cosine\s+of|cosine|cos\s+of|cos)\s*\(?\s*([a-zA-Z0-9_]+)\s*\)?", r"cos(\1)"),
            (r"\b(?:тангенс(?:\s+от)?|tangent\s+of|tangent|tan\s+of|tan)\s*\(?\s*([a-zA-Z0-9_]+)\s*\)?", r"tan(\1)"),
            (r"\b(?:экспонента(?:\s+от)?|exponential\s+of|exp\s+of)\s*\(?\s*([a-zA-Z0-9_]+)\s*\)?", r"exp(\1)"),
            (r"\b(?:логарифм(?:\s+от)?|ln|log)\s*\(?\s*([a-zA-Z0-9_]+)\s*\)?", r"log(\1)"),
            (r"\b(?:модуль|abs)\s*\(?\s*([a-zA-Z0-9_]+)\s*\)?", r"abs(\1)"),
            (r"\b(?:умножить\s+на|умножить|multiplied\s+by|times)\b", "*"),
            (r"\b(?:разделить\s+на|делить\s+на|деленное\s+на|divided\s+by|over)\b", "/"),
            (r"\b(?:плюс|plus|прибавить)\b", "+"),
            (r"\b(?:минус|minus|вычесть)\b", "-"),
            (r"\b(?:равно|равен|равна|равном|equals|equal\s+to)\b", "="),
        ]
        for pat, repl in spoken_ops:
            s = re.sub(pat, repl, s, flags=re.IGNORECASE)
        return s

    def clean_display_formula(expr_str: str) -> str:
        s = normalize_spoken_math(expr_str or "").strip()
        s = re.sub(r"^[fzy]\s*(\([^)]*\))?\s*=\s*", "", s, flags=re.IGNORECASE)
        s = s.replace("np.", "").replace("Math.", "").replace("**", "^")
        s = re.sub(r"(?<![a-zA-Z])X1(?![0-9])", "x1", s)
        s = re.sub(r"(?<![a-zA-Z])X2(?![0-9])", "x2", s)
        s = re.sub(r"\bx\b", "x1", s)
        s = re.sub(r"\by\b", "x2", s)
        s = re.sub(r"\s*\^\s*", "^", s)
        return s.strip() or "x1^2 - x2^2"

    def math_to_numpy(expr_str: str) -> str:
        s = normalize_spoken_math(expr_str or "")
        if not s:
            return "X1**2 - X2**2"
        s = re.sub(r"^[fzy]\s*(\([^)]*\))?\s*=\s*", "", s, flags=re.IGNORECASE)
        s = s.replace("Math.", "np.")
        s = s.replace("^", "**")
        s = re.sub(r"(\d)\s*([a-zA-Z\(])", r"\1*\2", s)
        s = re.sub(r"(\))\s*([a-zA-Z\d\(])", r"\1*\2", s)
        s = re.sub(r"(x_?[12])\s+(x_?[12])", r"\1*\2", s, flags=re.IGNORECASE)
        s = re.sub(r"(x_?[12])\s+(sin|cos|tan|exp|sqrt|log|abs)\b", r"\1*\2", s, flags=re.IGNORECASE)
        s = re.sub(r"(?<![a-zA-Z])x_?1(?![0-9])", "X1", s, flags=re.IGNORECASE)
        s = re.sub(r"(?<![a-zA-Z])x_?2(?![0-9])", "X2", s, flags=re.IGNORECASE)
        s = re.sub(r"\bx\b", "X1", s)
        s = re.sub(r"\by\b", "X2", s)
        for fn in ("sin", "cos", "tan", "exp", "sqrt", "log", "abs", "atan2", "arcsin", "arccos"):
            s = re.sub(rf"\b(?<!np\.){fn}\b", f"np.{fn}", s, flags=re.IGNORECASE)
        for fn in ("sin", "cos", "tan", "exp", "sqrt", "log", "abs"):
            s = re.sub(rf"\bnp\.{fn.upper()}\b", f"np.{fn}", s, flags=re.IGNORECASE)
        s = re.sub(r"\bln\b", "np.log", s, flags=re.IGNORECASE)
        s = re.sub(r"\bpi\b", "np.pi", s, flags=re.IGNORECASE)
        return s

    def is_valid_numpy_expr(np_expr: str) -> bool:
        try:
            test_env = {
                "np": np,
                "X1": np.array([0.5, 1.0]),
                "X2": np.array([0.5, 1.0]),
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "exp": np.exp,
                "sqrt": np.sqrt,
                "log": np.log,
                "abs": np.abs,
                "pi": np.pi,
            }
            res = eval(np_expr, {"__builtins__": {}}, test_env)
            return res is not None
        except Exception:
            return False

    def parse_and_apply_command(raw_cmd: str, current_state: dict) -> tuple[dict, bool]:
        """
        Парсит ВСЕ данные из команды (формулу f(x1,x2), векторное поле [u,v],
        диапазон от A до B, координаты a1/x1 и a2/x2, точку (a1,a2), уровень c,
        параметры r/N/t, слои и нужный режим анимации ползунков) и вставляет их в стейт.
        """
        s = dict(current_state)
        norm = normalize_spoken_math(raw_cmd)
        low = norm.lower().strip()

        if not low:
            return s, False

        # Сброс к исходной лекции
        if any(w in low for w in ("сброс", "сначала", "лекция 14", "lecture 14", "reset")):
            fresh = dict(PRESET_STATES["preset_lecture14"])
            fresh["status"] = "⚡ Сброшено к Lecture 14"
            return fresh, True

        # Если вся строка сама по себе является чистой формулой (например: "x1^3 - x2^2")
        direct_np = math_to_numpy(norm)
        is_pure_formula = (
            is_valid_numpy_expr(direct_np)
            and any(v in direct_np for v in ("X1", "X2"))
            and not any(
                kw in low
                for kw in (
                    "покаж",
                    "сделай",
                    "построй",
                    "нарисуй",
                    "срез",
                    "сечен",
                    "касательн",
                    "градиент",
                    "риман",
                    "интеграл",
                    "шар",
                    "окрестност",
                    "векторн",
                    "поток",
                    "анимир",
                    "двиг",
                    "при ",
                    "от ",
                    "точк",
                    "уровень",
                    "create",
                    "show",
                    "plot",
                    "draw",
                    "slice",
                    "tangent",
                    "animate",
                )
            )
        )
        if is_pure_formula:
            disp = clean_display_formula(norm)
            s["formula"] = disp
            s["eval_z"] = direct_np
            s["title"] = f"Поверхность y = {disp}"
            # Сохраняем текущий режим анимации пользователя, не форсируем срез c
            s["status"] = f"✅ Вставлена формула y = {disp}"
            return s, True

        handled = False
        parsed_parts = []
        turn_off = any(w in low for w in ("скрой", "убери", "выключи", "hide", "disable", "remove"))

        # Проверка остановки анимации
        if any(w in low for w in ("стоп", "останови", "пауза", "зафиксируй", "не двигай", "stop", "pause", "freeze")):
            s["anim_mode"] = "none"
            s["status"] = "⏸️ Анимация ползунков остановлена"
            handled = True

        # Явный запрос анимации
        wants_anim = any(
            w in low
            for w in (
                "анимир",
                "анимац",
                "двиг",
                "передвиг",
                "покажи как меняется",
                "в движении",
                "в динамике",
                "прокрут",
                "крути",
                "качай",
                "плавно",
                "сам ползун",
                "animate",
                "animation",
                "move slider",
                "sweep",
            )
        )

        # 1. Именованные поверхности
        named_surfaces = [
            (
                ("mess", "chaotic", "crazy", "хаос", "безумн", "сложн", "шум"),
                "0.7*sin(3*x1)*cos(3*x2) + 0.5*cos(4*x1*x2)",
                "0.7 * np.sin(3*X1) * np.cos(3*X2) + 0.5 * np.cos(4*X1*X2)",
            ),
            (("обезьянье седло", "monkey saddle"), "x1^3 - 3*x1*x2^2", "X1**3 - 3*X1*X2**2"),
            (("седло", "седлов", "гипербол", "saddle"), "x1^2 - x2^2", "X1**2 - X2**2"),
            (("перевернут", "купол", "шапк", "inverted", "dome"), "4 - x1^2 - x2^2", "4 - X1**2 - X2**2"),
            (("парабол", "чаш", "parabol", "bowl"), "x1^2 + x2^2 - 1", "X1**2 + X2**2 - 1"),
            (
                ("сфер", "полусфер", "sphere", "hemisphere"),
                "sqrt(2.5 - x1^2 - x2^2)",
                "np.sqrt(np.maximum(0.0, 2.5 - X1**2 - X2**2))",
            ),
            (("гаусс", "колокол", "холм", "gaussian", "bell"), "2.2 * exp(-(x1^2 + x2^2))", "2.2 * np.exp(-(X1**2 + X2**2))"),
            (
                ("вулкан", "кратер", "volcano", "crater"),
                "2.5 * (x1^2 + x2^2) * exp(-(x1^2 + x2^2))",
                "2.5 * (X1**2 + X2**2) * np.exp(-(X1**2 + X2**2))",
            ),
            (("волн", "синусоид", "waves", "wave"), "sin(x1) * cos(x2)", "np.sin(X1) * np.cos(X2)"),
            (
                ("сомбреро", "капл", "рябь", "ripple", "sombrero"),
                "sin(2.5 * sqrt(x1^2 + x2^2))",
                "np.sin(2.5*np.sqrt(X1**2 + X2**2 + 1e-5))",
            ),
            (("конус", "воронк", "cone", "funnel"), "sqrt(x1^2 + x2^2)", "np.sqrt(X1**2 + X2**2)"),
            (("цилиндр", "желоб", "cylinder"), "x1^2", "X1**2"),
            (("пирамид", "крыш", "pyramid", "roof"), "2 - abs(x1) - abs(x2)", "2.0 - np.abs(X1) - np.abs(X2)"),
        ]
        for keywords, disp_f, np_f in named_surfaces:
            if any(k in low for k in keywords):
                s["formula"] = disp_f
                s["eval_z"] = np_f
                s["title"] = f"Поверхность y = {disp_f}"
                parsed_parts.append(f"f = {disp_f}")
                handled = True
                break

        # 2. Векторное поле [u, v]
        vf_bracket = re.search(r"\[\s*([^,\]]+)\s*,\s*([^\]]+)\s*\]", low)
        if vf_bracket:
            u_str = clean_display_formula(vf_bracket.group(1))
            v_str = clean_display_formula(vf_bracket.group(2))
            s["vector_u"] = u_str
            s["vector_v"] = v_str
            s["show_vector_field"] = True
            parsed_parts.append(f"F = [{u_str}, {v_str}]")
            handled = True
        elif any(w in low for w in ("вихр", "вращен", "swirl", "vortex")):
            s["vector_u"] = "-x2"
            s["vector_v"] = "x1"
            s["show_vector_field"] = True
            parsed_parts.append("F = [-x2, x1]")
            handled = True
        elif any(w in low for w in ("источник", "дивергенц", "source")):
            s["vector_u"] = "x1"
            s["vector_v"] = "x2"
            s["show_vector_field"] = True
            parsed_parts.append("F = [x1, x2]")
            handled = True
        elif any(w in low for w in ("сток", "sink")):
            s["vector_u"] = "-x1"
            s["vector_v"] = "-x2"
            s["show_vector_field"] = True
            parsed_parts.append("F = [-x1, -x2]")
            handled = True

        # 3. Диапазон области определения: "от 0 до 10", "from -3 to 3"
        rng_m = re.search(r"(?:\bот|\bfrom)\s+(-?\d+(?:\.\d+)?)\s+(?:до|to)\s+(-?\d+(?:\.\d+)?)", low)
        has_custom_range = False
        if rng_m:
            r_min = float(rng_m.group(1))
            r_max = float(rng_m.group(2))
            if r_max < r_min:
                r_min, r_max = r_max, r_min
            if r_max - r_min >= 0.2:
                s["x1_range"] = [r_min, r_max]
                s["x2_range"] = [r_min, r_max]
                # Если область несимметрична (например от 0 до 10), выключаем круглую обрезку диска
                if abs(r_min + r_max) > 0.1:
                    s["circular_domain"] = False
                parsed_parts.append(f"область [{r_min:g}, {r_max:g}]")
                has_custom_range = True
                handled = True

        # 4. Точка (a1, a2) и координаты срезов x1 / x2 / a1 / a2
        has_explicit_coord = False
        pt_m = re.search(
            r"(?:точк[еауи]|point)\s*\(?\s*(-?\d+(?:\.\d+)?)\s*(?:,|и|and|\s)\s*(-?\d+(?:\.\d+)?)\s*\)?",
            low,
        )
        if pt_m:
            s["a1"] = float(pt_m.group(1))
            s["a2"] = float(pt_m.group(2))
            has_explicit_coord = True
            parsed_parts.append(f"a = ({s['a1']:g}, {s['a2']:g})")
            handled = True

        a1_m = re.search(r"(?:\bпри\s+|\bпо\s+|\bat\s+)?\b(?:a1|x1)\s*=\s*(-?\d+(?:\.\d+)?)", low)
        if a1_m:
            s["a1"] = float(a1_m.group(1))
            has_explicit_coord = True
            parsed_parts.append(f"x₁ = {s['a1']:g}")
            handled = True

        a2_m = re.search(r"(?:\bпри\s+|\bпо\s+|\bat\s+)?\b(?:a2|x2)\s*=\s*(-?\d+(?:\.\d+)?)", low)
        if a2_m:
            s["a2"] = float(a2_m.group(1))
            has_explicit_coord = True
            parsed_parts.append(f"x₂ = {s['a2']:g}")
            handled = True

        # Авто-расширение диапазона, если координата a1/a2 выходит за текущие границы
        for coord_val, rng_key in ((s["a1"], "x1_range"), (s["a2"], "x2_range")):
            cur_min, cur_max = float(s[rng_key][0]), float(s[rng_key][1])
            if coord_val < cur_min or coord_val > cur_max:
                pad = max(1.0, abs(coord_val) * 0.35)
                new_min = min(cur_min, coord_val - pad)
                new_max = max(cur_max, coord_val + pad)
                s["x1_range"] = [round(new_min, 2), round(new_max, 2)]
                s["x2_range"] = [round(new_min, 2), round(new_max, 2)]
                s["circular_domain"] = False

        # 5. Уровень c (сечение плоскостью y = c / z = c)
        c_m = re.search(r"\b(?:уровень|высота|сечение\s+при\s+y|при\s+y|при\s+c|level|c)\s*=?\s*(-?\d+(?:\.\d+)?)", low)
        if c_m:
            s["c_val"] = float(c_m.group(1))
            s["show_level_plane"] = True
            has_explicit_coord = True
            parsed_parts.append(f"c = {s['c_val']:g}")
            handled = True

        # 6. Параметр r / N / t (радиус, число разбиений Римана, время потока)
        rnt_m = re.search(
            r"\b(?:разбиений|призм|радиус[ае]?|шар\s+радиуса|время|radius|partitions|time|r|t|n)\s*=?\s*(-?\d+(?:\.\d+)?)",
            low,
        )
        if rnt_m:
            s["extra_val"] = max(0.15, float(rnt_m.group(1)))
            has_explicit_coord = True
            parsed_parts.append(f"r/N/t = {s['extra_val']:g}")
            handled = True

        # 7. Слои и математические темы
        topic_anim_suggestion = None

        if any(w in low for w in ("касательн", "градиент", "нормал", "tangent", "gradient")):
            s["show_tangent"] = not turn_off
            if not turn_off:
                topic_anim_suggestion = "orbit"
            parsed_parts.append("касательная + ∇f")
            handled = True

        if any(w in low for w in ("риман", "riemann", "интеграл", "integral", "призм", "объем", "volume")):
            s["show_riemann"] = not turn_off
            if not turn_off:
                if s["extra_val"] < 2.0:
                    s["extra_val"] = 7.0
                topic_anim_suggestion = "rnt"
            parsed_parts.append("суммы Римана")
            handled = True

        if any(w in low for w in ("векторн", "поток", "линию тока", "линия тока", "vector field", "flow")):
            s["show_vector_field"] = not turn_off
            if not turn_off:
                if s["extra_val"] < 1.0:
                    s["extra_val"] = 5.0
                topic_anim_suggestion = "rnt"
            parsed_parts.append("векторное поле")
            handled = True

        if any(w in low for w in ("шар", "окрестност", "ball", "neighborhood", "границу")):
            s["show_ball"] = not turn_off
            if not turn_off:
                if s["extra_val"] > 2.5:
                    s["extra_val"] = 0.85
                topic_anim_suggestion = "rnt"
            parsed_parts.append("окрестность B_r(a)")
            handled = True

        if any(
            w in low
            for w in (
                "вертикальн",
                "след",
                "срезы",
                "срез ",
                "по x1",
                "по x2",
                "при x1",
                "при x2",
                "slice",
                "trace",
            )
        ):
            s["show_xy_traces"] = not turn_off
            if not turn_off:
                if "x1" in low and "x2" not in low:
                    topic_anim_suggestion = "a1"
                else:
                    topic_anim_suggestion = "a2"
            parsed_parts.append("вертикальные срезы")
            handled = True
        elif any(w in low for w in ("сечен", "линию уровня", "линия уровня", "уровн", "level")):
            s["show_level_plane"] = not turn_off
            if not turn_off:
                topic_anim_suggestion = "c"
            parsed_parts.append("сечение y = c")
            handled = True

        if any(w in low for w in ("2d", "2д", "двумерн", "карта", "контур", "contour")):
            s["split_2d"] = not turn_off
            handled = True
        elif "только 3" in low or "only 3d" in low:
            s["split_2d"] = False
            handled = True

        if any(w in low for w in ("сетк", "куб", "оси", "grid", "box")):
            s["show_box_grid"] = not turn_off
            handled = True

        if any(w in low for w in ("включи камеру", "вруби камеру", "крути через камеру", "крути камерой", "управление камерой", "жестами", "webcam", "camera on", "start camera")):
            s["cam_active"] = True
            parsed_parts.append("📷 управление камерой ВКЛ")
            handled = True
        elif any(w in low for w in ("выключи камеру", "отключи камеру", "закрой камеру", "camera off", "stop camera")):
            s["cam_active"] = False
            parsed_parts.append("📷 управление камерой ВЫКЛ")
            handled = True

        if any(w in low for w in ("квадратн", "прямоугольн", "square")):
            s["circular_domain"] = False
            handled = True
        elif any(w in low for w in ("кругл", "диск", "disk")):
            s["circular_domain"] = True
            handled = True

        # 8. Относительные сдвиги ползунков голосом
        if any(w in low for w in ("вправо", "правее", "right")):
            s["a1"] = round(float(s["a1"]) + 0.3, 2)
            handled = True
        elif any(w in low for w in ("влево", "левее", "left")):
            s["a1"] = round(float(s["a1"]) - 0.3, 2)
            handled = True

        if any(w in low for w in ("вперед", "дальше", "forward")):
            s["a2"] = round(float(s["a2"]) + 0.3, 2)
            handled = True
        elif any(w in low for w in ("назад", "ближе", "back")):
            s["a2"] = round(float(s["a2"]) - 0.3, 2)
            handled = True

        if any(w in low for w in ("выше", "подними", "up", "higher")):
            s["c_val"] = round(float(s["c_val"]) + 0.3, 2)
            handled = True
        elif any(w in low for w in ("ниже", "опусти", "down", "lower")):
            s["c_val"] = round(float(s["c_val"]) - 0.3, 2)
            handled = True

        if any(w in low for w in ("приблизь", "зум плюс", "крупнее", "zoom in")):
            r1, r2 = s["x1_range"], s["x2_range"]
            s["x1_range"] = [round(r1[0] * 0.78, 2), round(r1[1] * 0.78, 2)]
            s["x2_range"] = [round(r2[0] * 0.78, 2), round(r2[1] * 0.78, 2)]
            handled = True
        elif any(w in low for w in ("отдали", "зум минус", "шире", "zoom out")):
            r1, r2 = s["x1_range"], s["x2_range"]
            s["x1_range"] = [round(r1[0] * 1.3, 2), round(r1[1] * 1.3, 2)]
            s["x2_range"] = [round(r2[0] * 1.3, 2), round(r2[1] * 1.3, 2)]
            handled = True

        # 9. Извлечение математической формулы f(x1, x2) из любой части фразы
        formula_src = low
        if vf_bracket:
            formula_src = formula_src.replace(vf_bracket.group(0), " ")
        formula_src = re.sub(r"\b[23][dд]\b", " ", formula_src)
        formula_src = re.sub(r"(?:\bот|\bfrom)\s+-?\d+(?:\.\d+)?\s+(?:до|to)\s+-?\d+(?:\.\d+)?", " ", formula_src)
        formula_src = re.sub(
            r"(?:точк[еауи]|point)\s*\(?\s*-?\d+(?:\.\d+)?\s*(?:,|и|and|\s)\s*-?\d+(?:\.\d+)?\s*\)?",
            " ",
            formula_src,
        )
        formula_src = re.sub(
            r"\b(?:при\s+|по\s+|at\s+)?(?:a1|a2|x1|x2|уровень|высота|level|разбиений|призм|радиус[ае]?|время|radius|time|c|r|t|n)\s*=\s*-?\d+(?:\.\d+)?",
            " ",
            formula_src,
        )
        formula_src = re.sub(r"\b[fzy]\s*(\([^)]*\))?\s*=\s*", " ", formula_src)

        math_token_pat = r"(?:(?:sin|cos|tan|exp|sqrt|log|abs|pi|x1|x2)|(?<![a-zA-Z0-9_])[xy](?![a-zA-Z0-9_])|\d+(?:\.\d+)?|[\+\-\*\/\^\(\)])"
        contiguous_spans = [
            m.group(0).strip()
            for m in re.finditer(rf"{math_token_pat}(?:\s*{math_token_pat})*", formula_src)
        ]
        valid_spans = [
            sp for sp in contiguous_spans if any(v in sp for v in ("x1", "x2", "x", "y"))
        ]
        valid_spans.sort(key=len, reverse=True)
        for raw_sp in valid_spans:
            candidate = re.sub(r"\s*\^\s*", "^", raw_sp).strip()
            # Убираем висящие операторы по краям
            candidate = re.sub(r"^[\+\*\/\^]+|[\+\-\*\/\^]+$", "", candidate).strip()
            if not candidate or not any(v in candidate for v in ("x1", "x2", "x", "y")):
                continue
            np_cand = math_to_numpy(candidate)
            if is_valid_numpy_expr(np_cand):
                disp = clean_display_formula(candidate)
                s["formula"] = disp
                s["eval_z"] = np_cand
                s["title"] = f"Поверхность y = {disp}"
                parsed_parts.append(f"f = {disp}")
                handled = True
                break

        # 10. Определение нужного режима авто-передвижения ползунков (анимации)
        wants_stop = any(
            w in low for w in ("стоп", "останови", "пауза", "зафиксируй", "не двигай", "статич", "stop", "pause", "freeze")
        )
        if wants_stop:
            s["anim_mode"] = "none"
        elif wants_anim:
            # Анимация включается ТОЛЬКО когда пользователь явно просит движение ("анимируй", "двигай", "в динамике")
            if any(w in low for w in ("x1", "a1")) and not any(w in low for w in ("x2", "a2")) and s.get("show_xy_traces"):
                s["anim_mode"] = "a1"
            elif any(w in low for w in ("срез", "slice")) or s.get("show_xy_traces"):
                s["anim_mode"] = "a2"
            elif any(w in low for w in ("касательн", "градиент", "tangent", "orbit")) or s.get("show_tangent"):
                s["anim_mode"] = "orbit"
            elif any(w in low for w in ("риман", "поток", "шар", "riemann", "flow", "ball")) or s.get("show_riemann") or s.get("show_vector_field") or s.get("show_ball"):
                s["anim_mode"] = "rnt"
            else:
                s["anim_mode"] = "c"
            parsed_parts.append(f"🎬 запущена анимация ({s['anim_mode']})")
        elif topic_anim_suggestion and s.get("anim_mode", "none") != "none":
            # Если анимация уже была активна, переключаем фокус на новый объект
            s["anim_mode"] = topic_anim_suggestion

        if handled:
            summary = ", ".join(parsed_parts) if parsed_parts else raw_cmd
            s["status"] = f"✅ Вставлено и запущено: {summary}"

        return s, handled

    # =========================================================================
    # 4. GEMINI 2.5 FLASH AI AGENT (СТРУКТУРИРОВАННЫЙ ПАРСИНГ СЛОЖНЫХ ЗАПРОСОВ)
    # =========================================================================
    def ask_gemini_ai(query: str, api_key: str, current_state: dict) -> tuple[dict, bool, str]:
        if not api_key:
            return current_state, False, "⚠️ Введите GEMINI_API_KEY в правом верхнем углу"
        try:
            client = genai.Client(api_key=api_key, http_options={"timeout": 5000})
            schema = {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "formula": {
                        "type": "string",
                        "description": "Clean math expression using x1 and x2, e.g. 'x1^2 - x2^2' or 'sin(x1)*cos(x2)'",
                    },
                    "vector_u": {"type": "string"},
                    "vector_v": {"type": "string"},
                    "x1_min": {"type": "number"},
                    "x1_max": {"type": "number"},
                    "a1": {"type": "number"},
                    "a2": {"type": "number"},
                    "c_val": {"type": "number"},
                    "extra_val": {"type": "number"},
                    "show_level_plane": {"type": "boolean"},
                    "show_xy_traces": {"type": "boolean"},
                    "show_tangent": {"type": "boolean"},
                    "show_ball": {"type": "boolean"},
                    "show_riemann": {"type": "boolean"},
                    "show_vector_field": {"type": "boolean"},
                    "circular_domain": {"type": "boolean"},
                    "split_2d": {"type": "boolean"},
                    "anim_mode": {
                        "type": "string",
                        "enum": ["none", "c", "a1", "a2", "orbit", "rnt"],
                    },
                },
                "required": [
                    "title",
                    "formula",
                    "x1_min",
                    "x1_max",
                    "a1",
                    "a2",
                    "c_val",
                    "extra_val",
                    "show_level_plane",
                    "show_xy_traces",
                    "show_tangent",
                    "show_ball",
                    "show_riemann",
                    "show_vector_field",
                    "circular_domain",
                    "split_2d",
                    "anim_mode",
                ],
            }
            sys_prompt = (
                "You are an interactive Multivariable Calculus studio controller (Desmos 3D + BS101 Lecture 14).\n"
                "Parse ALL mathematical data from the user's request (in Russian or English):\n"
                "- formula: function f(x1, x2) using x1, x2, sin, cos, tan, exp, sqrt, log, abs.\n"
                "- x1_min, x1_max: domain bounds (default -1.8 to 1.8 unless specified like 'от 0 до 10').\n"
                "- a1, a2: point coordinates or slice positions.\n"
                "- c_val: level height y=c.\n"
                "- extra_val: radius r (0.2..2.0), Riemann partitions N (2..16), or flow time t (1..10).\n"
                "- anim_mode: choose 'a2' or 'a1' to animate slices, 'c' to animate level curve, 'orbit' to animate tangent/point, 'rnt' to animate Riemann/ball/flow, or 'none' if static."
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
            raw_text = response.text or "{}"
            data = json.loads(raw_text)
            new_st = dict(current_state)
            disp_f = clean_display_formula(data.get("formula", new_st["formula"]))
            np_f = math_to_numpy(disp_f)
            if is_valid_numpy_expr(np_f):
                new_st["formula"] = disp_f
                new_st["eval_z"] = np_f
            new_st["title"] = data.get("title", f"Поверхность y = {new_st['formula']}")
            if data.get("vector_u"):
                new_st["vector_u"] = clean_display_formula(data["vector_u"])
            if data.get("vector_v"):
                new_st["vector_v"] = clean_display_formula(data["vector_v"])
            xmin = float(data.get("x1_min", new_st["x1_range"][0]))
            xmax = float(data.get("x1_max", new_st["x1_range"][1]))
            if xmax - xmin >= 0.2:
                new_st["x1_range"] = [xmin, xmax]
                new_st["x2_range"] = [xmin, xmax]
            for k in (
                "a1",
                "a2",
                "c_val",
                "extra_val",
                "show_level_plane",
                "show_xy_traces",
                "show_tangent",
                "show_ball",
                "show_riemann",
                "show_vector_field",
                "circular_domain",
                "split_2d",
                "anim_mode",
            ):
                if k in data:
                    new_st[k] = data[k]
            new_st["status"] = f"✨ Gemini 2.5 Flash вставил все данные и настроил сцену"
            return new_st, True, new_st["status"]
        except Exception as e:
            return current_state, False, f"⚠️ Локальный парсер (Gemini API: {str(e)[:65]})"

    # =========================================================================
    # 5. ПОЛНОФУНКЦИОНАЛЬНЫЙ ИНТЕРАКТИВНЫЙ ВИДЖЕТ С АВТО-ПОЛЗУНКАМИ И 60 FPS WEBGL
    # =========================================================================
    class DesmosMultivarStudio(anywidget.AnyWidget):
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

        // Быстрый безопасный компилятор математических выражений f(x1, x2) в JS для 60 FPS анимации ползунков
        function compileMathFn(formulaStr) {
          let s = String(formulaStr || "x1^2 - x2^2").trim();
          const mapUni = {
            "⁰":"^0","¹":"^1","²":"^2","³":"^3","⁴":"^4","⁵":"^5","⁶":"^6","⁷":"^7","⁸":"^8","⁹":"^9",
            "₁":"1","₂":"2","₃":"3","−":"-","–":"-","—":"-","×":"*","·":"*","÷":"/","π":"pi"
          };
          for (const [k, v] of Object.entries(mapUni)) s = s.split(k).join(v);
          s = s.replace(/^[fzy]\s*(\([^)]*\))?\s*=\s*/i, "");
          s = s.replace(/np\./g, "").replace(/Math\./g, "");
          s = s.replace(/\^/g, "**");
          s = s.replace(/(\d)\s*([a-zA-Z\(])/g, "$1*$2");
          s = s.replace(/(\))\s*([a-zA-Z\d\(])/g, "$1*$2");
          s = s.replace(/(x_?[12])\s+(x_?[12])/gi, "$1*$2");
          s = s.replace(/(?<![a-zA-Z])x_?1(?![0-9])/gi, "x1");
          s = s.replace(/(?<![a-zA-Z])x_?2(?![0-9])/gi, "x2");
          s = s.replace(/\bx\b/g, "x1").replace(/\by\b/g, "x2");
          s = s.replace(/\bln\b/gi, "log");
          try {
            const fn = new Function(
              "x1", "x2",
              "const {sin,cos,tan,exp,sqrt,log,abs,atan2,asin,acos,pow,min,max,PI} = Math; const pi = PI; return (" + s + ");"
            );
            const test = fn(0.5, 0.5);
            if (typeof test === "number" && !isNaN(test)) return fn;
          } catch (e) {}
          return (x1, x2) => x1*x1 - x2*x2;
        }

        export default {
          render({ model, el }) {
            let state = {};
            try {
              state = JSON.parse(model.get("state_json") || "{}");
            } catch (e) {}

            let animRaf = null;
            let tweenRaf = null;
            let lastFrameTs = 0;
            let animPhase = 0;
            let userDraggingSlider = false;
            let isApplyingModelUpdate = false;

            el.innerHTML = `
              <style>
                .dm-studio {
                  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                  color: #0f172a;
                  background: #ffffff;
                  border: 1px solid #e2e8f0;
                  border-radius: 14px;
                  padding: 12px 16px;
                  box-shadow: 0 4px 20px rgba(15, 23, 42, 0.04);
                }
                .dm-topbar {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  gap: 12px;
                  flex-wrap: wrap;
                  padding-bottom: 8px;
                  border-bottom: 1px solid #f1f5f9;
                }
                .dm-brand {
                  font-size: 16px;
                  font-weight: 700;
                  color: #0f172a;
                  display: flex;
                  align-items: center;
                  gap: 8px;
                }
                .dm-brand span {
                  font-weight: 500;
                  color: #475569;
                  font-size: 14px;
                }
                .dm-voice-bar {
                  display: flex;
                  align-items: center;
                  gap: 10px;
                  background: linear-gradient(90deg, #f8fafc 0%, #f0f7ff 100%);
                  border: 1px solid #cbd5e1;
                  border-radius: 10px;
                  padding: 6px 12px;
                  margin-top: 8px;
                  flex-wrap: wrap;
                }
                .dm-mic-btn {
                  display: inline-flex;
                  align-items: center;
                  gap: 7px;
                  padding: 7px 14px;
                  border-radius: 999px;
                  font-weight: 700;
                  font-size: 12.5px;
                  cursor: pointer;
                  border: none;
                  transition: all 0.18s ease;
                  color: #fff;
                  background: #2563eb;
                }
                .dm-mic-btn.active {
                  background: #dc2626;
                  box-shadow: 0 0 0 4px rgba(220, 38, 38, 0.2);
                  animation: dmPulse 1.5s infinite;
                }
                .dm-cam-btn {
                  display: inline-flex;
                  align-items: center;
                  gap: 7px;
                  padding: 7px 14px;
                  border-radius: 999px;
                  font-weight: 700;
                  font-size: 12.5px;
                  cursor: pointer;
                  border: none;
                  transition: all 0.18s ease;
                  color: #ffffff;
                  background: #0d9488;
                }
                .dm-cam-btn:hover {
                  background: #0f766e;
                }
                .dm-cam-btn.active {
                  background: #e11d48;
                  box-shadow: 0 0 0 4px rgba(225, 29, 72, 0.25);
                  animation: dmPulse 1.5s infinite;
                }
                @keyframes dmPulse {
                  0% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.4); }
                  70% { box-shadow: 0 0 0 7px rgba(220, 38, 38, 0); }
                  100% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
                }
                .dm-select, .dm-input, .dm-num-input {
                  padding: 6px 10px;
                  border-radius: 8px;
                  border: 1px solid #cbd5e1;
                  background: #fff;
                  font-size: 13px;
                  color: #0f172a;
                  outline: none;
                  transition: border-color 0.15s, box-shadow 0.15s;
                }
                .dm-select:focus, .dm-input:focus, .dm-num-input:focus {
                  border-color: #2563eb;
                  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
                }
                .dm-input-highlight {
                  border-color: #16a34a !important;
                  background: #f0fdf4 !important;
                }
                .dm-controls-row {
                  display: grid;
                  grid-template-columns: 220px 1fr 230px auto;
                  gap: 8px;
                  align-items: end;
                  margin-top: 8px;
                }
                @media (max-width: 1024px) {
                  .dm-controls-row {
                    grid-template-columns: 1fr 1fr;
                  }
                }
                .dm-field-label {
                  font-size: 11px;
                  font-weight: 600;
                  color: #475569;
                  margin-bottom: 3px;
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                }
                .dm-btn {
                  padding: 7px 12px;
                  border-radius: 8px;
                  border: 1px solid #cbd5e1;
                  background: #f8fafc;
                  color: #0f172a;
                  font-weight: 600;
                  font-size: 12.5px;
                  cursor: pointer;
                  transition: all 0.15s;
                  white-space: nowrap;
                }
                .dm-btn:hover {
                  background: #e2e8f0;
                }
                .dm-btn-primary {
                  background: #2563eb;
                  color: #ffffff;
                  border-color: #1d4ed8;
                }
                .dm-btn-primary:hover {
                  background: #1d4ed8;
                }
                .dm-btn-ai {
                  background: #7c3aed;
                  color: #ffffff;
                  border-color: #6d28d9;
                }
                .dm-btn-ai:hover {
                  background: #6d28d9;
                }
                .dm-sliders-grid {
                  display: grid;
                  grid-template-columns: repeat(4, 1fr);
                  gap: 10px;
                  margin-top: 10px;
                  background: #f8fafc;
                  padding: 9px 12px;
                  border-radius: 10px;
                  border: 1px solid #e2e8f0;
                }
                @media (max-width: 960px) {
                  .dm-sliders-grid {
                    grid-template-columns: repeat(2, 1fr);
                  }
                }
                .dm-slider-card {
                  display: flex;
                  flex-direction: column;
                  gap: 4px;
                }
                .dm-slider-head {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  font-size: 12px;
                  font-weight: 600;
                  color: #1e293b;
                }
                .dm-slider-val {
                  font-family: 'JetBrains Mono', monospace;
                  font-size: 12px;
                  font-weight: 700;
                  color: #2563eb;
                  background: #eff6ff;
                  padding: 1px 6px;
                  border-radius: 5px;
                  border: 1px solid #bfdbfe;
                }
                .dm-slider-row {
                  display: flex;
                  align-items: center;
                  gap: 6px;
                }
                .dm-slider-row input[type="range"] {
                  flex: 1;
                  accent-color: #2563eb;
                  cursor: pointer;
                  height: 6px;
                }
                .dm-play-mini {
                  border: 1px solid #cbd5e1;
                  background: #ffffff;
                  color: #334155;
                  border-radius: 6px;
                  width: 26px;
                  height: 24px;
                  font-size: 11px;
                  cursor: pointer;
                  display: inline-flex;
                  align-items: center;
                  justify-content: center;
                  padding: 0;
                  transition: all 0.15s;
                }
                .dm-play-mini.playing {
                  background: #16a34a;
                  color: #ffffff;
                  border-color: #15803d;
                }
                .dm-layers-bar {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  flex-wrap: wrap;
                  gap: 6px;
                  margin-top: 8px;
                }
                .dm-chips {
                  display: flex;
                  align-items: center;
                  flex-wrap: wrap;
                  gap: 6px;
                }
                .dm-chip {
                  display: inline-flex;
                  align-items: center;
                  gap: 5px;
                  padding: 4px 10px;
                  border-radius: 999px;
                  font-size: 12px;
                  font-weight: 600;
                  border: 1px solid #cbd5e1;
                  background: #f8fafc;
                  color: #334155;
                  cursor: pointer;
                  user-select: none;
                  transition: all 0.14s;
                }
                .dm-chip.active {
                  background: #eff6ff;
                  border-color: #2563eb;
                  color: #1d4ed8;
                }
                .dm-anim-bar {
                  display: flex;
                  align-items: center;
                  gap: 5px;
                  flex-wrap: wrap;
                }
                .dm-anim-pill {
                  padding: 4px 9px;
                  border-radius: 999px;
                  font-size: 11.5px;
                  font-weight: 700;
                  border: 1px solid #cbd5e1;
                  background: #ffffff;
                  color: #334155;
                  cursor: pointer;
                  transition: all 0.15s;
                }
                .dm-anim-pill.active {
                  background: #16a34a;
                  color: #ffffff;
                  border-color: #15803d;
                }
                .dm-status-strip {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  margin-top: 8px;
                  padding: 5px 10px;
                  border-radius: 8px;
                  background: #f8fafc;
                  border: 1px solid #f1f5f9;
                  font-size: 13px;
                  flex-wrap: wrap;
                  gap: 8px;
                }
                .dm-plot-wrap {
                  width: 100%;
                  height: 600px;
                  margin-top: 4px;
                  position: relative;
                }
                .dm-cam-pip {
                  position: absolute;
                  right: 14px;
                  bottom: 14px;
                  width: 242px;
                  background: rgba(15, 23, 42, 0.94);
                  border: 1px solid rgba(255, 255, 255, 0.20);
                  border-radius: 12px;
                  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.50), 0 0 0 1px rgba(0, 0, 0, 0.2);
                  backdrop-filter: blur(12px);
                  z-index: 45;
                  overflow: hidden;
                  user-select: none;
                  transition: box-shadow 0.2s;
                }
                .dm-cam-header {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  padding: 6px 10px;
                  background: rgba(30, 41, 59, 0.92);
                  border-bottom: 1px solid rgba(255, 255, 255, 0.10);
                  cursor: grab;
                }
                .dm-cam-header:active {
                  cursor: grabbing;
                }
                .dm-cam-icon-btn {
                  background: transparent;
                  border: none;
                  color: #94a3b8;
                  font-size: 13px;
                  cursor: pointer;
                  padding: 2px 5px;
                  border-radius: 4px;
                  transition: all 0.15s;
                }
                .dm-cam-icon-btn:hover {
                  background: rgba(255, 255, 255, 0.18);
                  color: #ffffff;
                }
                .dm-cam-footer {
                  padding: 8px 10px;
                  background: rgba(15, 23, 42, 0.96);
                  border-top: 1px solid rgba(255, 255, 255, 0.08);
                }
                .dm-math-footer {
                  margin-top: 6px;
                  padding: 8px 12px;
                  border-radius: 8px;
                  background: #f8fafc;
                  border: 1px solid #e2e8f0;
                  font-size: 12.5px;
                  color: #1e293b;
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  flex-wrap: wrap;
                  gap: 10px;
                }
              </style>

              <div class="dm-studio">
                <!-- ВЕРХНЯЯ ПАНЕЛЬ БРЕНДА И API КЛЮЧА -->
                <div class="dm-topbar">
                  <div class="dm-brand">
                    🧭 Desmos 3D Multivariable <span>Auto-Parsing, Auto-Input & Self-Moving Sliders Studio</span>
                  </div>
                  <div style="display:flex;align-items:center;gap:8px;">
                    <span style="font-size:12px;color:#475569;font-weight:600;">🔑 Gemini API Key:</span>
                    <input id="dm-apikey" type="password" class="dm-input" style="width:190px;padding:4px 8px;" placeholder="AIzaSy..." />
                  </div>
                </div>

                <!-- ПАНЕЛЬ ГОЛОСОВОГО УПРАВЛЕНИЯ И БЫСТРОГО ЗАПРОСА НА ЕСТЕСТВЕННОМ ЯЗЫКЕ -->
                <div class="dm-voice-bar">
                  <button id="dm-mic-btn" class="dm-mic-btn">🎙️ Включить Live-микрофон</button>
                  <button id="dm-cam-btn" class="dm-cam-btn">📷 Управление камерой</button>
                  <select id="dm-lang" class="dm-select" style="padding:4px 8px;font-weight:600;">
                    <option value="ru-RU">🇷🇺 RU</option>
                    <option value="en-US">🇺🇸 EN</option>
                  </select>
                  <input id="dm-nl-input" type="text" class="dm-input" style="flex:1;min-width:260px;"
                    placeholder="Говори в микрофон или напиши: «покажи срез x1^2 - x2^2 от 0 до 10 при x2=5», «анимируй касательную плоскость к sin(x1)*cos(x2)»..." />
                  <button id="dm-nl-run" class="dm-btn dm-btn-primary">⚡ Выполнить и вставить</button>
                  <button id="dm-nl-ai" class="dm-btn dm-btn-ai">🤖 Gemini AI</button>
                  <span id="dm-voice-live" style="font-size:12px;color:#475569;font-style:italic;"></span>
                </div>

                <!-- СТРОКА АВТО-ВСТАВЛЯЕМЫХ ПОЛЕЙ: ПРЕСЕТ, ФОРМУЛА f(x1,x2), ДИАПАЗОН [min, max], ПОЛЕ [u, v] -->
                <div class="dm-controls-row">
                  <div>
                    <div class="dm-field-label"><span>📚 Пресеты тем:</span></div>
                    <select id="dm-preset" class="dm-select" style="width:100%;">
                      <option value="preset_lecture14">1. Lecture 14: Сечение y = f(x) = c</option>
                      <option value="preset_trace">2. Срезы x₁ = a₁ и x₂ = a₂ (Traces)</option>
                      <option value="preset_tangent">3. Касательная плоскость и градиент ∇f</option>
                      <option value="preset_flow">4. Векторное поле F и линия тока r(t)</option>
                      <option value="preset_riemann">5. 3D суммы Римана (Двойной интеграл)</option>
                      <option value="preset_ball">6. Окрестность B_r(a) и граница ∂B_r</option>
                    </select>
                  </div>

                  <div>
                    <div class="dm-field-label">
                      <span>📐 Вставленная формула поверхности <b>y = f(x₁, x₂)</b>:</span>
                      <span style="color:#64748b;font-weight:400;">авто-заполняется из речи/текста</span>
                    </div>
                    <input id="dm-formula" type="text" class="dm-input" style="width:100%;font-family:'JetBrains Mono',monospace;font-weight:600;"
                      value="x1^2 - x2^2" placeholder="Напр. x1^3 - x2^2, sin(x1)*cos(x2), 4 - x1^2 - x2^2" />
                  </div>

                  <div>
                    <div class="dm-field-label"><span>📏 Диапазон <b>x₁, x₂ ∈ [min, max]</b>:</span></div>
                    <div style="display:flex;align-items:center;gap:6px;">
                      <input id="dm-xmin" type="number" step="0.2" class="dm-num-input" style="width:100%;font-family:monospace;" value="-1.8" />
                      <span style="color:#64748b;font-weight:700;">..</span>
                      <input id="dm-xmax" type="number" step="0.2" class="dm-num-input" style="width:100%;font-family:monospace;" value="1.8" />
                    </div>
                  </div>

                  <div id="dm-vf-inputs" style="display:none;">
                    <div class="dm-field-label"><span>🧭 Поле <b>F = [u, v]</b>:</span></div>
                    <div style="display:flex;align-items:center;gap:4px;">
                      <input id="dm-vfu" type="text" class="dm-input" style="width:78px;font-family:monospace;" value="-x2" />
                      <input id="dm-vfv" type="text" class="dm-input" style="width:78px;font-family:monospace;" value="x1" />
                    </div>
                  </div>
                </div>

                <!-- 4 САМОДВИЖУЩИХСЯ ПОЛЗУНКА С КНОПКАМИ ПЛАВНОЙ АНИМАЦИИ -->
                <div class="dm-sliders-grid">
                  <div class="dm-slider-card">
                    <div class="dm-slider-head">
                      <span>📍 Координата <b>a₁ (x¹)</b>:</span>
                      <span id="dm-val-a1" class="dm-slider-val">0.55</span>
                    </div>
                    <div class="dm-slider-row">
                      <button id="dm-play-a1" class="dm-play-mini" title="Анимировать ползунок a₁">▶</button>
                      <input id="dm-sl-a1" type="range" min="-1.8" max="1.8" step="0.02" value="0.55" />
                    </div>
                  </div>

                  <div class="dm-slider-card">
                    <div class="dm-slider-head">
                      <span>📍 Координата <b>a₂ (x²)</b>:</span>
                      <span id="dm-val-a2" class="dm-slider-val">0.85</span>
                    </div>
                    <div class="dm-slider-row">
                      <button id="dm-play-a2" class="dm-play-mini" title="Анимировать ползунок a₂ (срез x₂)">▶</button>
                      <input id="dm-sl-a2" type="range" min="-1.8" max="1.8" step="0.02" value="0.85" />
                    </div>
                  </div>

                  <div class="dm-slider-card">
                    <div class="dm-slider-head">
                      <span>📐 Уровень сечения <b>c (y = c)</b>:</span>
                      <span id="dm-val-c" class="dm-slider-val">-0.50</span>
                    </div>
                    <div class="dm-slider-row">
                      <button id="dm-play-c" class="dm-play-mini" title="Анимировать плоскость y = c">▶</button>
                      <input id="dm-sl-c" type="range" min="-3.5" max="3.5" step="0.03" value="-0.50" />
                    </div>
                  </div>

                  <div class="dm-slider-card">
                    <div class="dm-slider-head">
                      <span id="dm-lbl-extra">⭕ Параметр <b>r / N / t</b>:</span>
                      <span id="dm-val-extra" class="dm-slider-val">0.90</span>
                    </div>
                    <div class="dm-slider-row">
                      <button id="dm-play-extra" class="dm-play-mini" title="Анимировать параметр r / N / t">▶</button>
                      <input id="dm-sl-extra" type="range" min="0.15" max="16.0" step="0.05" value="0.90" />
                    </div>
                  </div>
                </div>

                <!-- ПЕРЕКЛЮЧАТЕЛИ СЛОЕВ И РЕЖИМОВ АВТО-АНИМАЦИИ ПОЛЗУНКОВ -->
                <div class="dm-layers-bar">
                  <div class="dm-chips">
                    <div id="chip-level" class="dm-chip active">☑️ Сечение y = c</div>
                    <div id="chip-traces" class="dm-chip">📐 Срезы x₁ = a₁, x₂ = a₂</div>
                    <div id="chip-tangent" class="dm-chip">🟢 Касательная и ∇f(a)</div>
                    <div id="chip-ball" class="dm-chip">⭕ Окрестность B_r(a)</div>
                    <div id="chip-riemann" class="dm-chip">📊 3D суммы Римана</div>
                    <div id="chip-vf" class="dm-chip">🌊 Векторное поле и поток</div>
                    <div id="chip-disk" class="dm-chip active">💿 Круглая кромка</div>
                    <div id="chip-2d" class="dm-chip">🗺️ 2D карта рядом</div>
                    <div id="chip-grid" class="dm-chip">🧊 Сетка куба</div>
                  </div>

                  <div class="dm-anim-bar">
                    <span style="font-size:11.5px;font-weight:700;color:#475569;">🎬 Авто-ползунки:</span>
                    <button id="anim-orbit" class="dm-anim-pill" title="Двигать точку (a₁, a₂) по кругу">🔄 Орбита (a₁, a₂)</button>
                    <button id="anim-a2" class="dm-anim-pill" title="Двигать срез x₂">📐 Срез x₂</button>
                    <button id="anim-c" class="dm-anim-pill" title="Двигать уровень y = c">↕️ Уровень c</button>
                    <button id="anim-rnt" class="dm-anim-pill" title="Двигать r / N / t">🌊 r / N / t</button>
                    <button id="anim-stop" class="dm-anim-pill" style="color:#dc2626;">⏹ Стоп</button>
                  </div>
                </div>

                <!-- СТРОКА ЗАГОЛОВКА И СТАТУСА ПАРСЕРА -->
                <div class="dm-status-strip">
                  <div id="dm-title" style="font-weight:700;color:#0f172a;">Lecture 14: Сечение поверхности y = x₁² - x₂² плоскостью y = c</div>
                  <div id="dm-status" style="font-size:12px;color:#15803d;font-weight:600;">⚡ Готово</div>
                </div>

                <!-- 3D / 2D ХОЛСТ PLOTLY WEBGL И ПЛАВАЮЩИЙ HUD КАМЕРЫ -->
                <div id="dm-plot-wrap" class="dm-plot-wrap">
                  <div id="dm-plot" style="width:100%;height:100%;"></div>

                  <!-- ПЛАВАЮЩИЙ HUD ВЕБ-КАМЕРЫ PRO: ВРАЩЕНИЕ, AIR-УКАЗКА, СРЕЗЫ, ЗУМ, СНИМКИ -->
                  <div id="dm-cam-pip" class="dm-cam-pip" style="display:none;">
                    <div id="dm-cam-header" class="dm-cam-header">
                      <div style="display:flex;align-items:center;gap:6px;">
                        <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;"></span>
                        <span style="font-weight:700;font-size:12px;color:#f8fafc;">📷 Motion 3D Cam Pro</span>
                      </div>
                      <div style="display:flex;align-items:center;gap:3px;">
                        <button id="dm-cam-reset-btn" class="dm-cam-icon-btn" title="Сбросить ракурс 3D (Home View)">🎯</button>
                        <button id="dm-cam-freeze-btn" class="dm-cam-icon-btn" title="Заморозить вращение (Стоп)">✋</button>
                        <button id="dm-cam-snap-btn" class="dm-cam-icon-btn" title="Сделать снимок графика (PNG)">📸</button>
                        <button id="dm-cam-min-btn" class="dm-cam-icon-btn" title="Свернуть / Развернуть">−</button>
                        <button id="dm-cam-close-btn" class="dm-cam-icon-btn" title="Выключить камеру">✕</button>
                      </div>
                    </div>
                    <div id="dm-cam-content">
                      <div style="position:relative;width:250px;height:165px;background:#090d16;overflow:hidden;">
                        <video id="dm-cam-video" playsinline muted autoplay style="display:none;"></video>
                        <canvas id="dm-cam-canvas" width="250" height="165" style="display:block;width:100%;height:100%;"></canvas>
                        <!-- Шкала энергии движения (Motion Energy Meter) -->
                        <div style="position:absolute;bottom:0;left:0;right:0;height:3px;background:rgba(255,255,255,0.12);">
                          <div id="dm-cam-meter-bar" style="height:100%;width:0%;background:linear-gradient(90deg, #10b981, #00f5d4, #f43f5e);transition:width 0.08s;"></div>
                        </div>
                      </div>
                      <div class="dm-cam-footer">
                        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:6px;">
                          <div>
                            <span style="font-size:10px;font-weight:600;color:#94a3b8;display:block;margin-bottom:2px;">Цель жестов:</span>
                            <select id="dm-cam-target" class="dm-select" style="width:100%;font-size:11px;padding:2px 4px;background:#1e293b;color:#f8fafc;border-color:#334155;">
                              <option value="orbit" selected>🔄 Вращение 3D</option>
                              <option value="point">📍 Точка a(a₁,a₂)</option>
                              <option value="slice_c">↕️ Высота среза c</option>
                            </select>
                          </div>
                          <div>
                            <span style="font-size:10px;font-weight:600;color:#94a3b8;display:block;margin-bottom:2px;">Стиль HUD:</span>
                            <select id="dm-cam-filter" class="dm-select" style="width:100%;font-size:11px;padding:2px 4px;background:#1e293b;color:#f8fafc;border-color:#334155;">
                              <option value="neon" selected>⚡ Cyberpunk</option>
                              <option value="thermal">🔥 Тепловизор</option>
                              <option value="normal">🎥 Обычный</option>
                            </select>
                          </div>
                        </div>

                        <div style="display:flex;align-items:center;justify-content:space-between;gap:6px;margin-bottom:6px;">
                          <span style="font-size:11px;font-weight:600;color:#94a3b8;">Режим:</span>
                          <select id="dm-cam-mode" class="dm-select" style="flex:1;font-size:11px;padding:2px 6px;background:#1e293b;color:#f8fafc;border-color:#334155;">
                            <option value="swipe" selected>Взмахи / Инерция</option>
                            <option value="joystick">Джойстик (смещение)</option>
                            <option value="direct">1:1 Слежение</option>
                          </select>
                        </div>

                        <div style="display:flex;align-items:center;justify-content:space-between;gap:6px;">
                          <span style="font-size:11px;font-weight:600;color:#94a3b8;">Зум:</span>
                          <button id="dm-cam-zoom-out" class="dm-cam-icon-btn" style="background:#1e293b;padding:1px 6px;font-size:11px;" title="Отдалить 3D">🔍−</button>
                          <button id="dm-cam-zoom-in" class="dm-cam-icon-btn" style="background:#1e293b;padding:1px 6px;font-size:11px;" title="Приблизить 3D">🔍+</button>
                          <span style="font-size:11px;font-weight:600;color:#94a3b8;margin-left:4px;">Чувств:</span>
                          <input id="dm-cam-speed" type="range" min="0.3" max="2.5" step="0.1" value="1.1" style="flex:1;height:4px;accent-color:#0d9488;" />
                          <span id="dm-cam-speed-val" style="font-size:10px;font-family:monospace;color:#38bdf8;">1.1x</span>
                        </div>

                        <div id="dm-cam-status-msg" style="margin-top:6px;font-size:10.5px;color:#38bdf8;text-align:center;font-weight:600;">
                          Помашите рукой в воздухе для управления
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- МАТЕМАТИЧЕСКАЯ СВОДКА В РЕАЛЬНОМ ВРЕМЕНИ -->
                <div id="dm-math-bar" class="dm-math-footer"></div>
              </div>
            `;

            const dom = {
              apiKey: el.querySelector("#dm-apikey"),
              micBtn: el.querySelector("#dm-mic-btn"),
              lang: el.querySelector("#dm-lang"),
              nlInput: el.querySelector("#dm-nl-input"),
              nlRun: el.querySelector("#dm-nl-run"),
              nlAi: el.querySelector("#dm-nl-ai"),
              voiceLive: el.querySelector("#dm-voice-live"),
              preset: el.querySelector("#dm-preset"),
              formula: el.querySelector("#dm-formula"),
              xmin: el.querySelector("#dm-xmin"),
              xmax: el.querySelector("#dm-xmax"),
              vfWrap: el.querySelector("#dm-vf-inputs"),
              vfu: el.querySelector("#dm-vfu"),
              vfv: el.querySelector("#dm-vfv"),
              slA1: el.querySelector("#dm-sl-a1"),
              slA2: el.querySelector("#dm-sl-a2"),
              slC: el.querySelector("#dm-sl-c"),
              slExtra: el.querySelector("#dm-sl-extra"),
              valA1: el.querySelector("#dm-val-a1"),
              valA2: el.querySelector("#dm-val-a2"),
              valC: el.querySelector("#dm-val-c"),
              valExtra: el.querySelector("#dm-val-extra"),
              lblExtra: el.querySelector("#dm-lbl-extra"),
              playA1: el.querySelector("#dm-play-a1"),
              playA2: el.querySelector("#dm-play-a2"),
              playC: el.querySelector("#dm-play-c"),
              playExtra: el.querySelector("#dm-play-extra"),
              chipLevel: el.querySelector("#chip-level"),
              chipTraces: el.querySelector("#chip-traces"),
              chipTangent: el.querySelector("#chip-tangent"),
              chipBall: el.querySelector("#chip-ball"),
              chipRiemann: el.querySelector("#chip-riemann"),
              chipVf: el.querySelector("#chip-vf"),
              chipDisk: el.querySelector("#chip-disk"),
              chip2d: el.querySelector("#chip-2d"),
              chipGrid: el.querySelector("#chip-grid"),
              animOrbit: el.querySelector("#anim-orbit"),
              animA2: el.querySelector("#anim-a2"),
              animC: el.querySelector("#anim-c"),
              animRnt: el.querySelector("#anim-rnt"),
              animStop: el.querySelector("#anim-stop"),
              title: el.querySelector("#dm-title"),
              status: el.querySelector("#dm-status"),
              plot: el.querySelector("#dm-plot"),
              mathBar: el.querySelector("#dm-math-bar"),
              camBtn: el.querySelector("#dm-cam-btn"),
              plotWrap: el.querySelector("#dm-plot-wrap"),
              camPip: el.querySelector("#dm-cam-pip"),
              camHeader: el.querySelector("#dm-cam-header"),
              camMinBtn: el.querySelector("#dm-cam-min-btn"),
              camCloseBtn: el.querySelector("#dm-cam-close-btn"),
              camContent: el.querySelector("#dm-cam-content"),
              camVideo: el.querySelector("#dm-cam-video"),
              camCanvas: el.querySelector("#dm-cam-canvas"),
              camMode: el.querySelector("#dm-cam-mode"),
              camSpeed: el.querySelector("#dm-cam-speed"),
              camSpeedVal: el.querySelector("#dm-cam-speed-val"),
              camStatusMsg: el.querySelector("#dm-cam-status-msg"),
              camResetBtn: el.querySelector("#dm-cam-reset-btn"),
              camFreezeBtn: el.querySelector("#dm-cam-freeze-btn"),
              camSnapBtn: el.querySelector("#dm-cam-snap-btn"),
              camTarget: el.querySelector("#dm-cam-target"),
              camFilter: el.querySelector("#dm-cam-filter"),
              camZoomIn: el.querySelector("#dm-cam-zoom-in"),
              camZoomOut: el.querySelector("#dm-cam-zoom-out"),
              camMeterBar: el.querySelector("#dm-cam-meter-bar"),
            };

            dom.apiKey.value = model.get("api_key") || "";
            dom.apiKey.addEventListener("change", () => {
              model.set("api_key", dom.apiKey.value.trim());
              model.save_changes();
            });

            // Подсветка авто-заполненных полей при парсинге
            function flashInsertedInputs() {
              [dom.formula, dom.xmin, dom.xmax].forEach((inp) => {
                inp.classList.add("dm-input-highlight");
                setTimeout(() => inp.classList.remove("dm-input-highlight"), 700);
              });
            }

            // Плавный доводчик (tween) ползунков к новым целевым координатам, когда анимация = 'none'
            function tweenSlidersTo(targetA1, targetA2, targetC, targetExtra) {
              if (tweenRaf) cancelAnimationFrame(tweenRaf);
              const startA1 = parseFloat(dom.slA1.value) || 0;
              const startA2 = parseFloat(dom.slA2.value) || 0;
              const startC = parseFloat(dom.slC.value) || 0;
              const startEx = parseFloat(dom.slExtra.value) || 0.9;
              const diff =
                Math.abs(targetA1 - startA1) +
                Math.abs(targetA2 - startA2) +
                Math.abs(targetC - startC) +
                Math.abs(targetExtra - startEx);
              if (diff < 0.02) {
                syncControlsFromState(false);
                renderPlot();
                return;
              }
              const duration = 520;
              const t0 = performance.now();
              function stepTween(now) {
                const p = Math.min(1, (now - t0) / duration);
                const ease = 1 - Math.pow(1 - p, 3);
                state.a1 = startA1 + (targetA1 - startA1) * ease;
                state.a2 = startA2 + (targetA2 - startA2) * ease;
                state.c_val = startC + (targetC - startC) * ease;
                state.extra_val = startEx + (targetExtra - startEx) * ease;
                syncSliderThumbsOnly();
                renderPlot();
                if (p < 1 && state.anim_mode === "none" && !userDraggingSlider) {
                  tweenRaf = requestAnimationFrame(stepTween);
                } else {
                  tweenRaf = null;
                }
              }
              tweenRaf = requestAnimationFrame(stepTween);
            }

            function syncSliderThumbsOnly() {
              const xMin = state.x1_range ? state.x1_range[0] : -1.8;
              const xMax = state.x1_range ? state.x1_range[1] : 1.8;
              dom.slA1.min = xMin;
              dom.slA1.max = xMax;
              dom.slA1.step = ((xMax - xMin) / 180).toFixed(4);
              dom.slA2.min = xMin;
              dom.slA2.max = xMax;
              dom.slA2.step = ((xMax - xMin) / 180).toFixed(4);

              dom.slA1.value = state.a1;
              dom.slA2.value = state.a2;
              dom.slC.value = state.c_val;
              dom.slExtra.value = state.extra_val;

              dom.valA1.textContent = Number(state.a1).toFixed(2);
              dom.valA2.textContent = Number(state.a2).toFixed(2);
              dom.valC.textContent = Number(state.c_val).toFixed(2);
              dom.valExtra.textContent = state.show_riemann
                ? "N = " + Math.max(2, Math.round(state.extra_val))
                : Number(state.extra_val).toFixed(2);
            }

            // Полная синхронизация всех полей ввода, ползунков и чипов со стейтом
            function syncControlsFromState(animateSliders = false) {
              const xMin = state.x1_range ? state.x1_range[0] : -1.8;
              const xMax = state.x1_range ? state.x1_range[1] : 1.8;

              if (state.preset_id && dom.preset.value !== state.preset_id) {
                dom.preset.value = state.preset_id;
              }
              dom.formula.value = state.formula || "x1^2 - x2^2";
              dom.xmin.value = xMin;
              dom.xmax.value = xMax;
              dom.vfu.value = state.vector_u || "-x2";
              dom.vfv.value = state.vector_v || "x1";
              dom.vfWrap.style.display = state.show_vector_field ? "block" : "none";

              if (state.show_riemann) {
                dom.lblExtra.innerHTML = "📊 Разбиений Римана <b>N</b>:";
              } else if (state.show_vector_field) {
                dom.lblExtra.innerHTML = "⏱️ Длина потока <b>t</b>:";
              } else {
                dom.lblExtra.innerHTML = "⭕ Радиус шара <b>r (B_r)</b>:";
              }

              const setChip = (chip, on) => chip.classList.toggle("active", !!on);
              setChip(dom.chipLevel, state.show_level_plane);
              setChip(dom.chipTraces, state.show_xy_traces);
              setChip(dom.chipTangent, state.show_tangent);
              setChip(dom.chipBall, state.show_ball);
              setChip(dom.chipRiemann, state.show_riemann);
              setChip(dom.chipVf, state.show_vector_field);
              setChip(dom.chipDisk, state.circular_domain);
              setChip(dom.chip2d, state.split_2d);
              setChip(dom.chipGrid, state.show_box_grid);

              const mode = state.anim_mode || "none";
              dom.playA1.classList.toggle("playing", mode === "a1");
              dom.playA1.textContent = mode === "a1" ? "⏸" : "▶";
              dom.playA2.classList.toggle("playing", mode === "a2");
              dom.playA2.textContent = mode === "a2" ? "⏸" : "▶";
              dom.playC.classList.toggle("playing", mode === "c");
              dom.playC.textContent = mode === "c" ? "⏸" : "▶";
              dom.playExtra.classList.toggle("playing", mode === "rnt");
              dom.playExtra.textContent = mode === "rnt" ? "⏸" : "▶";

              dom.animOrbit.classList.toggle("active", mode === "orbit");
              dom.animA2.classList.toggle("active", mode === "a2");
              dom.animC.classList.toggle("active", mode === "c");
              dom.animRnt.classList.toggle("active", mode === "rnt");

              dom.title.textContent = state.title || ("Поверхность y = " + dom.formula.value);
              dom.status.textContent = state.status || "⚡ Готово";

              if (typeof state.cam_active === "boolean" && state.cam_active !== camActive) {
                if (state.cam_active) startWebcamTracking();
                else stopWebcamTracking();
              }

              if (animateSliders && mode === "none") {
                tweenSlidersTo(state.a1, state.a2, state.c_val, state.extra_val);
              } else {
                syncSliderThumbsOnly();
              }
              updateAnimationLoop();
            }

            // Цикл плавной 60 FPS авто-анимации ползунков
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
                  animPhase += dt * 1.35;
                  const xMin = state.x1_range ? state.x1_range[0] : -1.8;
                  const xMax = state.x1_range ? state.x1_range[1] : 1.8;
                  const xMid = 0.5 * (xMin + xMax);
                  const xAmp = 0.42 * (xMax - xMin);

                  if (curMode === "a1") {
                    state.a1 = xMid + xAmp * Math.sin(animPhase);
                  } else if (curMode === "a2") {
                    state.a2 = xMid + xAmp * Math.sin(animPhase);
                  } else if (curMode === "orbit") {
                    state.a1 = xMid + xAmp * 0.78 * Math.cos(animPhase);
                    state.a2 = xMid + xAmp * 0.78 * Math.sin(animPhase);
                  } else if (curMode === "c") {
                    const cMin = parseFloat(dom.slC.min) || -2.5;
                    const cMax = parseFloat(dom.slC.max) || 2.5;
                    const cMid = 0.5 * (cMin + cMax);
                    const cAmp = 0.44 * (cMax - cMin);
                    state.c_val = cMid + cAmp * Math.sin(animPhase);
                  } else if (curMode === "rnt") {
                    if (state.show_riemann) {
                      state.extra_val = 2 + ((Math.sin(animPhase * 0.85) + 1) * 0.5) * 12;
                    } else if (state.show_vector_field) {
                      state.extra_val = 0.8 + ((Math.sin(animPhase * 0.9) + 1) * 0.5) * 8.5;
                    } else {
                      state.extra_val = 0.25 + ((Math.sin(animPhase * 1.1) + 1) * 0.5) * 1.35;
                    }
                  }
                  syncSliderThumbsOnly();
                  renderPlot();
                }
                animRaf = requestAnimationFrame(stepAnim);
              }
              animRaf = requestAnimationFrame(stepAnim);
            }

            // Быстрый клиентский парсер (0.2 мс) + синхронизация с Python / Gemini AI
            const JS_PRESETS = {
              preset_lecture14: {
                preset_id: "preset_lecture14",
                title: "Lecture 14: Сечение поверхности y = x₁² - x₂² плоскостью y = c",
                formula: "x1^2 - x2^2", vector_u: "-x2", vector_v: "x1",
                x1_range: [-1.8, 1.8], x2_range: [-1.8, 1.8],
                a1: 0.55, a2: 0.85, c_val: -0.50, extra_val: 0.90,
                show_level_plane: true, show_xy_traces: false, show_tangent: false,
                show_ball: false, show_riemann: false, show_vector_field: false,
                circular_domain: true, split_2d: false, show_box_grid: false,
                anim_mode: "none", cam_active: false,
                status: "⚡ Пресет Lecture 14: сечение плоскостью y = c"
              },
              preset_trace: {
                preset_id: "preset_trace",
                title: "Slices & Traces: Срезы z = sin(x₁)·cos(x₂) плоскостями x₁ = a₁ и x₂ = a₂",
                formula: "sin(x1) * cos(x2)", vector_u: "-x2", vector_v: "x1",
                x1_range: [-3.2, 3.2], x2_range: [-3.2, 3.2],
                a1: 1.0, a2: 0.6, c_val: 0.0, extra_val: 1.0,
                show_level_plane: false, show_xy_traces: true, show_tangent: false,
                show_ball: false, show_riemann: false, show_vector_field: false,
                circular_domain: false, split_2d: true, show_box_grid: false,
                anim_mode: "a2", cam_active: false,
                status: "🎬 Авто-анимация среза x₂ = a₂ запущена"
              },
              preset_tangent: {
                preset_id: "preset_tangent",
                title: "Касательная плоскость, нормаль и градиент ∇f(a) к y = x₁² - x₂²",
                formula: "x1^2 - x2^2", vector_u: "-x2", vector_v: "x1",
                x1_range: [-1.8, 1.8], x2_range: [-1.8, 1.8],
                a1: 0.80, a2: 0.45, c_val: 0.44, extra_val: 0.90,
                show_level_plane: true, show_xy_traces: false, show_tangent: true,
                show_ball: false, show_riemann: false, show_vector_field: false,
                circular_domain: true, split_2d: true, show_box_grid: false,
                anim_mode: "orbit", cam_active: false,
                status: "🎬 Авто-анимация точки a=(a₁, a₂) и касательной плоскости"
              },
              preset_flow: {
                preset_id: "preset_flow",
                title: "Векторное поле F(x₁, x₂) = [-x₂, x₁] и линия тока r(t)",
                formula: "0.15 * (x1^2 + x2^2)", vector_u: "-x2", vector_v: "x1",
                x1_range: [-2.8, 2.8], x2_range: [-2.8, 2.8],
                a1: 1.6, a2: 0.3, c_val: 0.4, extra_val: 5.5,
                show_level_plane: false, show_xy_traces: false, show_tangent: false,
                show_ball: false, show_riemann: false, show_vector_field: true,
                circular_domain: false, split_2d: true, show_box_grid: false,
                anim_mode: "rnt", cam_active: false,
                status: "🎬 Авто-анимация потока векторного поля r(t)"
              },
              preset_riemann: {
                preset_id: "preset_riemann",
                title: "Двойной интеграл и 3D суммы Римана: f(x₁, x₂) = 4 - x₁² - x₂²",
                formula: "4 - x1^2 - x2^2", vector_u: "-x2", vector_v: "x1",
                x1_range: [-1.6, 1.6], x2_range: [-1.6, 1.6],
                a1: 0.7, a2: 0.7, c_val: 1.5, extra_val: 7.0,
                show_level_plane: false, show_xy_traces: false, show_tangent: false,
                show_ball: false, show_riemann: true, show_vector_field: false,
                circular_domain: false, split_2d: false, show_box_grid: false,
                anim_mode: "rnt", cam_active: false,
                status: "🎬 Авто-анимация числа разбиений Римана N"
              },
              preset_ball: {
                preset_id: "preset_ball",
                title: "Открытая окрестность B_r(a) и граница ∂B_r(a) вокруг точки a=(a₁, a₂)",
                formula: "x1^2 + x2^2 - 1", vector_u: "-x2", vector_v: "x1",
                x1_range: [-2.0, 2.0], x2_range: [-2.0, 2.0],
                a1: 0.55, a2: 0.45, c_val: -0.50, extra_val: 0.85,
                show_level_plane: true, show_xy_traces: false, show_tangent: false,
                show_ball: true, show_riemann: false, show_vector_field: false,
                circular_domain: true, split_2d: true, show_box_grid: false,
                anim_mode: "rnt", cam_active: false,
                status: "🎬 Авто-анимация радиуса окрестности B_r(a)"
              }
            };

            function normalizeSpokenJS(raw) {
              let s = String(raw || "").trim();
              const uni = {
                "⁰":"^0","¹":"^1","²":"^2","³":"^3","⁴":"^4","⁵":"^5","⁶":"^6","⁷":"^7","⁸":"^8","⁹":"^9",
                "⁻":"-","₁":"1","₂":"2","₃":"3","−":"-","–":"-","—":"-","×":"*","·":"*","∙":"*","÷":"/","π":"pi"
              };
              for (const [k, v] of Object.entries(uni)) s = s.split(k).join(v);
              s = s.replace(/√\s*\(([^)]+)\)/g, "sqrt($1)").replace(/√\s*([a-zA-Z0-9_]+)/g, "sqrt($1)");
              s = s.replace(/(\d),(\d)/g, "$1.$2");
              const nums = [
                [/минус\s+полтора/gi, "-1.5"], [/полтора/gi, "1.5"], [/ноль\s+пять/gi, "0.5"],
                [/(?<![a-zA-Zа-яА-Я])(?:ноль|нулю|нуля|zero)(?![a-zA-Zа-яА-Я])/gi, "0"],
                [/(?<![a-zA-Zа-яА-Я])(?:единиц[аеыу]|один|одной|одного|one)(?![a-zA-Zа-яА-Я])/gi, "1"],
                [/(?<![a-zA-Zа-яА-Я])(?:два|двух|two)(?![a-zA-Zа-яА-Я])/gi, "2"],
                [/(?<![a-zA-Zа-яА-Я])(?:три|трех|трёх|three)(?![a-zA-Zа-яА-Я])/gi, "3"],
                [/(?<![a-zA-Zа-яА-Я])(?:четыре|четырех|four)(?![a-zA-Zа-яА-Я])/gi, "4"],
                [/(?<![a-zA-Zа-яА-Я])(?:пять|пяти|five)(?![a-zA-Zа-яА-Я])/gi, "5"],
                [/(?<![a-zA-Zа-яА-Я])(?:шесть|шести|six)(?![a-zA-Zа-яА-Я])/gi, "6"],
                [/(?<![a-zA-Zа-яА-Я])(?:семь|семи|seven)(?![a-zA-Zа-яА-Я])/gi, "7"],
                [/(?<![a-zA-Zа-яА-Я])(?:восемь|восьми|eight)(?![a-zA-Zа-яА-Я])/gi, "8"],
                [/(?<![a-zA-Zа-яА-Я])(?:девять|девяти|nine)(?![a-zA-Zа-яА-Я])/gi, "9"],
                [/(?<![a-zA-Zа-яА-Я])(?:десять|десяти|ten)(?![a-zA-Zа-яА-Я])/gi, "10"],
                [/(?<![a-zA-Zа-яА-Я])(?:двенадцать|twelve)(?![a-zA-Zа-яА-Я])/gi, "12"],
                [/(?<![a-zA-Zа-яА-Я])(?:шестнадцать|sixteen)(?![a-zA-Zа-яА-Я])/gi, "16"]
              ];
              for (const [rx, rep] of nums) s = s.replace(rx, rep);
              const ops = [
                [/(?<![a-zA-Zа-яА-Я])(?:а|a)\s*_?\s*1(?![a-zA-Zа-яА-Я0-9])/gi, "a1"],
                [/(?<![a-zA-Zа-яА-Я])(?:а|a)\s*_?\s*2(?![a-zA-Zа-яА-Я0-9])/gi, "a2"],
                [/(?<![a-zA-Zа-яА-Я])(?:икс|х|x)\s*_?\s*1(?![a-zA-Zа-яА-Я0-9])/gi, "x1"],
                [/(?<![a-zA-Zа-яА-Я])(?:икс|х|x)\s*_?\s*2(?![a-zA-Zа-яА-Я0-9])/gi, "x2"],
                [/(?<![a-zA-Zа-яА-Я])игрек(?![a-zA-Zа-яА-Я])/gi, "x2"],
                [/(?<![a-zA-Zа-яА-Я])икс(?![a-zA-Zа-яА-Я])/gi, "x1"],
                [/\b(?:to\s+the\s+)?power\s+(?:of\s+)?(\d+)/gi, "^$1"],
                [/(?:в\s+квадрате|квадрат|squared)/gi, "^2"],
                [/(?:в\s+кубе|куб|cubed)/gi, "^3"],
                [/в\s+четвертой\s+степени/gi, "^4"],
                [/в\s+степени\s*(\d+)/gi, "^$1"],
                [/(?:корень\s+(?:из\s+)?|square\s+root\s+(?:of\s+)?)([a-zA-Z0-9_\^\+\-\*]+)/gi, "sqrt($1)"],
                [/(?:синус(?:\s+от)?|sine\s+of|sine|sin\s+of)\s*\(?\s*([a-zA-Z0-9_]+)\s*\)?/gi, "sin($1)"],
                [/(?:косинус(?:\s+от)?|cosine\s+of|cosine|cos\s+of)\s*\(?\s*([a-zA-Z0-9_]+)\s*\)?/gi, "cos($1)"],
                [/(?:тангенс(?:\s+от)?|tangent\s+of|tangent)\s*\(?\s*([a-zA-Z0-9_]+)\s*\)?/gi, "tan($1)"],
                [/(?:экспонента(?:\s+от)?|exponential\s+of)\s*\(?\s*([a-zA-Z0-9_]+)\s*\)?/gi, "exp($1)"],
                [/(?:умножить\s+на|умножить|multiplied\s+by|times)/gi, "*"],
                [/(?:разделить\s+на|делить\s+на|деленное\s+на|divided\s+by|over)/gi, "/"],
                [/(?:плюс|plus|прибавить)/gi, "+"],
                [/(?:минус|minus|вычесть)/gi, "-"],
                [/(?:равно|равен|равна|равном|equals|equal\s+to)/gi, "="]
              ];
              for (const [rx, rep] of ops) s = s.replace(rx, rep);
              return s;
            }

            function applyLocalCommandImmediate(rawText) {
              const norm = normalizeSpokenJS(rawText);
              const low = norm.toLowerCase().trim();
              if (!low) return;

              if (["сброс", "сначала", "лекция 14", "lecture 14", "reset"].some(w => low.includes(w))) {
                state = JSON.parse(JSON.stringify(JS_PRESETS.preset_lecture14));
                flashInsertedInputs();
                syncControlsFromState(false);
                renderPlot();
                return;
              }

              const turnOff = ["скрой", "убери", "выключи", "hide", "disable", "remove"].some(w => low.includes(w));
              const wantsStop = ["стоп", "останови", "пауза", "зафиксируй", "не двигай", "stop", "pause"].some(w => low.includes(w));
              let parts = [];
              let topicAnim = null;

              const named = [
                [["mess", "chaotic", "crazy", "хаос", "безумн", "сложн", "шум"], "0.7*sin(3*x1)*cos(3*x2) + 0.5*cos(4*x1*x2)"],
                [["обезьянье седло", "monkey saddle"], "x1^3 - 3*x1*x2^2"],
                [["седло", "седлов", "гипербол", "saddle"], "x1^2 - x2^2"],
                [["перевернут", "купол", "шапк", "inverted", "dome"], "4 - x1^2 - x2^2"],
                [["парабол", "чаш", "parabol", "bowl"], "x1^2 + x2^2 - 1"],
                [["сфер", "полусфер", "sphere", "hemisphere"], "sqrt(max(0, 2.5 - x1^2 - x2^2))"],
                [["гаусс", "колокол", "холм", "gaussian", "bell"], "2.2 * exp(-(x1^2 + x2^2))"],
                [["вулкан", "кратер", "volcano", "crater"], "2.5 * (x1^2 + x2^2) * exp(-(x1^2 + x2^2))"],
                [["волн", "синусоид", "waves", "wave"], "sin(x1) * cos(x2)"],
                [["сомбреро", "капл", "рябь", "ripple", "sombrero"], "sin(2.5 * sqrt(x1^2 + x2^2))"],
                [["конус", "воронк", "cone", "funnel"], "sqrt(x1^2 + x2^2)"],
                [["цилиндр", "желоб", "cylinder"], "x1^2"],
                [["пирамид", "крыш", "pyramid", "roof"], "2 - abs(x1) - abs(x2)"]
              ];
              for (const [kws, fStr] of named) {
                if (kws.some(k => low.includes(k))) {
                  state.formula = fStr;
                  state.title = "Поверхность y = " + fStr;
                  parts.push("f = " + fStr);
                  break;
                }
              }

              // Векторное поле [u, v]
              const vfM = low.match(/\[\s*([^,\]]+)\s*,\s*([^\]]+)\s*\]/);
              if (vfM) {
                state.vector_u = vfM[1].trim();
                state.vector_v = vfM[2].trim();
                state.show_vector_field = true;
                topicAnim = "rnt";
                parts.push(`F = [${state.vector_u}, ${state.vector_v}]`);
              }

              // Диапазон от A до B
              const rngM = low.match(/(?:от|from)\s+(-?\d+(?:\.\d+)?)\s+(?:до|to)\s+(-?\d+(?:\.\d+)?)/);
              if (rngM) {
                let r1 = parseFloat(rngM[1]), r2 = parseFloat(rngM[2]);
                if (r2 < r1) [r1, r2] = [r2, r1];
                if (r2 - r1 >= 0.2) {
                  state.x1_range = [r1, r2];
                  state.x2_range = [r1, r2];
                  if (Math.abs(r1 + r2) > 0.1) state.circular_domain = false;
                  parts.push(`диапазон [${r1}, ${r2}]`);
                }
              }

              // Точка (a1, a2) и срезы x1=..., x2=...
              const ptM = low.match(/(?:точк[еауи]|point)\s*\(?\s*(-?\d+(?:\.\d+)?)\s*(?:,|и|and|\s)\s*(-?\d+(?:\.\d+)?)\s*\)?/);
              if (ptM) {
                state.a1 = parseFloat(ptM[1]);
                state.a2 = parseFloat(ptM[2]);
                parts.push(`a = (${state.a1}, ${state.a2})`);
              }
              const a1M = low.match(/(?:при\s+|по\s+|at\s+)?\b(?:a1|x1)\s*=\s*(-?\d+(?:\.\d+)?)/);
              if (a1M) {
                state.a1 = parseFloat(a1M[1]);
                parts.push(`x₁ = ${state.a1}`);
              }
              const a2M = low.match(/(?:при\s+|по\s+|at\s+)?\b(?:a2|x2)\s*=\s*(-?\d+(?:\.\d+)?)/);
              if (a2M) {
                state.a2 = parseFloat(a2M[1]);
                parts.push(`x₂ = ${state.a2}`);
              }

              // Авто-расширение диапазона под выбранную точку
              for (const val of [state.a1, state.a2]) {
                if (val < state.x1_range[0] || val > state.x1_range[1]) {
                  const pad = Math.max(1.0, Math.abs(val) * 0.35);
                  const nMin = Math.min(state.x1_range[0], val - pad);
                  const nMax = Math.max(state.x1_range[1], val + pad);
                  state.x1_range = [Number(nMin.toFixed(2)), Number(nMax.toFixed(2))];
                  state.x2_range = [Number(nMin.toFixed(2)), Number(nMax.toFixed(2))];
                  state.circular_domain = false;
                }
              }

              const cM = low.match(/\b(?:уровень|высота|при\s+y|при\s+c|level|c)\s*=?\s*(-?\d+(?:\.\d+)?)/);
              if (cM) {
                state.c_val = parseFloat(cM[1]);
                state.show_level_plane = true;
                parts.push(`c = ${state.c_val}`);
              }

              const rntM = low.match(/\b(?:разбиений|призм|радиус[ае]?|шар\s+радиуса|время|radius|partitions|time|r|t|n)\s*=?\s*(-?\d+(?:\.\d+)?)/);
              if (rntM) {
                state.extra_val = Math.max(0.15, parseFloat(rntM[1]));
                parts.push(`r/N/t = ${state.extra_val}`);
              }

              // Слои
              if (["касательн", "градиент", "нормал", "tangent", "gradient"].some(w => low.includes(w))) {
                state.show_tangent = !turnOff;
                if (!turnOff) topicAnim = "orbit";
                parts.push("касательная + ∇f");
              }
              if (["риман", "riemann", "интеграл", "integral", "призм", "объем", "volume"].some(w => low.includes(w))) {
                state.show_riemann = !turnOff;
                if (!turnOff) {
                  if (state.extra_val < 2) state.extra_val = 7;
                  topicAnim = "rnt";
                }
                parts.push("суммы Римана");
              }
              if (["векторн", "поток", "линию тока", "линия тока", "vector field", "flow"].some(w => low.includes(w))) {
                state.show_vector_field = !turnOff;
                if (!turnOff) {
                  if (state.extra_val < 1) state.extra_val = 5;
                  topicAnim = "rnt";
                }
                parts.push("векторное поле");
              }
              if (["шар", "окрестност", "ball", "neighborhood", "границу"].some(w => low.includes(w))) {
                state.show_ball = !turnOff;
                if (!turnOff) {
                  if (state.extra_val > 2.5) state.extra_val = 0.85;
                  topicAnim = "rnt";
                }
                parts.push("окрестность B_r(a)");
              }
              if (["вертикальн", "след", "срезы", "срез", "по x1", "по x2", "при x1", "при x2", "slice", "trace"].some(w => low.includes(w))) {
                state.show_xy_traces = !turnOff;
                if (!turnOff) topicAnim = (low.includes("x1") && !low.includes("x2")) ? "a1" : "a2";
                parts.push("срезы");
              } else if (["сечен", "линию уровня", "линия уровня", "уровн", "level"].some(w => low.includes(w))) {
                state.show_level_plane = !turnOff;
                if (!turnOff) topicAnim = "c";
                parts.push("сечение y = c");
              }
              if (["2d", "2д", "двумерн", "карта", "контур", "contour"].some(w => low.includes(w))) {
                state.split_2d = !turnOff;
              }

              if (["включи камеру", "вруби камеру", "крути через камеру", "крути камерой", "управление камерой", "камеру", "жестами", "camera on", "webcam"].some(w => low.includes(w))) {
                state.cam_active = true;
                parts.push("📷 управление камерой ВКЛ");
                startWebcamTracking();
              } else if (["выключи камеру", "отключи камеру", "закрой камеру", "camera off"].some(w => low.includes(w))) {
                state.cam_active = false;
                parts.push("📷 управление камерой ВЫКЛ");
                stopWebcamTracking();
              } else if (["сделай снимок", "сфотографируй", "снимок", "скриншот", "snapshot", "screenshot"].some(w => low.includes(w))) {
                takeSnapshot();
                parts.push("📸 снимок сохранен");
              } else if (["сбрось ракурс", "сбрось камеру", "исходный ракурс", "дефолтный ракурс", "reset view", "home view"].some(w => low.includes(w))) {
                resetCameraHome();
                parts.push("🎯 ракурс сброшен");
              } else if (["управляй точкой", "указка", "air pointer", "двигай точку"].some(w => low.includes(w))) {
                if (dom.camTarget) dom.camTarget.value = "point";
                parts.push("📍 цель жестов: точка a");
                startWebcamTracking();
              } else if (["управляй срезом", "управляй высотой", "двигай срез", "двигай уровень"].some(w => low.includes(w))) {
                if (dom.camTarget) dom.camTarget.value = "slice_c";
                parts.push("↕️ цель жестов: высота среза c");
                startWebcamTracking();
              } else if (["вращай сцену", "крути сцену", "крути фигуру", "вращение фигуры"].some(w => low.includes(w))) {
                if (dom.camTarget) dom.camTarget.value = "orbit";
                parts.push("🔄 цель жестов: вращение 3D");
                startWebcamTracking();
              }

              // Извлечение математической формулы из любой части фразы
              let fSrc = low;
              if (vfM) fSrc = fSrc.replace(vfM[0], " ");
              fSrc = fSrc.replace(/\b[23][dд]\b/g, " ");
              fSrc = fSrc.replace(/(?:от|from)\s+-?\d+(?:\.\d+)?\s+(?:до|to)\s+-?\d+(?:\.\d+)?/g, " ");
              fSrc = fSrc.replace(/(?:точк[еауи]|point)\s*\(?\s*-?\d+(?:\.\d+)?\s*(?:,|и|and|\s)\s*-?\d+(?:\.\d+)?\s*\)?/g, " ");
              fSrc = fSrc.replace(/\b(?:при\s+|по\s+|at\s+)?(?:a1|a2|x1|x2|уровень|высота|level|разбиений|призм|радиус[ае]?|время|radius|time|c|r|t|n)\s*=\s*-?\d+(?:\.\d+)?/g, " ");
              fSrc = fSrc.replace(/\b[fzy]\s*(\([^)]*\))?\s*=\s*/g, " ");

              const spanRx = /(?:(?:sin|cos|tan|exp|sqrt|log|abs|pi|x1|x2)|(?<![a-zA-Z0-9_])[xy](?![a-zA-Z0-9_])|\d+(?:\.\d+)?|[\+\-\*\/\^\(\)])(?:\s*(?:(?:sin|cos|tan|exp|sqrt|log|abs|pi|x1|x2)|(?<![a-zA-Z0-9_])[xy](?![a-zA-Z0-9_])|\d+(?:\.\d+)?|[\+\-\*\/\^\(\)]))*/g;
              const matches = fSrc.match(spanRx) || [];
              const validSpans = matches
                .map(m => m.replace(/\s*\^\s*/g, "^").replace(/^[\+\*\/\^]+|[\+\-\*\/\^]+$/g, "").trim())
                .filter(m => m.length >= 2 && (m.includes("x1") || m.includes("x2") || /\bx\b|\by\b/.test(m)))
                .sort((a, b) => b.length - a.length);

              if (validSpans.length > 0) {
                const cand = validSpans[0].replace(/\bx\b/g, "x1").replace(/\by\b/g, "x2");
                state.formula = cand;
                state.title = "Поверхность y = " + cand;
                parts.push("f = " + cand);
              }

              // Анимация включается ТОЛЬКО если пользователь прямо попросил движение/анимацию
              const wantsAnim = ["анимир", "анимац", "двиг", "передвиг", "динамик", "крути", "качай", "прокрут", "sweep", "animate", "animation"].some(w => low.includes(w));
              if (wantsStop) {
                state.anim_mode = "none";
              } else if (wantsAnim) {
                if (topicAnim) {
                  state.anim_mode = topicAnim;
                } else if (state.show_xy_traces) {
                  state.anim_mode = "a2";
                } else if (state.show_tangent) {
                  state.anim_mode = "orbit";
                } else if (state.show_riemann || state.show_vector_field || state.show_ball) {
                  state.anim_mode = "rnt";
                } else {
                  state.anim_mode = "c";
                }
                const xMin = state.x1_range[0], xMax = state.x1_range[1];
                const xMid = 0.5 * (xMin + xMax), xAmp = Math.max(0.1, 0.42 * (xMax - xMin));
                if (state.anim_mode === "a2") {
                  const ratio = Math.max(-1, Math.min(1, (state.a2 - xMid) / xAmp));
                  animPhase = Math.asin(ratio);
                } else if (state.anim_mode === "a1") {
                  const ratio = Math.max(-1, Math.min(1, (state.a1 - xMid) / xAmp));
                  animPhase = Math.asin(ratio);
                }
                parts.push(`🎬 запущена анимация (${state.anim_mode})`);
              } else if (topicAnim && state.anim_mode && state.anim_mode !== "none") {
                state.anim_mode = topicAnim;
              }

              state.status = "✅ Вставлено и запущено: " + (parts.join(", ") || rawText);
              flashInsertedInputs();
              syncControlsFromState(false);
              renderPlot();
            }

            // Отправка команды в Python (парсер + Gemini AI)
            function sendCommandToPython(cmdText, useAi = false, presetId = "") {
              if (presetId && JS_PRESETS[presetId]) {
                state = JSON.parse(JSON.stringify(JS_PRESETS[presetId]));
                flashInsertedInputs();
                syncControlsFromState(false);
                renderPlot();
              } else if (cmdText && !useAi) {
                applyLocalCommandImmediate(cmdText);
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

            // Слушатель обновлений стейта из Python
            model.on("change:state_json", () => {
              try {
                const next = JSON.parse(model.get("state_json") || "{}");
                isApplyingModelUpdate = true;
                state = next;
                flashInsertedInputs();
                syncControlsFromState(true);
                renderPlot();
                isApplyingModelUpdate = false;
              } catch (e) {}
            });

            // Обработчики ввода команды, пресета, формулы и диапазона
            dom.nlRun.addEventListener("click", () => {
              const txt = dom.nlInput.value.trim() || dom.formula.value.trim();
              if (txt) {
                dom.status.textContent = "⏳ Парсинг и вставка данных...";
                sendCommandToPython(txt, false, "");
              }
            });
            dom.nlInput.addEventListener("keydown", (e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                dom.nlRun.click();
              }
            });
            dom.nlAi.addEventListener("click", () => {
              const txt = dom.nlInput.value.trim() || dom.formula.value.trim() || "покажи интересную поверхность с анимацией";
              dom.status.textContent = "🤖 Запрос к Gemini 2.5 Flash...";
              sendCommandToPython(txt, true, "");
            });

            dom.preset.addEventListener("change", () => {
              sendCommandToPython("", false, dom.preset.value);
            });

            function applyFormulaAndRangeInputs() {
              if (isApplyingModelUpdate) return;
              state.formula = dom.formula.value.trim() || "x1^2 - x2^2";
              let xMin = parseFloat(dom.xmin.value);
              let xMax = parseFloat(dom.xmax.value);
              if (!isNaN(xMin) && !isNaN(xMax) && xMax - xMin >= 0.2) {
                state.x1_range = [xMin, xMax];
                state.x2_range = [xMin, xMax];
              }
              state.vector_u = dom.vfu.value.trim() || "-x2";
              state.vector_v = dom.vfv.value.trim() || "x1";
              state.title = "Поверхность y = " + state.formula;
              state.status = "⚡ Обновлена формула: y = " + state.formula;
              syncControlsFromState(false);
              renderPlot();
            }

            dom.formula.addEventListener("change", applyFormulaAndRangeInputs);
            dom.formula.addEventListener("keydown", (e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                applyFormulaAndRangeInputs();
              }
            });
            dom.xmin.addEventListener("change", applyFormulaAndRangeInputs);
            dom.xmax.addEventListener("change", applyFormulaAndRangeInputs);
            dom.vfu.addEventListener("change", applyFormulaAndRangeInputs);
            dom.vfv.addEventListener("change", applyFormulaAndRangeInputs);

            // Обработчики ручного движения ползунков
            window.addEventListener("pointerup", () => {
              userDraggingSlider = false;
            });
            [
              [dom.slA1, "a1"],
              [dom.slA2, "a2"],
              [dom.slC, "c_val"],
              [dom.slExtra, "extra_val"],
            ].forEach(([sl, key]) => {
              sl.addEventListener("pointerdown", () => {
                userDraggingSlider = true;
              });
              sl.addEventListener("pointerup", () => {
                userDraggingSlider = false;
              });
              sl.addEventListener("input", () => {
                state[key] = parseFloat(sl.value);
                syncSliderThumbsOnly();
                renderPlot();
              });
            });

            // Кнопки анимации на каждом ползунке и в панели
            function toggleAnimMode(targetMode) {
              state.anim_mode = state.anim_mode === targetMode ? "none" : targetMode;
              if (state.anim_mode === "a2" || state.anim_mode === "a1") state.show_xy_traces = true;
              if (state.anim_mode === "c") state.show_level_plane = true;
              syncControlsFromState(false);
            }
            dom.playA1.addEventListener("click", () => toggleAnimMode("a1"));
            dom.playA2.addEventListener("click", () => toggleAnimMode("a2"));
            dom.playC.addEventListener("click", () => toggleAnimMode("c"));
            dom.playExtra.addEventListener("click", () => toggleAnimMode("rnt"));
            dom.animOrbit.addEventListener("click", () => toggleAnimMode("orbit"));
            dom.animA2.addEventListener("click", () => toggleAnimMode("a2"));
            dom.animC.addEventListener("click", () => toggleAnimMode("c"));
            dom.animRnt.addEventListener("click", () => toggleAnimMode("rnt"));
            dom.animStop.addEventListener("click", () => {
              state.anim_mode = "none";
              syncControlsFromState(false);
            });

            // Чипы переключения слоев
            const chipMap = [
              [dom.chipLevel, "show_level_plane"],
              [dom.chipTraces, "show_xy_traces"],
              [dom.chipTangent, "show_tangent"],
              [dom.chipBall, "show_ball"],
              [dom.chipRiemann, "show_riemann"],
              [dom.chipVf, "show_vector_field"],
              [dom.chipDisk, "circular_domain"],
              [dom.chip2d, "split_2d"],
              [dom.chipGrid, "show_box_grid"],
            ];
            chipMap.forEach(([chipEl, key]) => {
              chipEl.addEventListener("click", () => {
                state[key] = !state[key];
                syncControlsFromState(false);
                renderPlot();
              });
            });

            // Web Speech API (Непрерывное голосовое управление)
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            let recognition = null;
            let isListening = false;

            if (SpeechRecognition) {
              recognition = new SpeechRecognition();
              recognition.continuous = true;
              recognition.interimResults = true;
              recognition.maxAlternatives = 1;

              let speechDebounceTimer = null;
              let lastDispatchedSpeech = "";

              const dispatchVoiceCmd = (rawTxt) => {
                const clean = String(rawTxt || "").trim();
                if (!clean || clean.toLowerCase() === lastDispatchedSpeech.toLowerCase()) return;
                lastDispatchedSpeech = clean;
                dom.nlInput.value = clean;
                dom.voiceLive.textContent = "🎙️ Распознано: «" + clean + "»";
                sendCommandToPython(clean, false, "");
              };

              recognition.onresult = (event) => {
                let interim = "";
                let finalCmd = "";
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                  const tr = event.results[i][0].transcript;
                  if (event.results[i].isFinal) {
                    finalCmd += tr;
                  } else {
                    interim += tr;
                  }
                }
                const cleanFinal = finalCmd.trim();
                const cleanInterim = interim.trim();

                if (cleanFinal) {
                  if (speechDebounceTimer) clearTimeout(speechDebounceTimer);
                  dispatchVoiceCmd(cleanFinal);
                } else if (cleanInterim) {
                  dom.voiceLive.textContent = "🗣️ Слушаю: «" + cleanInterim + "...»";
                  if (speechDebounceTimer) clearTimeout(speechDebounceTimer);
                  
                  // Мгновенное срабатывание при законченных командах (250-450 мс вместо ожидания 2 сек тишины Chrome)
                  const isQuickAction = /стоп|пауза|сброс|домой|снимок|скриншот|парабол|седл|сфер|конус|камер|указка|управл|замороз/i.test(cleanInterim);
                  const delayMs = isQuickAction ? 260 : 480;

                  speechDebounceTimer = setTimeout(() => {
                    dispatchVoiceCmd(cleanInterim);
                  }, delayMs);
                }
              };

              recognition.onerror = () => {};
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
                  dom.micBtn.textContent = "🔴 Live-микрофон АКТИВЕН";
                  dom.voiceLive.textContent = "Говорите команду (все данные и ползунки выставятся сами)...";
                } else {
                  try { recognition.stop(); } catch (e) {}
                  dom.micBtn.classList.remove("active");
                  dom.micBtn.textContent = "🎙️ Включить Live-микрофон";
                  dom.voiceLive.textContent = "";
                }
              });

              dom.lang.addEventListener("change", () => {
                if (isListening && recognition) {
                  try { recognition.stop(); } catch (e) {}
                  recognition.lang = dom.lang.value;
                }
              });
            } else {
              dom.micBtn.textContent = "⚠️ Браузер без Web Speech API";
              dom.micBtn.disabled = true;
            }

            // =========================================================================
            // ВЕБ-КАМЕРА: 3D ТРЕКИНГ ЖЕСТОВ И ВРАЩЕНИЕ ФИГУРЫ (60 FPS COMPUTER VISION)
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

            // Сферические координаты камеры Plotly
            let camTheta = -2.39;
            let camPhi = 0.38;
            let camDist = 2.27;
            let currentEye = { x: -1.55, y: -1.45, z: 0.82 };

            function syncSphericalFromEye(eye) {
              if (!eye) return;
              const x = typeof eye.x === "number" ? eye.x : -1.55;
              const y = typeof eye.y === "number" ? eye.y : -1.45;
              const z = typeof eye.z === "number" ? eye.z : 0.82;
              camDist = Math.max(0.6, Math.hypot(x, y, z));
              camTheta = Math.atan2(y, x);
              const rXY = Math.hypot(x, y);
              camPhi = Math.atan2(z, Math.max(1e-4, rXY));
            }

            function applyCameraEye() {
              const cosPhi = Math.cos(camPhi);
              const x = camDist * Math.cos(camTheta) * cosPhi;
              const y = camDist * Math.sin(camTheta) * cosPhi;
              const z = camDist * Math.sin(camPhi);
              currentEye = {
                x: Number(x.toFixed(3)),
                y: Number(y.toFixed(3)),
                z: Number(z.toFixed(3))
              };
              if (window.Plotly && dom.plot && dom.plot._fullLayout) {
                Plotly.relayout(dom.plot, {
                  'scene.camera.eye': currentEye,
                  'scene.camera.up': { x: 0, y: 0, z: 1 }
                });
              }
            }

            const procCanvas = document.createElement("canvas");
            procCanvas.width = 160;
            procCanvas.height = 120;
            const procCtx = procCanvas.getContext("2d", { willReadFrequently: true });
            const dispCtx = dom.camCanvas ? dom.camCanvas.getContext("2d") : null;

            async function startWebcamTracking() {
              if (camActive) return;
              try {
                if (dom.camStatusMsg) dom.camStatusMsg.textContent = "⌛ Запуск камеры...";
                const stream = await navigator.mediaDevices.getUserMedia({
                  video: { width: { ideal: 320 }, height: { ideal: 240 }, facingMode: "user" },
                  audio: false
                });
                camStream = stream;
                dom.camVideo.srcObject = stream;
                await dom.camVideo.play();
                camActive = true;
                if (dom.camBtn) {
                  dom.camBtn.classList.add("active");
                  dom.camBtn.textContent = "🔴 Камера: АКТИВНА";
                }
                if (dom.camPip) dom.camPip.style.display = "block";
                if (dom.camStatusMsg) dom.camStatusMsg.textContent = "👋 Помашите рукой перед камерой";

                if (dom.plot && dom.plot.layout && dom.plot.layout.scene && dom.plot.layout.scene.camera) {
                  syncSphericalFromEye(dom.plot.layout.scene.camera.eye);
                }
                prevFrameData = null;
                startCamLoop();
              } catch (err) {
                console.error("Camera access error:", err);
                if (dom.camStatusMsg) dom.camStatusMsg.textContent = "⚠️ Доступ к камере отклонен";
                if (dom.status) dom.status.textContent = "⚠️ Доступ к веб-камере отклонен в браузере. Разрешите камеру в настройках сайта.";
                stopWebcamTracking();
              }
            }

            function stopWebcamTracking() {
              camActive = false;
              if (camRaf) {
                cancelAnimationFrame(camRaf);
                camRaf = null;
              }
              if (camStream) {
                camStream.getTracks().forEach(t => t.stop());
                camStream = null;
              }
              if (dom.camVideo) dom.camVideo.srcObject = null;
              if (dom.camBtn) {
                dom.camBtn.classList.remove("active");
                dom.camBtn.textContent = "📷 Управление камерой";
              }
              if (dom.camPip) dom.camPip.style.display = "none";
            }

            function toggleWebcam(forceState) {
              const shouldOpen = typeof forceState === "boolean" ? forceState : !camActive;
              if (shouldOpen) startWebcamTracking();
              else stopWebcamTracking();
            }

            function resetCameraHome() {
              camDist = 2.27;
              camTheta = -2.39;
              camPhi = 0.38;
              angVelTheta = 0;
              angVelPhi = 0;
              applyCameraEye();
              if (dom.camStatusMsg) dom.camStatusMsg.textContent = "🎯 Ракурс сброшен в Home View";
            }

            function freezeCamera() {
              angVelTheta = 0;
              angVelPhi = 0;
              if (dom.camStatusMsg) dom.camStatusMsg.textContent = "✋ Вращение остановлено";
            }

            function takeSnapshot() {
              if (window.Plotly && dom.plot) {
                const fname = "desmos3d_" + (state.formula || "surface").replace(/[^a-zA-Z0-9]/g, "_");
                Plotly.downloadImage(dom.plot, {
                  format: "png",
                  width: 1600,
                  height: 1000,
                  filename: fname,
                });
                if (dom.camStatusMsg) dom.camStatusMsg.textContent = "📸 Снимок 3D графика сохранен (PNG)!";
              }
            }

            function zoomCamera(delta) {
              camDist = Math.max(0.8, Math.min(6.0, camDist * delta));
              applyCameraEye();
              if (dom.camStatusMsg) dom.camStatusMsg.textContent = `🔍 Дистанция: ${camDist.toFixed(2)}`;
            }

            if (dom.camBtn) dom.camBtn.addEventListener("click", () => toggleWebcam());
            if (dom.camCloseBtn) dom.camCloseBtn.addEventListener("click", () => stopWebcamTracking());
            if (dom.camResetBtn) dom.camResetBtn.addEventListener("click", resetCameraHome);
            if (dom.camFreezeBtn) dom.camFreezeBtn.addEventListener("click", freezeCamera);
            if (dom.camSnapBtn) dom.camSnapBtn.addEventListener("click", takeSnapshot);
            if (dom.camZoomIn) dom.camZoomIn.addEventListener("click", () => zoomCamera(0.85));
            if (dom.camZoomOut) dom.camZoomOut.addEventListener("click", () => zoomCamera(1.18));

            if (dom.camSpeed) {
              dom.camSpeed.addEventListener("input", () => {
                const val = parseFloat(dom.camSpeed.value) || 0.7;
                let desc = "Плавный";
                if (val > 1.2) desc = "Быстрый";
                else if (val > 0.8) desc = "Средний";
                if (dom.camSpeedVal) dom.camSpeedVal.textContent = `${val.toFixed(1)}x (${desc})`;
              });
            }

            // Перетаскивание окна PIP
            let isDraggingPip = false;
            let pipOffset = { x: 0, y: 0 };
            if (dom.camHeader) {
              dom.camHeader.addEventListener("pointerdown", (e) => {
                if (e.target.tagName === "BUTTON" || e.target.closest("button")) return;
                isDraggingPip = true;
                const rect = dom.camPip.getBoundingClientRect();
                pipOffset.x = e.clientX - rect.left;
                pipOffset.y = e.clientY - rect.top;
                dom.camHeader.setPointerCapture(e.pointerId);
              });
              dom.camHeader.addEventListener("pointermove", (e) => {
                if (!isDraggingPip) return;
                const parentRect = dom.plotWrap.getBoundingClientRect();
                let newLeft = e.clientX - parentRect.left - pipOffset.x;
                let newTop = e.clientY - parentRect.top - pipOffset.y;
                newLeft = Math.max(0, Math.min(parentRect.width - dom.camPip.offsetWidth, newLeft));
                newTop = Math.max(0, Math.min(parentRect.height - dom.camPip.offsetHeight, newTop));
                dom.camPip.style.left = newLeft + "px";
                dom.camPip.style.top = newTop + "px";
                dom.camPip.style.right = "auto";
                dom.camPip.style.bottom = "auto";
              });
              dom.camHeader.addEventListener("pointerup", (e) => {
                isDraggingPip = false;
                try { dom.camHeader.releasePointerCapture(e.pointerId); } catch (err) {}
              });
            }

            let isPipMinimized = false;
            if (dom.camMinBtn) {
              dom.camMinBtn.addEventListener("click", () => {
                isPipMinimized = !isPipMinimized;
                if (dom.camContent) dom.camContent.style.display = isPipMinimized ? "none" : "block";
                dom.camMinBtn.textContent = isPipMinimized ? "+" : "−";
              });
            }

            function startCamLoop() {
              function camStep() {
                if (!camActive) return;
                if (dom.camVideo && dom.camVideo.readyState >= 2) {
                  // 1. Зеркальный кадр в procCanvas (160x120)
                  procCtx.save();
                  procCtx.scale(-1, 1);
                  procCtx.drawImage(dom.camVideo, -160, 0, 160, 120);
                  procCtx.restore();

                  const frame = procCtx.getImageData(0, 0, 160, 120);
                  const d = frame.data;

                  let sumX = 0, sumY = 0, totalMotion = 0;
                  let minX = 160, maxX = 0, minY = 120, maxY = 0;

                  if (prevFrameData) {
                    for (let y = 6; y < 114; y += 2) {
                      for (let x = 6; x < 154; x += 2) {
                        const idx = (y * 160 + x) * 4;
                        const r = d[idx], g = d[idx + 1], b = d[idx + 2];
                        const pr = prevFrameData[idx], pg = prevFrameData[idx + 1], pb = prevFrameData[idx + 2];
                        const diff = Math.abs(r - pr) + Math.abs(g - pg) + Math.abs(b - pb);
                        // Оптимальный порог: 34 для четкого захвата движения любой ладони в веб-камере
                        if (diff > 34) {
                          const isSkin = (r > 60 && g > 40 && b > 20 && r > g && (r - g) > 10);
                          const w = isSkin ? diff * 2.0 : diff;
                          sumX += x * w;
                          sumY += y * w;
                          totalMotion += w;
                          if (x < minX) minX = x;
                          if (x > maxX) maxX = x;
                          if (y < minY) minY = y;
                          if (y > maxY) maxY = y;
                        }
                      }
                    }
                  } else {
                    prevFrameData = new Uint8ClampedArray(d.length);
                  }
                  prevFrameData.set(d);

                  // Легкий и надежный триггер: 1700 (срабатывает сразу при взмахе)
                  const motionDetected = totalMotion > 1700;
                  const camSensitivity = dom.camSpeed ? (parseFloat(dom.camSpeed.value) || 1.1) : 1.1;
                  const mode = dom.camMode ? dom.camMode.value : "swipe";
                  const target = dom.camTarget ? dom.camTarget.value : "orbit";
                  const filterMode = dom.camFilter ? dom.camFilter.value : "neon";

                  // Обновление шкалы энергии движения
                  if (dom.camMeterBar) {
                    const meterPct = Math.min(100, Math.round((totalMotion / 7000) * 100));
                    dom.camMeterBar.style.width = meterPct + "%";
                  }

                  let deltaX = 0, deltaY = 0;
                  let normX = 0, normY = 0;

                  if (motionDetected) {
                    const rawX = sumX / totalMotion;
                    const rawY = sumY / totalMotion;
                    // Сбалансированное сглаживание: 68% фильтра + 32% мгновенной реакции (быстро следует за рукой, без резких скачков)
                    smoothCentroidX = smoothCentroidX * 0.68 + rawX * 0.32;
                    smoothCentroidY = smoothCentroidY * 0.68 + rawY * 0.32;

                    deltaX = smoothCentroidX - lastCentroidX;
                    deltaY = smoothCentroidY - lastCentroidY;
                    lastCentroidX = smoothCentroidX;
                    lastCentroidY = smoothCentroidY;

                    normX = (smoothCentroidX - 80) / 80;
                    normY = (smoothCentroidY - 60) / 60;

                    // Оптический зум (приближение ладони)
                    const boxArea = (maxX - minX) * (maxY - minY);
                    if (boxArea > 9500 && target === "orbit") {
                      camDist = Math.max(0.8, camDist - 0.007 * camSensitivity);
                    } else if (boxArea > 0 && boxArea < 2000 && target === "orbit") {
                      camDist = Math.min(5.5, camDist + 0.007 * camSensitivity);
                    }

                    if (target === "orbit") {
                      if (mode === "swipe") {
                        // Чуткий свайп: легко раскручивает и плавно скользит
                        if (Math.abs(deltaX) > 0.7) {
                          const impulse = -deltaX * 0.0024 * camSensitivity;
                          angVelTheta = Math.max(-0.055, Math.min(0.055, angVelTheta + impulse));
                        }
                        if (Math.abs(deltaY) > 0.7) {
                          const impulse = -deltaY * 0.0018 * camSensitivity;
                          angVelPhi = Math.max(-0.045, Math.min(0.045, angVelPhi + impulse));
                        }
                      } else if (mode === "joystick") {
                        // Комфортная мертвая зона (0.20) и прямая плавная скорость
                        const deadzone = 0.20;
                        if (normX > deadzone) {
                          const p = (normX - deadzone) / (1 - deadzone);
                          angVelTheta = -p * 0.028 * camSensitivity;
                        } else if (normX < -deadzone) {
                          const p = (-normX - deadzone) / (1 - deadzone);
                          angVelTheta = p * 0.028 * camSensitivity;
                        } else {
                          angVelTheta = 0;
                        }

                        if (normY > deadzone) {
                          const p = (normY - deadzone) / (1 - deadzone);
                          angVelPhi = -p * 0.022 * camSensitivity;
                        } else if (normY < -deadzone) {
                          const p = (-normY - deadzone) / (1 - deadzone);
                          angVelPhi = p * 0.022 * camSensitivity;
                        } else {
                          angVelPhi = 0;
                        }
                      } else if (mode === "direct") {
                        const targetTheta = -normX * (Math.PI * 0.95);
                        const targetPhi = -normY * 1.0;
                        camTheta = camTheta * 0.82 + targetTheta * 0.18;
                        camPhi = camPhi * 0.82 + targetPhi * 0.18;
                      }
                    } else if (target === "point") {
                      // Воздушная указка (Air Pointer): плавное кинематографическое наведение точки a=(a1, a2)
                      const x1Min = state.x1_range ? state.x1_range[0] : -1.8;
                      const x1Max = state.x1_range ? state.x1_range[1] : 1.8;
                      const x2Min = state.x2_range ? state.x2_range[0] : -1.8;
                      const x2Max = state.x2_range ? state.x2_range[1] : 1.8;
                      const tA1 = x1Min + (normX + 1) * 0.5 * (x1Max - x1Min);
                      const tA2 = x2Min + (1 - (normY + 1) * 0.5) * (x2Max - x2Min);
                      const nA1 = Number((state.a1 * 0.88 + tA1 * 0.12).toFixed(2));
                      const nA2 = Number((state.a2 * 0.88 + tA2 * 0.12).toFixed(2));
                      if (Math.abs(nA1 - state.a1) >= 0.01 || Math.abs(nA2 - state.a2) >= 0.01) {
                        state.a1 = nA1;
                        state.a2 = nA2;
                        syncSliderThumbsOnly();
                        renderPlot();
                      }
                    } else if (target === "slice_c") {
                      // Управление высотой среза y = c рукой (плавно и без дерганий)
                      const cMin = parseFloat(dom.slC.min) || -2.5;
                      const cMax = parseFloat(dom.slC.max) || 2.5;
                      const tC = cMin + (1 - (normY + 1) * 0.5) * (cMax - cMin);
                      const nC = Number((state.c_val * 0.88 + tC * 0.12).toFixed(2));
                      if (Math.abs(nC - state.c_val) >= 0.01) {
                        state.c_val = nC;
                        state.show_level_plane = true;
                        syncSliderThumbsOnly();
                        renderPlot();
                      }
                    }
                  } else {
                    lastCentroidX = smoothCentroidX;
                    lastCentroidY = smoothCentroidY;
                    if (mode === "joystick") {
                      angVelTheta = 0;
                      angVelPhi = 0;
                    }
                  }

                  if (target === "orbit") {
                    if (mode === "swipe") {
                      camTheta += angVelTheta;
                      camPhi += angVelPhi;
                      // Сбалансированное трение: мягкое вращение с естественным затуханием
                      angVelTheta *= 0.86;
                      angVelPhi *= 0.86;
                      if (Math.abs(angVelTheta) < 1e-4) angVelTheta = 0;
                      if (Math.abs(angVelPhi) < 1e-4) angVelPhi = 0;
                    } else if (mode === "joystick") {
                      camTheta += angVelTheta;
                      camPhi += angVelPhi;
                    }
                    camPhi = Math.max(-1.38, Math.min(1.38, camPhi));

                    if (Math.abs(angVelTheta) > 1e-4 || Math.abs(angVelPhi) > 1e-4 || mode === "direct") {
                      applyCameraEye();
                    }
                  }

                  // 2. Отображение HUD на экране (250x165) с выбранным стилем
                  if (!isPipMinimized && dispCtx) {
                    dispCtx.save();
                    dispCtx.scale(-1, 1);
                    if (filterMode === "neon") {
                      dispCtx.filter = "contrast(190%) brightness(110%) hue-rotate(170deg) saturate(180%)";
                    } else if (filterMode === "thermal") {
                      dispCtx.filter = "contrast(220%) invert(100%) saturate(300%) hue-rotate(90deg)";
                    } else {
                      dispCtx.filter = "none";
                    }
                    dispCtx.drawImage(dom.camVideo, -250, 0, 250, 165);
                    dispCtx.restore();

                    // Тёмное неоновое стекло
                    dispCtx.fillStyle = "rgba(15, 23, 42, 0.22)";
                    dispCtx.fillRect(0, 0, 250, 165);

                    // Центр
                    dispCtx.strokeStyle = "rgba(56, 189, 248, 0.35)";
                    dispCtx.lineWidth = 1;
                    dispCtx.beginPath();
                    dispCtx.moveTo(125, 74); dispCtx.lineTo(125, 90);
                    dispCtx.moveTo(117, 82); dispCtx.lineTo(133, 82);
                    dispCtx.stroke();

                    if (mode === "joystick" && target === "orbit") {
                      dispCtx.strokeStyle = "rgba(255, 255, 255, 0.22)";
                      dispCtx.setLineDash([3, 3]);
                      dispCtx.strokeRect(100, 62, 50, 40);
                      dispCtx.setLineDash([]);
                    }

                    if (motionDetected) {
                      const hx = smoothCentroidX * (250 / 160);
                      const hy = smoothCentroidY * (165 / 120);

                      dispCtx.save();
                      // Голографическое прицельное кольцо
                      dispCtx.beginPath();
                      dispCtx.arc(hx, hy, 18, 0, 2 * Math.PI);
                      dispCtx.strokeStyle = target === "point" ? "#ec4899" : target === "slice_c" ? "#f59e0b" : "#00f5d4";
                      dispCtx.lineWidth = 2.5;
                      dispCtx.shadowColor = dispCtx.strokeStyle;
                      dispCtx.shadowBlur = 9;
                      dispCtx.stroke();

                      // Точка в центре
                      dispCtx.beginPath();
                      dispCtx.arc(hx, hy, 3.5, 0, 2 * Math.PI);
                      dispCtx.fillStyle = "#ffffff";
                      dispCtx.fill();

                      // Векторная стрелка
                      if (Math.abs(deltaX) > 0.6 || Math.abs(deltaY) > 0.6) {
                        dispCtx.beginPath();
                        dispCtx.moveTo(hx, hy);
                        dispCtx.lineTo(hx - deltaX * 3.5, hy + deltaY * 3.5);
                        dispCtx.strokeStyle = "#38bdf8";
                        dispCtx.lineWidth = 2.5;
                        dispCtx.stroke();
                      }
                      dispCtx.restore();

                      let dirText = "Нейтраль";
                      if (target === "point") {
                        dirText = `📍 Air-указка: a(${state.a1.toFixed(2)}, ${state.a2.toFixed(2)})`;
                      } else if (target === "slice_c") {
                        dirText = `↕️ Срез y = c (${state.c_val.toFixed(2)})`;
                      } else {
                        if (Math.abs(angVelTheta) > 0.005) {
                          dirText = angVelTheta > 0 ? "Вращение влево ⬅️" : "Вращение вправо ➡️";
                        } else if (Math.abs(angVelPhi) > 0.004) {
                          dirText = angVelPhi > 0 ? "Наклон вверх ⬆️" : "Наклон вниз ⬇️";
                        } else if (mode === "direct") {
                          dirText = "1:1 Слежение 🎯";
                        }
                      }
                      if (dom.camStatusMsg) dom.camStatusMsg.textContent = `⌖ ${dirText}`;
                    } else {
                      if (dom.camStatusMsg) dom.camStatusMsg.textContent = "👋 Помашите рукой перед камерой";
                    }
                  }
                }
                camRaf = requestAnimationFrame(camStep);
              }
              camRaf = requestAnimationFrame(camStep);
            }

            // =====================================================================
            // ВЫСОКОСКОРОСТНОЙ РЕНДЕР 3D И 2D СЦЕНЫ PLOTLY (60 FPS MESH-CACHED ENGINE)
            // =====================================================================
            let plotInitialized = false;
            let cachedMesh = null;
            let cachedMeshKey = "";

            function renderPlot() {
              loadPlotly().then((Plotly) => {
                const fn = compileMathFn(state.formula || "x1^2 - x2^2");
                const uFn = compileMathFn(state.vector_u || "-x2");
                const vFn = compileMathFn(state.vector_v || "x1");

                const x1Min = state.x1_range ? Number(state.x1_range[0]) : -1.8;
                const x1Max = state.x1_range ? Number(state.x1_range[1]) : 1.8;
                const x2Min = state.x2_range ? Number(state.x2_range[0]) : -1.8;
                const x2Max = state.x2_range ? Number(state.x2_range[1]) : 1.8;

                const a1 = Number(state.a1 || 0);
                const a2 = Number(state.a2 || 0);
                const cVal = Number(state.c_val || 0);
                const extraVal = Number(state.extra_val || 0.9);

                const cx = 0.5 * (x1Min + x1Max);
                const cy = 0.5 * (x2Min + x2Max);
                const rx = Math.max(0.2, 0.5 * (x1Max - x1Min));
                const ry = Math.max(0.2, 0.5 * (x2Max - x2Min));

                const currentKey = `${state.formula || ""}|${x1Min}|${x1Max}|${x2Min}|${x2Max}|${!!state.circular_domain}|${!!state.split_2d}`;
                let X1, X2, Z, zMin, zMax, zSpan;
                let rimX1 = [], rimX2 = [], rimZ = [];
                let x1Lin = [], x2Lin = [], zGrid2d = [];
                const N = 45;

                if (cachedMesh && cachedMeshKey === currentKey) {
                  X1 = cachedMesh.X1;
                  X2 = cachedMesh.X2;
                  Z = cachedMesh.Z;
                  zMin = cachedMesh.zMin;
                  zMax = cachedMesh.zMax;
                  zSpan = cachedMesh.zSpan;
                  rimX1 = cachedMesh.rimX1;
                  rimX2 = cachedMesh.rimX2;
                  rimZ = cachedMesh.rimZ;
                  x1Lin = cachedMesh.x1Lin;
                  x2Lin = cachedMesh.x2Lin;
                  zGrid2d = cachedMesh.zGrid2d;
                } else {
                  X1 = [];
                  X2 = [];
                  Z = [];
                  zMin = Infinity;
                  zMax = -Infinity;
                  const maxCoord = Math.max(2.0, Math.abs(x1Min), Math.abs(x1Max), Math.abs(x2Min), Math.abs(x2Max));
                  const zCap = Math.max(40, 2.5 * maxCoord * maxCoord * maxCoord);

                  for (let i = 0; i < N; i++) {
                    const v = -1 + (2 * i) / (N - 1);
                    const rowX1 = [];
                    const rowX2 = [];
                    const rowZ = [];
                    for (let j = 0; j < N; j++) {
                      const u = -1 + (2 * j) / (N - 1);
                      let x1, x2;
                      if (state.circular_domain) {
                        x1 = cx + rx * u * Math.sqrt(Math.max(0, 1 - 0.5 * v * v));
                        x2 = cy + ry * v * Math.sqrt(Math.max(0, 1 - 0.5 * u * u));
                      } else {
                        x1 = cx + rx * u;
                        x2 = cy + ry * v;
                      }
                      let z = fn(x1, x2);
                      if (!isFinite(z)) z = 0;
                      z = Math.max(-zCap, Math.min(zCap, z));
                      if (z < zMin) zMin = z;
                      if (z > zMax) zMax = z;
                      rowX1.push(x1);
                      rowX2.push(x2);
                      rowZ.push(z);
                    }
                    X1.push(rowX1);
                    X2.push(rowX2);
                    Z.push(rowZ);
                  }
                  if (!isFinite(zMin) || Math.abs(zMax - zMin) < 1e-4) {
                    zMin = -2.0;
                    zMax = 2.0;
                  }
                  zSpan = zMax - zMin;

                  // Предрасчет круглой кромки (Lecture 14 rim)
                  const rimPts = 120;
                  for (let k = 0; k <= rimPts; k++) {
                    const th = (2 * Math.PI * k) / rimPts;
                    let rx1, rx2;
                    if (state.circular_domain) {
                      rx1 = cx + rx * Math.cos(th);
                      rx2 = cy + ry * Math.sin(th);
                    } else {
                      const cosTh = Math.cos(th), sinTh = Math.sin(th);
                      const scale = 1 / Math.max(Math.abs(cosTh), Math.abs(sinTh));
                      rx1 = cx + rx * cosTh * scale;
                      rx2 = cy + ry * sinTh * scale;
                    }
                    rimX1.push(rx1);
                    rimX2.push(rx2);
                    rimZ.push(fn(rx1, rx2));
                  }

                  // Предрасчет сетки 2D контура
                  if (state.split_2d) {
                    for (let i = 0; i < N; i++) {
                      x1Lin.push(x1Min + ((x1Max - x1Min) * i) / (N - 1));
                      x2Lin.push(x2Min + ((x2Max - x2Min) * i) / (N - 1));
                    }
                    for (let i = 0; i < N; i++) {
                      const rZ = [];
                      for (let j = 0; j < N; j++) rZ.push(fn(x1Lin[j], x2Lin[i]));
                      zGrid2d.push(rZ);
                    }
                  }

                  cachedMeshKey = currentKey;
                  cachedMesh = { X1, X2, Z, zMin, zMax, zSpan, rimX1, rimX2, rimZ, x1Lin, x2Lin, zGrid2d };
                }
                const zPad = 0.22 * zSpan;
                const zFloor = state.show_level_plane ? cVal : zMin - 0.1 * zSpan;

                // Обновляем границы ползунка c под реальный диапазон поверхности
                dom.slC.min = (zMin - 0.15 * zSpan).toFixed(2);
                dom.slC.max = (zMax + 0.15 * zSpan).toFixed(2);

                // Значение функции и градиент в точке a = (a1, a2)
                const fa = fn(a1, a2);
                const eps = 1e-4;
                const df1 = (fn(a1 + eps, a2) - fn(a1 - eps, a2)) / (2 * eps);
                const df2 = (fn(a1, a2 + eps) - fn(a1, a2 - eps)) / (2 * eps);
                const gradNorm = Math.hypot(df1, df2);

                const traces = [];
                const is2D = !!state.split_2d;

                // Главная 3D поверхность в стиле BS101 Lecture 14
                traces.push({
                  type: "surface",
                  x: X1,
                  y: X2,
                  z: Z,
                  colorscale: [
                    [0.0, "#dcebfa"],
                    [0.35, "#b9d8f7"],
                    [0.7, "#94c3f3"],
                    [1.0, "#72aee6"],
                  ],
                  showscale: false,
                  opacity: state.show_riemann ? 0.52 : 0.88,
                  lighting: { ambient: 0.84, diffuse: 0.35, specular: 0.08, roughness: 0.85 },
                  contours: {
                    x: { show: true, color: "rgba(55, 95, 145, 0.25)", width: 1 },
                    y: { show: true, color: "rgba(55, 95, 145, 0.25)", width: 1 },
                    z: { show: true, color: "rgba(55, 95, 145, 0.20)", width: 1 },
                  },
                  hoverinfo: "x+y+z",
                  name: "y = f(x)",
                });

                // Темно-синяя круглая кромка поверхности (Lecture 14 rim - из кэша)
                if (state.circular_domain && rimX1 && rimX1.length > 0) {
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: rimX1, y: rimX2, z: rimZ,
                    line: { color: "#1d3b6c", width: 5 },
                    showlegend: false,
                    hoverinfo: "skip",
                  });
                }

                // Стрелки координатных осей в стиле учебника
                const x1AxMin = Math.min(0, x1Min) - 0.14 * (x1Max - x1Min);
                const x1AxMax = Math.max(0, x1Max) + 0.14 * (x1Max - x1Min);
                const x2AxMin = Math.min(0, x2Min) - 0.14 * (x2Max - x2Min);
                const x2AxMax = Math.max(0, x2Max) + 0.14 * (x2Max - x2Min);
                const zTop = Math.max(zMax + zPad, cVal + 0.4);
                const zBot = Math.min(zMin - 0.1 * zSpan, cVal - 0.2, -0.3);

                traces.push({
                  type: "scatter3d",
                  mode: "lines",
                  x: [x1AxMin, x1AxMax, null, 0, 0, null, 0, 0],
                  y: [0, 0, null, x2AxMin, x2AxMax, null, 0, 0],
                  z: [zFloor, zFloor, null, zFloor, zFloor, null, zBot, zTop],
                  line: { color: "#111827", width: 4 },
                  showlegend: false,
                  hoverinfo: "skip",
                });

                // L1: СЕЧЕНИЕ y = c И ЛИНИЯ УРОВНЯ f(x1, x2) = c
                if (state.show_level_plane) {
                  traces.push({
                    type: "surface",
                    x: [[x1Min, x1Max], [x1Min, x1Max]],
                    y: [[x2Min, x2Min], [x2Max, x2Max]],
                    z: [[cVal, cVal], [cVal, cVal]],
                    colorscale: [[0, "rgba(148,163,184,0.22)"], [1, "rgba(148,163,184,0.22)"]],
                    showscale: false,
                    opacity: 0.25,
                    hoverinfo: "skip",
                  });
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: [x1Min, x1Max, x1Max, x1Min, x1Min],
                    y: [x2Min, x2Min, x2Max, x2Max, x2Min],
                    z: [cVal, cVal, cVal, cVal, cVal],
                    line: { color: "#94a3b8", width: 3 },
                    showlegend: false,
                    hoverinfo: "skip",
                  });

                  // Извлечение кривой уровня f(x1, x2) = c методом линейной интерполяции ребер
                  const lvX = [], lvY = [], lvZ = [];
                  for (let i = 0; i < N; i++) {
                    for (let j = 0; j < N - 1; j++) {
                      const d1 = Z[i][j] - cVal;
                      const d2 = Z[i][j + 1] - cVal;
                      if (d1 * d2 <= 0 && Math.abs(d1 - d2) > 1e-9) {
                        const t = d1 / (d1 - d2);
                        lvX.push(X1[i][j] + t * (X1[i][j + 1] - X1[i][j]));
                        lvY.push(X2[i][j] + t * (X2[i][j + 1] - X2[i][j]));
                        lvZ.push(cVal);
                      }
                    }
                  }
                  if (lvX.length > 0) {
                    traces.push({
                      type: "scatter3d",
                      mode: "markers",
                      x: lvX, y: lvY, z: lvZ,
                      marker: { color: "#a84339", size: 3.5 },
                      showlegend: false,
                      name: "f(x)=c",
                    });
                  }
                }

                // L2: ВЕРТИКАЛЬНЫЕ СРЕЗЫ x1 = a1 И x2 = a2
                if (state.show_xy_traces) {
                  const sSteps = 80;
                  const tr1X = [], tr1Y = [], tr1Z = [];
                  const tr2X = [], tr2Y = [], tr2Z = [];
                  for (let k = 0; k <= sSteps; k++) {
                    const s1 = x1Min + ((x1Max - x1Min) * k) / sSteps;
                    const s2 = x2Min + ((x2Max - x2Min) * k) / sSteps;
                    tr1X.push(a1); tr1Y.push(s2); tr1Z.push(fn(a1, s2));
                    tr2X.push(s1); tr2Y.push(a2); tr2Z.push(fn(s1, a2));
                  }
                  // Полупрозрачная секущая плоскость x2 = a2
                  traces.push({
                    type: "surface",
                    x: [[x1Min, x1Max], [x1Min, x1Max]],
                    y: [[a2, a2], [a2, a2]],
                    z: [[zMin, zMin], [zMax, zMax]],
                    colorscale: [[0, "rgba(234,88,12,0.16)"], [1, "rgba(234,88,12,0.16)"]],
                    showscale: false,
                    opacity: 0.22,
                    hoverinfo: "skip",
                  });
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: tr1X, y: tr1Y, z: tr1Z,
                    line: { color: "#2563eb", width: 6 },
                    name: "Срез x₁ = a₁",
                  });
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: tr2X, y: tr2Y, z: tr2Z,
                    line: { color: "#ea580c", width: 6 },
                    name: "Срез x₂ = a₂",
                  });
                }

                // L3: КАСАТЕЛЬНАЯ ПЛОСКОСТЬ, НОРМАЛЬ И ГРАДИЕНТ ∇f(a)
                if (state.show_tangent) {
                  const span = 0.32 * rx;
                  const tpX = [[a1 - span, a1 + span], [a1 - span, a1 + span]];
                  const tpY = [[a2 - span, a2 - span], [a2 + span, a2 + span]];
                  const tpZ = [
                    [fa + df1 * (-span) + df2 * (-span), fa + df1 * span + df2 * (-span)],
                    [fa + df1 * (-span) + df2 * span, fa + df1 * span + df2 * span],
                  ];
                  traces.push({
                    type: "surface",
                    x: tpX, y: tpY, z: tpZ,
                    colorscale: [[0, "#10b981"], [1, "#059669"]],
                    opacity: 0.62,
                    showscale: false,
                    name: "Касательная плоскость",
                  });
                  if (gradNorm > 1e-5) {
                    const gScale = Math.min(0.85, 0.5 / (gradNorm + 0.35));
                    const gx = a1 + df1 * gScale;
                    const gy = a2 + df2 * gScale;
                    traces.push({
                      type: "scatter3d",
                      mode: "lines+markers",
                      x: [a1, gx], y: [a2, gy], z: [zFloor, zFloor],
                      line: { color: "#7c3aed", width: 6 },
                      marker: { size: [3, 6], color: "#7c3aed" },
                      name: "∇f(a)",
                    });
                  }
                }

                // L4: ОТКРЫТАЯ ОКРЕСТНОСТЬ B_r(a) И ЕЕ ОБРАЗ НА ПОВЕРХНОСТИ
                if (state.show_ball) {
                  const rBall = Math.max(0.15, Math.min(2.5, extraVal));
                  const bX = [], bY = [], bZFloor = [], bZSurf = [];
                  const M = 80;
                  for (let k = 0; k <= M; k++) {
                    const th = (2 * Math.PI * k) / M;
                    const bx = a1 + rBall * Math.cos(th);
                    const by = a2 + rBall * Math.sin(th);
                    bX.push(bx);
                    bY.push(by);
                    bZFloor.push(zFloor);
                    bZSurf.push(fn(bx, by));
                  }
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: bX, y: bY, z: bZFloor,
                    line: { color: "#e11d48", width: 5, dash: "dash" },
                    name: "∂B_r(a)",
                  });
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: bX, y: bY, z: bZSurf,
                    line: { color: "#e11d48", width: 4 },
                    name: "f(∂B_r(a))",
                  });
                }

                // L5: 3D СУММЫ РИМАНА (ДВОЙНОЙ ИНТЕГРАЛ)
                let riemannSumVal = 0;
                if (state.show_riemann) {
                  const nR = Math.max(2, Math.min(15, Math.round(extraVal)));
                  const dx1 = (x1Max - x1Min) / nR;
                  const dx2 = (x2Max - x2Min) / nR;
                  const vx = [], vy = [], vz = [];
                  const ti = [], tj = [], tk = [];
                  let off = 0;
                  const tris = [
                    [0,1,2],[0,2,3],[4,5,6],[4,6,7],[0,1,5],[0,5,4],
                    [1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]
                  ];
                  for (let i = 0; i < nR; i++) {
                    const xm = x1Min + (i + 0.5) * dx1;
                    const x0 = x1Min + i * dx1 + 0.04 * dx1;
                    const x1b = x1Min + (i + 1) * dx1 - 0.04 * dx1;
                    for (let j = 0; j < nR; j++) {
                      const ym = x2Min + (j + 0.5) * dx2;
                      if (state.circular_domain && Math.hypot((xm - cx) / rx, (ym - cy) / ry) > 1.0) continue;
                      const y0 = x2Min + j * dx2 + 0.04 * dx2;
                      const y1b = x2Min + (j + 1) * dx2 - 0.04 * dx2;
                      const hz = fn(xm, ym);
                      riemannSumVal += hz * dx1 * dx2;
                      const pts = [
                        [x0,y0,0],[x1b,y0,0],[x1b,y1b,0],[x0,y1b,0],
                        [x0,y0,hz],[x1b,y0,hz],[x1b,y1b,hz],[x0,y1b,hz]
                      ];
                      for (const p of pts) { vx.push(p[0]); vy.push(p[1]); vz.push(p[2]); }
                      for (const t of tris) { ti.push(off + t[0]); tj.push(off + t[1]); tk.push(off + t[2]); }
                      off += 8;
                    }
                  }
                  if (vx.length > 0) {
                    traces.push({
                      type: "mesh3d",
                      x: vx, y: vy, z: vz,
                      i: ti, j: tj, k: tk,
                      intensity: vz,
                      colorscale: "Viridis",
                      opacity: 0.78,
                      showscale: false,
                      name: "Суммы Римана",
                    });
                  }
                }

                // L6: ВЕКТОРНОЕ ПОЛЕ И ЛИНИЯ ТОКА r(t)
                if (state.show_vector_field) {
                  const gN = 9;
                  const qX = [], qY = [], qZ = [];
                  for (let i = 0; i < gN; i++) {
                    const x = x1Min + ((x1Max - x1Min) * i) / (gN - 1);
                    for (let j = 0; j < gN; j++) {
                      const y = x2Min + ((x2Max - x2Min) * j) / (gN - 1);
                      const u = uFn(x, y);
                      const v = vFn(x, y);
                      const m = Math.hypot(u, v) + 1e-6;
                      const sc = 0.16 * rx * Math.min(1.5, m) / m;
                      qX.push(x, x + u * sc, null);
                      qY.push(y, y + v * sc, null);
                      qZ.push(zFloor, zFloor, null);
                    }
                  }
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: qX, y: qY, z: qZ,
                    line: { color: "rgba(37,99,235,0.65)", width: 3 },
                    showlegend: false,
                    hoverinfo: "skip",
                  });

                  // Интегрирование линии тока r(t) из точки a = (a1, a2)
                  const tMax = Math.max(0.4, Math.min(12.0, extraVal));
                  const steps = 110;
                  const dt = (tMax * 0.6) / steps;
                  let px = a1, py = a2;
                  const flX = [px], flY = [py], flZF = [zFloor], flZS = [fn(px, py)];
                  for (let s = 0; s < steps; s++) {
                    const u = uFn(px, py);
                    const v = vFn(px, py);
                    const n = Math.hypot(u, v) + 1e-6;
                    px += (u / Math.max(1, n * 0.45)) * dt;
                    py += (v / Math.max(1, n * 0.45)) * dt;
                    flX.push(px); flY.push(py);
                    flZF.push(zFloor); flZS.push(fn(px, py));
                  }
                  traces.push({
                    type: "scatter3d",
                    mode: "lines",
                    x: flX, y: flY, z: flZS,
                    line: { color: "#dc2626", width: 6 },
                    name: "r(t) на поверхности",
                  });
                }

                // Точка a = (a1, a2) на плоскости и (a1, a2, f(a)) на поверхности
                traces.push({
                  type: "scatter3d",
                  mode: "lines+markers+text",
                  x: [a1, a1],
                  y: [a2, a2],
                  z: [zFloor, fa],
                  line: { color: "#111827", width: 3, dash: "dash" },
                  marker: { size: [5, 6], color: ["#111827", "#b91c1c"] },
                  text: [`a(${a1.toFixed(2)}, ${a2.toFixed(2)})`, `f(a)=${fa.toFixed(2)}`],
                  textposition: ["bottom center", "top center"],
                  showlegend: false,
                });

                // 2D КАРТА ЛИНИЙ УРОВНЯ РЯДОМ (если включен чип 2D карта - из кэша)
                if (is2D) {
                  traces.push({
                    type: "contour",
                    x: x1Lin,
                    y: x2Lin,
                    z: zGrid2d,
                    xaxis: "x",
                    yaxis: "y",
                    colorscale: [
                      [0.0, "#eef6ff"],
                      [0.5, "#bae6fd"],
                      [1.0, "#7dd3fc"],
                    ],
                     showscale: false,
                    contours: { coloring: "fill", showlines: true },
                    line: { color: "rgba(30,58,138,0.3)", width: 1 },
                  });
                  traces.push({
                    type: "scatter",
                    mode: "markers+text",
                    x: [a1],
                    y: [a2],
                    xaxis: "x",
                    yaxis: "y",
                    marker: { size: 10, color: "#111827", line: { width: 2, color: "#fff" } },
                    text: [`a(${a1.toFixed(2)}, ${a2.toFixed(2)})`],
                    textposition: "top right",
                    showlegend: false,
                  });
                }

                const showBox = !!state.show_box_grid;
                const axStyle = {
                  visible: showBox,
                  showgrid: showBox,
                  showbackground: showBox,
                  zeroline: false,
                };

                const layout = {
                  template: "plotly_white",
                  paper_bgcolor: "#ffffff",
                  plot_bgcolor: "#ffffff",
                  margin: { l: 8, r: 8, t: 10, b: 8 },
                  showlegend: false,
                  uirevision: "keep_camera_view",
                  scene: {
                    domain: is2D ? { x: [0.0, 0.60], y: [0.0, 1.0] } : { x: [0.0, 1.0], y: [0.0, 1.0] },
                    xaxis: { ...axStyle, range: [x1AxMin, x1AxMax], title: "x¹" },
                    yaxis: { ...axStyle, range: [x2AxMin, x2AxMax], title: "x²" },
                    zaxis: { ...axStyle, range: [zBot - 0.1 * zSpan, zTop + 0.12 * zSpan], title: "y" },
                    aspectmode: "manual",
                    aspectratio: { x: 1.15, y: 1.15, z: 0.92 },
                    camera: { eye: currentEye, up: { x: 0, y: 0, z: 1 } },
                  },
                };

                if (is2D) {
                  layout.xaxis = {
                    domain: [0.65, 0.99],
                    range: [x1Min, x1Max],
                    title: "x¹",
                    gridcolor: "#e2e8f0",
                  };
                  layout.yaxis = {
                    domain: [0.08, 0.94],
                    range: [x2Min, x2Max],
                    title: "x²",
                    scaleanchor: "x",
                    scaleratio: 1,
                    gridcolor: "#e2e8f0",
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
                        state.a1 = pt.x;
                        state.a2 = pt.y;
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

                // Обновление нижней математической строки
                let riemannInfo = state.show_riemann
                  ? ` • <b>Сумма Римана:</b> ≈ ${riemannSumVal.toFixed(3)}`
                  : "";
                dom.mathBar.innerHTML = `
                  <div>
                    <b>Формула:</b> <code>y = ${state.formula || "x1^2 - x2^2"}</code> •
                    <b>Точка a:</b> (${a1.toFixed(2)}, ${a2.toFixed(2)}) •
                    <b>f(a):</b> ${fa.toFixed(3)} •
                    <b>Уровень c:</b> ${cVal.toFixed(2)} •
                    <b>Градиент ∇f(a):</b> (${df1.toFixed(2)}, ${df2.toFixed(2)}) (‖∇f‖ = ${gradNorm.toFixed(2)})${riemannInfo}
                  </div>
                  <div style="color:#64748b;font-size:11.5px;">
                    💡 Кликни по 3D/2D графику, чтобы перенести точку <b>a</b>, или скажи голосом команду
                  </div>
                `;
              });
            }

            syncControlsFromState(false);
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

            # 1. Выбран пресет
            if preset_id and preset_id in PRESET_STATES:
                next_st = dict(PRESET_STATES[preset_id])
                self.state_json = json.dumps(next_st, ensure_ascii=False)
                return

            if not cmd_text:
                return

            # 2. Сначала мгновенный локальный парсер (вставляет формулу, диапазон, координаты, слои и анимацию)
            next_st, handled = parse_and_apply_command(cmd_text, cur_st)

            # 3. Если нажата кнопка Gemini AI или локальный парсер не распознал нетривиальный запрос
            key = (self.api_key or env_key or "").strip()
            if use_ai or (not handled and key):
                ai_st, ai_ok, _ = ask_gemini_ai(cmd_text, key, next_st if handled else cur_st)
                if ai_ok:
                    next_st = ai_st
                    handled = True

            if not handled:
                next_st["status"] = (
                    f"💬 Не удалось распознать «{cmd_text}». Назовите формулу (напр. x1^3 - x2^2), срез, анимацию или нажмите 🤖 Gemini AI."
                )

            self.state_json = json.dumps(next_st, ensure_ascii=False)

    studio_widget = mo.ui.anywidget(
        DesmosMultivarStudio(
            initial_state=dict(PRESET_STATES["preset_lecture14"]),
            initial_key=env_key,
        )
    )
    studio_widget
    return (
        DesmosMultivarStudio,
        PRESET_STATES,
        ask_gemini_ai,
        clean_display_formula,
        env_key,
        is_valid_numpy_expr,
        math_to_numpy,
        normalize_spoken_math,
        parse_and_apply_command,
        studio_widget,
    )


if __name__ == "__main__":
    app.run()

