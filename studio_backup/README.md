# 🌌 MultivarGrapher 3D — 100% Marimo Reactive Calculus & Linear Algebra Suite

An interactive multivariable calculus, linear algebra, and constrained 3D surface visualizer powered natively by **[marimo](https://github.com/marimo-team/marimo)** (`app.py` + `calculus_engine.py` + `custom.css`).

- ⚡ **Launch Reactive Marimo App**: `python main.py` or `marimo run app.py`
- ✏️ **Open Marimo Reactive Editor**: `python main.py --marimo-edit` or `marimo edit app.py`
- 🌐 **Render Web Service** (Auto Gemini AI with `GEMINI_API_KEY`): Ready to deploy with `render.yaml`!
- 📦 **Legacy HTML/JS/CSS Backup**: Preserved safely in [`legacy_backup/`](legacy_backup/) (`index.html`, `styles.css`, `app.js`).

---

## ✨ Architecture & Features

### 1. ⚡ 100% Reactive Marimo Application (`app.py` + `calculus_engine.py`)
- **Pure Reactive Dataflow DAG**: Every slider, preset selector, constraint chip, and AI Tutor action automatically updates the underlying reactive state (`mo.state` + `mo.query_params`) and re-renders the 2D/3D Plotly figures and symbolic LaTeX derivations in real time.
- **5 Dedicated Interactive Tabs + Global Sidebar**:
  1. **🏛️ Function & Constraints**: 17 built-in presets, custom formulas, matrices in $\mathbb{R}^2/\mathbb{R}^3$, vector fields, and 1-click free-variable cylinder chips.
  2. **🎯 Level Set & Point $\mathbf{a}$**: Level constant $c$ & radius $r = \sqrt{c}$ sync, **Snap Point $\mathbf{a}$ to Level Curve**, **Snap to Critical Point ($\nabla f = \mathbf{0}$)**, and Total Derivative row matrix $\mathbf{D}f(\mathbf{a})$.
  3. **📐 Affine Plane & Normal**: Best first-order linear approximation $g(\mathbf{x}) = f(\mathbf{a}) + \mathbf{D}f(\mathbf{a})(\mathbf{x} - \mathbf{a})$, 2D/3D orthogonal normal vectors ($90^\circ$ right-angle marker), and Taylor linearization error calculator at $\mathbf{x}_{\text{test}}$.
  4. **🔍 Hessian & Extrema**: Symbolic and numeric Hessian matrix $\mathbf{H}_f(\mathbf{a})$, eigenvalues $\lambda_i$, trace, discriminant $D = f_{11}f_{22} - f_{12}^2$, and Second Derivative Test classification.
  5. **🤖 AI Calculus Tutor**: Powered by `gemini-3.5-flash-lite` (with automatic Offline Calculus Engine fallback). Supports 1-click and natural-language **Auto Graph Actions** that configure functions, constraints, and 3D views automatically (with raw JSON code blocks cleanly hidden from chat).

### 2. 🏛️ Optional Requirements & Free-Variable 3D Cylinders
- Enter any equality or inequality requirement in the **Optional Requirement / Domain Constraint** box:
  - Example: `F(x1, x2, x3) = [x1; x2; x3]` with requirement `x1^2/4 + x2 = 1` or `x1^2/4 + x2^2/9 = 1`.
  - Because $x_3$ is a free variable ($x_3 \in (-\infty, \infty)$), the engine automatically extrudes the 2D Marching-Squares curve along the vertical $x_3$-axis to render a **3D Parabolic or Elliptic Cylinder**!

### 3. 🧊 Matrices & Vector Fields in $\mathbb{R}^2$ and $\mathbb{R}^3$
- Enter $2 \times 2$ matrices (e.g. `[2, 1; 1, 2]`) or $3 \times 3$ matrices (e.g. `[1, 2, 3; 4, 5, 6; 7, 8, 9]`) to visualize transformed basis arrows $\mathbf{A}\mathbf{e}_i$, evaluation vector $\mathbf{a} \mapsto \mathbf{A}\mathbf{a}$, unit sphere/circle deformation, determinant $\det(\mathbf{A})$, trace, and eigenvalues.

### 4. 🎬 Interactive 3D Animations
- **360° Camera Orbit**, **Animated Level Slice $c(t)$**, and **Gliding Point $\mathbf{a}(t)$** with dynamic tangent planes built directly into the Plotly WebGL viewport.

---

## 💻 Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the reactive Marimo web app (default)
python main.py

# Or run directly with the marimo CLI:
marimo run app.py
```

### Additional CLI Commands
```bash
python main.py --marimo-edit     # Open Marimo notebook editor
python main.py --export-marimo   # Export standalone HTML snapshots (index.html & marimo_app.html)
python main.py --legacy-server   # Serve the backed-up vanilla HTML/JS/CSS version from legacy_backup/
python test_grapher.py           # Run the full verification test suite
```
