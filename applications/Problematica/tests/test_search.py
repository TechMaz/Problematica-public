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
unittest.TextTestRunner(verbosity=2).run(suite)

ret = not unittest.TextTestRunner(verbosity=2).wasSuccessful()
sys.exit(ret)
