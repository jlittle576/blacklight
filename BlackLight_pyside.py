__author__ = 'JoesDesktop'
from lxml import etree

#root = etree.fromstring('<note to= "Tiff" from="Joe"><heading>Reminder</heading><body>Don`t forget me this weekend!</body></note>')

import sys, os, time, pdb, re
#from copy import copy
from lxml import etree, objectify
from PySide import QtGui, QtCore, QtUiTools
from gui import Ui_MainWindow
import copy
from QColorScheme import QColorScheme

# try:
#     _fromUtf8 = QtCore.QString.fromUtf8
# except AttributeError:
# def _fromUtf8(s):
#     return str(s)




# root = etree.parse('MDI_300_300_spr.xml')
# #tree = etree.ElementTree(root)
# for e in root.iter():
#     print tree.getpath(e)




class GUI(QtGui.QMainWindow):
    def __init__(self, parent=None):

        #Initialization
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        global window, ui, qTree, qText, lineNumber, cursor, focus
        lineNumber = -1
        window = self
        ui = self.ui
        self.ui.setupUi(self)
        qTree = ui.treeWidget
        qText = ui.textBrowser
        cursor = qText.textCursor()
        focus = qText

        #self.setup_qText()
        self.setup_qTree()
        #self.setup_tFilter()
        self.setup_toolBar()



        #self.tFilter = QtGui.QLineEdit(self.toolbar)


        #socket functions
        def treeDisplay():
            global focus
            focus = qTree

        def filter():
            global focus
            focus = tFilter
            currentTrunk.treeBlip()

        def displayRoot():
            global currentBranch
            currentBranch = qTree.headerItem().data(0, 32).toPyObject()
            currentBranch.display()

        def displayCurrent():
            try:
                currentBranch.display()
            except:
                pass

        #sockets
        self.ui.actionOpen.triggered.connect(open)
        tFilter.textChanged.connect(filter)
        qTree.itemClicked.connect(treeDisplay)
        #qTree.itemClicked.connect(display)
        # self.ui.stylePick.activated.connect(displayCurrent)
        # self.ui.depthPick.activated.connect(displayCurrent)


        #gui initialization
        qTree.headerItem().setText(0, '')
        qTree.header().setClickable(True)


        #------------ keyboard shortcuts -------------
        def enter():
            currentTrunk.display()

        keyReturn = QtGui.QShortcut(QtGui.QKeySequence("Return"), self)
        keyReturn.activated.connect(enter)


    def setup_qTree(self):

        def on_context_menu():
             self.popMenu.exec_( QtGui.QCursor.pos())

        def collapse_siblings():
            pass

        qTree.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
        qTree.customContextMenuRequested.connect(on_context_menu)

        collapseSiblingsAction = QtGui.QAction( "Collapse All Siblings", self)
        collapseSiblingsAction.triggered.connect(collapse_siblings)
        expandSiblingsAction = QtGui.QAction( "Expand All Siblings", self)
        expandSiblingsAction.triggered.connect(collapse_siblings)


        # Popup Menu is not visible, but we add actions from above
        self.popMenu = QtGui.QMenu( self )
        self.popMenu.addAction( collapseSiblingsAction )
        self.popMenu.addAction( expandSiblingsAction )

    def setup_toolBar(self):
        #------- Toolbar --------------------------------------

        #-- Upper Toolbar --
        self.toolbar = self.addToolBar("Options")

        openAction = QtGui.QAction(QtGui.QIcon("icons/open.png"), "Open", self)
        openAction.setStatusTip("Open existing document")
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(open)
        self.toolbar.addAction(openAction)

        helpAction = QtGui.QAction(QtGui.QIcon("icons/settings.png"), "Settings", self)
        helpAction.setStatusTip("Settings")
        helpAction.setShortcut("Ctrl+S")
        self.toolbar.addAction(helpAction)

        helpAction = QtGui.QAction(QtGui.QIcon("icons/help.png"), "Help", self)
        helpAction.setStatusTip("Help")
        helpAction.setShortcut("Ctrl+H")
        self.toolbar.addAction(helpAction)

        global tFilter
        tFilter = QtGui.QLineEdit(self)
        tFilter.setObjectName(_fromUtf8("tFilter"))

        self.toolbar.addWidget(tFilter)




class Trunk():
    def __init__(self, xmlFile):
        global currentTrunk
        currentTrunk = self
        self.tree = etree.parse(xmlFile)
        self.root = self.tree.getroot()
        self.directory = []
        qTree.headerItem().setText(0, xmlFile)

        objectify.deannotate(self.tree, pytype=True, xsi=True, xsi_nil=True)
        objectify.deannotate(self.root, pytype=True, xsi=True, xsi_nil=True)

        self.populate()


    def populate(self):

        ancestry = []
        cAncestry = []
        address = []
        prev_depth = 0

        for e in self.root.iter():
            tag = e.tag
            cTag = clean(tag)
            text = e.text
            xpath = self.tree.getpath(e)
            depth = len(xpath.split('/')) - 2

            #depth
            if depth == 0 or depth == len(ancestry):
                ancestry.append(tag)
                cAncestry.append(cTag)
            else:
                ancestry[depth] = tag
                cAncestry[depth] = cTag

            if depth <= prev_depth:
                cAncestry = cAncestry[:depth+1]
                ancestry = ancestry[:depth+1]

            #address
            if depth == 0 or depth == len(address):
                address.append(0)
            else:
                address[depth] += 1

            if depth <= prev_depth:
                address = address[:depth + 1]

            #trailing init
            prev_depth = depth

            #stroage
            props = dict(zip(
                ('e', 'cTag', 'tag', 'depth', 'text', 'address', 'ancestry', 'cAncestry', 'attrib', 'trunk'),
                (e, cTag, tag, depth, text, copy.deepcopy(address), copy.deepcopy(ancestry), copy.deepcopy(cAncestry),
                 e.attrib, self)  #e.attrib, self)
            ))

            #generate a new object and add to list
            branch = Branch(props)
            self.directory.append(branch)
        self.treeBlip()

    def filterSet(self):

        direct_matches = []

        for branch in self.directory:
            branch.filterMatch = 0

        # if tFilter.text() == '':
        #     return

        for branch in self.directory:

            ancestor = None
            fStrs = str(tFilter.text()).lower().rstrip().split(' ')
            #print '!!',fStrs
            match = False
            for fStr in fStrs:
                fStr = fStr.lower()
                fStr = fStr.replace("**", "$$$")
                fStr = fStr.replace("*", "\w*")
                fStr = fStr.replace("?", "\w")
                fStr = fStr.replace("/", "\w*/\w*")

                expStr = fStr.split('/')
                fLen = len(expStr)


                ances = '/'.join(branch.cAncestry).lower()

                if not fStr[-3:] == '$$$':
                    fStr = fStr+'\w*\Z'

                if '$$$' in fStr:
                    fStr = fStr.replace("$$$", ".*")
                    wild = True
                    concat_ancestry = '/'.join(branch.cAncestry).lower()
                else:
                    concat_ancestry = '/'.join(branch.cAncestry[(-1 * fLen):]).lower()



                tag = branch.cTag.lower()
                try:
                    ui.statusBar.showMessage('')
                    fSearch = re.search(fStr, concat_ancestry)
                except:
                    ui.statusBar.showMessage('Current search string invalid, dynamic updating paused')
                    fSearch = False

                # if ('bush' in '/'.join(branch.cAncestry).lower()) and ('stiff' in '/'.join(branch.cAncestry).lower()):
                #      print '>>', fStr, concat_ancestry, fSearch
                direct_matches = []

                if fSearch:

                    if 0: #fSearch.groups():   grouping were used
                        pass
                        # for group in fSearch.groups():
                        #     ancestor = branch
                        #     while ancestor:
                        #         if re.search(group, ancestor.cTag):
                        #             ancestor.filterMatch = 1
                        #             direct_matches.append(ancestor.address)
                        #             match = True
                        #         elif match:
                        #             ancestor.branchMatch = 2
                        #             ancestor = branch.parent


                    else:
                        branch.filterMatch = 1
                        direct_matches.append(branch.address)
                        for child in branch.children:
                            #print '>>', branch.cTag, child.cTag
                            child.filterMatch = 3
                        ancestor = branch.parent
                        while ancestor:
                            if ancestor.filterMatch != 1:
                                ancestor.filterMatch = 2
                            ancestor = ancestor.parent


        #decendants
        for branch in currentTrunk.directory:
            if branch.filterMatch == 0:
                for match in direct_matches:
                    if match in branch.address:
                        branch.filterMatch == 3

    def treeBlip(self):
        qTree.clear()

        #filterSet sets each branch's filterMatch flag based in tFilter
        self.filterSet()

        #display settings
            #displayed, expanded, color #
        settings = [[0, 0, 0],    #unselected
                    [1, 1, 1],    #active
                    [1, 1, 2],    #parent
                    [1, 0, 0]]    #children

        for branch in self.directory:

            if settings[branch.filterMatch][0]:
                #tree item
                tItem = QtGui.QTreeWidgetItem()
                if branch.address == [0]:
                    qTree.addTopLevelItem(tItem)
                else:
                    # try:
                    branch.parent.tItem.addChild(tItem)
                    # except:
                    #     print '??',branch.cAncestry, branch.filterMatch
                    #     #sys.exit()

                tItem.setText(0, branch.cTag)
                tItem.setData(0, 32, branch)
                branch.tItem = tItem
                branch.tItem.setExpanded(settings[branch.filterMatch][1])
                branch.tItem.setForeground(0, colors.tree[settings[branch.filterMatch][2]])

    def display(self):
        qText.clear()

        #determin if and which criteria for displaying elements
        if focus == tFilter:
            def check(branch):
                return branch.filterMatch
                #print branch.filterMatch,'}}'
        elif qTree.currentItem():
            currentBranch = qTree.currentItem().data(0, 32).toPyObject()
            currentAddress = currentBranch.address

            def check(branch):
                #isChild()
                if len(branch.address) >= len(currentAddress):
                    return currentAddress == branch.address[:len(currentAddress)]
                else:
                    return False
        else:
            def check(a):
                return True
        prev_depth = 0

        #conditional loop print
        for branch in self.directory:
            if check(branch):
                depth = branch.depth
                cInsert(depth, branch, None, branch.filterMatch)
                if branch.filterMatch == 1:
                    for key in branch.attrib:
                        cInsert(depth, branch, key)

                    cursor.insertText('\n')
                prev_depth = depth

    def getDecendants(self, limb):
        decendants = []
        for branch in self.directory:
            if not limb.address == branch.address:
                if '.'.join(branch.address) in '.'.join(limb.address):
                    decendants.append(branch)
        return decendants




class Branch():
    def __init__(self, props):
        #print 'Putting  ',props
        #unpack properties
        self.e = props['e']
        self.tag = props['tag']
        self.cTag = props['cTag']
        self.depth = props['depth']
        self.text = props['text']
        self.ancestry = props['ancestry']
        self.cAncestry = props['cAncestry']
        self.address = props['address']
        self.attrib = props['attrib']
        self.trunk = props['trunk']
        self.relate(self.trunk)  #sets Parent

        self.children = []
        self.filterMatch = 2
        #tree item
        self.tItem = None

    def props(self):
        self.props = dict(zip(
            (
                'e', 'cTag', 'tag', 'depth', 'text', 'address', 'ancestry', 'cAncestry', 'attrib', 'parent', 'filterMatch'),
            (self.e, self.cTag, self.tag, self.depth, self.text, self.address, self.ancestry, self.cAncestry,
             self.e.attrib, self.parent, self.filterMatch)
        ))
        return self.props

    def relate(self, trunk):
        parent_address = self.address[:-1]
        for limb in reversed(trunk.directory):
            if limb.address == parent_address:
                limb.addChild(self)
                self.parent = limb
                return

        #if root
        self.parent = None

    def addChild(self, branch):
        self.children.append(branch)
        self.numChildren = len(self.children)


def clean(tag):
    if '}' in tag:
        return tag.split('}')[1]
    else:
        return tag

def colorize(app):
    #ilitialize colors object
    global colors
    class theme: pass
    colors = theme()

    #custom colors
    gunmetal = QtGui.QColor()
    gunmetal.setHsl(324, 0, 60)
    brightBlue = QtGui.QColor()
    brightBlue.setHsv(200, 255, 255)
    fadedBlue = QtGui.QColor()
    fadedBlue.setHsv(200, 150, 150)

    #colorscheme
    app.ColorScheme = QColorScheme(gunmetal,brightBlue, 2.5)

    #text colors
    #unselected, active, parent, child
    colors.tree = [QtCore.Qt.darkGray, brightBlue, QtCore.Qt.white, QtCore.Qt.darkGray]
    colors.display = [QtCore.Qt.darkGray, brightBlue, QtCore.Qt.white, QtCore.Qt.darkGray]
    colors.att = QtCore.Qt.magenta
    colors.txt = QtCore.Qt.white

def cInsert(depth, branch, key=None, filterMatch=1):

    #line printer
    #handles identation, coloring, formatting

    global cursor

    #iterprint is for debugging text output
    iterPrint = False

    #formatting options
    newLines = 1
    indent_spacing = 3
    indent = ' ' * depth * indent_spacing

    #formatting functions
    def default():
        format.setForeground(colors.txt)
        cursor.setCharFormat(format)

    def lineNum():
        #format = qText.textCursor().charFormat()
        format.setForeground(QtCore.Qt.black)
        #format.setBackground(QtCore.Qt.lightGray)
        cursor.setCharFormat(format)
        cursor.insertText(' %03d ' % (cursor.blockNumber()))
        default()

    def close():
        if 0:  #branch.filterMatch == 1:  #element
            ancestry = '/'.join(branch.cAncestry)
            format.setForeground(QtCore.Qt.lightGray)
            cursor.setCharFormat(format)
            cursor.insertText('  (%s)\n' % (ancestry))
            default()
        else:
            cursor.insertText('\n')

    #color, name, data for element/attribute
    if not key:
        #child
        name = branch.cTag
        data = branch.text
        nColor = colors.display[filterMatch]
    else:
        #attribute
        name = key
        data = branch.attrib[key]
        indent = (depth+1)*indent_spacing*" "
        nColor = colors.att

    if iterPrint: print 'Printing', name


    #data formatting
    #rstripts data to reduce white space

    if data:
        datas = data.split('\n')
        i = 0
        for line in datas:
            if line.rstrip() == "":
                datas.pop(i)
            i += 1


    #get format, insert indent
    global format
    format = cursor.charFormat()
    #lineNum()
    cursor.insertText(indent)

    #name print
    format.setForeground(nColor)
    cursor.setCharFormat(format)
    cursor.insertText(name.rstrip())

    #data print
    if data and filterMatch == 1:
        cursor.insertText(': ')
        format.setForeground(colors.txt)
        cursor.setCharFormat(format)

        if len(datas) == 1:
            cursor.insertText(datas[0].rstrip().lstrip())
            close()
        else:
            close()
            for line in datas:
                #lineNum()
                format.setForeground(colors.txt)
                cursor.setCharFormat(format)
                cursor.insertText('%s' % (line.rstrip()))
                cursor.insertText('\n')
                newLines += 1
    else:
        close()

    default()
    if iterPrint: print '\n-----------------------\n', qText.toPlainText(), '\n-----------------------\n',
    if iterPrint:
        if stopTag in name: sys.exit()

    return newLines


def open(xmlFile):
    qTree.clear()
    qText.clear()
    tFilter.clear()

    fd = QtGui.QFileDialog()
    if not xmlFile:
        xmlFile = str(fd.getOpenFileName(None, "Select an XML file", "./", "*.xml"))
    if xmlFile:
        try:
            tree = Trunk(xmlFile)
            tree.treeBlip()
            tree.display()
            window.setWindowTitle("BlackLight - " + os.path.basename(xmlFile))
        except:
            ui.statusBar.showMessage('Failed to open ' + xmlFile)


def main():
    #Launch the GUI
    app = QtGui.QApplication(sys.argv)
    myApp = loadUiWidget('gui.ui')
    colorize(myApp)
    myApp.setWindowIcon(QtGui.QIcon('icon_small.png'))
    myApp.setWindowTitle("BlackLight")
    myApp.show()

    #auto-open for testing
    if len(sys.argv) > 1:
        open(sys.argv[1])


    sys.exit(app.exec_())


main()
