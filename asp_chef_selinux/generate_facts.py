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
