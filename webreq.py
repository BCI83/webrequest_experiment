#!/usr/bin/env python3
import requests
from datetime import datetime
import urllib3
#url2 = f"https://api-symphony-dev.vnocsymphony.com/symphony-cloud-api/device/monitored/find/v3?macAddress={mac_address}"
def print_col(text, color_code):

    red = "\033[91m"
    yellow = "\033[93m"
    green = "\033[92m"

    if color_code == "red":
        color_code = red
    if color_code == "yellow":
        color_code = yellow
    if color_code == "green":
        color_code = green

    default = "\033[0m"

    print(f"{color_code}{text}{default}")

class obtained_data:
    def __init__(self, environment, expiry_date, account_name, account_id, account_active, mac_address, mac_active):
        self.environment = environment
        self.expiry_date = expiry_date
        self.account_name = account_name
        self.account_id = account_id
        self.account_active = account_active
        self.mac_address = mac_address
        self.mac_active = mac_active

def check_for_cloud_connector(username="", password="", full_url="", mac_address=""):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        new_url = full_url.replace("/symphony-api/provisioning/user/me", f"/symphony-cloud-api/device/monitored/find/v3?macAddress={mac_address}")
        response = requests.get(new_url, auth=(username, password), verify=False)
        data = response.json()
        if response.status_code == 200:
            brand = data["deviceManufacturer"]
        else:
            try:
                message = data["message"]
            except:
                pass
            if "No device found based on provided criteria" in message:
                brand = "Not found"
            else:
                brand = "Unknown"
        if brand == "Not found" or brand == "Unknown":
            mac_active = "No"
        else:
            mac_active = "Yes"
        return mac_active
    except:
        brand = "Unknown"
        return mac_active

def get_xcsrf_token(url):
    r = requests.options(url, verify=False)
    return {"X-CSRF-TOKEN": r.headers.get('X-CSRF-TOKEN')}, r.cookies

def check_login_and_return_data(username="", password=""):

    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        short_url = "https://api-symphony-int.avisplsymphony.com/symphony-api/"
        full_url = "https://api-symphony-int.avisplsymphony.com/symphony-api/user/login"

        headers, cookies = get_xcsrf_token(short_url)
        print(f"HEADERS:\n{headers}")
        print(f"COOKIES:\n{cookies}")
        
        payload = {
            'username': 'briancox@avispl.com',
            'password': 'SuckMyC0x!'
        }        

        response = requests.post(full_url, json=payload, headers=headers, cookies=cookies, verify=False)
        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(response.text)
    except:
        pass
    '''domains = ["avisplsymphony.com", "vnocsymphony.com"]
    url_list = ["", "-emea", "-int", "-dev"]
    object_list = []
    url_successes = []
    for url in url_list:
        for domain in domains:
            try:
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                full_url = f"https://api-symphony{url}.{domain}/symphony-api/provisioning/user/me"
                response = requests.get(full_url, auth=(username, password), verify=False)
                if response.status_code == 200:
                    data = response.json()
                    url_successes.append(full_url)
                    account_id = data["account"]["id"]
                    account_name = data["account"]["name"]
                    account_active = data["account"]["active"]
                    java_epoch_time = data["account"]["accountEntitlementOptions"]["dateExpired"]
                    expiry_date = datetime.fromtimestamp(java_epoch_time / 1000)
                    
                    mac_address = (
                        "02:42:AC:"
                        +account_id[-6:].upper()[:2]
                        + ":"
                        + account_id[-6:].upper()[2:4]
                        + ":"
                        + account_id[-6:].upper()[4:]
                    )

                    extracted_env_chars = ""
                    for char in full_url[8:]:
                        if char != ".":
                            extracted_env_chars += char
                        else:
                            break
                    if extracted_env_chars != "":
                        if extracted_env_chars[13:] == "":
                            detected_env = "prod"
                        else:
                            detected_env = extracted_env_chars[13:] 
                        environment = detected_env
                        # Check for Cloud Connector
                        mac_active = check_for_cloud_connector(username, password, full_url, mac_address)
                    else:
                        environment = ""
                    object_list.append(obtained_data(environment=environment, expiry_date=expiry_date, account_name=account_name, account_id=account_id, account_active=account_active, mac_address=mac_address, mac_active=mac_active))
            except:
                pass
    if len(object_list) == 0:
        print("\nThe provided credentials didn't work for any account on any environment\n\nReach out to your contact at AVI-SPL to get the credentials regenerated/confirmed.")
        return False
    else:
        while True:
            if len(object_list) > 1:
                print("\nThe provided credentials worked with more than one environment, please select which environment is correct for you\n(This information is in your welcome email)\n")
                enviro = 1
                for obj in object_list:
                    print(f"{enviro}: '{object_list[obj].account_name}' on the '{object_list[obj].environment.upper()}' environment")
                    enviro += 1
                ans = input("Enter your choice: ")
                if 1 <= int(ans) <= len(object_list):
                    item = (int(ans) - 1)
                    break
                else:
                    print(f"The entered option '{ans}' is not valid")
            else:
                item = 0
                break
    return object_list[item]'''

    
# Basic Authentication credentials

#username = "briancox@avispl.com"
#password = "SuckMyC0x!"

username = "Bci_cloudconnector@avispl.com"
password = "c7Zad&4E"
check_login_and_return_data(username, password)
'''success_list = check_login_and_return_data(username, password)

if success_list:
    print(success_list.environment.upper())
    if success_list.account_active == True:
        print(success_list.account_active)    
        print(success_list.expiry_date)
    else:
        print(success_list.account_active)
        print("False")
    print_col(success_list.account_name.replace(" ", "-"), "red")
    print_col(success_list.account_id, "green")
    print_col(success_list.mac_address, "yellow")
    print(success_list.mac_active)
else:
    print("Failed")

date_obj = datetime.strptime(str(success_list.expiry_date), "%Y-%m-%d %H:%M:%S")
now = datetime.now()
if date_obj < now:
    print_col(f"{success_list.expiry_date}", "red")
elif date_obj > now:
    print_col(f"{success_list.expiry_date}", "green")'''