import unittest
from pprint import pprint as pp
import diffier

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

class TestDiffy(unittest.TestCase):

    def setUp(self):
        self.diffy = diffier.Diffy()

    def test_calculate_diff(self):


        result1, result2 = self.diffy.calculate_diff(text_1.split('\n'), text_2.split('\n'))

        self.assertEqual(
            [r.get_data() for r in result1], 
            [(6, 0), (9, 24)]
        )

        self.assertEqual(
            [r.get_data() for r in result2], 
            [(3, 0), (8, 0), (9, 0), (10, 0), (12, 24)]
        )

if __name__ == '__main__':
    unittest.main()