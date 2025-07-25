import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QAction, QTabWidget, QWidget, QVBoxLayout, QMessageBox, QInputDialog, QLineEdit, QToolBar, QSplitter, QTreeView, QFileSystemModel, QMenu, QStackedWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QStatusBar)
from PyQt5.QtGui import QIcon
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciLexerCPP, QsciLexerJavaScript
from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal
import jedi
from pygments.lexers import HtmlLexer, CssLexer, JavascriptLexer
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QToolTip
import uuid
import threading
import websocket
import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QApplication
from PyQt5.QtGui import QClipboard

class CodeEditor(QsciScintilla):
    def __init__(self, parent=None, language='python'):
        super().__init__(parent)
        self.setUtf8(True)
        self.setMarginsFont(self.font())
        self.setMarginWidth(0, '00000')
        self.setMarginLineNumbers(0, True)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setAutoIndent(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(Qt.lightGray)
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        self.setLexerByLanguage(language)
        self.language = language
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionThreshold(1)
        self.setCallTipsStyle(QsciScintilla.CallTipsContext)
        self.setCallTipsVisible(3)
        self.setMouseTracking(True)
        self.last_hover_pos = None
        self.hover_timer = QTimer(self)
        self.hover_timer.setSingleShot(True)
        self.hover_timer.timeout.connect(self.show_hover_tooltip)
        self.cursorPositionChanged.connect(self.cancel_hover)

    def setLexerByLanguage(self, language):
        self.language = language
        if language == 'python':
            lexer = QsciLexerPython()
        elif language == 'cpp':
            lexer = QsciLexerCPP()
        elif language == 'js':
            lexer = QsciLexerJavaScript()
        else:
            lexer = QsciLexerPython()
        self.setLexer(lexer)
        self.setup_autocompletion_keywords(language)

    def setup_autocompletion_keywords(self, language):
        if language == 'python':
            self.setAutoCompletionSource(QsciScintilla.AcsAll)
            self.setAutoCompletionThreshold(1)
        elif language == 'html':
            html_keywords = [
                'html', 'head', 'body', 'div', 'span', 'a', 'img', 'ul', 'li', 'table', 'tr', 'td', 'th', 'form', 'input', 'button', 'script', 'style', 'link', 'meta', 'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'hr', 'label', 'select', 'option', 'textarea', 'iframe', 'nav', 'footer', 'header', 'section', 'article', 'main', 'aside', 'canvas', 'svg', 'video', 'audio', 'source', 'track', 'embed', 'object', 'param', 'blockquote', 'cite', 'code', 'pre', 'small', 'strong', 'em', 'b', 'i', 'u', 's', 'sub', 'sup', 'mark', 'del', 'ins', 'details', 'summary', 'figure', 'figcaption', 'fieldset', 'legend', 'datalist', 'output', 'progress', 'meter', 'template', 'noscript', 'area', 'map', 'col', 'colgroup', 'caption', 'tbody', 'thead', 'tfoot', 'address', 'abbr', 'acronym', 'applet', 'base', 'basefont', 'bdo', 'big', 'center', 'dir', 'font', 'frame', 'frameset', 'noframes', 'strike', 'tt'
            ]
            self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
            self.api = QsciScintilla.APIs(self.lexer())
            for kw in html_keywords:
                self.api.add(kw)
            self.api.prepare()
        elif language == 'css':
            css_keywords = [
                'color', 'background', 'background-color', 'width', 'height', 'margin', 'padding', 'border', 'font', 'font-size', 'font-family', 'display', 'position', 'top', 'left', 'right', 'bottom', 'float', 'clear', 'z-index', 'overflow', 'visibility', 'opacity', 'content', 'align-items', 'justify-content', 'flex', 'grid', 'gap', 'row-gap', 'column-gap', 'box-shadow', 'text-shadow', 'text-align', 'vertical-align', 'line-height', 'letter-spacing', 'word-spacing', 'white-space', 'list-style', 'cursor', 'pointer', 'transition', 'animation', 'transform', 'border-radius', 'box-sizing', 'min-width', 'max-width', 'min-height', 'max-height', 'outline', 'clip', 'filter', 'resize', 'user-select', 'object-fit', 'object-position', 'background-image', 'background-repeat', 'background-size', 'background-position', 'background-clip', 'background-origin', 'border-collapse', 'border-spacing', 'caption-side', 'empty-cells', 'table-layout', 'direction', 'unicode-bidi', 'writing-mode', 'quotes', 'counter-reset', 'counter-increment', 'content', 'page-break-before', 'page-break-after', 'page-break-inside', 'orphans', 'widows', 'columns', 'column-count', 'column-gap', 'column-rule', 'column-span', 'column-width', 'break-before', 'break-after', 'break-inside', 'will-change', 'caret-color', 'scroll-behavior', 'scroll-snap-type', 'scroll-snap-align', 'scroll-snap-stop', 'scrollbar-color', 'scrollbar-width', 'tab-size', 'text-decoration', 'text-overflow', 'text-transform', 'word-break', 'word-wrap', 'writing-mode', 'zoom'
            ]
            self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
            self.api = QsciScintilla.APIs(self.lexer())
            for kw in css_keywords:
                self.api.add(kw)
            self.api.prepare()
        elif language == 'js':
            js_keywords = [
                'break', 'case', 'catch', 'class', 'const', 'continue', 'debugger', 'default', 'delete', 'do', 'else', 'export', 'extends', 'finally', 'for', 'function', 'if', 'import', 'in', 'instanceof', 'let', 'new', 'return', 'super', 'switch', 'this', 'throw', 'try', 'typeof', 'var', 'void', 'while', 'with', 'yield', 'async', 'await', 'constructor', 'get', 'set', 'static', 'of', 'from', 'as', 'null', 'true', 'false', 'undefined', 'NaN', 'Infinity', 'arguments', 'eval', 'isFinite', 'isNaN', 'parseFloat', 'parseInt', 'decodeURI', 'decodeURIComponent', 'encodeURI', 'encodeURIComponent', 'escape', 'unescape', 'Object', 'Function', 'Boolean', 'Symbol', 'Error', 'EvalError', 'InternalError', 'RangeError', 'ReferenceError', 'SyntaxError', 'TypeError', 'URIError', 'Number', 'Math', 'Date', 'String', 'RegExp', 'Array', 'Int8Array', 'Uint8Array', 'Uint8ClampedArray', 'Int16Array', 'Uint16Array', 'Int32Array', 'Uint32Array', 'Float32Array', 'Float64Array', 'Map', 'Set', 'WeakMap', 'WeakSet', 'ArrayBuffer', 'SharedArrayBuffer', 'Atomics', 'DataView', 'JSON', 'Promise', 'Generator', 'GeneratorFunction', 'Reflect', 'Proxy', 'Intl', 'WebAssembly', 'window', 'document', 'console', 'alert', 'prompt', 'confirm', 'fetch', 'XMLHttpRequest', 'setTimeout', 'setInterval', 'clearTimeout', 'clearInterval', 'requestAnimationFrame', 'cancelAnimationFrame', 'addEventListener', 'removeEventListener', 'dispatchEvent', 'localStorage', 'sessionStorage', 'location', 'history', 'navigator', 'screen', 'frames', 'self', 'parent', 'top', 'opener', 'event', 'Image', 'Audio', 'File', 'FileReader', 'Blob', 'URL', 'Worker', 'postMessage', 'onmessage', 'close', 'open', 'print', 'stop', 'focus', 'blur', 'scroll', 'scrollTo', 'scrollBy', 'moveTo', 'moveBy', 'resizeTo', 'resizeBy', 'getComputedStyle', 'matchMedia', 'querySelector', 'querySelectorAll', 'getElementById', 'getElementsByClassName', 'getElementsByTagName', 'createElement', 'createTextNode', 'appendChild', 'removeChild', 'replaceChild', 'insertBefore', 'cloneNode', 'hasChildNodes', 'contains', 'compareDocumentPosition', 'getAttribute', 'setAttribute', 'removeAttribute', 'hasAttribute', 'attributes', 'style', 'classList', 'className', 'id', 'innerHTML', 'outerHTML', 'textContent', 'value', 'checked', 'selected', 'disabled', 'readonly', 'required', 'type', 'name', 'form', 'action', 'method', 'enctype', 'target', 'submit', 'reset', 'elements', 'length', 'options', 'selectedIndex', 'selectedOptions', 'files', 'accept', 'multiple', 'size', 'maxLength', 'minLength', 'pattern', 'placeholder', 'step', 'min', 'max', 'autocomplete', 'autofocus', 'spellcheck', 'tabIndex', 'accessKey', 'draggable', 'hidden', 'contentEditable', 'contextMenu', 'dir', 'lang', 'title', 'translate', 'dataset', 'dropzone', 'itemScope', 'itemType', 'itemId', 'itemRef', 'itemProp', 'itemValue', 'role', 'aria-*', 'data-*'
            ]
            self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
            self.api = QsciScintilla.APIs(self.lexer())
            for kw in js_keywords:
                self.api.add(kw)
            self.api.prepare()
        else:
            self.setAutoCompletionSource(QsciScintilla.AcsNone)

    def keyPressEvent(self, event):
        if self.language == 'python' and event.text() and event.text().isidentifier():
            # Trigger Jedi completion on dot or after typing
            QTimer.singleShot(0, self.show_python_completions)
        super().keyPressEvent(event)

    def show_python_completions(self):
        # Get current line and column
        line, index = self.getCursorPosition()
        text = self.text()
        script = jedi.Script(text, path='')
        try:
            completions = script.complete(line+1, index)
            if completions:
                self.clearAutoCompletionWordSeparators()
                self.autoCompleteFromAPIs()
                self.api = QsciScintilla.APIs(self.lexer())
                for c in completions:
                    self.api.add(c.name)
                self.api.prepare()
        except Exception:
            pass

    def mouseMoveEvent(self, event):
        self.last_hover_pos = event.pos()
        self.hover_timer.start(400)  # 400ms delay before showing tooltip
        super().mouseMoveEvent(event)

    def cancel_hover(self):
        self.hover_timer.stop()

    def show_hover_tooltip(self):
        if not self.last_hover_pos:
            return
        pos = self.last_hover_pos
        # Use SCI_CHARPOSITIONFROMPOINT to get char position
        x, y = pos.x(), pos.y()
        char_pos = self.SendScintilla(QsciScintilla.SCI_CHARPOSITIONFROMPOINT, x, y)
        if char_pos < 0:
            return
        line = self.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, char_pos)
        index = char_pos - self.SendScintilla(QsciScintilla.SCI_POSITIONFROMLINE, line)
        word = self.wordAtPoint(pos)
        if not word:
            return
        if self.language == 'python':
            text = self.text()
            import jedi
            script = jedi.Script(text, path='')
            try:
                definitions = script.help(line+1, index)
                if definitions:
                    doc = definitions[0].docstring()
                    if doc:
                        from PyQt5.QtWidgets import QToolTip
                        QToolTip.showText(self.mapToGlobal(pos), doc, self)
            except Exception:
                pass
        elif self.language == 'html':
            html_docs = {'div': 'Defines a division or section.', 'span': 'Defines a section in a document.', 'a': 'Defines a hyperlink.'}
            if word in html_docs:
                from PyQt5.QtWidgets import QToolTip
                QToolTip.showText(self.mapToGlobal(pos), html_docs[word], self)
        elif self.language == 'css':
            css_docs = {'color': 'Sets the color of text.', 'background': 'Sets all background style properties at once.'}
            if word in css_docs:
                from PyQt5.QtWidgets import QToolTip
                QToolTip.showText(self.mapToGlobal(pos), css_docs[word], self)
        elif self.language == 'js':
            js_docs = {'function': 'Defines a function.', 'var': 'Declares a variable.'}
            if word in js_docs:
                from PyQt5.QtWidgets import QToolTip
                QToolTip.showText(self.mapToGlobal(pos), js_docs[word], self)

class EditorTab(QWidget):
    def __init__(self, file_path=None, language='python'):
        super().__init__()
        self.file_path = file_path
        self.language = language
        self.editor = CodeEditor(language=language)
        self.modified = False
        self.editor.textChanged.connect(self.on_text_changed)
        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def on_text_changed(self):
        self.modified = True

    def set_saved(self):
        self.modified = False

class FileExplorer(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QFileSystemModel()
        self.model.setReadOnly(False)
        self.setModel(self.model)
        self.setRootIndex(self.model.index(os.path.expanduser('~')))
        self.setMinimumWidth(250)
        self.setMaximumWidth(500)
        self.setHeaderHidden(True)
        self.file_open_callback = None
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)
        self.doubleClicked.connect(self.on_double_click)
        self.project_dir = None
        # Only show files and folders, not system files
        self.model.setNameFilters(['*.py', '*.cpp', '*.h', '*.js', '*.json', '*.txt', '*.md', '*.html', '*.css', '*'])
        self.model.setNameFilterDisables(False)

    def set_project_dir(self, path):
        self.project_dir = path
        self.model.setRootPath(path)
        self.setRootIndex(self.model.index(path))

    def on_double_click(self, index: QModelIndex):
        if self.model.isDir(index):
            return
        file_path = self.model.filePath(index)
        if self.file_open_callback:
            self.file_open_callback(file_path)

    def set_file_open_callback(self, callback):
        self.file_open_callback = callback

    def open_context_menu(self, position):
        index = self.indexAt(position)
        menu = QMenu()
        # Add context menu actions as buttons
        new_file_action = menu.addAction('New File')
        new_folder_action = menu.addAction('New Folder')
        rename_action = menu.addAction('Rename')
        delete_action = menu.addAction('Delete')
        # Connect actions
        new_file_action.triggered.connect(lambda: self.create_new_file(index))
        new_folder_action.triggered.connect(lambda: self.create_new_folder(index))
        rename_action.triggered.connect(lambda: self.rename_item(index))
        delete_action.triggered.connect(lambda: self.delete_item(index))
        menu.exec_(self.viewport().mapToGlobal(position))

    def create_new_file(self, index):
        dir_path = self.model.filePath(index)
        if not os.path.isdir(dir_path):
            dir_path = os.path.dirname(dir_path)
        name, ok = QInputDialog.getText(self, 'New File', 'Enter file name:')
        if ok and name:
            file_path = os.path.join(dir_path, name)
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('')

    def create_new_folder(self, index):
        dir_path = self.model.filePath(index)
        if not os.path.isdir(dir_path):
            dir_path = os.path.dirname(dir_path)
        name, ok = QInputDialog.getText(self, 'New Folder', 'Enter folder name:')
        if ok and name:
            folder_path = os.path.join(dir_path, name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    def rename_item(self, index):
        old_path = self.model.filePath(index)
        if not old_path:
            return
        name, ok = QInputDialog.getText(self, 'Rename', 'Enter new name:', QLineEdit.Normal, os.path.basename(old_path))
        if ok and name:
            new_path = os.path.join(os.path.dirname(old_path), name)
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)

    def delete_item(self, index):
        path = self.model.filePath(index)
        if not path:
            return
        if os.path.isdir(path):
            try:
                os.rmdir(path)
            except OSError:
                QMessageBox.warning(self, 'Delete', 'Folder is not empty or cannot be deleted.')
        else:
            os.remove(path)

    def apply_theme(self, theme):
        if theme == 'dark':
            self.setStyleSheet('QTreeView { background: #232629; color: #f8f8f2; selection-background-color: #444; } QMenu { background: #232629; color: #f8f8f2; } QPushButton { background: #444; color: #f8f8f2; }')
        else:
            self.setStyleSheet('')

class HomePage(QWidget):
    def __init__(self, open_project_callback, new_file_callback, open_recent_callback, theme='light', create_session_callback=None, join_session_callback=None):
        super().__init__()
        self.open_project_callback = open_project_callback
        self.new_file_callback = new_file_callback
        self.open_recent_callback = open_recent_callback
        self.create_session_callback = create_session_callback
        self.join_session_callback = join_session_callback
        self.theme = theme
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel('DevHub Editor')
        title.setStyleSheet('font-size: 36px; font-weight: bold; margin-bottom: 30px;')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        btn_open_project = QPushButton('Open Project')
        btn_open_project.setFixedHeight(40)
        btn_open_project.clicked.connect(self.open_project_callback)
        layout.addWidget(btn_open_project)

        btn_new_file = QPushButton('New File')
        btn_new_file.setFixedHeight(40)
        btn_new_file.clicked.connect(self.new_file_callback)
        layout.addWidget(btn_new_file)

        btn_create_session = QPushButton('Create Session')
        btn_create_session.setFixedHeight(40)
        btn_create_session.clicked.connect(self.create_session_callback)
        layout.addWidget(btn_create_session)

        btn_join_session = QPushButton('Join Session')
        btn_join_session.setFixedHeight(40)
        btn_join_session.clicked.connect(self.join_session_callback)
        layout.addWidget(btn_join_session)

        layout.addSpacing(20)
        recent_label = QLabel('Recent Files/Projects')
        recent_label.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout.addWidget(recent_label)
        self.recent_list = QListWidget()
        self.recent_list.setFixedHeight(120)
        self.recent_list.itemDoubleClicked.connect(self.open_recent_callback)
        layout.addWidget(self.recent_list)
        layout.addStretch()
        self.setLayout(layout)
        self.apply_theme(self.theme)

    def set_recent(self, recent_items):
        self.recent_list.clear()
        for item in recent_items:
            self.recent_list.addItem(item)

    def apply_theme(self, theme):
        self.theme = theme
        if theme == 'dark':
            self.setStyleSheet('QWidget { background: #232629; color: #f8f8f2; } QPushButton { background: #444; color: #f8f8f2; border-radius: 6px; } QPushButton:hover { background: #555; } QListWidget { background: #232629; color: #f8f8f2; } QLabel { color: #f8f8f2; }')
        else:
            self.setStyleSheet('')

class SessionCreatedDialog(QDialog):
    def __init__(self, session_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Session Created')
        layout = QVBoxLayout()
        label = QLabel('Share this session link to collaborate:')
        layout.addWidget(label)
        hbox = QHBoxLayout()
        self.link_label = QLabel(session_id)
        hbox.addWidget(self.link_label)
        copy_btn = QPushButton('Copy')
        copy_btn.clicked.connect(self.copy_link)
        hbox.addWidget(copy_btn)
        layout.addLayout(hbox)
        ok_btn = QPushButton('OK')
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)
        self.setLayout(layout)

    def copy_link(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.link_label.text())

class MainWindow(QMainWindow):
    collab_update_signal = pyqtSignal(str, str)  # file_path, content
    collab_open_file_signal = pyqtSignal(str, str)  # file_path, content
    collab_presence_signal = pyqtSignal(list)  # user list

    def __init__(self):
        super().__init__()
        self.setWindowTitle('DevHub - Python Code Editor')
        self.setGeometry(100, 100, 1200, 700)
        self.theme = 'light'
        self.recent_files = []
        self.stacked = QStackedWidget()
        self.home_page = HomePage(self.open_project_from_home, self.new_file_from_home, self.open_recent_from_home, self.theme, self.create_session, self.join_session)
        self.stacked.addWidget(self.home_page)
        self.editor_widget = QWidget()
        self.init_editor_ui()
        self.stacked.addWidget(self.editor_widget)
        self.setCentralWidget(self.stacked)
        self.show_home()
        self.session_id = None
        self.collab_update_signal.connect(self.apply_collab_update)
        self.collab_open_file_signal.connect(self.apply_collab_open_file)
        self.collab_presence_signal.connect(self.update_presence)
        self.open_files = {}  # file_path: tab index
        self.user_id = None
        self.users_in_session = []
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def show_home(self):
        self.home_page.set_recent(self.recent_files)
        self.stacked.setCurrentWidget(self.home_page)
        self.apply_theme()

    def show_editor(self):
        self.stacked.setCurrentWidget(self.editor_widget)
        self.apply_theme()

    def open_project_from_home(self):
        self.show_editor()
        self.open_project_dir()

    def new_file_from_home(self):
        self.show_editor()
        self.new_tab()

    def open_recent_from_home(self, item):
        path = item.text()
        self.show_editor()
        if os.path.isdir(path):
            self.file_explorer.set_project_dir(path)
        else:
            self.open_file_by_path(path)

    def add_recent(self, path):
        if path not in self.recent_files:
            self.recent_files.insert(0, path)
            self.recent_files = self.recent_files[:10]

    def init_editor_ui(self):
        self.file_explorer = FileExplorer()
        self.file_explorer.set_file_open_callback(self.open_file_from_explorer)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        splitter = QSplitter()
        splitter.addWidget(self.tabs)
        splitter.addWidget(self.file_explorer)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 1)
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.editor_widget.setLayout(layout)
        self.create_menu()
        self.create_toolbar()
        self.new_tab()
        self.apply_theme()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        open_action = QAction('Open File', self)
        open_action.triggered.connect(self.open_file)
        open_dir_action = QAction('Open Project Directory', self)
        open_dir_action.triggered.connect(self.open_project_dir)
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_file)
        saveas_action = QAction('Save As', self)
        saveas_action.triggered.connect(self.save_file_as)
        new_action = QAction('New', self)
        new_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(open_dir_action)
        file_menu.addAction(save_action)
        file_menu.addAction(saveas_action)
        file_menu.addSeparator()
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu('Edit')
        find_action = QAction('Find', self)
        find_action.triggered.connect(self.find_text)
        edit_menu.addAction(find_action)

        view_menu = menubar.addMenu('View')
        theme_action = QAction('Toggle Theme', self)
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)

    def create_toolbar(self):
        toolbar = QToolBar('Main Toolbar')
        self.addToolBar(toolbar)
        new_btn = QAction(QIcon(), 'New', self)
        new_btn.triggered.connect(self.new_tab)
        open_btn = QAction(QIcon(), 'Open File', self)
        open_btn.triggered.connect(self.open_file)
        open_dir_btn = QAction(QIcon(), 'Open Project Directory', self)
        open_dir_btn.triggered.connect(self.open_project_dir)
        save_btn = QAction(QIcon(), 'Save', self)
        save_btn.triggered.connect(self.save_file)
        find_btn = QAction(QIcon(), 'Find', self)
        find_btn.triggered.connect(self.find_text)
        theme_btn = QAction(QIcon(), 'Theme', self)
        theme_btn.triggered.connect(self.toggle_theme)
        toolbar.addAction(new_btn)
        toolbar.addAction(open_btn)
        toolbar.addAction(open_dir_btn)
        toolbar.addAction(save_btn)
        toolbar.addAction(find_btn)
        toolbar.addAction(theme_btn)

    def new_tab(self):
        tab = EditorTab()
        idx = self.tabs.addTab(tab, 'Untitled')
        self.tabs.setCurrentIndex(idx)
        self.apply_theme_to_tab(tab)
        tab.editor.textChanged.connect(self.on_editor_text_changed_collab)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*);;Python (*.py);;C++ (*.cpp *.h);;JavaScript (*.js)')
        if file_path:
            self.open_file_by_path(file_path)

    def open_file_by_path(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        language = self.detect_language(file_path)
        tab = EditorTab(file_path=file_path, language=language)
        tab.editor.setText(text)
        idx = self.tabs.addTab(tab, os.path.basename(file_path))
        self.tabs.setCurrentIndex(idx)
        self.apply_theme_to_tab(tab)
        self.add_recent(file_path)
        self.open_files[file_path] = idx
        tab.editor.textChanged.connect(self.on_editor_text_changed_collab)
        # If in collab session, broadcast file open
        if hasattr(self, 'collab_ws') and self.collab_ws and self.collab_ws.sock and self.collab_ws.sock.connected:
            msg = json.dumps({'type': 'open_file', 'file_path': file_path, 'content': text, 'session_id': self.session_id})
            try:
                self.collab_ws.send(msg)
            except Exception:
                pass

    def open_file_from_explorer(self, file_path):
        self.open_file_by_path(file_path)

    def open_project_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Open Project Directory', '')
        if dir_path:
            self.file_explorer.set_project_dir(dir_path)
            self.apply_theme()
            self.add_recent(dir_path)

    def save_file(self):
        tab = self.tabs.currentWidget()
        if tab.file_path:
            with open(tab.file_path, 'w', encoding='utf-8') as f:
                f.write(tab.editor.text())
            self.tabs.setTabText(self.tabs.currentIndex(), os.path.basename(tab.file_path))
            if hasattr(tab, 'set_saved'):
                tab.set_saved()
        else:
            self.save_file_as()

    def save_file_as(self):
        tab = self.tabs.currentWidget()
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save File As', '', 'All Files (*);;Python (*.py);;C++ (*.cpp *.h);;JavaScript (*.js)')
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(tab.editor.text())
            tab.file_path = file_path
            ext = file_path.split('.')[-1]
            tab.language = 'python' if ext == 'py' else 'cpp' if ext in ['cpp', 'h'] else 'js' if ext == 'js' else 'python'
            tab.editor.setLexerByLanguage(tab.language)
            self.tabs.setTabText(self.tabs.currentIndex(), os.path.basename(file_path))

    def close_tab(self, index):
        tab = self.tabs.widget(index)
        if tab and getattr(tab, 'modified', False):
            reply = QMessageBox.question(self, 'Unsaved Changes', 'This file has unsaved changes. Save before closing?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.tabs.setCurrentIndex(index)
                self.save_file()
                tab.set_saved()
            elif reply == QMessageBox.Cancel:
                return
        self.tabs.removeTab(index)
        if self.tabs.count() == 0:
            self.show_home()

    def find_text(self):
        tab = self.tabs.currentWidget()
        if not tab:
            return
        text, ok = QInputDialog.getText(self, 'Find', 'Enter text to find:', QLineEdit.Normal)
        if ok and text:
            editor = tab.editor
            pos = editor.findFirst(text, False, False, False, True)
            if not pos:
                QMessageBox.information(self, 'Find', f'"{text}" not found.')

    def toggle_theme(self):
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.apply_theme()

    def apply_theme(self):
        if self.theme == 'dark':
            self.setStyleSheet('QMainWindow { background: #232629; color: #f8f8f2; } QTabWidget::pane { border: 1px solid #444; } QTabBar::tab { background: #444; color: #f8f8f2; } QTabBar::tab:selected { background: #232629; } QToolBar { background: #232629; color: #f8f8f2; }')
        else:
            self.setStyleSheet('')
        for i in range(self.tabs.count()):
            self.apply_theme_to_tab(self.tabs.widget(i))
        self.file_explorer.apply_theme(self.theme)
        self.home_page.apply_theme(self.theme)

    def apply_theme_to_tab(self, tab):
        if self.theme == 'dark':
            tab.editor.setCaretLineBackgroundColor(Qt.darkGray)
        else:
            tab.editor.setCaretLineBackgroundColor(Qt.lightGray)

    def closeEvent(self, event):
        # Check all tabs for unsaved changes
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if tab and getattr(tab, 'modified', False):
                self.tabs.setCurrentIndex(i)
                reply = QMessageBox.question(self, 'Unsaved Changes', 'One or more files have unsaved changes. Save before exiting?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.save_file()
                    tab.set_saved()
                elif reply == QMessageBox.Cancel:
                    event.ignore()
                    return
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def start_collab_client(self):
        self.collab_ws = websocket.WebSocketApp(
            'ws://localhost:8765',
            on_open=self.on_collab_open,
            on_message=self.on_collab_message,
            on_close=self.on_collab_close,
            on_error=self.on_collab_error
        )
        self.collab_thread = threading.Thread(target=self.collab_ws.run_forever, daemon=True)
        self.collab_thread.start()
        self._collab_ignore_next = False
        self.connect_editor_signal()
        self.tabs.currentChanged.connect(self.connect_editor_signal)

    def create_session(self):
        session_id = str(uuid.uuid4())
        self.session_id = session_id
        dlg = SessionCreatedDialog(session_id, self)
        dlg.exec_()
        self.show_editor()
        self.start_collab_client()

    def join_session(self):
        session_id, ok = QInputDialog.getText(self, 'Join Session', 'Enter session link:')
        if ok and session_id:
            self.session_id = session_id
            self.show_editor()
            self.start_collab_client()



    def on_collab_open(self, ws):
        join_msg = json.dumps({'type': 'join', 'session_id': self.session_id})
        ws.send(join_msg)

    def on_collab_message(self, ws, message):
        data = json.loads(message)
        if data.get('type') == 'edit':
            file_path = data.get('file_path')
            content = data.get('content')
            self.collab_update_signal.emit(file_path, content)
        elif data.get('type') == 'open_file':
            file_path = data.get('file_path')
            content = data.get('content')
            self.collab_open_file_signal.emit(file_path, content)
        elif data.get('type') == 'presence':
            users = data.get('users', [])
            self.collab_presence_signal.emit(users)

    def on_collab_close(self, ws, *args):
        pass

    def on_collab_error(self, ws, error):
        print('Collab error:', error)

    def apply_collab_update(self, file_path, content):
        # Only update if this file is open and current
        idx = self.open_files.get(file_path)
        if idx is not None and self.tabs.currentIndex() == idx:
            editor = self.tabs.widget(idx).editor
            if editor.text() != content:
                cursor = editor.getCursorPosition()
                self._collab_ignore_next = True
                editor.setText(content)
                editor.setCursorPosition(*cursor)

    def apply_collab_open_file(self, file_path, content):
        # If file is already open, switch to it; else open new tab
        idx = self.open_files.get(file_path)
        if idx is not None:
            self.tabs.setCurrentIndex(idx)
        else:
            tab = EditorTab(file_path=file_path, language=self.detect_language(file_path))
            tab.editor.setText(content)
            idx = self.tabs.addTab(tab, os.path.basename(file_path))
            self.tabs.setCurrentIndex(idx)
            self.open_files[file_path] = idx
            self.apply_theme_to_tab(tab)
        # Connect editor signal for this tab
        self.tabs.widget(idx).editor.textChanged.connect(self.on_editor_text_changed_collab)

    def detect_language(self, file_path):
        ext = file_path.split('.')[-1]
        return 'python' if ext == 'py' else 'cpp' if ext in ['cpp', 'h'] else 'js' if ext == 'js' else 'python'

    def on_editor_text_changed_collab(self):
        if getattr(self, '_collab_ignore_next', False):
            self._collab_ignore_next = False
            return
        if hasattr(self, 'collab_ws') and self.collab_ws and self.collab_ws.sock and self.collab_ws.sock.connected:
            tab = self.tabs.currentWidget()
            if tab and hasattr(tab, 'file_path'):
                content = tab.editor.text()
                msg = json.dumps({'type': 'edit', 'file_path': tab.file_path, 'content': content, 'session_id': self.session_id})
                try:
                    self.collab_ws.send(msg)
                except Exception:
                    pass

    def update_presence(self, users):
        self.users_in_session = users
        self.status_bar.showMessage(f'Users in session: {len(users)} | IDs: {", ".join(users)}')

    def connect_editor_signal(self):
        try:
            self.tabs.currentWidget().editor.textChanged.disconnect(self.on_editor_text_changed_collab)
        except Exception:
            pass
        try:
            self.tabs.currentWidget().editor.textChanged.connect(self.on_editor_text_changed_collab)
        except Exception:
            pass

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()   