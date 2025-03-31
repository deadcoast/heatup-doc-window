# editor_ui.py establishes the overall user interface framework of the HEAT UP text editor {1AZ_t 5/6}

import tkinter as tk
from tkinter import Menu, simpledialog, filedialog, messagebox
from tkinter import Tk, Text, BOTH, W, N, E, S, Menu, filedialog, END, messagebox
from tkinter.ttk import Frame, Button, Label, Style

from src.widgets.document_widget import DocumentWidget
from src.widgets.flare_widget import FlareWidget
from src.editors.syntax_highlighter import SyntaxHighlighter
from src.editora_configuration import EditorConfiguration


class EditorUI(Frame):
    """
    The UI class for the HEAT UP editor, dealing with the graphical interface
    """
    def __init__(self, master, palette):
        super().__init__(master)
        self.initUI()
        self.palette = palette
        self.config(bg=self.palette['secondary'])  # Set the editor's bg color to a HEAT color
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.create_menu()

    def initUI(self):
        """
        Initializes the User Interface for the HEAT UP editor
        """
        self.master.title("HEAT UP - Retro Text Editor")
        self.pack(fill=BOTH, expand=True)

        # Create menu bar
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = Menu(menubar)
        file_menu.add_command(label="Open", command=self.on_open)
        file_menu.add_command(label="Save", command=self.on_save)
        menubar.add_cascade(label="File", menu=file_menu)

        # Create the editor's text area
        self.text_area = Text(self)
        self.text_area.pack(fill=BOTH, expand=True)

        # Define the editor's style using a retro appearance
        style = Style()
        style.configure("Editor.TFrame", background="#202020")
        style.configure("Editor.TButton", background="#505050", foreground="#FFFFFF")
        style.configure("Editor.TLabel", background="#303030", foreground="#FFFFFF")
        style.configure("Editor.TText", background="#303030", foreground="#FFFFFF", borderwidth=0)

        # Apply retro style to the text area
        self.text_area.configure(bg="#303030")
        self.text_area.configure(fg="#FFFFFF")
        self.text_area.configure(font=("Courier", 12))
        self.text_area.configure(insertbackground="#FFFFFF")  # Cursor color

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
    
    def create_widgets(self):
        """
        Creates and lays out the core widgets of the editor's user interface.
        """
        # Setting up the main editing text area with custom colors from the Tailwind palette
        self.text_area = tk.Text(self, bg=self.palette['raisin_black'][100], fg=self.palette['white'],
                                 insertbackground=self.palette['xanthous'],
                                 font=('Consolas', 12), undo=True, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH)
    
    def new_file(self):
        """
        Clears existing content to start a new file.
        """
        self.text_area.delete(1.0, tk.END)

    def on_open(self):
        """
        Handles the opening of files within the editor
        """
        file_path = filedialog.askopenfilename()
        with open(file_path, 'r') as file:
            self.text_area.delete('1.0', END)
            self.text_area.insert('1.0', file.read())

    def on_save(self):
        """
        Handles the saving of files within the editor
        """
        file_path = filedialog.asksaveasfilename()
        with open(file_path, 'w') as file:
            file.write(self.text_area.get('1.0', END))


    # Start the application
    def main():
        root = Tk()
        root.geometry("800x600+300+300")
        app = EditorUI(root)
        root.mainloop()

if __name__ == '__main__':
    main()

# Example use case:
# master is the Tk root, typically obtained from the main application bootstrapping file
# editor_palette is an object with access to the HEAT UP editor's color palette
# example_ui = EditorUI(master, editor_palette)
# example_ui.mainloop() # This will start the UI element's loop within the master Tk window
