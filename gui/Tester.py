"""

Bastian Osterloh (TLK-Thermo)

23.04.2018
"""
# -*- coding: utf-8 -*

from PyQt5 import QtGui, QtCore, QtWidgets



from PyQt5 import QtGui, QtCore, QtWidgets


class TextItem(QtWidgets.QGraphicsItem):
    def __init__(self, scene, pos, text):
        try:
            self.scene = scene
            self.pos = pos
            super(TextItem, self).__init__()


            self.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable)
            # self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable)

            self.draw()

            self.scene.addItem(self)
        except Exception as err:
            print(err)

    def draw(self):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setBrush(QtCore.Qt.white)
        # painter.drawRect()
        painter.setPen(QtCore.Qt.red)
        painter.drawEllipse(self.pos, 100, 100)
        painter.end()


def removeItem(object):
    pass

def addDroppedItem(mimeData, pos, scene):
    try:
        urls = mimeData.urls()
        for url in urls:
            if str(url).endswith('.py'):
                print("dropped Python Script")
            else:
                print("dropped item of %s" % url)
                item = TextItem(scene, pos, str(url))
    except Exception as err:
        print(err)



class NewWindow(QtWidgets.QWidget):
    def __init__(self, parent):
        super(NewWindow, self).__init__()

        scene = MyScene(parent)
        # scene.selectionChanged.connect(parent.graphicsSelectionChanged)
        view = MyView(scene)
        view.setMinimumWidth(200)
        # view.setRenderHint(QtGui.QPainter.Antialiasing)
        view.removeItem.connect(removeItem)
        view.addDroppedItem.connect(addDroppedItem)

        # Layout
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        self.layout().addWidget(view,1,1,1,5)
        self.resize(800,600)

class MyScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent):
        # super(MyScene, self).__init__()
        QtWidgets.QGraphicsScene.__init__(self)


    def mouseMoveEvent(self, event):
        scenePos = event.lastScenePos()
        items = self.items(scenePos, QtCore.Qt.IntersectsItemShape)
        if len(items) > 0:
            print("intersected item %s" %items)
            # if isinstance(item, Connector):
            # if isinstance(item, Label) ...

    def mouseDoubleClickEvent(self, event):
        print("scene mouseDoubeClick")
        scenePos = event.lastScenePos()
        items = self.items(scenePos, QtCore.Qt.IntersectsItemShape)
        if len(items) > 0:
            print("double clicked Item %s " %items)
            items[0].mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        print("Scene Mouse press event")
        items = self.items(event.lastScenePos(), QtCore.Qt.IntersectsItemShape)
        if len(items) > 0:
            item = items[0]
            print("clicked Item")
            # if isinstance(item, Nodes.BaseNode):
            item.mousePressEvent(event)
            # self.moveMode = 1

    def mouseReleaseEvent(self, event):
        items = self.selectedItems()
        # if self.moveMode:
        #   self.moveMode = 0
        #   for item in selItems:
        #       item.mouseReleaseEvent(event)
        if len(items) > 0:
            for item in items:
                item.mouseReleaseEvent(event)

MIN_POS = -10000
MAX_SIZE = 20000

class MyView(QtWidgets.QGraphicsView):

    removeItem = QtCore.pyqtSignal(object)
    addDroppedItem = QtCore.pyqtSignal(object,object,object)

    def __init__(self, scene):
        # super(MyView, self).__init__(self, scene)
        QtWidgets.QGraphicsView.__init__(self, scene)
        self.setScene(scene)
        self.setAcceptDrops(True)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setStyleSheet('background-color: #282828;')
        self._zoom = 0

    def enterEvent(self, event):
        super(MyView, self).enterEvent(event)

    def leaveEvent(self, event):
        super(MyView, self).leaveEvent(event)

    def mouseReleaseEvent(self, event):
        super(MyView, self).mouseReleaseEvent(event)
        # self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        # self.viewport().setCursor(QtCore.Qt.ArrowCursor)

    def keyPressEvent(self, event):
        try:
            selItems = [] # self.scene.selectedItems()
            if len(selItems) > 0 :
                if event.key == QtCore.Qt.Key_Delete:
                    for item in selItems:
                        self.removeItem.emit(item)
        except Exception as err:
            print(err)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            print("accept")
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        pass

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            self.addDroppedItem.emit(event.mimeData(), event.pos(), self.scene())
            #  self.scene.clearSelection()

    def wheelEvent(self, event):
        try:
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                sceneRect = self.mapToScene(self.rect()).boundingRect()
                maxSize = max(sceneRect.height(), sceneRect.width())
                minPos = min(sceneRect.x(), sceneRect.y())
                if minPos > MIN_POS and maxSize < MAX_SIZE:
                    factor = 0.8
                    self._zoom -= 1
                else:
                    factor = 1
            self.scale(factor, factor)
        except Exception as err:
            print(err)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    exec = NewWindow(None)
    exec.show()
    sys.exit(app.exec_())