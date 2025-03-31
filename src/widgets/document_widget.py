# {1AZ_t #step/#total} [COMMENTS ]
# document_widget.py manages keyword-to-flare interactions within the HEAT UP editor
import tkinter as tk
import tkinter as tk
from tkinter import Toplevel, Text, simpledialog, Menu, messagebox
from tkinter.font import Font


class DocumentWidget(tk.Text):
    """
    Enhances the keyword interaction within the editor, allowing 'ctrl+click' to highlight 
    and create document widgets (FLARE) for expanded, in-depth editing.
    """
    def __init__(self, parent, keyword, palette, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.keyword = keyword
        self.palette = palette
        self.configure(bg=palette['raisin_black'][500], fg=palette['white'][100])
        self.bind("<Control-Button-1>", self.on_ctrl_click)
        parent.add_with_tag(self, keyword)

    def on_ctrl_click(self, event):
        """ Handles 'ctrl+click' to create or view the corresponding FLARE window. """
        # The implementation should create a FlareWidget or bring it to view if already created
        pass  # Logic for handling ctrl+click will be implemented here

    def highlight_keyword(self):
        """ Applies the predefined color to the keyword within the editor. """
        start_index = f'1.0'
        while True:
            start_index = self.search(self.keyword, start_index, tk.END)
            if not start_index:
                break
            end_index = f"{start_index}+{len(self.keyword)}c"
            self.tag_add('highlight', start_index, end_index)
            self.tag_config('highlight', background=self.palette['dark_purple'][300])
            start_index = end_index
        # Additional logic could be implemented for removing highlights or changing the keyword
