# {1AZ_t #step/#total} [COMMENTS ]

# Comprehensive Flare Widget for the HEAT UP editor with pinning and advanced text editing features

import tkinter as tk
from tkinter import Toplevel, Text
import tkinter as tk
from tkinter import Toplevel, Text, Scrollbar, font, Frame, Scrollbar
# Depending on the platform, use the appropriate library for window effects
try:
    import win32gui
    import win32con
    platform_specific = 'MacOSX'
except ImportError:
    platform_specific = 'Other'


class FlareWidget(Frame):
    """
    Initialize the FLARE widget with a sophisticated in-depth editor.
    Parameters:
        master (tk.Tk): The master Tkinter application/window object.
        title (str): The title for the FLARE window.
        keyword (str): The linked keyword which opens the FLARE window upon Ctrl+Click.
        content (str): The initial content for the in-depth editor.
        palette (dict): The dictionary containing the color palette.
    """
    
    def __init__(self, master, title, keyword, content='', palette=None):
        super().__init__(parent, *args, **kwargs)
        self.title = title
        self.content = content
        # FLR Editor State, can be 'view' or 'edit'
        self.state = 'view'
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
        self.master = master
        self.title = title
        self.keyword = keyword
        self.content = content
        self.palette = palette or self.default_palette()
        self.create_widget()
        self.keyword = keyword
        self.palette = palette
        self.text_editor = tk.Text(self)
        self.configure_widget()
        self.populate_text_editor()
        self._configure_appearance()
        self.is_pinned = False  # Track pinning state
        self._create_widgets()
        self._apply_styling()

    def _create_widgets(self):
        """ Create and place the text editor and scrollbar within the widget. """
        self.text_editor = Text(self, wrap=tk.WORD, undo=True, font=('Consolas', 12))
        self.text_editor.pack(expand=True, fill=tk.BOTH)
        self.text_editor.insert(tk.END, self.content)

        # Scrollbar for the text editor
        self.scrollbar = Scrollbar(self, command=self.text_editor.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_editor['yscrollcommand'] = self.scrollbar.set
    
    def _apply_styling(self):
        """ Apply theme styling from the palette and custom configurations. """
        self.text_editor.config(
            bg=self.palette['editor_bg'] if self.palette else '#312a3b',
            fg=self.palette['editor_fg'] if self.palette else '#ffffff',
            insertbackground=self.palette['xanthous'] if self.palette else '#fcbf49'
        )

    def _configure_appearance(self):
        """
        Configures the FlareWidget's aesthetics and keybindings for an intuitive coding environment.
        """
        # Apply the color theme
        self.config(bg=self.palette['base']['background'])
        self.text_editor.config(
            bg=self.palette['base']['background'],
            fg=self.palette['base']['foreground'],
            insertbackground=self.palette['highlight']
        )

        # Custom keybinding for formatting (bold, italic) and key actions (save, close)
        self.text_editor.bind('<Control-b>', self._apply_bold)
        self.text_editor.bind('<Control-i>', self._apply_italic)
        self.text_editor.bind('<Control-s>', self._save_content)
        self.text_editor.bind('<Escape>', lambda _: self.place_forget())
    
    def configure_widget(self):
        """
        Configures the initial appearance of the FLARE widget, utilising the HEAT color palette.
        """
        # Set the aesthetics for the FLARE window
        self.config(bg=self.palette['dark_purple'][500])
        self.text_editor.config(
            font=font.Font(family="Consolas", size=12, weight='normal'),
            bg=self.palette['dark_purple'][200],
            fg=self.palette['peach_yellow'][100],
            insertbackground=self.palette['xanthous'][500]  # Cursor color
        )
        # Borderless and rounded corners are OS-specific and need manual implementation
        self.text_editor.pack(expand=True, fill='both')
    
    def populate_text_editor(self):
        """
        Populates the text editor with sample text and sets up rich text formatting features.
        """
        # Insertion of sample text for demonstration
        sample_text = f"This is the sample text for keyword '{self.keyword}'.\n"
        sample_text += "The FLARE widget aims to provide a detailed editing pane.\n"
        self.text_editor.insert('1.0', sample_text)

        # Setup for other typical text editing functionalities (bold, italic, underline)
        self.text_editor.tag_configure('bold', font=font.Font(family="Consolas", size=12, weight='bold'))
        self.text_editor.tag_configure('italic', font=font.Font(family="Consolas", size=12, slant='italic'))

    def toggle_visibility(self):
        """
        Toggles the visibility of the FLARE widget based on user interaction.
        """
        if self.winfo_viewable():
            self.place_forget()  # Hide the widget
        else:
            self.place(relx=0.5, rely=0.5, anchor='center')  # Show the widget in the center of parent

    
    def _build_ui(self):
        """ Constructs the user interface for the FLARE widget. """
        self.window = Toplevel()
        self.window.title(f"FLARE: {self.title}")
        self.window.geometry('600x400')  # Ideal size for an editor window
        self.window.resizable(True, True)  # Allow window resizing
        self.window.configure(bg=self.palette['secondary'])

        # Text Area creation with custom aesthetics
        self.text_area = Text(self.window, wrap='word', bd=0, undo=True,
                              font=('Consolas', 12), padx=10, pady=10,
                              relief='flat', highlightthickness=0)
        self.text_area.insert('1.0', self.content)
        self.text_area.pack(side="top", fill="both", expand=True)

        # Create and pack the scrollbar
        scrollbar = ttk.Scrollbar(self.window, orient='vertical', command=self.text_area.yview)
        scrollbar.pack(side='right', fill='y')
        self.text_area['yscrollcommand'] = scrollbar.set

        # Apply the custom theme
        self._apply_theme()
        self.window.bind('<FocusIn>', lambda _: self.window.attributes('-alpha', 1.0))
        self.window.bind('<FocusOut>', lambda _: self.window.attributes('-alpha', 0.8))
    
    def _apply_window_style(self):
        """
        Applies borderless window style with rounded corners, if supported by the OS.
        """
        if platform_specific == 'Windows':
            # Obtain current window style
            style = win32gui.GetWindowLong(self.window.winfo_id(), win32con.GWL_STYLE)
            # Set new window style without border
            style = style & ~win32con.WS_OVERLAPPEDWINDOW
            win32gui.SetWindowLong(self.window.winfo_id(), win32con.GWL_STYLE, style)
            # Remove window title bar to make it borderless
            self.window.overrideredirect(True)
            # Additional, more intricate steps would be necessary to add custom minimize/maximize/close buttons

    def _configure_widget(self, palette, content):
        """
        Configures the FLARE widget's text area with aesthetic options.
        Parameters:
            palette (dict): Color palette to style the widget.
            content (str): Content to preload into the text area.
        """
        self.text_area.insert('1.0', content)
        self.text_area.pack(expand=True, fill='both')
        Scrollbar(self.window, command=self.text_area.yview).pack(side='right', fill='y')
        
        # Apply color theme from the palette
        self.text_area.configure(bg=palette['background'], fg=palette['foreground'])

    def _apply_theme(self):
        """ Apply the color theme to this widget based on the provided palette. """
        self.text_area.configure(bg=self.palette['500'], fg=self.palette['50'],
                                 insertbackground=self.palette['100'])

        for theme in ['r', 'g', 'b']:
            self.text_area.tag_configure(f'highlight_{theme}', background=self.palette[f'highlight_{theme}'])

    def _default_palette(self):
        """ Provides a default color palette, scaled from dark to light. """
        # This would be a subset of the provided official HEAT color palette
        return {
            '50': '#fef3db',      # For normal text
            '100': '#fee6b7',     # For insert cursor
            '500': '#292331',     # Background for editor
            # Add other color levels as needed
            'highlight_r': '#6c2c39',    # Highlight background color for red-themed text
            'highlight_g': '#a12a31',    # Highlight background color for green-themed text
            'highlight_b': '#fcbf49',    # Highlight background color for blue-themed text
        }

    def show(self):
        """ Method for showing the Flare Widget with all UI enhancements. """
        self.window.deiconify()
        self.text_area.focus_set()

    def hide(self):
        """ Method for hiding the Flare Widget. """
        self.window.withdraw()

    def create_widget(self):
        """
        Constructs the FLARE window with all its rich text capabilities and aesthetic elements.
        """
        self.window = Toplevel(self.master)
        self.window.title(f"FLARE: {self.title}")
        self.window.geometry('600x400')

        # Configure the main text area
        self.text_area = Text(self.window, wrap='word')
        self.text_area.insert('1.0', self.content)
        self.text_area.pack(expand=True, fill='both')

        # Implement rich text features like font choices, bold, italic, etc.
        self.setup_text_features()

        # Add a scrollbar
        scrollbar = Scrollbar(self.window, command=self.text_area.yview)
        scrollbar.pack(side='right', fill='y')
        self.text_area.config(yscrollcommand=scrollbar.set)

        # Apply the color scheme from the palette
        self.apply_colors()

    def setup_text_features(self):
        """
        Configures text styling features like bold, italic, and font size adjustments.
        """
        # Example: Configure a bold font
        bold_font = Font(family='Consolas', size=12, weight='bold')
        self.text_area.tag_configure('bold', font=bold_font)  # Tag to handle bold text style
        # Similar setup for italic and other styles

        # Bind keys for text styling
        self.text_area.bind('<Control-b>', lambda event: self.toggle_style('bold'))
        self.text_area.bind('<Control-i>', lambda event: self.toggle_style('italic'))
        # Add more bindings for additional styles

    def toggle_style(self, tag_name):
        """
        Toggles the assigned style tag_name based on current text selection in the text area.
        """
        current_tags = self.text_area.tag_names('sel.first')
        if tag_name in current_tags:
            self.text_area.tag_remove(tag_name, 'sel.first', 'sel.last')
        else:
            self.text_area.tag_add(tag_name, 'sel.first', 'sel.last')

    def apply_colors(self):
        """
        Alters the color scheme of the text area to match the palette assigned to the flare widget.
        """
        self.text_area.config(bg=self.palette['secondary'], fg=self.palette['primary'],
                              insertbackground=self.palette['primary'])

    @staticmethod
    def default_palette():
        """
        Provides a default palette if none is specified. This is a fallback and can be omitted if a palette is guaranteed.
        """
        return {
            'primary': '#ffffff',
            'secondary': '#292331',  # From the HEAT Tailwind palette provided
            # ... add all the other color shade mappings
        }

    def update_content(self, new_content):
        """
        Updates the content of the Flare editor window.
        Parameters:
            new_content (str): The new content for the editor.
        """
        self.text_area.delete('1.0', tk.END)
        self

    def set_content(self, new_content):
        """
        Sets the content of the FLR.
        Parameters:
            new_content (str): The new content to set into the FLR
        """
        self.content = new_content

    def toggle_state(self):
        """
        Toggles the FLR's state between 'view' and 'edit' modes.
        """
        self.state = 'edit' if self.state == 'view' else 'view'
        self.update_content()
    
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

    def on_ctrl_click(self, event):
        """ Handler for the Ctrl+Click event to toggle the visibility of the FLARE widget. """
        self.toggle_visibility()
        
    def toggle_visibility(self):
        """ Toggles the visibility of this FLARE widget. """
        if self.window.state() == 'normal':
            self.window.withdraw()
        else:
            self.window.deiconify()
            self.window.focus_set()

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
