from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *
from editor import Editor
from file_manager import FileManager
from fuzzy_searcher import SearchItem, SearchWorker
from TextLexer import QsciLexerText
import resources

import config,sys,os
from pathlib import Path
import jedi
import git
#from git import Repo
from github import Github 
import inspect

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.app_name = "QCodeEditor"

        self.current_file = None
        self.current_side_bar = None
        self.process = None
        self.timer = QTime()
        
        self.envs = list(jedi.find_virtualenvs())
        self.init_ui()


    @property
    def current_file(self) -> Path:
        return self._current_file

    @current_file.setter
    def current_file(self, file: Path):
        self._current_file: Path = file

    def init_ui(self):
        self.setWindowTitle(self.app_name)
        self.resize(1300, 900)

        # set stye sheet file
        self.setStyleSheet(open("./src/styles/style.qss", "r").read())
        self.window_font = QFont("FiraCode", 12)
        self.setFont(self.window_font)

        self.set_up_menu()

        self.setUpBody()

        self.set_up_status_bar()

        self.show()

    def get_editor(self, path: Path = None, is_python_file=True) -> QsciScintilla:
        """Create a New Editor"""
        venv = None
        if len(self.envs) > 0:
            venv = self.envs[0]
        editor = Editor(path=path, env=venv, python_file=is_python_file)

        return editor
    
    #def initLexers(self):
    #    # Dict that maps lexer actions to their respective strings
    #    self.lexActs = {}
    #    langGrp = QActionGroup(self.lang)
    #    langGrp.setExclusive(True)
    #    self.lang.addAction(self.noLexAct)
    #    self.noLexAct.setCheckable(True)
        #self.noLexAct.setChecked(True)
    #    self.noLexAct.setActionGroup(langGrp)
    #    self.lang.addSeparator()
    #    languages = sorted(config.LEXERS.keys())
    #    for i in languages:
    #        langAct = self.lang.addAction(i)
    #        langAct.setCheckable(True)
    #        langAct.setActionGroup(langGrp)
    #        self.lexActs[langAct] = i
    #    langGrp.triggered.connect(lambda lex: self.getEditor(self.tabNum+1).setLang(self.lexActs.get(lex)))
    
    
    #def guessLexer(self):
        #try:
        #    x = config.docList[self.tab.currentIndex()+1]
        #    n, e = os.path.basename(x).lower().split(".")
        #    if e == "sh" or e == "bsh":
        #        self.getEditor(self.tabNum).setLang("Bash")
        #    elif e == "cmd" or e == "bat" or e == "btm" or e == "nt":
        #        self.getEditor(self.tabNum).setLang("Batch")
        #    elif e == "cmake" or e == "cmakelists":
        #        self.getEditor(self.tabNum).setLang("CMake")
        #    elif e == "cpp" or e == "cxx" or e == "cc" or e == "c" or e == "h"\
        #    or e == "hh" or e == "hpp":
        #        self.getEditor(self.tabNum).setLang("C++")
        #    elif e == "cs":
        #        self.getEditor(self.tabNum).setLang("C#")
        #    elif e == "css":
        #        self.getEditor(self.tabNum).setLang("CSS")
        #    elif e == "d":
        #        self.getEditor(self.tabNum).setLang("D")
        #    elif e == "diff" or e == "patch":
        #        self.getEditor(self.tabNum).setLang("Diff")
        #    elif e == "f90" or e == "f95" or e == "f2k" or e == "f03" or e == "f15":
        #        self.getEditor(self.tabNum).setLang("Fortran")
        #    elif e == "f" or e == "for":
        #        self.getEditor(self.tabNum).setLang("Fortran77")
        #    elif e == "html" or e == "htm":
        #        self.getEditor(self.tabNum).setLang("HTML")
        #    elif e == "java":
        #        self.getEditor(self.tabNum).setLang("Java")
        #    elif e == "js":
        #        self.getEditor(self.tabNum).setLang("JavaScript")
        #    elif e == "lua":
        #        self.getEditor(self.tabNum).setLang("Lua")
        #    elif e == "mak" or n == "gnumakefile" or n == "makefile":
        #        self.getEditor(self.tabNum).setLang("Makefile")
        #    elif e == "m":
        #        self.getEditor(self.tabNum).setLang("MATLAB")
        #    elif e == "pas" or e == "inc":
        #        self.getEditor(self.tabNum).setLang("Pascal")
        #    elif e == "ps":
        #        self.getEditor(self.tabNum).setLang("PostScript")
        #    elif e == "pov" or e == "tga":
        #        self.getEditor(self.tabNum).setLang("POV-Ray")
        #    elif e == "py" or e == "pyw":
        #        self.getEditor(self.tabNum).setLang("Python")
        #        #print "p"
        #    elif e == "rb" or e == "rbw":
        #        self.getEditor(self.tabNum).setLang("Ruby")
        #    elif e == "cir":
        #        self.getEditor(self.tabNum).setLang("Spice")
        #    elif e == "sql":
        #        self.getEditor(self.tabNum).setLang("SQL")
        #    elif e == "tcl":
        #        self.getEditor(self.tabNum).setLang("TCL")
        #    elif e == "tex":
        #        self.getEditor(self.tabNum).setLang("TeX")
        #    elif e == "v" or e == "sv" or e == "vh" or e == "svh":
        #        self.getEditor(self.tabNum).setLang("Verilog")
        #    elif e == "vhd" or e == "vhdl":
        #        self.getEditor(self.tabNum).setLang("VHDL")
        #    elif e == "xml" or e == "xsl" or e == "xsml" or e == "xsd" or \
        #    e == "kml" or e == "wsdl" or e == "xlf" or e == "xliff":
        #        self.getEditor(self.tabNum).setLang("XML")
        #    elif e == "yml":
        #        self.getEditor(self.tabNum).setLang("YML")
        #except (ValueError, IndexError):
        #        self.lexer = QsciLexerText()
        #        self.lexer.setDefaultFont(config.font)
        #        self.lexer.setDefaultColor(QColor("Black"))
        #        self.getEditor(self.tabNum).setLexer(self.lexer)
        #        self.noLexAct.setChecked(True)

    #def readSettings(self):
    #    # The default fonts represented as a toString() list
    #    DEFAULT_FONT = str(config.font.family())+",12,-1,5,50,0,0,0,0,0"
    #    settings = QSettings()
    #    if config.font.fromString(settings.value("Editor/font",
    #                                            QVariant(DEFAULT_FONT),type=str)):
    #        #config.lexer.setDefaultColor(QColor("Black"))
    #        config.lexer.setFont(config.font)
            
    def chooseFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            config.font = font
            try:
                self.getEditor(self.tab.currentIndex()).lexer().setFont(config.font)
            except AttributeError:
                self.getEditor(self.tab.currentIndex()).setLang(QsciLexerText())
                #print self.getEditor(self.tab.currentIndex()).lexer()
                self.getEditor(self.tab.currentIndex()).lexer().setFont(config.font)

    def set_cursor_pointer(self, e: QEnterEvent) -> None:
        self.setCursor(Qt.PointingHandCursor)

    def set_cursor_arrow(self, e) -> None:
        self.setCursor(Qt.ArrowCursor)

    def get_sidebar_button(self, img_path: str, widget) -> QLabel:
        label = QLabel()
        label.setPixmap(QPixmap(img_path).scaled(QSize(32, 32)))
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setFont(self.window_font)
        label.mousePressEvent = lambda e: self.show_hide_tab(e, widget)
        label.setMouseTracking(True)
        label.enterEvent = self.set_cursor_pointer
        label.leaveEvent = self.set_cursor_arrow
        return label

    def get_frame(self) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.NoFrame)
        frame.setFrameShadow(QFrame.Plain)
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setStyleSheet(
        """
            QFrame {
                background-color: #21252b;
                border-radius: 5px;
                border: none;
                padding: 5px;
                color: #D3D3D3;
            }

            QFrame::hover {
                color: white;
            }
        """
        )

        return frame

    def create_label(self, text, style_sheet, alignment, font="Consolas", font_size=15, min_height=200):
        lbl = QLabel(text)
        lbl.setAlignment(alignment)
        lbl.setFont(QFont(font, font_size))
        lbl.setStyleSheet(style_sheet)
        lbl.setContentsMargins(0, 0, 0, 0)
        lbl.setMaximumHeight(min_height)
        return lbl


    def setUpBody(self):
        ###############################################
        ################ BODY ####################
        body_frame = QFrame()
        body_frame.setFrameShape(QFrame.NoFrame)
        body_frame.setFrameShadow(QFrame.Plain)
        body_frame.setLineWidth(0)
        body_frame.setMidLineWidth(0)
        body_frame.setContentsMargins(0, 0, 0, 0)
        body_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body_frame.setLayout(body)
        
        
        # console_bar
        
        self.console_bar = QFrame()
        #self.resize(200,40)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.console_bar.sizePolicy().hasHeightForWidth())
        #self.console_bar.setSizePolicy(sizePolicy)
        self.console_bar.setFrameShape(QFrame.StyledPanel)
        self.console_bar.setContentsMargins(0,0,0,0)
        self.console_bar.setObjectName("console")
        self.console_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.console_bar.setStyleSheet("background-color: #3c3f41")
        verticalLayout = QVBoxLayout(self.console_bar)
        verticalLayout.setObjectName("verticalLayout")
        
        
        self.field_result_output = QTextBrowser(self.console_bar)
        self.field_result_output.setStyleSheet("background-color: #F4F9F9; color: #a4a3a3; border-width: 2px; border-style: solid; border-color: #555555 #555555 #555555 #555555;")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.field_result_output.setSizePolicy(sizePolicy)
        sizePolicy.setHeightForWidth(self.field_result_output.sizePolicy().hasHeightForWidth())        
        self.field_result_output.setObjectName("field_result_output")
        verticalLayout.addWidget(self.field_result_output)
        
        self.field_path_current_file = QLabel(self.console_bar)
        self.field_path_current_file.setObjectName("field_path_current_file")
        self.field_path_current_file.setStyleSheet("color: #a4a3a3;")
        verticalLayout.addWidget(self.field_path_current_file)

        ###############################################
        ################# HSPLIT ######################
        # horizontal split view
        self.hsplit = QSplitter(Qt.Horizontal)
        
        self.vsplit = QSplitter(Qt.Vertical)
        self.vsplit.addWidget(self.hsplit)
        self.vsplit.addWidget(self.console_bar)
        
        self.setLayout(body)
    
        ###############################################
        ################ TAB VIEW ####################
        # Tab Widget to add editor to
        self.tab_view = QTabWidget()
        self.tab_view.setContentsMargins(0, 0, 0, 0)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setMovable(True)
        self.tab_view.setDocumentMode(True)
        self.tab_view.tabCloseRequested.connect(self.close_tab)
        self.tab_view.setMouseTracking(True)
        self.tab_view.enterEvent = self.set_cursor_pointer
        self.tab_view.leaveEvent = self.set_cursor_arrow
        self.tab_view.currentChanged.connect(self.tab_changed)


        ###############################################
        ############## SideBar #######################
        self.side_bar = QFrame()
        self.side_bar.setFrameShape(QFrame.StyledPanel)
        self.side_bar.setFrameShadow(QFrame.Raised)
        self.side_bar.setContentsMargins(0, 0, 0, 0)
        self.side_bar.setMaximumWidth(40)
        self.side_bar.setStyleSheet(
            """
            background-color: #282c34;
        """
        )
        side_bar_content = QVBoxLayout()
        side_bar_content.setContentsMargins(5, 10, 5, 0)
        side_bar_content.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        
        ###############################################
        ############ File Manager ###############

        # frame and layout to hold tree view
        self.file_manager_frame = self.get_frame()
        self.file_manager_frame.setMaximumWidth(400)
        self.file_manager_frame.setMinimumWidth(200)

        # layout for tree view
        self.file_manager_layout = QVBoxLayout() # was tree_view_layout
        self.file_manager_layout.setContentsMargins(0, 0, 0, 0)
        self.file_manager_layout.setSpacing(0)

        self.file_manager = FileManager(tab_view=self.tab_view,set_new_tab=self.set_new_tab, main_window=self) # was tree_view

        # setup layout
        self.file_manager_layout.addWidget(self.file_manager)
        self.file_manager_frame.setLayout(self.file_manager_layout)

        ###############################################
        ############## Search View ####################

        # layout for search view
        self.search_frame = self.get_frame()
        self.search_frame.setMaximumWidth(400)
        self.search_frame.setMinimumWidth(200)
        search_layout = QVBoxLayout()
        search_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        search_layout.setContentsMargins(0, 10, 0, 0)
        search_layout.setSpacing(0)
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search")
        search_input.setFont(self.window_font)
        search_input.setAlignment(Qt.AlignmentFlag.AlignTop)

        ############# CHECKBOX ################
        self.search_checkbox = QCheckBox("Search in modules")
        self.search_checkbox.setFont(self.window_font)
        self.search_checkbox.setStyleSheet("color: white; margin-bottom: 10px;")

        self.search_worker = SearchWorker()
        self.search_worker.finished.connect(self.search_finished)
        search_input.textChanged.connect(
            lambda text: self.search_worker.update(
                text,
                self.file_manager.model.rootDirectory().absolutePath(),
                self.search_checkbox.isChecked(),
            )
        )

        ###############################################
        ############## Search ListView ####################
        self.search_list_view = QListWidget()
        self.search_list_view.setFont(QFont("FiraCode", 13))

        self.search_list_view.itemClicked.connect(self.search_list_view_clicked)

        search_layout.addWidget(self.search_checkbox)
        search_layout.addWidget(search_input)
        search_layout.addSpacerItem(
            QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        )
        search_layout.addWidget(self.search_list_view)
        self.search_frame.setLayout(search_layout)

    
        ####################################################
        ############## SideBar Icons #######################
        folder_label = self.get_sidebar_button(
            ":/icons/folder-icon-blue.svg", self.file_manager_frame
        )
        side_bar_content.addWidget(folder_label)
        search_label = self.get_sidebar_button(":/icons/search-icon.svg", self.search_frame)
        side_bar_content.addWidget(search_label)

        self.side_bar.setLayout(side_bar_content)
        body.addWidget(self.side_bar)


        self.welcome_frame = self.get_frame()
        self.welcome_frame.setStyleSheet(
        """
            QFrame {
                background-color: #21252b;
                border: none;
                color: #D3D3D3;
            }
            QFrame::hover {
                color: white;
            }
        """
        )

        welcome_layout = QVBoxLayout()
        welcome_layout.setContentsMargins(0, 0, 0, 0)
        welcome_layout.setSpacing(20)
        welcome_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

        wlcm_title = self.create_label(
            "Bienvenido a OpencorEditor!",
            "color: #84878B;",
            Qt.AlignmentFlag.AlignHCenter,
            font_size=25,
            min_height=90,
        )
        wlcm_msg = self.create_label(
            "Aquí podrás programar con tu lenguaje ani.",
            "color: #84878B;",
            Qt.AlignmentFlag.AlignHCenter,
            font_size=15,
            min_height=100,
        )

        welcome_layout.addWidget(wlcm_title)
        welcome_layout.addWidget(wlcm_msg)
        self.welcome_frame.setLayout(welcome_layout)    
        
        
    
        # add file manager and tab view
        self.hsplit.addWidget(self.file_manager_frame)
        #self.hsplit.addWidget(self.ventana)
        self.hsplit.addWidget(self.welcome_frame)
        self.current_side_bar = self.file_manager_frame
        
        # self.hsplit.addWidget(self.tab_view)

        # add hsplit and sidebar to body
        body.addWidget(self.side_bar)
        body.addWidget(self.vsplit)
        body_frame.setLayout(body)

        # set central widget

        self.setCentralWidget(body_frame)

    def search_finished(self, items):
        self.search_list_view.clear()
        for i in items:
            self.search_list_view.addItem(i)

    def search_list_view_clicked(self, item: SearchItem):
        self.set_new_tab(Path(item.full_path))
        editor: Editor = self.tab_view.currentWidget()
        editor.setCursorPosition(item.lineno, item.end)
        editor.setFocus()

    def new_file_act(self):
        """Create new file"""
        ...

    def show_hide_tab(self, e: QMouseEvent, widget: str):
        if self.current_side_bar == widget:
            if widget.isHidden():
                widget.show()
            else:
                widget.hide()

            return

       
        self.hsplit.replaceWidget(0, widget)
        self.current_side_bar = widget
        self.current_side_bar.show()


    def close_tab(self, index: int):
        self.tab_view.removeTab(index)

    def tab_changed(self, index: int):
        editor = self.tab_view.widget(index)
        if editor:
            self.current_file = editor.path

    def set_up_status_bar(self):
        # Create a status bar
        stat = QStatusBar(self)
        # change message
        stat.setStyleSheet("color: #D3D3D3;")
        stat.showMessage("Ready", 3000)
        self.setStatusBar(stat)

    def set_up_menu(self):
        # Create a menu bar ,
        menu_bar = self.menuBar()
        

        # File menu
        file_menu = menu_bar.addMenu("File")

        new_file = QAction("New", self)
        new_file.setShortcut("Ctrl+N")
        new_file.triggered.connect(self.new_file)

        save_file = QAction("Save", self)
        save_file.setShortcut("Ctrl+S")
        save_file.triggered.connect(self.save_file)

        save_as = QAction("Save As", self)
        save_as.setShortcut("Ctrl+Shift+S")
        save_as.triggered.connect(self.save_as)

        open_file = QAction("Open File", self)
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file_dlg)

        open_folder_action = QAction("Open Folder", self)
        open_folder_action.setShortcut("Ctrl+K")
        open_folder_action.triggered.connect(self.open_folder)
        
        self.toggleIntAct = QAction("Indentation Guides",self)
        self.toggleIntAct.triggered.connect(self.toggleIntGuide)
        self.toggleIntAct.setCheckable(True)
        self.toggleIntAct.setChecked(True)

        self.toggleLNAct = QAction("Line Numbers",self)
        self.toggleLNAct.triggered.connect(self.toggleLN)
        self.toggleLNAct.setCheckable(True)
        self.toggleLNAct.setChecked(True)
        
        self.fontAct = QAction("Choose Font",self)
        self.fontAct.triggered.connect(self.chooseFont)

        # Add the menu item to the menu
        file_menu.addAction(new_file)
        file_menu.addAction(open_file)
        file_menu.addAction(open_folder_action)
        file_menu.addSeparator()
        file_menu.addAction(save_file)
        file_menu.addAction(save_as)
        file_menu.addSeparator()
        file_menu.addAction(self.toggleIntAct)
        file_menu.addAction(self.toggleLNAct)
        file_menu.addAction(self.fontAct)
        
         # Add el menu de ejecutar
        run_menu = menu_bar.addMenu("Run")
        run_file = QAction("Run", self)
        run_file.setShortcut("Ctrl+R")
        run_file.triggered.connect(self.run)
        
         # Parar Codigo
        parar = QAction("Detener Codigo",self)
        parar.triggered.connect(self.stop_code) 
        
        # Add borrar consola 
        borrar = QAction("Borrar",self)
        borrar.triggered.connect(self.borrar)
        
        # Add eliminar consola 
        eliminar = QAction("Eliminar Consola",self)
        eliminar.triggered.connect(self.eliminar)
        
        # Mostrar Consola 
        mostrar = QAction("Mostrar Consola", self)
        mostrar.triggered.connect(self.mostrar)
        
        run_menu.addAction(run_file)
        run_menu.addAction(parar)
        run_menu.addAction(borrar)
        run_menu.addAction(eliminar)
        run_menu.addAction(mostrar)

        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        copy_action = QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)

        edit_menu.addAction(copy_action)
        
        # GIT_MENU
        
        git_menu = menu_bar.addMenu("Save GIT")
        save_git = QAction("SaveGit",self)
        save_git.setShortcut("Ctrl+G")
        save_git.triggered.connect(self.save_git)
        
        back_git = QAction("BackGit",self)
        back_git.setShortcut("Ctrl+B")
        back_git.triggered.connect(self.back_git)
        
        crear_repositorio = QAction("CrearRepo",self)
        crear_repositorio.setShortcut("Ctrl+Shit+C")
        crear_repositorio.triggered.connect(self.crear_repositorio)
        
        git_menu.addAction(crear_repositorio)
        git_menu.addAction(save_git)
        git_menu.addAction(back_git)

    def is_binary(self, path):
        """
        Check if file is binary
        """
        with open(path, "rb") as f:
            return b"\0" in f.read(1024)

    def copy(self):
        t = self.tab_view.currentWidget()
        if t is not None:
            t.copy()

    def set_new_tab(self, path: Path, is_new_file=False):
        # check if file is binary or not
        if self.welcome_frame:
            idx = self.hsplit.indexOf(self.welcome_frame)
            self.hsplit.replaceWidget(idx, self.tab_view)
            self.welcome_frame = None
        text_edit = self.get_editor(path, path.suffix in {".py", ".pyw",".ani"})
        if is_new_file:
            self.tab_view.addTab(text_edit, "untitled")
            self.setWindowTitle("untitled - " + self.app_name)
            self.statusBar().showMessage(f"Opened untitled", 2000)
            self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
            self.current_file = None
            return

        if not path.is_file():
            return
        if self.is_binary(path):
            self.statusBar().showMessage("Cannot Opne Binary File", 2000)
            return

        # check if file is already open
        for i in range(self.tab_view.count()):
            if self.tab_view.tabText(i) == path.name:
                # set the active tab to that
                self.tab_view.setCurrentIndex(i)
                self.current_file = path
                return

        self.tab_view.addTab(text_edit, path.name)
        text_edit.setText(path.read_text())
        self.setWindowTitle(f"{path.name} - {self.app_name}")
        self.statusBar().showMessage(f"Opened {path.name}", 2000)
        # set the active tab to that
        self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
        self.current_file = path

    def new_file(self):
        # create new file
        self.set_new_tab(None, True)

    def save_file(self):
        # save file
        if self.current_file is None and self.tab_view.count() > 0:
            self.save_as()
            return
        text_edit = self.tab_view.currentWidget()
        self.current_file.write_text(text_edit.text())
        self.statusBar().showMessage(f"Saved {self.current_file.name}", 2000)
        

    def save_as(self):
        # save as
        text_edit = self.tab_view.currentWidget()
        if text_edit is None:
            return
        file_path = QFileDialog.getSaveFileName(self, "Save As", os.getcwd())[0]
        if file_path == "":
            self.statusBar().showMessage("Cancelled", 2000)
            return
        path = Path(file_path)
        path.write_text(text_edit.text())
        self.tab_view.setTabText(self.tab_view.currentIndex(), path.name)
        self.statusBar().showMessage(f"Saved {path.name}", 2000)

    def open_file_dlg(self):
        ops = QFileDialog.Options()
        # use custom dialog
        ops |= QFileDialog.DontUseNativeDialog
        new_file, _ = QFileDialog.getOpenFileName(
            self, "Pick A File", "", "All Files (*);;Python Files (*.py)", options=ops
        )

        f = Path(new_file)
        self.set_new_tab(f)

    def open_folder(self, ):
        ops = QFileDialog.Options()
        ops |= QFileDialog.DontUseNativeDialog
        new_folder = QFileDialog.getExistingDirectory(
            self, "Pick A Folder", "", options=ops
        )
        if new_folder:
            self.model = QFileSystemModel()
            self.model.setRootPath(new_folder)
            self.file_manager.setRootIndex(self.model.index(new_folder))
            self.statusBar().showMessage(f"Opened {new_folder}", 2000)
            
            
    def exit_the_program(self):
        self.close()        
            
    def hide_result_field(self):
        self.field_result_output.hide()

    def run(self):
        self.field_result_output.show()
        self.field_result_output.clear()
        if self.process is None:
            self.field_result_output.append("[Started]\n")
            self.process = QProcess()
            self.process.readyReadStandardOutput.connect(self.handle_stdout)
            self.process.readyReadStandardError.connect(self.handle_stderr)
            self.process.started.connect(self.timer.start)
            self.process.finished.connect(self.finished_code)
            try:
                self.process.start("python", [f"{self.field_path_current_file.text()}"])
            except Exception as error:
                warning = QMessageBox()
                warning.setWindowTitle("Error")
                warning.setText(f"{error}")
                warning.setIcon(QMessageBox.Warning)
                x = warning.exec_()
            
        self.field_result_output.setText("Archivo Compilado"+self.tab_view.objectName())
    
    def stop_code(self):
        try:
            self.process.kill()
        except Exception as error:
            warning = QMessageBox()
            warning.setWindowTitle("Error")
            warning.setText(f"{error}")
            warning.setIcon(QMessageBox.Warning)
            x = warning.exec_()
        
    def finished_code(self):
        process_execution_time = self.timer.elapsed()
        self.field_result_output.append(f"[Finished in {process_execution_time / 1000}s]")
        self.process = None
        
    
    def borrar(self):
        self.field_result_output.clear()
    
    
    def eliminar(self):
        self.field_result_output.setVisible(False)
        
        
    def mostrar(self):
        self.field_result_output.setVisible(True)
        
        
    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.field_result_output.append(stderr)


    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.field_result_output.append(stdout)
        
    
    def save_git(self):
        
        #repo_dir = "/Users/felipecastillo/Desktop/ProyectosFelipe/Visual Studio/OpenCoreEditorFinal/.git/"
        
        repo_dir = os.getcwd()
        
        repo = git.Repo(repo_dir)
        
        repo.git.add(A=True)
    
        repo.index.commit("Mensaje del commit") 
        
        origin = repo.remote('origin')   
        
        origin.push()
        
    
    def crear_repositorio(self): 
        
        self.ventana4 = QWidget()

        # Crear cuadro de texto para ingresar URL   
        self.textbox4 = QLineEdit(self.ventana4)   
        
        # Crear etiqueta para el cuadro de texto para ingresar URL  
        self.label4 = QLabel("Ingresar nombre de usuario GitHub: ", self.ventana4) 

        # Boton para ingresar la url  
        self.button4 = QPushButton("Ingresar", self.ventana4)    

        # Posiciones en la ventana  
        self.label4.move(60, 25)   

        # Posiciones en la ventana   
        self.textbox4.move(60, 50)    

         # Posiciones en la ventana   
        self.button4.move(100, 260) 
        
        self.ventana5 = QWidget()             
        # Crear cuadro de texto para ingresar URL            
        self.textbox5 = QLineEdit(self.ventana4)                     
        # # Crear etiqueta para el cuadro de texto para ingresar URL           
        self.label5 = QLabel("Ingresar nombre del repo:", self.ventana4)           
        # # Boton para ingresar la url           
        #self.button2 = QPushButton("Ingresar", self.ventana)              
        # # Posiciones en la ventana           
        self.label5.move(60, 120)             
        # # Posiciones en la ventana            
        self.textbox5.move(60, 150)               
        # # Posiciones en la ventana            
        #self.button2.move(150, 180)
        
        #self.ventana6 = QWidget()             
        # Crear cuadro de texto para ingresar URL            
        #self.textbox6 = QLineEdit(self.ventana4)                     
        # # Crear etiqueta para el cuadro de texto para ingresar URL           
        #self.label6 = QLabel("Ingresar ruta de su repo:", self.ventana4)           
        # # Boton para ingresar la url           
        #self.button3 = QPushButton("Ingresar", self.ventana)              
        # # Posiciones en la ventana           
        #self.label6.move(60, 200)             
        # # Posiciones en la ventana            
        #self.textbox6.move(60, 220)               
        # # Posiciones en la ventana            
        #self.button3.move(150, 180)
        
        # Señal al hacer click sobre el botón     
        git_url = self.button4.clicked.connect(self.ruta) 
          
        # Mostrar todos los elementos en la pantalla  
        self.ventana4.show() 
    
    
    def ruta(self,url):
        
        nom_repo = str(self.textbox5.text())
        
        nom_usuario = str(self.textbox4.text())
        
        carpeta = os.getcwd()
        
        repo = git.Repo.init(carpeta) #Crea el repositorio en la carpeta mi_codigo 

        os.chdir(carpeta) #Cambia el directorio de trabajo a la carpeta del repositorio creado

        repo.index.add(['carpeta/*']) #Agrega todos los archivos de la carpeta al repositorio

        repo.index.commit("Guardado en GitHub") #Realiza el commit con el mensaje "Guardado en GitHub"

        origin = repo.create_remote('origin', 'https://github.com/nom_usuario/nom_repo.git') #Crea un remoto llamado "origin" en el repositorio de Github indicado

        origin.push() #Envia los cambios al repositorio remoto
        
    
    def back_git(self):
        
        
        self.ventana = QWidget()

        # Crear cuadro de texto para ingresar URL   
        self.textbox = QLineEdit(self.ventana)   
        
        # Crear etiqueta para el cuadro de texto para ingresar URL  
        self.label = QLabel("Ingresar Usuario de Github : ", self.ventana) 

        # Boton para ingresar la url  
        self.button = QPushButton("Ingresar", self.ventana)    

        # Posiciones en la ventana  
        self.label.move(60, 25)   

        # Posiciones en la ventana   
        self.textbox.move(60, 50)    

         # Posiciones en la ventana   
        self.button.move(100, 260)    
        
        self.ventana2 = QWidget()             
        # Crear cuadro de texto para ingresar URL            
        self.textbox2 = QLineEdit(self.ventana)                     
        # # Crear etiqueta para el cuadro de texto para ingresar URL           
        self.label2 = QLabel("Ingresar Contraseña:", self.ventana)           
        # # Boton para ingresar la url           
        #self.button2 = QPushButton("Ingresar", self.ventana)              
        # # Posiciones en la ventana           
        self.label2.move(60, 120)             
        # # Posiciones en la ventana            
        self.textbox2.move(60, 150)               
        # # Posiciones en la ventana            
        #self.button2.move(150, 180)
        
        self.ventana3 = QWidget()             
        # Crear cuadro de texto para ingresar URL            
        self.textbox3 = QLineEdit(self.ventana)                     
        # # Crear etiqueta para el cuadro de texto para ingresar URL           
        self.label3 = QLabel("Ingresar ruta de su repo:", self.ventana)           
        # # Boton para ingresar la url           
        #self.button3 = QPushButton("Ingresar", self.ventana)              
        # # Posiciones en la ventana           
        self.label3.move(60, 200)             
        # # Posiciones en la ventana            
        self.textbox3.move(60, 220)               
        # # Posiciones en la ventana            
        #self.button3.move(150, 180)

         # Señal al hacer click sobre el botón     
        self.button.clicked.connect(self.descargar_repositorio) 
          
        # Mostrar todos los elementos en la pantalla  
        self.ventana.show()  
        #self.ventana1.show()
                  
    
    def descargar_repositorio(self,url):
        #Descarga un repositorio de Github en el directorio indicado.

        #Argumentos:
        #url (str): La dirección URL del repositorio.
        #directorio (str): El directorio donde se guardará el proyecto.

        #Devuelve:
        #None.
        
        ruta_repo = str(self.textbox3.text())
         
        # Descargar el repositorio en el directorio indicado.
        git.Git(os.getcwd()).clone(ruta_repo)
        
    
    def closeEvent(self, event):
        self.save_file()
        reply = QMessageBox.question(self, 'Exit',
                                     'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
      
    
    def toggleLN(self):
        state = self.edit.marginLineNumbers(0)
        self.edit.setMarginLineNumbers(0, not state)
        self.edit.setMarginWidth(0,0) if state == True else self.edit. \
                                setMarginWidth(0,self.edit.metrics.width("00000"))
                                
    def chooseFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            config.font = font
            try:
                self.getEditor(self.tab.currentIndex()).lexer().setFont(config.font)
            except AttributeError:
                self.getEditor(self.tab.currentIndex()).setLang(QsciLexerText())
                #print self.getEditor(self.tab.currentIndex()).lexer()
                self.getEditor(self.tab.currentIndex()).lexer().setFont(config.font)
      
            
    def toggleIntGuide(self):
        state = self.edit.indentationGuides()
        self.edit.setIndentationGuides(not state)
    


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
