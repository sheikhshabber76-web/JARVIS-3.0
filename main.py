
import os

from kivy.app import App
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle


class JarvisApp(App):

    def build(self):
        self.title = "JARVIS 3.0"

        self.themes = {
            "Neon Blue": (0.0, 0.65, 1, 1),
            "Purple": (0.65, 0.25, 1, 1),
            "Green": (0.0, 0.75, 0.4, 1),
            "Red": (1, 0.2, 0.2, 1),
            "Gold": (1, 0.65, 0.0, 1)
        }

        self.theme_name = "Neon Blue"
        self.blue = self.themes[self.theme_name]
        self.bg = (0.005, 0.018, 0.045, 1)

        self.messages = []

        # Telugu font
        self.font_path = os.path.join(
            os.path.dirname(__file__),
            "fonts",
            "NotoSansTelugu-Regular.ttf"
        )

        if not os.path.exists(self.font_path):
            self.font_path = None

        root = BoxLayout(
            orientation="vertical",
            padding=dp(8),
            spacing=dp(8)
        )

        with root.canvas.before:
            Color(*self.bg)
            self.background = RoundedRectangle(
                pos=root.pos,
                size=root.size
            )

        root.bind(pos=self.update_bg, size=self.update_bg)
        self.root_layout = root

        # HEADER
        header = BoxLayout(
            size_hint_y=None,
            height=dp(65)
        )

        menu = self.make_button("☰", 27, 48)
        menu.bind(on_release=lambda x: self.show_menu())

        logo = Label(
            text="[b][color=00DFFF]◉[/color][/b]",
            markup=True,
            font_size=sp(38),
            size_hint_x=None,
            width=dp(55)
        )

        heading = Label(
            text="[b]JARVIS [color=008CFF]3.0[/color][/b]\n"
                 "[color=55BCEB]Your Personal Assistant[/color]",
            markup=True,
            halign="left",
            font_size=sp(17)
        )

        theme = self.make_button("◉", 25, 48)
        theme.bind(on_release=lambda x: self.show_themes())

        dots = self.make_button("⋮", 30, 42)
        dots.bind(on_release=lambda x: self.show_menu())

        for item in [menu, logo, heading, theme, dots]:
            header.add_widget(item)

        root.add_widget(header)

        # CHAT AREA
        self.chat = GridLayout(
            cols=1,
            spacing=dp(12),
            size_hint_y=None,
            padding=dp(8)
        )

        self.chat.bind(
            minimum_height=self.chat.setter("height")
        )

        scroll = ScrollView()
        scroll.add_widget(self.chat)
        root.add_widget(scroll)

        self.add_message(
            "JARVIS",
            "నమస్కారం బాస్! నేను JARVIS 3.0.\n"
            "మీకు ఏ విధంగా సహాయం చేయగలను?"
        )

        # MESSAGE BAR
        message_bar = BoxLayout(
            size_hint_y=None,
            height=dp(58),
            spacing=dp(5)
        )

        plus = Button(
            text="+",
            font_size=sp(29),
            size_hint_x=None,
            width=dp(48),
            background_color=(0.02, 0.12, 0.28, 1)
        )
        plus.bind(on_release=lambda x: self.show_plus())

        self.input = TextInput(
            hint_text="Type your message...",
            multiline=False,
            font_size=sp(16),
            foreground_color=(1, 1, 1, 1),
            background_color=(0.01, 0.04, 0.10, 1),
            cursor_color=self.blue,
            padding=[dp(12), dp(15)]
        )

        if self.font_path:
            self.input.font_name = self.font_path

        self.input.bind(
            on_text_validate=self.send_message
        )

        mic = Button(
            text="🎤",
            font_size=sp(22),
            size_hint_x=None,
            width=dp(50),
            background_color=(0.01, 0.12, 0.25, 1)
        )
        mic.bind(
            on_release=lambda x: self.notice(
                "Voice",
                "Telugu voice recognition will be connected later."
            )
        )

        send = Button(
            text="➤",
            font_size=sp(25),
            size_hint_x=None,
            width=dp(48),
            background_color=(0.0, 0.35, 0.95, 1)
        )
        send.bind(on_release=self.send_message)

        for item in [plus, self.input, mic, send]:
            message_bar.add_widget(item)

        root.add_widget(message_bar)

        # FEATURE BUTTONS
        features = [
            ("▦  Calculator", "Calculator"),
            ("◎  Web", "Web"),
            ("📷  Camera", "Camera"),
            ("▧  Gallery", "Gallery"),
            ("🎤  Voice (తెలుగు)", "Voice"),
            ("🎨  Themes", "Themes"),
            ("⚙  Settings", "Settings"),
            ("▤  Clear Chat", "Clear Chat")
        ]

        grid = GridLayout(
            cols=2,
            spacing=dp(7),
            size_hint_y=None
        )

        grid.bind(
            minimum_height=grid.setter("height")
        )

        for title, action in features:
            btn = Button(
                text=title,
                font_size=sp(14),
                size_hint_y=None,
                height=dp(48),
                background_color=(0.015, 0.07, 0.16, 1)
            )

            btn.bind(
                on_release=lambda x, a=action: self.feature(a)
            )

            grid.add_widget(btn)

        root.add_widget(grid)

        return root

    def make_button(self, text, size, width):
        return Button(
            text=text,
            font_size=sp(size),
            background_color=(0, 0, 0, 0),
            size_hint_x=None,
            width=dp(width)
        )

    def update_bg(self, widget, value):
        self.background.pos = widget.pos
        self.background.size = widget.size

    def add_message(self, sender, message):
        label = Label(
            text=f"[b][color=00BFFF]{sender}[/color][/b]\n{message}",
            markup=True,
            size_hint_y=None,
            halign="left",
            valign="middle",
            font_size=sp(16),
            padding=(dp(12), dp(10))
        )

        if self.font_path:
            label.font_name = self.font_path

        label.bind(
            texture_size=lambda obj, size:
            setattr(
                obj,
                "size",
                (self.chat.width, size[1] + dp(20))
            )
        )

        label.text_size = (
            self.chat.width - dp(25),
            None
        )

        self.chat.add_widget(label)

    def send_message(self, *args):
        message = self.input.text.strip()

        if not message:
            return

        self.add_message("YOU", message)
        self.input.text = ""

        self.add_message(
            "JARVIS",
            "మీ సందేశం అందింది బాస్! AI connection "
            "తర్వాతి దశలో ఏర్పాటు చేస్తాం."
        )

    def show_popup(self, title, options):
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(5),
            padding=dp(8)
        )

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.85, 0.65)
        )

        for option in options:
            btn = Button(
                text=option,
                size_hint_y=None,
                height=dp(43),
                background_color=(0.02, 0.10, 0.22, 1)
            )

            btn.bind(
                on_release=lambda x, value=option:
                self.popup_action(value, popup)
            )

            content.add_widget(btn)

        popup.open()

    def show_plus(self):
        self.show_popup("Add Features", [
            "Camera",
            "Photos / Gallery",
            "Files",
            "Plugins",
            "Think harder",
            "Close"
        ])

    def show_menu(self):
        self.show_popup("More Options", [
            "Share",
            "Unpin",
            "Add to project",
            "Uploaded files",
            "Find in chat",
            "Add to home",
            "Archive",
            "Delete",
            "Close"
        ])

    def show_themes(self):
        self.show_popup("Choose Theme", [
            "Neon Blue",
            "Purple",
            "Green",
            "Red",
            "Gold",
            "Close"
        ])

    def popup_action(self, value, popup):
        popup.dismiss()

        if value == "Clear Chat":
            self.clear_chat()

        elif value == "Delete":
            self.notice(
                "Security",
                "Confirm before deleting chat."
            )

        elif value in self.themes:
            self.change_theme(value)

        elif value != "Close":
            self.feature(value)

    def change_theme(self, name):
        self.theme_name = name
        self.blue = self.themes[name]

        self.notice(
            "Theme",
            name + " theme selected."
        )

    def clear_chat(self):
        self.chat.clear_widgets()
        self.add_message(
            "JARVIS",
            "కొత్త Chat ప్రారంభమైంది బాస్!"
        )

    def feature(self, name):
        if name == "Clear Chat":
            self.clear_chat()

        else:
            self.notice(
                name,
                name + " feature will be connected in a later step."
            )

    def notice(self, title, message):
        content = Label(
            text=message,
            halign="center",
            valign="middle"
        )

        if self.font_path:
            content.font_name = self.font_path

        Popup(
            title=title,
            content=content,
            size_hint=(0.85, 0.35)
        ).open()


if __name__ == "__main__":
    JarvisApp().run()

