from datetime import datetime

import fire  # type: ignore

from nova_act import NovaAct


def main() -> None:
    with NovaAct(starting_page="https://www.caltrain.com/?active_tab=route_explorer_tab") as client:
        formatted_time = datetime.now().strftime("%I:%M %p")
        client.act(
            "scroll down on the page to find the southbound table. "
            "make sure you scroll down all the way to see the san francisco row in the table.",
        )
        next_time = client.act(
            f"find the next time in the san francisco row that is after {formatted_time}. "
            "scroll right in the southbound table if necessary. return that time.",
        )
        print(f"Next time is {next_time}")


if __name__ == "__main__":
    fire.Fire(main)
