import os

import fire  # type: ignore

from nova_act import NovaAct


def main(starting_page: str, user_data_dir: str) -> None:
    os.makedirs(user_data_dir, exist_ok=True)

    with NovaAct(starting_page=starting_page, user_data_dir=user_data_dir, clone_user_data_dir=False):
        input("Set up the browser state and hit return when done")


if __name__ == "__main__":
    fire.Fire(main)
