from PySide2.QtCore import *
from PySide2.QtWidgets import *

desktop = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)


def askOpenFile(title: str, nameFilter='*'):
    s = QSettings()

    d = QFileDialog(None, title, s.value('Last' + title, defaultValue=desktop))
    d.setAcceptMode(QFileDialog.AcceptOpen)
    d.setFileMode(QFileDialog.ExistingFile)
    d.setViewMode(QFileDialog.Detail)
    d.setFilter(QDir.AllEntries | QDir.NoSymLinks | QDir.NoDotAndDotDot)
    d.setNameFilter(nameFilter)

    if d.exec_() != QDialog.Accepted or len(d.selectedFiles()) < 1:
        return None

    s.setValue('Last' + title, d.selectedFiles()[0])
    return d.selectedFiles()[0]


def askSaveFile(title: str, suffix='*', nameFilter=None):
    s = QSettings()

    d = QFileDialog(None, title, s.value('Last' + title, defaultValue=desktop))
    d.setAcceptMode(QFileDialog.AcceptSave)
    d.setFileMode(QFileDialog.AnyFile)
    d.setViewMode(QFileDialog.Detail)
    d.setFilter(QDir.AllEntries | QDir.NoSymLinks | QDir.NoDotAndDotDot)
    d.setDefaultSuffix(suffix)
    d.setNameFilter(nameFilter)

    if nameFilter is None:
        d.setNameFilter(suffix)

    if d.exec_() != QDialog.Accepted or len(d.selectedFiles()) < 1:
        return None

    s.setValue('Last' + title, d.selectedFiles()[0])
    return d.selectedFiles()[0]


def askOpenFiles(title: str):
    s = QSettings()

    d = QFileDialog(None, title, s.value('Last' + title, defaultValue=desktop))
    d.setAcceptMode(QFileDialog.AcceptOpen)
    d.setFileMode(QFileDialog.ExistingFiles)
    d.setViewMode(QFileDialog.Detail)
    d.setFilter(QDir.AllEntries | QDir.NoSymLinks | QDir.NoDotAndDotDot)

    if d.exec_() != QDialog.Accepted or len(d.selectedFiles()) < 1:
        return None

    s.setValue('Last' + title, QFileInfo(d.selectedFiles()[0]).absolutePath())
    return d.selectedFiles()


def askDirectory(title: str):
    s = QSettings()

    d = QFileDialog(None, title, s.value('Last' + title, defaultValue=desktop))
    d.setAcceptMode(QFileDialog.AcceptOpen)
    d.setFileMode(QFileDialog.Directory)
    d.setViewMode(QFileDialog.Detail)
    d.setFilter(QDir.AllEntries | QDir.NoSymLinks | QDir.NoDotAndDotDot)

    if d.exec_() != QDialog.Accepted or len(d.selectedFiles()) < 1:
        return None

    s.setValue('Last' + title, d.selectedFiles()[0])
    return d.selectedFiles()[0]


def askSeries(title: str, series):
    items = [str(i) for i in series]

    dialog = QDialog()
    dialog.setWindowTitle(title)
    dialog.setLayout(QVBoxLayout())

    def tabCloseRequested(i):
        del items[i]
        tabs.removeTab(i)

    tabs = QTabWidget(dialog)
    tabs.setTabsClosable(True)
    tabs.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
    tabs.tabCloseRequested.connect(tabCloseRequested)

    for i in items:
        label = QLabel(text=i)
        tabs.addTab(label, str(tabs.count() + 1))

    button = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
    button.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
    button.accepted.connect(dialog.accept)
    button.rejected.connect(dialog.reject)

    dialog.layout().addWidget(tabs)
    dialog.layout().addWidget(button)

    if dialog.exec_() == QDialog.Accepted:
        if 0 <= tabs.currentIndex() < len(series):
            return series[tabs.currentIndex()]
    return None


def info(text: str, title: str = '提示 (info)'):
    QMessageBox.information(None, title, text)
