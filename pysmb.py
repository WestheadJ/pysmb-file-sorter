from smb.SMBConnection import SMBConnection
from datetime import datetime
import os
import json
import calendar
import getpass
import logging
import time
import uuid

server_profiles = []

ignored_directories = []

valid_extensions = []

log = logging.getLogger("my_logger")

# 2. Set the logging level
log.setLevel(logging.DEBUG)


class SERVER_PROFILE:
    SERVER_NAME = ""
    USERNAME = ""
    PASSWORD = ""
    DOMAIN = ""
    SHARE_NAME = ""


def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%y-%m-%d")


def extract_month_year(timestamp_str):
    dt = datetime.strptime(timestamp_str, "%y-%m-%d")
    month_str = dt.strftime("%B")
    return [month_str, dt.strftime("%Y"), dt.strftime("%d")]


def get_share_information():
    log.debug("getting share information")
    while True:
        SERVER_NAME = input("Enter the server name: ")
        DOMAIN = input("Enter the domain name: ")
        SHARE_NAME = input("Enter the share name: ")

        print(
            f"""SERVER SETTINGS:
    Server Name: {SERVER_NAME}
    Domain Name: {DOMAIN}
    Share Name: {SHARE_NAME}
Are these details correct?"""
        )

        detailsCorrectPrompt = input("true/false (leave empty for true)")
        if detailsCorrectPrompt == True or detailsCorrectPrompt == "":
            break

    USERNAME = input("Enter the username needed: ")
    PASSWORD = getpass.getpass(f"Enter the password for {USERNAME}: ")

    connection_successful = check_server_profile_connection(
        SERVER_NAME, USERNAME, PASSWORD, DOMAIN, SHARE_NAME
    )

    if connection_successful:
        return [SERVER_NAME, USERNAME, PASSWORD, DOMAIN, SHARE_NAME]
    return False


def check_directory_exists(share, directory_path):
    try:
        paths = conn.listPath(share, directory_path)
        dir_exists = False
        for path in paths:
            if path.filename == directory_path:
                dir_exists = True
        return dir_exists
    except:
        return False


def check_server_profile_connection(
    SERVER_NAME, USERNAME, PASSWORD, DOMAIN, SHARE_NAME
):
    try:
        conn = SMBConnection(
            USERNAME, PASSWORD, "python_smb", SERVER_NAME, DOMAIN, use_ntlm_v2=True
        )
        conn.connect(SERVER_NAME, 445)
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def create_new_server_profile(server_profiles):
    log.debug("starting create new server profile")
    profile = get_share_information()
    if profile != False:
        server_profiles.append(profile)

        profiles = []

        for profile in server_profiles:
            print(profile)
            newProfile = {
                "SERVER_NAME": profile[0],
                "USERNAME": profile[1],
                "PASSWORD": profile[2],
                "DOMAIN": profile[3],
                "SHARE_NAME": profile[4],
            }
            profiles.append(newProfile)

        data = {
            "profiles": profiles,
            "ignored-directories": ignored_directories,
            "output-directory": output_directory,
            "valid-extensions": valid_extensions,
        }
        write_config(data)
    else:
        print("Can't connect!")


def write_config(data):
    with open("/Users/james/Desktop/pysmb/smb-configs.json", "w") as profilesFile:
        json.dump(data, profilesFile, indent=4)


def read_config():
    data = ""
    with open("/Users/james/Desktop/pysmb/smb-configs.json", "r") as profilesFile:
        data = json.load(profilesFile)
    return data


# def edit_existing_server_profile():


def get_existing_server_profile(server_profiles):
    log.info(" Getting existing server profiles...")
    time.sleep(0.7)
    data = read_config()
    for profile in data["profiles"]:
        newProfile = [
            profile["SERVER_NAME"],
            profile["USERNAME"],
            profile["PASSWORD"],
            profile["DOMAIN"],
            profile["SHARE_NAME"],
        ]
        server_profiles.append(newProfile)

    if len(server_profiles) == 0:
        log.warning(" No profiles exist! \n")
    else:
        log.info(" Profiles found! \n")
    time.sleep(0.7)

    return server_profiles


def get_output_directory():
    log.debug("Getting the output directory")
    path = read_config()["output-directory"]
    if path == "":
        log.critical(
            "No output directory, this will lead to things being moved to the base directory"
        )
    log.info("Output path found")
    time.sleep(0.7)

    return path


def get_ignored_directories(ignored_directories):

    log.debug("Getting ignored directories")
    time.sleep(0.7)
    data = read_config()
    for directory in data["ignored-directories"]:
        ignored_directories.append(directory)

    if len(ignored_directories) == 0:
        log.warning(
            "No directories found! This could take longer or worse move files from unwanted folders!"
        )
    else:
        log.info("Directories found to ignore \n")
    time.sleep(0.7)
    return ignored_directories


def create_new_directory(share, new_path_name):
    print("Creating new directory: ", new_path_name)
    try:
        conn.createDirectory(share, new_path_name)
        print("Created new directory")
    except:
        print("Cannot create a new directory")


def move_file(SHARE_NAME, original_file_path, output_directory, filename, timestamp):
    log.debug(f'moving file at: "{original_file_path}"')

    random_uuid = uuid.uuid4()

    new_path = f"{output_directory}/{timestamp[1]}/{timestamp[0]}/{timestamp[2]}"
    new_file_name = (
        f"{timestamp[1]}-{timestamp[0]}-{timestamp[2]}-{random_uuid}-{filename}"
    )

    print(f"Moving to: {new_path}/{new_file_name}")

    try:
        conn.rename(SHARE_NAME, original_file_path, f"{new_path}/{new_file_name}")
    except:
        conn.rename(SHARE_NAME, original_file_path, f"{new_path}/copy-{new_file_name}")


def loop_through_path(passed_path, SHARE_NAME):

    print(f"\nPassed base path: {passed_path}")

    # loop through the paths that are listed with the given passed path
    for path in conn.listPath(SHARE_NAME, passed_path):

        # Don't go through hidden paths/files
        if path.filename.startswith(".") != True:

            extension = path.filename.split(".")[-1] if "." in path.filename else ""

            # if the path is a directory and isn't in the ignored directories in the config file then loop through that directory
            if path.isDirectory and path.filename not in ignored_directories:
                print(passed_path + "/" + path.filename)

                if passed_path == "/":
                    loop_through_path(passed_path + path.filename, SHARE_NAME)

                else:
                    loop_through_path(passed_path + "/" + path.filename, SHARE_NAME)

            # If a path is a file and is a valid extenstions
            elif not extension in valid_extensions:

                # get the month,year,day of the files create_time ISO timestamp
                date_created = extract_month_year(format_timestamp(path.create_time))
                print(date_created)

                # Does the file creation year directory exist

                if (
                    check_directory_exists(
                        SHARE_NAME, f"{output_directory}/{date_created[1]}"
                    )
                    == False
                ):
                    create_new_directory(
                        SHARE_NAME, f"{output_directory}/{date_created[1]}"
                    )

                # Does the file creation month directory exist

                if (
                    check_directory_exists(
                        SHARE_NAME,
                        f"{output_directory}/{date_created[1]}/{date_created[0]}",
                    )
                    == False
                ):
                    create_new_directory(
                        SHARE_NAME,
                        f"{output_directory}/{date_created[1]}/{date_created[0]}",
                    )

                # Does the file creation day directory exist

                if (
                    check_directory_exists(
                        SHARE_NAME,
                        f"{output_directory}/{date_created[1]}/{date_created[0]}/{date_created[2]}",
                    )
                    == False
                ):
                    create_new_directory(
                        SHARE_NAME,
                        f"{output_directory}/{date_created[1]}/{date_created[0]}/{date_created[2]}",
                    )

                move_file(
                    SHARE_NAME,
                    f"{passed_path}/{path.filename}",
                    output_directory,
                    path.filename,
                    date_created,
                )


def select_profile(server_profiles, SERVER_PROFILE):
    if len(server_profiles) == 0:
        server_profiles = create_new_server_profile(server_profiles)
    else:
        print("Choose what profile to load:\n")

        for count, profile in enumerate(server_profiles):
            print(f"Profile: {count+1}")
            print(
                f"""    Server Name: {profile[0]}
    Domain: {profile[3]}
    Share Name : {profile[4]}
    Username: {profile[1]}
    Password: {"*" * len(profile[2])}\n"""
            )
        print("Enter 0 to create a new server profile\n")
        profileChoice = int(input("Profile of choice number: ")) - 1

        if profileChoice == -1:
            server_profiles = create_new_server_profile(server_profiles)

        elif profileChoice < 0 or profileChoice >= len(server_profiles):
            print("Choice out of range try again!")
            exit(0)

        SERVER_PROFILE.SERVER_NAME = server_profiles[profileChoice][0]
        SERVER_PROFILE.DOMAIN = server_profiles[profileChoice][3]
        SERVER_PROFILE.SHARE_NAME = server_profiles[profileChoice][4]
        SERVER_PROFILE.USERNAME = server_profiles[profileChoice][1]
        SERVER_PROFILE.PASSWORD = server_profiles[profileChoice][2]

        return SERVER_PROFILE


if __name__ == "__main__":
    # Prepare terminal
    os.system("cls||clear")

    # Get important information

    server_profiles = get_existing_server_profile(server_profiles)
    ignored_directories = get_ignored_directories(ignored_directories)
    output_directory = get_output_directory()

    SERVER_PROFILE = select_profile(server_profiles, SERVER_PROFILE)

    conn = SMBConnection(
        SERVER_PROFILE.USERNAME,
        SERVER_PROFILE.PASSWORD,
        "python_smb",
        SERVER_PROFILE.SERVER_NAME,
        SERVER_PROFILE.DOMAIN,
        use_ntlm_v2=True,
    )
    conn.connect(SERVER_PROFILE.SERVER_NAME, 445)

    if check_directory_exists(SERVER_PROFILE.SHARE_NAME, "/") == False:
        create_new_directory(SERVER_PROFILE.SHARE_NAME, output_directory)

        loop_through_path("Test-Folder", SERVER_PROFILE.SHARE_NAME)
    conn.close()
