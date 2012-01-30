from sublime import Region
from sublime_plugin import TextCommand


class MoveTextHorizCommand(TextCommand):
    def move_text_horiz(self, edit, direction):
        for region in self.view.sel():
            if region.empty():
                continue

            orig_region = region
            sel_region = Region(region.begin() + direction, region.end() + direction)

            if sel_region.a < 0 or sel_region.b > self.view.size():
                continue

            if direction < 0:
                dest_region = Region(region.begin() + direction, region.end())
                move_text = self.view.substr(region) + self.view.substr(Region(region.begin() + direction, region.begin()))
            else:
                dest_region = Region(region.begin(), region.end() + direction)
                move_text = self.view.substr(Region(region.end(), region.end() + direction)) + self.view.substr(region)

            # Remove selection from RegionSet
            self.view.sel().subtract(orig_region)
            # Replace the selection with transformed text
            self.view.replace(edit, dest_region, move_text)
            # Add the new selection
            self.view.sel().add(sel_region)


class MoveTextLeftCommand(MoveTextHorizCommand):
    def run(self, edit):
        e = self.view.begin_edit('move_text_horiz')
        self.move_text_horiz(edit, -1)
        self.view.end_edit(e)


class MoveTextRightCommand(MoveTextHorizCommand):
    def run(self, edit):
        e = self.view.begin_edit('move_text_horiz')
        self.move_text_horiz(edit, 1)
        self.view.end_edit(e)


class MoveTextVertCommand(TextCommand):
    def __init__(self, view):
        super(MoveTextVertCommand, self).__init__(view)
        view.move_text_vert_column = None

    def move_text_vert(self, region, edit, direction):
        if region.empty():
            return

        orig_region = region
        move_text = self.view.substr(region)

        # calculate number of characters to the left
        row, col = self.view.rowcol(region.begin())

        # if the last command was a vertical move, use that column
        # the column is stored on the view - each command has its own instance,
        # and we don't want two buffers to modify the same object (e.g. MoveTextVertCommand)
        cmd, _, _ = self.view.command_history(0, True)
        if cmd != 'move_text_up' and cmd != 'move_text_down':
            self.view.move_text_vert_column = col
        else:
            col = self.view.move_text_vert_column

        dest_row = row + direction

        if dest_row < 0 or dest_row > self.view.rowcol(self.view.size())[0]:
            return

        self.view.sel().subtract(orig_region)
        self.view.replace(edit, region, '')

        # starting at the destination row at col 0, count off "col" characters
        # it's possible that there aren't enough characters in the destination row,
        # so stop if we end up on the wrong row, or past the buffer
        dest_point = self.view.text_point(dest_row, 0)
        if dest_point is None:
            dest_point = self.view.size()
        else:
            dest_line = self.view.line(dest_point)
            if dest_point + col > dest_line.b:
                dest_point = dest_line.b
            else:
                dest_point = dest_point + col

        insert_region = Region(dest_point, dest_point)
        sel_region = Region(dest_point, dest_point + len(move_text))

        self.view.replace(edit, insert_region, move_text)
        self.view.sel().add(sel_region)
        self.view.show(sel_region)


class MoveTextUpCommand(MoveTextVertCommand):
    def run(self, edit):
        e = self.view.begin_edit('move_text_vert')
        regions = [region for region in self.view.sel()]

        # sort by region.end() DESC
        def compare(region_a, region_b):
            return cmp(region_b.end(), region_a.end())
        regions.sort(compare)

        for region in regions:
            self.move_text_vert(region, edit, -1)
        self.view.end_edit(e)


class MoveTextDownCommand(MoveTextVertCommand):
    def run(self, edit):
        e = self.view.begin_edit('move_text_vert')
        regions = [region for region in self.view.sel()]

        # sort by region.end() DESC
        def compare(region_a, region_b):
            return cmp(region_b.end(), region_a.end())
        regions.sort(compare)

        for region in regions:
            self.move_text_vert(region, edit, 1)
        self.view.end_edit(e)
