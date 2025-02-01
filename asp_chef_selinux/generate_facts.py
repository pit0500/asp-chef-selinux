import re
import webbrowser
from dumbo_asp.queries import pack_asp_chef_url
from rich.console import Console

types = """
auditadm_t
dbadm_t
guest_t
logadm_t
nx_server_t
secadm_t
staff_t
sysadm_t
unconfined_t
user_t
webadm_t
xguest_t""".strip().split('\n')

with open("rules.txt", "r") as rules_file:
    policy_string = rules_file.read()

pattern = re.compile(
    r"allow\s+((?:\S+_t\s+)+)(\S+):(\S+)\s+(\{[^\}]+\}|[^\s\[]+)(?:\s*\[([^\]]+)\]\s*:\s*(\S+))?;"
)

matches = pattern.findall(policy_string)

policy_dict = {}

console = Console()

with console.status("Parsing policies...") as status:
    for match in matches:
        subjects_str = match[0].strip()
        object_type = match[1]
        class_type = match[2]
        permissions_str = match[3].strip("{}").strip()
        options_key = match[4]
        options_value = match[5]

        subjects = list(set(subjects_str.split()))

        permissions = list(set(permissions_str.split()))

        for subject in subjects:
            if subject in types:
                key = f"{subject}:{object_type}:{class_type}"
                if key not in policy_dict:
                    policy_dict[key] = {"permissions": set(), "options": {}}

                policy_dict[key]["permissions"].update(permissions)

                if options_key and options_value:
                    policy_dict[key]["options"][options_key] = options_value

for key in policy_dict:
    policy_dict[key]["permissions"] = list(policy_dict[key]["permissions"])

with console.status("Generating ASP code...") as status:
    input_policies = ""

    for key, value in policy_dict.items():
        subject, object_type, class_type = key.split(":")
        permissions = "; ".join([perm.lower() for perm in value["permissions"]])
        if len(permissions.split("; ")) > 1:
            input_policies += f'policy("{subject.lower()}", "{object_type.lower()}", "{class_type.lower()}", ({permissions})).\n'
        else:
            input_policies += f'policy("{subject.lower()}", "{object_type.lower()}", "{class_type.lower()}", {permissions}).\n'

with console.status("Opening the browser...") as status:
    url = pack_asp_chef_url(
        recipe="https://asp-chef.alviano.net/#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%21",
        the_input=input_policies
    )
    
    webbrowser.open(url, new=0, autoraise=True)
