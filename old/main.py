import sys, os, time, pdb
from copy import copy
from lxml import etree, objectify
from PyQt4 import QtGui, uic, QtCore
from gui import Ui_MainWindow


class GUI(QtGui.QMainWindow):
    def __init__(self, parent=None):

        #Initialization
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        global window, ui, qTree, qText, lineNumber, cursor
        lineNumber = -1
        window = self
        ui = self.ui
        self.ui.setupUi(self)
        qTree = ui.treeWidget
        qText = ui.textBrowser
        cursor = qText.textCursor()


#------- Toolbar --------------------------------------

#-- Upper Toolbar --



        openAction = QtGui.QAction(QtGui.QIcon("icons/open.png"), "Open file",self)
        openAction.setStatusTip("Open existing document")
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(Open)

        findAction = QtGui.QAction(QtGui.QIcon("icons/find.png"), "Find",self)
        findAction.setShortcut("Ctrl+F")
        findAction.setStatusTip("Increase Font Size")
        #newAction.triggered.connect(self.New)

        zoomInAction = QtGui.QAction(QtGui.QIcon("icons/zoom_in.png"), "Zoom In",self)
        zoomInAction.setShortcut("Ctrl +")
        zoomInAction.setStatusTip("Increase Font Size")
        #newAction.triggered.connect(self.New)


        zoomOutAction = QtGui.QAction(QtGui.QIcon("icons/zoom_out.png"), "Zoom Out",self)
        zoomOutAction.setStatusTip("Decrease Font Size")
        zoomOutAction.setShortcut("Ctrl -")
        #saveAction.triggered.connect(self.Save)


        self.toolbar = self.addToolBar("Options")
        self.toolbar.addAction(openAction)
        self.toolbar.addAction(findAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(zoomInAction)
        self.toolbar.addAction(zoomOutAction)


        #socket functions
        def display():
            global currentBranch
            currentBranch = qTree.currentItem().data(0, 32).toPyObject()
            currentBranch.display()

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
        self.ui.actionOpen.triggered.connect(Open)
        qTree.itemClicked.connect(display)
        qTree.header().sectionClicked.connect(displayRoot)
        self.ui.stylePick.activated.connect(displayCurrent)
        self.ui.depthPick.activated.connect(displayCurrent)


        #gui initialization
        qTree.headerItem().setText(0, '')
        qTree.header().setClickable(True)

        self.ui.stylePick.addItem('YAML - ish')
        self.ui.stylePick.addItem('XML')

        #self.ui.depthPick.addItem('Auto')
        self.ui.depthPick.addItem('Full')
        self.ui.depthPick.addItem('Children')
        #self.ui.depthPick.addItem('Grandchildren')


class TreeBranch:
    def __init__(self, element, parent, trunk=None):


        tItem = QtGui.QTreeWidgetItem()
        if not parent:
            qTree.addTopLevelItem(tItem)
            self.isTopLvl = True
            self.trunk = trunk
        else:
            parent.tItem.addChild(tItem)
            self.isTopLvl = False
            self.trunk = parent.trunk

        self.parent = parent
        self.element = element
        self.tItem = tItem
        self.tag = element.tag

        tItem.setText(0, element.tag)
        tItem.setData(0, 32, self)

    def display(self):
        global cursor
        qText.clear()
        self.attrib = self.element.attrib
        if str(ui.stylePick.currentText()) == "XML":
            qText.append(etree.tostring(self.element))
        else:

            #root tag print
            cInsert(0, self.element)

            #attrib print
            for attrib in self.attrib:
                cInsert(1, self.element, attrib)
            branches = []

            #cursor.insertText('\n')
            #children print
            for branch in self.element.getchildren():
                cInsert(1, branch)

                #recursive prep
                twigs = branch.getchildren()
                if not twigs is None:
                    branches.append([branch, qText.textCursor().blockNumber(), twigs])

            #recursive print
            depth = 1
            while len(branches) > 0:
                limbs = branches
                branches = []
                depth += 1
                if depth > 99:
                    print 'Overflow'
                    sys.exit()
                delta = 0
                for limb in limbs:
                    n = limb[1]+delta
                    if iterPrint: print 'Setting line to ',n
                    cursor.movePosition(QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)
                    #cursor.movePosition(QtGui.QTextCursor.Down)
                    for i in range(n):
                        cursor.movePosition(QtGui.QTextCursor.Down)


                    localDelta = 0
                    for attrib in limb[0].attrib:
                        localDelta += cInsert(depth, branch, attrib)
                        #if iterPrint: time.sleep(5)

                    for branch in limb[2]:
                        localDelta += cInsert(depth, branch)
                        #if iterPrint: time.sleep(5)
                        twigs = branch.getchildren()
                        if (len(twigs) != 0) or (branch.attrib):
                            if branch.tag == 'File':
                                print branch.tag, qText.textCursor().blockNumber()
                                #sys.exit()
                            branches.append([branch, n+localDelta, twigs])

                    delta += localDelta

                    #if len(branches)>0:
                    #cursor.insertText('\n')


class TreeTrunk(TreeBranch):
    def __init__(self, xmlFile, treeWidget):
        self.tree = etree.parse(xmlFile)
        self.root = self.tree.getroot()
        self.element = self.root
        self.treeWidget = treeWidget
        qTree.headerItem().setText(0, os.path.basename(xmlFile))
        qTree.headerItem().setData(0, 32, self)

        #clean up namespaces
        for elem in self.root.getiterator():
            i = elem.tag.find('}')
            if i >= 0:
                elem.tag = elem.tag[i + 1:]
        objectify.deannotate(self.root)#, cleanup_namespaces=True)


    def tBlip(self):
        qTree.clear()
        qText.clear()

        branches = []
        limbs = []
        lvl = 0

        for twig in self.root.getchildren():
            branch = TreeBranch(twig, None, self)
            branches.append(branch)

        lvl = 1
        limbs = copy(branches)
        branches = []

        while True:
            for limb in limbs:
                twigs = limb.element.getchildren()
                if not twigs is None:
                    for twig in twigs:
                        branch = TreeBranch(twig, limb)
                        branches.append(branch)

            if len(branches) == 0:
                break
            lvl = lvl + 1
            limbs = copy(branches)
            branches = []

def setCursorLine(n):
    global cursor
    print 'Setting line to ',n
    cursor.movePosition(QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)
    cursor.movePosition(QtGui.QTextCursor.Down,  QtGui.QTextCursor.MoveAnchor, n+1)
    #cursor.movePosition(QtGui.QTextCursor.EndOfLine)
    #cursor.insertText('\n')

def cInsert(depth, element, key=None):
    newLines = 1
    global cursor
    #line printer
    #handles identation, coloring, formatting

    #get cursor, set line number
    #cursor = qText.textCursor()




    indent_spacing = 3
    indent =  ' ' * depth * indent_spacing


    #formatting functions
    def default():
        #format = qText.textCursor().charFormat()
        format.setBackground(QtCore.Qt.white)
        format.setForeground(QtCore.Qt.black)
        qText.setCurrentCharFormat(format)

    def lineNum():
        #format = qText.textCursor().charFormat()
        format.setForeground(QtCore.Qt.black)
        format.setBackground(QtCore.Qt.lightGray)
        cursor.setCharFormat(format)
        cursor.insertText(' %03d ' % (cursor.blockNumber()))
        default()



    #color, name, data for element/attribute
    dColor = QtCore.Qt.darkMagenta
    if not key:
        #child
        name = element.tag
        data = element.text
        nColor = QtCore.Qt.darkBlue
        #indent = indent + ' '*indent_spacing
    else:
        #attribute
        name = key
        data = element.get(key)
        nColor = QtCore.Qt.darkRed

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
    default()

    #name print
    format.setForeground(nColor)
    cursor.setCharFormat(format)
    cursor.insertText(name)

    #data print
    if not data is None:
        cursor.insertText(':')
        format.setForeground(dColor)
        cursor.setCharFormat(format)
        if data:
            if len(datas) == 1:
                cursor.insertText(datas[0])
                cursor.insertText('\n')
            else:
                cursor.insertText('\n')
                for line in datas:
                    #lineNum()
                    format.setForeground(dColor)
                    cursor.setCharFormat(format)
                    cursor.insertText(' %s' % (line))
                    cursor.insertText('\n')
                    newLines +=1
    else:
       cursor.insertText('\n')


    default()
    if iterPrint: print '\n-----------------------\n',qText.toPlainText(),'\n-----------------------\n',
    if iterPrint:
        if stopTag in name:sys.exit()

    return newLines

def Open():
    # Test
    # tItem = QtGui.QTreeWidgetItem()
    # tItem.setText(0,"test")
    # qTree.addTopLevelItem(tItem)
    fd = QtGui.QFileDialog()
    xmlFile = str(fd.getOpenFileName(None, "Select an XML file", "./", "*.xml"))
    if os.path.isfile(xmlFile):
        tree = TreeTrunk(xmlFile, qTree)
        tree.tBlip()
        window.setWindowTitle("Tarzan - " + os.path.basename(xmlFile))


def test():
    qText.clear()
    cursor = qText.textCursor()
    cursor.insertText('a\nb\nc')
    cursor.movePosition(QtGui.QTextCursor.Start)
    cursor.insertText('test\n')
    cursor.movePosition(QtGui.QTextCursor.Down)
    cursor.movePosition(QtGui.QTextCursor.Down)
    cursor.insertText('test\n')

def main():
    #Launch the GUI
    app = QtGui.QApplication(sys.argv)
    myApp = GUI()
    myApp.setWindowIcon(QtGui.QIcon('icon512.png'))
    myApp.setWindowTitle("Tarzan")
    myApp.show()

    #tree = TreeTrunk(r"menu.xml", qTree)
    tree = TreeTrunk(r"MDI_300_300_spr.xml", qTree)
    tree.tBlip()

    #debug stuff

    #test()
    global iterPrint,stopTag
    iterPrint = True
    stopTag = 'dodo'

    sys.exit(app.exec_())






    #tree = TreeTop(r"D:\Dropbox\code\projects\tarzan\menu.xml", window.treeView)
    #tree.tBlip()


if __name__ == '__main__':
    main()
