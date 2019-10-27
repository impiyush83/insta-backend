register_user = {
    'first_name': {'type': 'string', 'required': True},
    'last_name': {'type': 'string', 'required': True},
    'gender': {'type': 'string', 'required': True},
    'favourite_song': {'type': 'string', 'required': True},
    'favourite_food': {'type': 'string', 'required': True},
    'favourite_color': {'type': 'string', 'required': True},
    'mobile': {'type': 'string', 'required': True},
    'email': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True}
}


login_user = {
    'email': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True}
}

transfer_profile_data = {
    'secret_key': {'type': 'string', 'required': True}
}
