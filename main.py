"""
MultivarGrapher 3D - Interactive Multivariable Function Visualizer
==================================================================

Features:
1. Runs an interactive local web server with instant browser launch.
2. Direct Python plotting engine with SymPy symbolic derivatives and Plotly.
3. Automated GitHub Pages deployment instructions & git initialization.

Usage:
    python main.py                  # Launch interactive web app in browser
    python main.py --port 8080      # Launch on custom port
    python main.py --plot           # Generate and open plot using Python/SymPy/Plotly
    python main.py --deploy-help    # View step-by-step GitHub Pages setup guide
    python main.py --init-git       # Initialize git repo and stage all files
"""

import os
import sys
import argparse
import webbrowser
import socket
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# Ensure utf-8 stdout on Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent

def find_available_port(start_port: int = 8000, max_attempts: int = 50) -> int:
    """Finds an unused TCP port starting from `start_port`."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    return start_port

def run_web_server(port: int = 8000, open_browser: bool = True):
    """Starts the local static server and launches the interactive app in the default web browser."""
    actual_port = find_available_port(port)
    server_address = ('127.0.0.1', actual_port)
    url = f"http://127.0.0.1:{actual_port}/index.html"

    print("=" * 70)
    print(" 🚀 MultivarGrapher 3D - Interactive Function Visualizer")
    print("=" * 70)
    print(f" Serving directory : {BASE_DIR}")
    print(f" Local URL         : {url}")
    print(f" GitHub Pages Ready: Yes (Zero backend required!)")
    print("=" * 70)
    print(" Press Ctrl+C at any time to shut down the server.\n")

    os.chdir(BASE_DIR)
    
    class CustomHandler(SimpleHTTPRequestHandler):
        def end_headers(self):
            # Disable caching during local development
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            super().end_headers()

    httpd = ThreadingHTTPServer(server_address, CustomHandler)

    if open_browser:
        print(" Opening application in your web browser...")
        webbrowser.open(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n Shutting down server gracefully. Goodbye!")
        httpd.server_close()
        sys.exit(0)

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
    show_browser: bool = True
):
    """
    Evaluates multivariable functions directly via Python (SymPy & NumPy)
    and produces an interactive 3D Plotly visualization.
    """
    try:
        import numpy as np
        import sympy as sp
        import plotly.graph_objects as go
    except ImportError as e:
        print(f"❌ Missing Python plotting library: {e}")
        print("Please install requirements using: pip install numpy sympy plotly")
        sys.exit(1)

    print(f"\n📊 Evaluating function in Python: z = f(x, y) = {formula}")
    print(f" Parameters: a={a}, b={b}")
    print(f" Domain: x in [{x_min}, {x_max}], y in [{y_min}, {y_max}]")

    x_sym, y_sym, a_sym, b_sym = sp.symbols('x y a b')
    
    # Clean formula syntax (^ to **)
    clean_formula = formula.replace('^', '**')
    parsed_expr = sp.sympify(clean_formula)

    # Compute symbolic derivatives
    df_dx_sym = sp.diff(parsed_expr, x_sym)
    df_dy_sym = sp.diff(parsed_expr, y_sym)

    print(f" Symbolic ∂z/∂x: {df_dx_sym}")
    print(f" Symbolic ∂z/∂y: {df_dy_sym}")

    # Substitute parameters
    subbed_expr = parsed_expr.subs({a_sym: a, b_sym: b})
    f_lambdified = sp.lambdify((x_sym, y_sym), subbed_expr, modules=['numpy', 'math'])

    # Generate 2D mesh
    x_vals = np.linspace(x_min, x_max, points)
    y_vals = np.linspace(y_min, y_max, points)
    X, Y = np.meshgrid(x_vals, y_vals)

    try:
        Z = f_lambdified(X, Y)
        # Handle scalar output if constant expression
        if isinstance(Z, (int, float)):
            Z = np.full_like(X, float(Z))
    except Exception as e:
        print(f"❌ Error computing grid values: {e}")
        return

    # Build Plotly 3D Surface
    fig = go.Figure(data=[
        go.Surface(
            x=X, y=Y, z=Z,
            colorscale='Turbo',
            colorbar=dict(title='z'),
            contours=dict(
                z=dict(show=True, usecolormap=True, project=dict(z=True))
            )
        )
    ])

    fig.update_layout(
        title=f"Multivariable Graph: z = {clean_formula} (a={a}, b={b})",
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.3))
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        template='plotly_dark'
    )

    out_path = BASE_DIR / output_html
    fig.write_html(str(out_path))
    print(f"✅ Interactive Plotly HTML generated at: {out_path}")

    if show_browser:
        webbrowser.open(out_path.as_uri())

def print_deploy_help():
    """Prints clear, foolproof instructions for deploying to GitHub Pages for free."""
    instructions = """
========================================================================
 🌐 HOW TO DEPLOY TO GITHUB PAGES (100% FREE, NO RENDER NEEDED!)
========================================================================

Because MultivarGrapher 3D runs entirely in the browser using WebGL and
client-side formula parsing, it requires NO BACKEND SERVER! You can host
it for free forever on GitHub Pages in 4 simple steps:

STEP 1: Initialize Git and commit files
---------------------------------------
Run the following in your terminal:
    git init
    git add .
    git commit -m "Deploy MultivarGrapher 3D to GitHub Pages"

STEP 2: Create a new repository on GitHub
-----------------------------------------
1. Go to https://github.com/new
2. Name the repository (e.g., "multivar-grapher")
3. Leave it Public, do not initialize with README (we already have one).
4. Click "Create repository".

STEP 3: Push your code to GitHub
--------------------------------
Run the commands GitHub gives you (replace USERNAME and REPO):
    git branch -M main
    git remote add origin https://github.com/<YOUR-USERNAME>/<REPO-NAME>.git
    git push -u origin main

STEP 4: Turn on GitHub Pages (Instant Hosting!)
-----------------------------------------------
1. In your GitHub repository, click on "Settings" (top tab).
2. On the left sidebar, click "Pages" (under Code and automation).
3. Under "Build and deployment" -> "Branch":
   - Select: "main"
   - Select folder: "/ (root)"
4. Click "Save".

🎉 That's it! In about 30 seconds, GitHub will give you a public URL:
   https://<YOUR-USERNAME>.github.io/<REPO-NAME>/

You can send this link to anyone or open it on your phone, tablet,
or laptop to graph 3D multivariable equations with 0 server costs!
========================================================================
"""
    print(instructions)

def init_git_repo():
    """Initializes git repository and makes an initial commit if git is available."""
    import subprocess
    try:
        subprocess.run(["git", "init"], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "add", "."], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit: MultivarGrapher 3D"], cwd=BASE_DIR, check=True)
        print("✅ Git repository initialized and initial commit created successfully!")
        print_deploy_help()
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")
    except FileNotFoundError:
        print("❌ 'git' is not installed or not in PATH.")

def main():
    parser = argparse.ArgumentParser(
        description="MultivarGrapher 3D - Interactive Multivariable Function Visualizer"
    )
    parser.add_argument("--port", type=int, default=8000, help="Local port for web server (default: 8000)")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open the browser")
    parser.add_argument("--plot", action="store_true", help="Plot directly with Python/SymPy/Plotly instead of web server")
    parser.add_argument("--formula", type=str, default="sin(sqrt(x**2 + y**2) * a) * b / (sqrt(x**2 + y**2) + 0.1)",
                        help="Mathematical formula for Python plotter")
    parser.add_argument("--a", type=float, default=2.0, help="Value for variable 'a'")
    parser.add_argument("--b", type=float, default=1.0, help="Value for variable 'b'")
    parser.add_argument("--deploy-help", action="store_true", help="Show instructions to deploy for free on GitHub Pages")
    parser.add_argument("--init-git", action="store_true", help="Initialize git repository and stage all files")

    args = parser.parse_args()

    if args.deploy_help:
        print_deploy_help()
    elif args.init_git:
        init_git_repo()
    elif args.plot:
        plot_with_python(
            formula=args.formula,
            a=args.a,
            b=args.b,
            show_browser=not args.no_browser
        )
    else:
        run_web_server(port=args.port, open_browser=not args.no_browser)

if __name__ == "__main__":
    main()
