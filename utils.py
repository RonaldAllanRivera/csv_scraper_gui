# utils.py – User-agent loading and helpers.

import random

def load_user_agents(file_path="user_agents.txt"):
    """Load a list of user-agents from file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("User agents file not found.")
        return ["Mozilla/5.0"]  # fallback
