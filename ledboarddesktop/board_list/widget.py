from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QListWidgetItem, QListWidget

from ledboardlib import ListedBoard

from ledboarddesktop.board_list.list_item_widget import BoardListItemWidget
from ledboarddesktop.components import Components


class BoardListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._widgets: list[BoardListItemWidget] = []

        board_communicator = Components().board_communicator
        board_communicator.boardChanged.connect(self._board_changed)
        board_communicator.boardDetailsAcquired.connect(lambda: self.setEnabled(True))
        board_communicator.boardDetailsAcquisitionFailed.connect(lambda: self.setEnabled(True))
        board_communicator.boardDetailsRequested.connect(lambda: self.setEnabled(False))
        board_communicator.boardsListed.connect(self.set_boards)

        self.setMinimumWidth(300)

    def board_widget(self, board: ListedBoard) -> BoardListItemWidget | None:
        for widget in self._widgets:
            if widget.board.serial_port_name == board.serial_port_name:
                return widget

        return None

    def selected_board(self) -> ListedBoard:
        return self.itemWidget(self.selectedItems()[0]).board if self.selectedItems() else None

    @Slot(list)
    def set_boards(self, boards: list[ListedBoard]):
        selected_board = self.selected_board()

        self.setUpdatesEnabled(False)
        self.blockSignals(True)

        self.clear()
        self._widgets.clear()

        for board in boards:
            widget = BoardListItemWidget(board)
            item = QListWidgetItem()
            item.setSizeHint(widget.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, widget)
            is_selected = board.serial_port_name == selected_board.serial_port_name if selected_board else False
            item.setSelected(is_selected)
            self._widgets.append(widget)

        self.blockSignals(False)
        self.setUpdatesEnabled(True)

        if selected_board and not self.selectedItems():
            self.itemSelectionChanged.emit()

    @Slot(ListedBoard)
    def _board_changed(self, board: ListedBoard):
        board_widget = self.board_widget(board)
        if board_widget is not None:
            board_widget.set_board(board)

        selected_board = self.selected_board()
        if selected_board is not None and selected_board.serial_port_name == board.serial_port_name:
            self.itemSelectionChanged.emit()
