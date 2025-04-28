import calendar
import random

import fire  # type: ignore

from nova_act import ActError, NovaAct


def main(name: str = "single-2", random_month_range: int = 0) -> None:
    rng = random.Random(42)
    with NovaAct(
        starting_page=f"https://agi-emerge-webgym-public.s3.us-west-2.amazonaws.com/datepicker/{name}.html"
    ) as client:
        error_dates = []
        for i in range(1, 31):
            client.page.reload()
            try:
                if "range" in name:
                    month_num = rng.randint(max(1, 6 - random_month_range // 2), min(11, 6 + random_month_range // 2))
                    month_name1 = calendar.month_name[month_num]
                    month_name2 = calendar.month_name[month_num + 1]
                    client.act(
                        f"select the date range {month_name1} {i} to {month_name2} {i}. "
                        "make sure the date range is properly selected."
                    )
                    answer = client.page.locator("#webgym-answer").text_content()
                    print(f"{i} -> {answer}")
                    if (
                        answer
                        == f"Start Date - 2023-{month_num:02d}-{i:02d}, End Date - 2023-{month_num+1:02d}-{i:02d}"
                    ):
                        print("Correct!")
                        continue
                else:
                    month_num = rng.randint(max(1, 6 - random_month_range // 2), min(12, 6 + random_month_range // 2))
                    month_name = calendar.month_name[month_num]
                    client.act(f"select the date {month_name} {i}. make sure the date is properly selected.")
                    answer = client.page.locator("#webgym-answer").text_content()
                    print(f"{month_num}/{i} -> {answer}")
                    if answer == f"2023-{month_num:02d}-{i:02d}":
                        print("Correct!")
                        continue
            except ActError:
                print(f"Failed to select date {i}")

            error_dates.append(i)

    print(f"Accuracy: {(30 - len(error_dates)) / 30}")
    print(f"Error dates: {error_dates}")


if __name__ == "__main__":
    fire.Fire(main)
