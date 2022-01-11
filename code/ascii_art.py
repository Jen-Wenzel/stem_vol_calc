from pyfiglet import Figlet

tree = r"""
         _-_
      /~~   ~~\
   /~~         ~~\
  {               }
   \  _-     -_  /
     ~  \\ //  ~
  _- -   | | _- _
    _ -  | |   -_
        // \\

""".split('\n')

def intro():
    fig = Figlet(font='big', width=118, justify='center')
    fig = fig.renderText('Stem volume calculator')

    for i in range(len(tree)):
        print(tree[i].ljust(100), tree[i])

    print(fig)

    for i in range(len(tree)):
        print(tree[i].ljust(100), tree[i])