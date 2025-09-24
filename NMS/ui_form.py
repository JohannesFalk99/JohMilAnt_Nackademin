# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMenu, QMenuBar, QSizePolicy,
    QStatusBar, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(665, 478)
        Widget.setMinimumSize(QSize(665, 0))
        self.actionlol = QAction(Widget)
        self.actionlol.setObjectName(u"actionlol")
        self.centralwidget = QWidget(Widget)
        self.centralwidget.setObjectName(u"centralwidget")
        self.menubar = QMenuBar(Widget)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 665, 21))
        self.menuggg = QMenu(self.menubar)
        self.menuggg.setObjectName(u"menuggg")
        self.menugabf = QMenu(self.menubar)
        self.menugabf.setObjectName(u"menugabf")
        self.statusbar = QStatusBar(Widget)
        self.statusbar.setObjectName(u"statusbar")

        self.menubar.addAction(self.menuggg.menuAction())
        self.menubar.addAction(self.menugabf.menuAction())
        self.menuggg.addAction(self.actionlol)
        self.menugabf.addSeparator()

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"MainWindow", None))
        self.actionlol.setText(QCoreApplication.translate("Widget", u"lol", None))
        self.menuggg.setTitle(QCoreApplication.translate("Widget", u"ggg", None))
        self.menugabf.setTitle(QCoreApplication.translate("Widget", u"gabf", None))
    # retranslateUi

