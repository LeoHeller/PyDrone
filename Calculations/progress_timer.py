"""Custom implementation for the progress timer class."""

import progressbar as pb


class progress_timer():
    """Custom prgress timer class."""

    def __init__(self, n_iter, description="Something"):
        """Init with args.

        Arguments:
            n_iter {int} -- steps in progress bar

        Keyword Arguments:
            description {str} -- description for progress bar (default: {"Something"})
        """
        self.n_iter = n_iter
        self.iter = 0
        self.description = description + ': '
        self.timer = None
        self.initialize()

    def initialize(self):
        """Initialize timer."""
        widgets = [self.description, pb.Percentage(), ' ',
                   pb.Bar(marker="="), ' ', pb.ETA()]
        self.timer = pb.ProgressBar(
            widgets=widgets, maxval=self.n_iter).start()

    def update(self, q=1):
        """Update timer."""
        self.timer.update(self.iter)
        self.iter += q

    def finish(self):
        """Finishes the pb."""
        self.timer.finish()
