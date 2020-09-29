from os import walk, getcwd, getenv, fork
from os.path import join, getsize, isfile, dirname
import sys
import subprocess
import json
from datetime import date, timedelta
import re


def load_json(file: str):
    with open(file, encoding="utf8") as json_file:
        json_data = json.loads(json_file.read())
        return json_data


def safely_update_json(file: str, json_data: dict):
    backup = join(getcwd(), "." + file + ".bak")
    if isfile(backup):
        subprocess.run(["mv", backup, join(getcwd(), "." + file + ".bak2")])
    subprocess.run(["mv", join(getcwd(), file), backup])
    # NOTE it fails on file existence because the file should have been
    # moved into a backup
    with open(file, "x", encoding="utf8",) as json_file:
        json_file.write(json.dumps(json_data))


def expand_path(rel_path: str) -> str:
    if rel_path.startswith("~"):
        return rel_path.replace("~", getenv("HOME"), 1)
    elif rel_path.startswith("./"):
        return rel_path.replace(".", getcwd(), 1)
    elif rel_path.startswith("../"):
        return rel_path.replace("..", getcwd()[0 : indexOf("/", getcwd()[::-2])], 1)
    else:
        return rel_path


def clean(dir: str):
    """Removes any files which are empty
    """
    for root, directories, files in walk(dir):
        if files is not None:
            for File in files:
                if getsize(join(root, File)) < 250:
                    subprocess.run(["rm", join(root, File)])

        if directories is not None:
            for directory in directories:
                clean(directory)


def cycle_journal_cache(journal_home: str, source_cache: str, target_cache: str):
    # TODO: implement new design for 4 fold cache

    for _, directories, _ in walk(join(journal_home + source_cache)):
        for directory in directories:
            for root, _, files in walk(join(journal_home, source_cache, directory)):
                for File in files:
                    subprocess.run(
                        [
                            "mv",
                            join(root, File),
                            join(journal_home, target_cache, directory),
                        ]
                    )


def get_allowed_names(data: dict, today: date) -> dict:
    allowed_names = {
        "str": str,
        "abs": abs,
        "date": date,
        "today": today,
        "days": timedelta.days,
        "month": date.month,
        "year": date.year,
    }
    internal_values = load_json("internal_values.json")
    for key in internal_values:
        if internal_values[key]["type"] == "isodate":
            allowed_names["isodate"] = date.fromisoformat
            allowed_names[key] = internal_values[key]["value"]

    return allowed_names


def eval_expression(expression: str, allowed_names: dict) -> str:
    code = compile(expression, "<string>", "eval")
    for name in code.co_names:
        if name not in allowed_names:
            raise NameError(f"the use of '{name}' is not allowed")

    return eval(code, {"__builtins__": {}}, allowed_names)


def get_replacement_map(data: dict, today):
    replacement_map = {}
    allowed_names = get_allowed_names(data, today)
    for key in data:
        if data[key]["type"] == "content":
            replacement_map[key] = data[key]["value"]
        elif data[key]["type"] == "date-string":
            replacement_map[key] = today.strftime(data[key]["format"])
        elif data[key]["type"] == "date-expression":
            replacement_map[key] = eval_expression(
                data[key]["expression"], allowed_names
            )

    return replacement_map


def replace_keywords(string: str, replacement_map: dict) -> str:
    rep_sorted = sorted(replacement_map, key=len, reverse=True)
    rep_escaped = map(re.escape, rep_sorted)
    pattern = re.compile("|".join(rep_escaped), 0)

    return pattern.sub(lambda match: replacement_map[(match.group(0))], string)


def create_journal(template: str, journal_location: str, replacement_map: dict):
    # TODO: implement try/catch statements
    # TODO: implement type checking
    data = ""
    with open(template, "r") as source:
        data = source.read()
    data = replace_keywords(data, replacement_map)
    with open(journal_location, "x") as target:
        target.write(data)


def update_keyword_data(journal, keywords: dict, data: dict) -> dict:

    key_data = ""
    header = None
    key = None
    key_found = False
    print("updating keyword data")
    with open(journal, "r") as f:
        line = f.readline()
        while line:
            if line.startswith("#"):
                # flip the bool to indicate section is over
                if key_found is True:
                    print(key_data)
                    if key_data.strip() != "":
                        data[key]["value"] = key_data
                        key_data = ""
                    else:
                        data[key]["value"] = "None"
                    key_found = False
                # in both cases check to see if next section in keys
                header = line.replace("#", "").strip()
                if header in keywords:
                    print(header)
                    key = keywords[header]
                    key_found = True
                    key_data = ""

            elif line.startswith("#") is False:
                if key_found is True:
                    key_data += line

            line = f.readline()
        # this should only happen if key was in last section
    if key_found is True:
        data["content_keywords"][key] = key_data
    return data


def update_internal_data(internal_values: dict):
    internal_data = load_json("internal_values.json")
    for key in internal_values:
        if key == "iso-start-date":
            internal_data["value"] = today.isoformat()
    safely_update_json("internal_values.json")


def launch(journal: str) -> bool:
    prelaunch_size = getsize(journal)
    # TODO: implement a better launcher, with error catching
    subprocess.run(["alacritty", "-e", "kak", journal])
    if prelaunch_size == getsize(journal):
        subprocess.run(["rm", journal])
        return False
    else:
        return True


if __name__ == "__main__":
    config = load_json("config.json")
    keyword_data = load_json("keyword_data.json")
    today = date.today()

    if sys.argv[1] == "-c" or sys.argv[1] == "--cycle":
        # NOTE: this option should be unnecessary but I added it in case something goes wrong
        clean(expand_path(config["journal_dir"]) + "current_week")
        # NOTE: stuff from last week is in it's own directory
        # to make it easier to look over when doing weekly journals
        if sys.argv[2] == "weekly":
            cycle_journal_cache(
                expand_path(config["journal_dir"]), "last_week", "this_quarter"
            )
            cycle_journal_cache(
                expand_path(config["journal_dir"]), "this_week", "last_week"
            )
        elif sys.argv[2] == "quarterly":
            cycle_journal_cache(
                expand_path(config["journal_dir"]), "this_quarter", "this_year"
            )
        sys.exit(0)
    elif sys.argv[1] == "-l" or sys.argv[1] == "--launch":
        template = expand_path(config["template_dir"]) + config[sys.argv[2]]["template"]
        journal = (
            expand_path(config["journal_dir"])
            + "current_week/"
            + config[sys.argv[2]]["dir"]
            + "/"
        )

        # get list of words to be searched for and replaced in
        # file names and template-based journals
        replacement_map = get_replacement_map(keyword_data, today)
        file_name = today.strftime(config[sys.argv[2]]["name"]) + ".md"
        # check filename for keywords
        file_name = replace_keywords(file_name, replacement_map)

        journal += file_name

        create_journal(template, journal, replacement_map)

        journal_status = launch(journal)

        if journal_status == False:
            sys.exit(0)

        # update the keywords
        if "keys" in config[sys.argv[2]].keys():
            keyword_data = update_keyword_data(
                journal, config[sys.argv[2]]["keys"], keyword_data
            )
            safely_update_json("keyword_data.json", keyword_data)
        if "internal_values" in config[sys.argv[2]].keys():
            internal_data = update_internal_data(config[sys.argv[2]]["internal_values"])

        # cycle the cache if it's if it's one of the plan templates
        if sys.argv[2] == "weekly":
            cycle_journal_cache(
                expand_path(config["journal_dir"]), "last_week", "this_quarter"
            )
            cycle_journal_cache(
                expand_path(config["journal_dir"]), "current_week", "last_week"
            )
        elif sys.argv[2] == "quarterly":
            cycle_journal_cache(
                expand_path(config["journal_dir"]), "this_quarter", "this_year"
            )
        elif sys.argv[2] == "semi-yearly" and replacement_map["HALF"] == "First Half":
            cycle_journal_cache(
                expand_path(config["journal_dir"]), "this_year", "vault"
            )

        # everything successful
        sys.exit(0)
    elif sys.argv[1] == "-t" or sys.argv[1] == "--test":
        print(str((abs(today - date.fromisoformat("2020-06-01")).days // 7) + 1))

        template = expand_path(config["template_dir"]) + config["weekly"]["template"]
        print(template)
        journal = (
            expand_path(config["journal_dir"])
            + "current_week/"
            + config["weekly"]["dir"]
            + "/"
        )
        print(journal)
        replacement_map = get_replacement_map(keyword_data, today)
        file_name = today.strftime(config["weekly"]["name"]) + ".md"
        # check filename for keywords
        file_name = replace_keywords(file_name, replacement_map)
        journal += file_name
        create_journal(template, journal, replacement_map)
        status = launch(journal)
        if status == False:
            print("this worked")
            sys.exit(0)
        # if file was saved before exiting
        if isfile(journal):
            keyword_data = update_keyword_data(
                journal, config["weekly"]["keys"], keyword_data
            )
            subprocess.run(["rm", journal])
            print(keyword_data)
            print(json.dumps(keyword_data))
        else:
            print("how was that running before?")

