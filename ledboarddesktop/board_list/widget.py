from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QListWidgetItem, QListWidget

from ledboardlib import ListedBoard

from ledboarddesktop.board_list.listed_board_widget import ListedBoardWidget
from ledboarddesktop.components import Components


class BoardListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._widgets: list[ListedBoardWidget] = []

        Components().board_detector.boardsPolled.connect(self.set_boards)
        Components().board_detector.boardChanged.connect(self._board_changed)

    def selected_board(self) -> ListedBoard:
        return self.itemWidget(self.selectedItems()[0]).board if self.selectedItems() else None

    @Slot()
    def set_boards(self, boards: list[ListedBoard]):
        print("list set_boards", boards)
        selected_board = self.selected_board()

        self.setUpdatesEnabled(False)
        self.blockSignals(True)

        self.clear()
        self._widgets.clear()

        for board in boards:
            widget = ListedBoardWidget(board)
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

    def _board_changed(self, board: ListedBoard):
        if self.selected_board() is None:
            return

        if self.selected_board().serial_port_name == board.serial_port_name:
            self.itemSelectionChanged.emit()
