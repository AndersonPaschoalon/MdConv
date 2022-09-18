import os


class TestExecutor:

    def __init__(self):
        self.n_suc = 0
        self.n_err = 0
        self.n_test = 0

    def exec_test(self, test_cmd: str, expected_exit_code = 0, test_name = "test-name"):
        self.n_test += 1
        ret = os.system(test_cmd)
        if ret != expected_exit_code:
            print("********************************************")
            print("** Error executing test ", test_name, " Exit code was: ", ret)
            print("********************************************")
            print("")
            self.n_err +=1
        else :
            print("** Success executing test ", test_name)
            self.n_suc += 1

    def print_summary(self):
        print("")
        print("********************************************")
        print("** Test Summary:")
        print("** Total:", self.n_test)
        print("** Success:", self.n_suc)
        print("** Error:", self.n_err)
        print("********************************************")

def exec_tests():
    test_exec = TestExecutor()
    test_exec.exec_test("mdconv.exe --help", 0, "help")
    test_exec.exec_test("mdconv.exe --version", 0, "version")
    test_exec.exec_test("mdconv.exe --license", 0, "license")

    test_exec.exec_test("mdconv.exe --md README.md --title html-test --output html", 0, "html-test")
    test_exec.exec_test("mdconv.exe --md README.md --title pdf-test --output pdf", 0, "pdf-test")
    test_exec.exec_test("mdconv.exe --md README.md --title txt-test --output txt", 0, "txt-test")
    test_exec.exec_test("mdconv.exe --md README.md --title docx-test --output docx", 0, "docx-test")

    test_exec.exec_test("mdconv.exe --md test-dir\\test.md --title dir-html-test --output html", 0, "dir-html-test")
    test_exec.exec_test("mdconv.exe --md test-dir\\test.md --title dir-pdf-test --output pdf", 0, "dir-pdf-test")
    test_exec.exec_test("mdconv.exe --md test-dir\\test.md --title dir-txt-test --output txt", 0, "dir-txt-test")
    test_exec.exec_test("mdconv.exe --md test-dir\\test.md --title dir-docx-test --output docx", 0, "dir-docx-test")
    test_exec.print_summary()

if __name__ == "__main__":
    exec_tests()




