import requests
import os

data_list = []
with open("secret_user.txt", "r") as file:
    data = file.readlines()
    for d in data:
        d.strip("\n")
        data_list.append(d[:30])
print(data)
print(data_list)
url1 = ''
url2 = ''
if data[1] != "secret_password":
    url1 = 'https://adiestradorcaninomadrid.com/user/00-askme.php?secret_user={}&secret_password={}&app_name=meneame&action=permissions'.format(str(data_list[0]), str(data_list[1]))
    url2 = 'https://adiestradorcaninomadrid.com/user/00-askme.php?secret_user={}&secret_password={}&app_name=meneame&action=download'.format(data_list[0], data_list[1])

if url1 != '':
    response = requests.get(url1)
    print(response.headers.get('Content-Type'))
    json_objects = response.json()
    if json_objects['status']:
        response_download = requests.get(url2)
        json_objects_down = response_download.json()
        down_link = json_objects_down['data']
        print(down_link[0])

        file = requests.get(down_link[0], allow_redirects=True)
        open('file.py', 'wb').write(file.content)

        # os.system('python file.py')
    else:
        print("You are not allowed to download files")
else:
    print("User not verified")

# tmpu = "2ni1osj32fk0w44sw0ck"
# response = requests.get("https://adiestradorcaninomadrid.com/user/00-askme.php?tmpu={}&app_name=meneame&action=check_login".format(
#                         tmpu))
# json_objects = response.json()
#
# if json_objects['status']:
#     data[0] = json_objects['secret_user'] + "\n"
#     data[1] = json_objects['secret_password'] + "\n"
#     print(data)
#     print(json_objects)

