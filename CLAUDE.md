# CLAUDE.md

## Project Overview

Caro AI — a two-player game (Human vs. AI) on a 9×9 board.
Win condition: **4 consecutive pieces** in any direction (horizontal, vertical, diagonal).
AI uses **Minimax** and **Alpha-Beta pruning** with a depth-limited search and heuristic evaluation.

---

## Tech Stack

- **Language:** Python 3.10+
- **UI:** `pygame` (graphical) or `rich` / plain `console` (fallback)
- **No external AI libraries** — algorithms must be implemented from scratch

---

## Project Structure

```
src/
  board.py          # Board state, move generation, win detection
  game.py           # Game loop, turn management
  ai/
    minimax.py      # Minimax algorithm
    alphabeta.py    # Alpha-Beta pruning
    evaluate.py     # Heuristic evaluation function
  ui/
    gui.py          # pygame interface (optional)
    console.py      # Console interface
  benchmark/
    runner.py       # Run both algorithms on test states
    states.py       # Predefined board states for testing
config.py           # Board size, win length, search depth, modes
main.py             # Entry point
report.pdf
README.md
requirements.txt
```

---

## Core Rules

- Board: minimum **9×9**
- Players: `X` (human), `O` (AI), `.` (empty)
- Turns alternate; no placing on occupied cells
- Win: **4 in a row** — no blocked-ends rule
- Draw: board full with no winner

---

## Algorithms

### Minimax
- Recurse to `max_depth`; terminal states return exact scores
- Non-terminal leaf nodes use `evaluate(board)`
- MAX node (AI) → maximise; MIN node (human) → minimise
- Returns `(best_move, score)`

### Alpha-Beta
- Same depth and evaluation function as Minimax
- Prune when `beta <= alpha`
- Returns `(best_move, score)` — must match Minimax result

### Evaluation Function (`evaluate.py`)
- Score open/half-open sequences of 2, 3, 4 pieces in all 4 directions
- Weights: `4-in-a-row > 3-open > 3-half > 2-open ...`
- Separate scoring for AI and human; return `score_ai - score_human`

---

## Metrics to Track (per move)

| Field | Description |
|---|---|
| `algorithm` | `minimax` / `alphabeta` |
| `depth` | Search depth used |
| `move` | `(row, col)` chosen |
| `score` | Evaluated score |
| `states_visited` | Node count |
| `time_ms` | Elapsed time (ms) |

---

## Benchmark

- Minimum **5 predefined board states** in `benchmark/states.py`
- Required states: opening, midgame, AI-can-win, must-block, mutual-attack
- Run both algorithms on each state at depths 1, 2, 3
- Output: comparison table (states visited, time, move chosen, scores match)

---

## Configuration (`config.py`)

```python
BOARD_SIZE   = 9       # Board dimension (N×N)
WIN_LENGTH   = 4       # Consecutive pieces to win
MAX_DEPTH    = 3       # Default search depth
AI_ALGO      = "alphabeta"   # "minimax" | "alphabeta"
CANDIDATE_RADIUS = 1   # Only consider moves adjacent to existing pieces
```

---

## Constraints

- Algorithms must be **self-implemented** — no chess/game libraries
- Minimax and Alpha-Beta must use **identical** evaluation and depth for fair comparison
- All benchmark results must come from **actual runs**, not fabricated data
- Code must be **runnable** (`python main.py`)

---

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Play human vs AI
python main.py

# Run benchmark
python -m benchmark.runner

# Run with specific algorithm and depth
python main.py --algo minimax --depth 3
```

---

## Deliverables

- `src/` — full source code
- `README.md` — setup & run instructions (1–2 pages)
- `report.pdf` — implementation + experimental analysis
- `requirements.txt` — dependencies