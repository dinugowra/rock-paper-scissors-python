"""Rock Paper Scissors

This module provides both a simple CLI and a small Tkinter GUI for playing
Rock-Paper-Scissors against the computer. Use `--gui` to force the GUI; by
default the CLI runs when invoked from a terminal. The program uses only
built-in libraries and is organized into clear functions for testability.
"""
from __future__ import annotations

import argparse
import random
import sys
from typing import Tuple

try:
    import tkinter as tk
except Exception:
    tk = None


# --- Constants and rules ---
CHOICES = ("rock", "paper", "scissors")
# Mapping: choice -> what it defeats
BEATS = {"rock": "scissors", "scissors": "paper", "paper": "rock"}


def normalize_choice(raw: str) -> str | None:
    """Normalize user input to one of CHOICES or return None if invalid.

    Accepts full names or first-letter abbreviations (r/p/s), case-insensitive.
    """
    if not raw:
        return None
    s = raw.strip().lower()
    if s in CHOICES:
        return s
    if s in ("r", "p", "s"):
        return {"r": "rock", "p": "paper", "s": "scissors"}[s]
    return None


def get_computer_choice() -> str:
    """Return a random choice for the computer."""
    return random.choice(CHOICES)


def determine_winner(user_choice: str, computer_choice: str) -> str:
    """Determine the winner.

    Returns one of: 'user', 'computer', 'tie'.
    """
    if user_choice == computer_choice:
        return "tie"
    if BEATS[user_choice] == computer_choice:
        return "user"
    return "computer"


def play_round(user_choice: str) -> Tuple[str, str, str]:
    """Play one round and return (user_choice, computer_choice, winner)."""
    comp = get_computer_choice()
    winner = determine_winner(user_choice, comp)
    return user_choice, comp, winner


# --- CLI Implementation ---
def run_cli() -> None:
    """Run an interactive command-line game loop."""
    user_score = 0
    computer_score = 0
    print("Welcome to Rock Paper Scissors! (type 'q' or 'quit' to exit)")
    while True:
        raw = input("Enter rock, paper, or scissors: ")
        if raw.strip().lower() in ("q", "quit"):
            print("Thanks for playing!")
            break
        user = normalize_choice(raw)
        if user is None:
            print("Invalid choice. Please enter rock/paper/scissors or r/p/s.")
            continue

        user_choice, comp_choice, winner = play_round(user)
        print(f"You chose: {user_choice}")
        print(f"Computer chose: {comp_choice}")

        if winner == "tie":
            print("Result: It's a tie!")
        elif winner == "user":
            print("Result: You win!")
            user_score += 1
        else:
            print("Result: Computer wins!")
            computer_score += 1

        print(f"Score - You: {user_score}, Computer: {computer_score}\n")


# --- GUI Implementation ---
class RPSGameGUI:
    """Simple Tkinter GUI for Rock Paper Scissors."""

    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Rock Paper Scissors")

        self.user_score = 0
        self.computer_score = 0

        self.user_choice_label = tk.Label(master, text="You chose: -")
        self.user_choice_label.pack()

        self.computer_choice_label = tk.Label(master, text="Computer chose: -")
        self.computer_choice_label.pack()

        self.result_label = tk.Label(master, text="Result: -")
        self.result_label.pack()

        self.score_label = tk.Label(master, text="Score - You: 0, Computer: 0")
        self.score_label.pack()

        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        for c in CHOICES:
            btn = tk.Button(button_frame, text=c.capitalize(), width=10, command=lambda c=c: self.play(c))
            btn.pack(side=tk.LEFT, padx=5)

        control_frame = tk.Frame(master)
        control_frame.pack(pady=8)

        tk.Button(control_frame, text="Reset", command=self.reset_scores).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Quit", command=master.quit).pack(side=tk.LEFT, padx=5)

    def play(self, user_choice: str) -> None:
        user_choice, comp_choice, winner = play_round(user_choice)
        self.user_choice_label.config(text=f"You chose: {user_choice}")
        self.computer_choice_label.config(text=f"Computer chose: {comp_choice}")

        if winner == "tie":
            self.result_label.config(text="Result: It's a tie!")
        elif winner == "user":
            self.result_label.config(text="Result: You win!")
            self.user_score += 1
        else:
            self.result_label.config(text="Result: Computer wins!")
            self.computer_score += 1

        self.score_label.config(text=f"Score - You: {self.user_score}, Computer: {self.computer_score}")

    def reset_scores(self) -> None:
        self.user_score = 0
        self.computer_score = 0
        self.score_label.config(text="Score - You: 0, Computer: 0")


def main(argv: list[str] | None = None) -> int:
    """Entry point. Choose GUI or CLI based on arguments and environment.

    Returns exit code (0 on success).
    """
    parser = argparse.ArgumentParser(description="Play Rock Paper Scissors")
    parser.add_argument("--gui", action="store_true", help="Run the Tkinter GUI")
    args = parser.parse_args(argv)

    # Prefer GUI only if requested and available
    if args.gui:
        if not tk:
            print("Tkinter is not available; falling back to CLI.")
            run_cli()
            return 0
        root = tk.Tk()
        # keep window above others briefly on macOS
        try:
            root.lift()
            root.attributes("-topmost", True)
            root.after_idle(root.attributes, "-topmost", False)
        except Exception:
            pass
        app = RPSGameGUI(root)
        root.mainloop()
        return 0

    # Default to CLI mode
    run_cli()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())