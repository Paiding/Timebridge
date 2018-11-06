#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class welcomePage(QMainWindow):
    

    close_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):  
        self.setWindowTitle('时光桥牌')
        #设置窗口的图标，引用当前目录下的time.png图片
        self.setWindowIcon(QIcon('time.png'))        
        self.setGeometry(300, 300, 600, 600) 

        self.btn = QToolButton(self)
        self.btn.setText("开始游戏")
        self.btn.resize(100, 60)
        self.btn.move(250, 400)
        self.show()

    def closeEvent(self, event):
        #是否确认退出
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
 
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class TimeBridgeGUI(QWidget):
    def __init__(self, parent=None):
        super(TimeBridgeGUI, self).__init__(parent)
        #坐标指示器
        grid = QGridLayout()
        x = 0
        y = 0
        
        self.text = "x: {0},  y: {1}".format(x, y)
        #self.setMouseTracking(True)
        self.label = QLabel(self.text, self)
        grid.addWidget(self.label, 0, 0, Qt.AlignTop)
        self.setLayout(grid)
        
        self.resize(800, 700)
        #self.setStyleSheet("background: black")

    #配合highlight_quest使用
    quest_state_0 = 0
    quest_state_1 = 0
    quest_state_2 = 0

    def mousePressEvent(self, e):
        
        x = int((e.x()-200)/80) 
        y = int((e.y()-180)/48) 
        
        text = "x: {0},  y: {1}".format(x, y)
        self.label.setText(text)

        if (e.x() >= 200 and e.x() <= 600) and (e.y() >=180 and e.y() <= 520):
        	quest_state_0 = 10 * y + x

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_player_area(qp)
        qp.end()

    def draw_player_area(self, qp):
      
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(col)
		#基础区域
        qp.setBrush(QColor(180, 180, 180))
        qp.drawRect(200, 0, 400, 91)
        qp.drawRect(371.5, 93, 57, 87)
        qp.drawRect(371.5, 520, 57, 87)
        qp.drawRect(200, 609, 400, 91)
        qp.drawRect(0, 150, 91, 400)
        qp.drawRect(709, 150, 91, 400)
        qp.drawRect(100, 306.5, 57, 87)
        qp.drawRect(643, 306.5, 57, 87)
        #叫牌区域
        qp.drawRect(200, 180, 400, 340)
        qp.setPen(pen)
        qp.drawLine(200, 228, 600, 228)
        qp.drawLine(200, 276, 600, 276)
        qp.drawLine(200, 324, 600, 324)
        qp.drawLine(200, 372, 600, 372)
        qp.drawLine(200, 420, 600, 420)
        qp.drawLine(200, 468, 600, 468)
        qp.drawLine(200, 516, 600, 516)
        qp.drawLine(280, 180, 280, 520)
        qp.drawLine(360, 180, 360, 520)
        qp.drawLine(440, 180, 440, 520)
        qp.drawLine(520, 180, 520, 520)

    def bid_map(xb, yb):
    #将叫牌区格位映射到坐标
    	return (80 * x + 200, 48 * y + 180, 80, 48)

    def bid_update(self, BidPlayer, BidResult):
    	xb = BidResult % 10
    	yb = BidResult / 10
    	qp = QPainter()
    	qp.begin(self)
    	qp.setBrush(Qcolor(BidPlayer * 20, 100 + BidPlayer * 10, 230 - BidPlayer * 15))#皮这一下就很开心
    	qp.drawRect(bid_map(xb, yb))
    	qp.setBrush(Qcolor(200, 200, 200))#把失效区域涂灰
    	for x in range(0, 4):
    		for y in range(0, 6):
    			if (y < yb or (y == yb and x < xb)):
    				qp.drawRect(bid_map(x, y))

    def highlight_quest(self, area):
        if area == 0:
            return self.quest_state_0
   
    def handle_click(self):
        if not self.isVisible():
            self.show()

    def handle_close(self):
        self.close()
        
if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = welcomePage()
    s = TimeBridgeGUI()
    ex.btn.clicked.connect(s.handle_click)
    ex.btn.clicked.connect(ex.hide)
    ex.close_signal.connect(ex.close)
    ex.show()
    sys.exit(App.exec_())