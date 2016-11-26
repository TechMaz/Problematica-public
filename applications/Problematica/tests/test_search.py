import unittest
import sys

from gluon.globals import Request
db = test_db
#execfile("applications/Problematica/controllers/default.py", globals())

class TestSearch(unittest.TestCase):

    # def setUp(self):
        #request = Request()  # Use a clean Request object

    def test_search(self):
        output_id = []
        user_list = [6]
        #input for the method
        output_users = PicaUser.search("Khoa")
        for users in output_users:
            output_id.append(users.get_id())
        self.assertEqual(user_list, output_id)

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestSearch))
test_result = unittest.TextTestRunner(verbosity=2).run(suite)

if len(test_result.failures) > 0:
    ret = 1
else:
    ret = 0

sys.exit(ret)
