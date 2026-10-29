"""
Comprehensive Verification Suite for MultivarGrapher 3D (100% Marimo Edition)
=============================================================================
Tests:
1. Legacy backup verification (`legacy_backup/index.html`, `legacy_backup/styles.css`, `legacy_backup/app.js`).
2. Core mathematical, constraint, matrix, Hessian & AI engine (`calculus_engine.py`) across all 17 presets.
3. Marimo reactive notebook integrity (`marimo check app.py` & `custom.css`).
4. Exported Marimo HTML verification (`index.html` & `marimo_app.html`).
5. Live Marimo server startup & HTTP 200 health check (`python main.py --port 8765 --no-browser`).
6. CLI helper tools (`--deploy-help` & `--plot`).
"""

import subprocess
import sys
import time
import urllib.request
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent


def test_legacy_backup():
    print("1. Testing legacy HTML/JS/CSS backup files in legacy_backup/...")
    legacy_dir = BASE_DIR / "legacy_backup"
    assert legacy_dir.exists(), "legacy_backup/ directory does not exist!"

    html_file = legacy_dir / "index.html"
    css_file = legacy_dir / "styles.css"
    js_file = legacy_dir / "app.js"

    assert html_file.exists() and html_file.stat().st_size > 200000, "legacy_backup/index.html missing or incomplete!"
    assert css_file.exists() and css_file.stat().st_size > 500, "legacy_backup/styles.css missing or incomplete!"
    assert js_file.exists() and js_file.stat().st_size > 100000, "legacy_backup/app.js missing or incomplete!"
    print(
        f"   [OK] Legacy backup verified: index.html ({html_file.stat().st_size} B), "
        f"styles.css ({css_file.stat().st_size} B), app.js ({js_file.stat().st_size} B)"
    )


def test_calculus_engine():
    print("2. Testing calculus_engine.py (all 17 presets, 3D cylinders, R2/R3 matrices, Hessian, AI Tutor)...")
    import calculus_engine as ce

    assert len(ce.PRESETS) >= 17, f"Expected at least 17 presets, found {len(ce.PRESETS)}"

    for key, p in ce.PRESETS.items():
        calc = ce.analyze_calculus(
            raw_expr=p["f"],
            raw_constraint=p["constraint"],
            a1=p["a1"],
            a2=p["a2"],
            a3=p.get("a3", 0.0),
            level_c=p["c"],
            notation="x1x2",
        )
        assert "mode" in calc and "f_latex" in calc, f"Preset {key} failed calculus analysis!"
        fig = ce.build_plotly_figure(
            calc=calc,
            a1=p["a1"],
            a2=p["a2"],
            a3=p.get("a3", 0.0),
            level_c=p["c"],
            view_mode=p["view_mode"],
        )
        assert len(fig.data) > 0, f"Preset {key} produced an empty figure!"

    # Specifically verify free-variable 3D cylinder (F(x1,x2,x3) = [x1;x2;x3] with x1^2/4 + x2 = 1)
    cyl_calc = ce.analyze_calculus(
        raw_expr="[x1; x2; x3]",
        raw_constraint="x1^2/4 + x2 = 1",
        a1=0.0,
        a2=1.0,
        a3=0.0,
        level_c=1.0,
    )
    assert cyl_calc["constraint"]["active"] is True
    assert "x₃" in cyl_calc["constraint"]["free_vars"]
    assert len(cyl_calc["constraint"]["polylines"]) > 0
    print(f"   [OK] Free-variable 3D cylinder verified: {cyl_calc['constraint']['status_text']}")

    # Specifically verify R^3 3x3 matrix visualization
    mat3_calc = ce.analyze_calculus(
        raw_expr="[1, 2, 3; 4, 5, 6; 7, 8, 9]",
        a1=1.0,
        a2=1.0,
        a3=1.0,
        level_c=1.0,
    )
    assert mat3_calc["mode"] == "matrix_3d" and mat3_calc["dim"] == 3
    fig_mat3 = ce.build_plotly_figure(calc=mat3_calc, view_mode="3d")
    assert len(fig_mat3.data) >= 5
    print("   [OK] 3x3 Matrix in R^3 transformation & basis arrows verified!")

    # Verify animation frames (orbit, slice, glide)
    saddle_calc = ce.analyze_calculus(raw_expr="x1^2 - x2^2", a1=0.0, a2=0.0, level_c=0.0)
    assert saddle_calc["extremum_type"] == "saddle"
    for anim in ("orbit", "slice", "glide"):
        fig_anim = ce.build_plotly_figure(calc=saddle_calc, view_mode="3d", anim_mode=anim)
        assert len(fig_anim.frames) > 0, f"Animation mode {anim} produced 0 frames!"
    print("   [OK] Hessian saddle classification & 3D animation modes (orbit, slice, glide) verified!")

    # Verify AI Tutor auto-action extraction & code block stripping
    reply_md, action, model_label = ce.ask_ai_tutor(
        message="Create a parabolic cylinder with x1^2/4 + x2 = 1",
        calc=saddle_calc,
        a1=0.0,
        a2=0.0,
        a3=0.0,
    )
    assert "```graph_action" not in reply_md, "Raw graph_action block was not stripped from chat reply!"
    assert action is not None and action.get("constraint", "").replace(" ", "") == "x1^2/4+x2=1"
    print(f"   [OK] AI Calculus Tutor ({model_label}) action extraction & clean markdown verified!")


def test_marimo_check_and_exports():
    print("3. Testing Marimo app check (`marimo check app.py`) and exported HTML files...")
    app_path = BASE_DIR / "app.py"
    css_path = BASE_DIR / "custom.css"
    assert app_path.exists(), "app.py does not exist!"
    assert css_path.exists(), "custom.css does not exist!"

    res_check = subprocess.run(
        [sys.executable, "-m", "marimo", "check", "app.py"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res_check.returncode == 0, f"marimo check app.py failed: {res_check.stderr}"
    print("   [OK] `marimo check app.py` passed with 0 errors!")

    for html_name in ("index.html", "marimo_app.html"):
        p = BASE_DIR / html_name
        assert p.exists(), f"{html_name} does not exist!"
        text = p.read_text(encoding="utf-8")
        assert "<marimo-filename" in text, f"{html_name} is not a Marimo exported HTML file!"
        print(f"   [OK] {html_name} verified as standalone Marimo export ({p.stat().st_size} bytes)")


def test_marimo_live_server():
    print("4. Testing live Marimo server startup (`python main.py --port 8765 --no-browser`)...")
    test_port = 8765
    proc = subprocess.Popen(
        [sys.executable, "main.py", "--host", "127.0.0.1", "--port", str(test_port), "--no-browser"],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        url = f"http://127.0.0.1:{test_port}/"
        status_code = None
        for _ in range(25):
            time.sleep(0.5)
            try:
                with urllib.request.urlopen(url, timeout=2) as resp:
                    status_code = resp.status
                    body = resp.read(2000).decode("utf-8", errors="ignore")
                    if status_code == 200 and ("marimo" in body.lower() or "<!doctype html>" in body.lower()):
                        break
            except Exception:
                continue
        assert status_code == 200, f"Marimo server did not respond with HTTP 200 on {url}"
        print(f"   [OK] Live Marimo server responded HTTP 200 at {url}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()


def test_cli_helpers():
    print("5. Testing CLI helpers (--deploy-help and --plot)...")
    res_help = subprocess.run(
        [sys.executable, "main.py", "--deploy-help"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res_help.returncode == 0
    assert "MARIMO" in res_help.stdout.upper()

    res_plot = subprocess.run(
        [sys.executable, "main.py", "--plot", "--no-browser", "--formula", "x**2 + y**2", "--a", "1.0"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res_plot.returncode == 0
    plot_file = BASE_DIR / "multivar_plot.html"
    assert plot_file.exists()
    plot_file.unlink(missing_ok=True)
    print("   [OK] CLI helpers (--deploy-help & --plot) passed!")


if __name__ == "__main__":
    try:
        test_legacy_backup()
        test_calculus_engine()
        test_marimo_check_and_exports()
        test_marimo_live_server()
        test_cli_helpers()
        print("\n[SUCCESS] ALL MARIMO VERIFICATION TESTS PASSED!")
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"\n[ERROR] Test failed: {e}")
        sys.exit(1)
