import requests
import os.path
from dotenv import load_dotenv

load_dotenv()

requests.packages.urllib3.disable_warnings()
AUTH_CODE = os.getenv('auth_code')
BASE_URL = os.getenv('base_url')

def get_item_id(item_path):
    item_id = item_path.split('/')[2]
    return item_id

def write_label(label_content, item_path):
    item_id = get_item_id(item_path)
    with (open(f"./created_tags/{item_id}.lemd", 'w')) as label_file:
        label_file.write(label_content)

def get_item_name(full_name):
        item_name = input(f"Name on label for \"{full_name}\": ")
        if item_name == "":
            item_name = full_name
        return item_name

def create_label(item_name, item_path):
    final_label_content = ""
    with open("./base_tag.lemd") as labelFile:
        labelFileContent = labelFile.read()
        final_label_content = labelFileContent.replace("ITEMURL", item_path.replace("/","\\/")).replace("TEXTPLACEHOLDER", item_name)
    return final_label_content

def item_already_handled(item_path):
    item_id = get_item_id(item_path)
    return os.path.isfile(f"./created_tags/{item_id}.lemd")

headers = {"Authorization": AUTH_CODE} # TODO real login or check how to set API key. Currently taken from browser cookie
resp = requests.get(f'{BASE_URL}/api/v1/items/export',verify=False, headers=headers)

csv_file_lines = resp.text.split("\n")[1:]

for line in csv_file_lines:
    try:
        item_path = line.split(',')[5]
        full_name = line.split(',')[6]  
    except Exception as e:
        # Should only trigger for empty lines. TODO better error handling.
        continue

    if not item_already_handled(item_path):
        print(item_path)
        item_name = get_item_name(full_name)
        final_item_label = create_label(item_name, item_path)
        write_label(final_item_label, item_path)

# handle csv from resp
pass
# create for all which are not generated yet
