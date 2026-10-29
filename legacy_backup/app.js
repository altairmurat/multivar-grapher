tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#f5f3ff',
              100: '#ede9fe',
              200: '#ddd6fe',
              300: '#c4b5fd',
              400: '#a78bfa',
              500: '#8b5cf6',
              600: '#7c3aed',
              700: '#6d28d9',
              800: '#5b21b6',
              900: '#4c1d95',
              950: '#2e1065'
            }
          }
        }
      }
    }

lucide.createIcons();

    // -------------------------------------------------------------------------
    // Application State
    // -------------------------------------------------------------------------
    const state = {
      theme: 'light', // 'light' (Purple-White Modern) or 'dark'
      view_mode: '2d',
      notation: 'x1x2',
      drag_mode: 'pan',
      f_expr_raw: "x1^2 + x2^2",
      params: {
        a: { val: 1.0, min: -5.0, max: 5.0, step: 0.1 },
        b: { val: 1.0, min: -5.0, max: 5.0, step: 0.1 },
        c: { val: 1.0, min: -5.0, max: 5.0, step: 0.1 },
        d: { val: 1.0, min: -5.0, max: 5.0, step: 0.1 }
      },
      t: 0.0,
      animating_t: false,
      animation_id: null,
      level_c: 4.0,
      radius_r: 2.0,
      x0: 2.0,
      y0: 0.0,
      z0: 0.0,
      dim: 2,
      test_x: 2.1,
      test_y: 0.2,
      x_range: [-6, 6],
      y_range: [-6, 6],
      grid_res: 50,
      color_scale: "Turbo",
      opacity: 0.95,
      show_gradient: true,
      show_tangent_line: true,
      show_normal_line: true,
      show_3d_normal_line: true,
      show_affine_plane: true,
      show_right_angle: true,
      show_all_contours: true,
      show_matrix_arrows: false,
      show_approx_arrow: false,
      show_3d_tangent_basis: false,
      show_error_rod: false,
      is_vector_func: false,
      is_matrix_input: false,
      f1_expr_raw: '',
      f2_expr_raw: '',
      f3_expr_raw: '',
      constraint_raw: '',
      show_constraint_surface: true,
      show_constraint_curve: true,
      is_orbiting: false,
      is_slicing: false
    };

    const presets = {
      circle_example: {
        expr: "x1^2 + x2^2",
        constraint: "",
        c: 4.0, r: 2.0, x0: 2.0, y0: 0.0, z0: 0.0,
        x: [-6, 6], y: [-6, 6], mode: '2d'
      },
      ellipse: {
        expr: "x1^2 / 4 + x2^2 / 9",
        constraint: "",
        c: 1.0, r: 1.0, x0: 1.0, y0: 1.5, z0: 0.0,
        x: [-6, 6], y: [-6, 6], mode: 'split'
      },
      saddle: {
        expr: "x1^2 - x2^2",
        constraint: "",
        c: 1.0, r: 1.0, x0: 1.414, y0: 1.0, z0: 0.0,
        x: [-5, 5], y: [-5, 5], mode: 'split'
      },
      r3_matrix: {
        expr: "[1, 2, 3; 4, 5, 6; 7, 8, 9]",
        constraint: "",
        c: 1.0, r: 1.0, x0: 1.0, y0: 1.0, z0: 1.0,
        x: [-5, 5], y: [-5, 5], mode: 'split'
      },
      r3_vector: {
        expr: "[x1; x2; x3]",
        constraint: "",
        c: 1.0, r: 1.0, x0: 1.0, y0: 2.0, z0: 1.0,
        x: [-5, 5], y: [-5, 5], mode: 'split'
      },
      r3_sphere: {
        expr: "x1^2 + x2^2 + x3^2",
        constraint: "",
        c: 4.0, r: 2.0, x0: 1.0, y0: 1.0, z0: 1.414,
        x: [-5, 5], y: [-5, 5], mode: 'split'
      },
      cylindrical_parabola: {
        expr: "[x1; x2; x3]",
        constraint: "x1^2/4 + x2 = 1",
        c: 1.0, r: 1.0, x0: 0.0, y0: 1.0, z0: 0.0,
        x: [-5, 5], y: [-5, 5], mode: 'split'
      },
      cylindrical_ellipse: {
        expr: "[x1; x2; x3]",
        constraint: "x1^2 / 4 + x2^2 / 9 = 1",
        c: 1.0, r: 1.0, x0: 2.0, y0: 0.0, z0: 0.0,
        x: [-5, 5], y: [-5, 5], mode: 'split'
      },
      lagrange_opt: {
        expr: "x1^2 + x2^2",
        constraint: "x1 + 2*x2 = 4",
        c: 4.0, r: 2.0, x0: 0.8, y0: 1.6, z0: 0.0,
        x: [-5, 5], y: [-5, 5], mode: 'split'
      },
      vector_field: {
        expr: "[-x2, x1]",
        c: 2.0, r: 1.414, x0: 1.0, y0: 1.0, z0: 0.0,
        x: [-5, 5], y: [-5, 5], mode: 'split'
      },
      ripple: {
        expr: "sin(sqrt(x1^2 + x2^2) * 2) / (sqrt(x1^2 + x2^2) + 0.1)",
        c: 0.5, r: 1.0, x0: 1.2, y0: 0.8, z0: 0.0,
        x: [-6, 6], y: [-6, 6], mode: 'split'
      },
      gaussian: {
        expr: "3 * exp(-(x1^2 + x2^2) / 4)",
        c: 1.5, r: 1.66, x0: 1.18, y0: 1.18, z0: 0.0,
        x: [-5, 5], y: [-5, 5], mode: 'split'
      },
      egg_carton: {
        expr: "sin(x1) * cos(x2)",
        c: 0.5, r: 1.0, x0: 0.78, y0: 0.61, z0: 0.0,
        x: [-5, 5], y: [-5, 5], mode: '2d'
      },
      rosenbrock: {
        expr: "(1 - x1)^2 + 10 * (x2 - x1^2)^2",
        c: 5.0, r: 1.0, x0: 1.0, y0: 1.5, z0: 0.0,
        x: [-3, 3], y: [-2, 4], mode: 'split'
      },
      sombrero: {
        expr: "cos(2 * sqrt(x1^2 + x2^2) - t) / (sqrt(x1^2 + x2^2) + 0.5)",
        c: 0.5, r: 1.0, x0: 1.5, y0: 0.5, z0: 0.0,
        x: [-6, 6], y: [-6, 6], mode: 'split'
      }
    };

    let compiledF = null;
    let compiledF1 = null;
    let compiledF2 = null;
    let compiledF3 = null;
    let compiledCells = null;
    let symDfD1 = null;
    let symDfD2 = null;
    let symDfD3 = null;
    let symH11 = null, symH12 = null, symH13 = null;
    let symH21 = null, symH22 = null, symH23 = null;
    let symH31 = null, symH32 = null, symH33 = null;
    let symJacobian = null;
    let parsedMatrixData = null;
    let compiledConstraint = null;
    let constraintInfo = {
      active: false,
      raw: "",
      op: "=",
      isInequality: false,
      isCylinderX3: false,
      hasX3: false,
      polylines: []
    };

    function parseMatrixOrVector(exprStr) {
      if (!exprStr) return { isMatrix: false, isVector: false };
      const trimmed = exprStr.trim();
      if (!trimmed.startsWith('[') || !trimmed.endsWith(']')) {
        return { isMatrix: false, isVector: false };
      }

      const inner = trimmed.slice(1, -1).trim();
      if (!inner) return { isMatrix: false, isVector: false };

      let rawRows = [];
      if (inner.startsWith('[')) {
        let depth = 0;
        let cur = "";
        for (let i = 0; i < inner.length; i++) {
          const ch = inner[i];
          if (ch === '[') {
            if (depth === 0) cur = "";
            depth++;
          } else if (ch === ']') {
            depth--;
            if (depth === 0) {
              rawRows.push(cur.trim());
              cur = "";
            }
          } else if (depth > 0) {
            cur += ch;
          }
        }
      } else {
        let depth = 0;
        let cur = "";
        for (let i = 0; i < inner.length; i++) {
          const ch = inner[i];
          if (ch === '(' || ch === '[' || ch === '{') depth++;
          else if (ch === ')' || ch === ']' || ch === '}') depth--;

          if (ch === ';' && depth === 0) {
            rawRows.push(cur.trim());
            cur = "";
          } else {
            cur += ch;
          }
        }
        if (cur.trim()) rawRows.push(cur.trim());
      }

      if (rawRows.length === 0) return { isMatrix: false, isVector: false };

      const matrix = [];
      for (const rowStr of rawRows) {
        const cols = [];
        let depth = 0;
        let cur = "";
        for (let i = 0; i < rowStr.length; i++) {
          const ch = rowStr[i];
          if (ch === '(' || ch === '[' || ch === '{') depth++;
          else if (ch === ')' || ch === ']' || ch === '}') depth--;

          if (ch === ',' && depth === 0) {
            cols.push(cur.trim());
            cur = "";
          } else {
            cur += ch;
          }
        }
        if (cur.trim()) cols.push(cur.trim());
        if (cols.length > 0) matrix.push(cols);
      }

      if (matrix.length === 0) return { isMatrix: false, isVector: false };

      const numRows = matrix.length;
      const numCols = Math.max(...matrix.map(r => r.length));

      for (const r of matrix) {
        while (r.length < numCols) r.push("0");
      }

      const isVector = (numCols === 1 && numRows >= 2) || (numRows === 1 && numCols >= 2);

      return {
        isMatrix: true,
        isVector,
        numRows,
        numCols,
        matrix,
        f1_raw: matrix[0] ? matrix[0][0] : '',
        f2_raw: numRows >= 2 ? (matrix[1] ? matrix[1][0] : '') : (matrix[0] && matrix[0][1] ? matrix[0][1] : ''),
        f3_raw: numRows >= 3 ? (matrix[2] ? matrix[2][0] : '') : (matrix[0] && matrix[0][2] ? matrix[0][2] : '')
      };
    }

    function parseVectorComponents(exprStr) {
      return parseMatrixOrVector(exprStr);
    }

    // -------------------------------------------------------------------------
    // Marching Squares 2D Contour Extractor & Constraint Engine
    // -------------------------------------------------------------------------
    function extractContourLines(evalFunc, xRange, yRange, nx = 75, ny = 75) {
      const xMin = Math.min(xRange[0], xRange[1]);
      const xMax = Math.max(xRange[0], xRange[1]);
      const yMin = Math.min(yRange[0], yRange[1]);
      const yMax = Math.max(yRange[0], yRange[1]);
      const dx = (xMax - xMin) / (nx - 1);
      const dy = (yMax - yMin) / (ny - 1);

      const grid = [];
      for (let j = 0; j < ny; j++) {
        const row = new Float64Array(nx);
        const y = yMin + j * dy;
        for (let i = 0; i < nx; i++) {
          const x = xMin + i * dx;
          row[i] = evalFunc(x, y);
        }
        grid.push(row);
      }

      function interp(x1, y1, v1, x2, y2, v2) {
        if (Math.abs(v2 - v1) < 1e-12) return [(x1 + x2) / 2, (y1 + y2) / 2];
        const t = Math.max(0, Math.min(1, -v1 / (v2 - v1)));
        return [x1 + t * (x2 - x1), y1 + t * (y2 - y1)];
      }

      const segments = [];
      for (let j = 0; j < ny - 1; j++) {
        const y0 = yMin + j * dy;
        const y1 = y0 + dy;
        for (let i = 0; i < nx - 1; i++) {
          const x0 = xMin + i * dx;
          const x1 = x0 + dx;

          const vTL = grid[j + 1][i];
          const vTR = grid[j + 1][i + 1];
          const vBR = grid[j][i + 1];
          const vBL = grid[j][i];

          let mask = 0;
          if (vTL > 0) mask |= 1;
          if (vTR > 0) mask |= 2;
          if (vBR > 0) mask |= 4;
          if (vBL > 0) mask |= 8;

          if (mask === 0 || mask === 15) continue;

          const pTop = (mask & 3) === 1 || (mask & 3) === 2 ? interp(x0, y1, vTL, x1, y1, vTR) : null;
          const pRight = (mask & 6) === 2 || (mask & 6) === 4 ? interp(x1, y1, vTR, x1, y0, vBR) : null;
          const pBottom = (mask & 12) === 4 || (mask & 12) === 8 ? interp(x1, y0, vBR, x0, y0, vBL) : null;
          const pLeft = (mask & 9) === 8 || (mask & 9) === 1 ? interp(x0, y0, vBL, x0, y1, vTL) : null;

          if (mask === 1 || mask === 14) segments.push([pLeft, pTop]);
          else if (mask === 2 || mask === 13) segments.push([pTop, pRight]);
          else if (mask === 3 || mask === 12) segments.push([pLeft, pRight]);
          else if (mask === 4 || mask === 11) segments.push([pRight, pBottom]);
          else if (mask === 5) { segments.push([pLeft, pTop]); segments.push([pRight, pBottom]); }
          else if (mask === 6 || mask === 9) segments.push([pTop, pBottom]);
          else if (mask === 7 || mask === 8) segments.push([pLeft, pBottom]);
          else if (mask === 10) { segments.push([pTop, pRight]); segments.push([pLeft, pBottom]); }
        }
      }

      const used = new Uint8Array(segments.length);
      const tolSq = (dx * dx + dy * dy) * 2.5;
      const polylines = [];

      for (let s = 0; s < segments.length; s++) {
        if (used[s]) continue;
        used[s] = 1;
        const poly = [segments[s][0], segments[s][1]];
        let extended = true;

        while (extended) {
          extended = false;
          const head = poly[0];
          const tail = poly[poly.length - 1];

          for (let k = 0; k < segments.length; k++) {
            if (used[k]) continue;
            const pA = segments[k][0];
            const pB = segments[k][1];

            if ((tail[0] - pA[0]) ** 2 + (tail[1] - pA[1]) ** 2 <= tolSq) {
              poly.push(pB); used[k] = 1; extended = true; break;
            } else if ((tail[0] - pB[0]) ** 2 + (tail[1] - pB[1]) ** 2 <= tolSq) {
              poly.push(pA); used[k] = 1; extended = true; break;
            } else if ((head[0] - pA[0]) ** 2 + (head[0] - pA[0]) ** 2 <= tolSq) {
              poly.unshift(pB); used[k] = 1; extended = true; break;
            } else if ((head[0] - pB[0]) ** 2 + (head[1] - pB[1]) ** 2 <= tolSq) {
              poly.unshift(pA); used[k] = 1; extended = true; break;
            }
          }
        }
        if (poly.length >= 3) {
          polylines.push(poly);
        }
      }

      // Merge polylines whose endpoints meet
      let merged = true;
      while (merged) {
        merged = false;
        for (let i = 0; i < polylines.length; i++) {
          const p1 = polylines[i];
          const p1Head = p1[0];
          const p1Tail = p1[p1.length - 1];
          for (let j = i + 1; j < polylines.length; j++) {
            const p2 = polylines[j];
            const p2Head = p2[0];
            const p2Tail = p2[p2.length - 1];

            if ((p1Tail[0] - p2Head[0]) ** 2 + (p1Tail[1] - p2Head[1]) ** 2 <= tolSq * 4) {
              p1.push(...p2); polylines.splice(j, 1); merged = true; break;
            } else if ((p1Tail[0] - p2Tail[0]) ** 2 + (p1Tail[1] - p2Tail[1]) ** 2 <= tolSq * 4) {
              p1.push(...p2.slice().reverse()); polylines.splice(j, 1); merged = true; break;
            } else if ((p1Head[0] - p2Tail[0]) ** 2 + (p1Head[1] - p2Tail[1]) ** 2 <= tolSq * 4) {
              p1.unshift(...p2); polylines.splice(j, 1); merged = true; break;
            } else if ((p1Head[0] - p2Head[0]) ** 2 + (p1Head[1] - p2Head[1]) ** 2 <= tolSq * 4) {
              p1.unshift(...p2.slice().reverse()); polylines.splice(j, 1); merged = true; break;
            }
          }
          if (merged) break;
        }
      }

      // If curve is closed loop, ensure smooth closure
      polylines.forEach(p => {
        if ((p[0][0] - p[p.length - 1][0]) ** 2 + (p[0][1] - p[p.length - 1][1]) ** 2 <= tolSq * 4) {
          p.push([p[0][0], p[0][1]]);
        }
      });

      return polylines;
    }

    function compileConstraint() {
      const statusEl = document.getElementById("constraintStatus");
      const badgeTab1 = document.getElementById("tab1ConstraintBadge");
      const badgeTab1Text = document.getElementById("tab1ConstraintText");
      const raw = (state.constraint_raw || "").trim();

      if (!raw) {
        constraintInfo = { active: false, raw: "", op: "=", isInequality: false, isCylinderX3: false, hasX3: false, polylines: [] };
        if (statusEl) {
          statusEl.textContent = "Optional (Inactive)";
          statusEl.className = "text-[10px] px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 border border-slate-300 dark:border-slate-700 font-medium";
        }
        if (badgeTab1) badgeTab1.classList.add("hidden");
        return;
      }

      // Detect operator
      let op = "=";
      let lhs = raw;
      let rhs = "0";

      if (raw.includes("<=")) { op = "<="; const p = raw.split("<="); lhs = p[0]; rhs = p[1]; }
      else if (raw.includes(">=")) { op = ">="; const p = raw.split(">="); lhs = p[0]; rhs = p[1]; }
      else if (raw.includes("<")) { op = "<"; const p = raw.split("<"); lhs = p[0]; rhs = p[1]; }
      else if (raw.includes(">")) { op = ">"; const p = raw.split(">"); lhs = p[0]; rhs = p[1]; }
      else if (raw.includes("==")) { op = "="; const p = raw.split("=="); lhs = p[0]; rhs = p[1]; }
      else if (raw.includes("=")) { op = "="; const p = raw.split("="); lhs = p[0]; rhs = p[1]; }

      const diffStr = `(${lhs.trim()}) - (${rhs.trim()})`;
      let compiledDiff = null;

      try {
        compiledDiff = math.compile(diffStr);
      } catch (err) {
        if (statusEl) {
          statusEl.textContent = "Syntax Error";
          statusEl.className = "text-[10px] px-2 py-0.5 rounded-full bg-rose-100 dark:bg-rose-900/50 text-rose-700 dark:text-rose-300 border border-rose-300 dark:border-rose-700 font-medium";
        }
        constraintInfo = { active: false, raw, op, isInequality: false, isCylinderX3: false, hasX3: false, polylines: [] };
        if (badgeTab1) badgeTab1.classList.add("hidden");
        return;
      }

      const hasX3 = raw.includes("x3") || raw.includes("z");
      const isInequality = ["<=", ">=", "<", ">"].includes(op);
      const isCylinderX3 = !hasX3 && !isInequality;

      constraintInfo = {
        active: true,
        raw,
        op,
        diffStr,
        compiledDiff,
        isInequality,
        isCylinderX3,
        hasX3,
        polylines: []
      };

      if (statusEl) {
        if (isCylinderX3) {
          statusEl.textContent = "Active: 3D Cylinder (x₃ free)";
          statusEl.className = "text-[10px] px-2 py-0.5 rounded-full bg-indigo-100 dark:bg-indigo-900/60 text-indigo-700 dark:text-cyan-300 border border-indigo-300 dark:border-indigo-700 font-bold";
        } else if (isInequality) {
          statusEl.textContent = "Active: Domain Restriction";
          statusEl.className = "text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/60 text-emerald-700 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-700 font-bold";
        } else {
          statusEl.textContent = "Active: 3D Constraint";
          statusEl.className = "text-[10px] px-2 py-0.5 rounded-full bg-violet-100 dark:bg-purple-900/60 text-violet-700 dark:text-purple-300 border border-violet-300 dark:border-purple-700 font-bold";
        }
      }

      if (badgeTab1 && badgeTab1Text) {
        badgeTab1Text.textContent = raw;
        badgeTab1.classList.remove("hidden");
      }

      // Extract 2D polylines for the constraint curve g(x1, x2) = 0
      try {
        const evalDiff = (xVal, yVal) => {
          const sc = getEvalScope(xVal, yVal, 0);
          try {
            const v = Number(compiledDiff.evaluate(sc));
            return isFinite(v) ? v : 0;
          } catch {
            return 0;
          }
        };

        const polylines = extractContourLines(evalDiff, state.x_range, state.y_range, 75, 75);
        constraintInfo.polylines = polylines;
      } catch (err) {
        console.warn("Could not extract constraint contour polylines:", err);
      }
    }

    let isInternalUpdating = false;
    let relayoutDebounce = null;

    // -------------------------------------------------------------------------
    // Theme Management (Light Modern Purple-White <-> Dark Mode)
    // -------------------------------------------------------------------------
    function initTheme() {
      const saved = localStorage.getItem('multivar_theme');
      if (saved) {
        state.theme = saved;
      } else {
        state.theme = 'light'; // Default to beautiful purple-white
      }
      applyTheme();
    }

    function toggleTheme() {
      state.theme = state.theme === 'light' ? 'dark' : 'light';
      localStorage.setItem('multivar_theme', state.theme);
      applyTheme();
      renderPlots(true);
    }

    function applyTheme() {
      const html = document.documentElement;
      if (state.theme === 'dark') {
        html.classList.add('dark');
        html.classList.remove('light');
      } else {
        html.classList.remove('dark');
        html.classList.add('light');
      }
    }

    // -------------------------------------------------------------------------
    // URL Hash State Persistence & Sharing
    // -------------------------------------------------------------------------
    function loadStateFromHash() {
      try {
        const hash = window.location.hash;
        if (!hash || hash.length <= 1) return false;
        let raw = hash.startsWith('#') ? hash.slice(1) : hash;
        if (!raw) return false;

        let jsonStr = raw;
        try {
          jsonStr = decodeURIComponent(raw);
        } catch (e) {
          jsonStr = raw;
        }

        const data = JSON.parse(jsonStr);
        if (!data || typeof data !== 'object') return false;

        // Function expression
        if (data.f) {
          state.f_expr_raw = String(data.f);
          const fInp = document.getElementById("functionInput");
          if (fInp) fInp.value = state.f_expr_raw;
        }

        // Level set c and radius r
        if (data.c !== undefined && !isNaN(Number(data.c))) {
          state.level_c = parseFloat(data.c);
          const cVal = document.getElementById("levelValueC");
          const cSld = document.getElementById("levelSliderC");
          if (cVal) cVal.value = state.level_c.toFixed(1);
          if (cSld) cSld.value = state.level_c;
        }
        if (data.r !== undefined && !isNaN(Number(data.r))) {
          state.radius_r = parseFloat(data.r);
          const rVal = document.getElementById("radiusInputR");
          if (rVal) rVal.value = state.radius_r.toFixed(2);
        }

        // Evaluation point a (x0, y0)
        if (data.x0 !== undefined && !isNaN(Number(data.x0))) {
          state.x0 = parseFloat(data.x0);
          const x0Inp = document.getElementById("x0Input");
          const x0Sld = document.getElementById("x0Slider");
          if (x0Inp) x0Inp.value = state.x0.toFixed(2);
          if (x0Sld) x0Sld.value = state.x0;
        }
        if (data.y0 !== undefined && !isNaN(Number(data.y0))) {
          state.y0 = parseFloat(data.y0);
          const y0Inp = document.getElementById("y0Input");
          const y0Sld = document.getElementById("y0Slider");
          if (y0Inp) y0Inp.value = state.y0.toFixed(2);
          if (y0Sld) y0Sld.value = state.y0;
        }
        if (data.z0 !== undefined && !isNaN(Number(data.z0))) {
          state.z0 = parseFloat(data.z0);
          const z0Inp = document.getElementById("z0Input");
          const z0Sld = document.getElementById("z0Slider");
          if (z0Inp) z0Inp.value = state.z0.toFixed(2);
          if (z0Sld) z0Sld.value = state.z0;
        }

        // Constraint / requirement
        if (data.constraint !== undefined) {
          state.constraint_raw = String(data.constraint);
          const cInp = document.getElementById("constraintInput");
          if (cInp) cInp.value = state.constraint_raw;
        }

        // View mode (2d, 3d, split)
        if (data.mode && ['2d', '3d', 'split'].includes(data.mode)) {
          state.view_mode = data.mode;
        }

        // Domain range
        if (Array.isArray(data.xr) && data.xr.length === 2) {
          state.x_range = [parseFloat(data.xr[0]), parseFloat(data.xr[1])];
        }
        if (Array.isArray(data.yr) && data.yr.length === 2) {
          state.y_range = [parseFloat(data.yr[0]), parseFloat(data.yr[1])];
        }

        // Theme
        if (data.theme && (data.theme === 'dark' || data.theme === 'light')) {
          state.theme = data.theme;
          applyTheme();
        }

        // Notation (x1x2 vs xy)
        if (data.notation && ['x1x2', 'xy'].includes(data.notation)) {
          state.notation = data.notation;
          const nXY = document.getElementById('notationXY');
          const nX1X2 = document.getElementById('notationX1X2');
          if (state.notation === 'xy' && nXY) {
            nXY.click();
          } else if (nX1X2) {
            nX1X2.click();
          }
        }

        // Parameters (a, b, c, d)
        if (data.params && typeof data.params === 'object') {
          ['a', 'b', 'c', 'd'].forEach(p => {
            if (data.params[p] !== undefined && state.params[p]) {
              const val = parseFloat(data.params[p]);
              state.params[p].val = val;
              const valEl = document.getElementById(`param_${p}_val`);
              const sldEl = document.getElementById(`param_${p}_slider`);
              if (valEl) valEl.textContent = val.toFixed(1);
              if (sldEl) sldEl.value = val;
            }
          });
        }

        // Geometric Toggles
        if (data.toggles && typeof data.toggles === 'object') {
          const t = data.toggles;
          if (t.norm !== undefined) { state.show_normal_line = Boolean(t.norm); const el = document.getElementById('showNormalLine'); if (el) el.checked = state.show_normal_line; }
          if (t.tang !== undefined) { state.show_tangent_line = Boolean(t.tang); const el = document.getElementById('showTangentLine'); if (el) el.checked = state.show_tangent_line; }
          if (t.grad !== undefined) { state.show_gradient = Boolean(t.grad); const el = document.getElementById('showGradientVector'); if (el) el.checked = state.show_gradient; }
          if (t.norm3d !== undefined) { state.show_3d_normal_line = Boolean(t.norm3d); const el = document.getElementById('show3DNormalLine'); if (el) el.checked = state.show_3d_normal_line; }
          if (t.affine !== undefined) { state.show_affine_plane = Boolean(t.affine); const el = document.getElementById('showAffinePlane'); if (el) el.checked = state.show_affine_plane; }
          if (t.angle !== undefined) { state.show_right_angle = Boolean(t.angle); const el = document.getElementById('showRightAngleMarker'); if (el) el.checked = state.show_right_angle; }
          if (t.contours !== undefined) { state.show_all_contours = Boolean(t.contours); const el = document.getElementById('showAllContourLines'); if (el) el.checked = state.show_all_contours; }
        }

        return true;
      } catch (err) {
        console.warn("Could not load state from URL hash:", err);
        return false;
      }
    }

    // -------------------------------------------------------------------------
    // Math Compilation & Differentiation
    // -------------------------------------------------------------------------
    function compileExpressions() {
      compileConstraint();
      const formulaStatus = document.getElementById("formulaStatus");
      const expr = state.f_expr_raw;

      const matInfo = parseMatrixOrVector(expr);

      if (matInfo.isMatrix) {
        state.is_matrix_input = true;
        state.is_vector_func = matInfo.isVector;
        parsedMatrixData = matInfo;
        const numRows = matInfo.numRows;
        const numCols = matInfo.numCols;

        // Check if any cell has 3D variables or if dimension >= 3
        let hasX3 = false;
        matInfo.matrix.forEach(row => {
          row.forEach(cellStr => {
            if (cellStr.includes('x3') || cellStr.includes('z')) hasX3 = true;
          });
        });
        if (numRows >= 3 || numCols >= 3 || hasX3) {
          state.dim = 3;
        } else {
          state.dim = 2;
        }

        try {
          compiledCells = matInfo.matrix.map(row =>
            row.map(cellStr => {
              try { return math.compile(cellStr); } catch { return math.compile("0"); }
            })
          );

          if (matInfo.isVector) {
            state.f1_expr_raw = matInfo.f1_raw;
            state.f2_expr_raw = matInfo.f2_raw;
            state.f3_expr_raw = matInfo.f3_raw;

            compiledF = {
              evaluate: (scope) => {
                let sumSq = 0;
                for (let r = 0; r < numRows; r++) {
                  for (let c = 0; c < numCols; c++) {
                    const v = Number(compiledCells[r][c].evaluate(scope)) || 0;
                    sumSq += v * v;
                  }
                }
                return Math.sqrt(sumSq);
              }
            };
            formulaStatus.textContent = state.dim === 3 ? `Vector F in ℝ³ [${numRows}×${numCols}]` : `Vector F in ℝ² [${numRows}×${numCols}]`;
          } else {
            compiledF = {
              evaluate: (scope) => {
                const c00 = Number(compiledCells[0][0].evaluate(scope)) || 0;
                const c01 = (numCols >= 2) ? (Number(compiledCells[0][1].evaluate(scope)) || 0) : 0;
                return c00 * (scope.x1 || 0) + c01 * (scope.x2 || 0);
              }
            };
            formulaStatus.textContent = `Matrix [${numRows}×${numCols}] in ℝ${state.dim}`;
          }
          formulaStatus.className = "text-[11px] px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-500/20 text-emerald-700 dark:text-emerald-400 border border-emerald-300 dark:border-emerald-500/30 font-medium";
        } catch (err) {
          formulaStatus.textContent = "Syntax Error";
          formulaStatus.className = "text-[11px] px-2 py-0.5 rounded-full bg-rose-100 dark:bg-rose-500/20 text-rose-700 dark:text-rose-400 border border-rose-300 dark:border-rose-500/30 font-medium";
        }

        // Symbolic Matrix or Jacobian calculation
        try {
          const varNames = state.notation === 'x1x2' 
            ? (state.dim === 3 ? ['x_1', 'x_2', 'x_3'] : ['x_1', 'x_2'])
            : (state.dim === 3 ? ['x', 'y', 'z'] : ['x', 'y']);
          const diffVars = state.notation === 'x1x2'
            ? (state.dim === 3 ? ['x1', 'x2', 'x3'] : ['x1', 'x2'])
            : (state.dim === 3 ? ['x', 'y', 'z'] : ['x', 'y']);

          if (matInfo.isVector && (numRows >= 2 || numCols >= 2)) {
            const components = [];
            for (let r = 0; r < numRows; r++) {
              for (let c = 0; c < numCols; c++) {
                components.push(matInfo.matrix[r][c]);
              }
            }
            const n = state.dim;

            symJacobian = [];
            let texRows = [];
            for (let i = 0; i < components.length; i++) {
              const compParsed = math.parse(components[i]);
              const rowDerivs = [];
              const rowTex = [];
              for (let j = 0; j < n; j++) {
                try {
                  const d = math.derivative(compParsed, diffVars[j]);
                  rowDerivs.push(d);
                  rowTex.push(d.toTex({ parenthesis: 'auto' }));
                } catch {
                  rowDerivs.push(null);
                  rowTex.push(`\\frac{\\partial F_${i+1}}{\\partial ${varNames[j]}}`);
                }
              }
              symJacobian.push(rowDerivs);
              texRows.push(rowTex.join(' & '));
            }

            const jacobianLatex = `\\mathbf{J}_F(${varNames.join(', ')}) = \\begin{bmatrix} ${texRows.join(' \\\\[4pt] ')} \\end{bmatrix}_{${components.length} \\times ${n}}`;
            katex.render(jacobianLatex, document.getElementById("katexMatrixSymbolic"), { throwOnError: false });

            if (symJacobian[0]) {
              const t0 = symJacobian[0].map(d => d ? d.toTex({ parenthesis: 'auto' }) : '0').join(', ');
              katex.render(`\\mathbf{D}F_1 = [${t0}]`, document.getElementById("katexDfDx"), { throwOnError: false });
            }
            if (symJacobian[1]) {
              const t1 = symJacobian[1].map(d => d ? d.toTex({ parenthesis: 'auto' }) : '0').join(', ');
              katex.render(`\\mathbf{D}F_2 = [${t1}]`, document.getElementById("katexDfDy"), { throwOnError: false });
            }
            if (symJacobian[2] && document.getElementById("katexDfDz")) {
              const t2 = symJacobian[2].map(d => d ? d.toTex({ parenthesis: 'auto' }) : '0').join(', ');
              katex.render(`\\mathbf{D}F_3 = [${t2}]`, document.getElementById("katexDfDz"), { throwOnError: false });
            }
          } else {
            const texRows = matInfo.matrix.map(row => 
              row.map(cell => {
                try { return math.parse(cell).toTex({ parenthesis: 'auto' }); } catch { return cell; }
              }).join(' & ')
            );
            const matLatex = `\\mathbf{M} = \\begin{bmatrix} ${texRows.join(' \\\\[4pt] ')} \\end{bmatrix}_{${numRows} \\times ${numCols}}`;
            katex.render(matLatex, document.getElementById("katexMatrixSymbolic"), { throwOnError: false });
            katex.render(`\\text{Row 1} = [${matInfo.matrix[0].join(', ')}]`, document.getElementById("katexDfDx"), { throwOnError: false });
            if (matInfo.matrix[1]) {
              katex.render(`\\text{Row 2} = [${matInfo.matrix[1].join(', ')}]`, document.getElementById("katexDfDy"), { throwOnError: false });
            }
            if (matInfo.matrix[2] && document.getElementById("katexDfDz")) {
              katex.render(`\\text{Row 3} = [${matInfo.matrix[2].join(', ')}]`, document.getElementById("katexDfDz"), { throwOnError: false });
            }
          }
        } catch (e) {
          document.getElementById("katexMatrixSymbolic").textContent = expr;
        }

      } else {
        state.is_matrix_input = false;
        state.is_vector_func = false;
        parsedMatrixData = null;

        try {
          compiledF = math.compile(expr);
          formulaStatus.textContent = "Valid";
          formulaStatus.className = "text-[11px] px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-500/20 text-emerald-700 dark:text-emerald-400 border border-emerald-300 dark:border-emerald-500/30 font-medium";
        } catch (err) {
          formulaStatus.textContent = "Syntax Error";
          formulaStatus.className = "text-[11px] px-2 py-0.5 rounded-full bg-rose-100 dark:bg-rose-500/20 text-rose-700 dark:text-rose-400 border border-rose-300 dark:border-rose-500/30 font-medium";
          console.warn("Compile error:", err);
        }

        try {
          const parsed = math.parse(expr);
          const vars = new Set();
          parsed.traverse(node => {
            if (node.isSymbolNode) vars.add(node.name);
          });

          if (vars.has('x3') || vars.has('z')) {
            state.dim = 3;
          } else {
            state.dim = 2;
          }

          const v1 = vars.has('x1') ? 'x1' : (vars.has('x') ? 'x' : 'x1');
          const v2 = vars.has('x2') ? 'x2' : (vars.has('y') ? 'y' : 'x2');
          const v3 = vars.has('x3') ? 'x3' : (vars.has('z') ? 'z' : 'x3');

          symDfD1 = math.derivative(parsed, v1);
          symDfD2 = math.derivative(parsed, v2);
          symDfD3 = state.dim === 3 ? math.derivative(parsed, v3) : null;

          const tex1 = symDfD1.toTex({ parenthesis: 'auto' });
          const tex2 = symDfD2.toTex({ parenthesis: 'auto' });
          const tex3 = symDfD3 ? symDfD3.toTex({ parenthesis: 'auto' }) : '0';

          katex.render(tex1, document.getElementById("katexDfDx"), { throwOnError: false });
          katex.render(tex2, document.getElementById("katexDfDy"), { throwOnError: false });
          if (document.getElementById("katexDfDz")) {
            katex.render(tex3, document.getElementById("katexDfDz"), { throwOnError: false });
          }

          const var1Name = state.notation === 'x1x2' ? 'x_1' : 'x';
          const var2Name = state.notation === 'x1x2' ? 'x_2' : 'y';
          const var3Name = state.notation === 'x1x2' ? 'x_3' : 'z';

          if (state.dim === 3) {
            const matrixSymbolicLatex = `\\mathbf{D}f(${var1Name}, ${var2Name}, ${var3Name}) = \\begin{bmatrix} \\frac{\\partial f}{\\partial ${var1Name}} & \\frac{\\partial f}{\\partial ${var2Name}} & \\frac{\\partial f}{\\partial ${var3Name}} \\end{bmatrix} = \\begin{bmatrix} ${tex1} & ${tex2} & ${tex3} \\end{bmatrix}_{1 \\times 3}`;
            katex.render(matrixSymbolicLatex, document.getElementById("katexMatrixSymbolic"), { throwOnError: false });
          } else {
            const matrixSymbolicLatex = `\\mathbf{D}f(${var1Name}, ${var2Name}) = \\begin{bmatrix} \\frac{\\partial f}{\\partial ${var1Name}} & \\frac{\\partial f}{\\partial ${var2Name}} \\end{bmatrix} = \\begin{bmatrix} ${tex1} & ${tex2} \\end{bmatrix}_{1 \\times 2}`;
            katex.render(matrixSymbolicLatex, document.getElementById("katexMatrixSymbolic"), { throwOnError: false });
          }

          symH11 = math.derivative(symDfD1, v1);
          symH12 = math.derivative(symDfD1, v2);
          symH21 = symH12;
          symH22 = math.derivative(symDfD2, v2);

          const h11Tex = symH11.toTex({ parenthesis: 'auto' });
          const h12Tex = symH12.toTex({ parenthesis: 'auto' });
          const h22Tex = symH22.toTex({ parenthesis: 'auto' });

          if (state.dim === 3 && symDfD3) {
            symH13 = math.derivative(symDfD1, v3);
            symH23 = math.derivative(symDfD2, v3);
            symH31 = symH13;
            symH32 = symH23;
            symH33 = math.derivative(symDfD3, v3);

            const h13Tex = symH13.toTex({ parenthesis: 'auto' });
            const h23Tex = symH23.toTex({ parenthesis: 'auto' });
            const h33Tex = symH33.toTex({ parenthesis: 'auto' });

            const hessianSymbolicLatex = `\\mathbf{H}f(${var1Name}, ${var2Name}, ${var3Name}) = \\begin{bmatrix}
              ${h11Tex} & ${h12Tex} & ${h13Tex} \\\\[4pt]
              ${h12Tex} & ${h22Tex} & ${h23Tex} \\\\[4pt]
              ${h13Tex} & ${h23Tex} & ${h33Tex}
            \\end{bmatrix}_{3 \\times 3}`;
            katex.render(hessianSymbolicLatex, document.getElementById("katexHessianSymbolic"), { throwOnError: false });
          } else {
            symH13 = null; symH23 = null; symH31 = null; symH32 = null; symH33 = null;
            const hessianSymbolicLatex = `\\mathbf{H}f(${var1Name}, ${var2Name}) = \\begin{bmatrix}
              \\frac{\\partial^2 f}{\\partial ${var1Name}^2} & \\frac{\\partial^2 f}{\\partial ${var1Name} \\partial ${var2Name}} \\\\[4pt]
              \\frac{\\partial^2 f}{\\partial ${var2Name} \\partial ${var1Name}} & \\frac{\\partial^2 f}{\\partial ${var2Name}^2}
            \\end{bmatrix} = \\begin{bmatrix} ${h11Tex} & ${h12Tex} \\\\[4pt] ${h12Tex} & ${h22Tex} \\end{bmatrix}_{2 \\times 2}`;
            katex.render(hessianSymbolicLatex, document.getElementById("katexHessianSymbolic"), { throwOnError: false });
          }

        } catch (e) {
          symDfD1 = null; symDfD2 = null; symDfD3 = null;
          symH11 = null; symH12 = null; symH22 = null;
          document.getElementById("katexDfDx").textContent = "Numerical derivative";
          document.getElementById("katexDfDy").textContent = "Numerical derivative";
          document.getElementById("katexMatrixSymbolic").textContent = "Df = [ ∂f/∂x₁   ∂f/∂x₂ ]";
          document.getElementById("katexHessianSymbolic").textContent = "Hf = [ ∂²f/∂x₁²  ∂²f/∂x₁∂x₂ ; ∂²f/∂x₂∂x₁  ∂²f/∂x₂² ]";
        }
      }

      // Update dimension UI
      const coordA3Row = document.getElementById("coordA3Row");
      const ptLabel = document.getElementById("pointOfTangencyLabel");
      const dfdx3Card = document.getElementById("dfdx3_card");
      const hessTitle = document.getElementById("hessianTitle");

      if (state.dim === 3) {
        if (coordA3Row) coordA3Row.classList.remove("hidden");
        if (ptLabel) ptLabel.textContent = "Point of Tangency a = (a₁, a₂, a₃)";
        if (dfdx3Card) dfdx3Card.classList.remove("hidden");
        if (hessTitle) hessTitle.textContent = state.is_matrix_input ? "Matrix Properties & Determinant [3 × 3]" : "Hessian Matrix ∇²f / Hf [3 × 3]";
      } else {
        if (coordA3Row) coordA3Row.classList.add("hidden");
        if (ptLabel) ptLabel.textContent = "Point of Tangency a = (a₁, a₂)";
        if (dfdx3Card) dfdx3Card.classList.add("hidden");
        if (hessTitle) hessTitle.textContent = state.is_matrix_input ? "Matrix Properties & Determinant [2 × 2]" : "Hessian Matrix ∇²f / Hf [2 × 2]";
      }

      updateKatexHeader();
      updateCalculusCalculations();
      updateHessianCalculations();
      updateAffineCalculations();
    }

    function updateKatexHeader() {
      const container = document.getElementById("katexEquation");
      if (!container) return;
      const is3D = state.dim === 3;
      const varTuple = state.notation === 'x1x2' 
        ? (is3D ? '(x_1, x_2, x_3)' : '(x_1, x_2)')
        : (is3D ? '(x, y, z)' : '(x, y)');

      let formulaLatex = "";
      if (state.is_matrix_input && parsedMatrixData) {
        const texRows = parsedMatrixData.matrix.map(row => 
          row.map(cell => {
            try { return math.parse(cell).toTex({ parenthesis: 'auto' }); } catch { return cell; }
          }).join(' & ')
        );
        const prefix = state.is_vector_func ? `\\mathbf{F}${varTuple} = ` : `\\mathbf{M} = `;
        formulaLatex = `${prefix}\\begin{bmatrix} ${texRows.join(' \\\\[4pt] ')} \\end{bmatrix}`;
      } else {
        try {
          const parsed = math.parse(state.f_expr_raw);
          const tex = parsed.toTex({ parenthesis: 'auto' });
          formulaLatex = `f${varTuple} = ${tex}`;
        } catch (e) {
          formulaLatex = `f = ${state.f_expr_raw}`;
        }
      }

      if (constraintInfo.active && constraintInfo.raw) {
        const v1 = state.notation === 'x1x2' ? 'x_1' : 'x';
        const v2 = state.notation === 'x1x2' ? 'x_2' : 'y';
        const v3 = state.notation === 'x1x2' ? 'x_3' : 'z';
        let cleanReq = constraintInfo.raw
          .replace(/x1/g, v1).replace(/x2/g, v2).replace(/x3/g, v3);
        formulaLatex += ` \\quad \\left[\\text{s.t. } ${cleanReq}\\right]`;
      }

      katex.render(formulaLatex, container, { throwOnError: false });
    }

    function getEvalScope(xVal, yVal, zVal) {
      const z_val = (zVal !== undefined && zVal !== null) ? zVal : (state.z0 !== undefined ? state.z0 : 0.0);
      const scope = {
        x1: xVal,
        x2: yVal,
        x3: z_val,
        x: xVal,
        y: yVal,
        z: z_val,
        t: state.t
      };
      for (const [k, v] of Object.entries(state.params)) {
        scope[k] = v.val;
      }
      return scope;
    }

    function evaluateAt(xVal, yVal, zVal) {
      const scope = getEvalScope(xVal, yVal, zVal);

      if (state.is_matrix_input && compiledCells && parsedMatrixData) {
        const numRows = parsedMatrixData.numRows;
        const numCols = parsedMatrixData.numCols;
        const evaluatedMatrix = [];
        let sumSq = 0;

        for (let r = 0; r < numRows; r++) {
          const rowVals = [];
          for (let c = 0; c < numCols; c++) {
            let v = 0;
            try {
              v = Number(compiledCells[r][c].evaluate(scope));
              if (isNaN(v)) v = 0;
            } catch { v = 0; }
            rowVals.push(v);
            sumSq += v * v;
          }
          evaluatedMatrix.push(rowVals);
        }

        const z = state.is_vector_func ? Math.sqrt(sumSq) : (evaluatedMatrix[0][0] || 0);
        const f1 = evaluatedMatrix[0] ? evaluatedMatrix[0][0] : 0;
        const f2 = (numRows >= 2 && evaluatedMatrix[1]) ? evaluatedMatrix[1][0] : (evaluatedMatrix[0] && evaluatedMatrix[0][1] ? evaluatedMatrix[0][1] : 0);
        const f3 = (numRows >= 3 && evaluatedMatrix[2]) ? evaluatedMatrix[2][0] : (evaluatedMatrix[0] && evaluatedMatrix[0][2] ? evaluatedMatrix[0][2] : 0);

        const jacobianEval = [];
        if (symJacobian && symJacobian.length > 0) {
          for (let i = 0; i < symJacobian.length; i++) {
            const row = [];
            for (let j = 0; j < symJacobian[i].length; j++) {
              let val = 0;
              try {
                if (symJacobian[i][j]) val = Number(symJacobian[i][j].evaluate(scope));
                if (isNaN(val)) val = 0;
              } catch { val = 0; }
              row.push(val);
            }
            jacobianEval.push(row);
          }
        }

        const j11 = jacobianEval[0] ? jacobianEval[0][0] : (evaluatedMatrix[0] ? evaluatedMatrix[0][0] : 0);
        const j12 = jacobianEval[0] ? (jacobianEval[0][1] || 0) : (evaluatedMatrix[0] ? evaluatedMatrix[0][1] || 0 : 0);
        const j21 = jacobianEval[1] ? jacobianEval[1][0] : (evaluatedMatrix[1] ? evaluatedMatrix[1][0] || 0 : 0);
        const j22 = jacobianEval[1] ? (jacobianEval[1][1] || 0) : (evaluatedMatrix[1] ? evaluatedMatrix[1][1] || 0 : 0);

        return {
          z, f1, f2, f3, fx: f1, fy: f2, fz: f3,
          isVector: state.is_vector_func,
          isMatrix: true,
          evaluatedMatrix,
          jacobianEval,
          j11, j12, j21, j22
        };
      }

      if (!compiledF) return { z: 0, fx: 0, fy: 0, fz: 0, f1: 0, f2: 0, f3: 0, isVector: false, isMatrix: false };

      let z = 0;
      try {
        const rawZ = compiledF.evaluate(scope);
        z = typeof rawZ === 'number' && !isNaN(rawZ) ? rawZ : 0;
      } catch {
        z = 0;
      }

      let fx = null, fy = null, fz = null;
      if (symDfD1 && symDfD2) {
        try {
          fx = Number(symDfD1.evaluate(scope));
          fy = Number(symDfD2.evaluate(scope));
          if (symDfD3) fz = Number(symDfD3.evaluate(scope));
        } catch {
          fx = null; fy = null; fz = null;
        }
      }

      if (fx === null || isNaN(fx) || fy === null || isNaN(fy) || (state.dim === 3 && (fz === null || isNaN(fz)))) {
        const h = 1e-4;
        try {
          const sR = getEvalScope(xVal + h, yVal, zVal);
          const sL = getEvalScope(xVal - h, yVal, zVal);
          const sU = getEvalScope(xVal, yVal + h, zVal);
          const sD = getEvalScope(xVal, yVal - h, zVal);
          fx = (compiledF.evaluate(sR) - compiledF.evaluate(sL)) / (2 * h);
          fy = (compiledF.evaluate(sU) - compiledF.evaluate(sD)) / (2 * h);
          if (state.dim === 3) {
            const z_v = (zVal !== undefined ? zVal : state.z0);
            const sF = getEvalScope(xVal, yVal, z_v + h);
            const sB = getEvalScope(xVal, yVal, z_v - h);
            fz = (compiledF.evaluate(sF) - compiledF.evaluate(sB)) / (2 * h);
          } else {
            fz = 0;
          }
        } catch {
          fx = 0; fy = 0; fz = 0;
        }
      }

      if (typeof fx !== 'number' || isNaN(fx)) fx = 0;
      if (typeof fy !== 'number' || isNaN(fy)) fy = 0;
      if (typeof fz !== 'number' || isNaN(fz)) fz = 0;

      return { z, fx, fy, fz, f1: z, f2: 0, f3: 0, isVector: false, isMatrix: false };
    }

    function evaluateAffineAt(xVal, yVal) {
      const ptA = evaluateAt(state.x0, state.y0, state.z0);
      return ptA.z + ptA.fx * (xVal - state.x0) + ptA.fy * (yVal - state.y0);
    }

    function updateAffineCalculations() {
      const ptA = evaluateAt(state.x0, state.y0, state.z0);
      const var1 = state.notation === 'x1x2' ? 'x_1' : 'x';
      const var2 = state.notation === 'x1x2' ? 'x_2' : 'y';
      const var3 = state.notation === 'x1x2' ? 'x_3' : 'z';

      const vecLatex = `g(\\mathbf{x}) = f(\\mathbf{a}) + \\mathbf{D}f(\\mathbf{a})(\\mathbf{x} - \\mathbf{a}) = f(\\mathbf{a}) + \\nabla f(\\mathbf{a}) \\cdot (\\mathbf{x} - \\mathbf{a})`;
      katex.render(vecLatex, document.getElementById("katexAffineVector"), { throwOnError: false });

      const signA1 = -state.x0 >= 0 ? `+ ${(-state.x0).toFixed(2)}` : `- ${state.x0.toFixed(2)}`;
      const signA2 = -state.y0 >= 0 ? `+ ${(-state.y0).toFixed(2)}` : `- ${state.y0.toFixed(2)}`;
      const signA3 = -state.z0 >= 0 ? `+ ${(-state.z0).toFixed(2)}` : `- ${state.z0.toFixed(2)}`;

      if (state.dim === 3) {
        const affineLatex = `g(${var1}, ${var2}, ${var3}) = ${ptA.z.toFixed(2)} + (${ptA.fx.toFixed(2)})(${var1} ${signA1}) + (${ptA.fy.toFixed(2)})(${var2} ${signA2}) + (${(ptA.fz||0).toFixed(2)})(${var3} ${signA3})`;
        katex.render(affineLatex, document.getElementById("katexAffineFormula"), { throwOnError: false });
        const constTerm = ptA.z - ptA.fx * state.x0 - ptA.fy * state.y0 - (ptA.fz || 0) * state.z0;
        const signConst = constTerm >= 0 ? `+ ${constTerm.toFixed(2)}` : `- ${Math.abs(constTerm).toFixed(2)}`;
        document.getElementById("katexAffineSimplified").textContent = 
          `Simplified: w = ${ptA.fx.toFixed(2)}${var1} + ${ptA.fy.toFixed(2)}${var2} + ${(ptA.fz||0).toFixed(2)}${var3} ${signConst}`;
      } else {
        const affineLatex = `g(${var1}, ${var2}) = ${ptA.z.toFixed(2)} + (${ptA.fx.toFixed(2)})(${var1} ${signA1}) + (${ptA.fy.toFixed(2)})(${var2} ${signA2})`;
        katex.render(affineLatex, document.getElementById("katexAffineFormula"), { throwOnError: false });
        const constTerm = ptA.z - ptA.fx * state.x0 - ptA.fy * state.y0;
        const signConst = constTerm >= 0 ? `+ ${constTerm.toFixed(2)}` : `- ${Math.abs(constTerm).toFixed(2)}`;
        document.getElementById("katexAffineSimplified").textContent = 
          `Simplified: z = ${ptA.fx.toFixed(2)}${var1} + ${ptA.fy.toFixed(2)}${var2} ${signConst}`;
      }

      const testPt = evaluateAt(state.test_x, state.test_y, state.z0);
      const approxVal = evaluateAffineAt(state.test_x, state.test_y);
      const err = Math.abs(testPt.z - approxVal);

      document.getElementById("approxValF").textContent = testPt.z.toFixed(4);
      document.getElementById("approxValG").textContent = approxVal.toFixed(4);
      document.getElementById("approxValErr").textContent = err.toFixed(4);
    }

    function updateCalculusCalculations() {
      const pt = evaluateAt(state.x0, state.y0, state.z0);
      const mag = Math.sqrt(pt.fx * pt.fx + pt.fy * pt.fy + (pt.fz ? pt.fz * pt.fz : 0));

      const var1 = state.notation === 'x1x2' ? 'a₁' : 'x';
      const var2 = state.notation === 'x1x2' ? 'a₂' : 'y';
      const var3 = state.notation === 'x1x2' ? 'a₃' : 'z';

      if (state.dim === 3) {
        document.getElementById("matrixEvalPointLabel").textContent = `(${var1} = ${state.x0.toFixed(2)}, ${var2} = ${state.y0.toFixed(2)}, ${var3} = ${state.z0.toFixed(2)})`;
      } else {
        document.getElementById("matrixEvalPointLabel").textContent = `(${var1} = ${state.x0.toFixed(2)}, ${var2} = ${state.y0.toFixed(2)})`;
      }

      if (pt.isMatrix) {
        const mat = pt.jacobianEval && pt.jacobianEval.length > 0 ? pt.jacobianEval : pt.evaluatedMatrix;
        const numRows = mat.length;
        const numCols = mat[0] ? mat[0].length : 0;
        const texRows = mat.map(row => row.map(v => Number(v).toFixed(3)).join(' & '));
        const prefix = pt.isVector ? `\\mathbf{J}_F(\\mathbf{a}) = ` : `\\mathbf{M}(\\mathbf{a}) = `;
        const matrixNumericLatex = `${prefix}\\begin{bmatrix} ${texRows.join(' \\\\[4pt] ')} \\end{bmatrix}_{${numRows} \\times ${numCols}}`;
        katex.render(matrixNumericLatex, document.getElementById("katexMatrixNumeric"), { throwOnError: false });

        document.getElementById("evalZ0").textContent = pt.isVector 
          ? `||F|| = ${pt.z.toFixed(3)} [${pt.f1.toFixed(2)}, ${pt.f2.toFixed(2)}${state.dim === 3 ? `, ${pt.f3.toFixed(2)}` : ''}]`
          : `M₁₁ = ${pt.f1.toFixed(3)}`;

        document.getElementById("resDfDx").textContent = mat[0] ? mat[0].map(v => Number(v).toFixed(3)).join(', ') : '0.000';
        if (mat[1]) document.getElementById("resDfDy").textContent = mat[1].map(v => Number(v).toFixed(3)).join(', ');
        if (mat[2] && document.getElementById("resDfDz")) document.getElementById("resDfDz").textContent = mat[2].map(v => Number(v).toFixed(3)).join(', ');

        document.getElementById("gradColumnVecDisplay").textContent = pt.isVector 
          ? (state.dim === 3 ? `F(a) = ⟨${pt.f1.toFixed(3)}, ${pt.f2.toFixed(3)}, ${pt.f3.toFixed(3)}⟩ᵀ` : `F(a) = ⟨${pt.f1.toFixed(3)}, ${pt.f2.toFixed(3)}⟩ᵀ`)
          : `Col 1 = ⟨${mat.map(r => Number(r[0]||0).toFixed(2)).join(', ')}⟩ᵀ`;
        document.getElementById("resGradMag").textContent = pt.z.toFixed(4);
      } else {
        if (state.dim === 3) {
          const matrixNumericLatex = `\\mathbf{D}f(\\mathbf{a}) = \\begin{bmatrix} ${pt.fx.toFixed(3)} & ${pt.fy.toFixed(3)} & ${pt.fz.toFixed(3)} \\end{bmatrix}_{1 \\times 3}`;
          katex.render(matrixNumericLatex, document.getElementById("katexMatrixNumeric"), { throwOnError: false });
          document.getElementById("gradColumnVecDisplay").textContent = `⟨${pt.fx.toFixed(3)}, ${pt.fy.toFixed(3)}, ${pt.fz.toFixed(3)}⟩ᵀ`;
          if (document.getElementById("resDfDz")) document.getElementById("resDfDz").textContent = pt.fz.toFixed(4);
        } else {
          const matrixNumericLatex = `\\mathbf{D}f(\\mathbf{a}) = \\begin{bmatrix} ${pt.fx.toFixed(3)} & ${pt.fy.toFixed(3)} \\end{bmatrix}_{1 \\times 2}`;
          katex.render(matrixNumericLatex, document.getElementById("katexMatrixNumeric"), { throwOnError: false });
          document.getElementById("gradColumnVecDisplay").textContent = `⟨${pt.fx.toFixed(3)}, ${pt.fy.toFixed(3)}⟩ᵀ`;
        }

        document.getElementById("evalZ0").textContent = pt.z.toFixed(3);
        document.getElementById("resDfDx").textContent = pt.fx.toFixed(4);
        document.getElementById("resDfDy").textContent = pt.fy.toFixed(4);
        document.getElementById("resGradMag").textContent = mag.toFixed(4);
      }

      if (mag > 1e-4) {
        document.getElementById("resNormalVec").textContent = state.dim === 3
          ? `⟨${(pt.fx / mag).toFixed(3)}, ${(pt.fy / mag).toFixed(3)}, ${(pt.fz / mag).toFixed(3)}⟩`
          : `⟨${(pt.fx / mag).toFixed(3)}, ${(pt.fy / mag).toFixed(3)}⟩`;
        document.getElementById("resTangentVec").textContent = `⟨${(-pt.fy / mag).toFixed(3)}, ${(pt.fx / mag).toFixed(3)}⟩`;
      } else {
        document.getElementById("resNormalVec").textContent = state.dim === 3 ? "⟨0, 0, 0⟩ (Critical pt)" : "⟨0, 0⟩ (Critical pt)";
        document.getElementById("resTangentVec").textContent = "Undefined";
      }

      const diff = Math.abs(pt.z - state.level_c);
      const badge = document.getElementById("levelMatchBadge");
      if (diff < 0.05) {
        badge.textContent = "On Level Set ✓";
        badge.className = "text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-500/20 text-emerald-700 dark:text-emerald-400 border border-emerald-300 dark:border-emerald-500/30 font-sans font-medium";
      } else {
        badge.textContent = `Off Level Set (Δ = ${diff.toFixed(2)})`;
        badge.className = "text-[10px] px-2 py-0.5 rounded-full bg-amber-100 dark:bg-amber-500/20 text-amber-700 dark:text-amber-400 border border-amber-300 dark:border-amber-500/30 font-sans font-medium";
      }

      const signX0 = -state.x0 >= 0 ? `+ ${(-state.x0).toFixed(2)}` : `- ${state.x0.toFixed(2)}`;
      const signY0 = -state.y0 >= 0 ? `+ ${(-state.y0).toFixed(2)}` : `- ${state.y0.toFixed(2)}`;
      const signZ0 = -state.z0 >= 0 ? `+ ${(-state.z0).toFixed(2)}` : `- ${state.z0.toFixed(2)}`;
      const v1Name = state.notation === 'x1x2' ? 'x₁' : 'x';
      const v2Name = state.notation === 'x1x2' ? 'x₂' : 'y';
      const v3Name = state.notation === 'x1x2' ? 'x₃' : 'z';

      if (state.dim === 3) {
        document.getElementById("tangentLineEq").textContent = 
          `${pt.fx.toFixed(2)}(${v1Name} ${signX0}) + ${pt.fy.toFixed(2)}(${v2Name} ${signY0}) + ${(pt.fz||0).toFixed(2)}(${v3Name} ${signZ0}) = 0`;
      } else {
        document.getElementById("tangentLineEq").textContent = 
          `${pt.fx.toFixed(2)}(${v1Name} ${signX0}) + ${pt.fy.toFixed(2)}(${v2Name} ${signY0}) = 0`;
      }

      if (typeof updateAiContextStrip === 'function') {
        updateAiContextStrip();
      }
    }

    function updateHessianCalculations() {
      const scope = getEvalScope(state.x0, state.y0, state.z0);
      const is3D = state.dim === 3;
      const evalPointLabel = document.getElementById("hessianEvalPointLabel");
      const badge = document.getElementById("hessianClassificationBadge");
      const detEl = document.getElementById("resHessianDet");
      const trEl = document.getElementById("resHessianTrace");
      const taylorEl = document.getElementById("katexTaylor2Formula");
      const numMatrixEl = document.getElementById("katexHessianNumeric");

      if (evalPointLabel) {
        evalPointLabel.textContent = is3D 
          ? `a = (${state.x0.toFixed(2)}, ${state.y0.toFixed(2)}, ${state.z0.toFixed(2)})`
          : `a = (${state.x0.toFixed(2)}, ${state.y0.toFixed(2)})`;
      }

      if (state.is_matrix_input && parsedMatrixData) {
        const mat = parsedMatrixData.matrix.map((row, r) => 
          row.map((_, c) => {
            try { return Number(compiledCells[r][c].evaluate(scope)) || 0; } catch { return 0; }
          })
        );
        const nRows = mat.length;
        const nCols = mat[0] ? mat[0].length : 0;
        const texRows = mat.map(row => row.map(v => Number(v).toFixed(3)).join(' & '));
        const numLatex = `\\mathbf{M}(\\mathbf{a}) = \\begin{bmatrix} ${texRows.join(' \\\\[4pt] ')} \\end{bmatrix}_{${nRows} \\times ${nCols}}`;
        katex.render(numLatex, numMatrixEl, { throwOnError: false });

        let det = 0;
        let trace = 0;
        if (nRows === 2 && nCols === 2) {
          det = mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0];
          trace = mat[0][0] + mat[1][1];
        } else if (nRows === 3 && nCols === 3) {
          det = mat[0][0] * (mat[1][1] * mat[2][2] - mat[1][2] * mat[2][1])
              - mat[0][1] * (mat[1][0] * mat[2][2] - mat[1][2] * mat[2][0])
              + mat[0][2] * (mat[1][0] * mat[2][1] - mat[1][1] * mat[2][0]);
          trace = mat[0][0] + mat[1][1] + mat[2][2];
        } else {
          det = 0;
          trace = mat[0][0] || 0;
        }

        if (detEl) detEl.textContent = det.toFixed(4);
        if (trEl) trEl.textContent = trace.toFixed(4);

        if (badge) {
          if (Math.abs(det) > 1e-5) {
            badge.textContent = "Invertible Matrix (det ≠ 0)";
            badge.className = "text-[10px] px-2.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-500/20 text-emerald-700 dark:text-emerald-400 border border-emerald-300 dark:border-emerald-500/30 font-bold";
          } else {
            badge.textContent = "Singular Matrix (det = 0)";
            badge.className = "text-[10px] px-2.5 py-0.5 rounded-full bg-amber-100 dark:bg-amber-500/20 text-amber-700 dark:text-amber-400 border border-amber-300 dark:border-amber-500/30 font-bold";
          }
        }

        if (taylorEl) {
          taylorEl.textContent = `det(M) = ${det.toFixed(4)}, Tr(M) = ${trace.toFixed(4)}`;
        }
        return;
      }

      let h11 = 0, h12 = 0, h22 = 0;
      let h13 = 0, h23 = 0, h33 = 0;

      if (symH11 && symH12 && symH22) {
        try {
          h11 = Number(symH11.evaluate(scope)) || 0;
          h12 = Number(symH12.evaluate(scope)) || 0;
          h22 = Number(symH22.evaluate(scope)) || 0;
          if (is3D && symH33) {
            h13 = Number(symH13 ? symH13.evaluate(scope) : 0) || 0;
            h23 = Number(symH23 ? symH23.evaluate(scope) : 0) || 0;
            h33 = Number(symH33.evaluate(scope)) || 0;
          }
        } catch {
          h11 = null;
        }
      }

      if (h11 === null || isNaN(h11) || isNaN(h12) || isNaN(h22)) {
        const h = 1e-3;
        const x = state.x0, y = state.y0, z = state.z0;
        const f0 = evaluateAt(x, y, z).z;
        const fXp = evaluateAt(x + h, y, z).z;
        const fXm = evaluateAt(x - h, y, z).z;
        const fYp = evaluateAt(x, y + h, z).z;
        const fYm = evaluateAt(x, y - h, z).z;
        const fXpYp = evaluateAt(x + h, y + h, z).z;
        const fXpYm = evaluateAt(x + h, y - h, z).z;
        const fXmYp = evaluateAt(x - h, y + h, z).z;
        const fXmYm = evaluateAt(x - h, y - h, z).z;

        h11 = (fXp - 2 * f0 + fXm) / (h * h);
        h22 = (fYp - 2 * f0 + fYm) / (h * h);
        h12 = (fXpYp - fXpYm - fXmYp + fXmYm) / (4 * h * h);

        if (is3D) {
          const fZp = evaluateAt(x, y, z + h).z;
          const fZm = evaluateAt(x, y, z - h).z;
          h33 = (fZp - 2 * f0 + fZm) / (h * h);
          const fXpZp = evaluateAt(x + h, y, z + h).z;
          const fXpZm = evaluateAt(x + h, y, z - h).z;
          const fXmZp = evaluateAt(x - h, y, z + h).z;
          const fXmZm = evaluateAt(x - h, y, z - h).z;
          h13 = (fXpZp - fXpZm - fXmZp + fXmZm) / (4 * h * h);

          const fYpZp = evaluateAt(x, y + h, z + h).z;
          const fYpZm = evaluateAt(x, y + h, z - h).z;
          const fYmZp = evaluateAt(x, y - h, z + h).z;
          const fYmZm = evaluateAt(x, y - h, z - h).z;
          h23 = (fYpZp - fYpZm - fYmZp + fYmZm) / (4 * h * h);
        }
      }

      let det = 0;
      let trace = 0;

      if (is3D) {
        det = h11 * (h22 * h33 - h23 * h23)
            - h12 * (h12 * h33 - h23 * h13)
            + h13 * (h12 * h23 - h22 * h13);
        trace = h11 + h22 + h33;

        const numLatex = `\\mathbf{H}f(\\mathbf{a}) = \\begin{bmatrix}
          ${h11.toFixed(3)} & ${h12.toFixed(3)} & ${h13.toFixed(3)} \\\\[4pt]
          ${h12.toFixed(3)} & ${h22.toFixed(3)} & ${h23.toFixed(3)} \\\\[4pt]
          ${h13.toFixed(3)} & ${h23.toFixed(3)} & ${h33.toFixed(3)}
        \\end{bmatrix}_{3 \\times 3}`;
        katex.render(numLatex, numMatrixEl, { throwOnError: false });

        const delta1 = h11;
        const delta2 = h11 * h22 - h12 * h12;
        const delta3 = det;

        if (badge) {
          if (delta1 > 1e-4 && delta2 > 1e-4 && delta3 > 1e-4) {
            badge.textContent = "Local Min 🟢 (Positive Definite)";
            badge.className = "text-[10px] px-2.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-500/20 text-emerald-700 dark:text-emerald-400 border border-emerald-300 dark:border-emerald-500/30 font-bold";
          } else if (delta1 < -1e-4 && delta2 > 1e-4 && delta3 < -1e-4) {
            badge.textContent = "Local Max 🔴 (Negative Definite)";
            badge.className = "text-[10px] px-2.5 py-0.5 rounded-full bg-rose-100 dark:bg-rose-500/20 text-rose-700 dark:text-rose-400 border border-rose-300 dark:border-rose-500/30 font-bold";
          } else if (Math.abs(delta3) > 1e-4) {
            badge.textContent = "Saddle Point 🟡 (Indefinite)";
            badge.className = "text-[10px] px-2.5 py-0.5 rounded-full bg-amber-100 dark:bg-amber-500/20 text-amber-700 dark:text-amber-400 border border-amber-300 dark:border-amber-500/30 font-bold";
          } else {
            badge.textContent = "Test Inconclusive ⚪ (det = 0)";
            badge.className = "text-[10px] px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-300 dark:border-slate-700 font-bold";
          }
        }

      } else {
        det = h11 * h22 - h12 * h12;
        trace = h11 + h22;

        const numLatex = `\\mathbf{H}f(\\mathbf{a}) = \\begin{bmatrix}
          ${h11.toFixed(3)} & ${h12.toFixed(3)} \\\\[4pt]
          ${h12.toFixed(3)} & ${h22.toFixed(3)}
        \\end{bmatrix}_{2 \\times 2}`;
        katex.render(numLatex, numMatrixEl, { throwOnError: false });

        if (badge) {
          if (det > 1e-4) {
            if (h11 > 1e-4) {
              badge.textContent = "Local Min 🟢 (D > 0, f₁₁ > 0)";
              badge.className = "text-[10px] px-2.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-500/20 text-emerald-700 dark:text-emerald-400 border border-emerald-300 dark:border-emerald-500/30 font-bold";
            } else if (h11 < -1e-4) {
              badge.textContent = "Local Max 🔴 (D > 0, f₁₁ < 0)";
              badge.className = "text-[10px] px-2.5 py-0.5 rounded-full bg-rose-100 dark:bg-rose-500/20 text-rose-700 dark:text-rose-400 border border-rose-300 dark:border-rose-500/30 font-bold";
            } else {
              badge.textContent = "Degenerate Extrema";
              badge.className = "text-[10px] px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-300 font-bold";
            }
          } else if (det < -1e-4) {
            badge.textContent = "Saddle Point 🟡 (D < 0)";
            badge.className = "text-[10px] px-2.5 py-0.5 rounded-full bg-amber-100 dark:bg-amber-500/20 text-amber-700 dark:text-amber-400 border border-amber-300 dark:border-amber-500/30 font-bold";
          } else {
            badge.textContent = "Test Inconclusive ⚪ (D = 0)";
            badge.className = "text-[10px] px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-300 dark:border-slate-700 font-bold";
          }
        }
      }

      if (detEl) detEl.textContent = det.toFixed(4);
      if (trEl) trEl.textContent = trace.toFixed(4);

      if (taylorEl) {
        const pt = evaluateAt(state.x0, state.y0, state.z0);
        const v1 = state.notation === 'x1x2' ? 'x₁' : 'x';
        const v2 = state.notation === 'x1x2' ? 'x₂' : 'y';
        const sX = -state.x0 >= 0 ? `+ ${(-state.x0).toFixed(2)}` : `- ${state.x0.toFixed(2)}`;
        const sY = -state.y0 >= 0 ? `+ ${(-state.y0).toFixed(2)}` : `- ${state.y0.toFixed(2)}`;

        const poly = `T₂(x) = ${pt.z.toFixed(2)} + ${pt.fx.toFixed(2)}(${v1}${sX}) + ${pt.fy.toFixed(2)}(${v2}${sY}) + 0.5[${h11.toFixed(2)}(${v1}${sX})² + 2(${h12.toFixed(2)})(${v1}${sX})(${v2}${sY}) + ${h22.toFixed(2)}(${v2}${sY})²]`;
        taylorEl.textContent = poly;
      }
    }

    function snapPointToLevelSet() {
      let x = state.x0, y = state.y0;
      const targetC = state.level_c;

      for (let iter = 0; iter < 12; iter++) {
        const pt = evaluateAt(x, y);
        const diff = targetC - pt.z;
        const gradSq = pt.fx * pt.fx + pt.fy * pt.fy;
        if (Math.abs(diff) < 1e-5 || gradSq < 1e-12) break;
        const step = diff / gradSq;
        x += pt.fx * step;
        y += pt.fy * step;
      }

      setEvaluationPoint(x, y);
    }

    // -------------------------------------------------------------------------
    // Seamless Mesh Grid Generation
    // -------------------------------------------------------------------------
    function computeSurfaces() {
      const t0 = performance.now();
      const n = parseInt(state.grid_res);

      const spanX = Math.abs(state.x_range[1] - state.x_range[0]) || 12;
      const spanY = Math.abs(state.y_range[1] - state.y_range[0]) || 12;
      const padX = spanX * 0.35;
      const padY = spanY * 0.35;

      const meshXMin = Math.min(state.x_range[0], state.x_range[1]) - padX;
      const meshXMax = Math.max(state.x_range[0], state.x_range[1]) + padX;
      const meshYMin = Math.min(state.y_range[0], state.y_range[1]) - padY;
      const meshYMax = Math.max(state.y_range[0], state.y_range[1]) + padY;

      const xArr = new Float64Array(n);
      const yArr = new Float64Array(n);
      const dx = (meshXMax - meshXMin) / (n - 1);
      const dy = (meshYMax - meshYMin) / (n - 1);

      for (let i = 0; i < n; i++) xArr[i] = meshXMin + i * dx;
      for (let j = 0; j < n; j++) yArr[j] = meshYMin + j * dy;

      const zArr = [];

      for (let j = 0; j < n; j++) {
        const row = new Float64Array(n);
        const yVal = yArr[j];
        for (let i = 0; i < n; i++) {
          const xVal = xArr[i];
          const scope = getEvalScope(xVal, yVal);
          let val = 0;
          try {
            val = compiledF ? compiledF.evaluate(scope) : 0;
            if (typeof val !== 'number' || isNaN(val) || !isFinite(val)) val = null;
          } catch {
            val = null;
          }
          if (val !== null && constraintInfo.active && constraintInfo.isInequality && constraintInfo.compiledDiff) {
            try {
              const diffVal = Number(constraintInfo.compiledDiff.evaluate(scope));
              let ok = true;
              if (constraintInfo.op === '<=') ok = diffVal <= 1e-5;
              else if (constraintInfo.op === '<') ok = diffVal < 0;
              else if (constraintInfo.op === '>=') ok = diffVal >= -1e-5;
              else if (constraintInfo.op === '>') ok = diffVal > 0;
              if (!ok) val = null;
            } catch {}
          }
          row[i] = val;
        }
        zArr.push(Array.from(row));
      }

      const t1 = performance.now();
      document.getElementById("calcTimeBadge").textContent = `Render: ${(t1 - t0).toFixed(1)}ms (${n}x${n})`;

      return {
        x: Array.from(xArr),
        y: Array.from(yArr),
        z: zArr
      };
    }

    // -------------------------------------------------------------------------
    // 2D Level Set Plot Traces
    // -------------------------------------------------------------------------
    function build2DTraces(mesh) {
      const traces = [];
      const pt0 = evaluateAt(state.x0, state.y0);
      const span = Math.abs(state.x_range[1] - state.x_range[0]) || 12;

      // 1. Background Level Sets
      if (state.show_all_contours) {
        traces.push({
          type: 'contour',
          x: mesh.x,
          y: mesh.y,
          z: mesh.z,
          colorscale: state.color_scale,
          opacity: 0.65,
          ncontours: 24,
          contours: {
            coloring: 'heatmap',
            showlabels: true,
            labelfont: { size: 10, color: state.theme === 'dark' ? '#f8fafc' : '#1e1b4b', family: 'monospace' }
          },
          colorbar: {
            len: 0.8, thickness: 12,
            tickfont: { color: state.theme === 'dark' ? '#94a3b8' : '#475569', size: 10 },
            title: { text: state.is_vector_func ? '||F||' : 'f(x₁,x₂)', font: { color: state.theme === 'dark' ? '#cbd5e1' : '#1e1b4b', size: 11 } }
          },
          name: state.is_vector_func ? '||F|| Field' : 'Isolines'
        });
      }

      // 1b. Vector Field Flow Arrows when is_vector_func is active
      if (state.is_vector_func && compiledF1 && compiledF2) {
        const gridSteps = 9;
        const qx = [], qy = [];
        const xMin = state.x_range[0], xMax = state.x_range[1];
        const yMin = state.y_range[0], yMax = state.y_range[1];
        const stepX = (xMax - xMin) / (gridSteps + 1);
        const stepY = (yMax - yMin) / (gridSteps + 1);
        const arrowMaxLen = Math.min(stepX, stepY) * 0.72;

        for (let ix = 1; ix <= gridSteps; ix++) {
          const gx = xMin + ix * stepX;
          for (let iy = 1; iy <= gridSteps; iy++) {
            const gy = yMin + iy * stepY;
            const ptG = evaluateAt(gx, gy);
            const len = Math.sqrt(ptG.f1 * ptG.f1 + ptG.f2 * ptG.f2);
            if (len > 1e-4) {
              const sc = Math.min(1, arrowMaxLen / len);
              const tipX = gx + ptG.f1 * sc;
              const tipY = gy + ptG.f2 * sc;
              qx.push(gx, tipX, null);
              qy.push(gy, tipY, null);
            }
          }
        }

        if (qx.length > 0) {
          traces.push({
            type: 'scatter',
            mode: 'lines',
            x: qx,
            y: qy,
            line: { color: state.theme === 'dark' ? 'rgba(168, 85, 247, 0.45)' : 'rgba(124, 58, 237, 0.35)', width: 1.5 },
            hoverinfo: 'none',
            name: 'Vector Field Flow F'
          });
        }
      }

      // 2. Highlighted Level Set Curve
      traces.push({
        type: 'contour',
        x: mesh.x,
        y: mesh.y,
        z: mesh.z,
        contours: {
          type: 'constraint',
          operation: '=',
          value: state.level_c,
          coloring: 'none'
        },
        line: { color: '#00d2ee', width: 4.5 },
        showscale: false,
        name: `Level Set: f = ${state.level_c.toFixed(2)}`
      });

      // 3. Point of Tangency a
      traces.push({
        type: 'scatter',
        mode: 'markers+text',
        x: [state.x0],
        y: [state.y0],
        text: [`a (${state.x0.toFixed(2)}, ${state.y0.toFixed(2)})`],
        textposition: 'top right',
        textfont: { color: state.theme === 'dark' ? '#ffffff' : '#0f172a', size: 12, family: 'sans-serif' },
        marker: { size: 10, color: '#f43f5e', symbol: 'circle', line: { color: '#ffffff', width: 2 } },
        name: 'Point a'
      });

      const gradMag = Math.sqrt(pt0.fx * pt0.fx + pt0.fy * pt0.fy);

      if (gradMag > 1e-4) {
        const nx = pt0.fx / gradMag;
        const ny = pt0.fy / gradMag;
        const tx = -ny;
        const ty = nx;
        const lineLen = span * 0.45;

        // 4. Normal Line in 2D
        if (state.show_normal_line) {
          traces.push({
            type: 'scatter',
            mode: 'lines',
            x: [state.x0 - lineLen * nx, state.x0 + lineLen * nx],
            y: [state.y0 - lineLen * ny, state.y0 + lineLen * ny],
            line: { color: '#06b6d4', width: 3, dash: 'longdash' },
            name: 'Normal Line (along ∇f, ⊥ Tangent)'
          });
        }

        // 5. Tangent Line to Level Set at a
        if (state.show_tangent_line) {
          traces.push({
            type: 'scatter',
            mode: 'lines',
            x: [state.x0 - lineLen * tx, state.x0 + lineLen * tx],
            y: [state.y0 - lineLen * ty, state.y0 + lineLen * ty],
            line: { color: '#ec4899', width: 3, dash: 'dash' },
            name: 'Tangent Line to Curve'
          });
        }

        // 6. Gradient Vector ∇f Arrow
        if (state.show_gradient) {
          const arrowLen = span * 0.22;
          const tipX = state.x0 + nx * arrowLen;
          const tipY = state.y0 + ny * arrowLen;

          traces.push({
            type: 'scatter',
            mode: 'lines+markers+text',
            x: [state.x0, tipX],
            y: [state.y0, tipY],
            text: ['', '∇f (90° Normal)'],
            textposition: 'top right',
            textfont: { color: '#f59e0b', size: 12, family: 'sans-serif' },
            line: { color: '#f59e0b', width: 4.5 },
            marker: { size: [0, 9], color: '#f59e0b', symbol: 'arrow' },
            name: 'Gradient Vector ∇f'
          });
        }

        // 7. Right Angle Symbol (90° Square Corner)
        if (state.show_right_angle && (state.show_normal_line || state.show_gradient) && state.show_tangent_line) {
          const s = span * 0.04;
          const p1x = state.x0 + s * tx;
          const p1y = state.y0 + s * ty;
          const p2x = state.x0 + s * tx + s * nx;
          const p2y = state.y0 + s * ty + s * ny;
          const p3x = state.x0 + s * nx;
          const p3y = state.y0 + s * ny;

          traces.push({
            type: 'scatter',
            mode: 'lines',
            x: [p1x, p2x, p3x],
            y: [p1y, p2y, p3y],
            line: { color: '#10b981', width: 2.5 },
            showlegend: false,
            hoverinfo: 'none'
          });
        }
      }

      // 8. Constraint / Requirement Curves in 2D
      if (constraintInfo.active && state.show_constraint_curve && constraintInfo.polylines && constraintInfo.polylines.length > 0) {
        constraintInfo.polylines.forEach((poly, idx) => {
          traces.push({
            type: 'scatter',
            mode: 'lines',
            x: poly.map(p => p[0]),
            y: poly.map(p => p[1]),
            line: { color: '#8b5cf6', width: 3.5, dash: 'solid' },
            name: idx === 0 ? `Requirement: ${state.constraint_raw}` : undefined,
            showlegend: idx === 0
          });
        });
      }

      return traces;
    }

    // -------------------------------------------------------------------------
    // 3D Surface Plot Traces
    // -------------------------------------------------------------------------
    function build3DTraces(mesh) {
      const traces = [];
      const pt0 = evaluateAt(state.x0, state.y0, state.z0);
      const isIdentityVector = (state.f_expr_raw || '').includes('[x1;') || 
                               (state.f_expr_raw || '').includes('[x1,') || 
                               (state.f_expr_raw || '').includes('[x;') || 
                               (state.f_expr_raw || '').includes('[x,');

      // 1. Regular 3D Function Surface (unless it's identity vector with active constraint)
      if (!isIdentityVector || !constraintInfo.active) {
        traces.push({
          type: 'surface',
          x: mesh.x,
          y: mesh.y,
          z: mesh.z,
          colorscale: state.color_scale,
          opacity: state.opacity,
          showscale: true,
          contours: {
            z: { show: true, usecolormap: true, highlightcolor: "#ffffff", project: { z: true } }
          },
          colorbar: {
            len: 0.65, thickness: 12,
            tickfont: { color: state.theme === 'dark' ? '#94a3b8' : '#475569', size: 10 },
            title: { text: 'z', font: { color: state.theme === 'dark' ? '#cbd5e1' : '#1e1b4b', size: 12 } }
          },
          name: state.is_matrix_input ? '||F||' : 'f(x₁, x₂)'
        });
      }

      // 2. 3D Cylinder / Extruded Constraint Surface (x3 free!)
      if (constraintInfo.active && state.show_constraint_surface && constraintInfo.polylines && constraintInfo.polylines.length > 0) {
        const zMin = state.y_range[0] || -5;
        const zMax = state.y_range[1] || 5;
        const numZ = 24;

        constraintInfo.polylines.forEach((poly, idx) => {
          if (poly.length < 2) return;
          const cylX = [];
          const cylY = [];
          const cylZ = [];

          for (let j = 0; j < numZ; j++) {
            const rowX = [];
            const rowY = [];
            const rowZ = [];
            const zVal = zMin + j * (zMax - zMin) / (numZ - 1);
            for (let k = 0; k < poly.length; k++) {
              rowX.push(poly[k][0]);
              rowY.push(poly[k][1]);
              rowZ.push(zVal);
            }
            cylX.push(rowX);
            cylY.push(rowY);
            cylZ.push(rowZ);
          }

          traces.push({
            type: 'surface',
            x: cylX,
            y: cylY,
            z: cylZ,
            colorscale: [
              [0, '#06b6d4'],
              [0.5, '#6366f1'],
              [1, '#a855f7']
            ],
            opacity: 0.82,
            showscale: isIdentityVector,
            contours: {
              z: { show: true, width: 2, color: '#ffffff', project: { z: false } }
            },
            lighting: { ambient: 0.85, diffuse: 0.8, specular: 0.3, roughness: 0.4 },
            name: idx === 0 ? `Cylinder: ${state.constraint_raw}` : undefined,
            showlegend: idx === 0
          });
        });
      }

      // 3. 3D Restriction Curve (f restricted to constraint)
      if (constraintInfo.active && state.show_constraint_curve && constraintInfo.polylines && constraintInfo.polylines.length > 0 && !isIdentityVector) {
        constraintInfo.polylines.forEach((poly, idx) => {
          const curX = [];
          const curY = [];
          const curZ = [];
          for (let k = 0; k < poly.length; k++) {
            const xVal = poly[k][0];
            const yVal = poly[k][1];
            const sc = getEvalScope(xVal, yVal, 0);
            let zVal = 0;
            try {
              zVal = compiledF ? Number(compiledF.evaluate(sc)) : 0;
              if (isNaN(zVal) || !isFinite(zVal)) continue;
            } catch { continue; }
            curX.push(xVal);
            curY.push(yVal);
            curZ.push(zVal);
          }
          if (curX.length > 1) {
            traces.push({
              type: 'scatter3d',
              mode: 'lines',
              x: curX,
              y: curY,
              z: curZ,
              line: { color: '#f43f5e', width: 8 },
              name: idx === 0 ? `f on constraint` : undefined,
              showlegend: idx === 0
            });
          }
        });
      }

      // 4. Affine Function Surface z = g(x) (Tangent Plane!)
      if (state.show_affine_plane && !isIdentityVector) {
        const span = 2.8;
        const tx = [state.x0 - span, state.x0 + span];
        const ty = [state.y0 - span, state.y0 + span];
        const tz = [
          [
            pt0.z + pt0.fx * (tx[0] - state.x0) + pt0.fy * (ty[0] - state.y0),
            pt0.z + pt0.fx * (tx[1] - state.x0) + pt0.fy * (ty[0] - state.y0)
          ],
          [
            pt0.z + pt0.fx * (tx[0] - state.x0) + pt0.fy * (ty[1] - state.y0),
            pt0.z + pt0.fx * (tx[1] - state.x0) + pt0.fy * (ty[1] - state.y0)
          ]
        ];

        traces.push({
          type: 'surface',
          x: tx,
          y: ty,
          z: tz,
          name: 'Affine g(x) (Tangent Plane)',
          showscale: false,
          opacity: 0.65,
          colorscale: [[0, '#10b981'], [1, '#10b981']]
        });
      }

      // 5. Point a in 3D
      const aZ = (isIdentityVector || state.dim === 3) ? state.z0 : pt0.z;
      traces.push({
        type: 'scatter3d',
        mode: 'markers+text',
        x: [state.x0],
        y: [state.y0],
        z: [aZ],
        text: [`a(${state.x0.toFixed(1)}, ${state.y0.toFixed(1)}, ${aZ.toFixed(1)})`],
        textposition: 'top center',
        textfont: { color: '#f43f5e', size: 11 },
        marker: { size: 7, color: '#f43f5e', symbol: 'circle' },
        name: 'Point a'
      });

      // 3D Surface Normal Line
      if (state.show_3d_normal_line) {
        const normLen = Math.sqrt(pt0.fx * pt0.fx + pt0.fy * pt0.fy + 1);
        const nx = -pt0.fx / normLen;
        const ny = -pt0.fy / normLen;
        const nz = 1 / normLen;
        const L = 3.5;

        traces.push({
          type: 'scatter3d',
          mode: 'lines',
          x: [state.x0 - L * nx, state.x0 + L * nx],
          y: [state.y0 - L * ny, state.y0 + L * ny],
          z: [pt0.z - L * nz, pt0.z + L * nz],
          name: '3D Normal Line (⊥ Plane)',
          line: { color: '#06b6d4', width: 6 }
        });
      }

      // 3D Gradient Vector
      if (state.show_gradient) {
        const mag = Math.sqrt(pt0.fx * pt0.fx + pt0.fy * pt0.fy);
        const scale = mag > 0 ? Math.min(1.5, Math.max(0.6, 1.2 / mag)) : 1;
        const vx = pt0.fx * scale;
        const vy = pt0.fy * scale;
        const vz = (pt0.fx * pt0.fx + pt0.fy * pt0.fy) * scale * 0.35;

        traces.push({
          type: 'scatter3d',
          mode: 'lines+markers+text',
          x: [state.x0, state.x0 + vx],
          y: [state.y0, state.y0 + vy],
          z: [pt0.z, pt0.z + vz],
          text: ['', '∇f (Steepest Ascent)'],
          textposition: 'top right',
          textfont: { color: '#f59e0b', size: 11 },
          line: { color: '#f59e0b', width: 7 },
          marker: { size: [0, 6], color: '#f59e0b', symbol: 'diamond' },
          name: '3D Gradient ∇f'
        });
      }

      return traces;
    }

    // -------------------------------------------------------------------------
    // Theme-Aware Plotly Layouts (Modern Purple & White or Dark Violet)
    // -------------------------------------------------------------------------
    function get2DLayout() {
      const isDark = state.theme === 'dark';
      const var1 = state.notation === 'x1x2' ? 'x₁' : 'x';
      const var2 = state.notation === 'x1x2' ? 'x₂' : 'y';

      return {
        autosize: true,
        dragmode: state.drag_mode || 'pan',
        margin: { l: 45, r: 20, b: 40, t: 25 },
        paper_bgcolor: isDark ? '#070314' : '#fcfaff',
        plot_bgcolor: isDark ? '#070314' : '#ffffff',
        xaxis: {
          title: `${var1} (Horizontal Axis)`,
          gridcolor: isDark ? '#1e1b4b' : '#ede9fe',
          zerolinecolor: isDark ? '#4338ca' : '#c4b5fd',
          tickfont: { color: isDark ? '#94a3b8' : '#475569' },
          titlefont: { color: isDark ? '#cbd5e1' : '#1e1b4b', size: 12 },
          range: state.x_range,
          autorange: false
        },
        yaxis: {
          title: `${var2} (Vertical Axis)`,
          gridcolor: isDark ? '#1e1b4b' : '#ede9fe',
          zerolinecolor: isDark ? '#4338ca' : '#c4b5fd',
          tickfont: { color: isDark ? '#94a3b8' : '#475569' },
          titlefont: { color: isDark ? '#cbd5e1' : '#1e1b4b', size: 12 },
          range: state.y_range,
          autorange: false,
          scaleanchor: 'x', scaleratio: 1
        },
        showlegend: true,
        legend: {
          x: 0.02, y: 0.98,
          bgcolor: isDark ? 'rgba(12, 7, 33, 0.88)' : 'rgba(255, 255, 255, 0.92)',
          bordercolor: isDark ? '#3b0764' : '#ddd6fe',
          borderwidth: 1,
          font: { color: isDark ? '#f3e8ff' : '#1e1b4b', size: 11 }
        }
      };
    }

    function get3DLayout() {
      const isDark = state.theme === 'dark';
      const var1 = state.notation === 'x1x2' ? 'X₁' : 'X';
      const var2 = state.notation === 'x1x2' ? 'X₂' : 'Y';

      return {
        autosize: true,
        margin: { l: 0, r: 0, b: 0, t: 0 },
        paper_bgcolor: isDark ? '#070314' : '#fcfaff',
        plot_bgcolor: isDark ? '#070314' : '#ffffff',
        scene: {
          xaxis: {
            title: var1,
            gridcolor: isDark ? '#1e1b4b' : '#ede9fe',
            zerolinecolor: isDark ? '#4338ca' : '#c4b5fd',
            tickfont: { color: isDark ? '#94a3b8' : '#475569' }
          },
          yaxis: {
            title: var2,
            gridcolor: isDark ? '#1e1b4b' : '#ede9fe',
            zerolinecolor: isDark ? '#4338ca' : '#c4b5fd',
            tickfont: { color: isDark ? '#94a3b8' : '#475569' }
          },
          zaxis: {
            title: 'Z',
            gridcolor: isDark ? '#1e1b4b' : '#ede9fe',
            zerolinecolor: isDark ? '#4338ca' : '#c4b5fd',
            tickfont: { color: isDark ? '#94a3b8' : '#475569' }
          },
          camera: { eye: { x: 1.5, y: 1.5, z: 1.2 } },
          aspectmode: 'cube'
        },
        showlegend: true,
        legend: {
          x: 0.02, y: 0.98,
          bgcolor: isDark ? 'rgba(12, 7, 33, 0.88)' : 'rgba(255, 255, 255, 0.92)',
          bordercolor: isDark ? '#3b0764' : '#ddd6fe',
          borderwidth: 1,
          font: { color: isDark ? '#f3e8ff' : '#1e1b4b', size: 11 }
        }
      };
    }

    const plotConfig2D = {
      responsive: true,
      scrollZoom: true,
      displayModeBar: true,
      displaylogo: false,
      modeBarButtonsToRemove: ['lasso2d', 'select2d'],
      doubleClick: 'reset+autosize'
    };

    const plotConfig3D = {
      responsive: true,
      scrollZoom: true,
      displayModeBar: true,
      displaylogo: false
    };

    function zoom2D(factor) {
      const cx = (state.x_range[0] + state.x_range[1]) / 2;
      const cy = (state.y_range[0] + state.y_range[1]) / 2;
      const hx = (state.x_range[1] - state.x_range[0]) * factor / 2;
      const hy = (state.y_range[1] - state.y_range[0]) * factor / 2;

      state.x_range = [cx - hx, cx + hx];
      state.y_range = [cy - hy, cy + hy];
      syncDomainInputs();
      renderPlots(false);
    }

    function syncDomainInputs() {
      const xMinInput = document.getElementById("xMin");
      const xMaxInput = document.getElementById("xMax");
      const yMinInput = document.getElementById("yMin");
      const yMaxInput = document.getElementById("yMax");
      if (xMinInput) xMinInput.value = Math.min(state.x_range[0], state.x_range[1]).toFixed(1);
      if (xMaxInput) xMaxInput.value = Math.max(state.x_range[0], state.x_range[1]).toFixed(1);
      if (yMinInput) yMinInput.value = Math.min(state.y_range[0], state.y_range[1]).toFixed(1);
      if (yMaxInput) yMaxInput.value = Math.max(state.y_range[0], state.y_range[1]).toFixed(1);
    }

    let isInitial2D = true;
    let isInitial3D = true;

    function renderPlots(preserveCamera = true) {
      if (!compiledF) compileExpressions();
      if (!compiledF) return;

      const mesh = computeSurfaces();
      const div2D = document.getElementById('plotContainer2D');
      const div3D = document.getElementById('plotContainer3D');

      isInternalUpdating = true;

      if (state.view_mode === '2d' || state.view_mode === 'split') {
        const traces2D = build2DTraces(mesh);
        if (isInitial2D) {
          Plotly.newPlot(div2D, traces2D, get2DLayout(), plotConfig2D).then(() => {
            attachPlotEvents2D();
            isInternalUpdating = false;
          });
          isInitial2D = false;
        } else {
          Plotly.react(div2D, traces2D, get2DLayout()).then(() => {
            setTimeout(() => { isInternalUpdating = false; }, 50);
          });
        }
      }

      if (state.view_mode === '3d' || state.view_mode === 'split') {
        const traces3D = build3DTraces(mesh);
        if (isInitial3D) {
          Plotly.newPlot(div3D, traces3D, get3DLayout(), plotConfig3D).then(() => {
            isInternalUpdating = false;
          });
          isInitial3D = false;
        } else {
          if (preserveCamera && div3D._fullLayout && div3D._fullLayout.scene) {
            const cam = div3D._fullLayout.scene._scene.getCamera();
            const layout = get3DLayout();
            if (cam) layout.scene.camera = { eye: cam.eye, center: cam.center, up: cam.up };
            Plotly.react(div3D, traces3D, layout).then(() => {
              setTimeout(() => { isInternalUpdating = false; }, 50);
            });
          } else {
            Plotly.react(div3D, traces3D, get3DLayout()).then(() => {
              setTimeout(() => { isInternalUpdating = false; }, 50);
            });
          }
        }
      }
    }

    function attachPlotEvents2D() {
      const div2D = document.getElementById('plotContainer2D');
      
      div2D.on('plotly_hover', function(data) {
        if (data.points && data.points.length > 0) {
          const pt = data.points[0];
          document.getElementById('coordReadout').textContent = 
            `Hover: (${pt.x.toFixed(3)}, ${pt.y.toFixed(3)}) | Value f = ${pt.z !== undefined ? pt.z.toFixed(3) : '-'}`;
        }
      });
      div2D.on('plotly_unhover', function() {
        document.getElementById('coordReadout').textContent = 'Scroll to Zoom • Drag to Pan • Click to set Point a';
      });

      div2D.on('plotly_click', function(data) {
        if (data.points && data.points.length > 0) {
          const pt = data.points[0];
          setEvaluationPoint(pt.x, pt.y);
        }
      });

      div2D.on('plotly_relayout', function(eventData) {
        if (isInternalUpdating || !eventData) return;

        if (eventData['xaxis.autorange'] || eventData['yaxis.autorange']) {
          state.x_range = [-6, 6];
          state.y_range = [-6, 6];
          syncDomainInputs();
          renderPlots(false);
          return;
        }

        let newX0 = eventData['xaxis.range[0]'];
        let newX1 = eventData['xaxis.range[1]'];
        let newY0 = eventData['yaxis.range[0]'];
        let newY1 = eventData['yaxis.range[1]'];

        let changed = false;
        if (newX0 !== undefined && newX1 !== undefined && isFinite(newX0) && isFinite(newX1)) {
          state.x_range = [newX0, newX1];
          changed = true;
        }
        if (newY0 !== undefined && newY1 !== undefined && isFinite(newY0) && isFinite(newY1)) {
          state.y_range = [newY0, newY1];
          changed = true;
        }

        if (changed) {
          clearTimeout(relayoutDebounce);
          relayoutDebounce = setTimeout(() => {
            syncDomainInputs();
            renderPlots(true);
          }, 120);
        }
      });
    }

    // -------------------------------------------------------------------------
    // Animation Loops (Orbit 3D & Slicing c)
    // -------------------------------------------------------------------------
    let orbitAngle = 0;
    let orbitAnimationId = null;

    function toggleOrbit3D() {
      state.is_orbiting = !state.is_orbiting;
      const btn = document.getElementById('orbit3DBtn');
      const icon = document.getElementById('orbitIcon');
      const txt = document.getElementById('orbitText');

      if (state.is_orbiting) {
        if (state.view_mode === '2d') {
          setViewMode('split');
        }
        if (btn) {
          btn.className = "px-2.5 py-1 rounded-lg bg-violet-600 border border-violet-600 text-white transition flex items-center space-x-1 shadow-sm font-semibold";
        }
        if (icon) icon.setAttribute('data-lucide', 'pause');
        if (txt) txt.textContent = 'Pause 3D';
        lucide.createIcons();
        startOrbitLoop();
      } else {
        if (btn) {
          btn.className = "px-2.5 py-1 rounded-lg bg-white dark:bg-purple-950 border border-violet-200 dark:border-purple-800 hover:bg-violet-100 dark:hover:bg-purple-900 text-slate-700 dark:text-purple-200 transition flex items-center space-x-1 shadow-sm font-semibold";
        }
        if (icon) icon.setAttribute('data-lucide', 'play');
        if (txt) txt.textContent = 'Orbit 3D';
        lucide.createIcons();
        stopOrbitLoop();
      }
    }

    function startOrbitLoop() {
      if (orbitAnimationId) cancelAnimationFrame(orbitAnimationId);
      function step() {
        if (!state.is_orbiting) return;
        orbitAngle += 0.012;
        const radius = 2.0;
        const eyeX = radius * Math.cos(orbitAngle);
        const eyeY = radius * Math.sin(orbitAngle);
        const eyeZ = 1.2 + 0.25 * Math.sin(orbitAngle * 0.7);
        const p3d = document.getElementById('plotContainer3D');
        if (p3d && p3d._fullLayout && p3d._fullLayout.scene) {
          Plotly.relayout(p3d, {
            'scene.camera.eye': { x: eyeX, y: eyeY, z: eyeZ }
          });
        }
        orbitAnimationId = requestAnimationFrame(step);
      }
      orbitAnimationId = requestAnimationFrame(step);
    }

    function stopOrbitLoop() {
      if (orbitAnimationId) {
        cancelAnimationFrame(orbitAnimationId);
        orbitAnimationId = null;
      }
    }

    let sliceDirection = 1;
    let sliceAnimationId = null;

    function toggleSliceAnimation() {
      state.is_slicing = !state.is_slicing;
      const btn = document.getElementById('animateSliceBtn');
      const txt = document.getElementById('sliceText');

      if (state.is_slicing) {
        if (btn) {
          btn.className = "px-2.5 py-1 rounded-lg bg-purple-600 border border-purple-600 text-white transition flex items-center space-x-1 shadow-sm font-semibold";
        }
        if (txt) txt.textContent = 'Pause c';
        startSliceLoop();
      } else {
        if (btn) {
          btn.className = "px-2.5 py-1 rounded-lg bg-white dark:bg-purple-950 border border-violet-200 dark:border-purple-800 hover:bg-violet-100 dark:hover:bg-purple-900 text-slate-700 dark:text-purple-200 transition flex items-center space-x-1 shadow-sm font-semibold";
        }
        if (txt) txt.textContent = 'Slice c';
        stopSliceLoop();
      }
    }

    function startSliceLoop() {
      if (sliceAnimationId) cancelAnimationFrame(sliceAnimationId);
      let lastTime = performance.now();
      function step(now) {
        if (!state.is_slicing) return;
        const dt = Math.min((now - lastTime) / 1000, 0.1);
        lastTime = now;
        let nextC = state.level_c + sliceDirection * dt * 2.5;
        if (nextC >= 7.5) {
          nextC = 7.5;
          sliceDirection = -1;
        } else if (nextC <= -3.5) {
          nextC = -3.5;
          sliceDirection = 1;
        }
        state.level_c = nextC;
        const cVal = document.getElementById('levelValueC');
        const cSld = document.getElementById('levelSliderC');
        if (cVal) cVal.value = nextC.toFixed(1);
        if (cSld) cSld.value = nextC;
        if (state.level_c >= 0) {
          state.radius_r = Math.sqrt(state.level_c);
          const rInp = document.getElementById('radiusInputR');
          if (rInp) rInp.value = state.radius_r.toFixed(2);
        }
        updateCalculusCalculations();
        renderPlots(true);
        sliceAnimationId = requestAnimationFrame(step);
      }
      sliceAnimationId = requestAnimationFrame(step);
    }

    function stopSliceLoop() {
      if (sliceAnimationId) {
        cancelAnimationFrame(sliceAnimationId);
        sliceAnimationId = null;
      }
    }

    function setViewMode(mode) {
      state.view_mode = mode;
      const div2D = document.getElementById('plotContainer2D');
      const div3D = document.getElementById('plotContainer3D');

      document.querySelectorAll('.view-mode-btn').forEach(btn => btn.classList.remove('active'));

      if (mode === '2d') {
        document.getElementById('viewMode2D').classList.add('active');
        div2D.classList.remove('hidden');
        div3D.classList.add('hidden');
      } else if (mode === '3d') {
        document.getElementById('viewMode3D').classList.add('active');
        div2D.classList.add('hidden');
        div3D.classList.remove('hidden');
      } else if (mode === 'split') {
        document.getElementById('viewModeSplit').classList.add('active');
        div2D.classList.remove('hidden');
        div3D.classList.remove('hidden');
      }

      setTimeout(() => {
        Plotly.Plots.resize(div2D);
        Plotly.Plots.resize(div3D);
        renderPlots(true);
      }, 50);
    }

    function setEvaluationPoint(x, y, z) {
      state.x0 = parseFloat(x);
      state.y0 = parseFloat(y);
      if (z !== undefined && z !== null && !isNaN(parseFloat(z))) {
        state.z0 = parseFloat(z);
      }

      const xInp = document.getElementById('x0Input');
      const yInp = document.getElementById('y0Input');
      const xSld = document.getElementById('x0Slider');
      const ySld = document.getElementById('y0Slider');
      const zInp = document.getElementById('z0Input');
      const zSld = document.getElementById('z0Slider');

      if (xInp) xInp.value = state.x0.toFixed(2);
      if (yInp) yInp.value = state.y0.toFixed(2);
      if (xSld) xSld.value = state.x0;
      if (ySld) ySld.value = state.y0;
      if (zInp) zInp.value = state.z0.toFixed(2);
      if (zSld) zSld.value = state.z0;

      updateCalculusCalculations();
      updateHessianCalculations();
      updateAffineCalculations();
      renderPlots(true);
    }

    function initSidebarTabs() {
      const tabs = [
        { btn: 'tabNavLevelSets', content: 'tabContentLevelSets' },
        { btn: 'tabNavAffine', content: 'tabContentAffine' },
        { btn: 'tabNavCalculus', content: 'tabContentCalculus' },
        { btn: 'tabNavFunctions', content: 'tabContentFunctions' }
      ];

      tabs.forEach(t => {
        document.getElementById(t.btn).addEventListener('click', () => {
          tabs.forEach(other => {
            document.getElementById(other.btn).classList.remove('active');
            document.getElementById(other.content).classList.add('hidden');
          });
          document.getElementById(t.btn).classList.add('active');
          document.getElementById(t.content).classList.remove('hidden');
        });
      });
    }

    // -------------------------------------------------------------------------
    // Event Listeners Binding
    // -------------------------------------------------------------------------
    function initEvents() {
      // Theme toggle (Light Modern Purple-White <-> Dark)
      document.getElementById('themeToggleBtn').addEventListener('click', toggleTheme);

      document.getElementById('viewMode2D').addEventListener('click', () => setViewMode('2d'));
      document.getElementById('viewMode3D').addEventListener('click', () => setViewMode('3d'));
      document.getElementById('viewModeSplit').addEventListener('click', () => setViewMode('split'));

      document.getElementById('zoomInBtn').addEventListener('click', () => zoom2D(0.72));
      document.getElementById('zoomOutBtn').addEventListener('click', () => zoom2D(1.38));
      
      document.getElementById('togglePanBtn').addEventListener('click', () => {
        state.drag_mode = state.drag_mode === 'pan' ? 'zoom' : 'pan';
        const isPan = state.drag_mode === 'pan';
        const txt = document.getElementById('panText');
        const icon = document.getElementById('panIcon');
        
        txt.textContent = isPan ? 'Pan' : 'Box Zoom';
        icon.setAttribute('data-lucide', isPan ? 'hand' : 'zoom-in');
        lucide.createIcons();
        
        Plotly.relayout(document.getElementById('plotContainer2D'), { dragmode: state.drag_mode });
      });

      document.getElementById('resetZoomBtn').addEventListener('click', () => {
        state.x_range = [-6, 6];
        state.y_range = [-6, 6];
        syncDomainInputs();
        renderPlots(false);
      });

      // 3D Orbit Animation
      const orbitBtn = document.getElementById('orbit3DBtn');
      if (orbitBtn) {
        orbitBtn.addEventListener('click', toggleOrbit3D);
      }

      // Slicing Animation
      const sliceBtn = document.getElementById('animateSliceBtn');
      if (sliceBtn) {
        sliceBtn.addEventListener('click', toggleSliceAnimation);
      }

      // Marimo Modal Open/Close
      const openMarimoBtn = document.getElementById('openMarimoBtn');
      const headerMarimoBtn = document.getElementById('headerMarimoBtn');
      const closeMarimoModal = document.getElementById('closeMarimoModal');
      const marimoModal = document.getElementById('marimoModal');

      if (openMarimoBtn && marimoModal) {
        openMarimoBtn.addEventListener('click', () => marimoModal.classList.remove('hidden'));
      }
      if (headerMarimoBtn && marimoModal) {
        headerMarimoBtn.addEventListener('click', () => marimoModal.classList.remove('hidden'));
      }
      if (closeMarimoModal && marimoModal) {
        closeMarimoModal.addEventListener('click', () => marimoModal.classList.add('hidden'));
      }

      // Theory modal
      document.getElementById('openTheoryBtn').addEventListener('click', () => {
        document.getElementById('theoryModal').classList.remove('hidden');
      });
      document.getElementById('closeTheoryModal').addEventListener('click', () => {
        document.getElementById('theoryModal').classList.add('hidden');
      });

      // Level set constant c input and slider
      document.getElementById('levelValueC').addEventListener('input', (e) => {
        state.level_c = parseFloat(e.target.value) || 0;
        document.getElementById('levelSliderC').value = state.level_c;
        if (state.level_c >= 0) {
          state.radius_r = Math.sqrt(state.level_c);
          document.getElementById('radiusInputR').value = state.radius_r.toFixed(2);
        }
        updateCalculusCalculations();
        renderPlots(true);
      });
      document.getElementById('levelSliderC').addEventListener('input', (e) => {
        state.level_c = parseFloat(e.target.value);
        document.getElementById('levelValueC').value = state.level_c.toFixed(1);
        if (state.level_c >= 0) {
          state.radius_r = Math.sqrt(state.level_c);
          document.getElementById('radiusInputR').value = state.radius_r.toFixed(2);
        }
        updateCalculusCalculations();
        renderPlots(true);
      });

      // Radius helper r -> c = r^2
      document.getElementById('applyRadiusBtn').addEventListener('click', () => {
        const r = parseFloat(document.getElementById('radiusInputR').value) || 1;
        state.radius_r = r;
        state.level_c = r * r;
        document.getElementById('levelValueC').value = state.level_c.toFixed(1);
        document.getElementById('levelSliderC').value = state.level_c;
        setEvaluationPoint(r, 0);
      });

      // Snap point a
      document.getElementById('snapToLevelSetBtn').addEventListener('click', snapPointToLevelSet);

      // Point evaluation inputs
      const onPointType = () => {
        const x = parseFloat(document.getElementById('x0Input').value) || 0;
        const y = parseFloat(document.getElementById('y0Input').value) || 0;
        const z = parseFloat(document.getElementById('z0Input')?.value) || 0;
        setEvaluationPoint(x, y, z);
      };
      document.getElementById('x0Input').addEventListener('input', onPointType);
      document.getElementById('y0Input').addEventListener('input', onPointType);
      document.getElementById('z0Input')?.addEventListener('input', onPointType);

      document.getElementById('x0Slider').addEventListener('input', (e) => {
        setEvaluationPoint(e.target.value, state.y0, state.z0);
      });
      document.getElementById('y0Slider').addEventListener('input', (e) => {
        setEvaluationPoint(state.x0, e.target.value, state.z0);
      });
      document.getElementById('z0Slider')?.addEventListener('input', (e) => {
        setEvaluationPoint(state.x0, state.y0, e.target.value);
      });

      // Linearization test point inputs
      document.getElementById('testXInput').addEventListener('input', (e) => {
        state.test_x = parseFloat(e.target.value) || 0;
        updateAffineCalculations();
      });
      document.getElementById('testYInput').addEventListener('input', (e) => {
        state.test_y = parseFloat(e.target.value) || 0;
        updateAffineCalculations();
      });

      // Geometric Toggles (Clean, essential multivariable geometry)
      document.getElementById('showNormalLine').addEventListener('change', (e) => {
        state.show_normal_line = e.target.checked;
        renderPlots(true);
      });
      document.getElementById('showTangentLine').addEventListener('change', (e) => {
        state.show_tangent_line = e.target.checked;
        renderPlots(true);
      });
      document.getElementById('showRightAngleMarker').addEventListener('change', (e) => {
        state.show_right_angle = e.target.checked;
        renderPlots(true);
      });
      document.getElementById('showGradientVector').addEventListener('change', (e) => {
        state.show_gradient = e.target.checked;
        renderPlots(true);
      });
      document.getElementById('show3DNormalLine').addEventListener('change', (e) => {
        state.show_3d_normal_line = e.target.checked;
        renderPlots(true);
      });
      document.getElementById('showAffinePlane').addEventListener('change', (e) => {
        state.show_affine_plane = e.target.checked;
        renderPlots(true);
      });
      document.getElementById('showAllContourLines').addEventListener('change', (e) => {
        state.show_all_contours = e.target.checked;
        renderPlots(true);
      });

      // Formula input
      let debounce = null;
      document.getElementById("functionInput").addEventListener("input", (e) => {
        clearTimeout(debounce);
        debounce = setTimeout(() => {
          state.f_expr_raw = e.target.value;
          compileExpressions();
          renderPlots(true);
        }, 200);
      });

      document.querySelectorAll(".math-insert").forEach(btn => {
        btn.addEventListener("click", () => {
          const input = document.getElementById("functionInput");
          input.value = btn.textContent;
          state.f_expr_raw = input.value;
          compileExpressions();
          renderPlots(true);
        });
      });

      // Notation toggles
      document.getElementById('notationX1X2').addEventListener('click', () => {
        state.notation = 'x1x2';
        document.getElementById('notationX1X2').className = "px-2.5 py-1 rounded bg-violet-600 text-white font-mono text-[11px] shadow-sm font-semibold";
        document.getElementById('notationXY').className = "px-2.5 py-1 rounded text-slate-600 dark:text-slate-400 hover:text-violet-700 dark:hover:text-white font-mono text-[11px]";
        document.getElementById('labelX1').textContent = "a₁ coordinate (x₁):";
        document.getElementById('labelX2').textContent = "a₂ coordinate (x₂):";
        const l3 = document.getElementById('labelX3');
        if (l3) l3.textContent = "a₃ coordinate (x₃):";
        document.getElementById('dfdx1_title').textContent = "∂f / ∂x₁ :";
        document.getElementById('dfdx2_title').textContent = "∂f / ∂x₂ :";
        const d3 = document.getElementById('dfdx3_title');
        if (d3) d3.textContent = "∂f / ∂x₃ :";
        compileExpressions();
        renderPlots(true);
      });
      document.getElementById('notationXY').addEventListener('click', () => {
        state.notation = 'xy';
        document.getElementById('notationXY').className = "px-2.5 py-1 rounded bg-violet-600 text-white font-mono text-[11px] shadow-sm font-semibold";
        document.getElementById('notationX1X2').className = "px-2.5 py-1 rounded text-slate-600 dark:text-slate-400 hover:text-violet-700 dark:hover:text-white font-mono text-[11px]";
        document.getElementById('labelX1').textContent = "a coordinate (x):";
        document.getElementById('labelX2').textContent = "b coordinate (y):";
        const l3 = document.getElementById('labelX3');
        if (l3) l3.textContent = "c coordinate (z):";
        document.getElementById('dfdx1_title').textContent = "∂f / ∂x :";
        document.getElementById('dfdx2_title').textContent = "∂f / ∂y :";
        const d3 = document.getElementById('dfdx3_title');
        if (d3) d3.textContent = "∂f / ∂z :";
        compileExpressions();
        renderPlots(true);
      });

      // Domain inputs
      const updateDomainFromInputs = () => {
        const xMin = parseFloat(document.getElementById("xMin").value) || -6;
        const xMax = parseFloat(document.getElementById("xMax").value) || 6;
        const yMin = parseFloat(document.getElementById("yMin").value) || -6;
        const yMax = parseFloat(document.getElementById("yMax").value) || 6;
        state.x_range = [Math.min(xMin, xMax - 0.5), Math.max(xMax, xMin + 0.5)];
        state.y_range = [Math.min(yMin, yMax - 0.5), Math.max(yMax, yMin + 0.5)];
        renderPlots(false);
      };
      ["xMin", "xMax", "yMin", "yMax"].forEach(id => {
        document.getElementById(id).addEventListener("change", updateDomainFromInputs);
      });

      // Visual styling
      document.getElementById("colorScaleSelect").addEventListener("change", (e) => {
        state.color_scale = e.target.value;
        renderPlots(true);
      });
      document.getElementById("opacitySlider").addEventListener("input", (e) => {
        state.opacity = parseFloat(e.target.value);
        renderPlots(true);
      });

      // Presets
      document.getElementById("presetSelect").addEventListener("change", (e) => {
        const pKey = e.target.value;
        const preset = presets[pKey];
        if (!preset) return;

        state.f_expr_raw = preset.expr;
        document.getElementById("functionInput").value = preset.expr;
        if (preset.c !== undefined) {
          state.level_c = preset.c;
          document.getElementById("levelValueC").value = preset.c;
          document.getElementById("levelSliderC").value = preset.c;
        }
        if (preset.r !== undefined) {
          state.radius_r = preset.r;
          document.getElementById("radiusInputR").value = preset.r;
        }
        if (preset.x0 !== undefined) state.x0 = preset.x0;
        if (preset.y0 !== undefined) state.y0 = preset.y0;
        if (preset.z0 !== undefined) state.z0 = preset.z0; else state.z0 = 0.0;
        if (preset.constraint !== undefined) {
          state.constraint_raw = preset.constraint;
          const cInp = document.getElementById("constraintInput");
          if (cInp) cInp.value = preset.constraint;
        } else {
          state.constraint_raw = "";
          const cInp = document.getElementById("constraintInput");
          if (cInp) cInp.value = "";
        }
        if (preset.x) {
          state.x_range = preset.x;
          syncDomainInputs();
        }
        if (preset.y) {
          state.y_range = preset.y;
          syncDomainInputs();
        }
        if (preset.mode) setViewMode(preset.mode);

        compileExpressions();
        setEvaluationPoint(state.x0, state.y0, state.z0);
        renderPlots(false);
      });

      // Constraint Input & Chips Listeners
      let constraintDebounce = null;
      document.getElementById("constraintInput")?.addEventListener("input", (e) => {
        clearTimeout(constraintDebounce);
        constraintDebounce = setTimeout(() => {
          state.constraint_raw = e.target.value;
          compileExpressions();
          renderPlots(true);
        }, 200);
      });

      document.querySelectorAll(".constraint-chip").forEach(btn => {
        btn.addEventListener("click", () => {
          const val = btn.getAttribute("data-val") || btn.textContent;
          const input = document.getElementById("constraintInput");
          if (input) input.value = val;
          state.constraint_raw = val;
          compileExpressions();
          renderPlots(true);
        });
      });

      document.getElementById("clearConstraintBtn")?.addEventListener("click", () => {
        const input = document.getElementById("constraintInput");
        if (input) input.value = "";
        state.constraint_raw = "";
        compileExpressions();
        renderPlots(true);
      });

      document.getElementById("showConstraintSurface")?.addEventListener("change", (e) => {
        state.show_constraint_surface = e.target.checked;
        renderPlots(true);
      });

      document.getElementById("showConstraintCurve")?.addEventListener("change", (e) => {
        state.show_constraint_curve = e.target.checked;
        renderPlots(true);
      });

      document.getElementById("tab1GoToConstraintBtn")?.addEventListener("click", () => {
        switchTab("tabNavFunctions", "tabContentFunctions");
        setTimeout(() => {
          const input = document.getElementById("constraintInput");
          if (input) {
            input.focus();
            input.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }, 100);
      });

      // Fullscreen
      document.getElementById("fullscreenBtn").addEventListener("click", () => {
        const container = document.getElementById("graphContainer");
        if (!document.fullscreenElement) {
          container.requestFullscreen().catch(err => alert(err.message));
        } else {
          document.exitFullscreen();
        }
      });

      // Export PNG
      document.getElementById("exportPngBtn").addEventListener("click", () => {
        const targetDiv = state.view_mode === '3d' ? document.getElementById('plotContainer3D') : document.getElementById('plotContainer2D');
        Plotly.downloadImage(targetDiv, {
          format: 'png', width: 1920, height: 1080, filename: `multivar_${Date.now()}`
        });
      });

      // Share modal
      const shareModal = document.getElementById("shareModal");
      document.getElementById("shareBtn").addEventListener("click", () => {
        const data = {
          f: state.f_expr_raw,
          constraint: state.constraint_raw,
          c: state.level_c,
          r: state.radius_r,
          x0: state.x0,
          y0: state.y0,
          z0: state.z0,
          mode: state.view_mode,
          xr: state.x_range,
          yr: state.y_range,
          theme: state.theme,
          notation: state.notation,
          params: {
            a: state.params.a.val,
            b: state.params.b.val,
            c: state.params.c.val,
            d: state.params.d.val
          },
          toggles: {
            norm: state.show_normal_line,
            tang: state.show_tangent_line,
            grad: state.show_gradient,
            norm3d: state.show_3d_normal_line,
            affine: state.show_affine_plane,
            angle: state.show_right_angle,
            contours: state.show_all_contours
          }
        };
        const hash = encodeURIComponent(JSON.stringify(data));
        // Update URL hash without causing full reload
        if (window.history && window.history.replaceState) {
          window.history.replaceState(null, '', '#' + hash);
        } else {
          window.location.hash = hash;
        }
        const baseHref = window.location.href.split('#')[0];
        const shareUrl = `${baseHref}#${hash}`;
        document.getElementById("shareUrlInput").value = shareUrl;
        document.getElementById("copySuccessMsg").classList.add("hidden");
        shareModal.classList.remove("hidden");
      });
      document.getElementById("closeShareModal").addEventListener("click", () => shareModal.classList.add("hidden"));
      document.getElementById("copyShareUrlBtn").addEventListener("click", () => {
        const input = document.getElementById("shareUrlInput");
        input.select();
        navigator.clipboard.writeText(input.value).then(() => {
          document.getElementById("copySuccessMsg").classList.remove("hidden");
        });
      });
    }

    // -------------------------------------------------------------------------
    // Mobile Layout Management (Graph View <-> Controls View)
    // -------------------------------------------------------------------------
    let mobileActiveTab = 'graph';

    function setMobileView(view) {
      mobileActiveTab = view;
      const graphBtn = document.getElementById('mobileViewGraphBtn');
      const controlsBtn = document.getElementById('mobileViewControlsBtn');
      const controlsPanel = document.getElementById('controlsPanel');
      const mainPlot = document.getElementById('mainViewport');

      if (view === 'graph') {
        if (graphBtn) graphBtn.className = "flex-1 py-1.5 px-2 rounded-lg transition flex items-center justify-center space-x-1.5 bg-violet-600 text-white shadow-sm font-bold";
        if (controlsBtn) controlsBtn.className = "flex-1 py-1.5 px-2 rounded-lg transition flex items-center justify-center space-x-1.5 text-slate-700 dark:text-purple-200 hover:text-violet-700";
        
        if (window.innerWidth < 1024) {
          if (controlsPanel) {
            controlsPanel.classList.add('hidden');
            controlsPanel.classList.remove('flex');
          }
          if (mainPlot) {
            mainPlot.classList.remove('hidden');
            mainPlot.classList.add('flex');
          }
        }
        
        setTimeout(() => {
          Plotly.Plots.resize('plotContainer2D');
          if (document.getElementById('plotContainer3D')) {
            Plotly.Plots.resize('plotContainer3D');
          }
        }, 60);
      } else {
        if (controlsBtn) controlsBtn.className = "flex-1 py-1.5 px-2 rounded-lg transition flex items-center justify-center space-x-1.5 bg-violet-600 text-white shadow-sm font-bold";
        if (graphBtn) graphBtn.className = "flex-1 py-1.5 px-2 rounded-lg transition flex items-center justify-center space-x-1.5 text-slate-700 dark:text-purple-200 hover:text-violet-700";
        
        if (window.innerWidth < 1024) {
          if (controlsPanel) {
            controlsPanel.classList.remove('hidden');
            controlsPanel.classList.add('flex');
          }
          if (mainPlot) {
            mainPlot.classList.add('hidden');
            mainPlot.classList.remove('flex');
          }
        }
      }
    }

    function initMobileLayout() {
      const graphBtn = document.getElementById('mobileViewGraphBtn');
      const controlsBtn = document.getElementById('mobileViewControlsBtn');
      const switchFromControlsBtn = document.getElementById('mobileViewGraphFromControlsBtn');

      if (graphBtn) graphBtn.addEventListener('click', () => setMobileView('graph'));
      if (controlsBtn) controlsBtn.addEventListener('click', () => setMobileView('controls'));
      if (switchFromControlsBtn) switchFromControlsBtn.addEventListener('click', () => setMobileView('graph'));

      window.addEventListener('resize', () => {
        const controlsPanel = document.getElementById('controlsPanel');
        const mainPlot = document.getElementById('mainViewport');
        if (window.innerWidth >= 1024) {
          if (controlsPanel) {
            controlsPanel.classList.remove('hidden');
            controlsPanel.classList.add('flex');
          }
          if (mainPlot) {
            mainPlot.classList.remove('hidden');
            mainPlot.classList.add('flex');
          }
        } else {
          setMobileView(mobileActiveTab);
        }
        Plotly.Plots.resize('plotContainer2D');
        if (document.getElementById('plotContainer3D')) {
          Plotly.Plots.resize('plotContainer3D');
        }
      });
    }

    // -------------------------------------------------------------------------
    // AI Calculus Tutor Engine & Context Analyzer
    // -------------------------------------------------------------------------
    function getLiveGraphContext() {
      const ptA = evaluateAt(state.x0, state.y0);
      const mag = Math.sqrt(ptA.fx * ptA.fx + ptA.fy * ptA.fy);
      const affineVal = evaluateAffineAt(state.test_x, state.test_y);
      const exactVal = evaluateAt(state.test_x, state.test_y).z;
      const approxErr = Math.abs(exactVal - affineVal);

      // Second order partial derivatives via finite differences
      const h = 1e-4;
      const p_r = evaluateAt(state.x0 + h, state.y0);
      const p_l = evaluateAt(state.x0 - h, state.y0);
      const p_u = evaluateAt(state.x0, state.y0 + h);
      const p_d = evaluateAt(state.x0, state.y0 - h);

      const f_xx = (p_r.fx - p_l.fx) / (2 * h);
      const f_yy = (p_u.fy - p_d.fy) / (2 * h);
      const f_xy = (p_u.fx - p_d.fx) / (2 * h);
      const D_hessian = f_xx * f_yy - f_xy * f_xy;

      let extremumType = 'none';
      if (mag < 1e-3) {
        if (D_hessian > 1e-5 && f_xx > 0) extremumType = 'local_min';
        else if (D_hessian > 1e-5 && f_xx < 0) extremumType = 'local_max';
        else if (D_hessian < -1e-5) extremumType = 'saddle';
        else extremumType = 'inconclusive';
      }

      const v1 = state.notation === 'x1x2' ? 'x_1' : 'x';
      const v2 = state.notation === 'x1x2' ? 'x_2' : 'y';

      return {
        formula: state.f_expr_raw,
        constraint: state.constraint_raw,
        has_constraint: Boolean((state.constraint_raw || "").trim()),
        point_a: [state.x0, state.y0],
        f_at_a: ptA.z,
        derivatives: { fx: ptA.fx, fy: ptA.fy },
        gradient_vector: [ptA.fx, ptA.fy],
        gradient_magnitude: mag,
        derivative_matrix: [ptA.fx, ptA.fy],
        normal_vector_2d: mag > 1e-4 ? [ptA.fx / mag, ptA.fy / mag] : [0, 0],
        tangent_vector_2d: mag > 1e-4 ? [-ptA.fy / mag, ptA.fx / mag] : [0, 0],
        surface_normal_3d: [-ptA.fx, -ptA.fy, 1],
        level_c: state.level_c,
        radius_r: state.radius_r,
        level_diff: Math.abs(ptA.z - state.level_c),
        test_point: [state.test_x, state.test_y],
        test_exact: exactVal,
        test_affine: affineVal,
        test_error: approxErr,
        hessian: { f_xx, f_yy, f_xy, det: D_hessian },
        extremumType,
        v1,
        v2
      };
    }

    function renderMarkdownAndMath(text) {
      const mathBlocks = [];
      // 1. Extract and render $$...$$
      let processed = text.replace(/\$\$([\s\S]*?)\$\$/g, (match, math) => {
        try {
          const rendered = katex.renderToString(math.trim(), { displayMode: true, throwOnError: false });
          mathBlocks.push(rendered);
          return `%%MATHBLOCK_${mathBlocks.length - 1}%%`;
        } catch {
          return match;
        }
      });

      // 2. Extract and render $...$
      processed = processed.replace(/\$([^\$\n]+?)\$/g, (match, math) => {
        try {
          const rendered = katex.renderToString(math.trim(), { displayMode: false, throwOnError: false });
          mathBlocks.push(rendered);
          return `%%MATHBLOCK_${mathBlocks.length - 1}%%`;
        } catch {
          return match;
        }
      });

      // 3. Escape HTML
      let html = processed
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

      // 4. Headings & Markdown elements
      html = html.replace(/^### (.*$)/gim, '<h4 class="font-bold text-violet-900 dark:text-cyan-300 text-xs mt-2 mb-1">$1</h4>');
      html = html.replace(/^#### (.*$)/gim, '<h5 class="font-bold text-slate-800 dark:text-purple-200 text-xs mt-1.5 mb-0.5">$1</h5>');
      html = html.replace(/^\s*[-*]\s+(.*$)/gim, '<div class="flex items-start space-x-1.5 ml-1 my-0.5"><span class="text-violet-500 font-bold">•</span><span>$1</span></div>');
      html = html.replace(/^\s*(\d+)\.\s+(.*$)/gim, '<div class="flex items-start space-x-1.5 ml-1 my-0.5"><span class="text-violet-600 dark:text-cyan-400 font-bold">$1.</span><span>$2</span></div>');
      html = html.replace(/\*\*([^*]+)\*\*/g, '<strong class="text-violet-900 dark:text-white font-bold">$1</strong>');
      html = html.replace(/\*([^*]+)\*/g, '<em class="text-slate-600 dark:text-purple-300">$1</em>');
      html = html.replace(/`([^`]+)`/g, '<code class="bg-violet-100 dark:bg-purple-900/60 px-1 py-0.5 rounded text-violet-800 dark:text-purple-200 font-mono text-[11px]">$1</code>');
      html = html.replace(/\n\n/g, '<div class="h-2"></div>');
      html = html.replace(/\n/g, '<br>');

      // 5. Restore KaTeX HTML
      html = html.replace(/%%MATHBLOCK_(\d+)%%/g, (match, index) => {
        return mathBlocks[parseInt(index)] || '';
      });

      return html;
    }

    function showToast(msg) {
      const toast = document.getElementById("graphActionToast");
      const text = document.getElementById("graphActionToastText");
      if (!toast || !text) return;
      text.textContent = msg;
      toast.classList.remove("opacity-0", "translate-y-[-20px]", "pointer-events-none");
      toast.classList.add("opacity-100", "translate-y-0");
      setTimeout(() => {
        toast.classList.remove("opacity-100", "translate-y-0");
        toast.classList.add("opacity-0", "translate-y-[-20px]", "pointer-events-none");
      }, 3500);
    }

    function applyGraphAction(action) {
      if (!action || typeof action !== 'object') return false;
      let applied = false;
      const changes = [];

      const expr = action.f || action.expr;
      if (expr && typeof expr === 'string') {
        state.f_expr_raw = expr;
        const fInp = document.getElementById("functionInput");
        if (fInp) fInp.value = expr;
        applied = true;
        changes.push(`f = ${expr}`);
      }

      const constraint = action.constraint || action.requirement || action.req;
      if (constraint !== undefined && typeof constraint === 'string') {
        state.constraint_raw = constraint;
        const cInp = document.getElementById("constraintInput");
        if (cInp) cInp.value = constraint;
        applied = true;
        changes.push(`req: ${constraint}`);
      }

      if (action.c !== undefined && !isNaN(Number(action.c))) {
        state.level_c = parseFloat(action.c);
        const cVal = document.getElementById("levelValueC");
        const cSld = document.getElementById("levelSliderC");
        if (cVal) cVal.value = state.level_c.toFixed(1);
        if (cSld) cSld.value = state.level_c;
        applied = true;
        changes.push(`c = ${state.level_c}`);
      }

      if (action.r !== undefined && !isNaN(Number(action.r))) {
        state.radius_r = parseFloat(action.r);
        const rInp = document.getElementById("radiusInputR");
        if (rInp) rInp.value = state.radius_r.toFixed(2);
      } else if (state.level_c >= 0) {
        state.radius_r = Math.sqrt(state.level_c);
        const rInp = document.getElementById("radiusInputR");
        if (rInp) rInp.value = state.radius_r.toFixed(2);
      }

      const pointA = action.point_a || action.a;
      if (Array.isArray(pointA) && pointA.length >= 2) {
        state.x0 = parseFloat(pointA[0]);
        state.y0 = parseFloat(pointA[1]);
        const x0Inp = document.getElementById("x0Input");
        const y0Inp = document.getElementById("y0Input");
        const x0Sld = document.getElementById("x0Slider");
        const y0Sld = document.getElementById("y0Slider");
        if (x0Inp) x0Inp.value = state.x0.toFixed(2);
        if (y0Inp) y0Inp.value = state.y0.toFixed(2);
        if (x0Sld) x0Sld.value = state.x0;
        if (y0Sld) y0Sld.value = state.y0;
        if (pointA.length >= 3) {
          state.z0 = parseFloat(pointA[2]);
          const z0Inp = document.getElementById("z0Input");
          const z0Sld = document.getElementById("z0Slider");
          if (z0Inp) z0Inp.value = state.z0.toFixed(2);
          if (z0Sld) z0Sld.value = state.z0;
          changes.push(`a = (${state.x0.toFixed(2)}, ${state.y0.toFixed(2)}, ${state.z0.toFixed(2)})`);
        } else {
          changes.push(`a = (${state.x0.toFixed(2)}, ${state.y0.toFixed(2)})`);
        }
        applied = true;
      }

      const vMode = action.mode || action.view_mode;
      if (vMode && ['2d', '3d', 'split'].includes(vMode)) {
        setViewMode(vMode);
        applied = true;
      }

      const xRange = action.xr || action.x_range;
      if (Array.isArray(xRange) && xRange.length === 2) {
        state.x_range = [parseFloat(xRange[0]), parseFloat(xRange[1])];
        applied = true;
      }
      const yRange = action.yr || action.y_range;
      if (Array.isArray(yRange) && yRange.length === 2) {
        state.y_range = [parseFloat(yRange[0]), parseFloat(yRange[1])];
        applied = true;
      }

      if (action.toggles && typeof action.toggles === 'object') {
        const t = action.toggles;
        if (t.show_gradient !== undefined) {
          state.show_gradient = Boolean(t.show_gradient);
          const el = document.getElementById('showGradientVector');
          if (el) el.checked = state.show_gradient;
        }
        if (t.show_normal_line !== undefined) {
          state.show_normal_line = Boolean(t.show_normal_line);
          const el = document.getElementById('showNormalLine');
          if (el) el.checked = state.show_normal_line;
        }
        if (t.show_tangent_line !== undefined) {
          state.show_tangent_line = Boolean(t.show_tangent_line);
          const el = document.getElementById('showTangentLine');
          if (el) el.checked = state.show_tangent_line;
        }
        if (t.show_affine_plane !== undefined) {
          state.show_affine_plane = Boolean(t.show_affine_plane);
          const el = document.getElementById('showAffinePlane');
          if (el) el.checked = state.show_affine_plane;
        }
      }

      if (applied) {
        compileExpressions();
        setEvaluationPoint(state.x0, state.y0, state.z0);
        syncDomainInputs();
        updateCalculusCalculations();
        updateAffineCalculations();
        updateHessianCalculations();
        renderPlots(false);

        const toastMsg = action.description || action.summary || `Applied: ${changes.join(', ')}`;
        showToast(toastMsg);
      }
      return applied;
    }

    window.reapplyAiAction = function(encoded) {
      try {
        const action = JSON.parse(decodeURIComponent(encoded));
        applyGraphAction(action);
      } catch (err) {
        console.warn("Could not reapply AI action:", err);
      }
    };

    function extractAndApplyGraphAction(rawText) {
      if (!rawText) return { cleanText: '', action: null };
      let cleanText = rawText;
      let matchedAction = null;

      // 1. Try to find ```graph_action ... ```
      const actionBlockRegex = /```graph_action\s*([\s\S]*?)(?:```|$)/i;
      const match = cleanText.match(actionBlockRegex);
      if (match) {
        try {
          const rawJson = match[1].trim().replace(/```$/, '').trim();
          matchedAction = JSON.parse(rawJson);
        } catch (e) {
          console.warn("Failed to parse graph_action block:", e);
        }
      }

      // 2. If not found, try to find ```json with action/f/point_a
      if (!matchedAction) {
        const jsonBlockRegex = /```(?:json)?\s*(\{[\s\S]*?(?:"action"\s*:\s*"update_graph"|"f"\s*:|"point_a"\s*:)[\s\S]*?\})(?:```|$)/i;
        const jsonMatch = cleanText.match(jsonBlockRegex);
        if (jsonMatch) {
          try {
            matchedAction = JSON.parse(jsonMatch[1].trim());
          } catch (e) {}
        }
      }

      // 3. If not found, try to find raw JSON at the end
      if (!matchedAction) {
        const rawJsonRegex = /(\{[\s\r\n]*"(?:action|f|point_a)"[\s\S]*?\})\s*$/i;
        const rawMatch = cleanText.match(rawJsonRegex);
        if (rawMatch) {
          try {
            matchedAction = JSON.parse(rawMatch[1].trim());
          } catch (e) {}
        }
      }

      // Apply the action automatically to inputs and live graph
      if (matchedAction) {
        applyGraphAction(matchedAction);
      }

      // Completely hide and strip all code blocks, action json, and raw tags from visible chat text
      cleanText = cleanText
        .replace(/```graph_action[\s\S]*?(?:```|$)/gi, '')
        .replace(/```(?:json)?\s*\{[\s\S]*?(?:"action"|"update_graph"|"point_a"|"f"\s*:)[\s\S]*?\}(?:```|$)/gi, '')
        .replace(/```(?:json)?\s*\{[\s\S]*?$/gi, '')
        .replace(/<div[\s\S]*?(?:<\/div>|$)/gi, '')
        .trim();

      return { cleanText, action: matchedAction };
    }

    function generateLocalAIResponse(query, ctx) {
      const q = query.toLowerCase();
      const v1 = ctx.v1;
      const v2 = ctx.v2;
      const a1 = ctx.point_a[0].toFixed(2);
      const a2 = ctx.point_a[1].toFixed(2);
      const fa = ctx.f_at_a.toFixed(3);
      const fx = ctx.derivatives.fx.toFixed(3);
      const fy = ctx.derivatives.fy.toFixed(3);
      const mag = ctx.gradient_magnitude.toFixed(3);

      // 0. Request for cylinder / constraint / free variable in R3
      if (q.includes('cylinder') || q.includes('цилиндр') || q.includes('requirement') || q.includes('constraint') || q.includes('domain') || q.includes('ограничение') || q.includes('free variable') || q.includes('x1^2/4')) {
        const isParabola = q.includes('parabol') || q.includes('парабол') || q.includes('+ x2 =') || q.includes('+x2=');
        const fVec = "[x1; x2; x3]";
        const reqStr = isParabola ? "x1^2 / 4 + x2 = 1" : "x1^2 / 4 + x2^2 / 9 = 1";
        const cylName = isParabola ? "Parabolic Cylinder" : "Elliptic Cylinder";
        const cylEq = isParabola ? "\\frac{x_1^2}{4} + x_2 = 1" : "\\frac{x_1^2}{4} + \\frac{x_2^2}{9} = 1";

        return `### 🏛️ ${cylName} in $\\mathbb{R}^3$ via Free Variable $x_3$

In multivariable calculus and $\\mathbb{R}^3$ geometry, an equation involving only two coordinates (such as $x_1$ and $x_2$) defines a **cylindrical surface**:
$$${cylEq}$$

- **Free Variable $x_3$:** The coordinate $x_3$ does not appear in the constraint equation. Therefore, $x_3$ can take **any real value** ($-\\infty < x_3 < \\infty$).
- **Geometric Construction:** The 2D cross-section curve in the $(x_1, x_2)$ plane is extruded vertically along the entire $x_3$ axis, forming a cylinder parallel to $x_3$.
- **Parametric Identity Vector:** With $\\mathbf{F}(x_1, x_2, x_3) = \\begin{bmatrix} x_1 \\\\ x_2 \\\\ x_3 \\end{bmatrix}$ and requirement $${cylEq}$, the 3D viewport plots the continuous 3D cylinder surface!

I have applied the identity vector field $\\mathbf{F} = [x_1; x_2; x_3]$ and requirement \`${reqStr}\` into your inputs:

\`\`\`graph_action
{
  "action": "update_graph",
  "description": "${cylName} in R3",
  "f": "${fVec}",
  "constraint": "${reqStr}",
  "mode": "3d",
  "xr": [-5, 5],
  "yr": [-5, 5]
}
\`\`\``;
      }

      // 1. Request to create ellipse
      if (q.includes('ellipse') || q.includes('еллипс') || q.includes('эллипс')) {
        return `### 🪐 Ellipse Level Set & Quadratic Form

An **ellipse** in the $(${v1}, ${v2})$ plane is represented by the quadratic equation:
$$\\frac{${v1}^2}{A^2} + \\frac{${v2}^2}{B^2} = c$$

Configured here with semi-axes $A = 2$ and $B = 3$:
$$f(${v1}, ${v2}) = \\frac{${v1}^2}{4} + \\frac{${v2}^2}{9}$$

At level value $c = 1.0$, the level curve $f^{-1}(1)$ forms the exact ellipse with horizontal radius $2$ and vertical radius $3$.
- **Derivative Matrix:** $\\mathbf{D}f(${v1}, ${v2}) = \\begin{bmatrix} \\frac{${v1}}{2} & \\frac{2${v2}}{9} \\end{bmatrix}_{1 \\times 2}$
- **Gradient Vector:** $\\nabla f(\\mathbf{a})$ points outward along the normal line, perpendicular ($90^\\circ$) to the tangent line of the ellipse!

I have automatically inserted these parameters into your graph inputs!

\`\`\`graph_action
{
  "action": "update_graph",
  "description": "Ellipse with semi-axes A=2, B=3 at level c=1",
  "f": "x1^2 / 4 + x2^2 / 9",
  "c": 1.0,
  "point_a": [1.0, 1.5],
  "mode": "split",
  "xr": [-6, 6],
  "yr": [-6, 6]
}
\`\`\``;
      }

      // 2. Request to create saddle
      if (q.includes('saddle') || q.includes('седло') || q.includes('гипербол')) {
        return `### 🐎 Saddle Surface (Hyperbolic Paraboloid)

A **hyperbolic paraboloid** is the quintessential saddle surface:
$$f(${v1}, ${v2}) = ${v1}^2 - ${v2}^2$$

- Along $x_2 = 0$, the trace is an upward parabola $z = ${v1}^2$.
- Along $x_1 = 0$, the trace is a downward parabola $z = -${v2}^2$.
- At $(0, 0)$, the Hessian determinant is $D = (2)(-2) - 0 = -4 < 0$, confirming a **saddle point**.
- The level curves ${v1}^2 - ${v2}^2 = c$ are hyperbolas asymptotic to $x_1 = \\pm x_2$.

I have automatically inserted these parameters into your graph inputs!

\`\`\`graph_action
{
  "action": "update_graph",
  "description": "Saddle Surface x1^2 - x2^2",
  "f": "x1^2 - x2^2",
  "c": 1.0,
  "point_a": [1.414, 1.0],
  "mode": "split",
  "xr": [-5, 5],
  "yr": [-5, 5]
}
\`\`\``;
      }

      // 3. Request to create circle
      if (q.includes('circle') || q.includes('круг') || q.includes('окружност')) {
        return `### ⭕ Circle Level Set $x_1^2 + x_2^2 = c$

A **circle** with radius $r = 2$ corresponds to:
$$f(${v1}, ${v2}) = ${v1}^2 + ${v2}^2 = r^2 = 4$$

- Level set constant: $c = r^2 = 4.0$.
- Evaluation point $\\mathbf{a} = (2.0, 0.0)$ lies directly on the circle.
- Derivative row matrix: $\\mathbf{D}f(\\mathbf{a}) = [4.0, 0.0]$.
- The gradient vector $\\nabla f(\\mathbf{a})$ points radially outward at a strictly $90^\\circ$ angle to the circle tangent!

I have automatically inserted these parameters into your graph inputs!

\`\`\`graph_action
{
  "action": "update_graph",
  "description": "Circle with radius r=2 (c=4)",
  "f": "x1^2 + x2^2",
  "c": 4.0,
  "r": 2.0,
  "point_a": [2.0, 0.0],
  "mode": "2d",
  "xr": [-6, 6],
  "yr": [-6, 6]
}
\`\`\``;
      }

      // 4. Request to create vector field
      if (q.includes('vector field') || q.includes('векторное поле') || q.includes('[-x2') || q.includes('[x1;')) {
        return `### 🌀 2D Vector Field $\\mathbf{F}(x_1, x_2) = [-x_2, x_1]^T$

This represents a classic **rotational vector field** (counterclockwise circulation):
$$\\mathbf{F}(x_1, x_2) = \\begin{bmatrix} -x_2 \\\\[2pt] x_1 \\end{bmatrix}$$

- **$2 \\times 2$ Jacobian Matrix:**
  $$\\mathbf{J}_F(x_1, x_2) = \\begin{bmatrix} \\frac{\\partial F_1}{\\partial x_1} & \\frac{\\partial F_1}{\\partial x_2} \\\\[4pt] \\frac{\\partial F_2}{\\partial x_1} & \\frac{\\partial F_2}{\\partial x_2} \\end{bmatrix} = \\begin{bmatrix} 0 & -1 \\\\[4pt] 1 & 0 \\end{bmatrix}_{2 \\times 2}$$
- The column vectors of $\\mathbf{J}_F$ are depicted as basis arrows on the canvas, alongside the vector field flow!

I have automatically inserted this vector field into your graph inputs!

\`\`\`graph_action
{
  "action": "update_graph",
  "description": "2D Rotational Vector Field [-x2, x1]",
  "f": "[-x2, x1]",
  "c": 2.0,
  "point_a": [1.0, 1.0],
  "mode": "split",
  "xr": [-5, 5],
  "yr": [-5, 5]
}
\`\`\``;
      }

      // 5. Request to create paraboloid
      if (q.includes('paraboloid') || q.includes('параболоид')) {
        return `### 🥣 Elliptic Paraboloid $z = ${v1}^2 + ${v2}^2$

The standard elliptic paraboloid forms a circular bowl opening upwards:
$$f(${v1}, ${v2}) = ${v1}^2 + ${v2}^2$$

- Global minimum at $(0, 0)$ with $f(0, 0) = 0$.
- Level curves are concentric circles of radius $r = \\sqrt{c}$.

I have automatically inserted these parameters into your graph inputs!

\`\`\`graph_action
{
  "action": "update_graph",
  "description": "Elliptic Paraboloid x1^2 + x2^2",
  "f": "x1^2 + x2^2",
  "c": 4.0,
  "point_a": [1.0, 1.732],
  "mode": "split",
  "xr": [-5, 5],
  "yr": [-5, 5]
}
\`\`\``;
      }

      // Gradient
      if (q.includes('gradient') || q.includes('grad') || q.includes('rate of increase') || q.includes('direction') || q.includes('градиент')) {
        return `### 🎯 Gradient Analysis $\\nabla f$

At evaluation point $\\mathbf{a} = (${a1}, ${a2})$ for function $f(${v1}, ${v2}) = ${ctx.formula}$:

- **Gradient Vector:**
  $$\\nabla f(\\mathbf{a}) = \\begin{bmatrix} \\frac{\\partial f}{\\partial ${v1}} \\\\[4pt] \\frac{\\partial f}{\\partial ${v2}} \\end{bmatrix} = \\begin{bmatrix} ${fx} \\\\[4pt] ${fy} \\end{bmatrix}_{2 \\times 1}$$
- **Magnitude (Length):**
  $$\\|\\nabla f(\\mathbf{a})\\| = \\sqrt{(${fx})^2 + (${fy})^2} = ${mag}$$

#### 💡 Mathematical & Geometric Meaning:
1. **Direction of Steepest Ascent:** The gradient vector $\\nabla f(\\mathbf{a})$ points in the direction where function $f$ increases fastest in the $(${v1}, ${v2})$ plane.
2. **Orthogonality to Level Curve ($90^\\circ$ Angle):** The gradient is always strictly perpendicular to the tangent line of the level curve $f(${v1}, ${v2}) = c$. The 2D unit normal vector is $\\mathbf{n} = \\langle ${ctx.normal_vector_2d[0].toFixed(3)}, ${ctx.normal_vector_2d[1].toFixed(3)} \\rangle$.
3. **Steepness:** The magnitude $\\|\\nabla f\\| = ${mag}$ represents the maximum directional derivative at point $\\mathbf{a}$.`;
      }

      // Affine function / tangent plane
      if (q.includes('affine') || q.includes('tangent plane') || q.includes('approximation') || q.includes('g(x)') || q.includes('linearization') || q.includes('аффин') || q.includes('касательн')) {
        const signA1 = -ctx.point_a[0] >= 0 ? `+ ${(-ctx.point_a[0]).toFixed(2)}` : `- ${ctx.point_a[0].toFixed(2)}`;
        const signA2 = -ctx.point_a[1] >= 0 ? `+ ${(-ctx.point_a[1]).toFixed(2)}` : `- ${ctx.point_a[1].toFixed(2)}`;
        const constTerm = (ctx.f_at_a - ctx.derivatives.fx * ctx.point_a[0] - ctx.derivatives.fy * ctx.point_a[1]).toFixed(2);
        const signConst = parseFloat(constTerm) >= 0 ? `+ ${constTerm}` : `- ${Math.abs(constTerm)}`;

        return `### 📐 Affine Function $g(\\mathbf{x})$ (Tangent Plane)

The affine function is the **best first-order linear approximation** (tangent plane) of $f$ near point $\\mathbf{a} = (${a1}, ${a2})$:

$$g(\\mathbf{x}) = f(\\mathbf{a}) + \\mathbf{D}f(\\mathbf{a})(\\mathbf{x} - \\mathbf{a})$$

#### Exact Formula for Current Graph:
$$g(${v1}, ${v2}) = ${fa} + (${fx})(${v1} ${signA1}) + (${fy})(${v2} ${signA2})$$

Simplified 3D plane equation:
$$z = ${fx}${v1} + ${fy}${v2} ${signConst}$$

#### 🔍 Linearization Test at $\\mathbf{x}_{\\text{test}} = (${ctx.test_point[0]}, ${ctx.test_point[1]})$:
- Exact value: $f(\\mathbf{x}_{\\text{test}}) = ${ctx.test_exact.toFixed(4)}$
- Affine approximation: $g(\\mathbf{x}_{\\text{test}}) = ${ctx.test_affine.toFixed(4)}$
- **Approximation Error:** $|f - g| = ${ctx.test_error.toFixed(4)}$

In 3D space, the graph of $z = g(${v1}, ${v2})$ represents the tangent plane kissing the surface $z = f(${v1}, ${v2})$ tangentially at point $\\mathbf{a}$.`;
      }

      // Normal line / 90 degree angle
      if (q.includes('normal') || q.includes('90') || q.includes('perpendicular') || q.includes('orthogonal') || q.includes('нормал') || q.includes('перпендикуляр')) {
        return `### 🧭 The Normal Line & $90^\\circ$ Orthogonality

The Normal Line is the line passing through point $\\mathbf{a} = (${a1}, ${a2})$ perpendicular to the tangent line (in 2D) or tangent plane (in 3D).

#### 1. In 2D (Level Sets $f = c$):
- Tangent vector to the level curve: $\\mathbf{T} = \\langle -\\frac{\\partial f}{\\partial ${v2}}, \\frac{\\partial f}{\\partial ${v1}} \\rangle = \\langle -${fy}, ${fx} \\rangle$.
- Gradient vector (Normal): $\\nabla f = \\langle ${fx}, ${fy} \\rangle$.
- **Proof of Perpendicularity:**
  $$\\mathbf{T} \\cdot \\nabla f = (-${fy})(${fx}) + (${fx})(${fy}) = 0$$
  Since the dot product equals zero, the angle between the tangent line and the normal line is **strictly $90^\\circ$**!

#### 2. In 3D (Surface $z = f(${v1}, ${v2})$):
- Surface normal vector:
  $$\\mathbf{n}_{3D} = \\langle -\\frac{\\partial f}{\\partial ${v1}}, -\\frac{\\partial f}{\\partial ${v2}}, 1 \\rangle = \\langle -${fx}, -${fy}, 1 \\rangle$$
- The 3D normal line passes through point $(\\mathbf{a}, f(\\mathbf{a}))$ perpendicular to the tangent plane $z = g(\\mathbf{x})$.`;
      }

      // Extremum / critical points / Hessian
      if (q.includes('extremum') || q.includes('minimum') || q.includes('maximum') || q.includes('saddle') || q.includes('critical') || q.includes('hessian') || q.includes('heissian') || q.includes('гессиан') || q.includes('second derivative') || q.includes('min') || q.includes('max') || q.includes('экстремум')) {
        const dHess = ctx.hessian.det.toFixed(3);
        const fxx = ctx.hessian.f_xx.toFixed(3);
        const fyy = ctx.hessian.f_yy.toFixed(3);
        const fxy = ctx.hessian.f_xy.toFixed(3);

        let verdict = '';
        if (ctx.extremumType === 'local_min') {
          verdict = `🟢 **LOCAL MINIMUM**\nBecause $\\nabla f = 0$, discriminant $D = ${dHess} > 0$ and $\\frac{\\partial^2 f}{\\partial ${v1}^2} = ${fxx} > 0$, the surface forms a local cup/basin.`;
        } else if (ctx.extremumType === 'local_max') {
          verdict = `🔴 **LOCAL MAXIMUM**\nBecause $\\nabla f = 0$, discriminant $D = ${dHess} > 0$ and $\\frac{\\partial^2 f}{\\partial ${v1}^2} = ${fxx} < 0$, the surface forms a hilltop peak.`;
        } else if (ctx.extremumType === 'saddle') {
          verdict = `🟡 **SADDLE POINT**\nBecause $\\nabla f = 0$ but discriminant $D = ${dHess} < 0$, the function increases in one direction and decreases in another.`;
        } else if (ctx.gradient_magnitude >= 1e-3) {
          verdict = `⚪ **NOT A CRITICAL POINT**\nThe gradient is non-zero: $\\|\\nabla f\\| = ${mag} \\ne 0$.\nThere is no local extremum here; the function slopes along $\\nabla f = \\langle ${fx}, ${fy} \\rangle$. Move point $\\mathbf{a}$ to where $\\nabla f = 0$ (e.g. $(0, 0)$ for $x_1^2 + x_2^2$) to find an extremum.`;
        } else {
          verdict = `⚪ **INCONCLUSIVE (D = 0)**\nThe second derivative test is inconclusive; higher-order terms must be checked.`;
        }

        return `### 🔍 Local Extrema & Hessian Matrix Analysis

At evaluation point $\\mathbf{a} = (${a1}, ${a2})$:

- **Gradient:** $\\nabla f(\\mathbf{a}) = \\langle ${fx}, ${fy} \\rangle$, $\\|\\nabla f\\| = ${mag}$
- **Second Partial Derivatives:**
  $$f_{${v1}${v1}} = ${fxx},\\quad f_{${v2}${v2}} = ${fyy},\\quad f_{${v1}${v2}} = ${fxy}$$
- **Hessian Determinant (Discriminant $D$):**
  $$D = f_{${v1}${v1}} f_{${v2}${v2}} - (f_{${v1}${v2}})^2 = (${fxx})(${fyy}) - (${fxy})^2 = ${dHess}$$

#### 🏁 Verdict:
${verdict}`;
      }

      // Level Set / c
      if (q.includes('level set') || q.includes('contour') || q.includes('isoline') || q.includes('radius') || q.includes('circle') || q.includes('уровн')) {
        const isOnCurve = ctx.level_diff < 0.05 ? 'lies directly on the level curve ✓' : `is off the level curve (difference $\\Delta = ${ctx.level_diff.toFixed(3)}$)`;
        const radStr = Math.sqrt(Math.max(0, ctx.level_c)).toFixed(2);
        return `### ⭕ Level Set $f^{-1}(c)$

- **Target Level Constant:** $c = ${ctx.level_c.toFixed(2)}$
- **Function Value at $\\mathbf{a}$:** $f(\\mathbf{a}) = ${fa}$
- **Point $\\mathbf{a}$ Status:** Point $\\mathbf{a}$ ${isOnCurve}.

#### 💡 How It Works:
1. The level set $f(${v1}, ${v2}) = c$ is the horizontal slice of the 3D surface at height $z = c$.
2. For circle functions $f = ${v1}^2 + ${v2}^2$, the level set $c = r^2$ forms a circle with radius $r = \\sqrt{c} = ${radStr}$.
3. Click the **"Snap to Curve"** button on the controls panel to project point $\\mathbf{a}$ along the gradient directly onto the level curve!`;
      }

      // Derivative Matrix Df [1 x n]
      if (q.includes('matrix') || q.includes('df') || q.includes('1xn') || q.includes('derivative') || q.includes('dimension') || q.includes('матриц')) {
        return `### 🔢 Total Derivative Matrix $\\mathbf{D}f$ $[1 \\times 2]$

The total derivative (Jacobian) of $f: \\mathbb{R}^2 \\to \\mathbb{R}$ is represented as a **$1 \\times 2$ row matrix**:

$$\\mathbf{D}f(\\mathbf{a}) = \\begin{bmatrix} \\frac{\\partial f}{\\partial ${v1}} & \\frac{\\partial f}{\\partial ${v2}} \\end{bmatrix} = \\begin{bmatrix} ${fx} & ${fy} \\end{bmatrix}_{1 \\times 2}$$

#### 🔄 Dual Relationship with Gradient:
- The gradient $\\nabla f(\\mathbf{a})$ is the **column vector transpose**:
  $$\\nabla f(\\mathbf{a}) = (\\mathbf{D}f(\\mathbf{a}))^T = \\begin{bmatrix} ${fx} \\\\[4pt] ${fy} \\end{bmatrix}_{2 \\times 1}$$
- The derivative maps a displacement vector $\\Delta \\mathbf{x} = \\begin{bmatrix} \\Delta ${v1} \\\\ \\Delta ${v2} \\end{bmatrix}$ via matrix multiplication:
  $$\\Delta f \\approx \\mathbf{D}f(\\mathbf{a}) \\Delta \\mathbf{x} = [${fx} \\;\\; ${fy}] \\begin{bmatrix} \\Delta ${v1} \\\\ \\Delta ${v2} \\end{bmatrix} = (${fx})\\Delta ${v1} + (${fy})\\Delta ${v2}$$`;
      }

      // General fallback in English
      return `### 🤖 Live Graph State for $f(${v1}, ${v2}) = ${ctx.formula}$

Here is the real-time mathematical snapshot from the graph:
- **Function:** $f(${v1}, ${v2}) = ${ctx.formula}$
- **Evaluation Point:** $\\mathbf{a} = (${a1}, ${a2})$, where $f(\\mathbf{a}) = ${fa}$
- **Gradient:** $\\nabla f(\\mathbf{a}) = \\langle ${fx}, ${fy} \\rangle$ (magnitude $\\|\\nabla f\\| = ${mag}$)
- **Derivative Row Matrix:** $\\mathbf{D}f(\\mathbf{a}) = [${fx} \\quad ${fy}]_{1 \\times 2}$
- **Level Set Constant:** $c = ${ctx.level_c.toFixed(2)}$
- **Affine Plane:** $g(\\mathbf{x}) = ${fa} + ${fx}(${v1} - ${a1}) + ${fy}(${v2} - ${a2})$

💬 *Suggested Questions:*
- "Make me an ellipse"
- "Show me a saddle surface"
- "Explain the Hessian matrix and 2nd derivative test"
- "Enter a 3x3 matrix in R3: [1, 2, 3; 4, 5, 6; 7, 8, 9]"
- "Explain the gradient at this point"
- "What does the affine function g(x) represent?"
- "Why is the normal perpendicular at 90 degrees?"`;
    }

    async function checkBackendAiStatus() {
      try {
        const res = await fetch('/api/status');
        if (res.ok) {
          const data = await res.json();
          if (data && data.has_gemini_key) {
            const statusEl = document.getElementById("aiHeaderStatus");
            if (statusEl) statusEl.textContent = `${data.model || 'gemini-3.5-flash-lite'} 🟢 (Render)`;
            const badge = document.getElementById("renderConnectedBadge");
            if (badge) badge.classList.remove("hidden");
            return true;
          }
        }
      } catch (e) {
        // Static server / GitHub Pages
      }
      return false;
    }

    async function askAiAssistant(userQuestion) {
      const ctx = getLiveGraphContext();

      // 1. Try Render Backend proxy first (uses server-configured GEMINI_API_KEY)
      try {
        const backendRes = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: userQuestion,
            context: ctx
          })
        });
        if (backendRes.ok) {
          const backendData = await backendRes.json();
          if (backendData && backendData.reply) {
            const statusEl = document.getElementById("aiHeaderStatus");
            if (statusEl) statusEl.textContent = `${backendData.model || 'gemini-3.5-flash-lite'} 🟢 (Render)`;
            return backendData.reply;
          }
        }
      } catch (err) {
        // Backend not available (e.g. static GitHub Pages)
      }

      // 2. Client-side API key if user provided in local settings
      const apiKey = localStorage.getItem('multivar_gemini_key') || '';
      if (!apiKey) {
        return new Promise(resolve => {
          setTimeout(() => {
            resolve(generateLocalAIResponse(userQuestion, ctx));
          }, 100);
        });
      }

      const systemPrompt = `You are an expert Multivariable Calculus AI Tutor in the MultivarGrapher web app.
IMPORTANT: ALWAYS RESPOND IN ENGLISH.
Use clear, pedagogical explanations with formatted LaTeX math ($...$ for inline and $$...$$ for block equations).

Current live graph state:
- Function: f(${ctx.v1}, ${ctx.v2}) = ${ctx.formula}
- Point a = (${ctx.point_a[0]}, ${ctx.point_a[1]})
- Value f(a) = ${ctx.f_at_a}
- Partial derivatives: df/d${ctx.v1} = ${ctx.derivatives.fx}, df/d${ctx.v2} = ${ctx.derivatives.fy}
- Gradient: ∇f(a) = [${ctx.derivatives.fx}, ${ctx.derivatives.fy}]^T (magnitude = ${ctx.gradient_magnitude})
- Derivative row matrix: Df(a) = [${ctx.derivatives.fx}, ${ctx.derivatives.fy}] [1x2]
- Level set constant c = ${ctx.level_c} (difference at a = ${ctx.level_diff})
- Affine function: g(x) = f(a) + Df(a)(x - a)
- Test point for linearization: (${ctx.test_point[0]}, ${ctx.test_point[1]}), exact = ${ctx.test_exact}, affine = ${ctx.test_affine}, error = ${ctx.test_error}
- Second derivatives: f_11 = ${ctx.hessian.f_xx}, f_22 = ${ctx.hessian.f_yy}, f_12 = ${ctx.hessian.f_xy}, Hessian determinant D = ${ctx.hessian.det}
- Extremum classification: ${ctx.extremumType}

Instructions:
1. Answer the user's question directly in English using LaTeX math equations ($...$ and $$...$$).
2. Ground your answer on the exact function and numeric values provided in the snapshot.
3. Be concise, mathematically accurate, and educational.
4. ACTION EXECUTION: If the user asks to create, plot, or change a function or shape (e.g. "make an ellipse", "show a saddle", "create a circle with radius 2", "plot [-x2, x1]", "set point a to (1, 2)"), in addition to your mathematical explanation in English, YOU MUST output a JSON block at the very end formatted EXACTLY as:
\`\`\`graph_action
{
  "action": "update_graph",
  "description": "Short description of what was set",
  "f": "mathematical expression for f(x1, x2) or vector [f1, f2]",
  "c": 1.0,
  "r": 1.0,
  "point_a": [1.0, 1.5],
  "mode": "split",
  "xr": [-6, 6],
  "yr": [-6, 6],
  "toggles": {
    "show_gradient": true,
    "show_matrix_arrows": true
  }
}
\`\`\`
The application will automatically parse this JSON and insert the values into the web page inputs!`;

      // Models to try in sequence: gemini-3.5-flash-lite first as requested by user
      const candidateModels = [
        'gemini-3.5-flash-lite',
        'gemini-2.5-flash-lite',
        'gemini-2.0-flash',
        'gemini-1.5-flash'
      ];

      for (const model of candidateModels) {
        try {
          const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
          const payload = {
            contents: [
              {
                role: 'user',
                parts: [{ text: `${systemPrompt}\n\nUser Question: ${userQuestion}` }]
              }
            ]
          };

          const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });

          if (res.ok) {
            const data = await res.json();
            const candidateText = data.candidates?.[0]?.content?.parts?.[0]?.text;
            if (candidateText) {
              const statusEl = document.getElementById("aiHeaderStatus");
              if (statusEl) statusEl.textContent = `${model} 🟢`;
              return candidateText;
            }
          }
        } catch (err) {
          console.warn(`Attempt with ${model} failed:`, err);
        }
      }

      // If all models fail, fallback to built-in local engine in English
      return generateLocalAIResponse(userQuestion, ctx) + 
        `\n\n> ⚠️ *(Gemini API returned an error. Answer generated by built-in MultivarGrapher Math Engine. Check your API key in Settings ⚙️)*`;
    }

    function appendChatMessage(sender, text) {
      const container = document.getElementById("aiChatMessages");
      if (!container) return;
      const isUser = sender === 'user';

      const row = document.createElement("div");
      row.className = isUser ? "flex items-start justify-end space-x-2" : "flex items-start space-x-2.5";

      if (!isUser) {
        const avatar = document.createElement("div");
        avatar.className = "w-7 h-7 rounded-xl bg-violet-600 text-white flex items-center justify-center shrink-0 shadow-sm mt-0.5";
        avatar.innerHTML = '<i data-lucide="sparkles" class="w-3.5 h-3.5 text-amber-300"></i>';
        row.appendChild(avatar);
      }

      const bubble = document.createElement("div");
      if (isUser) {
        bubble.className = "bg-gradient-to-r from-violet-600 to-purple-600 text-white p-3 rounded-2xl rounded-tr-sm text-xs max-w-[85%] font-medium shadow-sm leading-relaxed";
        bubble.textContent = text;
      } else {
        bubble.className = "bg-violet-50/90 dark:bg-purple-950/60 p-3 rounded-2xl rounded-tl-sm border border-violet-100 dark:border-purple-900/60 text-slate-800 dark:text-purple-100 max-w-[85%] space-y-1.5 shadow-sm leading-relaxed overflow-x-auto";
        bubble.innerHTML = renderMarkdownAndMath(text);
      }

      row.appendChild(bubble);
      container.appendChild(row);
      container.scrollTop = container.scrollHeight;
      lucide.createIcons();
    }

    function showAiTypingIndicator() {
      const container = document.getElementById("aiChatMessages");
      if (!container || document.getElementById("aiTypingIndicator")) return;
      const ind = document.createElement("div");
      ind.id = "aiTypingIndicator";
      ind.className = "flex items-start space-x-2.5";
      ind.innerHTML = `
        <div class="w-7 h-7 rounded-xl bg-violet-600 text-white flex items-center justify-center shrink-0 shadow-sm mt-0.5">
          <i data-lucide="sparkles" class="w-3.5 h-3.5 text-amber-300"></i>
        </div>
        <div class="bg-violet-50/90 dark:bg-purple-950/60 px-3.5 py-2.5 rounded-2xl rounded-tl-sm border border-violet-100 dark:border-purple-900/60 flex items-center space-x-1.5 shadow-sm">
          <span class="w-2 h-2 rounded-full bg-violet-600 animate-bounce"></span>
          <span class="w-2 h-2 rounded-full bg-purple-600 animate-bounce [animation-delay:0.2s]"></span>
          <span class="w-2 h-2 rounded-full bg-indigo-600 animate-bounce [animation-delay:0.4s]"></span>
        </div>
      `;
      container.appendChild(ind);
      container.scrollTop = container.scrollHeight;
      lucide.createIcons();
    }

    function removeAiTypingIndicator() {
      const ind = document.getElementById("aiTypingIndicator");
      if (ind) ind.remove();
    }

    async function handleUserAiQuery(text) {
      if (!text || !text.trim()) return;
      appendChatMessage('user', text.trim());
      showAiTypingIndicator();
      const answer = await askAiAssistant(text.trim());
      removeAiTypingIndicator();
      const { cleanText } = extractAndApplyGraphAction(answer);
      appendChatMessage('ai', cleanText);
    }

    function updateAiContextStrip() {
      const fEl = document.getElementById("aiCtxFormula");
      const ptEl = document.getElementById("aiCtxPt");
      const cEl = document.getElementById("aiCtxC");
      if (fEl) fEl.textContent = state.f_expr_raw;
      if (ptEl) ptEl.textContent = `(${state.x0.toFixed(1)}, ${state.y0.toFixed(1)})`;
      if (cEl) cEl.textContent = state.level_c.toFixed(1);
    }

    function toggleAiChat() {
      const win = document.getElementById("aiChatWindow");
      if (!win) return;
      const isClosed = win.classList.contains("opacity-0");
      if (isClosed) {
        win.classList.remove("opacity-0", "pointer-events-none", "scale-95");
        win.classList.add("opacity-100", "pointer-events-auto", "scale-100");
        updateAiContextStrip();
        setTimeout(() => {
          const input = document.getElementById("aiChatInput");
          if (input) input.focus();
        }, 120);
      } else {
        win.classList.add("opacity-0", "pointer-events-none", "scale-95");
        win.classList.remove("opacity-100", "pointer-events-auto", "scale-100");
      }
    }

    function initAiChat() {
      const toggleBtn = document.getElementById("toggleAiChatBtn");
      const closeBtn = document.getElementById("closeAiChatBtn");
      const clearBtn = document.getElementById("aiClearBtn");
      const settingsBtn = document.getElementById("aiSettingsBtn");
      const closeSettingsBtn = document.getElementById("closeAiSettingsBtn");
      const saveSettingsBtn = document.getElementById("saveAiSettingsBtn");
      const clearApiKeyBtn = document.getElementById("clearAiApiKeyBtn");
      const sendBtn = document.getElementById("aiChatSendBtn");
      const input = document.getElementById("aiChatInput");
      const refreshBtn = document.getElementById("aiRefreshContextBtn");
      const overlay = document.getElementById("aiSettingsOverlay");
      const keyInput = document.getElementById("geminiApiKeyInput");

      if (toggleBtn) toggleBtn.addEventListener("click", toggleAiChat);
      if (closeBtn) closeBtn.addEventListener("click", toggleAiChat);
      
      if (clearBtn) {
        clearBtn.addEventListener("click", () => {
          const msgs = document.getElementById("aiChatMessages");
          if (msgs) {
            msgs.innerHTML = `
              <div class="flex items-start space-x-2.5">
                <div class="w-7 h-7 rounded-xl bg-violet-600 text-white flex items-center justify-center shrink-0 shadow-sm mt-0.5">
                  <i data-lucide="sparkles" class="w-3.5 h-3.5 text-amber-300"></i>
                </div>
                <div class="bg-violet-50/90 dark:bg-purple-950/60 p-3 rounded-2xl rounded-tl-sm border border-violet-100 dark:border-purple-900/60 text-slate-800 dark:text-purple-100 max-w-[85%] space-y-1.5 shadow-sm">
                  <p class="font-bold text-violet-900 dark:text-cyan-300 text-[11px] uppercase tracking-wider">AI Calculus Assistant</p>
                  <p>Чат очищен. Задайте любой вопрос или нажмите на подсказку ниже!</p>
                </div>
              </div>
            `;
            lucide.createIcons();
          }
        });
      }

      if (settingsBtn && overlay) {
        settingsBtn.addEventListener("click", () => {
          const saved = localStorage.getItem("multivar_gemini_key") || "";
          if (keyInput) keyInput.value = saved;
          overlay.classList.remove("hidden");
        });
      }

      if (closeSettingsBtn && overlay) {
        closeSettingsBtn.addEventListener("click", () => overlay.classList.add("hidden"));
      }

      if (saveSettingsBtn && overlay && keyInput) {
        saveSettingsBtn.addEventListener("click", () => {
          const key = keyInput.value.trim();
          if (key) {
            localStorage.setItem("multivar_gemini_key", key);
            const statusEl = document.getElementById("aiHeaderStatus");
            if (statusEl) statusEl.textContent = "gemini-3.5-flash-lite 🟢";
          } else {
            localStorage.removeItem("multivar_gemini_key");
            const statusEl = document.getElementById("aiHeaderStatus");
            if (statusEl) statusEl.textContent = "Live Graph Synced";
          }
          overlay.classList.add("hidden");
        });
      }

      if (clearApiKeyBtn && keyInput) {
        clearApiKeyBtn.addEventListener("click", () => {
          keyInput.value = "";
          localStorage.removeItem("multivar_gemini_key");
          const statusEl = document.getElementById("aiHeaderStatus");
          if (statusEl) statusEl.textContent = "Live Graph Synced";
          overlay.classList.add("hidden");
        });
      }

      if (refreshBtn) refreshBtn.addEventListener("click", updateAiContextStrip);

      const doSend = () => {
        if (!input) return;
        const txt = input.value;
        input.value = "";
        handleUserAiQuery(txt);
      };

      if (sendBtn) sendBtn.addEventListener("click", doSend);
      if (input) {
        input.addEventListener("keydown", (e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            doSend();
          }
        });
      }

      document.querySelectorAll(".ai-chip").forEach(chip => {
        chip.addEventListener("click", () => {
          const p = chip.getAttribute("data-prompt");
          handleUserAiQuery(p);
        });
      });

      const existingKey = localStorage.getItem("multivar_gemini_key");
      if (existingKey) {
        const headerStatus = document.getElementById("aiHeaderStatus");
        if (headerStatus) headerStatus.textContent = "gemini-3.5-flash-lite 🟢";
      }
    }

    // -------------------------------------------------------------------------
    // App Initialization
    // -------------------------------------------------------------------------
    window.addEventListener("DOMContentLoaded", () => {
      initTheme();
      initSidebarTabs();
      initEvents();
      initMobileLayout();
      initAiChat();
      checkBackendAiStatus();
      loadStateFromHash();
      compileExpressions();
      syncDomainInputs();
      setEvaluationPoint(state.x0, state.y0);
      setViewMode(state.view_mode);
    });

    window.addEventListener("hashchange", () => {
      if (loadStateFromHash()) {
        compileExpressions();
        syncDomainInputs();
        setEvaluationPoint(state.x0, state.y0);
        setViewMode(state.view_mode);
        renderPlots(false);
      }
    });