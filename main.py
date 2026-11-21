
import ast
import operator

from kivy.app import App
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

Window.clearcolor = (0.015, 0.025, 0.05, 1)


class JARVISApp(App):

    def build(self):
        self.title = "JARVIS 3.0"
        self.accent = (0.0, 0.65, 1.0, 1)
        self.bg = (0.015, 0.025, 0.05, 1)
        self.history = []

        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        with root.canvas.before:
            self.bg_color = Color(*self.bg)
            self.bg_rect = RoundedRectangle(
                pos=root.pos,
                size=root.size
            )

        root.bind(pos=self.update_bg, size=self.update_bg)
        self.root = root

        # HEADER
        header = BoxLayout(
            size_hint_y=None,
            height=dp(62),
            spacing=dp(6)
        )

        header.add_widget(self.make_button("☰", self.menu, 45))
        header.add_widget(Label(
            text="◉",
            font_size=sp(32),
            color=self.accent,
            size_hint_x=None,
            width=dp(48)
        ))

        title_box = BoxLayout(orientation="vertical")

        self.heading = Label(
            text="[b]JARVIS 3.0[/b]",
            markup=True,
            font_size=sp(22),
            color=self.accent,
            halign="left"
        )

        title_box.add_widget(self.heading)
        title_box.add_widget(Label(
            text="Your Personal Assistant",
            font_size=sp(12),
            halign="left",
            color=(0.5, 0.7, 0.85, 1)
        ))

        header.add_widget(title_box)
        header.add_widget(self.make_button("🎨", self.themes, 45))
        root.add_widget(header)

        # CHAT
        self.scroll = ScrollView(
            do_scroll_x=False,
            bar_width=dp(3)
        )

        self.chat = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(5),
            size_hint_y=None
        )

        self.chat.bind(minimum_height=self.chat.setter("height"))
        self.scroll.add_widget(self.chat)
        root.add_widget(self.scroll)

        # INPUT
        bar = BoxLayout(
            size_hint_y=None,
            height=dp(55),
            spacing=dp(5)
        )

        bar.add_widget(self.make_button("+", self.plus, 42))

        self.input = TextInput(
            hint_text="Type your message...",
            multiline=False,
            font_size=sp(16),
            background_color=(0.04, 0.08, 0.14, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=self.accent
        )

        self.input.bind(on_text_validate=self.send)
        bar.add_widget(self.input)

        bar.add_widget(self.make_button("🎙", self.voice, 45))

        self.send_btn = self.make_button("➤", self.send, 45)
        bar.add_widget(self.send_btn)

        root.add_widget(bar)

        # FEATURES
        features = [
            ("Calculator", self.calculator),
            ("Web", self.web),
            ("Camera", self.camera),
            ("Gallery", self.gallery),
            ("Telugu Voice", self.voice),
            ("Themes", self.themes),
            ("Settings", self.settings),
            ("Clear Chat", self.clear_chat),
        ]

        grid = GridLayout(
            cols=4,
            spacing=dp(6),
            size_hint_y=None,
            height=dp(120)
        )

        for name, action in features:
            grid.add_widget(self.feature_button(name, action))

        root.add_widget(grid)

        self.add_message(
            "JARVIS",
            "Hello! JARVIS 3.0 is ready."
        )

        return root

    # BACKGROUND
    def update_bg(self, *args):
        self.bg_rect.pos = self.root.pos
        self.bg_rect.size = self.root.size

    # BUTTONS
    def make_button(self, text, action, width):
        button = Button(
            text=text,
            size_hint_x=None,
            width=dp(width),
            background_normal="",
            background_color=self.accent,
            color=(1, 1, 1, 1),
            font_size=sp(17)
        )
        button.bind(on_release=action)
        return button

    def feature_button(self, text, action):
        button = Button(
            text=text,
            background_normal="",
            background_color=(0.035, 0.075, 0.13, 1),
            color=(0.85, 0.92, 1, 1),
            font_size=sp(12)
        )
        button.bind(on_release=action)
        return button

    # CHAT
    def send(self, *args):
        text = self.input.text.strip()
        if not text:
            return

        self.input.text = ""
        self.add_message("You", text, True)
        self.add_message(
            "JARVIS",
            "Message received. AI connection will be added later."
        )

    def add_message(self, sender, message, is_user=False):
        row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(75),
            spacing=dp(6)
        )

        if is_user:
            row.add_widget(Label(text="", size_hint_x=0.12))
            bubble_color = (0.02, 0.12, 0.23, 1)
        else:
            row.add_widget(Label(
                text="◉",
                color=self.accent,
                size_hint_x=0.12,
                font_size=sp(24)
            ))
            bubble_color = (0.03, 0.07, 0.13, 1)

        bubble = BoxLayout(
            orientation="vertical",
            padding=dp(8),
            size_hint_x=0.88
        )

        with bubble.canvas.before:
            Color(*bubble_color)
            rect = RoundedRectangle(
                pos=bubble.pos,
                size=bubble.size,
                radius=[dp(12)]
            )

        bubble.bind(
            pos=lambda obj, val: setattr(rect, "pos", val),
            size=lambda obj, val: setattr(rect, "size", val)
        )

        name = Label(
            text=f"[b]{sender}[/b]",
            markup=True,
            font_size=sp(13),
            color=self.accent,
            halign="left",
            size_hint_y=None,
            height=dp(20)
        )

        msg = Label(
            text=message,
            font_size=sp(14),
            color=(0.92, 0.96, 1, 1),
            halign="left",
            valign="middle",
            size_hint_y=None
        )

        msg.bind(width=lambda obj, val:
                 setattr(obj, "text_size", (val, None)))
        msg.bind(texture_size=lambda obj, val:
                 setattr(obj, "height", val[1] + dp(8)))

        bubble.add_widget(name)
        bubble.add_widget(msg)
        row.add_widget(bubble)

        if not is_user:
            row.add_widget(Label(text="", size_hint_x=0.02))

        self.chat.add_widget(row)
        self.history.append((sender, message))
        self.scroll.scroll_y = 0

    # PLUS MENU
    def plus(self, *args):
        self.show_menu("Add", [
            ("Camera", self.camera),
            ("Photos", self.gallery),
            ("Files", self.files),
            ("Plugins", self.plugins),
            ("Think harder", self.think),
        ])

    # MAIN MENU
    def menu(self, *args):
        self.show_menu("JARVIS Menu", [
            ("Themes", self.themes),
            ("Settings", self.settings),
            ("Clear Chat", self.clear_chat),
        ])

    def show_menu(self, title, options):
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(5),
            padding=dp(8)
        )

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.55)
        )

        for name, action in options:
            button = Button(text=name, size_hint_y=None, height=dp(45))
            button.bind(
                on_release=lambda btn, fn=action:
                (popup.dismiss(), fn())
            )
            content.add_widget(button)

        popup.open()

    # CALCULATOR
    def calculator(self, *args):
        expression = {"value": ""}

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(6),
            padding=dp(8)
        )

        display = TextInput(
            text="0",
            readonly=True,
            multiline=False,
            halign="right",
            font_size=sp(24),
            size_hint_y=None,
            height=dp(55)
        )

        content.add_widget(display)

        grid = GridLayout(cols=4, spacing=dp(5))
        content.add_widget(grid)

        popup = Popup(
            title="Calculator",
            content=content,
            size_hint=(0.9, 0.72)
        )

        keys = [
            ["C", "⌫", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["0", ".", "=", ""]
        ]

        def press(key):
            current = expression["value"]

            if key == "C":
                current = ""

            elif key == "⌫":
                current = current[:-1]

            elif key == "=":
                try:
                    current = str(self.safe_calculate(current))
                except Exception:
                    current = "Error"

            elif key == "%":
                try:
                    current = str(self.safe_calculate(current) / 100)
                except Exception:
                    current = "Error"

            else:
                current += {
                    "÷": "/",
                    "×": "*",
                    "−": "-"
                }.get(key, key)

            expression["value"] = current
            display.text = current or "0"

        for line in keys:
            for key in line:
                if not key:
                    grid.add_widget(Label())
                    continue

                button = Button(text=key, font_size=sp(20))
                button.bind(on_release=lambda btn, k=key: press(k))
                grid.add_widget(button)

        popup.open()

    # SAFE MATH
    def safe_calculate(self, expression):
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv
        }

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                return node.value

            if isinstance(node, ast.BinOp) and type(node.op) in operators:
                left = evaluate(node.left)
                right = evaluate(node.right)
                result = operators[type(node.op)](left, right)
                if abs(result) > 1e100:
                    raise ValueError("Number too large")
                return result

            raise ValueError("Invalid expression")

        return evaluate(ast.parse(expression, mode="eval"))

    # PLACEHOLDER FEATURES
    def web(self, *args):
        self.notice("Web", "Web integration will be added later.")

    def camera(self, *args):
        self.notice("Camera", "Camera integration will be added later.")

    def gallery(self, *args):
        self.notice("Gallery", "Gallery integration will be added later.")

    def files(self, *args):
        self.notice("Files", "File picker will be added later.")

    def voice(self, *args):
        self.notice("Voice", "Telugu voice integration will be added later.")

    def plugins(self, *args):
        self.notice("Plugins", "Plugin support will be added later.")

    def think(self, *args):
        self.notice("Think", "AI connection will be added later.")

    # THEMES
    def themes(self, *args):
        options = [
            ("Blue", (0, 0.65, 1, 1), (0.015, 0.025, 0.05, 1)),
            ("Purple", (0.7, 0.35, 1, 1), (0.04, 0.02, 0.07, 1)),
            ("Green", (0.2, 0.85, 0.55, 1), (0.02, 0.05, 0.04, 1)),
            ("Red", (1, 0.25, 0.35, 1), (0.06, 0.02, 0.03, 1)),
            ("Orange", (1, 0.6, 0.2, 1), (0.06, 0.04, 0.02, 1))
        ]

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(6),
            padding=dp(8)
        )

        popup = Popup(
            title="Themes",
            content=content,
            size_hint=(0.8, 0.6)
        )

        for name, accent, background in options:
            button = Button(text=name, background_normal="",
                           background_color=accent)
            button.bind(
                on_release=lambda btn, a=accent, bg=background:
                self.set_theme(a, bg, popup)
            )
            content.add_widget(button)

        popup.open()

    def set_theme(self, accent, background, popup):
        self.accent = accent
        self.bg = background
        self.bg_color.rgba = background
        Window.clearcolor = background
        self.heading.color = accent
        self.send_btn.background_color = accent
        popup.dismiss()

    # SETTINGS
    def settings(self, *args):
        self.notice("Settings", "Settings will be added later.")

    # CLEAR CHAT
    def clear_chat(self, *args):
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(8)
        )

        popup = Popup(
            title="Clear Chat",
            content=content,
            size_hint=(0.8, 0.35)
        )

        content.add_widget(Label(text="Clear all messages?"))

        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(8)
        )

        cancel = Button(text="Cancel")
        confirm = Button(text="Clear")

        cancel.bind(on_release=popup.dismiss)

        def clear_chat_now(instance):
            self.chat.clear_widgets()
            self.history.clear()
            popup.dismiss()

        confirm.bind(on_release=clear_chat_now)

        buttons.add_widget(cancel)
        buttons.add_widget(confirm)
        content.add_widget(buttons)

        popup.open()

    # NOTICE
    def notice(self, title, message):
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(8)
        )

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.35)
        )

        content.add_widget(Label(text=message))

        close = Button(
            text="OK",
            size_hint_y=None,
            height=dp(45)
        )
        close.bind(on_release=popup.dismiss)
        content.add_widget(close)

        popup.open()


if __name__ == "__main__":
    JARVISApp().run()
