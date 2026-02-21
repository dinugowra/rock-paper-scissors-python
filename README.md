# Rock Paper Scissors

A small Rock-Paper-Scissors game with both CLI and Tkinter GUI interfaces.

Features
- Play via the command-line (default)
- Launch a simple Tkinter GUI with `--gui`
- Input normalization (full names or `r`/`p`/`s`)
- Score keeping and a GUI reset button

Requirements
- Python 3.8+ (built-in libraries only)
- Tkinter (optional; used only for GUI mode)

Files
- `rock_paper_scissor.py` — main program

Quick run

Run CLI (default):

```bash
python3 rock_paper_scissor.py
```

Run GUI (Tkinter must be available):

```bash
python3 rock_paper_scissor.py --gui
```

If the GUI does not appear, verify Tkinter availability:

```bash
python3 - <<'PY'
try:
    import tkinter as tk
    tk.Tk().destroy()
    print("tkinter OK")
except Exception as e:
    print("tkinter error:", e)
PY
```

Notes
- The program falls back to the CLI when Tkinter is not available or when `--gui` is not provided.
- To exit the CLI, type `q` or `quit`.

Examples
- Play one round on CLI: enter `rock`, `paper`, `scissors`, or `r`/`p`/`s`.
- In GUI, click the choice buttons to play; use "Reset" to clear scores.
