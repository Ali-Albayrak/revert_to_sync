def handler(
    jwt: dict,
    new_data: dict,
    old_data: dict,
    well_known_urls: dict,
    method: str = ""
):
    if old_data.get('user'): # if customer doesn't have a user return
        return
    import requests
    from fastapi import HTTPException

    delete_user_url = f"{well_known_urls['zeauth']}/users/{old_data.get('user')}"
    AUTH_HEADERS = {
        "Authorization": f"Bearer {jwt}",
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    try:
        resp = requests.delete(url=create_user_url, headers=AUTH_HEADERS).json()
    except HTTPException:
        return
