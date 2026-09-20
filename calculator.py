import ast
import math
import operator
from pathlib import Path
import tkinter as tk
from tkinter import ttk


APP_NAME = "Better Calculator"
ICON_PATH = Path(__file__).with_name("better_calculator.ico")
THEMES = {
    "light": {
        "bg": "#f5f7fb", "panel": "#ffffff", "key": "#eef1f6", "key_hover": "#e1e6ef",
        "text": "#182230", "muted": "#637083", "accent": "#1769e0", "accent_hover": "#1257bd", "operator_text": "#174f9e",
        "operator": "#e3efff", "clear": "#fde8e7", "clear_text": "#bb2d28",
    },
    "dark": {
        "bg": "#151a23", "panel": "#202735", "key": "#2b3545", "key_hover": "#39465a",
        "text": "#f3f6fb", "muted": "#aab6c7", "accent": "#66a3ff", "accent_hover": "#4b8ce8", "operator_text": "#b9d5ff",
        "operator": "#263f63", "clear": "#542c35", "clear_text": "#ffaaa8",
    },
}


class SafeEvaluator(ast.NodeVisitor):
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise ValueError("Niedozwolona wartość")

    def visit_BinOp(self, node):
        operation = self.OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Niedozwolona operacja")
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("Za duża potęga")
        return operation(left, right)

    def visit_UnaryOp(self, node):
        operation = self.OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Niedozwolona operacja")
        return operation(self.visit(node.operand))

    def generic_visit(self, node):
        raise ValueError("Nieprawidłowe wyrażenie")


def evaluate(expression):
    expression = expression.replace("×", "*").replace("÷", "/").replace(",", ".")
    tree = ast.parse(expression, mode="eval")
    result = SafeEvaluator().visit(tree)
    if not math.isfinite(result):
        raise ValueError("Wynik poza zakresem")
    return result


class PremiumCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("960x640")
        self.minsize(760, 540)
        self.theme_name = "light"
        self.theme = THEMES[self.theme_name]
        self._button_widgets = []
        if ICON_PATH.exists():
            self.iconbitmap(str(ICON_PATH))
        self.configure(bg=self.theme["bg"])
        self.expression = tk.StringVar()
        self.result = tk.StringVar(value="0")
        self.status = tk.StringVar(value="Gotowy")
        self.history = []
        self.memory = 0
        self._build_style()
        self._build_ui()
        self.bind("<Key>", self._on_key)
        self.bind("<Return>", lambda _event: self.calculate())
        self.bind("<Escape>", lambda _event: self.clear())

    def _build_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("App.TFrame", background=self.theme["bg"])
        style.configure("Panel.TFrame", background=self.theme["panel"])
        style.configure("Title.TLabel", background=self.theme["bg"], foreground=self.theme["text"], font=("Segoe UI", 20))
        style.configure("Subtitle.TLabel", background=self.theme["bg"], foreground=self.theme["muted"], font=("Segoe UI", 10))
        style.configure("Display.TLabel", background=self.theme["panel"], foreground=self.theme["text"], font=("Segoe UI", 32), anchor="e")
        style.configure("Expression.TLabel", background=self.theme["panel"], foreground=self.theme["muted"], font=("Segoe UI", 13), anchor="e")
        style.configure("Status.TLabel", background=self.theme["bg"], foreground=self.theme["muted"], font=("Segoe UI", 9))
        style.configure("History.TLabel", background=self.theme["panel"], foreground=self.theme["text"], font=("Segoe UI", 11), anchor="w")
        style.configure("TButton", background=self.theme["key"], foreground=self.theme["text"], padding=(10, 6))
        style.map("TButton", background=[("active", self.theme["key_hover"])], foreground=[("active", self.theme["text"])])
        style.configure("Theme.TButton", background=self.theme["key"], foreground=self.theme["text"], padding=(12, 7))

    def _build_ui(self):
        root = ttk.Frame(self, style="App.TFrame", padding=24)
        root.pack(fill="both", expand=True)
        header = ttk.Frame(root, style="App.TFrame")
        header.pack(fill="x", pady=(0, 18))
        ttk.Label(header, text=APP_NAME, style="Title.TLabel").pack(side="left")
        ttk.Label(header, text="Prosty i szybki", style="Subtitle.TLabel").pack(side="left", padx=(14, 0), pady=(8, 0))
        self.theme_button = ttk.Button(header, text="🌙  Tryb ciemny", style="Theme.TButton", command=self.toggle_theme)
        self.theme_button.pack(side="right")

        workspace = ttk.Frame(root, style="App.TFrame")
        workspace.pack(fill="both", expand=True)
        workspace.columnconfigure(0, weight=1, minsize=250)
        workspace.columnconfigure(1, weight=2, minsize=440)
        workspace.rowconfigure(0, weight=1)

        history = ttk.Frame(workspace, style="Panel.TFrame", padding=20)
        history.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        history_header = ttk.Frame(history, style="Panel.TFrame")
        history_header.pack(fill="x")
        ttk.Label(history_header, text="Historia", style="History.TLabel").pack(side="left")
        ttk.Button(history_header, text="Wyczyść", command=self.clear_history).pack(side="right")
        self.history_label = ttk.Label(history, text="Brak ostatnich działań", style="History.TLabel", wraplength=230, justify="left")
        self.history_label.pack(fill="x", pady=(20, 0))
        ttk.Label(history, text="Enter oblicza  •  Esc czyści", style="Status.TLabel").pack(side="bottom", anchor="w")

        calculator = ttk.Frame(workspace, style="Panel.TFrame", padding=20)
        calculator.grid(row=0, column=1, sticky="nsew")
        calculator.rowconfigure(1, weight=1)
        calculator.columnconfigure(0, weight=1)
        display = ttk.Frame(calculator, style="Panel.TFrame")
        display.grid(row=0, column=0, sticky="ew", pady=(4, 20))
        ttk.Label(display, textvariable=self.expression, style="Expression.TLabel").pack(fill="x", pady=(0, 8))
        ttk.Label(display, textvariable=self.result, style="Display.TLabel").pack(fill="x")

        keypad = tk.Frame(calculator, bg=self.theme["panel"])
        self.keypad = keypad
        keypad.grid(row=1, column=0, sticky="nsew")
        for row in range(6):
            keypad.rowconfigure(row, weight=1, minsize=55)
        for column in range(4):
            keypad.columnconfigure(column, weight=1, minsize=80)

        buttons = [
            ("AC", 0, 0, "clear", self.clear), ("⌫", 0, 1, "normal", self.backspace), ("%", 0, 2, "operator", lambda: self.add("%")), ("÷", 0, 3, "operator", lambda: self.add("÷")),
            ("7", 1, 0, "normal", lambda: self.add("7")), ("8", 1, 1, "normal", lambda: self.add("8")), ("9", 1, 2, "normal", lambda: self.add("9")), ("×", 1, 3, "operator", lambda: self.add("×")),
            ("4", 2, 0, "normal", lambda: self.add("4")), ("5", 2, 1, "normal", lambda: self.add("5")), ("6", 2, 2, "normal", lambda: self.add("6")), ("−", 2, 3, "operator", lambda: self.add("-")),
            ("1", 3, 0, "normal", lambda: self.add("1")), ("2", 3, 1, "normal", lambda: self.add("2")), ("3", 3, 2, "normal", lambda: self.add("3")), ("+", 3, 3, "operator", lambda: self.add("+")),
            ("M", 4, 0, "normal", self.memory_recall), ("0", 4, 1, "normal", lambda: self.add("0")), (".", 4, 2, "normal", lambda: self.add(".")), ("=", 4, 3, "equals", self.calculate),
            ("M−", 5, 0, "normal", self.memory_subtract), ("M+", 5, 1, "normal", self.memory_add), ("±", 5, 2, "normal", self.toggle_sign), ("Kopiuj", 5, 3, "normal", self.copy_result),
        ]
        colors = self._button_colors()
        for label, row, column, kind, command in buttons:
            background, foreground = colors[kind]
            font_size = 10 if label == "Kopiuj" else 12
            button = tk.Button(
                keypad,
                text=label,
                command=command,
                bg=background,
                fg=foreground,
                activebackground=self._button_hover_color(kind),
                activeforeground=foreground,
                relief="flat",
                overrelief="flat",
                bd=0,
                highlightthickness=1,
                highlightbackground=self.theme["panel"],
                highlightcolor=self.theme["panel"],
                padx=4,
                pady=4,
                font=("Segoe UI", font_size, "bold"),
                cursor="hand2",
            )
            button.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)
            button.bind("<Enter>", lambda _event, item=button, item_kind=kind: self._set_button_hover(item, item_kind, True))
            button.bind("<Leave>", lambda _event, item=button, item_kind=kind: self._set_button_hover(item, item_kind, False))
            self._button_widgets.append((button, kind))

    def _button_colors(self):
        return {
            "normal": (self.theme["key"], self.theme["text"]),
            "operator": (self.theme["operator"], self.theme["operator_text"]),
            "equals": (self.theme["accent"], "#ffffff"),
            "clear": (self.theme["clear"], self.theme["clear_text"]),
        }

    def _button_hover_color(self, kind):
        if kind == "equals":
            return self.theme["accent_hover"]
        if kind == "operator":
            return self.theme["key_hover"]
        return self.theme["key_hover"]

    def _set_button_hover(self, button, kind, hovered):
        if hovered:
            button.configure(bg=self._button_hover_color(kind))
            return
        button.configure(bg=self._button_colors()[kind][0])

    def toggle_theme(self):
        self.theme_name = "dark" if self.theme_name == "light" else "light"
        self.theme = THEMES[self.theme_name]
        self.configure(bg=self.theme["bg"])
        self._build_style()
        self.keypad.configure(bg=self.theme["panel"])
        for button, kind in self._button_widgets:
            background, foreground = self._button_colors()[kind]
            button.configure(
                bg=background,
                fg=foreground,
                activebackground=self._button_hover_color(kind),
                activeforeground=foreground,
                highlightbackground=self.theme["panel"],
                highlightcolor=self.theme["panel"],
            )
        self.theme_button.configure(text="☀️  Tryb jasny" if self.theme_name == "dark" else "🌙  Tryb ciemny")

    def add(self, value):
        self.expression.set(self.expression.get() + value)
        self.status.set("Wprowadzanie")

    def clear(self):
        self.expression.set("")
        self.result.set("0")
        self.status.set("Gotowy")

    def clear_history(self):
        self.history.clear()
        self.history_label.config(text="Brak działań")
        self.status.set("Historia wyczyszczona")

    def backspace(self):
        self.expression.set(self.expression.get()[:-1])

    def _numeric_result(self):
        try:
            return float(self.result.get())
        except ValueError:
            return None

    def memory_add(self):
        value = self._numeric_result()
        if value is not None:
            self.memory += value
            self.status.set("Dodano do pamięci")

    def memory_subtract(self):
        value = self._numeric_result()
        if value is not None:
            self.memory -= value
            self.status.set("Odjęto od pamięci")

    def memory_recall(self):
        self.expression.set(f"{self.memory:.12g}")
        self.status.set("Wczytano pamięć")

    def toggle_sign(self):
        expression = self.expression.get().strip()
        if expression.startswith("-"):
            self.expression.set(expression[1:])
        elif expression:
            self.expression.set(f"-({expression})")

    def insert_result(self):
        value = self._numeric_result()
        if value is not None:
            self.expression.set(f"{value:.12g}")
            self.status.set("Wstawiono wynik")

    def copy_result(self):
        value = self.result.get()
        self.clipboard_clear()
        self.clipboard_append(value)
        self.update()
        self.status.set("Wynik skopiowany")

    def calculate(self):
        expression = self.expression.get().strip()
        if not expression:
            return
        try:
            value = evaluate(expression)
            formatted = f"{value:.12g}"
            self.result.set(formatted)
            self.history.insert(0, f"{expression} = {formatted}")
            self.history = self.history[:3]
            self.history_label.config(text="\n".join(self.history))
            self.status.set("Obliczono pomyślnie")
        except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
            self.result.set("BŁĄD")
            self.status.set("Sprawdź wyrażenie")

    def _on_key(self, event):
        if event.char in "0123456789.+-*/()%":
            self.add("×" if event.char == "*" else "÷" if event.char == "/" else event.char)
        elif event.keysym == "BackSpace":
            self.backspace()


if __name__ == "__main__":
    PremiumCalculator().mainloop()
