import mysql.connector
import re
import getpass
import hashlib
from dotenv import main
from requests import post, get
import os
import base64
import json
import webbrowser
import datetime
from datetime import date
from time import strftime
import time

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

# Get environment variables from .env file
main.load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# finished
def get_token() -> str:
    """Retrieve access token for Spotify API (expires after 1 hour)"""
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


def homePage(username: str) -> None:  # FIXME: missing feed and posted reviews viewing
    user_input = ""
    while user_input != "l":
        print(BOLD + "------" + username + "'s " + GREEN + "Soundtrackd" + END + BOLD + " home page------")
        print(BOLD + "s" + END + ": Search for albums, artists, songs, or users")
        print(
            BOLD
            + "f"
            + END + RED
            + ": View your feed (reviews posted by your followed users)" + END
        )
        print(BOLD + "r" + END + ": View/edit your posted reviews")
        print(BOLD + "l" + END + ": Log out")
        user_input = input(ITALIC + "Choose an option: " + END)
        if user_input == "s":
            search_options(username)
        elif user_input == "f":
            pass
        elif user_input == "r":
            view_my_reviews(username)
        elif user_input != "l":
            print(RED + "Invalid input entered, please try again." + END)


def search_options(username: str) -> None:  # FIXME: missing user search
    """Print search options, choose what kind of search to do, route to that search"""
    user_input = ""
    while user_input != "b":
        print(BOLD + "What would you like to search for?" + END)
        print(BOLD + "a" + END + ": Search for an album")
        print(BOLD + "u" + END + RED + ": Search for a user" + END)
        print(BOLD + "b" + END + ": Back")
        user_input = input(ITALIC + "Choose an option: " + END)
        if user_input == "a":
            album_search(username)
        elif user_input == "u":
            pass
        elif user_input != "b":
            print(RED + "Invalid input entered, please try again." + END)

# Finished
def spotify_search(token: str, type:str , search:str ) -> list:
    """Uses the Spotify web API to return 10 search results of the given type relating to the search string"""
    print("Connecting to " + GREEN + BOLD + "Spotify" + END + "...")
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + token}
    query = f"?q={search}&type={type}&limit=10"
    query_url = url + query
    response = get(query_url, headers=headers)
    result = json.loads(response.content)[type+"s"]["items"]
    return result

# Finished
def album_search(username: str) -> None:
    """Prompt for an album name, return 10 options from spotify search, allow viewing of each option or starting a new search"""
    search_str = ""
    token = get_token()
    while search_str != "b":
        # use the spotify web API to search albums (get the first 10 results)
        print(BOLD + f'---Album Search---' + END)
        search_str = input(ITALIC + "Enter an album name (or b to go back): " + END)
        results = spotify_search(token, "album", search_str)
        user_input = ""
        while user_input not in ("b", "s"):
            print(BOLD + f'---Album Search: "{search_str}"---' + END)
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
            if user_input.isnumeric() and int(user_input) in range(1, len(results) + 1):
                view_album(username, results[int(user_input) - 1]["id"])
                user_input = ""
            elif user_input == "b":
                search_str = "b"
            elif user_input != "s":
                print(RED + "Invalid input entered, please try again." + END)


def view_album(username: str, album_id: str) -> None: #FIXME: missing all options implementations
    # search for the album in the database. If missing, add it
    cursor.execute("SELECT title, release_date, num_tracks, spotify_link, image_link FROM album WHERE id = %s",[album_id],)
    album_info = cursor.fetchall()
    if not album_info:
        create_album(album_id)
        cursor.execute("SELECT title, release_date, num_tracks, spotify_link, image_link FROM album WHERE id = %s",[album_id],)
        album_info = cursor.fetchall()
    album_info = album_info[0]
    # create title string for printing in the loop (100 characters wide)
    title_str = f"{album_info[0]} ({str(album_info[1])[:4]})"
    left_pad = "-" * ((98 - len(title_str)) // 2)
    right_pad = left_pad
    if(len(left_pad) * 2 + len(title_str) + 2 < 100):
        right_pad += "-"
    # create information portion for printing in the loop
    info_str = "| Released by {:<57} | {:>3} tracks | {:>3} reviews |"
    cursor.execute("SELECT name FROM artist a WHERE EXISTS (SELECT * FROM released_album WHERE (album_id=%s and artist_id=a.id))", [album_id])
    artist_names = cursor.fetchall()
    artist_str = ''
    for i in range(len(artist_names) - 1):
        artist_str += artist_names[i][0] + ", "
    artist_str += artist_names[-1][0]
    if len(artist_str) > 57:
        artist_str = artist_str[:56] + "…"
    user_input = ""
    
    # begin input loop (and print album info)
    while user_input != "b":
        cursor.execute("SELECT COUNT(*) FROM review WHERE album_id=%s", [album_id],)
        num_reviews = cursor.fetchall()[0][0]
        print(BOLD + "+" + left_pad + title_str + right_pad + "+" + END)
        print(info_str.format(artist_str, album_info[2], num_reviews))
        print(BOLD + "+" + "-" * 98 + "+" + END)
        print(BOLD + "t" + END + RED + ": View tracklist (comment on songs)" + END)
        print(BOLD + "c" + END + ": View cover art")
        print(BOLD + "s" + END + ": Open album in " + GREEN + BOLD + "Spotify" + END)
        print(BOLD + "w" + END + ": Write an album review")
        print(BOLD + "r" + END + RED + ": View album's existing reviews" + END)
        print(BOLD + "b" + END + ": Back")
        user_input = input(ITALIC + "Choose an option: " + END)
        if user_input == "t":
            #view tracklist
            pass
        elif user_input == "c":
            webbrowser.open(album_info[4])
        elif user_input == "s":
            webbrowser.open(album_info[3])
        elif user_input == "w":
            write_review(username, album_id, album_info[0])
            pass
        elif user_input == "r":
            #print a bunch of reviews that match the album id
            pass
        elif user_input != "b":
            print(RED + "Invalid input entered, please try again." + END)


def create_album(album_id: str) -> None: # FIXME: missing tracks
    """Transfer album/artist information from Spotify API to the database"""
    global db, cursor
    print("Retrieving data from " + GREEN + BOLD + "Spotify" + END + "...")
    token = get_token()
    url = f"https://api.spotify.com/v1/albums/{album_id}"
    headers = {"Authorization": "Bearer " + token}
    response = get(url, headers=headers)
    album = json.loads(response.content)

    cursor.execute("INSERT INTO album VALUES (%s, %s, %s, %s, %s, %s)", [album_id, album["name"], album["release_date"], album["total_tracks"], 
                                                                         album["external_urls"]["spotify"], album["images"][0]["url"]],)
    # add artist released album relationship for each artist
    for x in album["artists"]:
        # Add artist to database if not there already
        cursor.execute("SELECT * FROM artist WHERE id=%s", [x["id"]],)
        if not cursor.fetchall():
            cursor.execute("INSERT INTO artist VALUES (%s, %s, %s)", [x["id"], x["name"], x["external_urls"]["spotify"]],)
        cursor.execute("INSERT INTO released_album VALUES (%s, %s)", [x["id"], album_id])
    db.commit()


def write_review(username, album_id, album_name): # TODO: Make preview review print nicely
    global cursor, db
    user_input = ""
    review_text = ""
    rating = 0
    while user_input != "e":
        print(BOLD + "---Reviewing " + album_name + "---" + END)
        print("What would you like your review to include?")
        print(BOLD + "t" + END + ": Text")
        print(BOLD + "r" + END + ": Rating (from 1-10)")
        print(BOLD + "b" + END + ": Both text AND a rating")
        print(BOLD + "e" + END + ": Exit")
        user_input = input(ITALIC + "Choose an option: " + END)
        if user_input in ("t", "r", "b"):
            # get text
            if user_input in ("t", "b"):
                print("What would you like to write about the album?")
                review_text = input(ITALIC + "Write your text below and press enter to submit (or submit an x to omit a text portion).\n" + END)
                if review_text == "x":
                    review_text = ""
            # get rating
            if user_input in ("r", "b"):
                print("What rating would you like to give the album?")
                rating = input(ITALIC + "Enter a number 1-10 (or 0 to omit a rating): " + END)                
                while (not rating.isdigit()) or (int(rating) < 0) or (int(rating) > 10):
                    print(RED + "Invalid input entered, please try again." + END)
                    rating = input(ITALIC + "Enter a number 1-10 (or 0 to omit a rating): " + END)
                rating = int(rating)
            # Check that at least one field was used
            if (review_text or rating):
                # Preview review
                print("Here is a preview of your review:")
                thedate = date.fromtimestamp(time.time())
                thetime = strftime("%H:%M:%S", time.localtime())
                fake_review = (0, username, album_id, thedate, thetime, rating, review_text)
                print_review(fake_review)
                # preview_review(username, album_name, rating, review_text)
                confirm = ""
                while not (confirm in ("y", "n")):
                    confirm = input(ITALIC + "Enter y to confirm (or n to abandon this review): " + END)
                    if not confirm in ("y", "n"):
                        print(RED + "Invalid input entered, please try again." + END)
                if confirm == "y":
                    thedate = date.fromtimestamp(time.time())
                    thetime = strftime("%H:%M:%S", time.localtime())
                    if review_text and rating:
                        cursor.execute("INSERT INTO review (posted_by, album_id, post_date, post_time, rating, body) VALUES (%s, %s, %s, %s, %s, %s)", [username, album_id, thedate, thetime, rating, review_text],)
                    elif rating:
                        cursor.execute("INSERT INTO review (posted_by, album_id, post_date, post_time, rating) VALUES (%s, %s, %s, %s, %s)", [username, album_id, thedate, thetime, rating],)
                    else:
                        cursor.execute("INSERT INTO review (posted_by, album_id, post_date, post_time, body) VALUES (%s, %s, %s, %s, %s)", [username, album_id, thedate, thetime, review_text],)
                    db.commit()
                    print(GREEN + BOLD + "Review successfully created!" + END)
                    user_input = "e"
            else:
                print(RED + "Error: your review must contain text and/or a rating. Please try again." + END)
        elif user_input != "e":
            print(RED + "Invalid input entered, please try again." + END)
            pass

# CURRENTLY BROKEN
def view_reviews(username, condition):
    """print out 5 reviews that match the condition and prompt for a respnse (exit if none match the condition)"""
    global cursor
    offset = 0
    user_input = ""
    cursor.execute(f"SELECT * FROM review WHERE {condition} LIMIT {offset}, 5",)
    review_list = cursor.fetchall()
    while user_input != "b":
        if len(review_list) == 0:
            print("-" * 42 + "Nothing to show" + "-" * 43)
        else:
            for i in range(len(review_list)):
                print("{:^100}".format(f"({i+1})"))
                print_review(review_list[i])
        print(BOLD + "Enter a review's number to comment on it, or choose another option." + END)
        if(len(review_list) == 5):
            print(BOLD + "n" + END + ": Next page")
        if(offset != 0):
            print(BOLD + "p" + END + ": Previous page")
        print(BOLD + "b" + END + ": Back")
        user_input = input(ITALIC + "Choose an option: " + END)
        if user_input in range(len(review_list)):
            # comment on review
            pass
        elif (len(review_list) == 5 and user_input == "n"):
            offset += 5
            cursor.execute(f"SELECT * FROM review WHERE {condition} LIMIT {offset}, 5",)
            review_list = cursor.fetchall()
        elif (offset != 0 and user_input == "p"):
            offset -=5
            cursor.execute(f"SELECT * FROM review WHERE {condition} LIMIT {offset}, 5",)
            review_list = cursor.fetchall()
        elif (user_input != "b"):
            print(RED + "Invalid input entered, please try again." + END)



def view_user(curr_user, viewed_user):  # FIXME: not functional at all
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


def print_review(r):
    """print a review in a pretty format
    called for each review when a user views their feed, views reviews on an album, or views another user's reviews
    r is a single result from SELECT * FROM review
    """
    id, posted_by, album_id, post_date, post_time, rating, body = r[0], r[1], r[2], r[3], r[4], r[5], r[6], 
    print(BOLD + "+" + "-" * 98 + "+" + END)
    # Title formatting
    cursor.execute("SELECT title, release_date FROM album WHERE id=%s", [album_id])
    album_info = list(cursor.fetchall()[0])
    if len(album_info[0]) > 40:
        album_info[0] = album_info[0][:39] + "…"
    title_str = BOLD + album_info[0] + f" ({str(album_info[1])[:4]}){END} by "
    # Artist formatting
    cursor.execute("SELECT name FROM artist a WHERE EXISTS (SELECT * FROM released_album WHERE (album_id=%s and artist_id=a.id))", [album_id])
    artist_names = cursor.fetchall()
    artist_str = ''
    for i in range(len(artist_names) - 1):
        artist_str += artist_names[i][0] + ", "
    artist_str += artist_names[-1][0]
    if len(artist_str) > (92-len(title_str)):
        artist_str = artist_str[:31] + "…"

    formatted_title = title_str + artist_str
    num_spaces = 92 - len(formatted_title)
    # Create rating field string
    if rating:
        rating_color = ""
        if rating < 4:
            rating_color = BOLD + UNDERLINE + "\33[41m"
        elif rating < 7:
            rating_color = BOLD + UNDERLINE + "\33[43m"
        else:
            rating_color = BOLD + UNDERLINE + "\33[42m"
        rating_str = f"|{rating_color} Rating: " + "{:>2} ".format(str(rating)) + END + "|"
    else:
        rating_str = " " * 13 + "|"
    title_str = "| " + formatted_title +  (" " * num_spaces) + rating_str
    print(title_str)

    user_data = f" Review by {posted_by}"
    date_time = f"Posted {post_time} {post_date} "
    numspaces = 98 - len(user_data) - len(date_time)
    if(body):
        div = UNDERLINE
    else:
        div = ""
    print("|" + div + user_data + " " * numspaces + date_time + END + "|")
    if body:
        full_text = body.split()
        lined_text = [""]
        line = 0
        lined_text[0] = f" \"{full_text[0]}"
        for word in full_text[1:-1]:
            if len(lined_text[line] + " " + word) <= 97:
                lined_text[line] += " " + word
            else:
                lined_text.append(" " + word)
                line += 1
        if len(full_text) > 1:
            if (len(lined_text[line] + " " + full_text[-1]) < 97) and (len(full_text) > 1):
                lined_text[line] += " " + full_text[-1] + "\""
            else:
                lined_text.append(" " + full_text[-1] + "\"")
        else:
            lined_text[0] += "\""
        for l in lined_text:
            l += " " * (97 - len(l))
            print("|" + ITALIC + l + END + " |")
    print(BOLD + "+" + "-" * 98 + "+" + END)

def view_my_reviews(username):
    """print out 5 reviews that match the condition and prompt for a respnse (exit if none match the condition)"""
    global cursor, db
    offset = 0
    user_input = ""
    
    while user_input != "b":
        cursor.execute(f"SELECT * FROM review WHERE posted_by=%s LIMIT {offset}, 5", [username],)
        review_list = cursor.fetchall()
        # Print reviews
        if len(review_list) == 0:
            print("-" * 42 + "Nothing to show" + "-" * 43)
        else:
            for i in range(len(review_list)):
                print("{:^100}".format(f"({i+1})"))
                print_review(review_list[i])
        # Print options and prompt for selection
        print(BOLD + UNDERLINE + "Enter a review's number to select it" + END + BOLD + ", or choose another option." + END)
        if(len(review_list) == 5):
            print(BOLD + "n" + END + ": Next page")
        if(offset != 0):
            print(BOLD + "p" + END + ": Previous page")
        print(BOLD + "b" + END + ": Back")
        user_input = input(ITALIC + "Choose an option: " + END)
        # Handle option selection
        if user_input.isdigit() and (0 < int(user_input) <= len(review_list)): # Select a review, handle more options
            review_index = int(user_input) - 1
            choice = ""
            while choice != "n":
                print(BOLD + f"What would you like to do with review #{review_index+1}?" + END)
                print(BOLD + "c" + END + RED + ": View comments" + END)
                print(BOLD + "a" + END + ": View the album's page")
                print(BOLD + "d" + END + ": Delete the review")
                print(BOLD + "n" + END + ": Nothing")
                choice = input(ITALIC + "Choose an option: " + END)
                if choice == "c":
                    # view_review_comments()
                    pass
                elif choice == "a": # View the reviewed album's page
                    view_album(username, review_list[review_index][2])
                    choice = "n"
                    pass
                elif choice == "d": # Delete the selected review
                    confirm = input(BOLD + RED + ITALIC + f"Are you sure you want to delete review #{review_index+1}?" + END + ITALIC + " Enter y to proceed: " + END)
                    if(confirm == "y"):
                        cursor.execute("DELETE FROM review WHERE id=%s", [review_list[review_index][0]],)
                        db.commit()
                        print(GREEN + BOLD + f"Review #{review_index+1} successfully deleted." + END)
                    choice = "n"
                elif choice != "n":
                    print(RED + "Invalid input entered, please try again." + END)
            pass
        elif (len(review_list) == 5 and user_input == "n"): # View the next 5 reviews
            offset += 5
        elif (offset != 0 and user_input == "p"): # View the previous 5 reviews
            offset -=5
        elif (user_input != "b"):
            print(RED + "Invalid input entered, please try again." + END)

# Finished
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


# Finished
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
        elif (len(input_list[1]) < 3) or (len(input_list[1]) > 60) or (not input_list[1].isalnum()):
            print(
                RED
                + "Username must be 3 to 60 alphanumeric characters, please try again."
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
                            "INSERT INTO user (email, username, password) VALUES (%s, %s, %s)",
                            (input_list[0], input_list[1], password),
                        )
                        db.commit()
                        print(BOLD + GREEN + "User successfully registered!" + END)
                        done = True


if __name__ == "__main__":
    dbuser = input("Enter your local MySQL username (usually root): ")
    dbpass = input("Enter your local MySQL password: ")
    # Conenct to the database (local)
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
