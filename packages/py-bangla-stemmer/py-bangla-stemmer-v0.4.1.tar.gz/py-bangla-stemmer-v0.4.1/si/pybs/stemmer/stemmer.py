from si.pybs.stemmer.rule_file_parser import RuleFileParser


class BengaliStemmer:
    def __init__(self):
        self.parser = RuleFileParser()

    def stem(self, word):
        if self.parser is None:
            raise Exception("NotInitialized")
        return self.parser.stem_of_word(word.strip())
