
import os
import ast
import operator
import webbrowser

from kivy.app import App
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle

Window.clearcolor = (0.015, 0.025, 0.05, 1)

FONT = "fonts/NotoSansTelugu-Regular.ttf"


class JARVISApp(App):

    def build(self):
        self.accent = (0.0, 0.65, 1.0, 1)
        self.bg = (0.015, 0.025, 0.05, 1)
        self.bubble = (0.03, 0.08, 0.16, 1)
        self.chat_history = []

        root = BoxLayout(
            orientation="vertical",
            padding=dp(8),
            spacing=dp(7)
        )

        with root.canvas.before:
            self.bg_color = Color(*self.bg)
            self.bg_rect = RoundedRectangle(
                pos=root.pos, size=root.size
            )

        root.bind(pos=self._update_bg, size=self._update_bg)
        self.root = root

        # HEADER
        header = BoxLayout(
            size_hint_y=None, height=dp(65), spacing=dp(8)
        )

        menu_btn = self.btn("☰", self.open_menu, 52)
        header.add_widget(menu_btn)

        logo = Label(
            text="◉",
            font_size=sp(38),
            color=self.accent,
            size_hint_x=None,
            width=dp(60)
        )
        header.add_widget(logo)

        titlebox = BoxLayout(orientation="vertical")

        self.title = Label(
            text="[b]JARVIS 3.0[/b]",
            markup=True,
            font_size=sp(23),
            color=self.accent,
            halign="left"
        )

        subtitle = Label(
            text="Your Personal Assistant",
            font_size=sp(14),
            color=(0.35, 0.65, 0.85, 1),
            halign="left"
        )

        titlebox.add_widget(self.title)
        titlebox.add_widget(subtitle)
        header.add_widget(titlebox)

        header.add_widget(self.btn("🎨", self.show_themes, 55))
        header.add_widget(self.btn("⋮", self.open_menu, 48))

        root.add_widget(header)

        # CHAT
        self.scroll = ScrollView(
            do_scroll_x=False, bar_width=dp(3)
        )

        self.chat = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(8),
            size_hint_y=None
        )

        self.chat.bind(
            minimum_height=self.chat.setter("height")
        )

        self.scroll.add_widget(self.chat)
        root.add_widget(self.scroll)

        # MESSAGE BAR
        messagebar = BoxLayout(
            size_hint_y=None, height=dp(60), spacing=dp(6)
        )

        messagebar.add_widget(
            self.btn("+", self.open_plus, 48)
        )

        self.input = TextInput(
            hint_text="Type your message...",
            multiline=False,
            font_size=sp(16),
            font_name=FONT if os.path.exists(FONT) else "Roboto",
            padding=[dp(12), dp(12)],
            background_color=(0.03, 0.07, 0.13, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=self.accent
        )

        self.input.bind(on_text_validate=self.send)
        messagebar.add_widget(self.input)

        messagebar.add_widget(
            self.btn("🎙", self.voice, 52)
        )

        self.send_button = self.btn("➤", self.send, 52)
        messagebar.add_widget(self.send_button)

        root.add_widget(messagebar)

        # FEATURE BUTTONS
        features = [
            ("▦  Calculator", self.calculator),
            ("◎  Web", self.web),
            ("📷  Camera", self.camera),
            ("▧  Gallery", self.gallery),
            ("🎙  Voice (తెలుగు)", self.voice),
            ("🎨  Themes", self.show_themes),
            ("⚙  Settings", self.settings),
            ("♲  Clear Chat", self.clear_chat),
        ]

        grid = GridLayout(
            cols=4,
            spacing=dp(6),
            size_hint_y=None,
            height=dp(116)
        )

        for label, action in features:
            grid.add_widget(
                self.feature_button(label, action)
            )

        root.add_widget(grid)

        return root

    # BACKGROUND
    def _update_bg(self, *args):
        self.bg_rect.pos = self.root.pos
        self.bg_rect.size = self.root.size

    # BUTTON
    def btn(self, text, action, width):
        b = Button(
            text=text,
            size_hint_x=None,
            width=dp(width),
            font_size=sp(18),
            background_normal="",
            background_color=self.accent,
            color=(1, 1, 1, 1)
        )
        b.bind(on_release=action)
        return b

    def feature_button(self, text, action):
        b = Button(
            text=text,
            font_size=sp(12),
            background_normal="",
            background_color=(0.025, 0.055, 0.11, 1),
            color=(0.8, 0.9, 1, 1)
        )
        b.bind(on_release=action)
        return b

    # CHAT
    def send(self, *args):
        text = self.input.text.strip()

        if not text:
            return

        self.input.text = ""
        self.add_message("You", text, True)

        self.add_message(
            "JARVIS",
            "Message received. AI connection is not set up yet.",
            False
        )

    # ADD MESSAGE
    def add_message(self, sender, message, is_user=False):
        row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(85),
            spacing=dp(8)
        )

        if is_user:
            row.add_widget(Label(size_hint_x=0.15, text=""))
            color = (0.025, 0.12, 0.24, 1)
        else:
            row.add_widget(
                Label(
                    text="◉",
                    color=self.accent,
                    font_size=sp(26),
                    size_hint_x=0.15
                )
            )
            color = (0.025, 0.065, 0.13, 1)

        bubble = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            size_hint_x=0.85
        )

        with bubble.canvas.before:
            Color(*color)
            rect = RoundedRectangle(
                pos=bubble.pos,
                size=bubble.size,
                radius=[dp(16)]
            )

        bubble.bind(
            pos=lambda obj, val: setattr(rect, "pos", val),
            size=lambda obj, val: setattr(rect, "size", val)
        )

        name = Label(
            text=f"[b]{sender}[/b]",
            markup=True,
            color=self.accent if not is_user else (0.3, 0.75, 1, 1),
            font_size=sp(14),
            halign="left",
            size_hint_y=None,
            height=dp(22)
        )

        msg = Label(
            text=message,
            font_size=sp(16),
            font_name=FONT if os.path.exists(FONT) else "Roboto",
            color=(0.92, 0.96, 1, 1),
            halign="left",
            valign="middle",
            size_hint_y=None
        )

        msg.bind(
            width=lambda obj, val:
            setattr(obj, "text_size", (val, None))
        )

        msg.bind(
            texture_size=lambda obj, val:
            setattr(obj, "height", val[1] + dp(10))
        )

        bubble.add_widget(name)
        bubble.add_widget(msg)
        row.add_widget(bubble)

        if not is_user:
            row.add_widget(Label(size_hint_x=0.02, text=""))

        self.chat.add_widget(row)
        self.scroll.scroll_y = 0
        self.chat_history.append((sender, message))

    # PLUS MENU
    def open_plus(self, *args):
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(5),
            padding=dp(8)
        )

        popup = Popup(
            title="Add",
            content=content,
            size_hint=(0.65, 0.5)
        )

        options = [
            ("Camera", self.camera),
            ("Photos", self.gallery),
            ("Files", self.files),
            ("Plugins", self.plugins),
            ("Think harder", self.think),
        ]

        for name, action in options:
            b = Button(
                text=name,
                size_hint_y=None,
                height=dp(44)
            )

            b.bind(
                on_release=lambda btn, fn=action:
                (popup.dismiss(), fn())
            )

            content.add_widget(b)

        popup.open()

    # MENU
    def open_menu(self, *args):
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(5),
            padding=dp(8)
        )

        popup = Popup(
            title="JARVIS Menu",
            content=content,
            size_hint=(0.7, 0.4)
        )

        options = [
            ("Themes", self.show_themes),
            ("Settings", self.settings),
            ("Clear Chat", self.clear_chat),
        ]

        for name, action in options:
            b = Button(
                text=name,
                size_hint_y=None,
                height=dp(45)
            )

            b.bind(
                on_release=lambda btn, fn=action:
                (popup.dismiss(), fn())
            )

            content.add_widget(b)

        popup.open()

    # CALCULATOR
    def calculator(self, *args):
        self.expression = ""

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(6),
            padding=dp(8)
        )

        display = TextInput(
            text="0",
            multiline=False,
            readonly=True,
            halign="right",
            font_size=sp(26),
            size_hint_y=None,
            height=dp(60)
        )

        content.add_widget(display)

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

        grid = GridLayout(cols=4, spacing=dp(5))
        content.add_widget(grid)

        def press(key):
            if key == "C":
                self.expression = ""

            elif key == "⌫":
                self.expression = self.expression[:-1]

            elif key == "=":
                try:
                    self.expression = str(
                        self.safe_calculate(self.expression)
                    )
                except Exception:
                    self.expression = "Error"

            elif key == "%":
                try:
                    self.expression = str(
                        self.safe_calculate(self.expression) / 100
                    )
                except Exception:
                    self.expression = "Error"

            else:
                self.expression += {
                    "÷": "/",
                    "×": "*",
                    "−": "-"
                }.get(key, key)

            display.text = self.expression or "0"

        for line in keys:
            for key in line:
                if key == "":
                    grid.add_widget(Label())
                    continue

                b = Button(text=key, font_size=sp(20))
                b.bind(
                    on_release=lambda btn, k=key: press(k)
                )
                grid.add_widget(b)

        popup.open()

    # SAFE CALCULATOR
    def safe_calculate(self, expression):
        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv
        }

        def calc(node):
            if isinstance(node, ast.Expression):
                return calc(node.body)

            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value

            if isinstance(node, ast.BinOp) and type(node.op) in ops:
                return ops[type(node.op)](
                    calc(node.left),
                    calc(node.right)
                )

            raise ValueError("Invalid expression")

        value = calc(ast.parse(expression, mode="eval"))

        if abs(value) > 1e100:
            raise ValueError("Too large")

        return value

    # WEB
    def web(self, *args):
        self.notice(
            "Web",
            "Web search integration is not connected yet."
        )

    # CAMERA
    def camera(self, *args):
        self.notice(
            "Camera",
            "Camera integration needs Android setup."
        )

    # GALLERY
    def gallery(self, *args):
        self.notice(
            "Gallery",
            "Gallery integration needs Android setup."
        )

    # FILES
    def files(self, *args):
        self.notice(
            "Files",
            "File picker integration needs Android setup."
        )

    # VOICE
    def voice(self, *args):
        self.notice(
            "Voice",
            "Telugu speech recognition is not connected yet."
        )

    # PLUGINS
    def plugins(self, *args):
        self.notice(
            "Plugins",
            "Plugins are not connected yet."
        )

    # THINK
    def think(self, *args):
        self.notice(
            "Think harder",
            "AI connection is required for this feature."
        )

    # THEMES
    def show_themes(self, *args):
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

        themes = [
            ("Blue", (0.0, 0.65, 1, 1), (0.015, 0.025, 0.05, 1)),
            ("Purple", (0.7, 0.35, 1, 1), (0.04, 0.02, 0.07, 1)),
            ("Green", (0.2, 0.85, 0.55, 1), (0.02, 0.05, 0.04, 1)),
            ("Red", (1, 0.25, 0.35, 1), (0.06, 0.02, 0.03, 1)),
            ("Orange", (1, 0.6, 0.2, 1), (0.06, 0.04, 0.02, 1)),
        ]

        for name, accent, background in themes:
            b = Button(
                text=name,
                background_normal="",
                background_color=accent
            )

            b.bind(
                on_release=lambda btn, a=accent, bg=background:
                self.set_theme(a, bg, popup)
            )

            content.add_widget(b)

        popup.open()

    # CHANGE THEME
    def set_theme(self, accent, background, popup):
        self.accent = accent
        self.bg = background
        self.bg_color.rgba = background
        Window.clearcolor = background
        self.title.color = accent
        self.send_button.background_color = accent
        popup.dismiss()

    # SETTINGS
    def settings(self, *args):
        self.notice(
            "Settings",
            "Settings options will be added here."
        )

    # CLEAR CHAT
    def clear_chat(self, *args):
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10)
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

        def clear(instance):
            self.chat.clear_widgets()
            self.chat_history = []
            popup.dismiss()

        confirm.bind(on_release=clear)

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
