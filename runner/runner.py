from typing import Callable, Union

from PySide6.QtCore import QTimer

import const

class Runner:
    current_res = const.RESERVOIR_NAMES[0]
    current_flo = 0.0
    current_msec = 0
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
        self.current_res = const.RESERVOIR_NAMES[0]
        self.current_flo = 0.0
        self.current_msec = 0
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

        self.current_res = res
        self.current_flo = flo
        self.current_msec = msec

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

