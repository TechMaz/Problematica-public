import random

def index():
    pass


#Problem Table Sorting ========================================================

def get_Problems_Related_To_User(userID, relation):
    if relation == "donation":
        query = (db.donations.donater_id == userID)
        problemIDsRow = db(query).select(db.donations.problem_id).as_list()
    elif relation == "solution": #need to add that solution must be correct
        query = (((db.solutions.attempter_id == userID) & (db.solutions.status=="right")))
        problemIDsRow = db(query).select(db.solutions.problem_id).as_list()
    problemIDs=[]
    for i in problemIDsRow:
        problemIDs.append(int(i['problem_id']))
    return problemIDs

def get_filter_expression(filterType, filterArguement):
    #filterType: "ALL", "userDonated", "userSolved" or "topic"
    #filterArguement:// user id or topic name depending on filter type

    if filterType == "ALL":
        filter_expression = ""
    elif filterType == "topic":
        topic = filterArguement
        filter_expression = db.problems.subject == topic
    elif filterType == "userDonated":
        userID = filterArguement
        problemIDs = get_Problems_Related_To_User(userID, "donation")
        filter_expression = (db.problems.id.belongs(problemIDs))
    elif filterType == "userSolved":
        userID = filterArguement
        problemIDs = get_Problems_Related_To_User(userID, "solution")
        filter_expression = db.problems.id.belongs(problemIDs)
    else:
        filter_expression = None
        raise Error("Invalid Filter given to get_problems")

    return(filter_expression)

def dbReadableSortingDirection(sortDirection):
    if(sortDirection=="LowToHigh"):
        return ""
    elif (sortDirection=="HighToLow"):
        return  "DESC"
    else:
        raise NameError('get_problems given incorrect sortDirection. Must be either LowToHigh or HighToLow')

#Main function ========================================================
def get_problems():

    columnToSort = request.vars.columnToSort
    sortDirection = dbReadableSortingDirection(request.vars.sortDirection)
    sortString = "problems."+columnToSort+" "+sortDirection

    filterType = request.vars.filterType
    filterArguement = request.vars.filterArguement

    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0

    filter_expression = get_filter_expression(filterType, filterArguement)

    problems = []
    has_more = False

    rows = db(filter_expression).select(db.problems.ALL, orderby=sortString, limitby=(start_idx, end_idx + 1))

    for i, r in enumerate(rows):
        problem = PicaProblem.fromEntry(r)
        if i < end_idx - start_idx:
            t = dict(
                id = problem.get_id(),
                title = problem.get_title(),
                num_donaters = problem.get_num_donators(),
                clean_num_donaters = problem.get_clean_num_donators(),
                current_bounty = problem.get_current_bounty(),
                clean_current_bounty = problem.get_clean_current_bounty(),
                date_posted = problem.get_date_posted(),
                clean_date_posted = problem.get_clean_date_posted(),
                subject = problem.get_topic().get_name()
            )
            problems.append(t)
        else:
            has_more = True
    return response.json(dict(
        problems=problems,
        has_more=has_more
    ))
