import sublime, sublime_plugin
import difflib
from pprint import pprint as pp


class RegionToDraw(object):
    def __init__(self, line_number, start):
        self.line_number = line_number
        self.start = start

    def __str__(self):
        return ""
        
    def __repr__(self):
        return self.__str__()

class LineToDraw(RegionToDraw):
    def __init__(self, line_number, start):
        super(LineToDraw, self).__init__(line_number, start)

    def get_region(self, view):
        point = view.text_point(self.line_number, 0)
        return view.line(point)

    def __str__(self):
        return "LineToDraw: {line_number}".format(line_number=self.line_number)

class WordToDraw(RegionToDraw):
    def __init__(self, line_number, start, end):
        super(WordToDraw, self).__init__(line_number, start)
        self.end = end

    def get_region(self, view):
        point_start = view.text_point(self.line_number, self.start)
        point_end = view.text_point(self.line_number, self.end)

        #take advantage of sublime's API to highlight a word
        return view.word(point_start)

    def __str__(self):
        return "WordToDraw: {line_number}: ({start}, {end})".format(line_number=self.line_number,start=self.start, end=self.end)



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

    def parse_diff_list(self, lst):
        #add a sentinal at the end
        lst.append("$3nt1n3L\n")

        #variables
        diff = []
        line_num = -1
        pre_diff_code = ""
        pre_line = ""

        for line in lst:
            line_num += 1
            diff_code = line[0]

            #the content of the original line
            pre_line_content = pre_line[2:]
            line_content = line[2:]

            #detect a change
            if diff_code == '?': 
                line_num -= 1
                continue
            elif diff_code == '+': line_num -= 1

            if pre_diff_code == '-' and diff_code == '+':
                if line_content == "" or line_content.isspace():
                    pp(pre_line_content + "   " + line_content)
                    pp(line_num)
                    r = LineToDraw(line_num - 1, 0)
                    diff.append(r)
                else:
                    s = difflib.SequenceMatcher(None, pre_line_content, line_content)
                    for tag, i1, i2, j1, j2 in s.get_opcodes():

                        if tag == 'insert':
                            r = WordToDraw(line_num, j1, j2)
                            diff.append(r)
                        elif tag == 'delete' or tag == 'replace':
                            r = WordToDraw(line_num, i1, i2)
                            diff.append(r)
            elif pre_diff_code == '-':
                r = LineToDraw(line_num - 1, 0)
                diff.append(r)

            #tracking
            pre_line = line
            pre_diff_code = diff_code

        return diff

    def calculate_diff(self, text1, text2):
        d = difflib.Differ()
        result1 = list(d.compare(text1, text2))
        pp(result1)
        diff_1 = self.parse_diff_list(result1)

        result2 = list(d.compare(text2, text1))
        diff_2 = self.parse_diff_list(result2)

        return diff_1, diff_2

    def set_view_point(self, view, lines):
        if len(lines) > 0:
            view.show(lines[0])

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

                    highlighted_lines_1 = self.draw_difference(view_1, diff_1)
                    highlighted_lines_2 = self.draw_difference(view_2, diff_2)

                    self.set_view_point(view_1, highlighted_lines_1)
                    self.set_view_point(view_2, highlighted_lines_2)