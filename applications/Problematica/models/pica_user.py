#pica is short for problematica
#Here and ONLY here user and user image database calls are handled

class PicaUser:

    #Constructor ===========================================================
    def __init__(self, user_id):
        if user_id == "fromEntry": #for constructing using a database entry
            self.db_user = None
        else:
            try:
                query = db.auth_user.id == user_id
                user = db(query).select().first()
                self.db_user = user
            except:
                self.db_user = None

    #constructs from database Row object. Use when possible to save time.
    @staticmethod
    def fromEntry(entry):
        newUser = PicaUser("fromEntry")
        newUser.db_user = entry
        return newUser

    #Static Methods ========================================================
    @staticmethod
    def search(searchInput): #returns users relating to search input
        searchInput = searchInput.split(' ')
        query = (db.auth_user.first_name.contains(searchInput, all=False)) | (db.auth_user.last_name.contains(searchInput, all=False))
        db_results = db(query).select()
        results = []
        for i in db_results:
            results.append(PicaUser(i.id))
        return results



    #Getter Methods ========================================================
    def is_found_in_database(self):
        if self.db_user is None:
            return False
        else:
            return True

    def is_user_same_as(self, other_user_id):
        if self.get_id() == other_user_id:
            return True
        else:
            return False

    def get_id(self):
        return self.db_user.id

    def get_profile_pic_source(self):
        query = db.images.owner_id==self.get_id()
        image = db(query).select().first()
        if image is None:
            return "http://placehold.it/124x124"
        else:
            return URL('default', 'download', args=image.picture ) #image.picture is the filename

    #Basic Data
    def get_bio(self):
        return self.db_user.bio

    def get_academic_fields(self):
        return self.db_user.acadfields

    def get_firstname(self):
        return self.db_user.first_name

    def get_lastname(self):
        return self.db_user.last_name

    def get_capitalized_fullname(self):
        return (self.get_firstname() + " " + self.get_lastname()).title()

    def get_URL(self):
        return URL('profile',args=(self.get_id()))

    #Solution Related
    def get_submitted_solutions(self):
        solutions = PicaSolution.get_solutions_by_user(self)
        return solutions

    def get_solved_problems(self):
        solvedProblems = PicaSolution.get_solved_problems_by_user(self)
        return solvedProblems

    def get_total_bounty_won(self):
        total = 0
        for problem in self.get_solved_problems():
            total = total + problem.get_current_bounty()
        return total

    def get_clean_total_bounty_won(self):
        return PicaBeautify.clean_number(self.get_total_bounty_won())

    def get_num_problems_solved(self):
        return len(self.get_solved_problems())

    #Donation Related

    def get_donations(self):
        donations = PicaDonation.get_donations_by_user(self)
        return donations

    def get_donated_problems(self):
        donations = self.get_donations()
        donatedProblems = []
        donatedProblemsIDs = []
        for d in donations:
            problem = d.get_problem();
            if not problem.get_id() in donatedProblemsIDs:
                donatedProblems.append(problem)
                donatedProblemsIDs.append(problem.get_id())
        return donatedProblems

    def get_total_money_donated(self):
        total = 0
        for donation in self.get_donations():
            total = total + donation.get_amount()
        return total

    def get_clean_total_money_donated(self):
        return PicaBeautify.clean_number(self.get_total_money_donated())

    #Setter Methods ========================================================

    def set_bio(self, new_bio):
        self.db_user.bio = new_bio
        self.db_user.update_record()
        return new_bio

    def set_academic_fields(self, new_academic_fields):
        self.db_user.acadfields = new_academic_fields
        self.db_user.update_record()
        return new_academic_fields
