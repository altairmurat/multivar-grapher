# 🌌 MultivarGrapher: 3D Surfaces, Level Sets & Derivative Matrices

An interactive multivariable calculus visualizer built with **Plotly.js**, **Math.js**, and **KaTeX**.

Hosted 100% free with **zero backend server** on **GitHub Pages**:
👉 **[Open Live App: https://altairmurat.github.io/multivar-grapher/](https://altairmurat.github.io/multivar-grapher/)**

---

## ✨ Features Highlight

### 1. 🎯 Level Sets $f^{-1}(c)$ & Circle Radius $r$
- **Level Set Equation**: Set any target value $c$ for the level set $f(x_1, x_2) = c$.
- **Radius Helper**: For circle functions like $f(x_1, x_2) = x_1^2 + x_2^2$, enter radius $r$ (e.g. $r = 2$) and click **Set $r^2$** to instantly set $c = 4$, rendering a clean circle of radius 2.
- **Snap Point $P_0$ to Curve**: One-click Newton-Raphson projection button snaps your evaluation point $P_0$ directly onto the level set curve.
- **2D & 3D Views**: Switch between 2D Level Set view, 3D Surface view, or Split View (both side-by-side).

### 2. 📐 90° Gradient Vector $\perp$ Tangent Line (Orthogonality)
- **Gradient Vector $\nabla f$**: Bright amber arrow originating at $P_0$ pointing in the direction of steepest ascent.
- **Tangent Line**: Pink dashed line tangent to the circle/level curve at $P_0$.
- **90° Right-Angle Symbol**: A dedicated square corner symbol at $P_0$ visually confirming that **$\nabla f$ is strictly perpendicular (90 degrees / normal) to the tangent line and level curve**.

### 3. 🔢 Derivative as a $[1 \times n]$ Matrix ($Df = \nabla f^T$)
- For scalar fields $f: \mathbb{R}^n \to \mathbb{R}$, the total derivative / Jacobian is represented as a **$1 \times n$ row matrix**:
  $$\mathbf{D}f(\mathbf{x}) = \begin{bmatrix} \frac{\partial f}{\partial x_1} & \frac{\partial f}{\partial x_2} \end{bmatrix}_{1 \times 2}$$
- **Evaluated Numerically at $P_0$**:
  $$\mathbf{D}f(P_0) = \begin{bmatrix} f_{x_1}(P_0) & f_{x_2}(P_0) \end{bmatrix}_{1 \times 2}$$
- Supports both **$(x_1, x_2)$** and **$(x, y)$** variable notation styles.

---

## 🚀 Run Locally

```powershell
python main.py
```
Starts a local server and opens your browser.

---

## 🌐 GitHub Pages Deployment

Updates are pushed directly to `main` branch and served via GitHub Pages:
[https://altairmurat.github.io/multivar-grapher/](https://altairmurat.github.io/multivar-grapher/)
