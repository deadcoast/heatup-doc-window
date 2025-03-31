
class InlineSearchManager:
    """
    Handles inline search within the document
    """
    def init(self, text_widget):
        self.text_widget = text_widget

    def search_for_text(self, search_query):
        # Search for the query text and highlight all occurrences
        start_index = '1.0'
        while True:
            start_index = self.text_widget.search(search_query, start_index, stopindex=tk.END)
            if not start_index:
                break
            end_index = f"{start_index}+{len(search_query)}c"
            self.text_widget.tag_add('search', start_index, end_index)
            self.text_widget.tag_config('search', background='yellow')
            start_index = end_index
        self.text_widget.tag_remove('sel', '1.0', tk.END) # Clear existing selections

    def bind_search(self):
        # Bind key combination for inline search functionality
        self.text_widget.bind('<Control-f>', self.prompt_search_query)

    def prompt_search_query(self, event):
        # Prompt user for search query
        search_query = simpledialog.askstring("Search", "Enter search text:")
        if search_query:
            self.search_for_text(search_query)