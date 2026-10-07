"""
Verification test suite for MultivarGrapher Calculus Suite.
Tests:
1. index.html structure & integrity.
2. Verification that GitHub repository button link is deleted.
3. Verification that URL hash loading (loadStateFromHash) & Render backend status checks exist.
4. Python plotter test.
5. Deploy help CLI test.
6. Render web server /api/status and /api/chat endpoints test.
"""

import os
import subprocess
import sys
import time
import json
import urllib.request
import urllib.error
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
        "zoomOutBtn",
        "themeToggleBtn",
        "mobileViewGraphBtn",
        "mobileViewControlsBtn",
        "toggleAiChatBtn",
        "aiChatWindow",
        "aiChatMessages",
        "aiChatInput",
        "aiChatSendBtn",
        "loadStateFromHash",
        "checkBackendAiStatus",
        "renderConnectedBadge"
    ]
    for s in required_strings:
        assert s in content, f"Missing required element/feature in index.html: {s}"

    # Verify GitHub button has been removed from header
    assert 'href="https://github.com/altairmurat/multivar-grapher"' not in content, (
        "GitHub repository button was NOT removed from index.html header!"
    )
    print("[OK] index.html integrity and GitHub button deletion verified!")

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
    assert "RENDER" in result.stdout
    print("[OK] --deploy-help CLI passed!")

def test_server_api_endpoints():
    print("Testing Render web server /api/status and /api/chat endpoints...")
    test_port = 8765
    server_proc = subprocess.Popen(
        [sys.executable, "main.py", "--host", "127.0.0.1", "--port", str(test_port), "--no-browser"],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        # Give server time to bind
        time.sleep(1.2)
        
        # Test /api/status
        status_url = f"http://127.0.0.1:{test_port}/api/status"
        req = urllib.request.Request(status_url)
        with urllib.request.urlopen(req, timeout=3) as resp:
            assert resp.status == 200
            data = json.loads(resp.read().decode('utf-8'))
            assert data.get("status") == "ok"
            assert data.get("model") == "gemini-3.5-flash-lite"
            print(f" [OK] /api/status responded: {data}")

        # Test /api/chat with missing GEMINI_API_KEY (expects 503 error)
        chat_url = f"http://127.0.0.1:{test_port}/api/chat"
        payload = json.dumps({"message": "What is the gradient?", "context": {}}).encode('utf-8')
        chat_req = urllib.request.Request(chat_url, data=payload, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(chat_req, timeout=3) as resp:
                pass
        except urllib.error.HTTPError as he:
            assert he.code == 503
            err_data = json.loads(he.read().decode('utf-8'))
            assert "GEMINI_API_KEY" in err_data.get("error", "")
            print(f" [OK] /api/chat cleanly reported 503 missing API key requirement: {err_data}")

        # Test static file serving /
        root_url = f"http://127.0.0.1:{test_port}/"
        with urllib.request.urlopen(root_url, timeout=3) as resp:
            assert resp.status == 200
            html_snippet = resp.read(200).decode('utf-8')
            assert "<!DOCTYPE html>" in html_snippet or "<html" in html_snippet
            print(" [OK] Root / correctly serves index.html")

    finally:
        server_proc.terminate()
        try:
            server_proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            server_proc.kill()
    print("[OK] Server API endpoints verified successfully!")

if __name__ == "__main__":
    try:
        test_index_html_structure()
        test_deploy_help()
        test_python_plotter()
        test_server_api_endpoints()
        print("\n[SUCCESS] ALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        sys.exit(1)
