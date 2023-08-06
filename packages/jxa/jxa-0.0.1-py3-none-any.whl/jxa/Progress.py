import time
import math


def time_sec():
    return int(time.time())


class Progress:
    def __init__(self, frequency) -> None:
        """

        :param frequency: display frequency in seconds
        """
        self.last_progress = time_sec()
        self.frequency = frequency

    @staticmethod
    def human_readable_byte_count(bytes, si: bool = False):
        unit = 1000 if si else 1024
        if bytes < unit:
            return f"{bytes} B"

        exp = int(math.log(bytes) // math.log(unit))
        pre = ("kMGTPE" if si else "KMGTPE")[exp - 1]
        pre += ("" if si else "i")
        return "{:.1f} {}B".format(bytes / math.pow(unit, exp), pre)

    def print(self, sofar, total,
              line_prefix="Downloaded",
              final=False):
        if self.frequency != 0 and not final:
            next_progress_time = self.last_progress + self.frequency
            if time_sec() < next_progress_time:
                return
            else:
                self.last_progress = time_sec()

        print("{} {} ({:.0f}%)".format(
            line_prefix,
            Progress.human_readable_byte_count(sofar),
            sofar / total * 100))

    def print_final(self, *args, **kwargs):
        kwargs['final'] = True
        self.print(*args, **kwargs)
