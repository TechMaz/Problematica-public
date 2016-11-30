#pica is short for problematica
#Here and ONLY here solution database calls are handled

class PicaSolution:
    #Constructor ===========================================================
    def __init__(self, solution_id):
        self.problem = None
        self.submitter = None
        if solution_id == "fromEntry": #for constructing using a database entry
            self.db_solution = None
        else:
            try:
                query = db.solutions.id == solution_id
                solution = db(query).select().first()
                self.db_solution = solution
            except:
                self.db_solution = None

    #constructs from database Row object. Use when possible to save time.
    @staticmethod
    def fromEntry(entry):
        newSolution = PicaSolution("fromEntry")
        newSolution.db_solution = entry
        return newSolution

    #Static Methods ========================================================
    @staticmethod
    def get_solutions_by_user(user):
        query = (((db.solutions.attempter_id == user.get_id())))
        dbSolutions = db(query).select(db.solutions.ALL)
        solutions = []
        for i in dbSolutions:
            solutions.append(PicaSolution.fromEntry(i))
        return solutions

    @staticmethod
    def get_solved_problems_by_user(user):
        query = (((db.solutions.attempter_id == user.get_id()) & (db.solutions.status=="right")))
        dbProblemIDs = db(query).select(db.solutions.problem_id).as_list()
        problemIDs = []
        for i in dbProblemIDs: problemIDs.append(i['problem_id'])
        solvedProblems = PicaProblem.get_problems_by_IDs(problemIDs)
        return solvedProblems

    @staticmethod
    def get_pending_solutions_by_problem(problem):
        query = ((db.solutions.problem_id == problem.get_id()) & (db.solutions.status == 'pending'))
        dbSolutions = db(query).select()
        solutions = []
        for i in dbSolutions: solutions.append(PicaSolution.fromEntry(i))
        return solutions

    @staticmethod
    def get_correct_solution_to_problem(problem):
        if problem.get_status() == 'open':
            raise NameError('get_correct_solution_to_problem() in class PicaSolution called on open problem')
        else:
            query = ((db.solutions.problem_id == problem.get_id()) & (db.solutions.status == 'right'))
            dbSolution = db(query).select().first()
            return PicaSolution.fromEntry(dbSolution)
    #Getter Methods ========================================================

    def get_id(self):
        return self.db_solution.id

    def get_status(self):
        return self.db_solution.status

    def get_problem(self):
        if self.problem is None:
            problem_id = self.db_solution.problem_id
            self.problem = PicaProblem(problem_id)
        return self.problem

    def get_submitter(self):
        if self.submitter is None:
            submitter_id = self.db_solution.attempter_id
            self.submitter = PicaUser(submitter_id)
        return self.submitter

    def get_link(self):
        return self.db_solution.link_to_solution

    def get_pdf_download_link(self):
        return URL('default', 'download', args=self.db_solution.solution_pdf)

    #Setter Methods ========================================================

    def set_status(self, status):
        if status == "right":
            self.db_solution.status = "right"
            self.db_solution.update_record()
        elif status == "wrong":
            self.db_solution.status = "wrong"
            self.db_solution.update_record()
        elif status == "too late":
            self.db_solution.status = "too late"
            self.db_solution.update_record()
        else:
            self.db_solution.status = "pending"
            self.db_solution.update_record()
