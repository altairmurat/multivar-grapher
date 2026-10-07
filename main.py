"""
MultivarGrapher 3D - Interactive Multivariable Function Visualizer & Calculus Suite
==================================================================================

Features:
1. Runs an interactive local & production web server (Render & GitHub Pages ready).
2. Built-in Gemini 3.5 Flash-Lite API backend proxy (/api/chat) for Render deployment.
3. Direct Python plotting engine with SymPy symbolic derivatives and Plotly.
4. Automated deployment guides for Render (with GEMINI_API_KEY) and GitHub Pages.

Usage:
    python main.py                  # Launch interactive web app locally
    python main.py --host 0.0.0.0   # Launch on public/container interface (Render)
    python main.py --port 8080      # Launch on custom port
    python main.py --plot           # Generate and open plot using Python/SymPy/Plotly
    python main.py --deploy-help    # View step-by-step Render and GitHub Pages guides
    python main.py --init-git       # Initialize git repo and stage all files
"""

import os
import sys
import argparse
import webbrowser
import socket
import json
import ssl
import urllib.request
import urllib.error
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

def call_gemini_api(api_key: str, message: str, context: dict = None) -> tuple:
    """
    Calls Google Gemini API in English with Live Graph Calculus Context.
    Uses gemini-3.5-flash-lite as primary model with graceful fallbacks.
    Returns (reply_text, model_name).
    """
    if not context:
        context = {}

    formula = context.get('formula', 'x1^2 + x2^2')
    v1 = context.get('v1', 'x1')
    v2 = context.get('v2', 'x2')
    point_a = context.get('point_a', [0, 0])
    fa = context.get('f_at_a', '')
    derivs = context.get('derivatives', {})
    fx = derivs.get('fx', '')
    fy = derivs.get('fy', '')
    mag = context.get('gradient_magnitude', '')
    c_val = context.get('level_c', '')
    diff = context.get('level_diff', '')
    t_pt = context.get('test_point', [0, 0])
    t_exact = context.get('test_exact', '')
    t_affine = context.get('test_affine', '')
    t_err = context.get('test_error', '')
    hess = context.get('hessian', {})
    ext_type = context.get('extremumType', 'Unknown')

    pt_x = point_a[0] if isinstance(point_a, (list, tuple)) and len(point_a) > 0 else 0
    pt_y = point_a[1] if isinstance(point_a, (list, tuple)) and len(point_a) > 1 else 0

    tp_x = t_pt[0] if isinstance(t_pt, (list, tuple)) and len(t_pt) > 0 else 0
    tp_y = t_pt[1] if isinstance(t_pt, (list, tuple)) and len(t_pt) > 1 else 0

    system_prompt = f"""You are an expert Multivariable Calculus AI Tutor in the MultivarGrapher web app.
IMPORTANT: ALWAYS RESPOND IN ENGLISH.
Use clear, pedagogical explanations with formatted LaTeX math ($...$ for inline and $$...$$ for block equations).

Current live graph state:
- Function: f({v1}, {v2}) = {formula}
- Point a = ({pt_x}, {pt_y})
- Value f(a) = {fa}
- Partial derivatives: df/d{v1} = {fx}, df/d{v2} = {fy}
- Gradient: ∇f(a) = [{fx}, {fy}]^T (magnitude = {mag})
- Derivative row matrix: Df(a) = [{fx}, {fy}] [1x2]
- Level set constant c = {c_val} (difference at a: f(a) - c = {diff})
- Affine function: g(x) = f(a) + Df(a)(x - a)
- Test point for linearization: ({tp_x}, {tp_y}), exact = {t_exact}, affine = {t_affine}, error = {t_err}
- Second derivatives: f_11 = {hess.get('f_xx', '')}, f_22 = {hess.get('f_yy', '')}, f_12 = {hess.get('f_xy', '')}, Hessian determinant D = {hess.get('det', '')}
- Extremum classification: {ext_type}

Instructions:
1. Answer the user's question directly in English using LaTeX math equations ($...$ and $$...$$).
2. Ground your answer on the exact function and numeric values provided in the snapshot.
3. Be concise, mathematically accurate, and educational."""

    candidate_models = [
        'gemini-3.5-flash-lite',
        'gemini-2.5-flash-lite',
        'gemini-2.0-flash',
        'gemini-1.5-flash'
    ]

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"{system_prompt}\n\nUser Question: {message}"
                    }
                ]
            }
        ]
    }
    payload_bytes = json.dumps(payload).encode('utf-8')
    ssl_context = ssl.create_default_context()

    last_error = None
    for model in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(
            url,
            data=payload_bytes,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
                if response.status == 200:
                    res_data = json.loads(response.read().decode('utf-8'))
                    candidates = res_data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts and "text" in parts[0]:
                            return parts[0]["text"], model
        except urllib.error.HTTPError as he:
            err_body = he.read().decode('utf-8', errors='ignore')
            last_error = f"{model} HTTP {he.code}: {err_body}"
        except Exception as e:
            last_error = f"{model} error: {str(e)}"

    raise RuntimeError(f"All Gemini models failed. Last error: {last_error}")

class MultivarServerHandler(SimpleHTTPRequestHandler):
    """
    HTTP Request Handler that serves MultivarGrapher static assets
    and exposes /api/status and /api/chat endpoints for Render deployment.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def send_json_response(self, status_code: int, data: dict):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        # API Health / Status Check
        if self.path in ('/api/status', '/api/health'):
            has_gemini = bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
            self.send_json_response(200, {
                "status": "ok",
                "service": "MultivarGrapher",
                "has_gemini_key": has_gemini,
                "model": "gemini-3.5-flash-lite"
            })
            return

        # Default root path serves index.html
        if self.path in ('/', ''):
            self.path = '/index.html'

        super().do_GET()

    def do_POST(self):
        # AI Chatbot proxy endpoint (Render backend)
        if self.path == '/api/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0:
                self.send_json_response(400, {"error": "Empty request body"})
                return

            raw_data = self.rfile.read(content_length)
            try:
                req_json = json.loads(raw_data.decode('utf-8'))
            except Exception as e:
                self.send_json_response(400, {"error": f"Invalid JSON body: {str(e)}"})
                return

            message = req_json.get('message', '').strip()
            context = req_json.get('context', {})

            if not message:
                self.send_json_response(400, {"error": "No message specified"})
                return

            api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                self.send_json_response(503, {
                    "error": "GEMINI_API_KEY is not set in server environment variables. Configure GEMINI_API_KEY in Render dashboard to enable server-side AI."
                })
                return

            try:
                reply, model_used = call_gemini_api(api_key, message, context)
                self.send_json_response(200, {
                    "reply": reply,
                    "model": model_used
                })
            except Exception as e:
                self.send_json_response(500, {
                    "error": f"Gemini API execution error: {str(e)}"
                })
            return

        self.send_json_response(404, {"error": f"Unknown endpoint: {self.path}"})

    def end_headers(self):
        # Disable caching in development and production reload
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

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

def run_web_server(port: int = 8000, host: str = "0.0.0.0", open_browser: bool = False):
    """Starts the web server with API proxy and launches interactive app."""
    # If Render sets PORT env var, prioritize it strictly
    env_port = os.environ.get("PORT")
    if env_port:
        actual_port = int(env_port)
    elif host == "127.0.0.1":
        actual_port = find_available_port(port)
    else:
        actual_port = port

    server_address = (host, actual_port)
    url = f"http://{host if host != '0.0.0.0' else 'localhost'}:{actual_port}/index.html"

    has_key = bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))

    print("=" * 75)
    print(" 🚀 MultivarGrapher 3D - Interactive Function Visualizer & Calculus Suite")
    print("=" * 75)
    print(f" Serving directory   : {BASE_DIR}")
    print(f" Listening interface : {host}:{actual_port}")
    print(f" Web URL             : {url}")
    print(f" Gemini Server Key   : {'🟢 Configured (gemini-3.5-flash-lite active)' if has_key else '⚪ None (Users can use client key or offline engine)'}")
    print(f" Render & GH Pages   : 100% Ready")
    print("=" * 75)
    print(" Press Ctrl+C at any time to shut down the server.\n")

    os.chdir(BASE_DIR)

    httpd = ThreadingHTTPServer(server_address, MultivarServerHandler)

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
    
    clean_formula = formula.replace('^', '**')
    parsed_expr = sp.sympify(clean_formula)

    df_dx_sym = sp.diff(parsed_expr, x_sym)
    df_dy_sym = sp.diff(parsed_expr, y_sym)

    print(f" Symbolic ∂z/∂x: {df_dx_sym}")
    print(f" Symbolic ∂z/∂y: {df_dy_sym}")

    subbed_expr = parsed_expr.subs({a_sym: a, b_sym: b})
    f_lambdified = sp.lambdify((x_sym, y_sym), subbed_expr, modules=['numpy', 'math'])

    x_vals = np.linspace(x_min, x_max, points)
    y_vals = np.linspace(y_min, y_max, points)
    X, Y = np.meshgrid(x_vals, y_vals)

    try:
        Z = f_lambdified(X, Y)
        if isinstance(Z, (int, float)):
            Z = np.full_like(X, float(Z))
    except Exception as e:
        print(f"❌ Error computing grid values: {e}")
        return

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
    """Prints clear, foolproof instructions for deploying to Render and GitHub Pages."""
    instructions = """
========================================================================
 🌟 DEPLOYMENT GUIDE: RENDER (WITH GEMINI AI) & GITHUB PAGES
========================================================================

OPTION 1: DEPLOY ON RENDER (NO CLIENT API KEY NEEDED!)
-------------------------------------------------------
Deploying to Render creates a web service where your GEMINI_API_KEY is
stored securely on the server, so any user visiting the site gets
instant AI Calculus Tutor responses without entering their own API key!

STEP 1: Push code to your GitHub repository
    git add .
    git commit -m "Configure Render web service deployment"
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

Render will give you a public URL (e.g., https://multivar-grapher.onrender.com).
The AI assistant will automatically use your server key with gemini-3.5-flash-lite!

------------------------------------------------------------------------
OPTION 2: DEPLOY TO GITHUB PAGES (STATIC HOSTING, 100% FREE)
------------------------------------------------------------------------
GITHUB PAGES hosts the visualizer directly from your repository:
1. In your GitHub repository, click on "Settings" (top tab).
2. On the left sidebar, click "Pages" (under Code and automation).
3. Under "Build and deployment" -> "Branch":
   - Select: "main"
   - Select folder: "/ (root)"
4. Click "Save".

Your URL: https://<YOUR-USERNAME>.github.io/<REPO-NAME>/
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
    default_port = int(os.environ.get("PORT", 8000))
    default_host = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"

    parser = argparse.ArgumentParser(
        description="MultivarGrapher 3D - Interactive Multivariable Function Visualizer"
    )
    parser.add_argument("--host", type=str, default=default_host, help=f"Interface to bind to (default: {default_host})")
    parser.add_argument("--port", type=int, default=default_port, help=f"Port for web server (default: {default_port})")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open the browser")
    parser.add_argument("--plot", action="store_true", help="Plot directly with Python/SymPy/Plotly instead of web server")
    parser.add_argument("--formula", type=str, default="sin(sqrt(x**2 + y**2) * a) * b / (sqrt(x**2 + y**2) + 0.1)",
                        help="Mathematical formula for Python plotter")
    parser.add_argument("--a", type=float, default=2.0, help="Value for variable 'a'")
    parser.add_argument("--b", type=float, default=1.0, help="Value for variable 'b'")
    parser.add_argument("--deploy-help", action="store_true", help="Show instructions to deploy on Render & GitHub Pages")
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
        # Open browser only if local development and not explicitly suppressed
        should_open = not args.no_browser and not bool(os.environ.get("PORT"))
        run_web_server(port=args.port, host=args.host, open_browser=should_open)

if __name__ == "__main__":
    main()
