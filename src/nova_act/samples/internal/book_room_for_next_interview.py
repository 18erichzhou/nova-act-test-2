import json

from nova_act import NovaAct

with NovaAct(
    starting_page="https://ballard.amazon.com/owa/viik@amazon.com/#path=/mail", record_video=True, logs_directory="."
) as client:
    _ = input("Please log into midway and press ENTER when done:")

    client.act("open the calendar through the menu button")
    client.act(
        "navigate to next week "
        "(not month - don't use the two arrows above 30-day view, use left/right arrows above week view)"
    )
    # next_phone_screen_date_time = client.act("return when (date and time) my next phone screen is scheduled")

    client.act("check out the details of my phone screen")
    event_details_info = client.act(
        "return the phone screen date time as JSON with fields 'date', 'startTime', 'endTime'"
    )
    next_phone_screen_deets = json.loads(event_details_info.response or "{}")

    client.go_to_url("https://meetings.amazon.com/#/")

    client.act("navigate to room booking through the menu")

    client.act("select building SFO19 (type and pick from dropdown options), floor 7")

    # client.act(f"select date the date and the start time "
    # f"(click on time, find in dropdown, then select) - {next_phone_screen_date_time} (ignore end time)")
    client.act(f"select the start date to be {next_phone_screen_deets['date']}")
    client.act(f"select the start time to be {next_phone_screen_deets['startTime']}")

    client.act("in the more options, select 1hr duration")

    client.act(
        f"pick the first available room option for the start time {next_phone_screen_deets['startTime']}"
        "(need to click the table cell corresponding to room and time)"
    )

    client.act("reserve it!")
