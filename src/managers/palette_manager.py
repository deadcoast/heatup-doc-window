# Advanced Palette Manager for HEAT UP Editor
# Finishing and implementing remaining functions for the HEAT UP text editor

import tkinter as tk
from tkinter import Toplevel, Text, simpledialog, Menu, messagebox
from tkinter.font import Font


# Enhanced Palette Manager with completed functionality
class PaletteManager:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.base_colors = {
            'primary': '#FFFAFA',    # Main font color, off-white for improved legibility
            'secondary': '#282C34',  # Background color, dark for contrast
            'tertiary': '#ABB2BF',   # Color for comments and secondary elements
            'dark_red': '#E06C75',   # Highlight color for hyperlinks
            'custom_colors': ['#56B6C2', '#C678DD', '#98C379', '#E5C07B', '#61AFEF', '#BE5046']  # Customizable by user
        }
    
    def apply_palette_to_widget(self):
        # Applies the color palette to the text widget
        self.text_widget.configure(bg=self.base_colors['secondary'])
        self.text_widget.configure(fg=self.base_colors['primary'])
        self.text_widget.configure(insertbackground=self.base_colors['dark_red'])  # Cursor color
    
    def update_custom_color(self, index, hex_color):
        # Updates a custom color at a specified index
        if 0 <= index < len(self.base_colors['custom_colors']):
            self.base_colors['custom_colors'][index] = hex_color
        else:
            messagebox.showerror("Error", "Invalid custom color index")

    def add_custom_color(self, color_key, hex_color):
        if color_key in self.base_colors:
            self.base_colors[color_key] = hex_color
        else:
            print(f"Color key {color_key} does not exist. Please add it to the base colors first.")

    def apply_palette_to_widget(self):
        # Applies the color palette to the text widget
        self.text_widget.configure(bg=self.base_colors['secondary'])
        self.text_widget.configure(fg=self.base_colors['primary'])
        self.text_widget.configure(insertbackground=self.base_colors['dark_red'])  # Cursor color

    def update_custom_color(self, index, hex_color):
        # Updates a custom color at a specified index
        if 0 <= index < len(self.base_colors['custom_colors']):
            self.base_colors['custom_colors'][index] = hex_color
        else:
            messagebox.showerror("Error", "Invalid custom color index")

