import os

from datetime import datetime

from PySide6.QtGui     import QTextCursor
from PySide6.QtCore    import QObject, Signal, Slot
from PySide6.QtWidgets import QTextEdit

class LogStream(QObject):
    written = Signal(tuple)
    def info(self, text):
        self.written.emit(('INFO',  text))
    def warn(self, text):
        self.written.emit(('WARN',  text))
    def error(self, text):
        self.written.emit(('ERROR', text))
    def debug(self, text):
        self.written.emit(('DEBUG', text))


class Logger(QTextEdit):
    isDebug: bool
    fname: str
    def __init__(self, isDebug: bool, outdir='./output/', **kwargs):
        QTextEdit.__init__(self, **kwargs)
        self.setReadOnly(True)
        self.isDebug = isDebug
        d = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        os.makedirs(outdir, exist_ok=True)
        self.fname = outdir+'log '+d+'.log'
        # Install the custom output stream
        # self.out = LogStream()
        # self.out.written.connect(self.written)

    @Slot(tuple)
    def written(self, arg):
        mode, text = arg
        if mode == 'DEBUG':
            if not self.isDebug:
                return
            color = '#000000'
        elif mode == 'ERROR':
            color = '#ff0000'
        elif mode == 'WARN':
            color = '#663399'
        else:
            color = '#00f131'
        tim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f'{tim} - {mode: <5} - {text}'
        esc = f'{mode: <5}'.replace(" ", "&nbsp;")
        html = f'<code style="font-size:16px;">{tim} - </code>'
        html += f'<code style="font-size:16px;color:{color};">{esc}</code>'
        html += f'<code style="font-size:16px;"> - {text}</code><br>'
        self.moveCursor(QTextCursor.End)
        self.insertHtml(html)
        self.moveCursor(QTextCursor.End)
        self.ensureCursorVisible()

        with open(self.fname, "a", encoding="utf-8") as f:
            f.write(msg+"\n")

        if self.isDebug:
            print(msg)
