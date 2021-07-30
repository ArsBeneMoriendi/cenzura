class Styles:
    Blue = 1
    Gray = 2
    Green = 3
    Red = 4
    Link = 5

class Components:
    def __init__(self, *rows):
        self.components = [row.__dict__ for row in rows]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self.guild.items()])}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self.guild.items()])}>"

    def add_row(self, row):
        self.components.append(row.__dict__)

class Row:
    def __init__(self, *items):
        self.type = 1
        self.components = [item.__dict__ for item in items]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self.guild.items()])}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self.guild.items()])}>"

    def add_button(self, item):
        self.components.append(item.__dict__)

class Button:
    def __init__(self, label: str = None, *, custom_id: str = None, style: int, url: str = None, disabled: bool = False, emoji: dict = None):
        self.type = 2
        self.label = label
        self.style = style
        if custom_id:
            self.custom_id = custom_id
        if url:
            self.url = url
        if disabled:
            self.disabled = disabled
        if emoji:
            self.emoji = emoji

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self.guild.items()])}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self.guild.items()])}>"

class SelectMenu:
    def __init__(self, *, custom_id: str, placeholder: str, min_values: int = 1, max_values: int = 1, disabled: bool = False, options):
        self.type = 3
        self.custom_id = custom_id
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.disabled = disabled
        self.options = [option.__dict__ for option in options]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self.guild.items()])}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self.guild.items()])}>"

    def add_option(self, option):
        self.components.append(option.__dict__)

class Option:
    def __init__(self, label: str, value: str, *, description: str = None, emoji: dict = None, default: bool = False):
        self.label = label
        self.value = value
        self.description = description
        self.emoji = emoji
        self.default = default

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self.guild.items()])}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self.guild.items()])}>"