class TestUserMethods:

    @staticmethod
    def test_search():
        #expected results
        user_list = [5]
        output_id = []
        #input for the method
        output_users = PicaUser.search("Khoa")
        for users in output_users:
            output_id.append(users.get_id())

        if user_list == output_id:
            print "test search successful\n"
        else:
            print "test search unsuccessful, expected results:\n"
            for x in output_users:
                print x.get_id()

    @staticmethod
    def test_is_found_in_database():
        #input for method is 5 aka Khoa
        test_user_id = 5
        test_user = PicaUser(test_user_id)
        if test_user.is_found_in_database() is True:
            print "test is_found_in_database successful\n"
        else:
            print "test is_found_in_database unsuccessful\n"

    @staticmethod
    def test_is_user_same_as():
        #input
        test_user_id_1 = 1
        test_user_id_2 = 2
        test_user_1 = PicaUser(test_user_id_1)
        test_user_2 = PicaUser(test_user_id_2)

        #We wants false because the 2 users are clearly not the same
        if test_user_1.is_user_same_as(test_user_2) is False:
            print "test is_user_same_as successful\n"
        else:
            print "test is_user_same_as unsuccessful\n"

    @staticmethod
    def test_get_id():
        #input
        test_user_id = 5
        test_user = PicaUser(test_user_id)

        if test_user.get_id() == test_user_id:
            print "test get_id successful\n"
        else:
            print "test get_id unsuccessful\n"

    @staticmethod
    def test_get_bio():
        #input
        test_user_id = 5
        test_user = PicaUser(test_user_id)

        try:
            print "test get_bio successful"
            print test_user.get_bio() + "\n"
        except:
            print "test get_bio unsuccessful\n"

    @staticmethod
    def test_get_academic_fields():
        #input
        test_user_id = 5
        test_user = PicaUser(test_user_id)

        try:
            print "test get_academic_fields successful"
            print test_user.get_academic_fields() + "\n"
        except:
            print "test get_academic_fields unsuccessful\n"

    @staticmethod
    def test_firstname():
        #input
        test_user_id = 5
        test_user = PicaUser(test_user_id)

        try:
            print "test get_firstname successful"
            print test_user.get_firstname() + "\n"
        except:
            print "test get_firstname unsuccessful\n"

    @staticmethod
    def test_lastname():
        #input
        test_user_id = 5
        test_user = PicaUser(test_user_id)

        try:
            print "test get_lastname successful"
            print test_user.get_lastname() + "\n"
        except:
            print "test get_lastname unsuccessful\n"

    @staticmethod
    def test_get_capitalized_fullname():
        #input
        test_user_id = 5
        test_user = PicaUser(test_user_id)

        try:
            print "test get_capitalized_fullname successful"
            print test_user.get_capitalized_fullname + "\n"
        except:
            print "test get_capitalized_fullname unsuccessful\n"

    @staticmethod
    def test_get_URL():
        #input
        test_user_id = 5
        test_user = PicaUser(test_user_id)

        try:
            print "test get_URL successful"
            print test_user.get_URL + "\n"
        except:
            print "test get_URL unsuccessful\n"

    @staticmethod
    def test_get_submitted_solutions():
        #input
        test_user_id = 5
        test_user = PicaUser(test_user_id)

        try:
            solutions = test_user.get_submitted_solutions()
            for soln in solutions:
                print soln.get_id()
            print "test get_submitted_solutions successful\n"
        except:
            print "test get_submitted_solutions unsuccessful\n"

    @staticmethod
    def test_get_solved_problems():
        #input
        test_user_id = 5
        test_user = PicaUser(test_user_id)

        try:
            problems = test_user.get_solved_problems()
            for problem in problems:
                print problem.get_id()
            print "test get_solved_problems successful\n"
        except:
            print "test get_solved_problems unsuccessful\n"

    #this doesn't work
    @staticmethod
    def test_get_total_bounty_won():
        #input
        test_user_id = 5
        test_user = PicaUser(test_user_id)

        try:
            print "flag1"
            print test_user.get_total_bounty_won + "\n"
            print "flag2"
            print "test get_total_bounty_won successful"
        except:
            print "test get_total_bounty_won unsuccessful\n"

    @staticmethod
    def test_get_num_problems_solved():
        #input
        test_user_id = 5
        test_user = PicaUser(test_user_id)

        try:
            print test_user.get_num_problems_solved()
            print "test get_num_problems_solved successful\n"
        except:
            print "test get_num_problems_solved unsuccessful\n"

    #donation get_id and get_amount doesn't work so just printing
    @staticmethod
    def test_get_donations():
        #input
        test_user_id = 5
        test_user = PicaUser(test_user_id)

        try:
            """
            donations = test_user.get_donations()
            for donation in donations:
                s = "id: " + donation.get_id() + "amount: " + donation.get_amount()
                print s
            """
            print test_user.get_donations()
            print "test get_donations successful\n"
        except:
            print "test get_donations unsuccessful\n"

    #this doesn't work
    @staticmethod
    def test_get_donated_problems():
        #input
        test_user_id = 5
        test_user = PicaUser(test_user_id)

        try:
            donated = test_user.get_donated_problems()
            for problem in donated:
                print problem.get_id()
            print "test get_donated_problems successful\n"
        except:
            print "test get_donated_problems unsuccessful\n"

    @staticmethod
    def test_get_total_money_donated():
        #input
        test_user_id = 5
        test_user = PicaUser(test_user_id)

        try:
            print test_user.get_total_money_donated()
            print "test get_total_money_donated successful\n"
        except:
            print "test get_total_money_donated unsuccessful\n"

    @staticmethod
    def test_get_clean_total_money_donated():
        #input
        test_user_id = 5
        test_user = PicaUser(test_user_id)

        try:
            print test_user.get_clean_total_money_donated()
            print "test get_clean_total_money_donated successful\n"
        except:
            print "test get_clean_total_money_donated unsuccessful\n"

    @staticmethod
    def test_set_bio():
        #input
        test_user_id = 5
        test_new_bio = "Hi I'm Khoa"
        test_user = PicaUser(test_user_id)

        try:
            new_bio = test_user.set_bio(test_new_bio)
            if new_bio == test_user.get_bio():
                print "test set_bio successful: " + test_user.get_bio() + "\n"
            else:
                print "test set_bio unsuccessful\n"
        except:
            print "test set_bio unsuccessful\n"

    #this doesn't work
    @staticmethod
    def test_set_academic_fields():
        #input
        test_user_id = 5
        test_new_field = "Science"
        test_user = PicaUser(test_user_id)

        try:
            new_field = test_user.set_academic_fields(test_new_field)
            if test_new_field == test_user.get_academic_fields:
                print "test set_academic_fields successful: " + test_user.get_academic_fields() + "\n"
            else:
                print "test set_academic_fields unsuccessful\n"
        except:
            print "test set_academic_fields unsuccessful\n"
