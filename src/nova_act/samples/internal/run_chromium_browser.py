from nova_act import NovaAct


def main():
    # Initialize the client with chrome channel
    n = NovaAct(
        starting_page="https://amazon.com/",  # Replace with desired starting page
        chrome_channel="chromium",  # Specify to run in Chrome. Chromium is the default
    )

    n.start()
    n.act("search for a coffee maker")  # Replace with whatever natural language act
    n.stop()


if __name__ == "__main__":
    main()
