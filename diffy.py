import sublime, sublime_plugin
import difflib

class DiffyCommand(sublime_plugin.TextCommand):
    def get_entire_content(self, view):
        selection = sublime.Region(0, view.size())
        content = view.substr(selection)
        return content

    def clear(self, view):
        view.erase_regions('highlighted_lines')

    def draw_difference(self, view, line_numbers):
        self.clear(view)

        lines = []
        for line_number in line_numbers:
            line = view.line(view.text_point(line_number, 0))
            lines.append(line)

        view.add_regions(
            'highlighted_lines', 
            lines, 
            'line', 
            '', 
            sublime.DRAW_OUTLINED
        )

    def calculate_diff(self, text1, text2):
        d = difflib.Differ()
        result = list(d.compare(text1, text2))

        diff_1 = []
        diff_2 = []

        index = 0
        for line in result:
            if line[0] == '-':
                diff_1.append(index)
            elif line[0] == '+':
                diff_2.append(index)

            index += 1 

        return diff_1, diff_2

    def run(self, edit, **kwargs):
        window = self.view.window()

        action = kwargs.get('action', None)

        view_1 = None
        view_2 = None
        if window.num_groups() == 2:
            view_1 = window.active_view_in_group(0)
            view_2 = window.active_view_in_group(1)

        if action == 'clear':
            if view_1: self.clear(view_1)
            if view_2: self.clear(view_2)
        else:
            #make sure there are 2 columns side by side
            if view_1 and view_2:
                text_1 = self.get_entire_content(view_1)
                text_2 = self.get_entire_content(view_2)

                if len(text_1) > 0 and len(text_2) > 0:
                    diff_1, diff_2 = self.calculate_diff(text_1.split('\n'), text_2.split('\n'))

                    self.draw_difference(view_1, diff_1)
                    self.draw_difference(view_2, diff_2)
