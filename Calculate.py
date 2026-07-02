import ast
import operator
import tkinter as tk
from tkinter import font


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("간단한 계산기")
        self.root.resizable(False, False)

        self.expression = ""
        self.display_var = tk.StringVar(value="0")

        self._build_ui()
        self.root.bind("<Escape>", self.on_escape)

    def _build_ui(self):
        self.root.configure(bg="#f2f2f2")
        self.display = tk.Entry(
            self.root,
            textvariable=self.display_var,
            justify="right",
            font=("Arial", 24),
            bd=10,
            relief="flat",
            state="readonly",
            readonlybackground="#ffffff",
        )
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        button_font = font.Font(family="Arial", size=16, weight="bold")
        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("C", 4, 2), ("+", 4, 3),
        ]

        for text, row, col in buttons:
            btn = tk.Button(
                self.root,
                text=text,
                width=8,
                height=2,
                font=button_font,
                command=lambda t=text: self.on_button_click(t),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)

        equal_btn = tk.Button(
            self.root,
            text="=",
            width=8,
            height=2,
            font=button_font,
            bg="#4f81bd",
            fg="white",
            command=self.on_equal,
        )
        equal_btn.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=4, pady=4)

        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)

    def clear_input(self):
        self.expression = ""
        self.display_var.set("0")

    def on_escape(self, event=None):
        self.clear_input()
        return "break"

    def on_button_click(self, value):
        if value == "C":
            self.clear_input()
            return

        if value in {"+", "-", "*", "/"}:
            if self.expression and self.expression[-1] not in {"+", "-", "*", "/"}:
                self.expression += value
            elif not self.expression:
                self.expression = "0" + value
            else:
                self.expression = self.expression[:-1] + value
        else:
            self.expression += value

        self.display_var.set(self.expression if self.expression else "0")

    def on_equal(self):
        try:
            safe_expr = self._sanitize_expression(self.expression)
            result = self._evaluate(safe_expr)
            self.display_var.set(str(result))
            self.expression = str(result)
        except Exception:
            self.display_var.set("오류")
            self.expression = ""

    def _sanitize_expression(self, expression):
        if not expression:
            return "0"

        try:
            parsed = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise ValueError("잘못된 수식입니다") from exc

        def _validate(node):
            if isinstance(node, ast.Expression):
                _validate(node.body)
                return
            if isinstance(node, ast.Constant):
                if not isinstance(node.value, (int, float)):
                    raise ValueError("숫자만 입력할 수 있습니다")
                return
            if isinstance(node, ast.BinOp):
                if not isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
                    raise ValueError("허용되지 않은 연산입니다")
                _validate(node.left)
                _validate(node.right)
                return
            if isinstance(node, ast.UnaryOp):
                if not isinstance(node.op, (ast.UAdd, ast.USub)):
                    raise ValueError("허용되지 않은 연산입니다")
                _validate(node.operand)
                return
            if isinstance(node, ast.Load):
                return
            raise ValueError("허용되지 않은 식입니다")

        _validate(parsed)
        return expression

    def _evaluate(self, expression):
        try:
            parsed = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise ValueError("잘못된 수식입니다") from exc

        def _eval_node(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            if isinstance(node, ast.UnaryOp):
                operand = _eval_node(node.operand)
                if isinstance(node.op, ast.UAdd):
                    return +operand
                if isinstance(node.op, ast.USub):
                    return -operand
                raise ValueError("허용되지 않은 연산입니다")
            if isinstance(node, ast.BinOp):
                left = _eval_node(node.left)
                right = _eval_node(node.right)
                if isinstance(node.op, ast.Add):
                    return operator.add(left, right)
                if isinstance(node.op, ast.Sub):
                    return operator.sub(left, right)
                if isinstance(node.op, ast.Mult):
                    return operator.mul(left, right)
                if isinstance(node.op, ast.Div):
                    if right == 0:
                        raise ZeroDivisionError("0으로 나눌 수 없습니다")
                    return operator.truediv(left, right)
                raise ValueError("허용되지 않은 연산입니다")
            raise ValueError("허용되지 않은 식입니다")

        return _eval_node(parsed.body)


def main():
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
