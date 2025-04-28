"""Simple example of adding a coffee maker to the cart.

Usage:
python -m nova_act.samples.order_a_coffee_maker [--record_video]
"""

import fire  # type: ignore

from nova_act import NovaAct


def main(record_video: bool = False) -> None:
    with NovaAct(
        starting_page="https://www.amazon.com",
        record_video=record_video,
    ) as nova:
        nova.act("search for a coffee maker")
        nova.act("select the first result")
        nova.act("scroll down or up until you see 'add to cart' and then click 'add to cart'")


if __name__ == "__main__":
    fire.Fire(main)
