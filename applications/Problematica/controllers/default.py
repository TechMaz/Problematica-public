# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#from pica_user import PicaUser
#PicaUser.db = db

#from pica_user import PicaUser
import stripe
import json
import requests
import os

logged_in_user_id = auth.user.id if auth.is_logged_in() else None

def index():
    topic_list = PicaTopic.get_all_topics()
    everything_topic = PicaTopic.get_everything_topic()

    return dict(topic_list=topic_list, everything_topic = everything_topic)

def testuserclass():
    print "========================================"
    TestUserMethods.test_search()
    TestUserMethods.test_is_found_in_database()
    TestUserMethods.test_is_user_same_as()
    TestUserMethods.test_get_id()
    TestUserMethods.test_get_bio()
    TestUserMethods.test_get_academic_fields()
    TestUserMethods.test_firstname()
    TestUserMethods.test_lastname()
    #TestUserMethods.test_get_capitalized_fullname()
    #TestUserMethods.test_get_URL()
    TestUserMethods.test_get_submitted_solutions()
    TestUserMethods.test_get_solved_problems()
    #TestUserMethods.test_get_total_bounty_won()
    TestUserMethods.test_get_num_problems_solved()
    #TestUserMethods.test_get_donations()
    #TestUserMethods.test_get_donated_problems()
    TestUserMethods.test_get_total_money_donated()
    TestUserMethods.test_get_clean_total_money_donated()
    TestUserMethods.test_set_bio()
    #TestUserMethods.test_set_academic_fields()

def testtopicclass():
    print "========================================"
    TestTopicMethods.test_get_all_topics()

def signup():
    #Customize Forms
    form = auth.register()
    form.custom.widget.first_name.update(_placeholder="first name")
    form.custom.widget.last_name.update(_placeholder="last name")
    form.custom.widget.email.update(_placeholder="email")
    form.custom.widget.password.update(_placeholder="password")
    form.custom.widget.password_two.update(_placeholder="confirm password")
    form.custom.widget.first_name.update(_placeholder="first name")

    form.custom.submit.update(_value="Create Account")

    return dict(form=form)

def search():
    searchInput = request.get_vars.search_input

    problemResults = PicaProblem.search(searchInput) #PicaProblem Objects
    userResults = PicaUser.search(searchInput)  #PicaUser Objects
    topicResults = PicaTopic.search(searchInput)    #PicaTopic Objects

    foundProblemResults = len(problemResults) != 0
    foundUserResults = len(userResults) != 0
    foundTopicResults = len(topicResults) != 0

    return dict(problemResults = problemResults, userResults = userResults, topicResults = topicResults,
     foundProblemResults = foundProblemResults, foundUserResults = foundUserResults, foundTopicResults = foundTopicResults)

def login():
    form = auth.login()
    form.custom.submit.update(_value="Login")
    form.custom.widget.email.update(_placeholder="email")
    form.custom.widget.password.update(_placeholder="password")
    return dict(form=form)

def profile():
    import time # this is used in the html
    requested_user_id = request.args(0) #gets id from URL
    if requested_user_id is None: redirect(URL('default', 'index'))
    else:
        user = PicaUser(requested_user_id)

        if not user.is_found_in_database():
            redirect(URL('default', 'pagenotfound'))
        else:
            isUsersAccount = user.is_user_same_as(logged_in_user_id)
            #if user is looking at own account, allow editing
            if(isUsersAccount):
                #Get user submitted solutions
                posted_soln = user.get_submitted_solutions()
                #Bio Editing Form
                bioEditForm = form = SQLFORM.factory(
                    Field('bio', requires=IS_NOT_EMPTY()),
                    table_name='profile_bio_edit')
                bioEditForm.custom.widget.bio.update(_placeholder="Tell us about you",_value=user.get_bio())

                if bioEditForm.process().accepted:
                    user.set_bio(bioEditForm.vars.bio)
                    redirect(user.get_URL())

                #Academic Fields Editing Form
                acadfieldsEditForm = SQLFORM.factory(
                Field('acadfields', requires=IS_NOT_EMPTY()),
                table_name='profile_fields_edit')
                acadfieldsEditForm.custom.widget.acadfields.update(_placeholder="Tell us about you",_value=user.get_academic_fields())

                if acadfieldsEditForm.process().accepted:
                    user.set_academic_fields(acadfieldsEditForm.vars.acadfields)
                    redirect(user.get_URL())

            else: #return empty forms if profile is not users
                posted_soln =[]
                bioEditForm=SQLFORM.factory()
                acadfieldsEditForm=SQLFORM.factory()

    return dict(user=user, isUsersAccount = isUsersAccount,
                bioEditForm=bioEditForm, acadfieldsEditForm=acadfieldsEditForm, posted_soln=posted_soln)

@auth.requires_login()
def uploadimage():

    #Check if user already has an image uploaded
    query = ((db.images.owner_id==auth.user.id))
    owner_image = db(query).select().first()
    image_entry_exists = (owner_image is not None)
    user_id = auth.user.id


    if image_entry_exists: #update the record with new image
        imageForm=SQLFORM(db.images, table_name='images',record=owner_image,hidden=dict(owner_id=auth.user.id))
        if imageForm.process().accepted:
            response.flash = 'form accepted'
            redirect(URL('profile', args=(user_id)))
        elif imageForm.errors:
            response.flash = 'form has errors'
        else:
            response.flash = 'please fill out the form'

    else: #create new record
        imageForm=SQLFORM(db.images,hidden=dict(owner_id=auth.user.id))
        if imageForm.process().accepted:
            response.flash = 'form accepted'
            redirect(URL('profile',args=(user_id)))
        elif imageForm.errors:
            response.flash = 'form has errors'
        else:
            response.flash = 'please fill out the form'
    return dict(imageForm=imageForm)

def problem():
    requestedProblemId = request.args(0)

    if requestedProblemId is None: redirect(URL('index'))
    else:
        problem = PicaProblem(requestedProblemId)
        if not problem.is_found_in_database(): redirect(URL('default', 'pagenotfound'))
        donors = problem.get_donors_with_amounts()

    return dict(problem=problem, donors=donors, requestedProblemId=requestedProblemId)

def logout():
    auth.logout()
    redirect(URL('default', 'index'))
    return dict()

def about():
    return dict()

def help():
    return dict()

def topic():
    requestedTopicId = PicaTopic.get_id_by_topic_name(request.args(0))
    topic = PicaTopic(requestedTopicId)

    #check if topic exists
    if not topic.is_found_in_database():
        redirect(URL('default', 'pagenotfound'))

    filter = 'ALL' if topic.get_name() == 'All' else 'topic'
    return dict(topic = topic, filter = filter)

def topics():
    topics = PicaProblem.get_problem_topics()

    return dict(topics=topics)

def pagenotfound():
    return dict()

def postedsolution():
    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    redirect(URL('/login'))
    return dict(form=auth())


@auth.requires(auth.has_membership(group_id='32') or auth.has_membership(group_id='33'))
def institution_portal():
    form = SQLFORM(db.problems)
    problems = db().select(db.problems.ALL, orderby=db.problems.subject)
    solutions = db().select(db.solutions.ALL, orderby=db.solutions.date_submitted)
    users = db().select(db.auth_user.ALL, orderby=db.auth_user.id)
    institution_id = None
    pending_solutions = []
    completed_solutions = []
    pending_solutions_count = 0
    user_id = auth.user.id
    # assign solutions to pending or completed
    for solution in solutions:
        for problem in problems:
            institution_id = int(problem.institution)
            if solution.problem_id == problem.id and user_id == institution_id and solution.status == "pending":
                pending_solutions_count += 1
                pending_solutions.append(solution)
            elif solution.problem_id == problem.id and user_id == institution_id and solution.status != "pending":
                completed_solutions.append(solution)
    if form.process().accepted:
        response.flash = 'your problem is posted'

    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please complete form'
    return dict(problems=problems, form=form, solutions=solutions,
                users=users, pending_solutions=pending_solutions,
                pending_solutions_count=pending_solutions_count,
                completed_solutions=completed_solutions)

#create form to post solutions
@auth.requires_login()
def postsolution():
    form = SQLFORM(db.solutions)
    solutions = db().select(db.solutions.ALL)
    problem_id = request.args(0, cast=int)
    problem = PicaProblem(problem_id)
    form.vars.problem_id = problem_id
    form.vars.attempter_id = auth.user.id
    if form.process().accepted:
        response.flash = 'Your solution is posted'
        #redirect(URL('problem', args=problem_id))
        redirect(URL('default', 'postedsolution'))
    elif form.errors:
        response.flash = 'Your form has errors'
    else:
        response.flash = 'Please complete form'
    return dict(solutions=solutions, form=form, problem=problem)


# form for donating to problems
@auth.requires_login()
def donate():
    request_amount = request.vars['donation_amount']
    print(request_amount)
    stripe_donation_amount = None
    donation_amount = None
    donater_email = auth.user.email
    donor = PicaUser(logged_in_user_id)
    problem_id = int(request.args(0))
    problem = PicaProblem(problem_id)
    if request_amount is not '' and request_amount != 'null':
        donation_amount = int(request_amount)
        if donation_amount <= 0:
            return "Please return to the previous page and enter a positive integer value as your donation amount."
        stripe_donation_amount = donation_amount*100 #stripe takes donation amount in pennies
        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here: https://dashboard.stripe.com/account/apikeys
        stripe.api_key = os.environ['STRIPE_API_KEY']
        checkout_key = os.environ['STRIPE_CHECKOUT_KEY']
        donater_email = auth.user.email
        donor = PicaUser(logged_in_user_id)
        problem_id = int(request.args(0))
        problem = PicaProblem(problem_id)
    else:
        return "Please return to the previous page and enter an integer value as your donation amount."

    return dict(stripe_donation_amount=stripe_donation_amount, donation_amount=donation_amount,
                donater_email=donater_email, problem_id=problem_id, problem=problem, donor = donor, checkout_key=checkout_key)


def sendDonation():
    stripe.api_key = os.environ['STRIPE_API_KEY']
    request_amount = request.vars['donation_amount']
    user_id = request.vars['user_id']
    donation_amount = None
    request_problem_id = request.args(0)
    if request_problem_id is not None:
        problem_id = int(request_problem_id)
    if request_amount:
        donation_amount = int(request_amount)
    if request_amount is None or request_problem_id is None:
        print ("No Donation")
        return "ok"
    else:
        stripe_donation_amount = donation_amount*100 #stripe takes donation amount in pennies
        token = json.loads(request.vars.stripe_token)
         #Create a charge: this will charge the user's card
        try:
            charge = stripe.Charge.create(
                amount=stripe_donation_amount,  # Amount in cents
                currency="usd",
                source=token,
                description="Donation"
            )
        except stripe.error.CardError as e:
            # The card has been declined
            redirect(URL('default', 'card_error'))
            return "nok"
        PicaDonation.make_new_donation(donation_amount, problem_id, user_id, '')
        # redirect(URL('default', 'payment_success'))
        # UPDATE db.donations HERE
    return dict()

def card_error():
    first_name = auth.user.first_name
    return dict(first_name=first_name)

def payment_success():
    donor = PicaUser(logged_in_user_id)
    return dict(donor = donor)


#Default Web2py Functions ======================================================

def download(): #for use in getting images from the database
    return response.download(request, db)

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
