import random

#Sorting ========================================================

def dbReadableSortingDirection(sortDirection):
    if(sortDirection=="LowToHigh"):
        return ""
    elif (sortDirection=="HighToLow"):
        return  "DESC"
    else:
        raise NameError('get_solutions given incorrect sortDirection. Must be either LowToHigh or HighToLow')

#Solutions ========================================================
def get_solutions():

    #Determine Sorting
    columnToSort = request.vars.columnToSort
    sortDirection = dbReadableSortingDirection(request.vars.sortDirection)
    sortString = "solutions."+columnToSort+" "+sortDirection

    #Get indices. Currently not used. Will be when sorting is implemented
    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0

    solutions = []
    associated_problems_ids = []
    has_more = False
    user_id = auth.user.id
    status_type = request.vars.status_type

    #Find all problems associated with this user
    query = db.problems.institution == user_id
    associated_problems_raw = db(query).select()

    for problem in associated_problems_raw:
        associated_problems_ids.append(int(problem.id))

    #Find all solutions to these problems
    if status_type == 'pending':
        query = ((db.solutions.problem_id.belongs(associated_problems_ids)) & (db.solutions.status=='pending'))
    elif status_type == 'judged':
        query = ((db.solutions.problem_id.belongs(associated_problems_ids)) & (db.solutions.status != 'pending'))

    rows = db(query).select(orderby=sortString) #limitby=(start_idx, end_idx + 1)

    #Create array of solutions
    for index, row in enumerate(rows):
        #get problem name
        problem = db(db.problems.id == row.problem_id).select().first()

        #get submitter name
        user = db(db.auth_user.id == row.attempter_id).select(orderby=db.auth_user.id).first()

        sol = dict(
            id = row.id,
            solution_to = problem.problem_title,
            problem_id = problem.id,
            submitter = user.first_name+" "+user.last_name,
            submitter_id = user.id,
            current_bounty = problem.current_bounty,
            date_submitted = row.date_submitted,
            beautified_date_submitted = "{:%B %d, %Y}".format(row.date_submitted), #Should be accurate to the second
            link_to_journal = row.link_to_solution,
            link_to_pdf = URL('default', 'download', args=row.solution_pdf),
            comment = row.submitter_comment,
            status = row.status
        )
        solutions.append(sol)

    return response.json(dict(
        solutions=solutions,
        has_more=has_more,
    ))

#My Problems ========================================================
def get_my_problems():

    problems = [];

    user_id = auth.user.id
    query = db.problems.institution == user_id

    rows = db(query).select()

    #Create array of solutions
    for index, row in enumerate(rows):

            problem = dict(
                id = row.id,
                title = row.problem_title,
                formulation = row.problem_text,
                about = row.problem_about,
                implications = row.problem_implications,
                updates = row.problem_updates,
                bounty = row.current_bounty,
                subject = row.subject
            )
            problems.append(problem)

    return response.json(dict(
        problems = problems
    ))

@auth.requires_signature()
def edit_problem():
    user_id = auth.user.id
    problem_id = request.vars.problem_id
    new_formulation_content = request.vars.new_formulation_content
    new_about_content = request.vars.new_about_content
    new_implications_content = request.vars.new_implications_content
    new_updates_content = request.vars.new_updates_content

    problem_editing = PicaProblem(problem_id)

    if problem_editing.get_institution().get_id() != user_id:
        raise ValueError('You tried to edit problem that did not belong to your institution')
    else:
        problem_editing.set_formulation(new_formulation_content)
        problem_editing.set_about(new_about_content)
        problem_editing.set_implications(new_implications_content)
        problem_editing.set_updates(new_updates_content)
    return response.json(dict())

def judge_solution():
    statusDecided = request.vars.status #status can be: "right" or "wrong"
    solution_id = request.vars.solution_id
    solution = PicaSolution(solution_id)
    solution.set_status(statusDecided)

    if statusDecided == "right":
        solution.get_problem().set_pending_solutions_to_too_late()
        solution.get_problem().set_status('closed')

    return response.json(dict())
