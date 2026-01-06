import requests
import os.path
from dotenv import load_dotenv

load_dotenv()

requests.packages.urllib3.disable_warnings()
AUTH_CODE = os.getenv('auth_code')
BASE_URL = os.getenv('base_url')

def write_label(label_content, item_path):
    item_id = item_path.split('/')[2]
    with (open(f"./created_tags/{item_id}", 'w+')) as label_file:
        label_file.write(label_content)

def create_label(full_name, item_path):
    if item_already_handled(item_path):
        return ""
    final_label_content = ""
    with open("./base_tag.lemd") as labelFile:
        labelFileContent = labelFile.read()
        item_name = input(f"Name on label for \"{full_name}\": ")
        if item_name == "":
            item_name = full_name
        final_label_content = labelFileContent.replace("ITEMURL", item_path.replace("/","\\/")).replace("TEXTPLACEHOLDER", item_name)
    return final_label_content

def item_already_handled(item_path):
    item_id = item_path.split('/')[2]
    return os.path.isfile(f"./created_tags/{item_id}")

headers = {"Authorization": AUTH_CODE} # TODO real login or check how to set API key. Currently taken from browser cookie
resp = requests.get(f'{BASE_URL}/api/v1/items/export',verify=False, headers=headers)

csv_file_lines = resp.text.split("\n")[1:]

for line in csv_file_lines:
    try:
        item_path = line.split(',')[5]
        full_name = line.split(',')[6]
        final_item_label = create_label(full_name, item_path)        
    except Exception as e:
        # Should only trigger for empty lines. TODO better error handling.
        pass
    write_label(final_item_label, item_path)


# handle csv from resp
pass
# create for all which are not generated yet
