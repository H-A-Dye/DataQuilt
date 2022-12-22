from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from borb.pdf import Paragraph
from borb.pdf import PDF

from borb.pdf import Image
from borb.pdf import OrderedList

# from borb.pdf import TableUtil
from borb.pdf import FlexibleColumnWidthTable
import pandas as pd

import PIL as pl

from decimal import Decimal


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


def borb_pattern(
    local_image: pl.Image,
    count: pd.DataFrame,
    levels: pd.DataFrame,
):
    # create Document
    doc: Document = Document()

    # create Page
    page1: Page = Page()

    # add Page to Document
    doc.add_page(page1)

    # set a PageLayout
    layout: PageLayout = SingleColumnLayout(page1)

    # add a Paragraph
    layout.add(Paragraph("Temperature Quilt"))

    layout.add(
        Paragraph(
            "You'll need a yard of background fabric",
            "and a range of 15 colors for this quilt",
        )
    )

    layout.add(Paragraph("Background Fabric"))
    layout.add(
        OrderedList()
        .add(
            Paragraph(
                "(2) 3.5 by 27.5 inch rectangles - top " + "and bottom border",
            )
        )
        .add(Paragraph("(2) 2.5 by 31.5 inch rectangles - side borders"))
        .add(Paragraph("(11) 1.5 by 31.5 inch strips for inner borders"))
    )

    layout.add(Paragraph("Temperature Fabric"))
    intro = (
        "The range of colors, piece counts, and "
        "temperatures are given in the list "
        "below. "
    )
    layout.add(Paragraph(intro))
    background_exp = "The background color is white in " "the diagram."
    layout.add(Paragraph(background_exp))

    flex_table1: FlexibleColumnWidthTable = FlexibleColumnWidthTable(
        number_of_columns=5,
        number_of_rows=17,
    )
    flex_table1.add(Paragraph("Code"))
    flex_table1.add(Paragraph("Color"))
    flex_table1.add(Paragraph("Count"))
    flex_table1.add(Paragraph("Celsius"))
    flex_table1.add(Paragraph("Fahrenheit"))
    for x in range(16):
        flex_table1.add(Paragraph(f"{count.iloc[x, 0]}"))
        flex_table1.add(Paragraph(f"{count.iloc[x, 1]}"))
        flex_table1.add(Paragraph(f"{count.iloc[x, 2]}"))
        flex_table1.add(Paragraph(f"{count.iloc[x, 3]}"))
        flex_table1.add(Paragraph(f"{count.iloc[x, 4]}"))
    flex_table1.set_padding_on_all_cells(
        Decimal(1),
        Decimal(1),
        Decimal(1),
        Decimal(1),
    )
    layout.add(flex_table1)

    # create Page
    page2: Page = Page()

    # add Page to Document
    doc.add_page(page2)

    # set a PageLayout
    layout2: PageLayout = SingleColumnLayout(page2)

    # add a Paragraph
    layout2.add(Paragraph("Temperature Quilt"))
    flex_table: FlexibleColumnWidthTable = FlexibleColumnWidthTable(
        number_of_columns=13,
        number_of_rows=32,
    )

    flex_table.add(Paragraph("Month"))
    for ix in range(12):
        flex_table.add(Paragraph(f"{ix + 1 }"))
    for i in range(len(levels)):
        flex_table.add(Paragraph(f"Day {i+1}"))
        for j in range(12):
            flex_table.add(Paragraph(f"{levels.iloc[i,j]}"))
    flex_table.set_padding_on_all_cells(
        Decimal(1),
        Decimal(1),
        Decimal(1),
        Decimal(1),
    )
    layout2.add(flex_table)

    # add Page to Document

    # create Page
    page3: Page = Page()

    doc.add_page(page3)

    # set a PageLayout
    layout3: PageLayout = SingleColumnLayout(page3)
    layout3.add(Paragraph("Layout Diagram"))
    layout3.add(Image(local_image))

    # store
    with open("output.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)
    return doc


# if __name__ == "__main__":
#  main()
