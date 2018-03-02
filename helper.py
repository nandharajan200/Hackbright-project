from flask import (Flask,  # Flask allows app object
                   session, flash,  # session allows use of session storage for login
                   render_template, redirect,  # render_template allows html render functionality
                   request,  # request allows use of forms in html templates
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
import query
import requests
import os


# SENDING EMAILS (MAILGUN API) #############################################

def send_team_invite(email_address, sender_name, message, team_name):
    """Takes in four strings, sends invitation via mailGun."""

    message_intro = "Here is your message from {}:\n".format(sender_name)

    site_summary = """\n\nSamePage is a responsive web app that makes
    getting things done a bit more fun, while still staying agile
    and portable. """

    text_content = message_intro + message + site_summary

    html_content = """<html><body>Here is your message from {sender}:
    <br><p>{message}</p><br><br><p>Accept the invitation by going to
    <a href="http://localhost:5000/">SamePage</a> and logging in or creating
    a new account.</p><br><p><i>SamePage is a responsive web app that makes
    getting things done a bit more fun, while still staying agile
    and portable.</i></p></body></html>""".format(sender=sender_name,
                                                  message=message)

    origin_domain = os.environ['MAILGUN_API_SANDBOX_DOMAIN']
    api_key = os.environ['MAILGUN_API_KEY']
    postmaster = os.environ['MAILGUN_API_POSTMASTER_ADDRESS']

    return requests.post(
        origin_domain,
        auth=("api", api_key),
        data={"from": "SamePage Beta, via Mailgun " + postmaster,
              "to": "<" + email_address + ">",
              "subject": "SamePage Team Invite from " + sender_name + ": " + team_name,
              "text": text_content,
              "html": html_content})

# You can see a record of this email in your logs: https://app.mailgun.com/app/logs .
# You can send up to 300 emails/day from this sandbox server.
# Next, you should add your own domain so you can send 10,000 emails/month for free.

# You can change the to line in data to look like this:
  # "to": "Liz <someemailaddress@stuff.com>"

# authorizing recipients: https://help.mailgun.com/hc/en-us/articles/217531258-Authorized-Recipients


# LOGIN HELPERS ##########################################################

def get_login_attempts():
    """Creates or updates login count tracker in the session."""

    if session.get("login_count") is None:  # Checks whether key exists
        session["login_count"] = 1
    else:
        session["login_count"] += 1

    return session["login_count"]


def calc_attempts_remaining(login_count):
    """Taking in an integer count, Returns number of remaining attempts."""

    max_attempts = 4
    remaining = max_attempts - login_count
    return remaining


def update_session_for_good_login(user_id, displayname):
    """Takes in integer for user id, updates session, returns nothing."""
    session["user_id"] = user_id
    session["displayname"] = displayname
    session["is_logged_in"] = True
    session["login_count"] = 0

    print "Session updated; logged in."


def handle_bad_attempts(remaining):
    """Gives proper path after user attempts and fails to log in:
        - Takes in login attempts remaining
        - Sets the session key login
        - Gives user flash feedback
        - Returns a string for the template to render"""

    session["is_logged_in"] = False

    if remaining <= 0:   # handling for negative numbers... still
                         # testing to see if this is possible to create.
        flash("""PASSWORD SECURITY FEATURE PENDING.
             Login attempts not linked to IP address or a specific email.
              Does cache matter? This is complicated.""")
        template = "password-recovery.html"

    elif remaining == 1:
        stringy_remaining = str(remaining)
        flash("You have " + stringy_remaining +
              " attempt remaining before account is locked.")
        flash("""PASSWORD SECURITY FEATURE PENDING.
             Login attempts not linked to IP address or a specific email.
              Does cach matter? This is complicated.""")
        template = "login.html"

    else:  # separate path to make sure user flash feedback is plural
        stringy_remaining = str(remaining)
        flash("You have " + stringy_remaining +
              " attempts remaining before account is locked.")
        flash("""PASSWORD SECURITY FEATURE PENDING.
             Login attempts not linked to IP address or a specific email.
              Does cach matter? This is complicated.""")
        template = "login.html"

    return template


# AUTHORIZED FOR VIEW BY URL #############################################

# def is_valid_url(url_user_id, url_team_id=None):
#     """Checks for a valid url:
#         - checks user id in url against the user id in the session
#         - then, if needed, checks for a userteam relationship between the
#           user in the session and the given team id from the url
#     """

#     logged_in = is_logged_in()  # checks logged in

#     if logged_in:
#         u_id = get_user_id_from_session()

#         # checks the user id is valid for when we are not given a team id:
#         if u_id == url_user_id and not url_team_id:
#             return True

#         # continues if user id is valid and there is a team id:
#         elif u_id == url_user_id:
#             # It is the right user so far
#             userteam = query.get_userteam_object(u_id, url_team_id)
#             if userteam:
#                 return True

#     return False
