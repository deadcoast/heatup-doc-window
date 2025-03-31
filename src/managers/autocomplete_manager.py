
class AutoCompleteManager:
    def __init__(self, text_widget, word_list=None):
        self.text_widget = text_widget
        self.word_list = word_list if word_list else []
        self.bind_auto_complete()

    def bind_auto_complete(self):
        # Bind to key-release events to suggest autocomplete options
        self.text_widget.bind('<KeyRelease>', self.on_key_release)

    def on_key_release(self, event):
        # Show auto-complete suggestions if applicable
        typed_word = event.widget.get("insert linestart", "insert")
        last_word = typed_word.split()[-1]
        if last_word:
            self.show_suggestions(last_word, event.widget.index("insert"))

    def show_suggestions(self, typed_word, position):
        # Displays the suggestions in the UI
        suggestions = [w for w in self.word_list if w.startswith(typed_word)]
        self.text_widget.delete("%s linestart" % position, position)
        self.text_widget.insert("%s linestart" % position, ' '.join(typed_word.split()[:-1]) + ' ' + (suggestions[0] if suggestions else typed_word))
        self.text_widget.mark_set("insert", position)
        
