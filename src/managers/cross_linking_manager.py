# Advanced Cross-Linking for Flare Widgets (Document Widgets)


class CrossLinkingManager:
    def __init__(self, text_widget, flare_widgets):
        """
        Manages cross-linking between various parts of documents and FLARE widgets
        Parameters:
            text_widget (tk.Text): The main text editor widget
            flare_widgets (dict): Dictionary mapping document keywords to FLARE widgets
        """
        self.text_widget = text_widget
        self.flare_widgets = flare_widgets

    def link_to_flare(self, keyword):
        # Check if FLARE widget already exists for keyword, if not, create one
        if keyword not in self.flare_widgets:
            flare_widget = Toplevel(self.text_widget)
            flare_widget.title(keyword)
            flare_text = Text(flare_widget)
            flare_text.pack(expand=True, fill='both')
            self.flare_widgets[keyword] = flare_text
        # Bring the FLARE widget associated with the keyword to the front
        self.flare_widgets[keyword].tkraise()

    def insert_link(self, start_idx, end_idx, keyword):
        # Insert a clickable link that will open the associated FLARE widget
        self.text_widget.tag_add(keyword, start_idx, end_idx)
        # Bind mouse click event to the link_to_flare method
        self.text_widget.tag_bind(keyword, "<Button-1>", lambda e, kw=keyword: self.link_to_flare(kw))