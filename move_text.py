from sublime import Region, status_message
from sublime_plugin import TextCommand


def move_text_horiz(view, edit, direction):
    for region in view.sel():
        if region.empty():
            continue

        orig_region = region
        if region.a > region.b:
            region = Region(region.b, region.a)

        sel_region = Region(region.a + direction, region.b + direction)
        if sel_region.a < 0 or sel_region.b >= view.size():
            continue

        if direction < 0:
            dest_region = Region(region.a + direction, region.b)
            substitute = view.substr(region) + view.substr(Region(region.a + direction, region.a))
        else:
            dest_region = Region(region.a, region.b + direction)
            substitute = view.substr(Region(region.b, region.b + direction)) + view.substr(region)

        # Remove selection from RegionSet
        view.sel().subtract(orig_region)
        # Replace the selection with transformed text
        view.replace(edit, dest_region, substitute)
        # Add the new selection
        view.sel().add(sel_region)


class MoveTextLeftCommand(TextCommand):
    def run(self, edit):
        e = self.view.begin_edit('move_text_horiz')
        move_text_horiz(self.view, edit, -1)
        self.view.end_edit(e)


class MoveTextRightCommand(TextCommand):
    def run(self, edit):
        e = self.view.begin_edit('move_text_horiz')
        move_text_horiz(self.view, edit, 1)
        self.view.end_edit(e)


def move_text_vert(view, edit, direction):
    for region in view.sel():
        if region.empty():
            continue

        orig_region = region
        if region.a > region.b:
            region = Region(region.b, region.a)

        # calculate number of characters to the left
        (row, col) = view.rowcol(region.a)
        dest_row = row + direction

        if direction < 0 and dest_row < 0 or \
           direction > 0 and dest_row >= view.rowcol(view.size())[0]:
            continue
        # starting at the destination row, count off "col" characters
        point = view.text_point(dest_row, 0)
        #
        # it's possible that there aren't enough characters in the destination row,
        # so try and advance the column until we end up on the wrong row
        dest_col = 0
        while view.rowcol(point + 1)[0] == dest_row and view.rowcol(point + 1)[1] <= col:
            print view.rowcol(point + 1)
            point += 1

        # status_message(str(point))

        substitute = view.substr(region)
        if direction > 0:
            point -= len(substitute)
        insert_region = Region(point, point)
        sel_region = Region(point, point + len(substitute))

        view.sel().subtract(orig_region)
        view.replace(edit, region, '')
        view.replace(edit, insert_region, substitute)
        view.sel().add(sel_region)


class MoveTextUpCommand(TextCommand):
    def run(self, edit):
        e = self.view.begin_edit('move_text_vert')
        move_text_vert(self.view, edit, -1)
        self.view.end_edit(e)


class MoveTextDownCommand(TextCommand):
    def run(self, edit):
        e = self.view.begin_edit('move_text_vert')
        move_text_vert(self.view, edit, 1)
        self.view.end_edit(e)
