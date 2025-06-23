from PySide6.QtCore import Slot
from PySide6.QtWidgets import QListWidgetItem, QListWidget

from ledboardlib.listed_board import ListedBoard

from ledboarddesktop.board_list.listed_board_widget import ListedBoardWidget


class BoardListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._widgets: list[ListedBoardWidget] = []

    def selected_board(self) -> ListedBoard:
        return self.itemWidget(self.selectedItems()[0]).board if self.selectedItems() else None

    @Slot()
    def set_boards(self, listed_boards: list[ListedBoard]):
        selected_board = self.selected_board()

        self.setUpdatesEnabled(False)
        self.blockSignals(True)

        self.clear()
        self._widgets.clear()

        for listed_board in listed_boards:
            widget = ListedBoardWidget(listed_board)
            item = QListWidgetItem()
            item.setSizeHint(widget.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, widget)
            is_selected = listed_board.serial_port_name == selected_board.serial_port_name if selected_board else False
            item.setSelected(is_selected)
            self._widgets.append(widget)

        self.blockSignals(False)
        self.setUpdatesEnabled(True)

        # if selected_board and not self.selectedItems():
        #     self.itemSelectionChanged.emit()
