class Command(Exception):
    def __init__(self, command: dict):
        self.command = command

class CommandNotFound(Exception):
    pass

class NoArgument(Command):
    def __init__(self, description, command: dict, needed_args, needed_arg):
        super().__init__(command)
        self.description = description
        self.needed_args = needed_args
        self.needed_arg = needed_arg

class InvalidArgumentType(Command):
    def __init__(self, description, command: dict, needed_args, needed_arg):
        super().__init__(command)
        self.description = description
        self.needed_args = needed_args
        self.needed_arg = needed_arg

class InvalidPseudoFunction(Exception):
    pass

class InvalidPseudoFunctionArgumentType(Exception):
    pass

class User(Exception):
    pass

class InvalidUser(User):
    pass

class Member(Exception):
    pass

class InvalidMember(Member):
    pass

class NoPermission(Member):
    def __init__(self, description, permission):
        self.description = description
        self.permission = permission

class Bot(Exception):
    pass

class Forbidden(Bot):
    pass

class Database(Exception):
    pass

class NotFound(Database):
    pass

class UnexpectedError(Exception):
    pass