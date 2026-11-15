
from kivy.app import App
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

class JarvisApp(App):

    def build(self):
        self.title = "JARVIS 3.0"
        self.bg = (0.005, 0.018, 0.045, 1)
        self.blue = (0.0, 0.65, 1, 1)
        self.messages = []

        root = BoxLayout(
            orientation="vertical",
            padding=dp(8),
            spacing=dp(8)
        )

        with root.canvas.before:
            Color(*self.bg)
            self.background = RoundedRectangle(
                pos=root.pos, size=root.size
            )
        root.bind(pos=self.update_bg, size=self.update_bg)

        # HEADER
        header = BoxLayout(size_hint_y=None, height=dp(65))

        menu = Button(
            text="☰", font_size=sp(27),
            background_color=(0,0,0,0),
            size_hint_x=None, width=dp(48)
        )
        menu.bind(on_release=lambda x: self.show_menu())

        logo = Label(
            text="[b][color=00DFFF]◉[/color][/b]",
            markup=True, font_size=sp(38),
            size_hint_x=None, width=dp(55)
        )

        heading = Label(
            text="[b]JARVIS [color=008CFF]3.0[/color][/b]\n"
                 "[color=55BCEB]Your Personal Assistant[/color]",
            markup=True, halign="left",
            font_size=sp(17)
        )

        theme = Button(
            text="◉", font_size=sp(25),
            background_color=(0,0,0,0),
            size_hint_x=None, width=dp(48)
        )
        theme.bind(on_release=lambda x: self.show_themes())

        dots = Button(
            text="⋮", font_size=sp(30),
            background_color=(0,0,0,0),
            size_hint_x=None, width=dp(42)
        )
        dots.bind(on_release=lambda x: self.show_menu())

        for item in [menu, logo, heading, theme, dots]:
            header.add_widget(item)

        root.add_widget(header)

        # CHAT AREA
        self.chat = GridLayout(
            cols=1, spacing=dp(12),
            size_hint_y=None, padding=dp(8)
        )
        self.chat.bind(minimum_height=self.chat.setter("height"))

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
            size_hint_y=None, height=dp(58),
            spacing=dp(5)
        )

        plus = Button(
            text="+", font_size=sp(29),
            size_hint_x=None, width=dp(48),
            background_color=(0.02,0.12,0.28,1)
        )
        plus.bind(on_release=lambda x: self.show_plus())

        self.input = TextInput(
            hint_text="Type your message...",
            multiline=False,
            font_size=sp(16),
            foreground_color=(1,1,1,1),
            background_color=(0.01,0.04,0.10,1),
            cursor_color=self.blue,
            padding=[dp(12), dp(15)]
        )
        self.input.bind(on_text_validate=self.send_message)

        mic = Button(
            text="🎤", font_size=sp(22),
            size_hint_x=None, width=dp(50),
            background_color=(0.01,0.12,0.25,1)
        )
        mic.bind(on_release=lambda x: self.notice(
            "Voice", "Voice recognition will be added in a later step."
        ))

        send = Button(
            text="➤", font_size=sp(25),
            size_hint_x=None, width=dp(48),
            background_color=(0.0,0.35,0.95,1)
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
            cols=2, spacing=dp(7),
            size_hint_y=None
        )
        grid.bind(minimum_height=grid.setter("height"))

        for title, action in features:
            btn = Button(
                text=title,
                font_size=sp(14),
                size_hint_y=None,
                height=dp(48),
                background_color=(0.015,0.07,0.16,1)
            )
            btn.bind(on_release=lambda x, a=action: self.feature(a))
            grid.add_widget(btn)

        root.add_widget(grid)

        return root

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
            padding=(dp(12),dp(10))
        )
        label.bind(
            texture_size=lambda obj, size:
            setattr(obj, "size", (self.chat.width, size[1]+dp(20)))
        )
        label.text_size = (self.chat.width-dp(25), None)
        self.chat.add_widget(label)

    def send_message(self, *args):
        text = self.input.text.strip()
        if not text:
            return

        self.add_message("YOU", text)
        self.input.text = ""

        self.add_message(
            "JARVIS",
            "మీ సందేశం అందింది బాస్! AI connection "
            "తర్వాతి దశలో ఏర్పాటు చేస్తాం."
        )

    def show_popup(self, title, options):
        content = BoxLayout(orientation="vertical", spacing=dp(5), padding=dp(8))

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
                background_color=(0.02,0.10,0.22,1)
            )
            btn.bind(on_release=lambda x, value=option:
                     self.popup_action(value, popup))
            content.add_widget(btn)

        popup.open()

    def show_plus(self):
        self.show_popup("Add Features", [
            "Camera", "Photos / Gallery", "Files",
            "Plugins", "Think harder", "Close"
        ])

    def show_menu(self):
        self.show_popup("More Options", [
            "Share", "Unpin", "Add to project",
            "Uploaded files", "Find in chat",
            "Add to home", "Archive", "Delete", "Close"
        ])

    def show_themes(self):
        self.show_popup("Choose Theme", [
            "Neon Blue", "Purple", "Green",
            "Red", "Gold", "Close"
        ])

    def popup_action(self, value, popup):
        popup.dismiss()

        if value == "Clear Chat":
            self.chat.clear_widgets()
        elif value == "Delete":
            self.notice("Security", "Confirm before deleting chat.")
        elif value in ["Neon Blue", "Purple", "Green", "Red", "Gold"]:
            self.notice("Theme", value + " theme will be configured.")
        elif value != "Close":
            self.feature(value)

    def feature(self, name):
        if name == "Clear Chat":
            self.chat.clear_widgets()
            self.add_message("JARVIS", "కొత్త Chat ప్రారంభమైంది బాస్!")
        else:
            self.notice(name, name + " feature will be connected in a later step.")

    def notice(self, title, message):
        Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.85, 0.35)
        ).open()


if __name__ == "__main__":
    JarvisApp().run()
