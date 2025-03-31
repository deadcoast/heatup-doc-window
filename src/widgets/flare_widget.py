# {1AZ_t #step/#total} [COMMENTS ]

# Comprehensive Flare Widget for the HEAT UP editor with pinning and advanced text editing features

import tkinter as tk
from tkinter import Toplevel, Text

class FlareWidget:
    """ 
    A floating widget for in-depth text editing, 'FLARE', which can be pinned on top and contains advanced
    editing features like bold, italic, and text size adjustments, fully adhering to the HEAT color palette.
    """
    
    def __init__(self, master, keyword, palette):
        self.setup_bold_italic_tags()
        self.setup_binding()
        self.master = master
        self.keyword = keyword
        self.palette = palette
        self.flare = Toplevel(self.master)
        self.flare.title(f'Editing "{self.keyword}"')
        self.flare.geometry('400x300+200+200')  # Example geometry, can be changed as needed
        # Make sure the FLARE window stays on top
        self.pinned = False
        # Configuring text styling extensions for Flare Text Widget
        self.flare_text = flare_text
        self.bold_font = Font(family='Courier New', size=14, weight='bold')
        self.italic_font = Font(family='Courier New', size=14, slant='italic')
        self.normal_font = Font(family='Courier New', size=14)
        self.text_editor = Text(self.flare, wrap='word', undo=True,
                                bg=self.palette['raisin_black'][500], 
                                fg=self.palette['dark_purple'][200],
                                insertbackground=self.palette['wine'][200])           
        self.text_editor.pack(expand=True, fill='both')
        self.bind_events()
    
        def toggle_italic(self, event):
            # Toggle italic formatting for selected text
            current_tags = self.flare_text.tag_names("sel.first")
            if 'italic' not in current_tags:
                self.flare_text.tag_add('italic', "sel.first", "sel.last")
            else:
                self.flare_text.tag_remove('italic', "sel.first", "sel.last")
                # Configuring text styling extensions for Flare Text Widget
                self.flare_text = flare_text
                self.bold_font = Font(family='Courier New', size=14, weight='bold')
                self.italic_font = Font(family='Courier New', size=14, slant='italic')
                self.normal_font = Font(family='Courier New', size=14)
                
                self.setup_bold_italic_tags()
                self.setup_binding()

    def setup_bold_italic_tags(self):
        # Configuring styling tags for bold and italic
        self.flare_text.tag_configure("bold", font=self.bold_font)
        self.flare_text.tag_configure("italic", font=self.italic_font)
        self.flare_text.tag_configure("normal", font=self.normal_font)
    
    def setup_bold_italic_tags(self):
        # Configuring styling tags for bold and italic
        self.flare_text.tag_configure("bold", font=self.bold_font)
        self.flare_text.tag_configure("italic", font=self.italic_font)
        self.flare_text.tag_configure("normal", font=self.normal_font)

    def toggle_bold(self, event):
        # Toggle bold formatting for selected text
        current_tags = self.flare_text.tag_names("sel.first")
        if 'bold' not in current_tags:
            self.flare_text.tag_add('bold', "sel.first", "sel.last")
        else:
            self.flare_text.tag_remove('bold', "sel.first", "sel.last")

    def setup_binding(self):
        # Setup key-bindings for text formatting
        self.flare_text.bind("<Control-b>", self.toggle_bold)
        self.flare_text.bind("<Control-i>", self.toggle_italic)

    def bind_events(self):
        """ Binds events for user interaction including ctrl+click for hyperlink activation. """
        self.text_editor.bind('<Control-Button-1>', self.toggle_pinned_state)

    def toggle_pinned_state(self, event=None):
        """ Toggles whether the FLARE window should always stay on top or not. """
        self.pinned = not self.pinned
        self.flare.attributes('-topmost', self.pinned)
        
    def toggle_visibility(self, event=None):
        """ Toggles the visibility of the FLARE widget. """
        if self.flare.winfo_viewable():
            self.flare.withdraw()
        else:
            self.flare.deiconify()
