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


# --- Score Tracker ---
class ScoreTracker:
    """Track wins, ties, and round history."""

    def __init__(self):
        self.rounds = []  # List of (user_choice, comp_choice, winner)
        self.player_wins = 0
        self.player_ties = 0
        self.computer_wins = 0

    def record_round(self, user_choice: str, comp_choice: str, winner: str) -> None:
        """Record a round result."""
        self.rounds.append((user_choice, comp_choice, winner))
        if winner == "user":
            self.player_wins += 1
        elif winner == "computer":
            self.computer_wins += 1
        else:
            self.player_ties += 1

    def reset(self) -> None:
        """Clear all stats."""
        self.rounds.clear()
        self.player_wins = 0
        self.player_ties = 0
        self.computer_wins = 0

    def format_stats(self) -> str:
        """Return formatted stats string."""
        total = len(self.rounds)
        return f"Player Wins: {self.player_wins} | Ties: {self.player_ties} | Computer Wins: {self.computer_wins} | Total: {total}"


# --- CLI Implementation ---
def run_cli() -> None:
    """Run an interactive command-line game loop."""
    tracker = ScoreTracker()
    print("Welcome to Rock Paper Scissors! (type 'q' or 'quit' to exit)")
    while True:
        raw = input("Enter rock, paper, or scissors: ")
        if raw.strip().lower() in ("q", "quit"):
            print("\nFinal Stats:")
            print(tracker.format_stats())
            print("Thanks for playing!")
            break
        user = normalize_choice(raw)
        if user is None:
            print("Invalid choice. Please enter rock/paper/scissors or r/p/s.")
            continue

        user_choice, comp_choice, winner = play_round(user)
        tracker.record_round(user_choice, comp_choice, winner)
        
        print(f"You chose: {user_choice}")
        print(f"Computer chose: {comp_choice}")

        if winner == "tie":
            print("Result: It's a tie!")
        elif winner == "user":
            print("Result: You win!")
        else:
            print("Result: Computer wins!")

        print(tracker.format_stats())
        print()


# --- GUI Implementation ---
class RPSGameGUI:
    """Simple Tkinter GUI for Rock Paper Scissors."""

    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Rock Paper Scissors")

        self.tracker = ScoreTracker()

        self.user_choice_label = tk.Label(master, text="You chose: -")
        self.user_choice_label.pack()

        self.computer_choice_label = tk.Label(master, text="Computer chose: -")
        self.computer_choice_label.pack()

        self.result_label = tk.Label(master, text="Result: -")
        self.result_label.pack()

        self.scoreboard_label = tk.Label(master, text="Player Wins: 0 | Ties: 0 | Computer Wins: 0 | Total: 0", font=("Arial", 10, "bold"))
        self.scoreboard_label.pack(pady=10)

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
        self.tracker.record_round(user_choice, comp_choice, winner)
        
        self.user_choice_label.config(text=f"You chose: {user_choice}")
        self.computer_choice_label.config(text=f"Computer chose: {comp_choice}")

        if winner == "tie":
            self.result_label.config(text="Result: It's a tie!")
        elif winner == "user":
            self.result_label.config(text="Result: You win!")
        else:
            self.result_label.config(text="Result: Computer wins!")

        self.update_scoreboard()

    def update_scoreboard(self) -> None:
        """Update the scoreboard display."""
        stats = self.tracker.format_stats()
        self.scoreboard_label.config(text=stats)

    def reset_scores(self) -> None:
        self.tracker.reset()
        self.user_choice_label.config(text="You chose: -")
        self.computer_choice_label.config(text="Computer chose: -")
        self.result_label.config(text="Result: -")
        self.scoreboard_label.config(text="Player Wins: 0 | Ties: 0 | Computer Wins: 0 | Total: 0")


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