# Master file integrating all components for the HEAT UP text editor with advanced features
import tkinter as tk
from tkinter import Toplevel, simpledialog, Menu, Text, filedialog
from tkinter.font import Font, BOLD, ITALIC
import tkinter as tk
from tkinter import Menu, simpledialog, filedialog, messagebox
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

        # Bind Ctrl+Click to create hyperlink action
        self.text_widget.bind("<Control-Button-1>", self.create_hyperlink)

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
