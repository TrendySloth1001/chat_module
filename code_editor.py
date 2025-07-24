import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QAction, QTabWidget, QWidget, QVBoxLayout, QMessageBox, QInputDialog, QLineEdit, QToolBar, QSplitter, QTreeView, QFileSystemModel, QMenu)
from PyQt5.QtGui import QIcon
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciLexerCPP, QsciLexerJavaScript
from PyQt5.QtCore import Qt, QModelIndex
import jedi
from pygments.lexers import HtmlLexer, CssLexer, JavascriptLexer
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QToolTip

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
        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyCode - Python Code Editor')
        self.setGeometry(100, 100, 1200, 700)
        self.theme = 'light'
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
        self.setCentralWidget(splitter)
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

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*);;Python (*.py);;C++ (*.cpp *.h);;JavaScript (*.js)')
        if file_path:
            self.open_file_by_path(file_path)

    def open_file_by_path(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        ext = file_path.split('.')[-1]
        language = 'python' if ext == 'py' else 'cpp' if ext in ['cpp', 'h'] else 'js' if ext == 'js' else 'python'
        tab = EditorTab(file_path=file_path, language=language)
        tab.editor.setText(text)
        idx = self.tabs.addTab(tab, os.path.basename(file_path))
        self.tabs.setCurrentIndex(idx)
        self.apply_theme_to_tab(tab)

    def open_file_from_explorer(self, file_path):
        self.open_file_by_path(file_path)

    def open_project_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Open Project Directory', '')
        if dir_path:
            self.file_explorer.set_project_dir(dir_path)
            self.apply_theme()

    def save_file(self):
        tab = self.tabs.currentWidget()
        if tab.file_path:
            with open(tab.file_path, 'w', encoding='utf-8') as f:
                f.write(tab.editor.text())
            self.tabs.setTabText(self.tabs.currentIndex(), os.path.basename(tab.file_path))
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
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

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

    def apply_theme_to_tab(self, tab):
        if self.theme == 'dark':
            tab.editor.setCaretLineBackgroundColor(Qt.darkGray)
        else:
            tab.editor.setCaretLineBackgroundColor(Qt.lightGray)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()   