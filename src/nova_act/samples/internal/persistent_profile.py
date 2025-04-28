import fire

from nova_act import NovaAct


def main(browser_profile_dir: str, quiet: bool = True, headless: bool = True) -> None:
    classes_with_homework: dict[str, str] = {}
    with NovaAct(
        starting_page="https://classroom.google.com",
        user_data_dir=browser_profile_dir,
        headless=headless,
        quiet=quiet,
    ) as client:
        class_list = client.act(
            "return the title of all the items in the left sidebar in an array of strings. "
            + "only include items that have a round colorful icon."
        )
        assert isinstance(class_list, list), f"class_list not a list {class_list}"
        for class_ in class_list:
            print(f"Getting status for class {class_}")
            client.act(f"click on {class_} in the left sidebar")
            upcoming_text = client.act(
                "return the text in the upcoming box. only return the text between upcoming and view all."
            )
            assert isinstance(upcoming_text, str), f"upcoming_text not a str {upcoming_text}"
            if not upcoming_text.startswith("Woohoo"):
                classes_with_homework[class_] = upcoming_text

    print(classes_with_homework)


if __name__ == "__main__":
    fire.Fire(main)
