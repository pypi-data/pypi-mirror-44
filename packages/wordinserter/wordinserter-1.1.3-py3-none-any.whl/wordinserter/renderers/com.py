import warnings
from contextlib import contextmanager
from decimal import Decimal

import webcolors

from . import BaseRenderer, renders
from ..operations import (BaseList, Bold, BulletList, CodeBlock, Footnote,
                          Format, Group, Heading, HyperLink, Image, InlineCode,
                          Italic, LineBreak, ListElement, NumberedList,
                          Paragraph, Span, Style, Table, TableCell, TableRow,
                          Text, UnderLine)

WORD_WDCOLORINDEX_MAPPING = {
    'lightgreen': 'wdBrightGreen',
    'darkblue': 'wdDarkBlue',
    'darkred': 'wdDarkRed',
    'grey': 'wdGray50',
    'silver': 'wdGray25',
}


class WordFormatter(object):
    @staticmethod
    def style_to_highlight_wdcolor(value, constants):
        try:
            name = webcolors.hex_to_name(value).lower() if value.startswith("#") else value.lower()
            if name in WORD_WDCOLORINDEX_MAPPING:
                return getattr(constants, WORD_WDCOLORINDEX_MAPPING[name])
            # Try and get the color from the wdColors enumeration
            return getattr(constants, "wd" + name.capitalize())
        except (AttributeError, ValueError):
            return None

    @staticmethod
    def rgbstring_to_hex(value):
        """
        Transform a string like rgb(199,12,15) into a wdColor format used by word
        :param value: A string like rgb(int,int,int)
        :return: An integer representation that Word understands
        """
        left, right = value.find("("), value.find(")")
        values = value[left + 1:right].split(",")
        rgblist = [int(v.strip()) for v in values]
        return webcolors.rgb_to_hex(rgblist)

    @staticmethod
    def hex_to_wdcolor(value):
        """
        Receive a HEX color attribute string like '#9bbb59' (or '9bbb59') and transform it to a numeric constant
        in order to use it as a Selection.Font.Color attribute (as an item of WdColor enumeration)
        :param value: A HEX color attribute
        :return: A numeric WDCOLOR value
        """
        rgbstrlst = webcolors.hex_to_rgb(value)
        return int(rgbstrlst[0]) + 0x100 * int(rgbstrlst[1]) + 0x10000 * int(rgbstrlst[2])

    @staticmethod
    def style_to_wdcolor(value):
        if value == 'none':
            return None

        try:
            if value.startswith('rgb('):
                value = WordFormatter.rgbstring_to_hex(value)
            elif value in webcolors.css3_names_to_hex:
                value = webcolors.css3_names_to_hex[value]

            return WordFormatter.hex_to_wdcolor(value)
        except Exception:
            return None

    @staticmethod
    def size_to_points(css_value):
        """
        Transform a pixel string into points (used by word).

        :param css_value: string optionally ending in px/pt
        :return: an integer point representation
        """
        if isinstance(css_value, str):
            is_pt = css_value.endswith('pt')
            if css_value.endswith("px") or is_pt:
                css_value = css_value[:-2]

            try:
                css_value = float(css_value)
            except ValueError:
                return None

            if is_pt:
                # Return pt sizes directly, no rounding or multiplication.
                return css_value

            css_value = round(css_value)

        return css_value * 0.75


class COMRenderer(BaseRenderer):
    def __init__(self, document, constants, range=None, debug=False, hooks=None):
        self.word = document.Application
        self.document = document
        self.constants = constants
        self._format_stack = None

        if range is not None:
            range.Select()

        super().__init__(debug, hooks)

    @property
    def selection(self):
        return self.document.ActiveWindow.Selection

    def range(self, start=None, end=None):
        if not (start or end):
            raise RuntimeError("Start and End are both None!")

        if start is None:
            start = end
        elif end is None:
            end = start

        return self.document.Range(Start=start, End=end)

    @contextmanager
    def get_range(self):
        rng = self.selection.Range.Duplicate
        try:
            yield rng
        finally:
            rng.SetRange(rng.Start, self.selection.End)

    @renders(Footnote)
    def footnote(self, op: Footnote):
        rng = self.selection.Range
        content = op.attributes['data-content']
        footnote = self.document.Footnotes.Add(rng)
        footnote.Range.Text = content

        new_range = self.range(rng.Start + 1, rng.End + 1)
        new_range.select()

    @renders(Span)
    def span(self, op: Span):
        yield

    @renders(Heading)
    def heading(self, op: Heading):
        with self.style(Style(name="Heading {0}".format(op.level), attributes=op.original_attributes)):
            yield self.new_operations(op.children)

    @renders(Style)
    def style(self, op: Style):
        # old_style = self.selection.Style
        self.selection.Style = self.document.Styles(op.name)
        with self.get_range() as rng:
            yield
        self.selection.TypeParagraph()

        if op.id:
            # Insert a bookmark
            self.document.Bookmarks.Add(str(op.id), rng)

    @renders(Bold)
    def bold(self, op: Bold):
        self.selection.BoldRun()
        yield
        self.selection.BoldRun()

    @renders(Italic)
    def italic(self, op: Italic):
        self.selection.ItalicRun()
        yield
        self.selection.ItalicRun()

    @renders(UnderLine)
    def underline(self, op: UnderLine):
        self.selection.Font.Underline = self.constants.wdUnderlineSingle
        yield
        self.selection.Font.Underline = self.constants.wdUnderlineNone

    @renders(Text)
    def text(self, op: Text):
        self.selection.TypeText(op.text)

    @renders(LineBreak)
    def linebreak(self, op: LineBreak):
        if op.format.page_break_after == "always":
            self.selection.InsertBreak(self.constants.wdPageBreak)
        elif isinstance(op.parent, Paragraph) or isinstance(op.parent, Group) and op.parent.is_root_group:
            self.selection.TypeParagraph()

    @renders(Paragraph)
    def paragraph(self, op: Paragraph):
        previous_style = None
        if op.has_child(LineBreak):
            previous_style = self.selection.Style
            self.selection.Style = self.document.Styles("No Spacing")

        yield

        if previous_style is not None:
            self.selection.Style = previous_style

        should_do_newline = True

        if op.has_children and isinstance(op[-1], (BaseList, Image, Table)):
            should_do_newline = False

        if isinstance(op.parent, (ListElement, TableCell)) and op.parent[-1] is op:
            # If our parent is a ListElement and our operation is the last one of it's children then we don't need to
            # add a newline.
            should_do_newline = False

        if should_do_newline:
            self.selection.TypeParagraph()

    @renders(InlineCode)
    def inline_code(self, op: InlineCode):
        previous_style = self.selection.Style
        previous_font_name, previous_font_size = self.selection.Font.Name, self.selection.Font.Size
        self.selection.Font.Name = "Courier New"
        yield
        self.selection.Style = previous_style
        self.selection.Font.Name = previous_font_name

    @renders(CodeBlock)
    def code_block(self, op: CodeBlock):
        self.selection.Style = self.document.Styles("No Spacing")
        self.selection.Font.Name = "Courier New"

        new_operations = op.highlighted_operations() if op.highlight else None

        with self.get_range() as rng:
            if new_operations:
                yield self.new_operations(new_operations)
            else:
                yield

        rng.NoProofing = True
        self.selection.ParagraphFormat.SpaceAfter = 8
        self.selection.TypeParagraph()
        self.selection.ClearFormatting()

    @renders(Image)
    def image(self, op: Image):
        location, height, width = op.get_image_path_and_dimensions()

        rng = self.selection

        try:
            image = rng.InlineShapes.AddPicture(FileName=location, SaveWithDocument=True)
        except Exception:
            location, height, width = op.get_404_image_and_dimensions()
            image = rng.InlineShapes.AddPicture(FileName=location, SaveWithDocument=True)

        if height:
            image.Height = height * 0.75

        if width:
            image.Width = width * 0.75

        if op.caption:
            self.selection.TypeParagraph()
            self.selection.Range.Style = self.document.Styles("caption")
            self.selection.TypeText(op.caption)

        op.render.image = image

        if not isinstance(op.parent, TableCell):
            self.selection.TypeParagraph()

    @renders(HyperLink)
    def hyperlink(self, op: HyperLink):
        with self.get_range() as rng:
            yield
        # Inserting a hyperlink that contains different styles can reset the style. IE:
        # Link<Bold<Text>> Text
        # Bold will turn bold off, but link will reset it meaning the second Text is bold.
        # Here we just reset the style after making the hyperlink.
        style = self.selection.Style

        if op.location.startswith('#'):
            self.document.Hyperlinks.Add(Anchor=rng, TextToDisplay="", SubAddress=op.location.replace('#', '', 1))
        elif op.location.startswith('!') or op.location.startswith('@'):
            if op.location.startswith('!'):
                text = "REF {} \h \* charformat".format(op.location.replace('!', '', 1))
            else:
                text = op.location.replace('@', '', 1)
                code = text.split(' ')[0]
                # Whitelist field codes
                if code not in {'FILENAME', 'STYLEREF'}:
                    return

            field = self.document.Fields.Add(
                Range=rng,
                Type=self.constants.wdFieldEmpty,
                Text=text,
                PreserveFormatting=False
            )
            # When inserting fields, the cursor stays at the beginning, select it and move the cursor to escape from it
            field.Result.Select()
            self.selection.MoveRight()
        else:
            self.document.Hyperlinks.Add(Anchor=rng, Address=op.location[:2048])  # Prevent out of memory error
        self.selection.Collapse(Direction=self.constants.wdCollapseEnd)
        self.selection.Style = style

    def _get_constants_for_list(self, op: BaseList):
        if isinstance(op, NumberedList):
            gallery_type, list_types = self.constants.wdNumberGallery, self.constants.wdListSimpleNumbering
        elif isinstance(op, BulletList):
            gallery_type, list_types = self.constants.wdBulletGallery, self.constants.wdListBullet
        else:
            raise RuntimeError("Unknown list type {0}".format(op.__class__.__name__))

        return gallery_type, list_types

    @renders(BulletList, NumberedList)
    def render_list(self, op):
        list_level = op.depth + 1
        first_list = list_level == 1

        gallery_type, list_types = self._get_constants_for_list(op)
        gallery = self.word.ListGalleries(gallery_type)
        template = gallery.ListTemplates(1)

        if op.type:
            style_values = {
                'roman-lowercase': self.constants.wdListNumberStyleLowercaseRoman,
                'roman-uppercase': self.constants.wdListNumberStyleUppercaseRoman
            }
            if op.type in style_values:
                value = style_values[op.type]
                for list_template in gallery.ListTemplates:
                    if list_template.ListLevels(1).NumberStyle == value:
                        template = list_template
                        break
                else:
                    warnings.warn('Unable to locate list style for {0}, using default'.format(op.type))

        if first_list:
            self.selection.Range.ListFormat.ApplyListTemplateWithLevel(
                ListTemplate=template,
                ContinuePreviousList=False,
                DefaultListBehavior=self.constants.wdWord10ListBehavior
            )

            if op.format.style:
                self._apply_style_to_range(op.format)
        else:
            self.selection.Range.ListFormat.ListIndent()

        yield

        if self.selection.Range.ListFormat.ListType != list_types:
            self.selection.Range.ListFormat.ApplyListTemplateWithLevel(
                ListTemplate=template,
                ContinuePreviousList=True,
                DefaultListBehavior=self.constants.wdWord10ListBehavior,
                ApplyLevel=list_level,
                ApplyTo=self.constants.wdListApplyToWholeList
            )

        if first_list:
            self.selection.Range.ListFormat.RemoveNumbers(NumberType=self.constants.wdNumberParagraph)
            self.selection.Style = self.constants.wdStyleNormal
        else:
            self.selection.Range.ListFormat.ListOutdent()

    @renders(ListElement)
    def list_element(self, op: ListElement):
        yield
        self.selection.TypeParagraph()

    @renders(Table)
    def table(self, op: Table):
        table_range = self.selection.Range
        self.selection.TypeParagraph()

        if isinstance(op.parent, TableCell):
            # There appears to be a bug in Word. If you are in a table cell and add a new table
            # then it appears to only add one row. We get around this by adding a new paragraph, then using that
            # range to insert. This ends up with an unrequested space/margin, but it's better than nothing.
            self.selection.Range.Select()
            table_range = self.selection.Range
            self.selection.TypeParagraph()

        end_range = self.selection.Range

        rows, columns = op.dimensions

        table = self.selection.Tables.Add(
            table_range,
            NumRows=rows,
            NumColumns=columns,
            AutoFitBehavior=self.constants.wdAutoFitFixed
        )
        table.Style = "Table Grid"
        table.AllowAutoFit = True

        table.Borders.Enable = 0 if op.border == '0' else 1

        # This code is super super slow, running list() on a Cells collection takes >15 seconds.
        # https://github.com/enthought/comtypes/issues/107

        # cell_mapping = [
        #    list(row.Cells) for row in table.Rows
        #    ]

        # This code is faster, but not as nice :(
        cell_mapping = [
            [row.Cells(i + 1) for i in range(len(row.Cells))]
            for row in list(table.Rows)
        ]

        processed_cells = set()
        has_rowspan = False

        # Handling merged cells is a bitch. We do it by finding the max dimensions of the table (the max sum of all
        # colspans in a row) then creating a table with those dimensions.
        # We then enumerate through each cell in each row, and find the corresponding word cell (the actual table cell)

        for row_index, row in enumerate(op):
            # Store the row object for later use. This cannot be used if the table has vertically merged cells
            row.render.row_object = table.Rows(row_index+1) if not has_rowspan else None

            # Loop through each row and extract the corresponding Row object from Word
            row_cells = cell_mapping[row_index]

            for column_index, cell in enumerate(row):
                # For each cell/column in our row extract the table cell from Word
                word_cell = row_cells[column_index]

                if word_cell is None or word_cell in processed_cells:
                    # Skip forward and find the next unprocessed cell
                    for possible_cell in row_cells[column_index:]:
                        if possible_cell is not None and possible_cell not in processed_cells:
                            word_cell = possible_cell
                            column_index = row_cells.index(word_cell)
                            break

                if cell.colspan > 1:
                    # If the cell has a colspan of more than 1 we need to get the 0-indexed
                    # column index (colspans are 1-indexed)
                    colspan_index = cell.colspan - 1
                    # If we want to merge from column 0 to column 3, we take the current column index and add the
                    # 0-indexed colspan index then merge all the cells up to that point.
                    word_cell.Merge(MergeTo=row_cells[column_index + colspan_index])
                    # We need to clear any 'dead' cells from our array. We delete all of the cells we have merged
                    # leaving the first one ('cell'), which is our merged cell.
                    del row_cells[column_index + 1:column_index + cell.colspan]

                if cell.rowspan > 1:
                    # If the cell has a rowspan things get tricky.
                    has_rowspan = True
                    if cell.colspan > 1:
                        # If it's got a colspan we need to go down the rows below it and merge those cells into
                        # a single cell, pretty much the same as above.
                        for idx in range(row_index + 1, row_index + cell.rowspan):
                            colspan_cell = cell_mapping[idx][column_index]
                            next_cell = cell_mapping[idx][column_index + (cell.colspan - 1)]
                            colspan_cell.Merge(MergeTo=next_cell)

                    # We merge the multi-cells together
                    word_cell.Merge(MergeTo=cell_mapping[row_index + cell.rowspan - 1][column_index])

                    # And go down and delete all merged cells below. We set them to None so the size of the rows
                    # is still uniform.
                    for idx in range(row_index + 1, row_index + cell.rowspan):
                        slice_length = len(cell_mapping[idx][column_index:column_index + cell.colspan or 0])
                        cell_mapping[idx][column_index:column_index + cell.colspan or 0] = (None for _ in
                                                                                            range(slice_length))

                # Store the cell object for later use
                cell.render.cell_object = word_cell
                processed_cells.add(word_cell)

        # Store the table object for later use
        op.render.table = table

        table_width, unit = op.width

        if table_width:
            width_type_map = {
                '%': self.constants.wdPreferredWidthPercent,
                'pt': self.constants.wdPreferredWidthPoints,
            }

            if unit == '%':
                table_width = max(0, min(table_width, 100))

            table.PreferredWidthType = width_type_map[unit]
            table.PreferredWidth = table_width

            for row_child in op.children:
                for cell_child in row_child.children:
                    cell_width, unit = cell_child.width

                    if cell_width is not None:
                        cell_o = cell_child.render.cell_object
                        cell_o.PreferredWidthType = width_type_map[unit]
                        cell_o.PreferredWidth = cell_width


            table.AllowAutoFit = False

        table.Select()
        yield
        end_range.Select()

    @renders(TableRow)
    def table_row(self, op):
        yield

    @renders(TableCell)
    def table_cell(self, op: TableCell):
        rng = op.render.cell_object.Range
        rng.Collapse()
        rng.Select()
        yield

        if op.orientation:
            # ToDo: Move this to the Format handling. It is specific to a table cell though
            mapping = {
                'sideways-lr': 'wdTextOrientationUpward',
                'sideways-rl': 'wdTextOrientationDownward',
            }
            if op.orientation in mapping:
                op.render.cell_object.Range.Orientation = getattr(self.constants, mapping[op.orientation])

    def _apply_style_to_range(self, op, rng=None):
        rng = rng or self.selection.Range

        for klass in op.style or []:
            try:
                rng.Style = klass
            except Exception:
                warnings.warn("Unable to apply style name '{0}'".format(klass))

    def render_operation(self, operation, *args, **kwargs):
        if operation.format is not None \
                and operation.format.has_format() \
                and operation.format.__class__ in self.render_methods:
            format_func = self.collect_format_data
        else:
            format_func = self.ignored_element

        if 'format_list' in kwargs:
            format_list = kwargs.pop('format_list')
        else:
            format_list = self._format_stack

        child_format_list = []

        with format_func(operation.format, operation, format_list):
            super().render_operation(operation, *args, format_list=child_format_list, **kwargs)

        if child_format_list:
            format_list.append(child_format_list)

    def render(self, *args, **kwargs):
        self._format_stack = []

        super().render(*args, **kwargs)
        self.apply_recursive_formatting(self._format_stack)
        self._format_stack = None

    @renders(Format)
    def collect_format_data(self, op, parent_operation, format_stack):
        with self.get_range() as rng:
            yield

        if not op.has_style:
            return

        format_stack.append((op, parent_operation, rng))

    def apply_recursive_formatting(self, stack):
        for item in stack:
            if isinstance(item, tuple):
                with self.with_hooks(*item):
                    self.handle_format(*item)
            else:
                self.apply_recursive_formatting(item)

    def handle_format(self, op, parent_operation, element_range):
        # should_type_x = op.should_use_x_hack

        # Why TypeText('X')? Styles seem to overrun their containers (especially when they span an entire line). This
        # adds a buffer to the end of the element, which is removed at the end. This is the least horrible way to do
        # this, trust us.
        # if should_type_x:
        #    self.selection.TypeText("X")

        if isinstance(parent_operation, TableCell):
            element_range = parent_operation.render.cell_object.Range

        if op.style and not isinstance(parent_operation, BaseList):
            self._apply_style_to_range(op, element_range)

        if op.font_size:
            size = WordFormatter.size_to_points(op.font_size)
            if size:
                element_range.Font.Size = size

        if op.color:
            col = WordFormatter.style_to_wdcolor(op.color)
            if col:
                element_range.Font.Color = col

        if op.text_decoration == "underline":
            element_range.Font.UnderlineColor = self.constants.wdColorAutomatic
            element_range.Font.Underline = self.constants.wdUnderlineSingle

        if op.margin:
            if op.margin["left"] == "auto" and op.margin["right"] == "auto":
                if not isinstance(parent_operation, Table):
                    # We don't want to center a table.
                    element_range.ParagraphFormat.Alignment = self.constants.wdAlignParagraphCenter

            if op.margin["left"] != 'auto':
                if isinstance(parent_operation, Table):
                    parent_operation.render.table.Rows.LeftIndent = WordFormatter.size_to_points(op.margin["left"])

        if op.background:
            background = op.background.split(" ")[0]
            # This needs refactoring :/
            if isinstance(parent_operation, Table):
                bg_color = WordFormatter.style_to_wdcolor(background)
                if bg_color:
                    parent_operation.render.table.Shading.BackgroundPatternColor = bg_color
            elif isinstance(parent_operation, TableCell):
                bg_color = WordFormatter.style_to_wdcolor(background)
                if bg_color:
                    parent_operation.render.cell_object.Shading.BackgroundPatternColor = bg_color
            else:
                if op.display == 'block':
                    # If it's a block element with a background then we set the Shading.BackgroundPatternColor
                    bg_color = WordFormatter.style_to_wdcolor(background)
                    if bg_color:
                        element_range.Shading.BackgroundPatternColor = bg_color
                else:
                    bg_color = WordFormatter.style_to_highlight_wdcolor(background, self.constants)
                    if bg_color:
                        element_range.HighlightColorIndex = bg_color

        if op.vertical_align:
            if isinstance(parent_operation, TableCell):
                alignment = {
                    'top': self.constants.wdCellAlignVerticalTop,
                    'middle': self.constants.wdCellAlignVerticalCenter,
                    'bottom': self.constants.wdCellAlignVerticalBottom
                }
                if op.vertical_align in alignment:
                    parent_operation.render.cell_object.VerticalAlignment = alignment[op.vertical_align]

        if op.text_align:
            alignment = {
                'center': self.constants.wdAlignParagraphCenter,
                'left': self.constants.wdAlignParagraphLeft,
                'right': self.constants.wdAlignParagraphRight
            }

            if op.text_align in alignment:
                element_range.ParagraphFormat.Alignment = alignment[op.text_align]

        if op.writing_mode:
            orientations = {"vertical-lr": 1, "sideways-lr": 2}
            if isinstance(parent_operation, TableCell):
                orientation = orientations.get(op.writing_mode)
                if orientation is not None:
                    parent_operation.render.cell_object.Range.Orientation = orientation

        if op.border:
            if isinstance(parent_operation, Image):
                img = parent_operation.render.image
                img.Line.Visible = True

                if op.border["style"]:
                    style = op.border["style"]
                    constants = {
                        "solid": self.constants.msoLineSolid,
                    }

                    if style in constants:
                        img.Line.DashStyle = constants[style]

                if op.border["width"]:
                    width = WordFormatter.size_to_points(op.border["width"])
                    if width:
                        img.Line.Weight = width

                if op.border["color"]:
                    color = WordFormatter.style_to_wdcolor(op.border["color"])
                    if color:
                        img.Line.ForeColor.RGB = color

            if isinstance(parent_operation, (Table, TableRow, TableCell)):
                edges = {
                    "bottom": self.constants.wdBorderBottom,
                    "top":  self.constants.wdBorderTop,
                    "left": self.constants.wdBorderLeft,
                    "right": self.constants.wdBorderRight,
                }

                # TODO: Support individual border-left, border-right, border-top and border-bottom properties
                borders = {edge: element_range.Borders(constant) for edge, constant in edges.items()}

                if op.border["style"]:
                    style = op.border["style"]
                    constants = {
                        "none": self.constants.wdLineStyleNone,
                        "solid": self.constants.wdLineStyleSingle,
                        "dotted": self.constants.wdLineStyleDot,
                        "dashed": self.constants.wdLineStyleDashSmallGap,
                        "double": self.constants.wdLineStyleDouble,
                        "inset": self.constants.wdLineStyleInset,
                        "outset": self.constants.wdLineStyleOutset,
                        "initial": self.word.Options.DefaultBorderLineStyle,
                    }

                    if style in constants:
                        for border in borders.values():
                            border.LineStyle = constants[style]

                if op.border["width"]:
                    width = WordFormatter.size_to_points(op.border["width"])
                    # Numbers? Where we are going we don't need numbers
                    constants = {
                        0.25: self.constants.wdLineWidth025pt,
                        0.5: self.constants.wdLineWidth050pt,
                        0.75: self.constants.wdLineWidth075pt,
                        1: self.constants.wdLineWidth100pt,
                        1.5: self.constants.wdLineWidth150pt,
                        2.25: self.constants.wdLineWidth225pt,
                        3: self.constants.wdLineWidth300pt,
                        4.5: self.constants.wdLineWidth450pt,
                        6: self.constants.wdLineWidth600pt,
                    }
                    if width in constants:
                        for border in borders.values():
                            border.LineWidth = constants[width]

                if op.border["color"]:
                    color = WordFormatter.style_to_wdcolor(op.border["color"])
                    if color:
                        for border in borders.values():
                            border.Color = color

        if op.padding:
            if op.padding['top']:
                px = WordFormatter.size_to_points(op.padding['top'])
                if px is not None:
                    if isinstance(parent_operation, Table):
                        parent_operation.render.table.TopPadding = px
                    elif isinstance(parent_operation, TableCell):
                        parent_operation.render.cell_object.TopPadding = px
                    else:
                        element_range.ParagraphFormat.SpaceBefore = px

            if op.padding['bottom']:
                px = WordFormatter.size_to_points(op.padding['bottom'])
                if px is not None:
                    if isinstance(parent_operation, Table):
                        parent_operation.render.table.BottomPadding = px
                    elif isinstance(parent_operation, TableCell):
                        parent_operation.render.cell_object.BottomPadding = px
                    else:
                        element_range.ParagraphFormat.SpaceAfter = px

            if op.padding['left']:
                px = WordFormatter.size_to_points(op.padding['left'])
                if px is not None:
                    if isinstance(parent_operation, Table):
                        parent_operation.render.table.LeftPadding = px
                    elif isinstance(parent_operation, TableCell):
                        parent_operation.render.cell_object.LeftPadding = px

            if op.padding['right']:
                px = WordFormatter.size_to_points(op.padding['right'])
                if px is not None:
                    if isinstance(parent_operation, Table):
                        parent_operation.render.table.RightPadding = px
                    elif isinstance(parent_operation, TableCell):
                        parent_operation.render.cell_object.RightPadding = px

        if op.line_height:
            if op.line_height.isdecimal():
                points = self.word.LinesToPoints(Decimal(op.line_height))
            elif op.line_height.strip().endswith('%'):
                points = self.word.LinesToPoints(Decimal(op.line_height.split('%')[0]) / 100)
            else:
                points = WordFormatter.size_to_points(op.line_height)
            element_range.ParagraphFormat.LineSpacing = points
