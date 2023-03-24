from typing import Callable, Union

from PySide6.QtCore import QTimer

import const

class Runner:
    def __init__(
        self, parent,
        start: Callable[[], None],
        stop: Callable[[], None],
        updateRow: Callable[[int], tuple[bool, str, float, int]],
        sendText: Callable[[str], None]
    ):
        self._start = start
        self._stop = stop
        self.parent = parent
        self.updateRow = updateRow
        self.sendText = sendText

        self.i = 0

        self.timer: Union[QTimer, None] = None

    def reset(self):
        self.i = 0
        if self.timer is not None:
            self.timer.stop()
        self.timer = None
        self._stop()

    def begin(self):
        self._start()
        self.update()

    def update(self):
        valid, res, flo, msec = self.updateRow(self.i)
        if not valid:
            self.reset()
            return

        self.i += 1

        text = _getText(res, flo)
        self.sendText(text)

        if self.timer is not None:
            self.timer.stop()
        self.timer = QTimer(self.parent)
        self.timer.setInterval(msec)
        self.timer.timeout.connect(self.update)
        self.timer.start()

def _getText(reservoir: str, flowRate: float):
    return f',{const.RESERVOIR_INDEX[reservoir]},{flowRate:.3f}'

