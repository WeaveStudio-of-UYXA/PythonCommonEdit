"""
# CEPainter
## CommonEdit Project (Python)
## Author: TsingYayin Org: WeaveStudio of UYXA
此部分代码为CommonEdit库的一部分，由TsingYayin开发，属WeaveStudio管理\n
此部分代码为针对Qt中部分绘图相关控件的再次封装，此部分以LGPL-3.0协议开源，不与CommonEdit项目的其他部分代码共享协议\n
注意，虽然此部分代码以LGPL-3.0协议开源，但不意味着TsingYayin放弃对此部分代码的所有权，此部分代码的所有权仍归属WeaveStudio\n
"""
from PySide2.QtCore import *
from PySide2.QtGui import *
from typing import *
from enum import *

class CEColorBandName(Enum):
    RedYelGre = 0
    RedYelGre_I = 1
    RedOraYelGre = 10
    RedOraYelGre_I = 11
    RedOraYelGreBlu = 20
    RedOraYelGreBlu_I = 21

class CEColorBand(QObject):
    ColorBand:List[QColor]
    NumericalBand:List[float]
    def setColorBand(this, band:List[QColor]):
        """
        设置颜色带\n
        颜色带中可以包含任意多的颜色，但是颜色必须按对应值从小到大的顺序排列\n
        有关不同具体值尝试使用哪个颜色，请参阅和调用`setNumericalBand`\n
        """
        this.ColorBand = band

    def setNumericalBand(this, band:List[float]):
        """
        设置数值带\n
        数值带中应该包含 `颜色带中所设置的颜色数量减一` 个数值\n
        并且按从小到大的顺序排列\n
        即设置颜色带中每个颜色的分界值\n
        """
        this.NumericalBand = band

    def testValue(this, value:float)->QColor:
        """
        测试一个值所对应的颜色\n
        `value`要测试的值\n
        """
        if (value < this.NumericalBand[0]):
            return this.ColorBand[0]
        if (value > this.NumericalBand[-1]):
            return this.ColorBand[-1]
        for i in range(len(this.NumericalBand)):
            if (value < this.NumericalBand[i]):
                return this.ColorBand[i]
        return this.ColorBand[-1]

    def getRibbonLegendPlot(this, width:int, height:int, margin:int = 5)->QImage:
        """
        获取一个用于绘制颜色带的图像，此图像可以用于绘制图例\n
        目前此图像提供一个自下而上的垂直色带并在其右侧绘制数值带，暂不支持其他排版\n
        `width`图像的宽度\n
        `height`图像的高度\n
        `margin`图像的边距\n
        """
        rtn = QImage(width, height, QImage.Format_ARGB32)
        rtn.fill(Qt.white)
        painter = QPainter(rtn)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 2))
        text_width = 45
        painter.drawRect(margin, margin, width-margin*2-text_width, height-margin*2)
        x_available = width-margin*2 - text_width - 2
        y_available = height-margin*2 - 2
        y_step = y_available/len(this.ColorBand)
        j = len(this.ColorBand)
        for i in range(j):
            painter.setPen(QPen(this.ColorBand[i]))
            painter.setBrush(QBrush(this.ColorBand[i]))
            painter.drawRect(margin+1, margin+1+y_step*(j - i - 1), x_available, y_step)
        painter.setFont(QFont("Microsoft YaHei", 10))
        painter.setPen(QPen(Qt.black, 2))
        for i in range(j-1):
            painter.drawText(margin+x_available+3, margin+1+y_step*(j - i - 1) - y_step/2, text_width, y_step, Qt.AlignCenter, str(this.NumericalBand[i]))
        return rtn
    
    def useDefaultColorBand(this, bandName:CEColorBandName):
        """
        使用默认的颜色带
        """
        if (bandName == CEColorBandName.RedYelGre):
            this.ColorBand = [QColor(255, 0, 0), QColor(255, 255, 0), QColor(0, 255, 0)]
        elif (bandName == CEColorBandName.RedYelGre_I):
            this.ColorBand = [QColor(0, 255, 0), QColor(255, 255, 0), QColor(255, 0, 0)]
        elif (bandName == CEColorBandName.RedOraYelGre):
            this.ColorBand = [QColor(255, 0, 0), QColor(255, 128, 0), QColor(255, 255, 0), QColor(0, 255, 0)]
        elif (bandName == CEColorBandName.RedOraYelGre_I):
            this.ColorBand = [QColor(0, 255, 0), QColor(255, 255, 0), QColor(255, 128, 0), QColor(255, 0, 0)]
        elif (bandName == CEColorBandName.RedOraYelGreBlu):
            this.ColorBand = [QColor(255, 0, 0), QColor(255, 128, 0), QColor(255, 255, 0), QColor(0, 255, 0), QColor(0, 0, 255)]
        elif (bandName == CEColorBandName.RedOraYelGreBlu_I):
            this.ColorBand = [QColor(0, 0, 255), QColor(0, 255, 0), QColor(255, 255, 0), QColor(255, 128, 0), QColor(255, 0, 0)]
    
class CECircularContourPlotter(QObject):
    ColorBand:CEColorBand
    def __init__(this, parent:QObject = None):
        super().__init__(parent)

    def setCEColorBand(this, band:CEColorBand):
        this.ColorBand = band

    def setNumericalBand(this, band:List[float]):
        """
        设置数值带\n
        `band`数值带，列表中的每个元素为一个数值，列表中的元素个数应与颜色带中的颜色个数相同\n
        # 此函数应该在setCEColorBand之后调用
        """
        this.ColorBand.setNumericalBand(band)

    def getContourPlot(this, contour:Dict, width, margin:int = 5)->QImage:
        """
        获取一个用于绘制等值线的图像\n
        向函数提供由等值线半径和其对应的值组成的字典，函数将返回一个正方形的图像\n
        此图中各环着色根据等值线的值在预先设置的CEColorBand中的测试结果进行着色，图像的中心为原点\n
        关于CEColorBand的测试结果，参见`CEColorBand.testValue`\n
        `contour`等值线的字典，键为等值线的半径，值为等值线的值\n
        `margin`图像的边距\n
        """
        testPointList = sorted(contour.keys())
        rawMax = testPointList[-1]
        rtn = QImage(width+margin*2,width+margin*2, QImage.Format_ARGB32)
        rtn.fill(Qt.transparent)
        center = QPoint(int(rtn.width()/2)+1, int(rtn.width()/2)+1)
        painter = QPainter(rtn)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(QFont("Microsoft YaHei", 10))
        for i in testPointList:
            painter.setPen(QPen(this.ColorBand.testValue(contour[i]), 3))
            paintRadius = i/rawMax * width/2
            painter.drawEllipse(center, paintRadius, paintRadius)
        painter.setPen(QPen(Qt.black, width*0.05))
        for i in testPointList:
            paintRadius = i/rawMax * width/2
            painter.drawText(center.x()+paintRadius/1.414 - 20, center.y()+paintRadius/1.414 - 20, 100, 20, Qt.AlignLeft, str(i)+"m: "+str(contour[i]))
        return rtn
    