import fire  # type: ignore

from nova_act import NovaAct


def main(cdp_endpoint_url: str, username: str, date: str):
    # On MacOS, stop the chrome browser and restart it from the cmd line with:
    #
    # /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --args --remote-debugging-port=922
    #
    # then pass in the ws url into cdp_endpoint_url.
    with NovaAct(starting_page="https://ballard.amazon.com/", cdp_endpoint_url=cdp_endpoint_url) as client:
        # Go to the calendar page. Fragments get dropped by the auth redirect so we need to do this with a goto.
        client.go_to_url("https://ballard.amazon.com/owa/#path=/calendar/view/WorkWeek")

        # Add a calendar event.
        client.act(
            f"add a new event with the title {username}@ OOTO, check the box for all day, "
            f"select the start date to be {date}, show as 'busy' and save"
        )

        # Auto-reply.
        client.act("navigate to https://ballard.amazon.com/owa/")
        client.act(
            "click the settings gear icon to reveal a menu. "
            "it is the middle icon from the set of three icons on the top right. "
            "do not click on the question mark. then select automatic replies in the menu "
            "and return once the panel is open."
        )
        client.act("ensure send automatic replies is selected")
        client.act("fill the reply inside my organization with: Hi. I am out of office. Please contact my manager.")
        client.act("uncheck send automatic reply messages to senders outside my organization")
        client.act("click cancel to close")

        # Request time off.
        client.act("navigate to https://atoz.amazon.work/time")
        client.act(f"request time off and leave and select paid time off, then select {date} in the date picker")
        client.act(
            "click on the button that has the text 'next' below the calendar. do not click on the calendar. "
            "scroll down if necessary."
        )
        client.act("cancel")


if __name__ == "__main__":
    fire.Fire(main)
