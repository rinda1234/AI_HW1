import json
import threading
import time
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from eightpuzzle import EightPuzzleSearchProblem, createRandomEightPuzzle
from search import astar, bfs, dfs, rand, ucs


HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>8-Puzzle Solver</title>
  <style>
    :root {
      --bg: #f3efe6;
      --panel: rgba(255, 252, 246, 0.92);
      --ink: #1f2937;
      --muted: #6b7280;
      --line: #d6d0c5;
      --tile: #1e5aa8;
      --tile-strong: #17457f;
      --blank: #ece7dd;
      --green: #2f855a;
      --red: #c05621;
      --yellow: #b7791f;
      --shadow: 0 20px 40px rgba(31, 41, 55, 0.12);
      --radius: 22px;
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Pretendard", "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(30, 90, 168, 0.12), transparent 30%),
        radial-gradient(circle at bottom right, rgba(191, 146, 46, 0.12), transparent 25%),
        var(--bg);
      min-height: 100vh;
    }

    .page {
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px;
    }

    .hero {
      background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(248,244,236,0.95));
      border: 1px solid rgba(214, 208, 197, 0.9);
      border-radius: 28px;
      box-shadow: var(--shadow);
      padding: 28px;
      margin-bottom: 20px;
    }

    .hero h1 {
      margin: 0 0 10px;
      font-size: clamp(28px, 4vw, 44px);
      line-height: 1.05;
      letter-spacing: -0.03em;
    }

    .hero p {
      margin: 0;
      color: var(--muted);
      line-height: 1.6;
      max-width: 760px;
    }

    .layout {
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 20px;
      align-items: start;
    }

    .card {
      background: var(--panel);
      border: 1px solid rgba(214, 208, 197, 0.95);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 22px;
      backdrop-filter: blur(10px);
    }

    .card h2 {
      margin: 0 0 16px;
      font-size: 20px;
      letter-spacing: -0.02em;
    }

    .board-wrap {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .board {
      display: grid;
      grid-template-columns: repeat(3, minmax(76px, 1fr));
      gap: 10px;
      width: min(100%, 460px);
      margin: 0 auto;
    }

    .tile {
      aspect-ratio: 1;
      border-radius: 18px;
      display: grid;
      place-items: center;
      font-size: clamp(28px, 4vw, 42px);
      font-weight: 700;
      background: var(--tile);
      color: white;
      border: 2px solid rgba(0, 0, 0, 0.08);
      box-shadow: inset 0 -8px 16px rgba(0,0,0,0.12);
    }

    .tile.blank {
      background: var(--blank);
      color: transparent;
      box-shadow: none;
      border-color: rgba(31, 41, 55, 0.08);
    }

    .controls {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 18px;
    }

    button {
      border: 0;
      border-radius: 14px;
      padding: 14px 16px;
      font: inherit;
      font-weight: 700;
      cursor: pointer;
      color: white;
      background: var(--tile);
      transition: transform 120ms ease, opacity 120ms ease, background 120ms ease;
    }

    button:hover { transform: translateY(-1px); }
    button:disabled { opacity: 0.45; cursor: wait; transform: none; }
    button.alt { background: #2f855a; }
    button.warn { background: #c05621; }
    button.stop { background: #b7791f; }
    button.active { background: var(--tile-strong); }

    .stats {
      display: grid;
      gap: 10px;
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .stat {
      padding: 14px;
      border-radius: 16px;
      background: rgba(255,255,255,0.7);
      border: 1px solid rgba(214, 208, 197, 0.95);
    }

    .stat .label {
      display: block;
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 4px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .stat .value {
      font-size: 18px;
      font-weight: 700;
    }

    .notes {
      margin: 0;
      padding-left: 18px;
      color: var(--muted);
      line-height: 1.65;
    }

    .status-searching { color: var(--yellow); }
    .status-goal { color: var(--green); }
    .status-ready { color: var(--ink); }
    .status-error { color: var(--red); }

    .footer {
      margin-top: 12px;
      color: var(--muted);
      font-size: 14px;
    }

    @media (max-width: 900px) {
      .layout { grid-template-columns: 1fr; }
    }

    @media (max-width: 560px) {
      .page { padding: 14px; }
      .hero, .card { padding: 18px; }
      .controls, .stats { grid-template-columns: 1fr; }
      .board { gap: 8px; }
    }
  </style>
</head>
<body>
  <div class="page">
    <section class="hero">
      <h1>8-Puzzle Solver</h1>
      <p>
        Generate a puzzle, run BFS, UCS, A*, DFS, or Random Search, and watch the
        solution animate directly in your browser. This UI uses the original puzzle
        and search logic from the project and avoids desktop GUI dependencies.
      </p>
    </section>

    <section class="layout">
      <div class="card board-wrap">
        <h2>Board</h2>
        <div id="board" class="board"></div>
      </div>

      <div class="card">
        <h2>Controls</h2>
        <div class="controls" id="controls"></div>

        <h2>Run Status</h2>
        <div class="stats">
          <div class="stat"><span class="label">Status</span><span class="value" id="status">Loading</span></div>
          <div class="stat"><span class="label">Algorithm</span><span class="value" id="algorithm">-</span></div>
          <div class="stat"><span class="label">Path Length</span><span class="value" id="pathLength">0</span></div>
          <div class="stat"><span class="label">Current Step</span><span class="value" id="currentStep">0/0</span></div>
          <div class="stat"><span class="label">Runtime</span><span class="value" id="runtime">-</span></div>
          <div class="stat"><span class="label">Error</span><span class="value" id="error">-</span></div>
        </div>

        <h2 style="margin-top:22px;">Instructions</h2>
        <ul class="notes">
          <li>New Puzzle creates a new randomized board.</li>
          <li>Select an algorithm to compute a full solution.</li>
          <li>Stop pauses only the animation, not the completed search result.</li>
          <li>Reset returns to the original start state of the current puzzle.</li>
        </ul>
        <div class="footer">If the browser does not open automatically, visit <span id="serverUrl"></span>.</div>
      </div>
    </section>
  </div>

  <script>
    const controls = [
      { label: "DFS", key: "dfs" },
      { label: "BFS", key: "bfs" },
      { label: "UCS", key: "ucs" },
      { label: "A*", key: "astar" },
      { label: "Random", key: "rand" },
      { label: "New Puzzle", action: "new", cls: "alt" },
      { label: "Reset", action: "reset", cls: "warn" },
      { label: "Stop", action: "stop", cls: "stop" }
    ];

    const boardEl = document.getElementById("board");
    const controlEl = document.getElementById("controls");
    const statusEl = document.getElementById("status");
    const algorithmEl = document.getElementById("algorithm");
    const pathLengthEl = document.getElementById("pathLength");
    const currentStepEl = document.getElementById("currentStep");
    const runtimeEl = document.getElementById("runtime");
    const errorEl = document.getElementById("error");
    document.getElementById("serverUrl").textContent = window.location.href;

    let uiState = null;
    let animationTimer = null;

    function buildControls() {
      controls.forEach((item) => {
        const button = document.createElement("button");
        button.textContent = item.label;
        if (item.cls) button.classList.add(item.cls);
        button.dataset.key = item.key || "";
        button.addEventListener("click", async () => {
          if (item.action) {
            await post(`/api/${item.action}`, {});
          } else {
            await post("/api/run", { algorithm: item.key });
          }
          await refresh();
        });
        controlEl.appendChild(button);
      });
    }

    function renderBoard(cells) {
      boardEl.innerHTML = "";
      cells.flat().forEach((value) => {
        const tile = document.createElement("div");
        tile.className = "tile" + (value === 0 ? " blank" : "");
        tile.textContent = value === 0 ? "" : String(value);
        boardEl.appendChild(tile);
      });
    }

    function setStatus(state) {
      statusEl.textContent = state.status_text;
      statusEl.className = "value " + state.status_class;
      algorithmEl.textContent = state.stats.algorithm || "-";
      pathLengthEl.textContent = String(state.stats.path_length ?? 0);
      currentStepEl.textContent = `${state.current_step}/${state.stats.path_length ?? 0}`;
      runtimeEl.textContent = state.stats.runtime == null ? "-" : `${state.stats.runtime.toFixed(4)}s`;
      errorEl.textContent = state.search_error || "-";

      document.querySelectorAll("#controls button").forEach((button) => {
        const isSelected = state.selected_algorithm && button.dataset.key === state.selected_algorithm;
        button.classList.toggle("active", isSelected);
        const disableRun = state.running_search && button.dataset.key;
        button.disabled = disableRun;
      });
    }

    function renderState(state) {
      uiState = state;
      renderBoard(state.puzzle.cells);
      setStatus(state);
    }

    async function post(url, payload) {
      await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
    }

    async function refresh() {
      const response = await fetch("/api/state");
      const state = await response.json();
      renderState(state);

      if (animationTimer) {
        clearTimeout(animationTimer);
        animationTimer = null;
      }

      if (state.animating) {
        animationTimer = setTimeout(async () => {
          await post("/api/step", {});
          await refresh();
        }, state.animation_speed);
      }
    }

    buildControls();
    refresh();
    setInterval(refresh, 1200);
  </script>
</body>
</html>
"""


class PuzzleSession:
    def __init__(self):
        self.lock = threading.Lock()
        self.algorithms = {
            "dfs": ("DFS", dfs),
            "bfs": ("BFS", bfs),
            "ucs": ("UCS", ucs),
            "astar": ("A*", astar),
            "rand": ("Random", rand),
        }
        self.search_token = 0
        self._reset_state(new_puzzle=True)

    def _reset_state(self, new_puzzle):
        if new_puzzle or getattr(self, "start_puzzle", None) is None:
            self.start_puzzle = createRandomEightPuzzle(20)
        self.puzzle = self.start_puzzle
        self.problem = EightPuzzleSearchProblem(self.start_puzzle)
        self.solution_path = []
        self.current_step = 0
        self.animating = False
        self.running_search = False
        self.selected_algorithm = None
        self.search_error = None
        self.stats = {"algorithm": None, "path_length": 0, "runtime": None}
        self.animation_speed = 250

    def new_puzzle(self):
        with self.lock:
            self.search_token += 1
            self._reset_state(new_puzzle=True)

    def reset(self):
        with self.lock:
            self.search_token += 1
            self._reset_state(new_puzzle=False)

    def stop(self):
        with self.lock:
            self.animating = False

    def run_algorithm(self, algorithm_key):
        with self.lock:
            if algorithm_key not in self.algorithms or self.running_search:
                return
            self.search_token += 1
            token = self.search_token
            name, func = self.algorithms[algorithm_key]
            self.selected_algorithm = algorithm_key
            self.running_search = True
            self.animating = False
            self.search_error = None
            self.stats = {"algorithm": name, "path_length": 0, "runtime": None}
            self.solution_path = []
            self.current_step = 0
            self.puzzle = self.start_puzzle

        worker = threading.Thread(
            target=self._search_worker,
            args=(token, name, func),
            daemon=True,
        )
        worker.start()

    def _search_worker(self, token, name, func):
        try:
            started = time.perf_counter()
            path = func(self.problem)
            runtime = time.perf_counter() - started
            with self.lock:
                if token != self.search_token:
                    return
                self.solution_path = path
                self.current_step = 0
                self.animating = True
                self.running_search = False
                self.search_error = None
                self.stats = {
                    "algorithm": name,
                    "path_length": len(path),
                    "runtime": runtime,
                }
                self.puzzle = self.start_puzzle
        except Exception as exc:
            with self.lock:
                if token != self.search_token:
                    return
                self.running_search = False
                self.animating = False
                self.search_error = str(exc)

    def step(self):
        with self.lock:
            if not self.animating or self.current_step >= len(self.solution_path):
                self.animating = False
                return
            move = self.solution_path[self.current_step]
            self.puzzle = self.puzzle.result(move)
            self.current_step += 1
            if self.current_step >= len(self.solution_path):
                self.animating = False

    def snapshot(self):
        with self.lock:
            if self.running_search:
                status_text = "Searching..."
                status_class = "status-searching"
            elif self.search_error:
                status_text = "Error"
                status_class = "status-error"
            elif self.puzzle.isGoal():
                status_text = "Goal Reached!"
                status_class = "status-goal"
            else:
                status_text = "Ready"
                status_class = "status-ready"

            return {
                "puzzle": {"cells": [row[:] for row in self.puzzle.cells]},
                "solution_path": list(self.solution_path),
                "current_step": self.current_step,
                "animating": self.animating,
                "running_search": self.running_search,
                "selected_algorithm": self.selected_algorithm,
                "search_error": self.search_error,
                "stats": dict(self.stats),
                "animation_speed": self.animation_speed,
                "status_text": status_text,
                "status_class": status_class,
            }


SESSION = PuzzleSession()


class PuzzleRequestHandler(BaseHTTPRequestHandler):
    def _json_response(self, payload, status=HTTPStatus.OK):
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _html_response(self, payload, status=HTTPStatus.OK):
        encoded = payload.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == "/":
            self._html_response(HTML)
            return
        if self.path == "/api/state":
            self._json_response(SESSION.snapshot())
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length) if content_length else b"{}"
        data = json.loads(raw.decode("utf-8")) if raw else {}

        if self.path == "/api/new":
            SESSION.new_puzzle()
            self._json_response(SESSION.snapshot())
            return
        if self.path == "/api/reset":
            SESSION.reset()
            self._json_response(SESSION.snapshot())
            return
        if self.path == "/api/stop":
            SESSION.stop()
            self._json_response(SESSION.snapshot())
            return
        if self.path == "/api/step":
            SESSION.step()
            self._json_response(SESSION.snapshot())
            return
        if self.path == "/api/run":
            SESSION.run_algorithm(data.get("algorithm", ""))
            self._json_response(SESSION.snapshot())
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def log_message(self, format, *args):
        return


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8001), PuzzleRequestHandler)
    url = "http://127.0.0.1:8000"
    print(f"8-Puzzle UI running at {url}")
    print("Press Ctrl+C to stop the server.")

    opener = threading.Timer(0.6, lambda: webbrowser.open(url))
    opener.daemon = True
    opener.start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
