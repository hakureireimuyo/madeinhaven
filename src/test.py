from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.slider import MDSlider
from kivymd.uix.toolbar import MDTopAppBar

from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.scrollview import ScrollView
import time
from datetime import datetime

class TestApp(MDApp):
    # App properties
    current_time = StringProperty("00:00:00")
    progress_value = NumericProperty(0)
    is_dark_theme = BooleanProperty(False)
    selected_item = StringProperty("None")
    
    def build(self):
        # Set theme
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # Create main layout
        self.main_layout = MDBoxLayout(orientation="vertical")
        
        # Add top app bar
        self.top_bar = MDTopAppBar(
            title="KivyMD Test Application",
            right_action_items=[
                ["theme-light-dark", lambda x: self.toggle_theme()],
                ["exit-to-app", lambda x: self.exit_app()]
            ]
        )
        self.main_layout.add_widget(self.top_bar)
        
        # Create content area
        self.content_layout = MDBoxLayout(orientation="vertical", padding=10, spacing=10)
        
        # Add welcome card
        welcome_card = MDCard(
            orientation="vertical",
            padding=20,
            size_hint_y=None,
            height=150,
            elevation=3,
            radius=[15]
        )
        
        welcome_label = MDLabel(
            text="Welcome to KivyMD Test App",
            halign="center",
            font_style="H5"
        )
        welcome_card.add_widget(welcome_label)
        
        subtitle_label = MDLabel(
            text="A test application built with pure KivyMD components",
            halign="center",
            font_style="Subtitle1"
        )
        welcome_card.add_widget(subtitle_label)
        
        self.content_layout.add_widget(welcome_card)
        
        # Add clock display
        clock_card = MDCard(
            orientation="vertical",
            padding=20,
            size_hint_y=None,
            height=120,
            elevation=3,
            radius=[15]
        )
        
        self.clock_label = MDLabel(
            text=self.current_time,
            halign="center",
            font_style="H2",
            theme_text_color="Primary"
        )
        clock_card.add_widget(self.clock_label)
        
        date_label = MDLabel(
            text=datetime.now().strftime("%Y-%m-%d %A"),
            halign="center",
            font_style="H6"
        )
        clock_card.add_widget(date_label)
        
        self.content_layout.add_widget(clock_card)
        
        # Add control buttons
        button_layout = MDBoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=60)
        
        buttons = [
            ("Toggle Theme", self.toggle_theme),
            ("Show Dialog", self.show_demo_dialog),
            ("Progress Demo", self.start_progress_demo)
        ]
        
        for text, callback in buttons:
            btn = MDRaisedButton(
                text=text,
                on_release=callback
            )
            button_layout.add_widget(btn)
        
        self.content_layout.add_widget(button_layout)
        
        # Add theme toggle switch
        theme_layout = MDBoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=50)
        theme_label = MDLabel(text="Dark Theme:", font_style="H6")
        theme_layout.add_widget(theme_label)
        
        self.theme_switch = MDSwitch(
            active=self.is_dark_theme,
            on_active=self.toggle_theme
        )
        theme_layout.add_widget(self.theme_switch)
        
        self.content_layout.add_widget(theme_layout)
        
        # Add slider control
        slider_layout = MDBoxLayout(orientation="vertical", spacing=10)
        slider_label = MDLabel(text="Volume Control:", font_style="H6")
        slider_layout.add_widget(slider_label)
        
        self.volume_slider = MDSlider(
            min=0,
            max=100,
            value=50,
            hint=True
        )
        slider_layout.add_widget(self.volume_slider)
        
        self.content_layout.add_widget(slider_layout)
        
        # Add list demo
        list_layout = MDBoxLayout(orientation="vertical", spacing=10)
        list_label = MDLabel(text="Select an item:", font_style="H6")
        list_layout.add_widget(list_label)
        
        # Create scrollable list
        scroll = ScrollView(size_hint_y=None, height=200)
        self.demo_list = MDList()
        
        for i in range(1, 11):
            item = OneLineListItem(
                text=f"Item {i}",
                on_release=lambda x, idx=i: self.select_item(f"Item {idx}")
            )
            self.demo_list.add_widget(item)
        
        scroll.add_widget(self.demo_list)
        list_layout.add_widget(scroll)
        
        # Display selected item
        self.selected_label = MDLabel(
            text=f"Selected: {self.selected_item}",
            halign="center"
        )
        list_layout.add_widget(self.selected_label)
        
        self.content_layout.add_widget(list_layout)
        
        self.main_layout.add_widget(self.content_layout)
        
        # Start clock update
        Clock.schedule_interval(self.update_time, 1)
        
        return self.main_layout
    
    def update_time(self, dt):
        """Update time display"""
        self.current_time = datetime.now().strftime("%H:%M:%S")
        self.clock_label.text = self.current_time
    
    def toggle_theme(self, *args):
        """Toggle dark/light theme"""
        self.is_dark_theme = not self.is_dark_theme
        self.theme_cls.theme_style = "Dark" if self.is_dark_theme else "Light"
        
        # Update switch state
        self.theme_switch.active = self.is_dark_theme
    
    def start_progress_demo(self, *args):
        """Start progress bar demo"""
        # Create a progress dialog
        progress_dialog = MDDialog(
            title="Progress Demo",
            text="Progress bar is running...",
            type="progress",
            auto_dismiss=False
        )
        
        # Create a progress bar
        progress_bar = MDSlider(
            min=0,
            max=100,
            value=0,
            hint=True
        )
        progress_dialog.add_widget(progress_bar)
        
        progress_dialog.open()
        
        # Simulate progress update
        def update_progress(dt):
            if progress_bar.value < 100:
                progress_bar.value += 5
                return True
            else:
                progress_dialog.dismiss()
                self.show_dialog("Complete", "Progress demo completed!")
                return False
        
        Clock.schedule_interval(update_progress, 0.2)
    
    def select_item(self, item_text):
        """Select list item"""
        self.selected_item = item_text
        self.selected_label.text = f"Selected: {self.selected_item}"
    
    def show_demo_dialog(self, *args):
        """Show demo dialog"""
        dialog = MDDialog(
            title="Demo Dialog",
            text="This is a dialog example created with KivyMD.",
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(text="OK", on_release=lambda x: self.dialog_confirm(dialog))
            ]
        )
        dialog.open()
    
    def dialog_confirm(self, dialog):
        """Dialog confirm button callback"""
        dialog.dismiss()
        self.show_dialog("Confirmed", "You clicked the OK button!")
    
    def show_dialog(self, title, text):
        """Show simple dialog"""
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()
    
    def exit_app(self, *args):
        """Exit application"""
        self.stop()

if __name__ == "__main__":
    TestApp().run()