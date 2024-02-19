def handler(
    jwt: dict,
    new_data: dict,
    old_data: dict,
    well_known_urls: dict,
    method: str = ""
):
    import requests
    customer_data = {"customer": str(new_data['id'])}
    print(customer_data)
    url_strategies = f"{well_known_urls['self']}strategies/"
    AUTH_HEADERS = {
        "Authorization": f"Bearer {jwt}",
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    resp = requests.post(url=url_strategies, json=customer_data, headers=AUTH_HEADERS).json()
    print(resp)

    url_briefs = f"{well_known_urls['self']}briefs/"
    return requests.post(url=url_briefs, json=customer_data, headers=AUTH_HEADERS).json()
