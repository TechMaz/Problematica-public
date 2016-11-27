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

    def test_get_id(self):
        test_user_id = 5
        test_user = PicaUser(test_user_id)
        self.assertEqual(test_user.get_id(), test_user_id)

    def test_get_bio(self):
        test_user_id = 5
        test_user = PicaUser(test_user_id)
        test_bio  = "Hi I'm Khoa Luong :)"
        self.assertEqual(test_user.get_bio(), test_bio)

    def test_get_academic_fields(self):
        test_user_id = 5
        test_user = PicaUser(test_user_id)
        test_acad_fields = "Video Games :)"
        self.assertEqual(test_user.get_academic_fields(), test_acad_fields)

    def test_firstname(self):
        test_user_id = 5
        test_user = PicaUser(test_user_id)
        test_firstname = "Khoa"
        self.assertEqual(test_user.get_firstname(), test_firstname)

    def test_firstname2(self):
        test_user_id = 2
        test_user = PicaUser(test_user_id)
        test_firstname = "kfir"
        self.assertEqual(test_user.get_firstname(), test_firstname)

    def test_lastname(self):
        test_user_id = 5
        test_user = PicaUser(test_user_id)
        test_lastname = "Luong"
        self.assertEqual(test_user.get_lastname(), test_lastname)

    def test_get_capitalized_fullname(self):
        test_user_id = 2
        test_user = PicaUser(test_user_id)
        test_caps_fullname = "Kfir Dolev"
        self.assertEqual(test_user.get_capitalized_fullname(), test_caps_fullname)

    def test_get_URL(self):
        test_user_id = 5
        test_user = PicaUser(test_user_id)
        test_user_url = "/profile/5"
        self.assertEqual(test_user.get_URL(), test_user_url)

    def test_get_submitted_solutions(self):
        test_user_id = 5
        test_user = PicaUser(test_user_id)
        solutions = test_user.get_submitted_solutions()
        self.assertEqual(solutions[0].get_id(), 31)

    def test_get_solved_problems(self):
        test_user_id = 5
        empty_list = []
        test_user = PicaUser(test_user_id)
        solved_problems = test_user.get_solved_problems()
        self.assertEqual(solved_problems, empty_list)

    def test_get_total_bounty_won(self):
        test_user_id = 2
        test_bounty = 1100
        test_user = PicaUser(test_user_id)
        self.assertEqual(test_user.get_total_bounty_won(), test_bounty)

    def test_get_num_problems_solved(self):
        test_user_id = 5
        test_num_solved = 0
        test_user = PicaUser(test_user_id)
        self.assertEqual(test_user.get_num_problems_solved(), test_num_solved)

    def test_get_num_problems_solved2(self):
        test_user_id = 2
        test_num_solved = 1
        test_user = PicaUser(test_user_id)
        self.assertEqual(test_user.get_num_problems_solved(), test_num_solved)

    def test_get_donations(self):
        test_user_id = 4
        test_user = PicaUser(test_user_id)
        test_donation_id = 5
        test_donation = PicaDonation(test_donation_id)
        donations = test_user.get_donations()
        if len(donations) > 0:
            self.assertEqual(donations[0].get_amount(), test_donation.get_amount())
        else:
            self.assertEqual(len(donations), 1)

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestClass))
test_result = unittest.TextTestRunner(verbosity=2).run(suite)

if (len(test_result.failures) > 0) | (len(test_result.errors) > 0):
    ret = 1
else:
    ret = 0

sys.exit(ret)
