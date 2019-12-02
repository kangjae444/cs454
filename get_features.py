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
            source_code = self._clean_up_code(source_code)
            print("// " + test_case)
            for line in source_code:
                print(line)
            print()
            test_file.close()

    def _clean_up_code(self, source_code):
        clean_code = []
        comment_flag = False
        # string_flag = False

        for line in source_code:
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
            line = line.replace('(', ' ').replace('{', ' ').replace('[', ' ')
            line = line.replace(')', ' ').replace('}', ' ').replace(']', ' ')
            line = line.replace('+', ' ').replace('-', ' ').replace(',', ' ').replace('!', ' ').replace(';', ' ')
            line = line.replace('=', ' ').replace('>', ' ').replace('<', ' ').replace('*', ' ').replace('&', ' ')
            line = line.replace('\\"', ' ')
            line = line.strip()

            if line != '':
                clean_code.append(line)
        return clean_code


class TestCaseInfo(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.features = []

fm = FeatureMaker()
fm.find_all_terms()
