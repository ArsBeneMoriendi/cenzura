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
    def __init__(self, *buttons):
        self.type = 1
        self.components = [button.__dict__ for button in buttons]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self.guild.items()])}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(['{}={!r}'.format(k, v) for k,v in self.guild.items()])}>"

    def add_button(self, button):
        self.components.append(button.__dict__)

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