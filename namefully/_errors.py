__all__ = ['NameError']


class NameError(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.name = self.__class__.__name__
        self.message = message

    def __str__(self):
        return f'{self.name}: {self.message}'

    def __repr__(self):
        return f'<{self.name}>'
