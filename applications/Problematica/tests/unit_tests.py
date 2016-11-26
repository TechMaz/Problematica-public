import unittest
import sys

from gluon.globals import Request
db = test_db
#execfile("applications/Problematica/controllers/default.py", globals())

class TestClass(unittest.TestCase):

    # def setUp(self):
        #request = Request()  # Use a clean Request object

    def test_search(self):
        output_id = []
        user_list = [5]
        #input for the method
        output_users = PicaUser.search("Khoa")
        for users in output_users:
            output_id.append(users.get_id())
        self.assertEqual(user_list, output_id)

    def test_search2(self):
        output_id = []
        user_list = []
        #input for the method
        output_users = PicaUser.search("axasfqsfdasd")
        for users in output_users:
            output_id.append(users.get_id())
        self.assertEqual(user_list, output_id)

    def test_is_found_in_database(self):
        test_user_id = 5
        test_user = PicaUser(test_user_id)
        self.assertTrue(test_user.is_found_in_database())

    def test_is_found_in_database2(self):
        test_user_id = 6
        test_user = PicaUser(test_user_id)
        self.assertFalse(test_user.is_found_in_database())

    def test_is_user_same_as(self):
        test_user_id_1 = 1
        test_user_id_2 = 2
        test_user_1 = PicaUser(test_user_id_1)
        test_user_2 = PicaUser(test_user_id_2)
        #We want false because the 2 users are clearly not the same
        self.assertFalse(test_user_1.is_user_same_as(test_user_2))

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestClass))
test_result = unittest.TextTestRunner(verbosity=2).run(suite)

if len(test_result.failures) > 0:
    ret = 1
else:
    ret = 0

sys.exit(ret)
