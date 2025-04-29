import sys
from getpass import getpass

from nova_act import NovaAct

"""
Routine For taking CLI input and logging a user in to Hyperion.
Outputs the cookies needed to make an authenticated call to Hyperion.

Powered by Playwright in a headless browser.
Set headless mode to False to debug the flow if DOM of Auth Portal has changed.

https://quip-amazon.com/Me5nAaX1hs1p/SDK-Extension-Hyperion-Informal-Auth-Solution

Usage: python -m nova_act.internal.hyperion
"""

with NovaAct(starting_page="https://nova-preprod.aka.amazon.com/chat", headless=True) as client:
    page = client._playwright.context.new_page()

    try:
        client.go_to_url("https://nova-preprod.aka.amazon.com/chat")
    except Exception:
        print("Failed to load https://nova-preprod.aka.amazon.com/chat. Are you on VPN?")
        sys.exit()

    if "Sorry, your passkey isn't working" in page.content():
        email_input = page.get_by_role("textbox", name="email")
        email = input("Enter your email: ")
        email_input.fill(email)

        continue_button = page.locator("input#continue")
        continue_button.click()

        page.wait_for_url("https://nova-preprod.aka.amazon.com/ap/signin")

        password_input = page.get_by_role("textbox", name="password")
        password = getpass("Enter your password: ")
        password_input.fill(password)

        signin_button = page.locator("input#signInSubmit")
        signin_button.click()

        page.wait_for_url("https://nova-preprod.aka.amazon.com/chat")

        print("Successfully logged in")
    else:
        print("Already logged in")

    print("\n=== Obtained Hyperion Cookies ===")
    for cookie in page.context.cookies():
        if cookie["domain"] in ["nova-preprod.aka.amazon.com", ".amazon.com"]:
            print(cookie["name"], ":", cookie["value"])
