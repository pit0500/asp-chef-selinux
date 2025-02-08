import re
import webbrowser
from dumbo_asp.queries import pack_asp_chef_url
from rich.console import Console

types = [
    "auditadm_t",
    "dbadm_t",
    "guest_t",
    "logadm_t",
    "nx_server_t",
    "secadm_t",
    "staff_t",
    "sysadm_t",
    "unconfined_t",
    "user_t",
    "webadm_t",
    "xguest_t",
]

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
        the_input=input_policies,
    )

    webbrowser.open(url, new=0, autoraise=True)
