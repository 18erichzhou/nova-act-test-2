from nova_act import NovaAct


def run1(starting_page):
    """
    This does not always pick the lowest price.
    """
    with NovaAct(starting_page=starting_page) as client:
        client.act("find black friday deals for macbook pro with 16 GB memory. make sure to hit enter.")
        client.act("go to the site of the retailer, and pick the option with the lowest price listed ")


def run2(starting_page):
    """
    This fails with an error.
    """
    with NovaAct(starting_page=starting_page) as client:
        prompt = (
            "Make sure you hit enter when needed. First, find black "
            "friday deals for Macbook pro with 16 GB Memory. Second, find the "
            "retailer that has the lowest price listed. Third, go to the "
            "retailer's site, and add the item to checkout."
        )
        client.act(prompt)


if __name__ == "__main__":
    run1("https://google.com/")
    print("Done.")
