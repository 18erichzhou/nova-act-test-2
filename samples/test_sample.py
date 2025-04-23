# Copyright 2025 Amazon Inc

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import fire  # type: ignore

from nova_act import NovaAct


def book_tennis_court(date, activity, time_of_day):
    """
    Book a court through the SF parks & rec system.

    Args:
        date (str): Date to book (e.g. "March 19 Wednesday")
        activity (str): Activity to book (e.g. "Tennis")
        time_of_day (str): Time of day preference (e.g. "Afternoon")
    """
    n = NovaAct(starting_page="https://www.rec.us/sfrecpark")
    n.start()
    n.act(f"update the Today selector to be {date} and press Done")
    n.act(f"update the Activities selector to be {activity} and then press Done")
    n.act(f"update the Time of day selector to be {time_of_day} and then press done")

    # Find and select latest time slot
    n.act(
        "among all the tennis courts shown on the page, find the time slot that is the latest in the day and select it"
    )

    # Book the slot
    n.act("book the slot you have selected")

    n.stop()


if __name__ == "__main__":
    fire.Fire(book_tennis_court)
