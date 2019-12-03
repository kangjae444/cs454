import os
import re
from test_case_info import TestCaseInfo


class FeatureMaker(object):
    def __init__(self, path_dir="./test_cases/"):
        self._path_dir = path_dir
        self._test_cases_list = os.listdir(path_dir)
        self.term_list = []
        self.case_info_list = []

        self._find_all_terms()
        self._make_feature_vectors()

    def term_num(self):
        return len(self.term_list)

    def _find_all_terms(self):
        replaced_letters_list = ['(', ')', '{', '}', '<', '>', '[', ']', '+', '-', '*', '/', '%', '=',
                                 ',', '!', '&', '|', ';', '.', '\\"']

        def _clean_up_code(dirty_code):
            clean_code = []
            comment_flag = False

            for line in dirty_code:
                if comment_flag:
                    if "*/" in line:
                        line = line.split("*/")[1]
                        comment_flag = False
                    else:
                        continue
                if "#include" in line:
                    continue
                if "#define" in line:
                    line = line.split("#define")[1]
                if "//" in line:
                    line = line.split("//")[0]
                if "/*" in line:
                    if "*/" in line:
                        first_part = line.split("/*")[0]
                        second_part = line.split("*/")[1]
                        line = first_part + second_part
                    else:
                        line = line.split("/*")[0]
                        comment_flag = True

                for replaced_letter in replaced_letters_list:
                    line = line.replace(replaced_letter, ' ')
                if '"' in line:
                    string_list = re.findall('"([^"]*)"', line)
                    for string in string_list:
                        line = line.replace('"{0}"'.format(string), ' SOME_STRING ')
                line = line.strip()

                if line != '':
                    clean_code.append(line)
            return clean_code

        for test_case in self._test_cases_list:
            test_case_info = TestCaseInfo(test_case)
            test_file = open(self._path_dir + test_case, 'r')
            source_code = test_file.readlines()

            source_code = _clean_up_code(source_code)
            for clean_line in source_code:
                term_list = clean_line.split()
                for term in term_list:
                    if self._is_not_number(term):
                        test_case_info.update_term_info(term)
                        if self._is_new_term(term):
                            self.term_list.append(term)

            test_file.close()
            self.case_info_list.append(test_case_info)
        self.term_list.sort()

    def _is_not_number(self, term):
        if term.isdigit() or term[:2] == "0x":
            return False
        return True

    def _is_new_term(self, term):
        if term in self.term_list:
            return False
        return True

    def _make_feature_vectors(self):
        for case_info in self.case_info_list:
            vector = [0]*self.term_num()
            case_info.set_vector(vector)


fm = FeatureMaker()
print(fm.term_list)
print(fm.case_info_list)
