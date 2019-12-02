import os


class FeatureMaker(object):
    def __init__(self, path_dir="./test_cases/"):
        self.path_dir = path_dir
        self.test_cases_list = os.listdir(path_dir)
        self.terms = []

    def find_all_terms(self):
        for test_case in self.test_cases_list:
            test_file = open(self.path_dir + test_case, 'r')
            source_code = test_file.readlines()
            source_code = self._check_ignore(source_code)
            print(test_case, source_code)
            test_file.close()

    def _check_ignore(self, source_code):
        modified_code = []
        comment_flag = False

        for line in source_code:
            if comment_flag:
                if "*/" in line:
                    line = line.split("*/")[1]
                    comment_flag = False
                else:
                    continue
            if "#include" in line:
                continue
            if "//" in line:
                line = line.split("//")[0]
            if '{' in line:
                line = line.replace('{', '')
            if '}' in line:
                line = line.replace('}', '')
            if "/*" in line:
                if "*/" in line:
                    first_part = line.split("/*")[0]
                    second_part = line.split("*/")[1]
                    line = first_part + second_part
                else:
                    line = line.split("/*")[0]
                    comment_flag = True

            line = line.strip().rstrip(';')
            if line != '':
                modified_code.append(line)
        return modified_code


class TestCaseInfo(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.features = []

fm = FeatureMaker()
fm.find_all_terms()
