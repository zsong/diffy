import sublime, sublime_plugin
import sys

if sys.version_info >= (3, 0):
    from .diffy_lib import diffier
else:
    from diffy_lib import diffier

class DiffyCommand(sublime_plugin.TextCommand):
    def get_entire_content(self, view):
        selection = sublime.Region(0, view.size())
        content = view.substr(selection)
        return content

    def clear(self, view):
        view.erase_regions('highlighted_lines')


    """
    return the marked lines
    """
    def draw_difference(self, view, diffs):
        self.clear(view)

        lines = [d.get_region(view) for d in diffs]

        view.add_regions(
            'highlighted_lines', 
            lines, 
            'keyword', 
            'dot', 
            sublime.DRAW_OUTLINED
        )

        return lines


    def set_view_point(self, view, lines):
        if len(lines) > 0:
            view.show(lines[0])

    def run(self, edit, **kwargs):
        diffy = diffier.Diffy()
        window = self.view.window()

        action = kwargs.get('action', None)

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
                    diff_1, diff_2 = diffy.calculate_diff(text_1.split('\n'), text_2.split('\n'))

                    highlighted_lines_1 = self.draw_difference(view_1, diff_1)
                    highlighted_lines_2 = self.draw_difference(view_2, diff_2)

                    self.set_view_point(view_1, highlighted_lines_1)
                    self.set_view_point(view_2, highlighted_lines_2)
