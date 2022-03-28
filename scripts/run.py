import os
import sys

sys.path.append(os.getcwd())

if __name__ == '__main__':
    from core import main

    main.MainRunner().run()
