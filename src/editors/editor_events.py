# Event handling for HEAT UP editor (assuming tkinter for GUI)

class EditorEvents:
    """
    The Events class is responsible for handling user interactions with widgets
    """
    def __init__(self, ui_instance, editor_instance):
        """
        Initializes the event handlers for the editor
        Parameters:
            ui_instance (EditorUI): The instance of the HEAT UP Editor UI
            editor_instance (Editor): The instance of the HEAT UP Editor logic
        """
        self.ui = ui_instance
        self.editor = editor_instance
        self.register_event_handlers()

    def register_event_handlers(self):
        """
        Registers the event handlers to the UI components
        """
        # Bind 'Ctrl+Click' to the create HEAT UP event
        self.ui.text_area.bind('<Control-Button-1>', self.ctrl_click_event)
        # Other events can be added here
        
    def ctrl_click_event(self, event):
        """
        Handles the 'Ctrl+Click' event to create Document Widgets (HEAT UP)
        Parameters:
            event: The event data containing information about the click
        """
        # Get the position of the mouse click
        pos = event.widget.index("@{},{}".format(event.x, event.y))
        # Using the position, extract the word at the cursor
        word = event.widget.get("{}.start".format(pos), "{}.end".format(pos))
        
        if word:
            # Create a document widget for the extracted word
            self.editor.create_document_widget(word)
            # Open the flare widget for the extracted word
            self.editor.open_flare_widget(word)
        

# Assuming 'editor_ui_instance' and 'editor_instance' are already created instances of the UI and Editor
editor_events = EditorEvents(editor_ui_instance, editor_instance)