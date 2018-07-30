from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import numpy as np


class MyView(pg.GraphicsView):
    def __init__(self, parent, sig, *args, **kwargs):
        pg.setConfigOption('foreground', 'k')
        pg.setConfigOption('background', 'w')
        super(MyView, self).__init__(*args, **kwargs)
        self._sig = sig
        plot = MyPlotItem(self)
        self.addItem(plot)
        plot.setPos(100, 100)
    # def resizeEvent(self, ev):
    #     print("resize item")
    #     super(MyPlotItem, self).resizeEvent(ev)
    #
    #
    # def mouseDoubleClickEvent(self, event):
    #     print("item double click")
    #     super(MyPlotItem, self).mouseDoubleClickEvent(event)
    #     event.accept()
    #
    #     if self._slctFrame:
    #         # self.getViewWidget().removeItem(self._slctFrame)
    #         self._slctFrame = None
    #         self.getViewBox().setBackgroundColor(None)
    #
    #     else:
    #         geo = self.viewGeometry().getCoords()
    #         h = geo[2] - geo[0]
    #         w = geo[3] - geo[1]
    #
    #         self.getViewBox().setBackgroundColor('g')
    #         try :
    #             """
    #             Create handle
    #             """
    #             s = +8.0
    #             b = self.boundingRect()
    #             print(self.boundingRect())
    #             # self._handle = QtCore.QRectF(b.right() - s,b.bottom() - s,s,s)
    #             print(QtCore.QRectF(b.right() - s,b.bottom() - s,s,s))
    #
    #             handle = QtWidgets.QGraphicsEllipseItem(QtCore.QRectF(b.right(),b.bottom(),5,5))
    #             handle.setPen(pg.mkPen(width=5, color='b'))
    #             self.addItem(handle)
    #
    #         except Exception as err:
    #             print(err)
    #         self._slctFrame = True
    #
    # def mousePressEvent(self, event):
    #     print("item mouse press")
    #     super(MyPlotItem, self).mousePressEvent(event)
    #
    # def mouseMoveEvent(self, event):
    #     print("item mouse move")
    #     super(MyPlotItem, self).mouseMoveEvent(event)
    #
    # def mouseReleaseEvent(self, event):
    #     print("item mouse release")
    #     super(MyPlotItem, self).mouseReleaseEvent(event)
    #
    # def hoverLeaveEvent(self, event):
    #     print("item mouse hover Leave")
    #     super(MyPlotItem, self).hoverLeaveEvent(event)
    #
    # def hoverMoveEvent(self, event):
    #     print("item mouse hover Move")
    #     super(MyPlotItem, self).hoverMoveEvent(event)
    #
    # def mouseDragEvent(self, event):
    #     print("item mouse drag")
    #     # if self._selected:
    #     #     event.accept()
    #     # else:
    #     #     # super(MyPlotItem, self).mouseDragEvent(event)
    #     #     pass
    #

class MyPlotItem(pg.PlotItem):
    def __init__(self, parent,  *args, **kwargs):
        super(MyPlotItem, self).__init__(*args, **kwargs)
        self.setAcceptHoverEvents(False)
        self.showGrid(True, True, 0.8)
        self.setFixedHeight(300)
        self.setFixedWidth(300)
        self.add_scatter()

    def add_scatter(self):
        scatter = pg.ScatterPlotItem(pen=pg.mkPen(width=5, color='r'), symbol='o', size=1)
        n = 1000
        data = np.random.normal(size=(2, n))
        pos = [{'pos': data[:, i]} for i in range(n)]
        scatter.setData(pos)
        self.addItem(scatter)

    def draw_marker(self):
        rect = QtWidgets.QGraphicsRectItem(*self.pos(), self.width(), self.height())
        rect.setPen(pg.mkPen(width=1, color='b',style=QtCore.Qt.DashLine))
        self.getViewWidget().addItem(rect)

        x0 = self.pos()[0] + self.width()
        y0 = self.pos()[1] + self.height()

        ploy = QtGui.QPolygonF()
        ploy.append(QtCore.QPointF(x0,y0))
        ploy.append(QtCore.QPointF(x0-10,y0))
        ploy.append(QtCore.QPointF(x0,y0-10))
        tri = QtWidgets.QGraphicsPolygonItem(ploy)
        tri.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
        self.getViewWidget().addItem(tri)