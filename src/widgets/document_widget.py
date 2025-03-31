# {1AZ_t #step/#total} [COMMENTS ]
# document_widget.py manages keyword-to-flare interactions within the HEAT UP editor
import tkinter as tk
import tkinter as tk
from tkinter import Toplevel, Text, simpledialog, Menu, messagebox
from tkinter.font import Font


class DocumentWidget(tk.Text):
    """
    Initialize a document widget with in-depth features.
    Parameters:
        master (tk.Widget): The parent widget.
        linked_word (str): Keyword triggering the document widget.
        content (str): Content inside the document.
        color (str): HEX color for the keyword highlight.
    """
    def __init__(self, master, linked_word, parent, keyword, palette, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.keyword = keyword
        self.palette = palette
        self.configure(bg=palette['raisin_black'][500], fg=palette['white'][100])
        self.bind("<Control-Button-1>", self.on_ctrl_click)
        parent.add_with_tag(self, keyword)
        self.linked_word = linked_word
        self.content = content
        self.color = color
        self.is_flare_visible = False
        self.id = str(uuid.uuid4())  # Unique identifier for the widget
        self.linked_word = linked_word
        self.content = content
        self.color = color
        self.master = master
        self.flare_widget = None  # Initialize without a Flare widget
        self._create_flare_widget()        
        # Bind the Ctrl+Click event to open the FLARE window
        self.master.bind('<Control-Button-1>', self.ctrl_click_event)
        self.parent = parent
        self.content = content
        self.palette = palette if palette else self._generate_default_palette()
        self.title = title
        self.text_widget = self._create_text_widget()
        self._style_widget_with_palette()
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

    def _create_text_widget(self):
        # Create a Tkinter Text widget for content editing
        text_widget = tk.Text(self.parent, wrap=tk.WORD, font=('Consolas', 12), undo=True, pady=10)
        text_widget.pack(expand=True, fill=tk.BOTH)
        return text_widget

    def _generate_default_palette(self):
        # Fallback method to generate a default color palette for the widget
        return {"background": "#292331", "foreground": "#E5E7EB", "insert": "#fcbf49",
                "highlight": "#a12a31", "accent": "#fedfa4", "title_bg": "#2d2636"}

    def _style_widget_with_palette(self):
        # Apply the color palette to the text widget for an engaging user experience
        title_font = font.Font(size=14, weight="bold", family='Consolas')
        self.text_widget.tag_configure("title", background=self.palette['title_bg'],
                                       foreground=self.palette['foreground'], font=title_font)
        self.text_widget.tag_configure("highlight", background=self.palette['highlight'])
        self.text_widget.tag_configure("accent", foreground=self.palette['accent'])

        # Insert the title at the top of the widget
        self.text_widget.insert(tk.END, f"{self.title}\n", "title")

        # Insert initial content with highlighted keywords as an example
        self.text_widget.insert(tk.END, self.content)
        self.text_widget.highlight_pattern(self.title, "highlight")

        # Configure the widget aesthetics such as cursor and selection colors
        self.text_widget.config(bg=self.palette['background'], fg=self.palette['foreground'],
                                insertbackground=self.palette['insert'], selectbackground=self.palette['accent'])

    def highlight_pattern(self, pattern, tag, start="1.0", end="end", regexp=False):
        # Function to highlight all occurrences of a given pattern
        start = self.text_widget.index(start)
        end = self.text_widget.index(end)
        self.text_widget.mark_set("matchStart", start)
        self.text_widget.mark_set("matchEnd", start)
        self.text_widget.mark_set("searchLimit", end)

        count = tk.StringVar()
        while True:
            index = self.text_widget.search(pattern, "matchEnd","searchLimit", count=count, regexp=regexp)
            if index == "": break
            if count.get() == '0': break  # no match was found
            self.text_widget.mark_set("matchStart", index)
            self.text_widget.mark_set("matchEnd", f"{index}+{count.get()}c")
            self.text_widget.tag_add(tag, "matchStart", "matchEnd")
    
    def ctrl_click_event(self, event):
        # Check if the click is within a HEAT UP word and open/hide the related FLARE window
        clicked_idx = self.master.index("@%d,%d" % (event.x, event.y))
        clicked_word = self.master.get(clicked_idx, f"{clicked_idx} wordend")
        
        if clicked_word == self.linked_word:
            # Toggle the FLARE window on Ctrl+Click
            self.toggle_flare_visibility()

    def create_flare_widget(self, palette):
        # Create a floating FLARE window with editable text
        flare_widget = Toplevel(self.master)
        flare_widget.title(f"FLARE: {self.linked_word}")
        flare_widget.geometry("400x300")  # Set the window size
        flare_widget.configure(bg=self.palette['secondary'])  # Use the secondary color as the background
        flare = Toplevel(self.master)
        flare.title(f"Editing: {self.linked_word}")
        flare.withdraw()  # Start with the flare window hidden
        # Create a text area with a scrollbar within the FLARE window
        text_area = Text(self.flare_widget, wrap='word', bg=self.palette['secondary'], fg=self.palette['primary'],
                         insertbackground=self.palette['primary'], font=('Consolas', 12))
        text_area.pack(expand=True, fill='both', padx=5, pady=5)  # Padding for aesthetics

        scrollbar = Scrollbar(self.flare_widget, orient='vertical', command=text_area.yview)
        scrollbar.pack(side='right', fill='y')
        text_area.config(yscrollcommand=scrollbar.set)

        # Enhance window visibility on hover
        self.flare_widget.bind('<Enter>', lambda e: self.flare_widget.attributes("-alpha", 0.9))  # More transparent on hover
        self.flare_widget.bind('<Leave>', lambda e: self.flare_widget.attributes("-alpha", 1))  # Less transparent when not hovered
        self.flare_widget.withdraw()  # Hide FLARE window initially

    def toggle_flare_visibility(self):
        """Toggles the visibility of the associated FLARE widget."""
        self.is_flare_visible = not self.is_flare_visible
        self.title = title  
        self.content = content
        # FLR Editor State, can be 'view' or 'edit'
        self.state = 'view'
    
    def update_content(self, new_content):
        """
        Updates the content of the document widget's FLARE content.
        Parameters:
            new_content (str): The new content to update in the flare.
        """
        # You might have additional logic to handle content changes
        self.content = new_content
        self.text_area.delete('1.0', 'end')
        self.text_area.insert('1.0', new_content)

    def save_changes(self):
        """
        Saves any modifications made in the FLARE text area to the main content.
        """
        updated_content = self.text_area.get('1.0', 'end-1c')  # Fetches text from Text widget
        self.update_content(updated_content)
        # Here you can add logic to persist changes to a file or database

    def get_content(self):
        """
        Retrieves the current content from this document widget.
        Returns:
            str: The current document content.
        """
        return self.content

    def __str__(self):
        """
        Returns a string representation of the document widget, useful for debugging.
        """
        return f"DocumentWidget(id='{self.id}', linked_word='{self.linked_word}', content='{self.content[:30]}...')"

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
