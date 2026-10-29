"""
MultivarGrapher 3D - 100% Marimo Reactive Multivariable Calculus Suite
======================================================================

Features:
1. Powered natively by Marimo (https://github.com/marimo-team/marimo) in `app.py` & `calculus_engine.py`.
2. Full 2D Level Sets, 3D Surface, Split Dual View, Matrices in R^2 & R^3, Free-Variable 3D Cylinders,
   Total Derivative Matrix Df(a), Affine Plane g(x), Normal Line (90°), and Hessian Matrix H_f(a).
3. Built-in AI Calculus Tutor (Gemini 3.5 Flash-Lite + Offline Engine) with Auto Graph Actions.
4. Legacy HTML/JS/CSS preserved safely in `legacy_backup/`.

Usage:
    python main.py                  # Launch interactive Marimo web app locally
    python main.py --host 0.0.0.0   # Launch Marimo server on public/container interface (Render)
    python main.py --port 8080      # Launch Marimo server on custom port
    python main.py --marimo-edit    # Open Marimo reactive notebook editor (`marimo edit app.py`)
    python main.py --export-marimo  # Export standalone Marimo HTML (`index.html` & `marimo_app.html`)
    python main.py --plot           # Generate standalone 3D plot using Python/SymPy/Plotly
    python main.py --legacy-server  # (Optional) Run the backed-up legacy HTML/JS server from legacy_backup/
    python main.py --deploy-help    # View step-by-step Render and GitHub Pages guides
"""

import argparse
import os
import socket
import subprocess
import sys
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# Ensure utf-8 stdout on Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
LEGACY_DIR = BASE_DIR / "legacy_backup"


def find_available_port(start_port: int = 8000, max_attempts: int = 50) -> int:
    """Finds an unused TCP port starting from `start_port`."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return start_port


def run_marimo_app(
    port: int = 8000,
    host: str = "127.0.0.1",
    edit_mode: bool = False,
    open_browser: bool = True,
):
    """Launches the primary reactive Marimo application (`app.py`)."""
    env_port = os.environ.get("PORT")
    if env_port:
        actual_port = int(env_port)
    elif host == "127.0.0.1":
        actual_port = find_available_port(port)
    else:
        actual_port = port

    action = "edit" if edit_mode else "run"
    cmd = [
        sys.executable,
        "-m",
        "marimo",
        action,
        "app.py",
        "--port",
        str(actual_port),
        "--host",
        host,
    ]
    if not open_browser:
        cmd.append("--headless")
    if not edit_mode:
        cmd.append("--no-token")

    has_key = bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
    display_host = "localhost" if host == "0.0.0.0" else host

    print("=" * 76)
    print(" 🌌 MultivarGrapher 3D - 100% Marimo Reactive Calculus & Linear Algebra Suite")
    print("=" * 76)
    print(f" Engine              : Marimo Reactive App (app.py + calculus_engine.py)")
    print(f" Mode                : {'Interactive Editor (marimo edit)' if edit_mode else 'Production Web App (marimo run)'}")
    print(f" Listening interface : {host}:{actual_port}")
    print(f" App URL             : http://{display_host}:{actual_port}")
    print(
        f" Gemini Server Key   : {'🟢 Configured (gemini-3.5-flash-lite active)' if has_key else '⚡ Offline Math Engine Ready (or enter key in UI)'}"
    )
    print(f" Legacy Backup       : {LEGACY_DIR}")
    print("=" * 76)
    print(" Press Ctrl+C at any time to shut down the Marimo server.\n")

    try:
        subprocess.run(cmd, cwd=BASE_DIR)
    except KeyboardInterrupt:
        print("\n Shutting down Marimo server gracefully. Goodbye!")
        sys.exit(0)


def export_marimo_html(out_file: str = "marimo_app.html"):
    """Exports `app.py` to self-contained Marimo HTML snapshots (`marimo_app.html` & `index.html`)."""
    for target in [out_file, "index.html"]:
        cmd = [sys.executable, "-m", "marimo", "export", "html", "app.py", "-o", target, "-f"]
        print(f"📦 Exporting reactive Marimo application to {target}...")
        subprocess.run(cmd, cwd=BASE_DIR, check=True)
        print(f"✅ Exported successfully to {target}!")


def run_legacy_backup_server(port: int = 8000, host: str = "127.0.0.1", open_browser: bool = True):
    """Serves the backed-up legacy HTML/JS/CSS version from `legacy_backup/`."""
    actual_port = find_available_port(port) if host == "127.0.0.1" else port
    url = f"http://{host if host != '0.0.0.0' else 'localhost'}:{actual_port}/index.html"

    class LegacyHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(LEGACY_DIR), **kwargs)

    print(f"📦 Serving legacy backup from {LEGACY_DIR} at {url}")
    httpd = ThreadingHTTPServer((host, actual_port), LegacyHandler)
    if open_browser:
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


def plot_with_python(
    formula: str = "sin(sqrt(x**2 + y**2) * a) * b / (sqrt(x**2 + y**2) + 0.1)",
    a: float = 2.0,
    b: float = 1.0,
    x_min: float = -5.0,
    x_max: float = 5.0,
    y_min: float = -5.0,
    y_max: float = 5.0,
    points: int = 60,
    output_html: str = "multivar_plot.html",
    show_browser: bool = True,
):
    """
    Evaluates multivariable functions directly via Python (SymPy & NumPy)
    and produces an interactive 3D Plotly visualization.
    """
    import numpy as np
    import plotly.graph_objects as go
    import sympy as sp

    print(f"\n📊 Evaluating function in Python: z = f(x, y) = {formula}")
    x_sym, y_sym, a_sym, b_sym = sp.symbols("x y a b")
    clean_formula = formula.replace("^", "**")
    parsed_expr = sp.sympify(clean_formula)

    df_dx_sym = sp.diff(parsed_expr, x_sym)
    df_dy_sym = sp.diff(parsed_expr, y_sym)
    print(f" Symbolic ∂z/∂x: {df_dx_sym}")
    print(f" Symbolic ∂z/∂y: {df_dy_sym}")

    subbed_expr = parsed_expr.subs({a_sym: a, b_sym: b})
    f_lambdified = sp.lambdify((x_sym, y_sym), subbed_expr, modules=["numpy", "math"])

    x_vals = np.linspace(x_min, x_max, points)
    y_vals = np.linspace(y_min, y_max, points)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = f_lambdified(X, Y)
    if isinstance(Z, (int, float)):
        Z = np.full_like(X, float(Z))

    fig = go.Figure(
        data=[
            go.Surface(
                x=X,
                y=Y,
                z=Z,
                colorscale="Turbo",
                colorbar=dict(title="z"),
                contours=dict(z=dict(show=True, usecolormap=True, project=dict(z=True))),
            )
        ]
    )
    fig.update_layout(
        title=f"Multivariable Graph: z = {clean_formula} (a={a}, b={b})",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.3)),
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        template="plotly_dark",
    )

    out_path = BASE_DIR / output_html
    fig.write_html(str(out_path))
    print(f"✅ Interactive Plotly HTML generated at: {out_path}")

    if show_browser:
        webbrowser.open(out_path.as_uri())


def print_deploy_help():
    """Prints clear instructions for deploying the Marimo app to Render and GitHub Pages."""
    instructions = """
========================================================================
 🌟 DEPLOYMENT GUIDE: MARIMO ON RENDER (WITH GEMINI AI) & GITHUB PAGES
========================================================================

OPTION 1: DEPLOY REACTIVE MARIMO APP ON RENDER
-------------------------------------------------------
Deploying to Render runs the live reactive Marimo Python server (`app.py`)
where your GEMINI_API_KEY is stored securely on the server!

STEP 1: Push code to your GitHub repository
    git add .
    git commit -m "Transition to 100% Marimo reactive calculus suite"
    git push origin main

STEP 2: Create a Web Service on Render
    1. Log in to https://dashboard.render.com/
    2. Click "New +" -> "Web Service".
    3. Connect your repository: altairmurat/multivar-grapher
    4. Fill in service settings:
       - Name: multivar-grapher
       - Runtime: Python 3
       - Build Command: pip install -r requirements.txt
       - Start Command: python main.py --host 0.0.0.0 --no-browser
    5. Under "Environment Variables":
       - Add: GEMINI_API_KEY = <your-gemini-api-key>
    6. Click "Deploy Web Service".

------------------------------------------------------------------------
OPTION 2: LOCAL MARIMO COMMANDS (https://github.com/marimo-team/marimo)
------------------------------------------------------------------------
    python main.py                  # Launches reactive Marimo app in browser
    python main.py --marimo-edit    # Launches Marimo notebook editor
    python main.py --export-marimo  # Exports static HTML (index.html & marimo_app.html)
    python main.py --legacy-server  # Serves backed-up vanilla HTML/JS from legacy_backup/

------------------------------------------------------------------------
OPTION 3: DEPLOY TO GITHUB PAGES
------------------------------------------------------------------------
1. Run `python main.py --export-marimo` to update `index.html`.
2. In your GitHub repository -> Settings -> Pages -> Branch: "main" / "(root)".
========================================================================
"""
    print(instructions)


def init_git_repo():
    """Initializes git repository and makes an initial commit if git is available."""
    try:
        subprocess.run(["git", "init"], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "add", "."], cwd=BASE_DIR, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit: MultivarGrapher 3D (Marimo)"],
            cwd=BASE_DIR,
            check=True,
        )
        print("✅ Git repository initialized and initial commit created successfully!")
        print_deploy_help()
    except Exception as e:
        print(f"❌ Git initialization error: {e}")


def main():
    default_port = int(os.environ.get("PORT", 8000))
    default_host = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"

    parser = argparse.ArgumentParser(
        description="MultivarGrapher 3D - 100% Marimo Reactive Multivariable Calculus Visualizer"
    )
    parser.add_argument(
        "--host",
        type=str,
        default=default_host,
        help=f"Interface to bind to (default: {default_host})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=default_port,
        help=f"Port for Marimo server (default: {default_port})",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not automatically open the browser",
    )
    parser.add_argument(
        "--marimo",
        action="store_true",
        help="Launch the reactive Marimo application (default behavior)",
    )
    parser.add_argument(
        "--marimo-edit",
        action="store_true",
        help="Launch Marimo in interactive notebook edit mode (`marimo edit app.py`)",
    )
    parser.add_argument(
        "--export-marimo",
        action="store_true",
        help="Export the Marimo reactive notebook to standalone HTML (`index.html` & `marimo_app.html`)",
    )
    parser.add_argument(
        "--legacy-server",
        action="store_true",
        help="Run the backed-up legacy HTML/JS/CSS server from legacy_backup/",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Plot directly with Python/SymPy/Plotly CLI helper",
    )
    parser.add_argument(
        "--formula",
        type=str,
        default="sin(sqrt(x**2 + y**2) * a) * b / (sqrt(x**2 + y**2) + 0.1)",
        help="Mathematical formula for Python CLI plotter",
    )
    parser.add_argument("--a", type=float, default=2.0, help="Value for variable 'a'")
    parser.add_argument("--b", type=float, default=1.0, help="Value for variable 'b'")
    parser.add_argument(
        "--deploy-help",
        action="store_true",
        help="Show instructions to deploy on Render & GitHub Pages",
    )
    parser.add_argument(
        "--init-git",
        action="store_true",
        help="Initialize git repository and stage all files",
    )

    args = parser.parse_args()

    if args.deploy_help:
        print_deploy_help()
    elif args.init_git:
        init_git_repo()
    elif args.export_marimo:
        export_marimo_html()
    elif args.legacy_server:
        run_legacy_backup_server(
            port=args.port,
            host=args.host,
            open_browser=not args.no_browser,
        )
    elif args.plot:
        plot_with_python(
            formula=args.formula,
            a=args.a,
            b=args.b,
            show_browser=not args.no_browser,
        )
    elif args.marimo_edit:
        run_marimo_app(
            port=args.port,
            host=args.host,
            edit_mode=True,
            open_browser=not args.no_browser,
        )
    else:
        should_open = not args.no_browser and not bool(os.environ.get("PORT"))
        run_marimo_app(
            port=args.port,
            host=args.host,
            edit_mode=False,
            open_browser=should_open,
        )


if __name__ == "__main__":
    main()
