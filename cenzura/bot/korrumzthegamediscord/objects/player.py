class Player:
    def __init__(self, username: str, x: int, y: int, pullRequests: int, imageNumber: int):
        self.username = username
        self.x = x
        self.y = y
        self.pull_requests = pullRequests
        self.image_number = imageNumber

    def __eq__(self, player: dict):
        return "username" in player and self.username == player["username"]