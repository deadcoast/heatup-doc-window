

class EditorConfiguration:
    def __init__(self):
        self.palette = self._initialize_default_palette()

    def _initialize_default_palette(self):
        """
        Initializes the editor's default color palette, including a range of greys, charcoals, and dark reds.
        """
        return {
            'raisin_black': '#292331',
            'dark_purple': '#2d2636',
            'dark_purple_2': '#312a3b',
            'dark_purple_3': '#362e41',
            'dark_purple_4': '#442e3f',
            'wine': '#6c2c39',
            'auburn': '#a12a31',
            'xanthous': '#fcbf49',
            'peach_yellow': '#fedfa4',
            'white': '#ffffff',
            'custom_colors': {}  # Users can add their own hex codes for additional themes
        }

    @staticmethod
    def load_tailwind_palette():
        """ Load the official HEAT Tailwind color palette """
        return {
            'raisin_black': ['#08070a', '#100e13', '#18141d', '#201b26', '#292331', '#524562', '#7c6994', '#a79bb8', '#d3cddb'],
            'dark_purple': ['#09080b', '#120f15', '#1b1720', '#241e2b', '#2d2636', '#564967', '#7f6c97', '#a99dba', '#d4cedc'],
            'wine': ['#16090b', '#2b1217', '#411b22', '#57232e', '#6c2c39', '#9f4154', '#c16779', '#d69aa6', '#eaccd2'],
            'auburn': ['#20080a', '#411114', '#61191e', '#822128', '#a12a31', '#cd3c46', '#d96d74', '#e69ea3', '#f2ced1'],
            'xanthous': ['#402b01', '#815602', '#c18203', '#fbab0a', '#fcbf49', '#fdcd6e', '#fdda92', '#fee6b7', '#fef3db'],
            'peach_yellow': ['#533601', '#a66c02', '#f8a203', '#fdc151', '#fedfa4', '#fee5b6', '#feecc8', '#fff2db', '#fff9ed'],
            'white': ['#333333', '#666666', '#999999', '#cccccc', '#ffffff']
        }


        # Hex code validation
        if not isinstance(hex_code, str) or not hex_code.startswith('#'):
            raise ValueError(f"Invalid hex code: {hex_code}. Hex codes should start with '#' and be valid colors.")
        
        # Add the validated custom color to the palette
        self.palette['custom_colors'][key] = hex_code

    def get_full_palette(self):
        """
        Retrieves the combined color palette of predefined colors and user-defined custom colors.
        Returns:
            dict: A dictionary containing both sets of colors.
        """
        return {**self.palette, **self.palette['custom_colors']}

    def add_custom_color(self, key, hex_code):
        """
        Provides the capability for users to add custom colors to the palette.
        """
        # Validation ensures color codes are in the proper format.
        if key in self.palette:
            raise KeyError(f"Key {key} is already in use.")
        if not isinstance(hex_code, str) or not hex_code.startswith('#'):
            raise ValueError("Hex code must be a valid string starting with '#'.")

        self.palette['custom_colors'][key] = hex_code

    def get_color(self, key):
        """
        Retrieves a specific color by key, supporting both default and custom colors.
        """
        # Extraction logic accounts for all elements of the color palette.
        return self.palette.get(key, self.palette['custom_colors'].get(key))

    def remove_custom_color(self, key):
        """
        Allows users to remove custom colors from the palette.
        """
        # Removal logic includes error handling for non-existent keys.
        try:
            del self.palette['custom_colors'][key]
        except KeyError:
            raise KeyError(f"No custom color found for key '{key}'.")

    def get_color_palette(self):
        """ Retrieves the complete color palette, including custom colors """
        return self.palette

    def get_color(self, key):
        """ Retrieve a specific color by key """
        return self.palette.get(key) or self.palette['custom_colors'].get(key)