def feature(self, name):

    if name == "Calculator":
        self.open_calculator()

    elif name == "Themes":
        self.show_themes()

    elif name == "Clear Chat":
        self.clear_chat()

    else:
        self.notice(
            name,
            name + " feature is not connected yet."
        )


def open_calculator(self):

    self.calc_expression = ""

    content = BoxLayout(
        orientation="vertical",
        spacing=dp(8),
        padding=dp(10)
    )

    self.calc_display = TextInput(
        text="0",
        multiline=False,
        readonly=True,
        halign="right",
        font_size=sp(28),
        size_hint_y=None,
        height=dp(65)
    )

    content.add_widget(self.calc_display)

    keys = [
        ["C", "⌫", "%", "÷"],
        ["7", "8", "9", "×"],
        ["4", "5", "6", "−"],
        ["1", "2", "3", "+"],
        ["0", ".", "=", ""]
    ]

    grid = GridLayout(
        cols=4,
        spacing=dp(6)
    )

    popup = Popup(
        title="JARVIS Calculator",
        content=content,
        size_hint=(0.92, 0.72)
    )

    for row in keys:
        for key in row:

            if key == "":
                grid.add_widget(Label())
                continue

            btn = Button(
                text=key,
                font_size=sp(23)
            )

            btn.bind(
                on_release=lambda b, k=key:
                self.calc_press(k)
            )

            grid.add_widget(btn)

    content.add_widget(grid)
    popup.open()

    self.calc_popup = popup


def calc_press(self, key):

    if key == "C":
        self.calc_expression = ""

    elif key == "⌫":
        self.calc_expression = self.calc_expression[:-1]

    elif key == "=":
        try:
            result = self.calculate_safe(self.calc_expression)
            self.calc_expression = str(result)
        except Exception:
            self.calc_expression = "Error"

    elif key == "%":
        try:
            value = self.calculate_safe(self.calc_expression)
            self.calc_expression = str(value / 100)
        except Exception:
            self.calc_expression = "Error"

    else:
        symbols = {
            "÷": "/",
            "×": "*",
            "−": "-"
        }

        self.calc_expression += symbols.get(key, key)

    self.calc_display.text = self.calc_expression or "0"


def calculate_safe(self, expression):

    import ast
    import operator

    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def solve(node):

        if isinstance(node, ast.Expression):
            return solve(node.body)

        if isinstance(node.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node.BinOp) and type(node.op) in operations:
            left = solve(node.left)
            right = solve(node.right)

            return operations[type(node.op)](left, right)

        raise ValueError("Invalid calculation")

    result = solve(ast.parse(expression, mode="eval"))

    if abs(result) > 1e100:
        raise ValueError("Number too large")

    return result