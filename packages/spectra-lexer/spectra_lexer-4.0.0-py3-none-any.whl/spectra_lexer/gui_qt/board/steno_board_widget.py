from typing import Callable, Dict, Iterable, List

from PyQt5.QtCore import QRectF, QXmlStreamReader
from PyQt5.QtGui import QPainter, QPaintEvent
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QWidget


class StenoBoardWidget(QWidget):
    """ Widget to display all the keys that make up a steno stroke pictorally. """

    _gfx_board: QSvgRenderer                     # Main renderer of SVG steno board graphics.
    _draw_list: List[tuple] = []                 # List of graphical element IDs with bounds rects.
    _bounds: Dict[str, tuple] = {}               # (x, y, w, h) bounds of each graphical element by id.
    resize_callback: Callable[..., None] = None  # Callback to send board size changes to the main component.

    def __init__(self, *args):
        super().__init__(*args)
        self._gfx_board = QSvgRenderer()

    def set_xml(self, xml_text:str, ids:Iterable[str]) -> None:
        """ Load the board graphics from an SVG XML string. Send a resize event at the end to update the main component.
            Compute and store a dict of bounds for all given element IDs, as well as the top-level viewbox. """
        self._gfx_board.load(QXmlStreamReader(xml_text))
        self._bounds = {k: self._gfx_board.boundsOnElement(k).getRect() for k in ids}
        self.resizeEvent()

    def set_layout(self, elements:Iterable[tuple]) -> None:
        """ Set the current list of element ids and bound rects and draw the new elements. """
        self._draw_list = []
        bounds = self._bounds
        for (e_id, ox, oy, scale) in elements:
            if e_id in bounds:
                x, y, w, h = [c * scale for c in bounds[e_id]]
                rectf = QRectF(x + ox, y + oy, w, h)
                self._draw_list.append((e_id, rectf))
        self.update()

    def paintEvent(self, event:QPaintEvent) -> None:
        """ Display the current steno key set on the board diagram when GUI repaint occurs.
            Undefined elements are simply ignored. """
        p = QPainter(self)
        render = self._gfx_board.render
        for (e_id, rectf) in self._draw_list:
            render(p, e_id, rectf)

    def resizeEvent(self, *args) -> None:
        """ Send new properties of the board widget on any size change. """
        if self.resize_callback is not None:
            self.resize_callback(self._gfx_board.viewBox().getRect(), self.width(), self.height())
