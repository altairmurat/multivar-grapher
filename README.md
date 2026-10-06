# 🌌 MultivarGrapher 3D & Level Sets

An interactive, high-performance 3D multivariable function visualizer and 2D Level Sets (Contour Map) explorer built with **Plotly.js**, **Math.js**, and **KaTeX**.

Features real-time parameter manipulation, exact point evaluation (e.g. $x = 2, y = 1$), symbolic partial derivatives, interactive gradient vectors $\nabla f$, surface normal vectors $\mathbf{n}$, and tangent planes.

Hosted 100% free with **zero backend server** on **GitHub Pages**:
👉 **[Open Live App: https://altairmurat.github.io/multivar-grapher/](https://altairmurat.github.io/multivar-grapher/)**

---

## ✨ Key Features

### 1. 🗺️ Level Sets & Contour Map (2D & 3D)
- **Dedicated 2D Level Sets View**: Switch between **3D Surface**, **2D Level Sets (Contour Map)**, or **Split View** side-by-side.
- **Isolines with Value Labels**: Clearly labeled contour lines with adjustable contour density.
- **Specific Level Curve $f(x, y) = c$**: Highlight any specific level curve with slider/input or click **Set $c = f(x_0, y_0)$** to highlight the exact curve passing through your evaluation point.
- **Gradient Vector Field**: Toggle a vector field of gradient arrows across the entire domain, demonstrating the fundamental calculus theorem that **gradient vectors are always orthogonal (perpendicular) to level sets**.

### 2. 📐 Exact Point Evaluation & Live Derivatives
- **Exact Point Inputs**: Type any exact coordinates (e.g., $x = 2$, $y = 1$) or drag the sliders. You can also click anywhere on the 2D contour map to set $P_0$.
- **Symbolic Partial Derivatives**: Live analytic display of $\frac{\partial f}{\partial x}$ and $\frac{\partial f}{\partial y}$ rendered via KaTeX.
- **Exact Numerical Calculus Values**:
  - Surface Value: $f(x_0, y_0)$
  - Partial Derivatives: $\frac{\partial f}{\partial x}(x_0, y_0)$ and $\frac{\partial f}{\partial y}(x_0, y_0)$
  - Gradient Vector: $\nabla f = \langle f_x, f_y \rangle$
  - Gradient Magnitude: $\|\nabla f\| = \sqrt{f_x^2 + f_y^2}$ (rate of steepest ascent)
  - Angle of Steepest Ascent: $\theta$
  - Tangent Plane Equation: $z = f_0 + f_x(x - x_0) + f_y(y - y_0)$

### 3. 🎯 On-Graph Vector Visualizations
- **3D Gradient Vector $\nabla f$**: Bright vector arrow drawn on the 3D surface pointing in the direction of steepest ascent.
- **2D Gradient Vector**: Vector arrow on the 2D level set map perpendicular to the contour curves.
- **Surface Normal Vector $\mathbf{n}$**: Vector $\mathbf{n} = \langle -f_x, -f_y, 1 \rangle$ pointing perpendicularly outward from the surface.
- **Tangent Plane**: Semi-transparent plane touching the surface tangentially at $P_0$.
- **Cross-Section Curves**: 3D slices along planes $x = x_0$ and $y = y_0$.

### 4. 🎛️ Real-Time Sliders & 4D Time Animation
- Interactive sliders for parameters $a, b, c, d$ (with live formula recalculation at 60 FPS).
- Add custom variables dynamically on the fly ($k, m, w$).
- Animated time variable $t$ with Play/Pause for ripples and traveling wave packets.

---

## 🚀 Run Locally

```powershell
python main.py
```
This starts a local development server and automatically opens the app in your browser.

---

## 🌐 Deploy to GitHub Pages

To push any updates:
```powershell
git add .
git commit -m "Update grapher features"
git push -u origin main
```
Your live link updates automatically at [https://altairmurat.github.io/multivar-grapher/](https://altairmurat.github.io/multivar-grapher/).
