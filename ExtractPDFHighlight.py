from typing import List, Tuple

import fitz  # install with 'pip install pymupdf'
import pandas as pd
import re

def _parse_highlight(annot: fitz.Annot, wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
    points = annot.vertices
    quad_count = int(len(points) / 4)
    sentences = []
    for i in range(quad_count):
        # where the highlighted part is
        r = fitz.Quad(points[i * 4 : i * 4 + 4]).rect
        words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
        words = sorted(words, key=lambda tup: tup[7]) #
        sentences.append(" ".join(w[4] for w in words))
    sentence = " ".join(sentences)
    sentence = sentence.replace(' ', '')

    return sentence

def handle_page(page):
    wordlist = page.getText("words")  # list of words on page
    wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x


    highlights = []
    annot = page.firstAnnot
    while annot and annot.type == (8, 'Highlight'):
        if annot.type[0] == 8:
            highlights.append(_parse_highlight(annot, wordlist))
        annot = annot.next
    return highlights


def main(filepath: str) -> List:
    doc = fitz.open(filepath)
    highlights = []
    for page in doc:
        highlights += handle_page(page)
    highlighted_text = ["".join(i.split(" ")) for i in highlights]  # adds a comma in place of spaces
    highlighted_text_ = []
    for i in range(len(highlighted_text)):
        flag = 0
        for j in range(len(highlighted_text)):
            if i != j and highlighted_text[i] in highlighted_text[j]:
                flag = 1
        if flag == 0:
            highlighted_text_.append(highlighted_text[i])
    for item in highlighted_text_:
        print(item)


if __name__ == "__main__":
    (main("tests/美好置业集团股份有限公司 2020 年年度报告.PDF"))

