from anytree import Node, RenderTree
import os
import keyboard
import sys
#custom import
sys.path.append('../')
import utils.console as console
import CUI.menuTree as tree

main = tree.Noda("main", lambda:
          print("This main func"))
third = tree.Noda("third", lambda:
                  print("Third"))
main.append(third)


main.childs[0].on_press()

class CUI(object):

    def __init__(self, mainMenuTitle = 'Main menu'):
        self.root = Node(mainMenuTitle)
        Node("Exit", parent = self.root)

    def test(self):
        print("test")

    def run(self):
        main.append("second", lambda:
                self.test())
        main.childs[1].on_press()

        while True:
            print(console.readChar())



test = CUI()
test.run()