"""Helper functions."""

import threading
import time
import time as t

update = "Sun Sep  9 22:08:04 2018"
name = "Leo Heller"


# filename = os.path.basename(main.__file__)


def setupdate():
    """Change the last update date."""
    global update
    update = t.ctime()


def head():
    """Print header."""
    print("=" * 32)
    print("|{:^30}|".format(name))
    print("|{:^30}|".format(filename))
    print("|{:^30}|".format(update))
    print("=" * 32, end="\n\n")


def read(filename):
    """Read the contents of the file and returns them.

    Arguments:
        filename {string} -- filename of the file that should be read

    Returns:
        string -- contents of the file

    """
    with open(filename, "r") as f:
        return f.read()


def write(filename, content):
    """Write the {content} to {filename}. Erases all content in the file before writing. If file does not exist it is created.

    Arguments:
        filename {string} -- filename of the file that should be written to
        content {string} -- text that should be written to the file
    """
    with open(filename, "w") as f:
        print(str(content), file=f)


class DoEvery(threading.Thread):
    def __init__(self, period, f):
        super().__init__()
        self.period = period
        self.f = f
        self.daemon = True
        self._stop = False

    def stop(self):
        self._stop = True

    def g_tick(self):
        t = time.time()
        count = 0
        while True:
            count += 1
            yield max(t + count * self.period - time.time(), 0)

    def run(self):
        g = self.g_tick()
        while not self._stop:
            time.sleep(next(g))
            self.f()
