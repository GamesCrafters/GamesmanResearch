from PrimitiveValues import PrimitiveValues

class Game:

    def do_move(self, p, m):
        raise NotImplementedError()

    def generate_moves(self, p):
        raise NotImplementedError()

    def primitive_value(self, p):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()

    def hash(self, p):
        raise NotImplementedError()
