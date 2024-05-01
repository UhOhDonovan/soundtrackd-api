import mysql.connector
import re
import getpass
import hashlib
from dotenv import main
from requests import post, get
import os
import base64
import json

END = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
REVERSE = "\033[7m"
HIDDEN = "\033[7m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
WELCOME_MSG = (
    BOLD
    + "--------------Welcome to "
    + GREEN
    + "Soundtrackd"
    + END
    + BOLD
    + "--------------"
    + END
)

main.load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def get_token():
    """Retrieve access token for spotify API (Expires after 1 hour)"""
    authorization_str = (CLIENT_ID + ":" + CLIENT_SECRET).encode("utf-8")
    authorization_str = str(base64.b64encode(authorization_str), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + authorization_str,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    response = post(url, headers=headers, data=data)
    token = json.loads(response.content)["access_token"]
    return token


def homePage(username) -> None:  # FIXME
    user_input = ""
    while user_input != "l":
        print(
            BOLD
            + "------"
            + username
            + "'s "
            + GREEN
            + "Soundtrackd"
            + END
            + BOLD
            + " home page------"
        )
        print(BOLD + "s" + END + ": Search for albums, artists, songs, or users")
        print(
            BOLD
            + "f"
            + END
            + ": View your feed (reviews posted by your followed users)"
        )
        print(BOLD + "r" + END + ": View/edit your posted reviews")
        print(BOLD + "l" + END + ": Log out")
        user_input = input(ITALIC + "Choose an option: " + END)
        if user_input == "s":
            search_options(username)
        elif user_input == "f":
            pass
        elif user_input == "r":
            pass
        elif user_input != "l":
            print(RED + "Invalid input entered, please try again." + END)


def search_options(username):  # FIXME
    """print search options, take search input, search database and Spotify API"""
    user_input = ""
    while user_input != "b":
        print(BOLD + "What would you like to search for?" + END)
        print(BOLD + "a" + END + ": Search for an album")
        print(BOLD + "u" + END + ": Search for a user")
        print(BOLD + "b" + END + ": Back")
        user_input = input(ITALIC + "Choose an option: " + END)
        if user_input == "a":
            album_search(username)
        elif user_input == "u":
            pass
        elif user_input != "b":
            print(RED + "Invalid input entered, please try again." + END)


def spotify_search(token, type, search):
    print("Connecting to " + GREEN + BOLD + "Spotify" + END + "...")
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + token}
    query = f"?q={search}&type={type}&limit=10"
    query_url = url + query
    response = get(query_url, headers=headers)
    result = json.loads(response.content)[type+"s"]["items"]
    return result


def album_search(username):  # FIXME
    search_str = ""
    token = get_token()
    while search_str != "b":
        search_str = input(ITALIC + "Enter an album name (or b to go back): " + END)
        results = spotify_search(token, "album", search_str)

        # use spotify API to search albums (get the first 10 results)
        print(BOLD + f'---Album Search: "{search_str}"---' + END)
        user_input = ""
        while user_input not in ("b", "s"):
            for i in range(len(results)):
                print(
                    BOLD
                    + str(i + 1)
                    + END + ": " + UNDERLINE
                    + f"{results[i]["name"]} ({results[i]["release_date"][:4]})" + END + " by ", end=""
                )
                for x in results[i]["artists"][:-1]:
                    print(x["name"], end=", ")
                print(results[i]["artists"][-1]["name"])
            print(BOLD + "s" + END + ": Search again")
            print(BOLD + "b" + END + ": Back")
            user_input = input(ITALIC + "Choose an option: " + END)
            if user_input.isnumeric() and int(user_input) in range(1, len(results)):
                view_album(username, results[i]["id"])
                user_input = "s"
            elif user_input == "b":
                search_str = "b"
            elif user_input != "s":
                print(RED + "Invalid input entered, please try again." + END)


def view_album(username, albumid):
    print(f"viewing album with id {albumid}")
    """----pseudocode---
    if albumid not in database
        create album from spotify API
    create ascii art of the cover and put into list
    album_info = list with album info"""
    cursor.execute("SELECT title, release_date, artist_id FROM album WHERE id = %s",[albumid],)
    album_info = cursor.fetchall()
    if not album_info:
        # create_album()
        cursor.execute("INSERT INTO artist VALUES ('fakeartistid', 'fakename')")
        cursor.execute("INSERT INTO album VALUES (%s, 'faketitle', '2002-01-01', 'fakeartistid')", [albumid],)
        cursor.execute("SELECT title, release_date, artist_id FROM album WHERE id = %s",[albumid],)
        album_info = cursor.fetchall()
        #get info from spotify
    album_info = album_info[0]
    print(BOLD + f"------{album_info[0]} ({str(album_info[1])[:4]})------" + END)
    """user_input = ""
    while user_input != "b":
        for i in range(len(ascii art list)):
            if i in range(len(album_info)):
                print(asci_list[i] + END + album_info[i])
            else:
                print(asci_list[i] + END)
        print(BOLD + "t" + END + ": View tracklist (comment on songs)")
        print(BOLD + "o" + END + ": Open album in Spotify")
        print(BOLD + "c" + END + ": Create an album review")
        print(BOLD + "r" + END + ": View album's existing reviews")
        print(BOLD + "b" + END + ": Back")
        if user_input == "t":
            view tracklist
        elif user_input == "o":
            webbrowser.open(album link)
        elif user_input == "c":
            write_review()
        elif user_input == "r":
            print a bunch of reviews that match the album id
        elif user_input != "b":
            print(RED + "Invalid input entered, please try again." + END)
    """
    pass
def create_album(albumid):
    print("Retrieving data from " + GREEN + BOLD + "Spotify" + END + "...")
    token = get_token()
    url = f"https://api.spotify.com/v1/albums/{albumid}"
    headers = {"Authorization": "Bearer " + token}
    response = get(url, headers=headers)
    album = json.loads(response.content)

    cursor.execute("INSERT INTO album VALUES (%s, %s, %s)", [albumid, album["name"], album["release_date"], ],)
    # Add artist to database if not there
    for x in album["artists"]:
        artist = [x["id"], x["name"]]
        cursor.execute("SELECT id, name FROM artist WHERE id=%s and name=%s", artist,)
        if not cursor.fetchall():
            cursor.execute("INSERT INTO artist VALUES (%s, %s)", [x["id"], x["name"]])
        cursor.execute("INSERT INTO released_album VALUES (%s, %s)", [x["id"], albumid])
    return result
    pass

def view_user(curr_user, viewed_user):  # FIXME
    """When a user is selected, give option to follow or view their posted reviews (maybe also some summary stats)"""
    global cursor, db
    user_input = ""
    while user_input != "b":
        print(BOLD + f"---User: {viewed_user}---" + END)
        print(BOLD + "f" + END + ": Follow {viewed_user}")
        print(BOLD + "r" + END + ": View {viewed_user}'s album reviews")
        print(BOLD + "b" + END + ": Back")
        user_input = input(ITALIC + "Choose an option: " + END)
        if user_input == "f":
            # cursor.execute("INSERT INTO follows_user")
            pass
        elif user_input == "r":
            pass
        elif user_input != "b":
            print(RED + "Invalid input entered, please try again." + END)


def print_review(review_id):
    """print a review in a pretty format
    called for each review when a user views their feed, views reviews on an album, or views another user's reviews
    """


# completed login
def login() -> None:
    """Log in page. Prompts for email/username and password, validates, and enters homepage if a matching user exists"""
    global cursor
    done = False
    username = ""
    valid_email = re.compile(r"^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    print(BOLD + "---------------Log in - Welcome Back!---------------" + END)
    while not done:
        username = str(
            input(
                ITALIC
                + "Enter your registered email address or username (or e to exit): "
                + END
            )
        )
        if username == "e":
            done = True
        else:
            if valid_email.match(username):
                cursor.execute(
                    "SELECT username, password FROM user WHERE email = %s", [username]
                )
            else:
                cursor.execute(
                    "SELECT username, password FROM user WHERE username = %s",
                    [username],
                )
            dbresult = cursor.fetchall()
            if dbresult:
                credentials = dbresult[0]
                while not done:
                    password = getpass.getpass(
                        ITALIC + "Enter your password (or e to exit): " + END
                    )
                    if password == "e":
                        done = True
                    elif credentials[1] == hashlib.sha256(password.encode()).hexdigest():
                        print(
                            BOLD
                            + GREEN
                            + f"Successfully logged in as {credentials[0]}!"
                            + END
                        )
                        homePage(credentials[0])
                        done = True
                    else:
                        print(RED + "Incorrect password, please try again." + END)
            else:
                print(
                    RED
                    + "No user exists with that email or username, please try again."
                    + END
                )


# Completed
def register() -> None:
    """Registration page. Prompts for email address and username, validates. Prompts for password. Stores the user in the databse."""
    global cursor, db
    input_list = []
    password = ""
    done = False
    valid_email = re.compile(r"^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    print(BOLD + "---------------Register a new user---------------" + END)
    while not done:
        # Collect username
        input_list = str(
            input(
                ITALIC
                + "Enter a valid email address and username, separated by spaces (or e to exit): "
                + END
            )
        ).split()

        cursor.execute("SELECT email FROM user")
        taken_emails = cursor.fetchall()
        cursor.execute("SELECT username FROM user")
        taken_users = cursor.fetchall()
        # Validate email/username
        if len(input_list) != 2:
            if input_list == ["e"]:
                print(WELCOME_MSG)
                done = True
            else:
                print(RED + "Incorrect number of inputs, please try again." + END)
        elif not valid_email.match(input_list[0]):
            print(RED + "Invalid email address, please try again." + END)
        elif len(input_list[1]) < 3 or not input_list[1].isalnum():
            print(
                RED
                + "Username must be 3 or more alphanumeric characters, please try again."
                + END
            )
        elif input_list[0] in taken_emails:
            print(
                RED
                + "There is already a registered user with that email address, please try again."
                + END
            )
        elif input_list[1] in taken_users:
            print(
                RED
                + "There is already a registered user with that username, please try again."
                + END
            )
        else:  # Collect password
            while (len(password) < 4) and not done:
                """print(
                    ITALIC
                    + "Enter a password that is 4 or more non-whitespace characters long (or e to exit): "
                    + END,
                    end="",
                )"""
                password = getpass.getpass(
                    ITALIC
                    + "Enter a password that is 4 or more non-whitespace characters long (or e to exit): "
                    + END
                )
                # Validate password
                if password == "e":
                    print(WELCOME_MSG)
                    done = True
                elif len(password) < 4:
                    print(RED + "Your password is too short, please try again." + END)
                elif (
                    (" " in password)
                    or ("\t" in password)
                    or ("\n" in password)
                    or ("\r" in password)
                ):
                    print(
                        RED
                        + "Your password contians whitespace, please try again."
                        + END
                    )
                    password = ""
                else:  # Confirm password
                    """print(
                        ITALIC + "Please re-enter your password to confirm it: " + END,
                        end="",
                    )"""
                    re_entered = getpass.getpass(
                        ITALIC + "Please re-enter your password to confirm it: " + END
                    )
                    if re_entered != password:
                        print(RED + "The passwords do not match." + END)
                        password = ""
                    else:  # Insert new user to database and exit
                        password = hashlib.sha256(password.encode()).hexdigest()
                        cursor.execute(
                            "INSERT INTO user VALUES (%s, %s, %s)",
                            (input_list[0], input_list[1], password),
                        )
                        db.commit()
                        print(BOLD + GREEN + "User successfully registered!" + END)
                        done = True


if __name__ == "__main__":
    dbuser = input("Enter your local MySQL username (usually root): ")
    dbpass = input("enter your local MySQL password: ")
    try:
        db = mysql.connector.connect(
            host="localhost",
            user=dbuser,
            passwd=dbpass,
            database="soundtrackd",
        )
    except:
        print(
            RED
            + BOLD
            + "oops, couldn't connect to database. Make sure your credentials are correct and initialize.sql has been run"
            + END
        )
    cursor = db.cursor()
    user_input = ""

    # Welcome/login/register (home page of the app is entered from within login)
    print(WELCOME_MSG)
    while user_input != "q":
        print(BOLD + "l" + END + ": Log in to an existing account")
        print(BOLD + "r" + END + ": Register a new user account")
        print(BOLD + "q" + END + ": Quit")
        user_input = input(ITALIC + "Choose an option: " + END)
        if user_input == "l":
            login()
            print(WELCOME_MSG)
        elif user_input == "r":
            register()
        elif user_input != "q":
            print(RED + "Invalid input entered, please try again." + END)
    print(
        BOLD + "Thank you for using " + GREEN + "Soundtrackd" + END + BOLD + "!" + END
    )
