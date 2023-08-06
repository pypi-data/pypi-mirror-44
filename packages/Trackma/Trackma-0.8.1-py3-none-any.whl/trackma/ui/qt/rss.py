# This file is part of Trackma.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

pyqt_version = 5

from datetime import date

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QDialog, QTableView, QVBoxLayout, QHBoxLayout,
    QDialogButtonBox, QAbstractItemView, QHeaderView, QPushButton,
    QLineEdit, QLabel)

from trackma.ui.qt.models import RSSTableModel
#from trackma.ui.qt.widgets import AddTableDetailsView, AddCardView

from trackma import utils

class RSSDialog(QDialog):
    def __init__(self, parent, worker):
        QDialog.__init__(self, parent)

        self.resize(950, 700)
        self.setWindowTitle('RSS Feed')
        self.worker = worker

        layout = QVBoxLayout()


        self.view = QTableView()
        m = RSSTableModel()
        proxy = QtCore.QSortFilterProxyModel()
        proxy.setSourceModel(m)
        proxy.setFilterKeyColumn(-1)
        proxy.setFilterCaseSensitivity(False)

        self.view.setGridStyle(QtCore.Qt.NoPen)
        self.view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view.setModel(proxy)

        top_layout = QHBoxLayout()
        self.refresh_btn = QPushButton('Refresh')
        self.refresh_btn.clicked.connect(lambda: self.load(refresh=True))
        self.filter = QLineEdit()
        self.filter.setClearButtonEnabled(True)
        self.filter.textChanged.connect(proxy.setFilterFixedString)
        top_layout.addWidget(self.refresh_btn)
        top_layout.addWidget(QLabel("Filter:"))
        top_layout.addWidget(self.filter)

        bottom_buttons = QDialogButtonBox()
        bottom_buttons.addButton("Cancel", QDialogButtonBox.RejectRole)
        self.download_btn = bottom_buttons.addButton("Download all checked", QDialogButtonBox.AcceptRole)
        self.download_btn.clicked.connect(self.s_download)
        self.download_btn.setEnabled(False)
        self.download_one_btn = bottom_buttons.addButton("Download selected", QDialogButtonBox.AcceptRole)
        self.download_one_btn.clicked.connect(self.s_download_one)
        self.download_one_btn.setEnabled(False)
        bottom_buttons.rejected.connect(self.close)

        layout.addLayout(top_layout)
        layout.addWidget(self.view)
        layout.addWidget(bottom_buttons)

        self.setLayout(layout)

        self.load(refresh=False)

    def _enable_widgets(self, enable):
        self.refresh_btn.setEnabled(enable)
        self.view.setEnabled(enable)
        self.download_btn.setEnabled(enable)
        self.download_one_btn.setEnabled(enable)

    def worker_call(self, function, ret_function, *args, **kwargs):
        # Run worker in a thread
        self.worker.set_function(function, ret_function, *args, **kwargs)
        self.worker.start()

    def load(self, refresh=False):
        self._enable_widgets(False)
        self.worker_call('rss_list', self.r_rss_loaded, refresh)

    def download(self, item):
        self._enable_widgets(False)
        self.worker_call('rss_download', self.r_generic, item)

    def s_download(self):
        proxy = self.view.model()
        to_download = []

        for n in range(proxy.rowCount()):
            row = proxy.mapToSource(proxy.index(n, 0)).row()
            item = proxy.sourceModel().result(row)

            if item['marked']:
                to_download.append(item)

        if to_download:
            self.download(to_download)

    def s_download_one(self):
        proxy = self.view.model()

        selected_index = self.view.selectionModel().selectedRows()[0]
        row = proxy.mapToSource(selected_index).row()
        item = proxy.sourceModel().result(row)

        self.download([item])

    def r_generic(self, result):
        self._enable_widgets(True)

    def r_rss_loaded(self, result):
        if result['success']:
            self.view.model().sourceModel().setResults(result['result'])
            self.view.resizeColumnToContents(RSSTableModel.COL_TITLE)
            self.view.resizeColumnToContents(RSSTableModel.COL_EPISODE)
            self.view.resizeColumnToContents(RSSTableModel.COL_DESCRIPTION)
            self.view.resizeRowsToContents()
            self._enable_widgets(True)
