import unittest
from pprint import pprint as pp
import __init__ as lib

class TestDiffy(unittest.TestCase):

    def setUp(self):
        self.diffy = lib.Diffy()

    def test_calculate_diff(self):
        text_1 = """
            Using scent:
            nose.config: INFO: Ignoring files matching ['^\\.', '^_', '^setup\\.py$']
            test_config (tests.test_common.test_config.Test_Config) ... ok

            ----------------------------------------------------------------------
            Ran 1 test in 0.003s
            <make></make>
            OK
            <ASDf>   asdfasdf </ASDF>
            In good standing
        """

        text_2 = """
            Using scent:
            nose.config: INFO: Ignoring files matching ['^\\.', '^_', '^setup\\.py$']
            adf
            test_config (tests.test_common.test_config.Test_Config) ... ok

            ----------------------------------------------------------------------
            Ran 1 test in 0.003s



            OK
            <ASDf>   asdfasdf </ASDF1>
            In good standing
        """

        result1, result2 = self.diffy.calculate_diff(text_1.split('\n'), text_2.split('\n'))

        self.assertEqual(result1, [LineToDraw: 6, WordToDraw: 9: (36, 37)])

        self.assertEqual(result2, [LineToDraw: 3,
            LineToDraw: 8,
            LineToDraw: 9,
            LineToDraw: 10,
            WordToDraw: 12: (36, 37)]
        )

if __name__ == '__main__':
    unittest.main()