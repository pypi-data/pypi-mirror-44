"""Freesia - Allows rapid Qt development with extra features"""
import sys
try:
    if "freesia" in dir(sys) and sys.freesia.no_new: raise ImportError
    from PySide2 import QtGui, QtCore, QtWidgets, QtTest
    QtWidgets.__dict__.update(QtGui.__dict__)
    source = "PySide2"
    try:
        from PySide2.QtWebEngineWidgets import QWebEngineView
        web = True
    except ImportError:
        web = False
except ImportError: 
    try:
        if "freesia" in dir(sys) and sys.freesia.no_old: raise ImportError
        from PySide import QtGui, QtCore, QtTest
        QtWidgets = QtGui
        source = "PySide"
        web = False
    except ImportError: 
        raise ImportError("No working Qt bindings found")

import base64
import random
import ast
import sys
import re
import os

__author__ = "Luke Williams"
__version__ = "3.3.2"

try: main = QtWidgets.QApplication(sys.argv)
except RuntimeError: pass

allwidgets = []
fonttable = {}

Qt = QtCore.Qt
WindowOnTop = 2
WindowOnBottom = 0
ArrowCursor = Qt.ArrowCursor
BlankCursor = Qt.BlankCursor
BusyCursor = Qt.BusyCursor
CrossCursor = Qt.CrossCursor
WhatsThisCursor = Qt.WhatsThisCursor
WaitCursor = Qt.WaitCursor
HandCursor = Qt.PointingHandCursor
ForbiddenCursor = Qt.ForbiddenCursor
HorizontalCursor = Qt.SizeHorCursor
VerticalCursor = Qt.SizeVerCursor
SizeCursor = Qt.SizeAllCursor
ACTIVE = True
DISABLED = False
NORMAL = True
HORIZONTAL = Qt.Horizontal
VERTICAL = Qt.Vertical
fonttable = {}
CENTER = "center"
NW = "nw"
N = "n"
NE = "ne"
SW = "sw"
S = "s"
SE = "se"
W = "w"
E = "e"
START = 0
END = -1

css_table = {"bg":"background-color", 
             "fg":"color", 
             "selectionbg":"selection-background-color", 
             "selectionfg":"selection-color"}

widgets = {"Window":QtWidgets.QWidget, 
           "Label":QtWidgets.QLabel, 
           "Button":QtWidgets.QPushButton, 
           "Entry":QtWidgets.QLineEdit,
           "Frame":QtWidgets.QFrame,
           "Text":QtWidgets.QTextEdit,
           "Combobox":QtWidgets.QComboBox,
           "List":QtWidgets.QListWidget,
           "Image":QtWidgets.QLabel,
           "Radio":QtWidgets.QRadioButton,
           "Slider":QtWidgets.QSlider,
           "Checkbox":QtWidgets.QCheckBox,
           "Calendar":QtWidgets.QCalendarWidget,
           "Splitter":QtWidgets.QSplitter,
           "Spinbox":QtWidgets.QSpinBox,
           "Plaintext":QtWidgets.QPlainTextEdit,
           "Menu":QtWidgets.QMenuBar}

if web:
    widgets["Webkit"] = QWebEngineView

func_table = {"font":"font_decoder",
              "text":"setText",
              "title":"setWindowTitle",
              "mode":"set_password",
              "path":"set_image",
              "data":"set_base64_image",
              "state":"set_state",
              "orientation":"setOrientation",
              "cursor":"cursor",
              "borderless":"set_borderless",
              "layer":"set_layer",
              "width":"set_width",
              "height":"set_height",
              "icon":"set_icon",
              "center":"center_screen",
              "rounded":"set_rounded",
              }

def bind_scale(self, function):
    """When the parent resizes, the widgets call a function"""
    if self.parent() is not None:
        self.parent().bind("<Configure>", function)

def screenSize():
    """Returns the size of the monitor as a tuple"""
    geo = main.desktop().screenGeometry()
    return geo.width(), geo.height()

def centerWindow(window):
    """Calculate where the center of the screen is"""
    screen = screenSize()
    x_center = (screen[0] / 2) - window.width() / 2
    y_center = (screen[1] / 2) - window.height() / 2
    return round(x_center), round(y_center)
    
def import_font(file, name):
    """Import a font from a file"""
    font_id = QtGui.QFontDatabase.addApplicationFont(file)
    font_db = QtGui.QFontDatabase()
    font_styles = font_db.styles(name)
    font_families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
    if not font_families: return
    else: fonttable[name] = QtGui.QFont(font_families[0])

def after(ms, function):
    """Call a function after some time"""
    QtCore.QTimer.singleShot(ms, function)
    
def get_theme():
    """Generates a random colour scheme"""
    darkgrey = '#%02x%02x%02x' % tuple([random.randint(0, 110)] * 3)
    lightgrey = '#%02x%02x%02x' % tuple([random.randint(140, 255)] * 3)
    colour1 = '#%02x%02x%02x' % tuple([random.randint(0, 255), 
                                       random.randint(0, 255), 
                                       random.randint(0, 255)])
    colour2 = '#%02x%02x%02x' % tuple([random.randint(0, 255), 
                                       random.randint(0, 255), 
                                       random.randint(0, 255)])
    return (darkgrey, lightgrey, colour1, colour2)

def ErrorBox(parent, title, text, fg = "black", buttonfg = "black"):
    """show an error message"""
    message = QtWidgets.QMessageBox(parent)
    ss = "QLabel{color: " + fg + ";} QPushButton{color: " + buttonfg + ";}"
    message.setStyleSheet(ss)
    message.setIcon(QtWidgets.QMessageBox.Critical)
    message.setWindowTitle(title)
    message.setText(text)
    message.show()
    return message
    
def WarningBox(parent, title, text, fg = "black", buttonfg = "black"):
    """show an warning message"""
    message = QtWidgets.QMessageBox(parent)
    ss = "QLabel{color: " + fg + ";} QPushButton{color: " + buttonfg + ";}"
    message.setStyleSheet(ss)
    message.setIcon(QtWidgets.QMessageBox.Warning)
    message.setWindowTitle(title)
    message.setText(text)
    message.show()
    return message
    
def InfoBox(parent, title, text, fg = "black", buttonfg = "black"):
    """show an info message"""
    message = QtWidgets.QMessageBox(parent)
    ss = "QLabel{color: " + fg + ";} QPushButton{color: " + buttonfg + ";}"
    message.setStyleSheet(ss)
    message.setIcon(QtWidgets.QMessageBox.Information)
    message.setWindowTitle(title)
    message.setText(text)
    message.show()
    return message

def OpenFile(filetypes = []):
    """Show the open file dialog"""
    data = ";;".join([i.upper() + " (." + i + ")" for i in filetypes])
    return QtWidgets.QFileDialog.getOpenFileName(None, "Open", "", data)

def SaveFile(filetypes = []):
    """Show the save file dialog"""
    data = ";;".join([i.upper() + " (." + i + ")" for i in filetypes])
    return QtWidgets.QFileDialog.getSaveFileName(None, "Save As", "", data)

def InputBox(parent, title = "Box", text = "Value: ", password = False):
    """Shows a dialog that asks the user for some information"""
    if password:
        inputd = QtWidgets.QInputDialog()
        inputd = inputd.getText(parent, title, text, QtWidgets.QLineEdit.Password)
    else:
        inputd = QtWidgets.QInputDialog()
        inputd = inputd.getText(parent, title, text)
    return inputd
    
def FontBox():
    """Shows a dialog that allows the user to customize a font"""
    return QtWidgets.QFontDialog.getFont()

def apply_font(widget, font):
    """Apply the font chosen in the dialog to the widget"""
    if len(font) > 1: font = font[0]
    widget.setFont(font)

def ColorBox():
    """Shows a color picker dialog"""
    return str(QtWidgets.QColorDialog.getColor().name())

def mainloop():
    """render and run the program"""
    main.exec_()

keys = [i[4:] for i in dir(Qt) if i.startswith("Key_")]
vals = [dict(vars(Qt))["Key_" + i] for i in keys]
text2key = dict([[item, vals[keys.index(item)]] for item in keys])
key2text = dict([[vals[keys.index(item)], item] for item in keys])

qtevents = {"<Button-1>":"mousePressEvent;button;Qt.LeftButton",
            "<Button-2>":"mousePressEvent;button;Qt.MiddleButton",
            "<Button-3>":"mousePressEvent;button;Qt.RightButton",
            "<Double-Button-1>":"mouseDoubleClickEvent;button;Qt.LeftButton",
            "<Double-Button-2>":"mouseDoubleClickEvent;button;Qt.MiddleButton",
            "<Double-Button-3>":"mouseDoubleClickEvent;button;Qt.RightButton",
            "<Configure>":"resizeEvent",
            "<B1-Motion>":"mouseMoveEvent;buttons;Qt.LeftButton",
            "<B2-Motion>":"mouseMoveEvent;buttons;Qt.MiddleButton",
            "<B3-Motion>":"mouseMoveEvent;buttons;Qt.RightButton",
            "<Leave>":"leaveEvent",
            "<Enter>":"enterEvent",
            "<ButtonRelease-1>":"mouseReleaseEvent;button;Qt.LeftButton",
            "<ButtonRelease-2>":"mouseReleaseEvent;button;Qt.MiddleButton",
            "<ButtonRelease-3>":"mouseReleaseEvent;button;Qt.RightButton",
            "<FocusIn>":"focusInEvent",
            "<FocusOut>":"focusOutEvent",
            "<Close>":"closeEvent",
            "<Show>":"showEvent",
            "<Hide>":"hideEvent",
            "<Move>":"moveEvent",
            "<Minimize>":"changeEvent;windowState;Qt.WindowMinimized",
            "<Maximize>":"changeEvent;windowState;Qt.WindowMaximized",
            "<Restore>":"changeEvent;windowState;Qt.WindowNoState",
            "<TextChange>":"textChanged",
            }

class FreeScale(object):
    def __init__(self):
        if self.code == "Image":
            self.bind("<Configure>", self.box_image)
    def fix_cut_off(self, force=False):
        """Fix widgets from being cutoff when resized"""
        if ("text" in dir(self) and self.code in ["Label"]) or force:
            if "setAlignment" in dir(self) and self.code in ["Label"]:
                self.setAlignment(Qt.AlignCenter)
            pad = self.get_element(self.qt_code, "padding")
            if pad is None: 
                pad = "0"
            if pad.endswith("px"):
                pad = pad[:-2]
            pad = int(pad)*2
            if self.text() != "":
                calc = self.fontMetrics().boundingRect(self.text())
                self.set_width(calc.width()+pad+4)
                self.set_height(calc.height()+pad)
    def box_image(self):
        """Resize a image widgets image to the size of the label"""
        self.setPixmap(self.acimage.scaled(self.width(), self.height()))
    def auto_font(self):
        if "cfgsize" in dir(self) and self.autofont:
            expand = str(int(round(((self.parent().width()+self.parent().height())/2)*self.fontratio)))+"px"
            self.add_element(self.qt_code, "font-size", expand)
            self.config()
    def auto_font_calc(self):
        if "cfgsize" not in dir(self):
            size = self.get_element(self.qt_code, "font-size")
            if size is not None:
                if size.endswith("px"):
                    size = size[:-2]
                self.cfgsize = int(size)
                self.fontratio = self.cfgsize / ((self.parent().width()+self.parent().height())/2)    

class FreePlace(object):
    def __init__(self):
        self.placed = False
    def place(self, relx, rely, anchor="NW", place_toggles=[True, True], 
              width_offset=0, height_offset=0):
        window = self.parent()
        self.place_toggles = place_toggles
        self.sfx = relx
        self.sfy = rely
        self.ratio_w = self.width() / window.width()
        self.ratio_h = self.height()  /  window.height()
        anchor = anchor.upper()
        if anchor == "CENTER":
            def onresize(self):
                x, y = window.width() * self.sfx, window.height() * self.sfy
                self.move(x-self.width() / 2, y-self.height() / 2)
        elif anchor == "NW":
            def onresize(self):
                x, y = window.width() * self.sfx, window.height() * self.sfy
                self.move(x, y)
        elif anchor == "N":
            def onresize(self):
                x, y = window.width() * self.sfx, window.height() * self.sfy
                self.move(x-self.width() / 2, y)
        elif anchor == "NE":
            def onresize(self):
                x, y = window.width() * self.sfx, window.height() * self.sfy
                self.move(x-self.width(), y)
        elif anchor == "W":
            def onresize(self):
                x, y = window.width() * self.sfx, window.height() * self.sfy
                self.move(x, y-self.height() / 2)
        elif anchor == "SE":
            def onresize(self):
                x, y = window.width() * self.sfx, window.height() * self.sfy
                self.move(x-self.width(), y-self.height())
        elif anchor == "S":
            def onresize(self):
                x, y = window.width() * self.sfx, window.height() * self.sfy
                self.move(x-self.width() / 2, y-self.height())
        elif anchor == "SW":
            def onresize(self):
                x, y = window.width() * self.sfx, window.height() * self.sfy
                self.move(x, y-self.height())
        elif anchor == "E":
            def onresize(self):
                x, y = window.width() * self.sfx, window.height() * self.sfy
                self.move(x-self.width(), y-self.height() / 2)
        def aresize(self):
            if self.placed and self.place_toggles != [True, True]: return
            onresize(self)
        def fullres(self):
            aresize(self)
            if self.rescale[0]:
                self.set_width(window.width() * self.ratio_w + width_offset)
            if self.rescale[1]:
                self.set_height(window.height() * self.ratio_h + height_offset)
            self.fix_cut_off()
        self.befx = self.x()
        self.befy = self.y()
        self.bind("<Configure>", lambda: aresize(self))
        window.bind("<Configure>", lambda: fullres(self))
        window.bind("<Configure>", lambda: self.auto_font())
        window.resizeEvent(None)
        self.placed = True
        return self

class FreeBind(object):
    def __init__(self):
        pass
    def bind(self, code, func):
        """Bind an event to a function"""
        if code == "<TextChange>":
            self.textChanged.connect(func)
            return
        if code not in qtevents: 
            ncode = code[1:-1]
            ncode = ncode.split("-")
            encode = "keyPressEvent;key;" + ncode[-1] + ";"
            if "Meta" in ncode:
                encode += "Meta;mods;"
            if "Control" in ncode:
                encode += "Control;mods;"
            if "Alt" in ncode:
                encode += "Alt;mods;"
            if "Shift" in ncode:
                encode += "Shift;mods;"
            if encode.endswith(";"):
                encode = encode[:-1]
            qtevents[code] = encode
        decode = qtevents[code].split(";")
        exec("self.temp = self." + decode[0], locals())
        conds = [decode[1:][i:i + 2] for i in range(0, len(decode[1:]), 2)]
        if len(decode) >= 3:
            trun = lambda ev: self.event_handler(ev, func, code,
                                                cond = dict(conds))
        else:
            trun = lambda ev: self.event_handler(ev, func, code)
        if code in self.events.keys():
            self.events[code].append(lambda ev: trun(ev))
        else:
            self.events[code] = [self.temp, lambda ev: trun(ev)]
            runner = lambda ev: self.bat(self.events[code], ev)
            exec("self." + decode[0] + " = runner", locals())
    def event_handler(self, ev, func, code, cond = {}):
        """Execute a certain key when a condition is true"""
        out = []
        for k, v in cond.items():
            if v == "mods":
                exec("out.append(ev.modifiers() & Qt." + k + "Modifier)")
            else:
                try:
                    exec("out.append(ev." + k + "() == " + v + ")")
                except NameError:
                    exec("out.append(ev." + k + "() == text2key['" + v + "'])")
                except AttributeError:
                    exec("out.append(self." + k + "() == " + v + ")")
        if False not in out:
            func()
    def bat(self, funcs, event = None):
        """Runs functions in a list"""
        for i in funcs: i(event)

class FreeStyle(object):
    def __init__(self):
        self.store = {}
        self.create_stylesheet(self.qt_code)
    def to_dict(self, css):
        """Convert css to a python dictionary"""
        if css == "":
            return {}
        css = css[css.find("{"):]
        css = css[1:-1]
        if css.endswith(";"):
            css = css[:-1]
        for k, v in [(" ", ""), (":", "':'"), (";", "','")]:
            css = css.replace(k, v)
        return ast.literal_eval("{'" + css + "'}")           
    def to_css(self, css):
        """Convert python dictionary to css"""
        dic = str(css)
        for k, v in [("'", ""), (",", ";")]:
            dic = dic.replace(k, v)
        return dic
    def create_stylesheet(self, name):
        """Add a widget stylesheet to a widget"""
        self.store[name] = {}
        self.build()
    def get_stylesheet(self, name):
        """Get a widgets stylesheet"""
        return self.store[name]
    def add_element(self, to, k, v):
        """Add an entry to a stylesheet"""
        dic = self.get_stylesheet(to)
        dic[k] = v
        self.store[to] = dic
        self.build()
    def get_element(self, to, k):
        """Get the element of a stylesheet"""
        dic = self.get_stylesheet(to)
        if k in dic: 
            return dic[k]
        else:
            return None
    def build(self):
        """Construct and set a widgets stylesheet"""
        store = "\n".join([k + self.to_css(v) for k, v in self.store.items()])
        self.setStyleSheet(store)
    def set_borderless(self, value):
        """Remove the widnow borders"""
        if value:
            new = self.windowFlags() | Qt.FramelessWindowHint
            self.setWindowFlags(new)
    def set_layer(self, value):
        """Set the layer of the window over other windows"""
        if value == 0:
            new = self.windowFlags() | Qt.WindowStaysOnBottomHint
            self.setWindowFlags(new)
        if value == 1:
            return
        if value == 2:
            new = self.windowFlags() | Qt.WindowStaysOnTopHint
            self.setWindowFlags(new)
    def center_screen(self, value):
        """Move the window to the center of the screen"""
        if value: 
            x, y = centerWindow(self)
            self.move(x, y)
    def set_password(self, password = "password"):
        """Set the entry and text widgets to hide its contents"""
        if password == "password":
            self.setEchoMode(self.Password)
    def font_decoder(self, code):
        """Convert a tkinter font code into Qt"""
        code = code.split()
        font = QtGui.QFont()
        self.setFont(font)
        out = {}
        if len(code) >= 1:
            if code[0] in fonttable.keys():
                font = fonttable[code[0]]
            else:
                out["font-family"] = code[0]
        if len(code) >= 2:
            if code[1].endswith("px"): code[1] = code[1][:-2]
            code[1] = str(int(int(code[1]) * 1.43))
            out["font-size"] = code[1] + "px"
        if len(code) >= 3:
            if "bold" in code[2:]:
                font.setBold(True)
            if "italic" in code[2:]:
                font.setItalic(True)
            if "underline" in code[2:]:
                font.setUnderline(True)
            else:
                font.setUnderline(False)
        self.setFont(font)
        for k, v in out.items():
            self.add_element(self.qt_code, k, v) 
    def set_image(self, path):
        """Set the image of the widget from a file"""
        pixmap = QtGui.QPixmap(path)
        self.acimage = pixmap
        #self.resize(pixmap.width(), pixmap.height())
        self.setPixmap(pixmap.scaled(self.width(), self.height()))    
    def set_base64_image(self, data):
        """Set the image of the widget from base64"""
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(base64.b64decode(data))
        self.acimage = pixmap
        #self.resize(pixmap.width(), pixmap.height())
        self.setPixmap(pixmap.scaled(self.width(), self.height()))
    def set_state(self, state):
        """Set an entry or text widget to be read only"""
        self.setReadOnly(not state)
    def set_width(self, width):
        """Set the width of a widget"""
        self.resize(width, self.height())
        if self.code not in ["Window"]:
            self.init_w = self.parent().width()
            self.init_h = self.parent().height()
            self.init_w_sf = self.width() / self.init_w
            self.init_h_sf = self.height() / self.init_h        
    def set_height(self, height):
        """Set the width of a widget"""
        self.resize(self.width(), height)
        if self.code not in ["Window"]:
            self.init_w = self.parent().width()
            self.init_h = self.parent().height()
            self.init_w_sf = self.width() / self.init_w
            self.init_h_sf = self.height() / self.init_h        
    def set_icon(self, path):
        """Set the widgets icon"""
        self.setWindowIcon(QtGui.QPixmap(path))

for name, widget in widgets.items():
    class FreeWidget(widget, FreeStyle, FreeBind, FreePlace, FreeScale):
        def __init__(self, parent=None, **args):
            global allwidgets
            args.setdefault("rescale", [True, True])
            args.setdefault("autofont", True)
            self.autofont = args.pop("autofont")
            self.rescale = args.pop("rescale")
            self.events = {}
            self.menustruct = {}
            self.actionstruct = {}
            exec("super(" + self.code + ", self).__init__(parent)")
            FreeStyle.__init__(self)
            FreePlace.__init__(self)
            FreeBind.__init__(self)
            FreeScale.__init__(self)
            self.config(**args)
            self.auto_font_calc()
            self.show()
            allwidgets.append(self)
        def config(self, **args):
            """Style the widget"""
            if "font" in args.keys() and "cfgsize" in dir(self):
                del self.cfgsize
            if self.code == "Window" and "bg" in args.keys():
                self.background = Frame(self, bg=args.pop("bg"), 
                                        width=self.width(), 
                                        height=self.height())
                self.background.place(0, 0, anchor=NW)
            elif self.code == "Frame" and "bg" in args.keys():
                if "old" not in dir(self.parent()):
                    self.old = True
                    self.background = Frame(self, bg=args.pop("bg"), 
                                            width=self.width(), 
                                            height=self.height())
                    self.background.place(0, 0, anchor=NW)
            for k, v in args.items():
                if k in css_table:
                    self.add_element(self.qt_code, css_table[k], v)
                elif k in func_table:
                    exec("self." + func_table[k] + "(v)")
                else:
                    self.add_element(self.qt_code, k, v)
            self.auto_font_calc()
            self.fix_cut_off()
        def geometry(self, width=None, height=None, x=None, y=None):
            if width is not None:
                self.set_width(width)
            if height is not None:
                self.set_height(height)
            if x is not None:
                self.setGeometry(x, self.y(), self.width(), self.height())
            if y is not None:
                self.setGeometry(self.x(), y, self.width(), self.height())
        def cursor(self, cursor):
            """Set the cursor over a widget"""
            self.setCursor(cursor)        
        def set(self, text):
            """Set the text of a widget"""
            if self.code == "Slider":
                self.setValue(text)
            else:
                self.config(text = text)
        def get(self, index = 0):
            """Get the text of a widget"""
            if self.code == "Text":
                return self.toPlainText()
            elif "text" in dir(self):
                return self.text()
            elif self.code == "Slider":
                return self.value()
            else:
                return self.contents()[index]
        def insert(self, index, text):
            """Insert text at a certain index"""
            self.insertItem(index, text)
        def delete(self, index):
            """Delete an item at a position in the list"""
            if self.code == "Combobox": 
                self.removeItem(index)
            elif self.code == "List": 
                item = self.takeItem(index)
                del item
        def deleteitem(self, text):
            """Delete an item from its contents"""
            self.delete(self.contents().index(text))
        def contents(self):
            """Get the contents of the listwidget"""
            if self.code == "Combobox": 
                return [self.itemText(i) for i in range(self.count())]
            else: 
                return [i.text() for i in self.findItems("", Qt.MatchContains)]
        def selected(self):
            """See what is selected"""
            try: 
                return self.currentText()
            except AttributeError: 
                try: 
                    return self.selectedItems()[0].text()
                except AttributeError:
                    try: 
                        return self.selectedText()
                    except AttributeError: 
                        return None
                except IndexError:
                    return None
        def checked(self):
            """Check if the widget is selected"""
            return self.isChecked()
        def check(self, state = True):
            """Select or deselect a widget"""
            if state: self.setChecked(True)
            else: self.setChecked(False)
        def range(self, low, high):
            """Set the range that a widget's value can be"""
            self.setMinimum(low)
            self.setMaximum(high)
        def date(self):
            """Get the date from the calendar widget"""
            return self.selectedDate().toString()
        def load(self, html):
            """Load up HTML into the widget"""
            self.setHtml(html)
        def fade_out(self, duration=1000):
            """Fade in"""
            self.effect = QtWidgets.QGraphicsOpacityEffect()
            self.setGraphicsEffect(self.effect)
            self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
            self.animation.setDuration(duration)
            self.animation.setStartValue(1)
            self.animation.setEndValue(0)
            self.animation.start()
        def fade_in(self, duration=1000):
            """Fade in"""
            self.effect = QtWidgets.QGraphicsOpacityEffect()
            self.setGraphicsEffect(self.effect)
            self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
            self.animation.setDuration(duration)
            self.animation.setStartValue(0)
            self.animation.setEndValue(1)
            self.animation.start()
        def goto(self, url):
            """Go to a url in a Webkit widget"""
            if self.qt_code == "Webkit":
                self.setUrl(QtCore.QUrl(url))
        def add(self, widget):
            """Add a widget to another widget"""
            if self.code == "Menu":
                self.menustruct[widget] = self.addMenu(widget)
                self.actionstruct[widget] = []
            else:
                self.addWidget(widget)
        def set_rounded(self, radius):
            """Set rounded edges on a widget"""
            def apply_round():
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(self.rect()), radius, radius)
                mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
                self.setMask(mask)
            self.bind("<Configure>", apply_round)
            apply_round()
        def gen_action(self, menu, name, trigger = None, shortcut = None):
            """Generate an action"""
            act = QtWidgets.QAction(name)
            if shortcut is not None:
                act.setShortcut(shortcut)
            if trigger is not None:
                act.triggered.connect(trigger)
            return act
        def action(self, menu, name, trigger = None, shortcut = None):
            """Add a new action"""
            exec("act = self.gen_action(menu, '" + name + "', \
trigger = trigger, shortcut = shortcut)", 
                 locals(), globals())
            exec("self.menustruct[menu].addAction(act)", locals(), globals())
            self.actionstruct[menu].append(act)        
    FreeWidget.code = name
    FreeWidget.qt_code = widget.__name__
    exec(name + " = FreeWidget")
