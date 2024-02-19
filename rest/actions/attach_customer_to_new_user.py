def handler(
    jwt: dict,
    new_data: dict,
    old_data: dict,
    well_known_urls: dict,
    method: str = ""
):
    if new_data.get('user'): # if customer already have a user don't create new one
        return new_data
    import requests, string, random
    all_characters = string.ascii_letters + string.digits
    password = "A#2@z" + (''.join(random.choice(all_characters) for _ in range(16)))

    user_payload = {
        "email": new_data.get('email'),
        "user_name": new_data.get('username'),
        "password": password,
        "first_name": new_data.get('first_name'),
        "last_name": new_data.get('last_name'),
        "phone": new_data.get('phone'),
        "reset_password": False,
        "permissions": new_data.get('permissions', ["l9pro-brandboost-user"])
    }
    create_user_url = f"{well_known_urls['zeauth']}/users/"
    AUTH_HEADERS = {
        "Authorization": f"Bearer {jwt}",
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    resp = requests.post(url=create_user_url, json=user_payload, headers=AUTH_HEADERS).json()
    new_data['user'] = resp['id']
    return new_data
