from typing import List
import reflex as rx

def table_header_cell(title: str):
    return rx.table.column_header_cell(title)

def summary_table_header(columns: List[str]):
    return rx.table.header(
            rx.table.row(
                rx.foreach(
                    columns, table_header_cell
                )
                #rx.table.column_header_cell("Country"),
                #rx.table.column_header_cell("Source"),
                #rx.table.column_header_cell("Companies"),
                #rx.table.column_header_cell("Individuals"),
                #rx.table.column_header_cell("Links")
            ),
        )

def summary_table_row(row: List[str]):
    """Show table row."""
    return rx.table.row(
        rx.table.cell(row[0]),
        rx.table.cell(row[1]),
        rx.table.cell(row[2]),
        rx.table.cell(row[3]),
        rx.table.cell(rx.link(f"Search {row[1]}", href=row[4])),
    )

def summary_table(columns: List[str], rows: List[List[str]]):
    return rx.table.root(
        summary_table_header(columns),
        rx.table.body(
            rx.foreach(
                rows, summary_table_row
            )
        ),
        width="100%",
    )
