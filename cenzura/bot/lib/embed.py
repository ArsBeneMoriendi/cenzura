class Embed:
    def __init__(self, **kwargs):
        allowed_args = ("title", "description", "color")

        for key, value in kwargs.items():
            if key in allowed_args:
                setattr(self, key, value)

    def set_image(self, *, url: str):
        self.image = {"url": url}

    def set_thumbnail(self, *, url: str):
        self.thumbnail = {"url": url}

    def set_footer(self, *, text: str, icon_url: str = None):
        self.footer = {"text": text}
        
        if icon_url:
            self.footer["icon_url"] = icon_url

    def set_author(self, *, name: str, icon_url: str = None):
        self.author = {"name": name}
        
        if icon_url:
            self.author["icon_url"] = icon_url

    def add_field(self, *, name: str, value: str, inline: bool = False):
        if not hasattr(self, "fields"):
            self.fields = []

        self.fields.append({
            "name": name,
            "value": value,
            "inline": inline
        })