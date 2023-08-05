"""
Utilities to create widgets
"""

__all__ = [
    'Dialog',
]

import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QLayout, QSizePolicy, QWidget)

from madgui.util.layout import HBoxLayout, VBoxLayout, Stretch
from madgui.util.qt import present

# short-hands:
Button = QDialogButtonBox


def perpendicular(orientation):
    """Get perpendicular orientation."""
    return (Qt.Horizontal | Qt.Vertical) ^ orientation


def expand(widget, orientation):
    """Expand widget in specified direction."""
    policy = widget.sizePolicy()
    if orientation == Qt.Horizontal:
        policy.setHorizontalPolicy(QSizePolicy.Minimum)
    else:
        policy.setVerticalPolicy(QSizePolicy.Minimum)
    widget.setSizePolicy(policy)


class SerializeButtons(QDialogButtonBox):

    """
    :ivar QWidget widget: the content area widget
    :ivar str folder: folder for exports/imports
    """

    def __init__(self, widget, folder, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = widget
        self.folder = folder
        self.addButton(Button.Open).clicked.connect(self.onImport)
        self.addButton(Button.Save).clicked.connect(self.onExport)
        self.addButton(Button.Ok).clicked.connect(self.onAccept)
        self.button(Button.Open).setAutoDefault(False)
        self.button(Button.Save).setAutoDefault(False)
        self.button(Button.Ok).setDefault(True)
        expand(self, perpendicular(self.orientation()))

    def updateButtons(self):
        self.button(Button.Save).setEnabled(
            hasattr(self.exporter, 'exportTo'))
        self.button(Button.Open).setEnabled(
            hasattr(self.exporter, 'importFrom') and
            not getattr(self.exporter, 'readonly', None))

    @property
    def exporter(self):
        return getattr(self.widget, 'exporter', None)

    def onImport(self):
        """Import data from JSON/YAML file."""
        from madgui.widget.filedialog import getOpenFileName
        filename = getOpenFileName(
            self.window(), 'Import values', self.folder,
            self.exporter.importFilters)
        if filename:
            self.exporter.importFrom(filename)
            self.folder, _ = os.path.split(filename)

    def onExport(self):
        """Export data to YAML file."""
        from madgui.widget.filedialog import getSaveFileName
        filename = getSaveFileName(
            self.window(), 'Export values', self.folder,
            self.exporter.exportFilters)
        if filename:
            self.exporter.exportTo(filename)
            self.folder, _ = os.path.split(filename)

    def onAccept(self):
        self.window().accept()


class Dialog(QDialog):

    # TODO: reset button

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizeGripEnabled(True)
        self.finished.connect(self.close)

    def setWidget(self, widget, tight=False):
        self._widget = widget
        if isinstance(widget, list):
            layout = VBoxLayout(widget)
        elif isinstance(widget, QLayout):
            layout = widget
        elif isinstance(widget, QWidget):
            layout = VBoxLayout([widget])
        else:
            raise NotImplementedError
        if tight:
            layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def widget(self):
        return self._widget

    # TODO: update enabled-state of apply-button?

    def closeEvent(self, event):
        # send closeEvent to children!
        if isinstance(self.widget(), QWidget):
            self.widget().close()
        super().close()

    def setExportWidget(self, widget, folder):
        self.serious = SerializeButtons(widget, folder, Qt.Vertical)
        self.serious.addButton(Button.Cancel).clicked.connect(self.reject)
        self.setWidget(HBoxLayout([widget, [
            Stretch(),
            self.serious,
        ]]))

    def setSimpleExportWidget(self, widget, folder):
        self.serious = SerializeButtons(widget, folder, Qt.Horizontal)
        self.setWidget(VBoxLayout([widget, self.serious]))

    present = present
