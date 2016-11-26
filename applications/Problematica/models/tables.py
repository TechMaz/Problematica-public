import datetime

if not os.environ.get("IS_TEST",None):
    db.define_table('problems_by_user',
                    Field('user_id', type='integer'),
                    Field('problem_id', type='integer'))

    db.define_table('images',
        Field('picture', 'upload', uploadfield='picture_file'),
        Field('picture_file', 'blob'),
    	Field('owner_id', type='integer')
    )

    db.define_table('problems',
                    Field('id'),
                    Field('problem_title', type='string'),
                    Field('time_access', type='datetime', default=datetime.datetime.utcnow()),
                    Field('problem_text', type='text'),
                    Field('problem_about', type='text'),
                    Field('problem_implications', type='text'),
                    Field('problem_updates', type='text'),
                    Field('num_donors', type='integer'),
                    Field('status', requires=IS_IN_SET(['open','closed'])),
    #                Field('initial_bounty', type='double', default=0),
                    Field('initial_bounty', type='double', default=0),
                    Field('current_bounty', type='double', default=0),
                    Field('date_posted', type='datetime', default=datetime.datetime.utcnow()),
                    Field('subject', requires=IS_IN_DB(db,'topics.topic_name')),
                    Field('institution', type='integer', default=auth.user_id)
    )

    db.define_table('donations',
                    Field('id'),
                    Field('donater_id', type='integer', default=auth.user_id),
                    Field('problem_id', type='integer', default=0),
                    Field('amount', type='integer', default='0'),
                    Field('donor_message', type='string'),
                    Field('date_made', type='datetime', default=datetime.datetime.utcnow())
    )

    db.define_table('solutions',
                    Field('id'),
                    Field('attempter_id', type='integer', default='0', requires=IS_NOT_EMPTY()),
                    Field('problem_id', type='integer', default='0', requires=IS_NOT_EMPTY()),
                    Field('link_to_solution', type='string', default='', requires=IS_NOT_EMPTY()),
                    Field('solution_pdf', type='upload', uploadfield='pdf_file'),
                    Field('pdf_file', 'blob'),
                    Field('status', requires=IS_IN_SET(['right','wrong','pending', 'too late']), default='pending'),
                    Field('submitter_comment'),
                    Field('date_submitted', type='datetime', default=datetime.datetime.utcnow())
    )

    db.define_table('topics',
        Field('topic_name', type='string'),
    	Field('topic_description', type='text')
    )

    # I don't want to display the user email by default in all forms.
    db.problems.time_access.readable = db.problems.time_access.writable = False
    db.problems.institution.readable = db.problems.institution.writable = False
    db.problems.date_posted.readable = db.problems.date_posted.writable = False

    #don't display these fields in the form for solutions
    db.solutions.status.readable = db.solutions.status.writable = False;
    db.solutions.date_submitted.readable = db.solutions.date_submitted.writable = False;
    db.solutions.attempter_id.readable = db.solutions.attempter_id.writable = False;
    db.solutions.problem_id.readable = db.solutions.problem_id.writable = False;

    #don't display these fields in the form for donations
    db.donations.donater_id.readable = db.donations.donater_id.writable = False;
    db.donations.problem_id.readable = db.donations.problem_id.writable = False;
    db.donations.date_made.readable = db.donations.date_made.writable = False;
