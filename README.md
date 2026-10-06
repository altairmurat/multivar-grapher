# 🌌 MultivarGrapher 3D

An interactive, high-performance 3D multivariable function visualizer built with **Plotly.js**, **Math.js**, and **KaTeX**, featuring real-time parameter manipulation, calculus analysis tools (tangent planes, symbolic derivatives, gradient exploration), and dual-surface intersection.

Designed to run **100% client-side**, allowing you to deploy directly to **GitHub Pages** for free with **zero backend setup** (no Render, Heroku, or AWS needed).

---

## ✨ Features

- **⚡ Real-Time Formula Parsing**: Type any custom function $z = f(x, y)$ or secondary surface $z = g(x, y)$ using natural mathematical syntax (`sin`, `cos`, `tan`, `sqrt`, `exp`, `log`, `^`, `pi`, `e`).
- **🎛️ Dynamic Parameter Sliders**: Real-time interactive sliders for parameters $a, b, c, d$ with custom min/max/step. Add your own custom variables dynamically on the fly!
- **⏱️ 4D Time Animation**: Dedicated animated parameter $t$ with Play/Pause and speed controls for wave packets, rippling water droplets, and oscillating surfaces.
- **📐 Calculus & Analysis Tools**:
  - **Symbolic Partial Derivatives**: Live analytic calculation of $\frac{\partial z}{\partial x}$ and $\frac{\partial z}{\partial y}$.
  - **Tangent Plane**: Interactive tangent plane touching the surface at probe point $(x_0, y_0)$ in real time.
  - **Cross-Section Slices**: Real-time 3D trace curves for $x = x_0$ and $y = y_0$.
- **🎨 Visual Customization**:
  - 8 distinct color palettes (Turbo, Viridis, Plasma, Magma, Jet, Electric, Spectral, Rainbow).
  - 3D surface contours and $xy$-plane floor projection contours.
  - Wireframe mesh grid toggle and opacity adjustments.
- **📚 Curated Preset Library**:
  - Hyperbolic Paraboloid (Saddle)
  - Elliptic Paraboloid (Bowl)
  - Monkey Saddle
  - Water Droplet Ripple (Sinc)
  - Gaussian Bell Wave Packet
  - Egg Carton Grid
  - Rosenbrock Valley
  - Animated Sombrero Wave
  - Chladni Nodal Surface
- **🔗 Shareable Links**: Serializes entire graph state (formulas, parameter values, ranges, view settings) into the URL hash so you can share exact graphs via a single URL.
- **📸 High-Res Export**: Save high-resolution PNG renders with one click.

---

## 🚀 Quickstart (Run Locally)

You can launch and use the app locally using Python's built-in tools (no pip installations required):

```bash
# Clone or navigate to the project directory
cd multivar_grapher

# Launch the app (automatically opens in your default browser)
python main.py
```

### Python-Native Plotting Mode (Optional)
If you want to evaluate equations and generate plots using Python's `SymPy` and `NumPy` engines:

```bash
# Install optional dependencies
pip install -r requirements.txt

# Run Python Plotter
python main.py --plot --formula "sin(x) * cos(y)" --a 2.0
```

---

## 🌐 Deploy to GitHub Pages (100% Free, No Render Needed!)

Because the app is fully static and executes calculations client-side in the browser via WebGL and JavaScript:
- **No server sleep/cold starts** (unlike Render free tier).
- **No hosting fees** (GitHub Pages is free forever).
- **Fast 60 FPS slider responsiveness** with zero latency.

### Step-by-Step Deployment:

1. **Initialize Git and commit**:
   ```bash
   git init
   git add .
   git commit -m "Deploy MultivarGrapher 3D"
   ```

2. **Create a new GitHub Repository**:
   - Go to [github.com/new](https://github.com/new).
   - Enter a repository name (e.g., `multivar-grapher`).
   - Choose **Public**, then click **Create repository**.

3. **Push to GitHub**:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<YOUR-USERNAME>/<YOUR-REPO-NAME>.git
   git push -u origin main
   ```

4. **Enable GitHub Pages**:
   - In your GitHub repository, click **Settings** (tab at the top).
   - In the left sidebar, click **Pages** (under the *Code and automation* section).
   - Under **Build and deployment** > **Branch**:
     - Select branch: `main`
     - Select folder: `/ (root)`
     - Click **Save**.

5. **Open your live link!**
   In about 30 seconds, your site will be live at:
   ```
   https://<YOUR-USERNAME>.github.io/<YOUR-REPO-NAME>/
   ```

---

## 🧮 Math Function Syntax Guide

| Function | Example Syntax |
| :--- | :--- |
| Trigonometric | `sin(x)`, `cos(y)`, `tan(x)`, `asin(x)`, `atan2(y, x)` |
| Exponential & Log | `exp(x)`, `log(x)` (natural log), `log10(x)` |
| Roots & Powers | `sqrt(x^2 + y^2)`, `x^2`, `x^3`, `cbrt(x)` |
| Constants | `pi`, `e`, `tau` |
| Parameters | `a`, `b`, `c`, `d`, `t` |

Example equations to try:
- `sin(sqrt(x^2 + y^2) * a) * b / (sqrt(x^2 + y^2) + 0.1)` (Ripple)
- `a * (x^2 - y^2) / 4` (Saddle)
- `a * sin(b * x) * cos(c * y)` (Egg Carton)
- `a * cos(b * sqrt(x^2 + y^2) - t)` (Animated Travelling Wave)
