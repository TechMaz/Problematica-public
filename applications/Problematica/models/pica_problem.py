#pica is short for problematica
#Here and ONLY here problem and problem files database calls are handled
from __future__ import division
from decimal import Decimal

class PicaProblem:

#Constructors ==========================================================
    def __init__(self, problem_id):
        self.institution = None
        self.topic = None
        if problem_id == "fromEntry": #for constructing using a database entry
            self.db_problem = None
        else:
            try:
                query = db.problems.id == problem_id
                problem = db(query).select().first()
                self.db_problem = problem
            except:
                self.db_problem = None

    #constructs from database Row object. Use when possible to save time.
    @staticmethod
    def fromEntry(entry):
        newProblem = PicaProblem("fromEntry")
        newProblem.db_problem = entry
        return newProblem


#Static Methods ========================================================

    @staticmethod
    def search(searchInput): #returns problems relating to search input
        searchInput = searchInput.split(' ')
        query = db.problems.problem_title.contains(searchInput, all=False)
        db_results = db(query).select()
        results = []
        for i in db_results:
            results.append(PicaProblem(i.id))
        return results

    @staticmethod
    def get_problem_topics():
        db_topics = db().select(db.problems.subject, groupby=db.problems.subject)
        topics = []
        for d in db_topics:
            topics.append(PicaTopic(PicaTopic.get_id_by_topic_name(d.subject)))
        return topics

    #returns a list of all problems as PicaProblems
    @staticmethod
    def get_all_problems():
        db_problem_list = db().select(db.problems.ALL)
        problem_list = []
        for i in db_problem_list:
            problem_list.append(PicaProblem(i.id))
        return problem_list

    #returns a list of problems with IDs in given list
    @staticmethod
    def get_problems_by_IDs(idsList):
        db_problem_list = db(db.problems.id.belongs(idsList)).select()
        problem_list = []
        for i in db_problem_list:
            problem_list.append(PicaProblem.fromEntry(i))
        return problem_list


#Getter Methods ========================================================
    def is_found_in_database(self):
        return not self.db_problem is None

    def get_id(self):
        return self.db_problem.id

    def get_institution(self):
        if self.institution is None:
            self.institution = PicaUser(self.db_problem.institution)
        return self.institution

    def get_title(self):
        return self.db_problem.problem_title

    def get_formulation(self):
        return self.db_problem.problem_text #Once all problem db calls are in this doc change 'problem_text' to 'formulation'

    def get_implications(self):
        return self.db_problem.problem_implications

    def get_updates(self):
        return self.db_problem.problem_updates

    def get_about(self):
        return self.db_problem.problem_about

    def get_current_bounty(self):
        return self.db_problem.current_bounty

    def get_clean_current_bounty(self):
        return PicaBeautify.clean_number(self.get_current_bounty())

    def get_date_posted(self):
        return self.db_problem.date_posted

    def get_clean_date_posted(self):
        return PicaBeautify.clean_date(self.get_date_posted())

    def get_how_long_ago_posted(self):
        return PicaBeautify.time_elapsed_since(self.get_date_posted())

    def get_topic(self):
        if self.topic is None:
            topic_name = self.db_problem.subject
            self.topic = PicaTopic(PicaTopic.get_id_by_topic_name(topic_name))
        return self.topic

    def get_status(self):
        return self.db_problem.status

    def get_URL(self):
        return URL('problem', args=self.get_id())

    #Donations Related
    def get_donations(self): #returns list of donations
        donations = PicaDonation.get_donations_to_problem(self)
        return donations

    def get_total_money_donated(self):
        return PicaDonation.get_sum_of_donations(PicaDonation.get_donations_to_problem(self))

    def get_donations_by_user(self, user): #returns all donations made by a specific user for this problem
        all_donations = PicaDonation.get_donations_by_user(user)
        donations_to_this_problem = []
        for i in all_donations:
            if i.get_problem().get_id() == self.get_id():
                donations_to_this_problem.append(i)
        return donations_to_this_problem

    def get_donators(self): #returns list of donators
        donators = []
        donatorIDs = []
        for d in self.get_donations():
            user = d.get_donater()
            if not user.get_id() in donatorIDs:
                donators.append(user)
                donatorIDs.append(user.get_id())
        return donators

    def get_donors_with_amounts(self):
        donorIDsAmounts = []
        donatorIDs = []
        rank1count = 0
        rank2count = 0
        rank3count = 0
        for d in self.get_donations():
            user = d.get_donater()
            if not user.get_id() in donatorIDs:
                total = PicaDonation.get_sum_of_donations(PicaDonation.get_donations_by_user_and_problem(user, self))
                percent = self.get_donation_percentage(total)
                rank = self.get_donation_rank_for_percentage(percent)
                this_rank_count = 0
                if (rank == 1):
                    rank1count = rank1count + 1
                    this_rank_count = rank1count
                elif (rank == 2):
                    rank2count =  rank2count + 1
                    this_rank_count = rank2count
                else:
                    rank3count =  rank3count + 1
                    this_rank_count = rank3count
                donorIDsAmounts.append((user, total, percent, rank, this_rank_count))
                donatorIDs.append(user.get_id())
        return donorIDsAmounts

    def get_num_donators(self):
        return int(self.db_problem.num_donors)

    def get_clean_num_donators(self):
        return PicaBeautify.clean_number(self.get_num_donators())

    def get_donation_percentage(self, amount):
        total = self.get_total_money_donated()
        percentage =  round(Decimal(format(Decimal((amount/total)*100),'.6f')),2)
        #print("total=" + str(total) + " ,amt=" + str(amount) + " ,percentage=" + str(percentage) + "%")
        return percentage

    def get_donation_rank_for_percentage(self, percent):
        rank = 0;
        percentage = round(Decimal(percent),2)
        #print("rounded percentage: " + str(percentage) + "%")
        if (percentage > 50):
            rank = 1
        elif ((percentage <= 50) & (percentage >= 5)):
            rank = 2
        else:
            rank = 3
        return rank

    #Solutions Related
    def get_pending_solutions(self):
        return PicaSolution.get_pending_solutions_by_problem(self)

    def get_solver(self):
        if self.get_status() == 'open':
            raise NameError('get_solved() in class PicaProblem called on open problem')
        else:
            rightSolution = PicaSolution.get_correct_solution_to_problem(self)
            solver = rightSolution.get_submitter()
            return solver


#Setter Methods ========================================================

    def set_formulation(self, new_formulation):
        self.db_problem.problem_text = new_formulation
        self.db_problem.update_record()

    def set_about(self, new_about):
        self.db_problem.problem_about = new_about
        self.db_problem.update_record()

    def set_implications(self, new_implications):
        self.db_problem.problem_implications = new_implications
        self.db_problem.update_record()

    def set_updates(self, new_updates):
        self.db_problem.problem_updates = new_updates
        self.db_problem.update_record()

    #sets the database version of num_donors
    def set_num_donors(self, new_num_donors):
        self.db_problem.num_donors = new_num_donors
        self.db_problem.update_record()

    def set_pending_solutions_to_too_late(self):
        solutions = self.get_pending_solutions()
        for s in solutions:
            s.set_status("too late")

    def set_status(self, status):
        if status == 'open':
            self.db_problem.status = 'open'
        elif status == 'closed':
            self.db_problem.status = 'closed'
        else:
            raise NameError('set_status() in class PicaProblem given invalid status')
        self.db_problem.update_record()

    def updateNumDonors(self):
        donors = self.get_donators()
        self.db_problem.num_donors = len(donors)
        self.db_problem.update_record()
        return True

    def updateBounty(self):
        donations = self.get_donations()
        self.db_problem.current_bounty = self.db_problem.initial_bounty + PicaDonation.get_sum_of_donations(donations)
        self.db_problem.update_record()
        return True
