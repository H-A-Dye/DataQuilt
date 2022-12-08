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


from decimal import Decimal
from pathlib import Path
from collections import defaultdict

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


def colorlist():
    local_dict = defaultdict(int)
    for i in range(15):
        local_dict[str(i)] = 10
    return local_dict


def color_table():
    x = [[str(i * j) for i in range(10)] for j in range(10)]
    return x


def main():
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
    layout.add(
        Image(
            Path("MinisAreForME.jpg"),
            width=Decimal(128),
            height=Decimal(128),
        )
    )

    layout.add(Paragraph("Background Fabric"))
    layout.add(
        OrderedList()
        .add(
            Paragraph(
                "(2) 3.5 by 27.5 inch rectangles - top ",
                "and bottom border",
            )
        )
        .add(Paragraph("(2) 2.5 by 31.5 inch rectangles - side borders"))
        .add(Paragraph("(11) 1.5 by 31.5 inch strips for inner borders"))
        .add(Paragraph("(10) 1.5 by 1.5 inch squares"))
    )
    color_count = colorlist()
    layout.add(Paragraph("Temperature Fabric"))

    square_list: OrderedList = OrderedList()
    for (val, count) in enumerate(color_count):
        square_list.add(Paragraph(f"{color_count.get(str(val))} squares"))
    layout.add(square_list)

    # create Page
    page2: Page = Page()

    # add Page to Document
    doc.add_page(page2)

    # set a PageLayout
    layout2: PageLayout = SingleColumnLayout(page2)

    # add a Paragraph
    layout2.add(Paragraph("Temperature Quilt"))
    flex_table: FlexibleColumnWidthTable = FlexibleColumnWidthTable(
        number_of_columns=13, number_of_rows=32
    )
    flex_table.add(Paragraph("Month"))
    for ix in range(12):
        flex_table.add(Paragraph(f"{ix + 1 }"))

    layout2.add(flex_table)

    # store
    with open("output1.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)
    return doc


if __name__ == "__main__":
    main()
