import datetime
import typing

from borb.pdf import Alignment
from borb.pdf import ConnectedShape
from borb.pdf import Document
from borb.pdf import FixedColumnWidthTable
from borb.pdf import HexColor
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf import Paragraph
from borb.pdf import PDF
from borb.pdf import Image
from borb.pdf import OrderedList
from borb.pdf import FlexibleColumnWidthTable

import pandas as pd
import PIL as pl

from decimal import Decimal

from borb.pdf import Table
from borb.pdf import TableCell
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.remote_go_to_annotation import RemoteGoToAnnotation

COMMONDAYS = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}


def _build_pdf_front_cover_page(d: Document,
                                zip_code: str,
                                year: int) -> None:
    """
    This function is called to build the cover Page of the PDF
    :param d:   the PDF to which the cover page can be added
    :return:    None
    """

    page: Page = Page()
    d.add_page(page)

    # draw shape 1
    ZERO: Decimal = Decimal(0)
    W: Decimal = page.get_page_info().get_width()  # width of paper
    H: Decimal = page.get_page_info().get_height()  # height of paper
    W70: Decimal = Decimal(0.70) * W  # width of our large triangle
    H87: Decimal = Decimal(0.87) * H  # height of our large triangle
    ConnectedShape(
        points=[(ZERO, H - H87), (ZERO, H), (W70, H)],
        fill_color=HexColor("#FDF0E6"),
        stroke_color=HexColor("#FDF0E6"),
    ).paint(page, Rectangle(ZERO, ZERO, W, H))

    # define a helper function
    # this function returns the y-coordinate for every x-coordinate on the longest side of the triangle
    # this is useful because all our other shapes will have a few coordinates in common with this side
    # being able to easily calculate a point on this side of the triangle is really going to help us out
    y_coordinate: typing.Callable[[Decimal], Decimal] = lambda x: Decimal(109.46) + Decimal(1.7588) * x

    # shape 2
    W20: Decimal = Decimal(0.20) * W70
    W40: Decimal = Decimal(0.40) * W70
    W60: Decimal = Decimal(0.60) * W70
    ConnectedShape(
        points=[
            (W20, y_coordinate(W20)),
            (W40, y_coordinate(W40)),
            (W20, y_coordinate(W60)),
            (ZERO, y_coordinate(W40)),
        ],
        fill_color=HexColor("#5F7367"),
        stroke_color=HexColor("#5F7367"),
        vertical_alignment=Alignment.BOTTOM,
    ).paint(page, Rectangle(ZERO, y_coordinate(W20), W, H))

    # shape 3
    ConnectedShape(
        points=[
            (W40, y_coordinate(W40)),
            (W60, y_coordinate(W60)),
            (W20, y_coordinate(W60)),
        ],
        fill_color=HexColor("#B07BAC"),
        stroke_color=HexColor("#B07BAC"),
        vertical_alignment=Alignment.BOTTOM,
    ).paint(page, Rectangle(W20, y_coordinate(W40), W, H))

    # shape 4
    W80: Decimal = Decimal(0.8) * W70
    ConnectedShape(
        points=[
            (W60, y_coordinate(W60)),
            (W60 + W20 * 2, y_coordinate(W60)),
            (W80 + W20 * 2, y_coordinate(W80)),
            (W80, y_coordinate(W80)),
        ],
        fill_color=HexColor("#5F7367"),
        stroke_color=HexColor("#5F7367"),
        vertical_alignment=Alignment.BOTTOM,
    ).paint(page, Rectangle(W60, y_coordinate(W60), W, H))

    # shape 5
    ConnectedShape(
        points=[
            (W80, y_coordinate(W80)),
            (W80 + W20 * 2, y_coordinate(W80)),
            (W + W20 * 2, y_coordinate(W)),
            (W, y_coordinate(W)),
        ],
        fill_color=HexColor("#FF7F11"),
        stroke_color=HexColor("#FF7F11"),
        vertical_alignment=Alignment.BOTTOM,
    ).paint(page, Rectangle(W80, y_coordinate(W80), W, H))

    # first paragraph
    p0: Paragraph = Paragraph(
        "Temperature Quilt",
        font_size=Decimal(20),
        font_color=HexColor("#B07BAC")
    )

    # second paragraph
    p1: Paragraph = Paragraph(
        datetime.datetime.now().strftime("%m/%d/%Y"),
        font_size=Decimal(12),
    )

    # third paragraph
    p2: Paragraph = Paragraph(
        f"This temperature quilt was made for zip-code {zip_code}, based on data from {year}."
        "The pattern was written by Heather Ann Dye, more information can be found at www.heatheranndye.com.",
        font_size=Decimal(8),
    )

    table: Table = (
        FixedColumnWidthTable(number_of_columns=1, number_of_rows=3)
        .add(p0)
        .add(p1)
        .add(p2)
        .no_borders()
    )

    # paint
    HORIZONTAL_MARGIN: Decimal = Decimal(0.06) * W
    VERTICAL_MARGIN: Decimal = Decimal(0.06) * H
    table.paint(
        page,
        Rectangle(
            HORIZONTAL_MARGIN,
            VERTICAL_MARGIN,
            W * Decimal(0.4) - HORIZONTAL_MARGIN * Decimal(2),
            H - VERTICAL_MARGIN * Decimal(2),
        ),
    )

def borb_pattern(
    year: int,
    zip_code: str,
    local_image: pl.Image,
    count: pd.DataFrame,
    levels: pd.DataFrame,
):
    # create Document
    doc: Document = Document()

    # cover
    _build_pdf_front_cover_page(doc,
                                zip_code=zip_code,
                                year=year)

    # create Page
    page1: Page = Page()

    # add Page to Document
    doc.add_page(page1)

    # set a PageLayout
    layout: SingleColumnLayout = SingleColumnLayout(page1)

    # requirements
    layout.add(Paragraph("1. Requirements", font="Helvetica-bold", font_color=HexColor("#B07BAC"), font_size=Decimal(14)))
    layout.add(Paragraph("One yard of background fabric and a range of 15 colors for this quilt", font_size=Decimal(10)))

    # background fabric cuts
    layout.add(Paragraph("1.1 Background Fabric Cuts", font="Helvetica-bold", font_color=HexColor("#B07BAC"), font_size=Decimal(12)))
    layout.add(
        OrderedList()
        .add(Paragraph("(2) 3.5 by 27.5 inch rectangles - top and bottom border", font_size=Decimal(10)))
        .add(Paragraph("(2) 2.5 by 31.5 inch rectangles - side borders", font_size=Decimal(10)))
        .add(Paragraph("(11) 1.5 by 31.5 inch strips for inner borders", font_size=Decimal(10)))
    )

    # temperature fabric
    layout.add(Paragraph("1.2 Temperature Fabric", font="Helvetica-bold", font_color=HexColor("#B07BAC"), font_size=Decimal(12)))
    layout.add(Paragraph("The range of colors, piece counts, and "
        "temperatures are given in the list "
        "below. Each day is "
        "represented by a 1 inch finished "
        "square. Cut a 1.5 inch square for"
        " each piece.", font_size=Decimal(10)))
    layout.add(Paragraph("The background color is white in the diagram.", font_size=Decimal(10)))

    # table containing the count for each color
    table1: FlexibleColumnWidthTable = FlexibleColumnWidthTable(number_of_columns=5,
                                                                number_of_rows=17,
                                                                horizontal_alignment=Alignment.CENTERED)
    table1.add(TableCell(Paragraph("Code",  font="Helvetica-bold", font_size=Decimal(10)), background_color=HexColor("f0f0f0")))
    table1.add(TableCell(Paragraph("Color", font="Helvetica-bold", font_size=Decimal(10)), background_color=HexColor("f0f0f0")))
    table1.add(TableCell(Paragraph("Count", font="Helvetica-bold", font_size=Decimal(10)), background_color=HexColor("f0f0f0")))
    table1.add(TableCell(Paragraph("Celcius", font="Helvetica-bold", font_size=Decimal(10)), background_color=HexColor("f0f0f0")))
    table1.add(TableCell(Paragraph("Fahrenheit", font="Helvetica-bold", font_size=Decimal(10)), background_color=HexColor("f0f0f0")))
    for x in range(16):
        table1.add(Paragraph(f"{count.iloc[x, 0]}", font_size=Decimal(10)))
        table1.add(Paragraph(f"{count.iloc[x, 1]}", font_size=Decimal(10)))
        table1.add(Paragraph(f"{count.iloc[x, 2]}", font_size=Decimal(10)))
        table1.add(Paragraph(f"{count.iloc[x, 3]}", font_size=Decimal(10)))
        table1.add(Paragraph(f"{count.iloc[x, 4]}", font_size=Decimal(10)))
    table1.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2),Decimal(2),)
    layout.add(table1)

    # add a Paragraph
    layout.switch_to_next_page()
    layout.add(Paragraph("2. Temperature Quilt", font="Helvetica-bold", font_color=HexColor("#B07BAC"), font_size=Decimal(12)))
    table2: FlexibleColumnWidthTable = FlexibleColumnWidthTable(number_of_columns=13,
                                                                number_of_rows=32,
                                                                horizontal_alignment=Alignment.CENTERED)
    table2.add(TableCell(Paragraph("Month",  font="Helvetica-bold", font_size=Decimal(10)), background_color=HexColor("f0f0f0")))
    for ix in range(12):
        table2.add(TableCell(Paragraph(f"{ix + 1 }",  font="Helvetica-bold", font_size=Decimal(10)), background_color=HexColor("f0f0f0")))
    for i in range(len(levels)):
        table2.add(TableCell(Paragraph(f"Day {i+1}",  font="Helvetica-bold", font_size=Decimal(10)), background_color=HexColor("f0f0f0")))
        for j in range(12):
            table2.add(Paragraph(str(int(levels.iloc[i,j])), font_size=Decimal(10)))
    table2.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2),)
    layout.add(table2)

    # set a PageLayout
    layout.switch_to_next_page()
    layout.add(Paragraph("2. Layout Diagram", font="Helvetica-bold", font_color=HexColor("#B07BAC"), font_size=Decimal(12)))
    if local_image is not None:
        layout.add(Image(local_image, horizontal_alignment=Alignment.CENTERED))

    # store
    with open("output.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)
    return doc


# if __name__ == "__main__":
#  main()
