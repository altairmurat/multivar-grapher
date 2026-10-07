# 🌌 MultivarGrapher: Affine Functions, Normal Lines & Level Sets

An advanced interactive multivariable calculus suite built with **Plotly.js**, **Math.js**, and **KaTeX**.

- 🌐 **Render Web Service** (Auto Gemini AI with `GEMINI_API_KEY`): Ready to deploy with `render.yaml`!
- 🌐 **GitHub Pages (Static 100% Free)**: [https://altairmurat.github.io/multivar-grapher/](https://altairmurat.github.io/multivar-grapher/)

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

### 5. 🔗 URL Hash State Sharing & Instant Restoration
- Clicking **Share** serializes the entire state (function formula, level set $c$, radius $r$, evaluation point $\mathbf{a}$, domain ranges, toggles, notation, and theme) into the URL hash `#...`.
- Opening or sharing the link instantly restores the exact mathematical configuration and recalculates all derivatives and graphs without resetting to defaults.

### 6. 📱 Mobile & Smartphone Full Compatibility
- **Dedicated Mobile Viewport**: Mobile segmented switch (`[📊 График]` vs `[⚙️ Параметры]`) providing a 100% full-height graph viewing experience on phones.
- **Touch Navigation**: Fluid pinch-to-zoom, touch pan, surface rotation, and tap-friendly on-screen zoom toolbar (`[+]`, `[-]`, `[Pan]`, `[Reset]`).
- **Responsive Controls**: Full-screen parameter workspace with large touch sliders, inputs, and a 1-tap "👉 Show Graph" button.

### 7. 🤖 AI Calculus Tutor Chatbot (`gemini-3.5-flash-lite`)
- **Live Graph Context Awareness**: Automatically parses and extracts your current function $f(x_1, x_2)$, evaluation point $\mathbf{a}$, gradient $\nabla f(\mathbf{a})$, derivative matrix $Df(\mathbf{a})$, affine approximation $g(\mathbf{x})$, level set $c$, and Hessian determinant $D$.
- **Render Backend Proxy (No Client API Key Needed)**: When deployed on Render with `GEMINI_API_KEY`, the server proxy handles queries automatically using `gemini-3.5-flash-lite` strictly in English.
- **Offline Math Intelligence Fallback**: 100% free offline calculus engine with rich KaTeX math equation rendering in chat.

---

## 🚀 Deployment

### Option A: Render Deployment (Recommended for AI Key Setup)

1. Push your repository to GitHub:
   ```bash
   git add .
   git commit -m "Deploy to Render"
   git push origin main
   ```
2. Go to [Render Dashboard](https://dashboard.render.com/) -> **New +** -> **Web Service**.
3. Select your repository `altairmurat/multivar-grapher`.
4. Configure service settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py --host 0.0.0.0 --no-browser`
5. In **Environment Variables**:
   - Add `GEMINI_API_KEY` = `<your-api-key>`
6. Click **Deploy Web Service**! Render will generate your public URL where Gemini AI is immediately available to all visitors without them needing to input any API key.

### Option B: GitHub Pages (Free Static Hosting)

1. In your GitHub repo, go to **Settings** -> **Pages**.
2. Under **Build and deployment** -> **Branch**, select `main` and folder `/ (root)`.
3. Click **Save**.
4. Access at: `https://altairmurat.github.io/multivar-grapher/`

---

## 💻 Run Locally

```bash
python main.py
```
Open [http://localhost:8000/index.html](http://localhost:8000/index.html) in your browser.
