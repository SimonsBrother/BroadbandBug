# Form implementation generated from reading ui file 'addrecorder.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AddRecorder(object):
    def setupUi(self, AddRecorder):
        AddRecorder.setObjectName("AddRecorder")
        AddRecorder.resize(368, 106)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddRecorder)
        self.verticalLayout.setObjectName("verticalLayout")
        self.idHLayout = QtWidgets.QHBoxLayout()
        self.idHLayout.setObjectName("idHLayout")
        self.idLabel = QtWidgets.QLabel(parent=AddRecorder)
        self.idLabel.setObjectName("idLabel")
        self.idHLayout.addWidget(self.idLabel)
        self.idLineEdit = QtWidgets.QLineEdit(parent=AddRecorder)
        self.idLineEdit.setObjectName("idLineEdit")
        self.idHLayout.addWidget(self.idLineEdit)
        self.verticalLayout.addLayout(self.idHLayout)
        self.methodHLayout = QtWidgets.QHBoxLayout()
        self.methodHLayout.setObjectName("methodHLayout")
        self.methodLabel = QtWidgets.QLabel(parent=AddRecorder)
        self.methodLabel.setObjectName("methodLabel")
        self.methodHLayout.addWidget(self.methodLabel)
        self.methodComboBox = QtWidgets.QComboBox(parent=AddRecorder)
        self.methodComboBox.setObjectName("methodComboBox")
        self.methodHLayout.addWidget(self.methodComboBox)
        self.verticalLayout.addLayout(self.methodHLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=AddRecorder)
        self.buttonBox.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddRecorder)
        self.buttonBox.accepted.connect(AddRecorder.accept) # type: ignore
        self.buttonBox.rejected.connect(AddRecorder.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(AddRecorder)

    def retranslateUi(self, AddRecorder):
        _translate = QtCore.QCoreApplication.translate
        AddRecorder.setWindowTitle(_translate("AddRecorder", "Add a recorder"))
        self.idLabel.setText(_translate("AddRecorder", "Recorder identifier:"))
        self.idLineEdit.setText(_translate("AddRecorder", "Rec1"))
        self.methodLabel.setText(_translate("AddRecorder", "Select recording method:"))
