

class EditorConfiguration:
    def __init__(self):
        # Initialize a color palette with default and customizable color slots.
        self.palette = {
            'primary': '#FFFFFF',
            'palette': self.load_tailwind_palette(),
            'custom_colors': {}
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

    def add_custom_color(self, key, hex_code):
        """
        Allows a user to define a custom color, validating the hex format.
        
        Parameters:
            key (str): The name for the custom color.
            hex_code (str): The hex color code (e.g., "#FFFFFF").
        """
        if not isinstance(key, str) or not key.isidentifier():
            raise ValueError("Key must be a valid identifier.")
        if not isinstance(hex_code, str) or not hex_code.startswith('#'):
            raise ValueError("Invalid hex code format.")
        self.palette['custom_colors'][key] = hex_code

    def remove_custom_color(self, key):
        """
        Removes a custom color, identified by its key.
        
        Parameters:
            key (str): The name for the custom color.
        """
        self.palette['custom_colors'].pop(key, None)  # Silently ignore if key does not exist

    def get_color_palette(self):
        """ Retrieves the complete color palette, including custom colors """
        return self.palette

    def get_color(self, key):
        """ Retrieve a specific color by key """
        return self.palette.get(key) or self.palette['custom_colors'].get(key)