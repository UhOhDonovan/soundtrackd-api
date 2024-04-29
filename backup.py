import mysql.connector
import re
import getpass
import hashlib

END = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
UNDERSCORE = "\033[4m"
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


def homePage(user) -> None:  # FIXME
    print(
        BOLD
        + "---"
        + user
        + "'s "
        + GREEN
        + "Soundtrackd"
        + END
        + BOLD
        + " home page---"
    )
    user_input = ""
    while user_input != "l":
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
            pass
        elif user_input == "f":
            pass
        elif user_input == "r":
            pass
        elif user_input != "l":
            print(RED + "Invalid input entered, please try again." + END)


def search():  # FIXME
    """print search options, take search input, search database and Spotify API"""
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
            dbresult = cursor.fetchall()[0]
            if dbresult:
                while not done:
                    password = getpass.getpass(
                        ITALIC + "Enter your password (or e to exit): " + END
                    )
                    if password == "e":
                        done = True
                    elif dbresult[1] == hashlib.sha256(password.encode()).hexdigest():
                        print(
                            BOLD
                            + GREEN
                            + f"Successfully logged in as {dbresult[0]}!"
                            + END
                        )
                        homePage(dbresult[0])
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
