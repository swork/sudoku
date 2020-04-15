#! /usr/bin/env python3

import logging, sys
from . import main

logger = logging.getLogger(__name__ if not __name__ == '__main__' else os.path.basename(__file__))

if __name__ == '__main__':
    logging.basicConfig()
    sys.exit(main())
