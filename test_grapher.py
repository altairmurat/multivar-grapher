"""
Verification test suite for MultivarGrapher Calculus Suite (Affine Functions & Normal Lines).
"""

import os
import subprocess
import sys
from pathlib import Path

# Ensure utf-8 stdout on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent

def test_index_html_structure():
    print("Testing index.html integrity...")
    index_path = BASE_DIR / "index.html"
    assert index_path.exists(), f"index.html does not exist at {index_path}!"
    
    content = index_path.read_text(encoding="utf-8")
    required_strings = [
        "plotly",
        "mathjs",
        "katex",
        "functionInput",
        "tabNavAffine",
        "katexAffineVector",
        "katexAffineFormula",
        "showNormalLine",
        "show3DNormalLine",
        "showAffinePlane",
        "testXInput",
        "testYInput",
        "approxValErr",
        "theoryModal",
        "openTheoryBtn",
        "levelValueC",
        "radiusInputR",
        "katexMatrixSymbolic",
        "katexMatrixNumeric",
        "plotContainer2D",
        "plotContainer3D",
        "zoomInBtn",
        "zoomOutBtn"
    ]
    for s in required_strings:
        assert s in content, f"Missing required element/feature in index.html: {s}"
    print("[OK] index.html integrity passed!")

def test_python_plotter():
    print("Testing Python-native Plotly/SymPy plotter...")
    result = subprocess.run(
        [sys.executable, "main.py", "--plot", "--no-browser", "--formula", "x**2 + y**2", "--a", "1.0"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    assert result.returncode == 0, f"Python plotter failed with stderr: {result.stderr}"
    
    exported_plot = BASE_DIR / "multivar_plot.html"
    assert exported_plot.exists(), "multivar_plot.html was not generated!"
    print("[OK] Python plotter generated plot successfully!")
    exported_plot.unlink(missing_ok=True)

def test_deploy_help():
    print("Testing --deploy-help CLI...")
    result = subprocess.run(
        [sys.executable, "main.py", "--deploy-help"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    assert result.returncode == 0, f"--deploy-help failed with stderr: {result.stderr}"
    assert "GITHUB PAGES" in result.stdout
    print("[OK] --deploy-help CLI passed!")

if __name__ == "__main__":
    try:
        test_index_html_structure()
        test_deploy_help()
        test_python_plotter()
        print("\n[SUCCESS] ALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        sys.exit(1)
