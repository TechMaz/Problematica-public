#pica is short for problematica
#Here and ONLY here donation database calls are handled

class PicaDonation:
#Constructor ===========================================================
    def __init__(self, donation_id):
        try:
            query = db.donations.id == donation_id
            donation = db(query).select().first()
            self.db_donation = donation
        except:
            self.db_donation = None

#Static Methods ========================================================

    @staticmethod
    def get_donations_to_problem(problem):
        query = (((db.donations.problem_id == problem.get_id())))
        donationIDs = db(query).select(db.donations.id).as_list()
        donations=[]
        for i in donationIDs:
            donations.append(PicaDonation(i['id']))
        return donations

    @staticmethod
    def get_donations_by_user(user):
        query = (db.donations.donater_id == user.get_id())
        donationIDsRow = db(query).select(db.donations.id).as_list()
        donations=[]
        for i in donationIDsRow:
            donations.append(PicaDonation(i['id']))
        return donations

    @staticmethod
    def get_donations_by_user_and_problem(user, problem):
        query = ((db.donations.donater_id == user.get_id()) & (db.donations.problem_id == problem.get_id()))
        donationIDsRow = db(query).select(db.donations.id).as_list()
        donations=[]
        for i in donationIDsRow:
            donations.append(PicaDonation(i['id']))
        return donations

    @staticmethod
    def get_sum_of_donations(dlist):
        value = 0
        for d in dlist:
            value = value + d.get_amount()
        return value

    @staticmethod
    def make_new_donation(amount, problem_id, user_id, message):
        donation = db.donations.insert(
            donater_id=user_id,
            problem_id=problem_id,
            amount=amount,
            donor_message = message)
        problem = PicaProblem(problem_id)
        problem.updateNumDonors()
        problem.updateBounty()
        print(donation.id)
        return "ok"


    # update total donation for problem and total users donating

#Getter Methods ========================================================
    def get_id(self):
        return self.db_donation.id

    def get_amount(self):
        return self.db_donation.amount

    def get_donater(self):
        return PicaUser(self.db_donation.donater_id)

    def get_problem(self):
        return PicaProblem(self.db_donation.problem_id)

#Setter Methods ========================================================
