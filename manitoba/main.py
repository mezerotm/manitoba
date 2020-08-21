# #!/bin/env python3.7
from PyInquirer import prompt
import digitalocean
import paramiko

import json

script_version = "1.1.5"
medusa_script = "https://gist.githubusercontent.com/mezerotm/6266bd247a026636d6530b2f94164045/raw/82b457329ff7c18972242520cd74d6738919a5e4/medusa.sh"

print(
    f"""
     ..     ..      ..      ..     .    .......   ..........    ....      ....          ..
    :**.   :**.    ***.    :**:   :*:  .::**:::  .::::**::::  .*::::*.   :*::::*:.     :**.
    :*.*. :::*.   :*.**    :***.  :*:     :*.        .*:     .*:    :*.  :*    .*:    :*.:*
    :*.::.*.:*.  .*: .*:   .*:.*. :*:     :*.        .*:     :*:    .*:  :*::::::.    *: .*:
    :*. :*. :*.  :*   :*.  .*: :*..*.     :*.        .*:     :*.    .*:  :*....:*.   :*.  :*.
    :*.     :*. .*:::::*:  .*:  :*:*:     :*.        .*:     .*:    :*.  :*     :*  .*:::::*:
    :*.     :*. **     :*: :*:   :**:  ...:*:..      .*:      :*:..:*:   :*....:*:  **     :*.
    .:      ......      :. ...    :..  .......:       :.       ..::..    .......   ...      ..

   :::::.:::::******************::::..                     ..:::::****************::::::***::::
  :F$$$$$V$$$$$MMMMM$$$VFI****::...            ..:::**IIV$$$MMMMMMMMNNNNNNNNNNMMMM$$$V$$$$MMM$VI:
 :F$$$$$$$$$$$VVVVVFI*****::::::::::******IIFV$$MMMMMMMMMMMMMNNNNNMNNMMNNNNNMMMMMMMM$$$$MMMMM$FIF*
 :V$$$$$M$$$$V$VIFIIFIVV$$$$$MMMMMMMMMMMMMMMMMMMMMMMMMMMMNMNNMNMMMMMMMMMMMMM$$$$$$V$$$$$$MMM$VV$$V:
  :V$$$$$$$$$VVVFIIFIFVV$V$$M$MMMMMMMMMMMMMMMMMMMNMMNMMMMMMMMMMMM$$VFI***:::..........:*IV$$$MMM$V*
   .*V$$$$$$$$VVVVFFFVV$V$$MMMMMMMMMMMMMMMNMMMMMMMMMMMMM$$VFI**::..               :**IF$$MMMMMM$$V:
     .*IFV$$$$$$$$$$$$$$$$$MMMMMMMMMMMMMMMMMMMMM$$$FI**:...                      .V$Vo***IF$$$$F*.
        ..:**IIFVVV$$$$$$$$$M$M$MMMMM$$$$VFI***:...                              .FVVI**III*II*:.
                ....:::::******:::::....                                          :I$$$VVVV$$*
                                                                                    *VV$$$M$V:
                                                                                     .*VV$VF:.
                                                                                       ..:..
version: {script_version}
by: Adder
contributor(s): Carlos Rincon and Ian Gerard
"""
)

# lib
def contains(filter_list, list, logic="or"):
    if logic == "or":
        for filter_item in filter_list:
            if filter_item in list:
                return True
        return False
    elif logic == "and":
        for filter_item in filter_list:
            if filter_item not in list:
                return False
        return True


def normalize_answers(answers):
    if isinstance(answers, list):
        return [answer.strip() for answer in answers]
    else:
        return answers.strip()


def is_not_empty(answers):
    answers = normalize_answers(answers)
    if answers == None or answers == "" or answers == [""]:
        return False
    else:
        return True


# main
init_answers = prompt(
    [
        {
            "type": "list",
            "name": "setup",
            "message": "What are you interested in doing?",
            "choices": ["Cudo Miner", "Command", "Custom Bash Script",],
        },
        {
            "type": "list",
            "name": "cudo_setup",
            "message": "What are you interested in doing?",
            "choices": ["Full Setup", "Check Status", "Organization Change"],
            "when": lambda answer: answer["setup"] == "Cudo Miner",
        },
        {
            "type": "input",
            "name": "organization",
            "message": "Organization name?",
            "validate": is_not_empty,
            "filter": normalize_answers,
            "when": lambda answer: answer["setup"] == "Cudo Miner"
            and (
                answer["cudo_setup"] == "Full Setup"
                or answer["cudo_setup"] == "Organization Change"
            ),
        },
        {
            "type": "list",
            "name": "service",
            "message": "What service would you like to run?",
            "choices": ["Snake Handler", "Digital Ocean"],
        },
    ]
)

snake_handler_list = []

if init_answers["service"] == "Snake Handler":
    snake_handler_answers = prompt(
        [
            {
                "type": "input",
                "name": "snake_handler_file_name",
                "message": "Name of the Snake Handler list?",
                "default": "snake-handler",
                "validate": is_not_empty,
                "filter": normalize_answers,
            },
        ]
    )

    with open(snake_handler_answers["snake_handler_file_name"]) as f:
        snake_handler_list = json.load(f)
elif init_answers["service"] == "Digital Ocean":
    digital_ocean_answers = prompt(
        [
            {
                "type": "input",
                "name": "username",
                "message": "Username for the droplet(s)?",
                "filter": normalize_answers,
                "default": "root",
            },
            {
                "type": "password",
                "name": "password",
                "message": "Password for the droplet(s)? (leave blank if using pkey)",
                "filter": normalize_answers,
                "default": "",
            },
            {
                "type": "input",
                "name": "key_filename",
                "message": "Give me the absolute path to your key:",
                "validate": is_not_empty,
                "filter": normalize_answers,
                "when": lambda answer: answer["password"] == "",
            },
            {
                "type": "input",
                "name": "token",
                "message": "What is your Digital Ocean API token?",
                "validate": is_not_empty,
                "filter": normalize_answers,
            },
            {
                "type": "input",
                "name": "tags",
                "message": "What Tags would you like to filter on? (seperate fields with a comma ',')",
                "filter": lambda answer: normalize_answers(
                    normalize_answers(answer).split(",")
                ),
            },
            {
                "type": "list",
                "name": "tags_logic",
                "message": "What filter logic would you like?",
                "choices": ["OR", "AND"],
                "when": lambda answer: is_not_empty(answer["tags"])
                and len(answer["tags"]) > 1,
            },
        ]
    )

    do = digitalocean.Manager(token=digital_ocean_answers["token"])
    droplets = do.get_all_droplets()

    def append_droplet(droplet):
        server = {
            "hostname": droplet.ip_address,
            "username": digital_ocean_answers["username"],
            "password": digital_ocean_answers["password"],
        }

        if "key_filename" in digital_ocean_answers["key_filename"]:
            server["key_filename"] = digital_ocean_answers["key_filename"]

        snake_handler_list.append(server)

    if is_not_empty(digital_ocean_answers["tags"]):
        logic = "or"

        if "tags_logic" in digital_ocean_answers:
            if digital_ocean_answers["tags_logic"] == "AND":
                logic = "and"

        for droplet in droplets:
            if contains(digital_ocean_answers["tags"], droplet.tags, logic=logic):
                append_droplet(droplet)
    else:
        for droplet in droplets:
            append_droplet(droplet)


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)


def ssh_connect(server):
    try:
        ssh.connect(
            hostname=server["hostname"],
            username=server["username"],
            password=server["password"],
            key_filename=server["key_filename"],
        )
    except Exception as e:
        print(f"""failed to connect onto: {server["hostname"]}, Exception: {e}""")


def print_stdout(stdout, server):
    print("----------")
    print(f"""hostname: {server["hostname"]}""")

    for line in stdout:
        line = line.strip("\n")
        print(line)


if init_answers["setup"] == "Cudo Miner":
    if init_answers["cudo_setup"] == "Full Setup":

        cudo_setup_answers = prompt(
            [
                {
                    "type": "list",
                    "name": "miner_type",
                    "message": "What type of miner will this be?",
                    "choices": ["CPU", "GPU"],
                }
            ]
        )

        for server in snake_handler_list:
            ssh_connect(server)

            stdin, stdout, stderr = ssh.exec_command(
                f"""env miner_type={cudo_setup_answers["miner_type"]} organization={init_answers["organization"]} bash <( wget -qO- {medusa_script} )"""
            )

            print_stdout(stdout, server)
    elif init_answers["cudo_setup"] == "Check Status":
        for server in snake_handler_list:
            ssh_connect(server)

            stdin, stdout, stderr = ssh.exec_command(
                f"""cudominercli info; cudominercli ps; cudominercli org"""
            )

            print_stdout(stdout, server)
    elif init_answers["cudo_setup"] == "Organization Change":
        for server in snake_handler_list:
            ssh_connect(server)

            stdin, stdout, stderr = ssh.exec_command(
                f"""cudominercli login {init_answers["organization"]}"""
            )

            print_stdout(stdout, server)
elif init_answers["setup"] == "Custom Bash Script":
    custom_script_answers = prompt(
        [
            {
                "type": "list",
                "name": "script_type",
                "message": "Where is your script stored?",
                "choices": ["Local", "URL"],
            },
            {
                "type": "input",
                "name": "url_script",
                "message": "Give me the url to your custom bash script:",
                "validate": is_not_empty,
                "filter": normalize_answers,
                "when": lambda answer: answer["script_type"] == "URL",
            },
            {
                "type": "input",
                "name": "local_script",
                "message": "Give me the absolute path to your custom bash script:",
                "validate": is_not_empty,
                "filter": normalize_answers,
                "when": lambda answer: answer["script_type"] == "Local",
            },
        ]
    )

    command = ""
    if custom_script_answers["script_type"] == "URL":
        command = f"""bash <( wget -qO- {custom_script_answers["url_script"]} )"""
    elif custom_script_answers["script_type"] == "Local":
        with open(custom_script_answers["local_script"]) as f:
            command = f.read()

    for server in snake_handler_list:
        ssh_connect(server)

        stdin, stdout, stderr = ssh.exec_command(command)

        print_stdout(stdout, server)
elif init_answers["setup"] == "Command":
    command_answers = prompt(
        [
            {
                "type": "input",
                "name": "command",
                "message": "command:",
                "validate": is_not_empty,
            }
        ]
    )

    for server in snake_handler_list:
        ssh_connect(server)

        stdin, stdout, stderr = ssh.exec_command(f"""{command_answers["command"]}""")

        print_stdout(stdout, server)

ssh.close()
