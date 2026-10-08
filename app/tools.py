import ast
import json
import operator
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import requests

NOTES_FILE = Path("notes.json")

# ---------- Tool 1: Safe calculator ----------
_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.Mod: operator.mod, ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        left, right = _eval(node.left), _eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("Exponent too large")
        return _OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("Unsupported expression")

def calculator(expression: str) -> str:
    """Evaluate a math expression exactly, e.g. '(12 + 8) * 3 / 4'.
    Supports + - * / % ** and parentheses. Use this for ALL arithmetic."""
    try:
        return str(_eval(ast.parse(expression, mode="eval").body))
    except Exception as e:
        return f"Calculator error: {e}"

# ---------- Tool 2: Wikipedia ----------
def wikipedia_search(topic: str) -> str:
    """Look up a factual summary of a topic from Wikipedia.
    Use for definitions, history, science and general knowledge."""
    headers = {"User-Agent": "StudyMateAgent/1.0 (student project)"}
    try:
        res = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={"action": "query", "list": "search", "srsearch": topic,
                    "format": "json", "srlimit": 1},
            headers=headers, timeout=10,
        ).json()
        hits = res["query"]["search"]
        if not hits:
            return "No Wikipedia article found for that topic."
        title = hits[0]["title"]
        summary = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title)}",
            headers=headers, timeout=10,
        ).json()
        return f"{summary.get('title')}: {summary.get('extract')}"
    except Exception as e:
        return f"Wikipedia error: {e}"

# ---------- Tool 3: Time ----------
def get_current_time() -> str:
    """Get the current date and time on the server."""
    return datetime.now().strftime("%A, %d %B %Y, %I:%M %p")

# ---------- Tool 4 & 5: Notes (simple file-based memory) ----------
def _load_notes() -> list:
    if NOTES_FILE.exists():
        return json.loads(NOTES_FILE.read_text())
    return []

def save_note(title: str, content: str) -> str:
    """Save a study note with a short title and its content."""
    notes = _load_notes()
    notes.append({"title": title, "content": content,
                  "saved_at": datetime.now().isoformat(timespec="seconds")})
    NOTES_FILE.write_text(json.dumps(notes, indent=2))
    return f"Note '{title}' saved. You now have {len(notes)} notes."

def list_notes() -> str:
    """Return all saved study notes."""
    notes = _load_notes()
    if not notes:
        return "No notes saved yet."
    return "\n".join(f"{i+1}. {n['title']}: {n['content']}" for i, n in enumerate(notes))