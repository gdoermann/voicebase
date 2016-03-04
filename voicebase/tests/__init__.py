import glob
import unittest

testSuite = unittest.TestSuite()
test_file_strings = glob.glob('test_*.py')
module_strings = [str[0:len(str)-3] for str in test_file_strings]

if __name__ == "__main__":
     unittest.main()