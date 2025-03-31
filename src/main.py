# Final synergy and execution of the HEAT UP advanced text editor with state-of-the-art advancements {1AZ_t 5/5}

import tkinter as tk
from editor.editor_configuration import EditorConfiguration
from editor.editor_effects import EditorEffects
from editor.editor_events import EditorEvents
from editor.editor_ui import EditorUI
from editor.heatup_editor import HeatUpEditor
from editor.main_editor import MainEditor
from editor.syntax_highlighter import SyntaxHighlighter

from managers.autocomplete_manager import AutocompleteManager
from managers.cross_linking_manager import CrossLinkingManager
from managers.inline_search_manager import InlineSearchManager
from managers.palette_manager import PaletteManager
from managers.theme_manager import ThemeManager

from widgets.document_widget import DocumentWidget
from widgets.flare_widget import FlareWidget
from widgets.user_experience_enhancement import UserExperienceEnhancements


def main():
    root = tk.Tk()
    root.title("HEAT UP - Advanced Code Editor")

    # Initialize the text widget
    text_widget = Text(root, wrap='none', undo=True)
    text_widget.pack(expand=True, fill='both')

    # Instantiate the editor configuration with the HEAT color palette
    color_palette = heat_palette.get_palette()
    editor_config = EditorConfiguration(color_palette)
    palette_manager = PaletteManager(text_widget)
    palette_manager.apply_palette_to_widget()

    # Auto-complete words (this list can be expanded or loaded from a file)
    word_list = ['function', 'variable', 'class', 'editor', 'palette', 'widget']
    autocomplete_manager = AutoCompleteManager(text_widget, word_list)

    # Theming
    theme_manager = ThemeManager(text_widget)
    theme_manager.apply_theme()
    # Retro Theme
    retro_theme_manager = RetroThemeManager(editor_ui_instance)
    
    # Syntax Highlighter
    syntax_highlighter = SyntaxHighlighter(main_editor.get_text_widget(), color_palette)
    syntax_highlighter.apply_highlighting_rules()

    # Initialize Main Editor with configuration
    main_editor = MainEditor(root, editor_config)

    # Set up the Editor UI interface
    editor_ui = EditorUI(root)
    main_editor.set_ui(editor_ui)
    
    # Binding enhancements to the UI
    user_experience_enhancements = UserExperienceEnhancements(text_widget)
    user_experience_enhancements.bind_enhancements()

    # Instantiate the Flare Widget for editing
    flare_widget = FlareWidget(root, palette=color_palette)
    # Bind 'Ctrl+Click' action to create hyperlinks that open the Flare Widget
    main_editor.setup_flare_bindings(flare_widget)

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == '__main__':
    main()