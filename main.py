import requests
import time
from config import *


check = False
pages = 0
users = []
user_id = ''     #Enter the user id of profiles connection list that you want the script to go through

while check == False:
    pages += 1
    connects = 0
    url = f'https://www.linkedin.com/search/results/people/?connectionOf=%5B%22{user_id}%22%5D&network=%5B%22F%22%2C%22S%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&sid=v2g'
    response = requests.get(url, headers = search_header)

    if 'fsd_profileActions:' not in response.text:
        print('no more pages')
        pages -= 1
        check = True
    elif 'fsd_profileActions:' in response.text:
        id = response.text.split('fsd_profileActions:(')[pages].split(',')[0]
        if id not in users:
            amount = response.text.count('fsd_profileActions:(')

            for i in range(amount):
                id = response.text.split('fsd_profileActions:(')[i +1].split(',')[0]
                if id not in users:
                    users.append(id)

            for user in users:
                url = 'https://www.linkedin.com/voyager/api/voyagerRelationshipsDashMemberRelationships?action=verifyQuotaAndCreate'

                data = {
                    'inviteeProfileUrn': f"urn:li:fsd_profile:{user}"
                }

                response = requests.post(url = url, headers = post_header, json = data)
                if 'included' in response.text:
                    connects += 1
                    print(f'followed: {connects}')
                    time.sleep(3)
            users = []


print(f'pages: {pages}')
