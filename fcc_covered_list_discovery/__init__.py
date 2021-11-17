from abc import ABC


class AbstractCell(ABC):
    pass


class StringCell(AbstractCell):
    def __init__(self, text):
        self.text = str(text) if text is not None else ""


class NumberCell(AbstractCell):
    def __init__(self, number):
        self.number = number


class HyperLinkCell(AbstractCell):
    def __init__(self, url, label):
        self.label = label
        self.url = url


class ReportBuilder(ABC):
    # interface of our class
    def create(self, file_name: str):
        raise NotImplementedError()

    def header(self, headers_labels) -> int:
        raise NotImplementedError()

    def write(self, col, row, cell: AbstractCell):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()
