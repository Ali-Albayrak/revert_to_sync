def handler(
    jwt: dict,
    new_data: dict,
    old_data: dict,
    well_known_urls: dict,
    method: str = ""
):
    if new_data.get('request_status') != 'success':
        return
    import requests

    ZENOTIFY_BASE_URL = f"https://api.zenotify.zekoder.brandboost.l9pro.zekoder.us/"

    AUTH_HEADERS = {
        "Authorization": f"Bearer {jwt}",
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    notification_response = cls.create_notification(recipient_email, template_id, params)
    params = {
        "action_link": well_known_urls['self'] + "content/" + new_data['id'],
        user_name: new_data['user_name']
    }

    json_data = {
        "recipients": [recipients],
        "provider": NOTIFICATION_PROVIDER, # id of the notification provider
        "template": "5883ef22-93fd-4d6c-944a-35be51561d12",
        "params": {"list": [params]},
        "target": "email",
        "status": "",
        "last_error": ""
    }
    notification_response = requests.post(f"{ZENOTIFY_BASE_URL}/notifications/", json=json_data)

    if not notification_response.json().get('id'):
        raise CreateNotificationError

    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {"notificationId": notification_response.json()['id']}
    send_email_url = "https://zenotify-service.zekoder.zestudio.zekoder.zekoder.net/send/email"
    response = requests.post(f"{semd_email_url}", json=json_data, headers=headers)

    if response.status_code != 200:
        raise SendNotificationError

    # url = f"{well_known_urls['zenotify']}"
    # return requests.post(url=url, json=new_data, headers=AUTH_HEADERS).json()
