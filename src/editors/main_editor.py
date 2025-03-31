# Master file integrating all components for the HEAT UP text editor with advanced features
import tkinter as tk
from tkinter.font import Font, BOLD, ITALIC
from tkinter import Menu, simpledialog, filedialog, messagebox, font, Toplevel, Menu, Text

from src.editors.editor_configuration import EditorConfiguration  # Ensure this module exists
from src.widgets.document_widget import DocumentWidget  # Ensure this module exists
from src.widgets.flare_widget import FlareWidget  # Ensure this module exists
from src.editors.syntax_highlighter import SyntaxHighlighter  # Ensure this module exists


class MainEditor:
    """
    Main editor orchestrating the HEAT UP editor environment, integrating text editing functionalities
    with advanced features like syntax highlighting, document widgets, and flare widgets.
    """
    
    def __init__(self, master, root, palette_manager):
        """
        Initializes the main editor window with given color palette
        """
        self.root = root
        self.config = EditorConfiguration()
        self.document_widgets = {} # Stores active Document Widgets indexed by the keyword
        self.current_flare = None # Reference to the currently active Flare widget
        self.configure_root()
        self.text_widget = self.create_text_widget()
        self.words_to_widgets = {}  # Maps words to their respective HEAT UP document widgets
        self.setup_menu()
        self.setup_binding()
        self.master = master
        self.setup_ui()
        self.editor_config = EditorConfiguration()
        self.document_widgets = {}
        self.flare_widgets = {}
        self.syntax_highlighter = None
        self.root = root
        self.palette_manager = palette_manager
        self.font = Font(family="Courier New", size=14)
        self.text_widget = Text(root, wrap='none', undo=True, font=self.font)
        self.text_widget.pack(expand=True, fill='both')
        self.apply_palette()
        self.root.title("HEAT UP Editor - birdie")
        self.palette = palette
        self.editor_font = font.Font(family="Consolas", size=12)
        self.text_area = self._create_text_area()
        self.flare_widget = None
        self.propagation_engine = PropagationEngine()
        self._bind_events()
        self.document_widgets = {}
        # Bind Ctrl+Click to create hyperlink action
        self.text_widget.bind("<Control-Button-1>", self.create_hyperlink)
        self.text_area = ScrolledText(master, font=('Consolas', 12), undo=True, wrap=tk.WORD,
                                bg=self.config.get_color('dark_purple')['500'],
                                fg=self.config.get_color('white')['200'])
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.setup_bindings()

    def setup_bindings(self):
        """
        Setup the keyboard/mouse bindings for executing editor commands like open, save, find, etc.
        """
        self.text_area.bind('<Control-o>', lambda e: self.open_file())
        self.text_area.bind('<Control-s>', lambda e: self.save_file())
        self.text_area.bind('<Control-f>', lambda e: self.find_text())

    def setup_ui(self):
        """
        Initializes the main user interface components, menus, and text editing area.
        """
        self.master.title("HEAT UP Editor")
        self.text_area = tk.Text(self.master, wrap='word', undo=True,
                                 bg=self.editor_config.get_color('secondary'),
                                 fg=self.editor_config.get_color('primary'))
        self.text_area.pack(expand=True, fill='both')
        self.menu_bar = Menu(self.master)
        self.setup_menu()

    def create_document_widget(self, keyword):
        """
        Creates a new Document Widget for a keyword.
        Parameters:
            keyword (str): The keyword to create a Document Widget for
        """
        if keyword not in self.document_widgets:
            self.document_widgets[keyword] = DocumentWidget(linked_word=keyword)
            # Set the color based on Editor's palette
            self.document_widgets[keyword].color = self.config.palette['dark_red']

    def open_flare_widget(self, keyword):
        """
        Opens the FLR for the given keyword, if it exists, else creates one.
        Parameters:
            keyword (str): The keyword whose FLR to open
        """
        if keyword in self.document_widgets:
            if self.current_flare and self.current_flare.title == keyword:
                # if FLR widget is already open, simply toggle its state
                self.current_flare.toggle_state()
            else:
                # Create a new FLR widget for the keyword if it doesn't already exist
                self.current_flare = FlareWidget(title=keyword)
                self.current_flare.toggle_state()  # Open the FLR widget in 'edit' state
        else:
            print(f"No document widget found for the keyword '{keyword}'")
    
    def create_text_area(self):
        """
        Creates the main text area widget with scrollbar and custom styling.
        """
        text_area = tk.Text(self.root, font=self.editor_font, undo=True, wrap='word')
        text_area.pack(expand=True, fill='both', side='left', padx=5, pady=5)

        # Set the text area colors based on the palette
        text_area.configure(bg=self.palette['background'], fg=self.palette['foreground'])

        # Configure scrollbar for the text area
        scrollbar = tk.Scrollbar(self.root, command=text_area.yview)
        scrollbar.pack(side='right', fill='y')
        text_area['yscrollcommand'] = scrollbar.set

        return text_area
    
    def find_text(self):
        """
        Initiates a search within the text content based on a user-provided query.
        """
        search_query = simpledialog.askstring("Find", "Enter the search term:")
        if search_query:
            index = '1.0'
            while True:  # Continue searching until the last character
                index = self.text_area.search(search_query, index, nocase=True, stopindex=tk.END)
                if not index: break
                last_index = f"{index}+{len(search_query)}c"
                self.text_area.tag_add('highlight', index, last_index)
                index = last_index
            self.text_area.tag_config('highlight', background='yellow')

    def bind_events(self):
        """
        Binds key events and functionalities to the text area.
        """
        self.text_area.bind('<Control-Button-1>', self.on_ctrl_click)
        self.text_area.bind('<Control-s>', self.save_file)
        self.text_area.bind('<Control-o>', self.open_file)

    def on_ctrl_click(self, event):
        """
        Event handler for Ctrl+Click to create or manage Document Widgets and Flares.
        """
        clicked_word = self.get_clicked_word(event.x, event.y)
        if clicked_word:
            self.create_or_toggle_flare(clicked_word)

    def get_clicked_word(self, x, y):
        """
        Gets the word where the mouse event occurred.
        """
        index = self.text_area.index(f"@{x},{y}")
        word = self.text_area.get(index, f"{index} wordend")
        return word.strip()

    def create_or_toggle_flare(self, keyword):
        """
        Creates a new Document Widget and FLARE or toggles the existing one.
        """
        # Create a new HEAT UP Document Widget and Flare widget
        if keyword not in self.document_widgets:
            # The color property can be fetched from the color palette by string matching
            document_widget = DocumentWidget(self.root, keyword, color=self.palette['highlight'])
            flare = FlareWidget(title=f'FLARE: {keyword}', content='', palette=self.palette)
            self.document_widgets[keyword] = (document_widget, flare)
        # Toggle the visibility of the existing widget
        else:
            self.document_widgets[keyword][1].toggle_visibility()

    def save_file(self, event=None):
        """
        Save current content in the text area to a file.
        """
        file_path = simpledialog.askstring("Save as", "Enter the file name:")
        try:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get('1.0', tk.END))
        except IOError as e:
            messagebox.showerror("Save failed", e)

    def open_file(self, event=None):
        """
        Open content from a file into the text area.
        """
        file_path = simpledialog.askstring("Open file", "Enter the file name:")
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert('1.0', content)
        except IOError as e:
            messagebox.showerror("Open failed", e)
        
    def create_text_widget(self):
        # Create text widget with advanced features for editing
        text_widget = Text(self.root, wrap='none', font=('Courier New', 14), undo=True)
        text_widget.pack(expand=True, fill='both')
        return text_widget

    def create_new_word_widget(self, widget):
        # Create a new HEAT UP document widget
        heat_up_widget = Toplevel(self.root)
        heat_up_widget.title("FLARE Document")
        flare_text = Text(heat_up_widget, wrap='word', undo=True, font=('Courier New', 14))
        flare_text.pack(expand=True, fill='both')
        self.words_to_widgets[widget] = heat_up_widget

    def setup_menu(self):
        # Menu setup with file opening and saving functionalities
        menu_bar = Menu(self.root)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)
    
    def setup_document_widget(self, keyword):
        """
        Creates and configures document widgets that react to 'ctrl+click' to open associated FLARE windows.
        """
        if keyword not in self.document_widgets:
            document_widget = DocumentWidget(self.text_area, keyword, self.editor_config.get_full_palette())
            self.document_widgets[keyword] = document_widget
            # Bind the 'ctrl+click' functionality to the document widget
            self.text_area.bind('<Control-Button-1>', document_widget.on_ctrl_click, add='+')

    def setup_flare_widgets(self):
        """
        Manages flare widgets for in-depth editing linked to keywords within the document widget.
        """
        for keyword in self.document_widgets:
            if keyword not in self.flare_widgets:
                flare_widget = FlareWidget(self.master, keyword, self.editor_config.get_full_palette())
                self.flare_widgets[keyword] = flare_widget

    def setup_syntax_highlighter(self):
        """ Integrates the syntax highlighting mechanisms into the text editing area. """
        self.syntax_highlighter = SyntaxHighlighter(self.text_area, self.editor_config.get_color_palette())
        self.syntax_highlighter.highlight_syntax()

    def create_flare_widget(self):
        """
        Creates a floating FLARE widget for long-form text entry
        """
        flare_top = Toplevel(self.root)
        flare_top.title("FLARE Document")
        flare_text = Text(flare_top, wrap='word', undo=True, font=self.font)
        flare_text.pack(expand=True, fill='both')
        # Set cursor and selection color for the FLARE widget
        flare_text.configure(insertbackground=self.palette_manager.base_colors['primary'], selectbackground=self.palette_manager.base_colors['secondary'])

        # Apply bold, italic, fonts and other features to FLARE
        self.apply_text_features(flare_text)

    def create_widgets(self):
        """
        Creates and lays out the core widgets of the editor's user interface.
        """
        # Setting up the main editing text area with custom colors from the Tailwind palette
        self.text_area = tk.Text(self, bg=self.palette['raisin_black'][100], fg=self.palette['white'],
                                    insertbackground=self.palette['xanthous'],
                                    font=('Consolas', 12), undo=True, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH)

    def create_menu(self):
        """
        Creates the menu system for the editor with file and edit operations.
        """
        self.menu_bar = Menu(self.master)

        # File menu with new, open, save, and exit operations
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu with undo and redo for now; more can be added 
        edit_menu = Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.master.config(menu=self.menu_bar)

    def setup_menu(self):
        """
        Creates the editor's menu system for file operations and integrates it into the UI.
        """
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        # Additional menu definitions can be added here
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.master.config(menu=self.menu_bar)

    def open_file(self):
        """
        Opens a dialog box to select a file and loads its content into the text area.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert(tk.END, file.read())

    def save_file(self):
        """
        Saves the current content in the text area to a file.
        """
        file_path = filedialog.asksaveasfilename()
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get('1.0', tk.END))

    def open_file(self):
        # Open a file and set its content to the text_widget
        file_path = tk.filedialog.askopenfilename()
        with open(file_path, 'r') as file:
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, file.read())

    def save_file(self):
        # Save the current content in the text_widget to a file
        file_path = tk.filedialog.asksaveasfilename()
        with open(file_path, 'w') as file:
            file.write(self.text_widget.get(1.0, tk.END))

    def setup_binding(self):
        # Keyboard and mouse bindings
        self.text_widget.bind('<Control-Button-1>', self.create_hyperlink)

    def create_hyperlink(self, event):
        # Create hyperlink on Ctrl+Click on a word, also create a HEAT UP widget if it doesn't exist
        word_index = self.text_widget.index('@%d,%d' % (event.x, event.y))
        word = self.text_widget.get(word_index, word_index + ' wordend')
        self.text_widget.tag_add('link', word_index, word_index + ' wordend')
        self.text_widget.tag_config('link', foreground='red', underline=1)
        if word not in self.words_to_widgets:
            self.create_new_word_widget(word)
    
    def apply_palette(self):
        """
        Applies the color palette to the text widget for syntax highlighting
        """
        self.text_widget.configure(bg=self.palette_manager.base_colors['tertiary'], fg=self.palette_manager.base_colors['primary'])

    def create_hyperlink(self, event=None):
        """
        Creates a document widget and applies color to the selected word
        """
        # Get the index of the current mouse click
        mouse_index = self.text_widget.index('@%d,%d' % (event.x, event.y))
        # Set the tag configuration for hyperlinked word
        self.text_widget.tag_config("hyper", foreground=self.palette_manager.base_colors['dark_red'])
        # Apply the tag to the selected word
        self.text_widget.tag_add("hyper", mouse_index, "{} wordend".format(mouse_index))
        # Create a top-level window as the FLARE widget
        self.create_flare_widget()

    def apply_text_features(self, text_widget):
        """
        Adds text formatting features to a text widget: bold, italic, size, font
        """
        # Configure a bold font
        bold_font = Font(family='Courier New', size=14, weight='bold')
        text_widget.tag_configure('bold', font=bold_font)
        # Bind keyboard shortcuts for bold, italic, etc.
        text_widget.bind('<Control-b>', lambda e, tw=text_widget: self.set_bold(tw))
        # Italic, font size, and other features can be set similarly

    def set_bold(self, text_widget):
        """
        Toggles bold formatting on selected text in the text widget
        """
        try:
            current_tags = text_widget.tag_names("sel.first")
            # Add or remove the bold tag
            if 'bold' in current_tags:
                text_widget.tag_remove('bold', "sel.first", "sel.last")
            else:
                text_widget.tag_add('bold', "sel.first", "sel.last")
        except tk.TclError:
            pass  # No text selected

    def setup_syntax_highlighter(self):
        """
        Integrates syntax highlighting within the text editing area.
        """
        self.syntax_highlighter = SyntaxHighlighter(self.text_area, self.editor_config.get_full_palette())
        # Apply highlighting rules based on the language syntax

    def run_editor():
        # Base colors for the palette
        base_colors = {
            'primary': '#B2B2B2',
            'secondary': '#888888',
            'tertiary': '#333333',
            'quaternary': '#222222',
            'dark_red': '#8B0000'
        }
    

# To instantiate and run the application
if __name__ == '__main__':
    root = tk.Tk()
    root.title("HEAT UP Editor")
    root.geometry("800x600")
    palette_manager = PaletteManager(base_colors)
    main_editor = MainEditor(root, palette_manager)
    app = MainEditor(root)
    # Proceed to set up document and flare widgets and configure syntax highlighting
    root.mainloop()
