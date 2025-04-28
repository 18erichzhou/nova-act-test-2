from nova_act import NovaAct


def get_user_input():
    """
    Prompts user for zip code and search term.

    Returns:
        tuple: (zip_code, search_term)
    """
    while True:
        zip_code = input("Enter your zip code (5 digits): ").strip()
        if zip_code.isdigit() and len(zip_code) == 5:
            break
        print("Invalid zip code. Please enter a 5-digit number.")

    search_term = input("What product would you like to search for? ").strip()
    while not search_term:
        search_term = input("Please enter a valid search term: ").strip()

    return zip_code, search_term


def run_fresh_demo(zip_code=None, search_term=None):
    """
    Demo for updating a zip code and inputting a search term

    Args:
        zip_code (str): Delivery location zip code
        search_term (str): Item to search for
    """
    if zip_code is None or search_term is None:
        zip_code, search_term = get_user_input()

    with NovaAct(
        starting_page="https://www.amazon.com/fresh",
    ) as client:
        # Set delivery location
        client.act(f"change my location to {zip_code}")

        # Search for product
        client.act(f"search for {search_term}")


if __name__ == "__main__":
    # Run with user input
    run_fresh_demo()

    # Alternatively, you can still run with specific values:
    # run_fresh_demo(zip_code="02142", search_term="tomato")
