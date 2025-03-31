import tkinter as tk
from tkinter import font as tkFont


class ThemeManager:
    """
    Manages themes and applies aesthetic styles to the editor
    """
    def __init__(self, root, text_widget):
        self.root = root
        self.text_widget = text_widget

    def apply_theme(self):
        # Set aesthetics using theming
        self.text_widget.configure(bg='#282C34', fg='#ABB2BF', insertbackground='#ABB2BF')  # Cursor color
        self.text_widget.configure(font=('Consolas', 12))
        # Apply custom tag styling for links
        self.text_widget.tag_configure('hyper', foreground='#E06C75', underline=1)  # Styles for hyperlinks

class RetroThemeManager:
    """
    Manages the application of a retro theme to the editor, including font and color themes
    """
    def __init__(self, ui_instance):
        """
        Initializes the Retro Theme Manager with a reference to the UI instance.
        Parameters:
            ui_instance (EditorUI): The instance of the HEAT UP Editor UI
        """
        self.ui = ui_instance
        self.apply_retro_theme()

    def apply_retro_theme(self):
        """
        Applies a retro theme to the editor UI components
        """
        # Apply retro color themes to the text area
        self.ui.text_area.configure(bg=self.ui.config.palette['secondary'])
        self.ui.text_area.configure(fg=self.ui.config.palette['dark_red'])
        
        # Apply the retro font style
        retro_font = tkFont.Font(family="Courier", size=12)
        self.ui.text_area.configure(font=retro_font)

        # Set text area's cursor color
        self.ui.text_area.configure(insertbackground=self.ui.config.palette['primary'])
        
        # Configure the theme of other UI elements as needed