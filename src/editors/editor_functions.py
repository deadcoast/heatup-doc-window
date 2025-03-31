# Advanced Editor Functionality
class EditorFunctions:
    def __init__(self, root, text_widget):
        """
        Adds an array of advanced functionalities to the main editor
        Parameters:
            root (tk.Tk): The Tkinter root object
            text_widget (tk.Text): The main text editor widget
        """
        self.root = root
        self.text_widget = text_widget
        self.flare_widgets = {}
        self.theme_manager = PaletteManager()
        self.cross_linking_manager = CrossLinkingManager(self.text_widget, self.flare_widgets)

    def handle_hyperlink_event(self, event):
        # Get the word where the event occurred and create or raise the Flare Widget
        mouse_index = self.text_widget.index("@%d,%d" % (event.x, event.y))
        selected_word = self.text_widget.get(mouse_index, f"{mouse_index} wordend")
        self.cross_linking_manager.insert_link(mouse_index, f"{mouse_index} wordend", selected_word)
        # Apply the color for the hyperlink
        self.text_widget.tag_config(selected_word, foreground=self.theme_manager.base_colors['dark_red'])
        # Open or raise the Flare Widget for extensive editing
        self.cross_linking_manager.link_to_flare(selected_word)

    def setup_advanced_bindings(self):
        # Bind advanced editor functions like hyperlink event
        self.text_widget.bind("<Control-Button-1>", self.handle_hyperlink_event)
