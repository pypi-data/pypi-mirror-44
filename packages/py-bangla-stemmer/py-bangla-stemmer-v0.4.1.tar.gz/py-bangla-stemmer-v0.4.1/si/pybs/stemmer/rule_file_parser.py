import os
import re
from collections import OrderedDict


class RuleFileParser:
    CURLY_OPEN = "{"
    CURLY_CLOSE = "}"

    def __init__(self, path="common.rules"):
        self.base_path = os.path.abspath(os.path.dirname(__file__))
        self.resources_base_path = os.path.join(self.base_path, "../../../resources")

        self.__replace_rule = {}
        self.__m_value = {}
        self.__lines = []
        self.__pass = [[]]
        self.__st = OrderedDict()
        self.__escape = OrderedDict()

        self.dependant_char_set_installation()

        with open(os.path.join(self.resources_base_path, path), encoding="UTF-8") as f:
            m_pattern = re.compile("[+].*")
            replace_pattern = re.compile("->.*")
            for line in f:
                line = self.comment_trim(self.white_space_trim(line))
                if line == "":
                    continue
                m = self.extract_value_of_m(line)
                line = m_pattern.sub("", line)
                replace = self.extract_replace_rule(line)
                line = replace_pattern.sub("", line)

                if m != 0:
                    self.__m_value[line] = m

                if replace != "":
                    self.__replace_rule[line] = replace
                self.__lines.append(line)

            cnt = 0
            i = 0
            while i < len(self.__lines):
                if self.__lines[i] == self.CURLY_OPEN:
                    self.__pass.append([])
                    i += 1
                    while i < len(self.__lines) and self.__lines[i] != self.CURLY_CLOSE:
                        self.__pass[cnt].append(self.__lines[i])
                        i += 1
                    cnt += 1
                i += 1

    def stem_of_word(self, word):
        m_rule = 0
        m = self.calculate_m(word)

        for i in range(0, len(self.__pass)):
            for j in range(0, len(self.__pass[i])):
                replace_prefix = self.__pass[i][j]
                matcher = re.compile(".*"+replace_prefix+"$")
                if matcher.match(word):
                    indx = len(word) - len(replace_prefix)
                    if replace_prefix in self.__m_value:
                        m_rule = self.__m_value.get(replace_prefix)
                    else:
                        m_rule = 0
                    if m < m_rule:
                        continue
                    if replace_prefix in self.__replace_rule:
                        replace_suffix = self.__replace_rule.get(replace_prefix)
                        builder = []
                        k = indx
                        _l = 0
                        while k < indx + len(replace_suffix):
                            if replace_suffix[_l] != '.':
                                builder[k] = replace_suffix[_l]
                            k += 1
                            _l += 1
                            print(builder)

                        word = "".join(builder)[0:k]
                    elif self.check(word[0:indx]):
                        word = word[0:indx]
                    break
        return word

    @staticmethod
    def extract_replace_rule(rule):
        pattern = re.compile(".*->.*")
        if pattern.match(rule):
            _l = rule.split("->")
            return _l[1]
        return ""

    @staticmethod
    def extract_value_of_m(string):
        m = 0
        # গুলি     $0
        pattern = re.compile(".*[+].*")
        if pattern.match(string):
            rule_parts = string.split("+")
            m = int(rule_parts[1])
        return m

    @staticmethod
    def white_space_trim(string):
        return re.sub(r"\s+", "", string)

    @staticmethod
    def comment_trim(string):
        return re.sub(r"[#].*", "", string)

    @staticmethod
    def calculate_m(word):
        return len(word)

    def dependant_char_set_installation(self):
        self.__st['া'] = True
        self.__st['ি'] = True
        self.__st['ী'] = True
        self.__st['ে'] = True
        self.__st['ু'] = True
        self.__st['ূ'] = True
        self.__st['ো'] = True

    def check(self, word=""):
        word_length = 0
        for i in range(0, len(word)):
            if self.__st.get(word[i]):
                continue
            word_length += 1
        return word_length >= 1
