

class Noda(object):
    childs = list()
    root = None
    def __init__(self, title, on_press):
        self.title = title
        self.on_press = on_press


    def append(self, *args):
        try:
            if len(args) == 1 and isinstance(args[0], Noda):
                args[0].root = self
                self.childs.append(args[0])
            if len(args) == 2 and isinstance(args[0], str):
                newNode = Noda(args[0], args[1])
                newNode.root = self
                self.childs.append(newNode)
        except Exception as err:
            print("Error! ", err)

    def root(self, rootRef):
        self.root = rootRef
