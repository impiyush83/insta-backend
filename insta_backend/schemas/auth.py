login_schema = dict(
    username=dict(required=True, empty=False, type='string'),
    password=dict(required=True, empty=False, type='string'),
)


signup_schema = dict(
    username=dict(required=True, empty=False, type='string'),
    password=dict(required=True, empty=False, type='string'),
    email=dict(required=True, empty=False, type='string'),
)
