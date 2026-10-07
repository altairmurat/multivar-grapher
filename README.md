# 🌌 MultivarGrapher: Affine Functions, Normal Lines & Level Sets

An advanced interactive multivariable calculus suite built with **Plotly.js**, **Math.js**, and **KaTeX**.

Hosted 100% free with **zero backend server** on **GitHub Pages**:
👉 **[Open Live App: https://altairmurat.github.io/multivar-grapher/](https://altairmurat.github.io/multivar-grapher/)**

---

## ✨ Features & Theory Highlight

### 1. 📐 Affine Function $g(\mathbf{x}) = f(\mathbf{a}) + \mathbf{D}f(\mathbf{a})(\mathbf{x} - \mathbf{a})$
- **Mathematical Definition**: The affine function is the best first-order linear approximation (tangent plane) of a differentiable function $f$ near point $\mathbf{a}$:
  $$g(x_1, x_2) = f(a_1, a_2) + \frac{\partial f}{\partial x_1}(\mathbf{a})(x_1 - a_1) + \frac{\partial f}{\partial x_2}(\mathbf{a})(x_2 - a_2)$$
- **3D Tangent Plane Visualization**: Render the affine function as a semi-transparent surface $z = g(x_1, x_2)$ touching $z = f(x_1, x_2)$ tangentially at point $\mathbf{a}$.
- **Approximation Error Calculator**: Test any nearby point $\mathbf{x}$ to compare the exact nonlinear value $f(\mathbf{x})$, the affine approximation $g(\mathbf{x})$, and the error $|f(\mathbf{x}) - g(\mathbf{x})|$.

### 2. 🧭 The Normal Line (2D & 3D Explained)
- **What is the Normal Line?**
  - **In 2D (Level Sets)**: The Normal Line is the line passing through point $\mathbf{a}$ in the direction of the gradient $\nabla f(\mathbf{a})$. It is **strictly perpendicular (at 90 degrees)** to the tangent line of the level curve! Along this line, the function changes fastest (steepest ascent).
  - **In 3D (Surface)**: The Surface Normal Line is the 3D line perpendicular to the tangent plane (affine surface $z = g(\mathbf{x})$) pointing in direction $\mathbf{n} = \langle -f_{x_1}, -f_{x_2}, 1 \rangle$.
- **90° Right-Angle Symbol**: Visually demonstrates orthogonality between the Normal Line and the Tangent Line on the graph.

### 3. 🎯 Level Sets $f^{-1}(c)$ & Circle Radius $r$
- **Level Set Definition**: Set any level constant $c$ to view $f(x_1, x_2) = c$.
- **Radius Helper**: For circle functions $f = x_1^2 + x_2^2$, enter radius $r$ (e.g. $r = 2$) and click **Set $r^2$** to draw the circle $c = 4$.
- **Snap to Curve**: Instantly project point $\mathbf{a}$ onto the level set.

### 4. 🔢 Derivative Matrix $\mathbf{D}f$ $[1 \times n]$
- View both symbolic and numeric evaluations of the total derivative row matrix $\mathbf{D}f(\mathbf{a}) = [ \frac{\partial f}{\partial x_1} \;\; \frac{\partial f}{\partial x_2} ]$ and gradient column vector $\nabla f = (\mathbf{D}f)^T$.

### 5. 🔍 Smooth Interactive Navigation
- **Scroll Zoom**: Zoom in and out effortlessly using the mouse wheel or touchpad pinch gestures.
- **Pan Mode**: Click and drag smoothly across the canvas.
- **On-Screen Zoom Buttons**: Dedicated `[+]`, `[-]`, and `[⟲ Reset]` buttons.
- **Seamless Boundary Buffer**: Auto-regenerates the mesh grid as you zoom or pan, preventing boundary cutoffs.

### 6. 🎨 Modern Purple-and-White UI & Dark Mode Toggle
- **Default Aesthetic**: Elegant modern purple-and-white glassmorphism design with violet accents.
- **Dark Mode**: Interactive header toggle (persisted via `localStorage`) switching both interface elements and Plotly canvas coordinate grids between light and dark themes.

### 7. 📱 Mobile & Smartphone Full Compatibility
- **Dedicated Mobile Viewport**: Mobile segmented switch (`[📊 График / Plot]` vs `[⚙️ Параметры / Controls]`) providing a 100% full-height graph viewing experience on phones.
- **Touch Navigation**: Fluid pinch-to-zoom, touch pan, surface rotation, and tap-friendly on-screen zoom toolbar (`[+]`, `[-]`, `[Pan]`, `[Reset]`).
- **Responsive Controls**: Full-screen parameter workspace with large touch sliders, inputs, and a 1-tap "👉 Show Graph" button.

### 8. 🤖 AI Calculus Tutor Chatbot (Live Graph Context)
- **Live Graph Context Awareness**: Automatically parses and extracts your current function $f(x_1, x_2)$, evaluation point $\mathbf{a}$, gradient $\nabla f(\mathbf{a})$, derivative matrix $Df(\mathbf{a})$, affine approximation $g(\mathbf{x})$, level set $c$, and Hessian determinant $D$.
- **Instant Client-Side Math Intelligence Engine**: Zero configuration, 100% free offline calculus expert with rich KaTeX math equation rendering in chat. Explains gradients, tangent planes, $90^\circ$ orthogonality proofs, and classifies critical points (local minimum, maximum, saddle point).
- **Optional Google Gemini API Integration**: Enter your Google Gemini API key in chat settings to enable open-ended reasoning powered by Gemini 2.5 Flash!
- **Quick Prompt Chips**: 1-tap suggested questions for instant explanations of current parameters.

---

## 🚀 Run Locally

```powershell
python main.py
```

---

## 🌐 GitHub Pages Deployment

Updates are pushed directly to `main` branch and served via GitHub Pages:
[https://altairmurat.github.io/multivar-grapher/](https://altairmurat.github.io/multivar-grapher/)
