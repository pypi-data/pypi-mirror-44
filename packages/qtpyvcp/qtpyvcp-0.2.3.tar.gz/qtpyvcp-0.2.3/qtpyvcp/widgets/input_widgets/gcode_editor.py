#    Gcode display / edit widget for QT_VCP
#    Copyright 2016 Chris Morley
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# This was based on
# QScintilla sample with PyQt
# Eli Bendersky (eliben@gmail.com)
# Which is code in the public domain
#
# See also:
# http://pyqt.sourceforge.net/Docs/QScintilla2/index.html
# https://qscintilla.com/

import sys
import os

from qtpy.QtCore import Property, QObject
from qtpy.QtGui import QFont, QFontMetrics, QColor

from qtpyvcp.utilities import logger

LOG = logger.getLogger(__name__)

try:
    from PyQt5.Qsci import QsciScintilla, QsciLexerCustom
except ImportError as e:
    LOG.critical("Can't import QsciScintilla - is package python-pyqt5.qsci installed?", exc_info=e)
    sys.exit(1)

from qtpyvcp.plugins import getPlugin
STATUS = getPlugin('status')

from qtpyvcp.core import Info
INFO = Info()


# ==============================================================================
# Simple custom lexer for Gcode
# ==============================================================================
class GcodeLexer(QsciLexerCustom):
    def __init__(self, parent=None, standalone=False):
        super(GcodeLexer, self).__init__(parent)

        # This prevents doing unneeded initialization
        # when QtDesginer loads the plugin.
        if parent is None and not standalone:
            return

        self._styles = {
            0: 'Default',
            1: 'Comment',
            2: 'Key',
            3: 'Assignment',
            4: 'Value',
        }
        for key, value in self._styles.iteritems():
            setattr(self, value, key)
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        font.setBold(True)
        self.setFont(font, 2)

    # Paper sets the background color of each style of text
    def setPaperBackground(self, color, style=None):
        if style is None:
            for i in range(0, 5):
                self.setPaper(color, i)
        else:
            self.setPaper(color, style)

    def description(self, style):
        return self._styles.get(style, '')

    def defaultColor(self, style):
        if style == self.Default:
            return QColor('#000000')  # black
        elif style == self.Comment:
            return QColor('#000000')  # black
        elif style == self.Key:
            return QColor('#0000CC')  # blue
        elif style == self.Assignment:
            return QColor('#CC0000')  # red
        elif style == self.Value:
            return QColor('#00CC00')  # green
        return QsciLexerCustom.defaultColor(self, style)

    def styleText(self, start, end):
        editor = self.editor()
        if editor is None:
            return

        # scintilla works with encoded bytes, not decoded characters.
        # this matters if the source contains non-ascii characters and
        # a multi-byte encoding is used (e.g. utf-8)
        source = ''
        if end > editor.length():
            end = editor.length()
        if end > start:
            if sys.hexversion >= 0x02060000:
                # faster when styling big files, but needs python 2.6
                source = bytearray(end - start)
                editor.SendScintilla(
                    editor.SCI_GETTEXTRANGE, start, end, source)
            else:
                source = unicode(editor.text()).encode('utf-8')[start:end]
        if not source:
            return

        # the line index will also be needed to implement folding
        index = editor.SendScintilla(editor.SCI_LINEFROMPOSITION, start)
        if index > 0:
            # the previous state may be needed for multi-line styling
            pos = editor.SendScintilla(
                editor.SCI_GETLINEENDPOSITION, index - 1)
            state = editor.SendScintilla(editor.SCI_GETSTYLEAT, pos)
        else:
            state = self.Default

        set_style = self.setStyling
        self.startStyling(start, 0x1f)

        # scintilla always asks to style whole lines
        for line in source.splitlines(True):
            # print line
            length = len(line)
            graymode = False
            msg = ('msg' in line.lower() or 'debug' in line.lower())
            for char in str(line):
                # print char
                if char == '(':
                    graymode = True
                    set_style(1, self.Comment)
                    continue
                elif char == ')':
                    graymode = False
                    set_style(1, self.Comment)
                    continue
                elif graymode:
                    if msg and char.lower() in ('m', 's', 'g', ',', 'd', 'e', 'b', 'u'):
                        set_style(1, self.Assignment)
                        if char == ',': msg = False
                    else:
                        set_style(1, self.Comment)
                    continue
                elif char in ('%', '<', '>', '#', '='):
                    state = self.Assignment
                elif char in ('[', ']'):
                    state = self.Value
                elif char.isalpha():
                    state = self.Key
                elif char.isdigit():
                    state = self.Default
                else:
                    state = self.Default
                set_style(1, state)

            # folding implementation goes here
            index += 1


# ==============================================================================
# Base editor class
# ==============================================================================
class EditorBase(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super(EditorBase, self).__init__(parent)
        # linuxcnc defaults
        self.idle_line_reset = False
        # don't allow editing by default
        self.setReadOnly(True)
        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("0000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))

        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)
        # setting marker margin width to zero make the marker highlight line
        self.setMarginWidth(1, 10)
        self.marginClicked.connect(self.on_margin_clicked)
        self.markerDefine(QsciScintilla.RightArrow,
                          self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#ffe4e4"),
                                      self.ARROW_MARKER_NUM)

        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))

        # Set custom gcode lexer
        self.lexer = GcodeLexer(self)
        self.lexer.setDefaultFont(font)
        self.setLexer(self.lexer)

        # default gray background
        self.set_background_color('#C0C0C0')

        # not too small
        # self.setMinimumSize(200, 100)

    # must set lexer paper background color _and_ editor background color it seems
    def set_background_color(self, color):
        self.SendScintilla(QsciScintilla.SCI_STYLESETBACK, QsciScintilla.STYLE_DEFAULT, QColor(color))
        self.lexer.setPaperBackground(QColor(color))

    def set_margin_background_color(self, color):
        self.setMarginsBackgroundColor(QColor(color))

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)


# ==============================================================================
# Gcode widget
# ==============================================================================
class GcodeEditor(EditorBase, QObject):
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super(GcodeEditor, self).__init__(parent)

        self._last_filename = None
        self.auto_show_mdi = True
        self.last_line = None
        # self.setEolVisibility(True)

        STATUS.file.notify(self.load_program)
        STATUS.motion_line.onValueChanged(self.highlight_line)
        # STATUS.connect('line-changed', self.highlight_line)
        # if self.idle_line_reset:
        #     STATUS.connect('interp_idle', lambda w: self.set_line_number(None, 0))

        # QSS Hack

        self._backgroundcolor = ''
        self.backgroundcolor = self._backgroundcolor

        self._marginbackgroundcolor = ''
        self.marginbackgroundcolor = self._marginbackgroundcolor

    @Property(str)
    def backgroundcolor(self):
        """Property to set the background color of the GCodeEditor (str).

        sets the background color of the GCodeEditor
        """
        return self._backgroundcolor

    @backgroundcolor.setter
    def backgroundcolor(self, color):
        self._backgroundcolor = color
        self.set_background_color(color)

    @Property(str)
    def marginbackgroundcolor(self):
        """Property to set the background color of the GCodeEditor margin (str).

        sets the background color of the GCodeEditor margin
        """
        return self._marginbackgroundcolor

    @marginbackgroundcolor.setter
    def marginbackgroundcolor(self, color):
        self._marginbackgroundcolor = color
        self.set_margin_background_color(color)

    def load_program(self, fname=None):
        if fname is None:
            fname = self._last_filename
        else:
            self._last_filename = fname
        self.load_text(fname)
        # self.zoomTo(6)
        self.setCursorPosition(0, 0)

    # when switching from MDI to AUTO we need to reload the
    # last (linuxcnc loaded) program.
    def reload_last(self):
        self.load_text(STATUS.old['file'])
        self.setCursorPosition(0, 0)

    # With the auto_show__mdi option, MDI history is shown
    def load_mdi(self):
        self.load_text(INFO.MDI_HISTORY_PATH)
        self._last_filename = INFO.MDI_HISTORY_PATH
        # print 'font point size', self.font().pointSize()
        # self.zoomTo(10)
        # print 'font point size', self.font().pointSize()
        self.setCursorPosition(self.lines(), 0)

    # With the auto_show__mdi option, MDI history is shown
    def load_manual(self):
        if STATUS.is_man_mode():
            self.load_text(INFO.MACHINE_LOG_HISTORY_PATH)
            self.setCursorPosition(self.lines(), 0)

    def load_text(self, fname):
        try:
            fp = os.path.expanduser(fname)
            self.setText(open(fp).read())
        except:
            LOG.error('File path is not valid: {}'.format(fname))
            self.setText('')
            return

        self.last_line = None
        self.ensureCursorVisible()
        self.SendScintilla(QsciScintilla.SCI_VERTICALCENTRECARET)

    def highlight_line(self, line):
        # if STATUS.is_auto_running():
        #     if not STATUS.old['file'] == self._last_filename:
        #         LOG.debug('should reload the display')
        #         self.load_text(STATUS.old['file'])
        #         self._last_filename = STATUS.old['file']
        self.markerAdd(line, self.ARROW_MARKER_NUM)
        if self.last_line:
            self.markerDelete(self.last_line, self.ARROW_MARKER_NUM)
        self.setCursorPosition(line, 0)
        self.ensureCursorVisible()
        self.SendScintilla(QsciScintilla.SCI_VERTICALCENTRECARET)
        self.last_line = line

    def set_line_number(self, line):
        pass

    def line_changed(self, line, index):
        # LOG.debug('Line changed: {}'.format(STATUS.is_auto_mode()))
        self.line_text = str(self.text(line)).strip()
        self.line = line
        if STATUS.is_mdi_mode() and STATUS.is_auto_running() is False:
            STATUS.emit('mdi-line-selected', self.line_text, self._last_filename)

    def select_lineup(self):
        line, col = self.getCursorPosition()
        LOG.debug(line)
        self.setCursorPosition(line - 1, 0)
        self.highlight_line(line - 1)

    def select_linedown(self):
        line, col = self.getCursorPosition()
        LOG.debug(line)
        self.setCursorPosition(line + 1, 0)
        self.highlight_line(line + 1)

    # designer recognized getter/setters
    # auto_show_mdi status
    def set_auto_show_mdi(self, data):
        self.auto_show_mdi = data

    def get_auto_show_mdi(self):
        return self.auto_show_mdi

    def reset_auto_show_mdi(self):
        self.auto_show_mdi = True

    auto_show_mdi_status = Property(bool, get_auto_show_mdi, set_auto_show_mdi, reset_auto_show_mdi)


# ==============================================================================
# For testing
# ==============================================================================
if __name__ == "__main__":
    from PyQt4.QtGui import QApplication

    app = QApplication(sys.argv)
    editor = GcodeEditor(standalone=True)
    editor.show()

    editor.setText(open(sys.argv[0]).read())
    app.exec_()
