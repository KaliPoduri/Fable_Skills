"""Source tokenizer shared by the bundled structural parsers.

One configurable lexer covers every brace-family language graphify extracts.
What varies between them -- comment markers, string delimiters, whether block
comments nest, which punctuation counts as part of an identifier -- is data in
:class:`LexSpec` rather than code.

Getting the lexer right is what makes the structural parsers above it safe: a
``{`` inside a string or comment must never be mistaken for a block opener, or
every enclosing declaration's body would be mis-scoped. Strings, comments and
raw/template literals are therefore consumed as single tokens and never
re-examined.
"""
from __future__ import annotations

__all__ = ["LexSpec", "Token", "tokenize"]

# Token kinds
IDENT = "ident"
NUMBER = "number"
STRING = "string"
COMMENT = "comment"
PUNCT = "punct"
NEWLINE = "newline"


class Token:
    """A lexed token with byte and row/column positions."""

    __slots__ = ("kind", "text", "start_byte", "end_byte", "row", "col", "end_row", "end_col")

    def __init__(self, kind, text, start_byte, end_byte, row, col, end_row, end_col):
        self.kind = kind
        self.text = text
        self.start_byte = start_byte
        self.end_byte = end_byte
        self.row = row
        self.col = col
        self.end_row = end_row
        self.end_col = end_col

    @property
    def start_point(self):
        return (self.row, self.col)

    @property
    def end_point(self):
        return (self.end_row, self.end_col)

    def __repr__(self):
        return f"Token({self.kind}, {self.text!r} @{self.row}:{self.col})"


class LexSpec:
    """Per-language lexer configuration."""

    __slots__ = (
        "line_comments",
        "block_comments",
        "nested_block_comments",
        "quotes",
        "triple_quotes",
        "ident_extra",
        "line_continuation",
        "heredocs",
    )

    def __init__(
        self,
        line_comments=("//",),
        block_comments=(("/*", "*/"),),
        nested_block_comments=False,
        quotes=('"', "'"),
        triple_quotes=(),
        ident_extra="_",
        line_continuation=False,
        heredocs=False,
    ):
        self.line_comments = tuple(line_comments)
        self.block_comments = tuple(block_comments)
        self.nested_block_comments = nested_block_comments
        self.quotes = tuple(quotes)
        self.triple_quotes = tuple(triple_quotes)
        self.ident_extra = ident_extra
        self.line_continuation = line_continuation
        self.heredocs = heredocs


def tokenize(source: bytes, spec: LexSpec) -> list:
    """Lex ``source`` into a flat token list.

    Decoding is lenient (``errors="replace"``) because graphify scans whole
    repositories and must not fail on a file with a stray non-UTF-8 byte. Byte
    offsets are tracked separately from character indices so that node positions
    stay in the byte units tree-sitter reports even when the text contains
    multi-byte characters.
    """
    text = source.decode("utf-8", errors="replace")
    tokens: list = []
    index = 0
    length = len(text)
    row = 0
    line_start_char = 0
    # Byte offset of the character at `index`, maintained incrementally.
    byte_offset = 0

    def char_bytes(segment: str) -> int:
        return len(segment.encode("utf-8"))

    def emit(kind, start_index, end_index, start_byte, start_row, start_col):
        end_row = row
        end_col = end_index - line_start_char
        tokens.append(
            Token(
                kind,
                text[start_index:end_index],
                start_byte,
                start_byte + char_bytes(text[start_index:end_index]),
                start_row,
                start_col,
                end_row,
                end_col,
            )
        )

    def advance_rows(start_index, end_index):
        """Update row/line tracking across a consumed span."""
        nonlocal row, line_start_char
        segment = text[start_index:end_index]
        newlines = segment.count("\n")
        if newlines:
            row += newlines
            line_start_char = start_index + segment.rfind("\n") + 1

    while index < length:
        char = text[index]
        start_index = index
        start_byte = byte_offset
        start_row = row
        start_col = index - line_start_char

        # ── newline ───────────────────────────────────────────────────────
        if char == "\n":
            tokens.append(Token(NEWLINE, "\n", start_byte, start_byte + 1, start_row, start_col, start_row, start_col + 1))
            index += 1
            byte_offset += 1
            row += 1
            line_start_char = index
            continue

        if char in " \t\r\f\v":
            index += 1
            byte_offset += 1
            continue

        # ── line continuation ─────────────────────────────────────────────
        if spec.line_continuation and char == "\\" and index + 1 < length and text[index + 1] == "\n":
            index += 2
            byte_offset += 2
            row += 1
            line_start_char = index
            continue

        # ── comments ──────────────────────────────────────────────────────
        matched_comment = False
        for opener, closer in spec.block_comments:
            if text.startswith(opener, index):
                depth = 1
                cursor = index + len(opener)
                while cursor < length and depth:
                    if spec.nested_block_comments and text.startswith(opener, cursor):
                        depth += 1
                        cursor += len(opener)
                    elif text.startswith(closer, cursor):
                        depth -= 1
                        cursor += len(closer)
                    else:
                        cursor += 1
                advance_rows(index, cursor)
                emit(COMMENT, start_index, cursor, start_byte, start_row, start_col)
                byte_offset += char_bytes(text[index:cursor])
                index = cursor
                matched_comment = True
                break
        if matched_comment:
            continue

        for marker in spec.line_comments:
            if text.startswith(marker, index):
                cursor = text.find("\n", index)
                cursor = length if cursor == -1 else cursor
                emit(COMMENT, start_index, cursor, start_byte, start_row, start_col)
                byte_offset += char_bytes(text[index:cursor])
                index = cursor
                matched_comment = True
                break
        if matched_comment:
            continue

        # ── strings ───────────────────────────────────────────────────────
        matched_string = False
        for quote in spec.triple_quotes:
            if text.startswith(quote, index):
                cursor = index + len(quote)
                while cursor < length:
                    if text[cursor] == "\\":
                        cursor += 2
                        continue
                    if text.startswith(quote, cursor):
                        cursor += len(quote)
                        break
                    cursor += 1
                else:
                    cursor = length
                advance_rows(index, cursor)
                emit(STRING, start_index, cursor, start_byte, start_row, start_col)
                byte_offset += char_bytes(text[index:cursor])
                index = cursor
                matched_string = True
                break
        if matched_string:
            continue

        if char in spec.quotes:
            cursor = index + 1
            while cursor < length:
                if text[cursor] == "\\":
                    cursor += 2
                    continue
                if text[cursor] == char:
                    cursor += 1
                    break
                # A newline ends a non-multiline string; template literals
                # (backtick) legitimately span lines, so they keep going.
                if text[cursor] == "\n" and char != "`":
                    break
                cursor += 1
            else:
                cursor = length
            advance_rows(index, cursor)
            emit(STRING, start_index, cursor, start_byte, start_row, start_col)
            byte_offset += char_bytes(text[index:cursor])
            index = cursor
            continue

        # ── identifiers ───────────────────────────────────────────────────
        if char.isalpha() or char in spec.ident_extra:
            cursor = index
            while cursor < length and (text[cursor].isalnum() or text[cursor] in spec.ident_extra):
                cursor += 1
            emit(IDENT, start_index, cursor, start_byte, start_row, start_col)
            byte_offset += char_bytes(text[index:cursor])
            index = cursor
            continue

        # ── numbers ───────────────────────────────────────────────────────
        if char.isdigit():
            cursor = index
            while cursor < length and (text[cursor].isalnum() or text[cursor] in "._"):
                cursor += 1
            emit(NUMBER, start_index, cursor, start_byte, start_row, start_col)
            byte_offset += char_bytes(text[index:cursor])
            index = cursor
            continue

        # ── punctuation ───────────────────────────────────────────────────
        emit(PUNCT, start_index, index + 1, start_byte, start_row, start_col)
        byte_offset += char_bytes(char)
        index += 1

    return tokens
