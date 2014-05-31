
import difflib
from pprint import pprint as pp


class RegionToDraw(object):
    def __init__(self, line_number, start):
        self.line_number = line_number
        self.start = start

    def get_data(self):
        return (self.line_number, self.start)

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


class Diffy(object):
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
        diff_1 = self.parse_diff_list(result1)

        result2 = list(d.compare(text2, text1))
        diff_2 = self.parse_diff_list(result2)

        return diff_1, diff_2