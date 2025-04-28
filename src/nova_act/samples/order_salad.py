"""Order your favorite Sweetgreen meal.

Requires specifying a user_data_dir for a browser that is logged in to order.sweetgreen.com
with an account that has a credit card and home address saved.

See README for how to set up user_data_dir.

Usage:
python -m nova_act.samples.order_salad [--order <salad name>] [--headless]
"""

import fire  # type: ignore

from nova_act import NovaAct


def main(user_data_dir: str, order: str = "Shroomami", headless: bool = False) -> None:
    with NovaAct(
        starting_page="https://order.sweetgreen.com",
        user_data_dir=user_data_dir,
        headless=headless,
    ) as nova:
        nova.act(
            "If there is a cookie banner, close it. "
            "Click Menu at the top of the page. "
            "Click Delivery on the sidebar. "
            "Select 'Home' address. "
            f"Scroll down and click on '{order}'. "
            "Click 'Add to Bag'. "
            "If visible, click 'Continue to bag', otherwise click the bag icon. "
            "Click 'Continue to checkout'. "
            "Select a 20% tip. "
            "Click 'Place Order'."
        )


if __name__ == "__main__":
    fire.Fire(main)
