from concurrent.futures import ThreadPoolExecutor, as_completed

import fire  # type: ignore
import pandas as pd
from pydantic import BaseModel

from nova_act import ActError, NovaAct

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/133.0.0.0 Safari/537.36"
)


class House(BaseModel):
    address: str
    location: str
    price: int
    beds: int
    baths: float
    sq_ft: int


class HouseList(BaseModel):
    houses: list[House]


class CaltrainBiking(BaseModel):
    biking_time_hours: int
    biking_time_minutes: int
    biking_distance_miles: float


def add_biking_distance(house: House, caltrain_city: str, headless: bool) -> CaltrainBiking | None:
    with NovaAct(
        starting_page="https://maps.google.com/",
        headless=headless,
        tty=not headless,
        user_agent=USER_AGENT,
    ) as client:
        client.act(
            f"Search for {caltrain_city} Caltrain station, "
            f"then get biking directions from {house.address}, {house.location}"
        )
        result = client.act(
            "Return the shortest time and distance for biking", schema=CaltrainBiking.model_json_schema()
        )
        if not result.matches_schema:
            print(f"Invalid JSON {result=}")
            return None
        time_distance = CaltrainBiking.model_validate(result.parsed_response)
        return time_distance


def main(caltrain_city: str = "Redwood City", bedrooms: int = 2, baths: int = 1, headless: bool = False):
    with NovaAct(
        starting_page="https://www.redfin.com/",
        headless=headless,
        tty=not headless,
        user_agent=USER_AGENT,
    ) as client:
        client.act(
            "Close any cookie banners. "
            "Click the 'Rent' tab. "
            f"Search for homes near {caltrain_city}, CA, then filter for {bedrooms} bedrooms and {baths}+ baths. "
            "If results mode is 'Split', switch to 'List'. "
            "Then change the view from photos to table."
        )
        result = client.act("Return the currently visible table of houses", schema=HouseList.model_json_schema())

    if not result.matches_schema:
        print(f"Invalid JSON {result=}")
        return
    house_list = HouseList.model_validate(result.parsed_response)
    print(house_list)

    houses_with_biking = []
    with ThreadPoolExecutor() as executor:
        future_to_house = {
            executor.submit(add_biking_distance, house, caltrain_city, headless): house for house in house_list.houses
        }
        for future in as_completed(future_to_house.keys()):
            try:
                house = future_to_house[future]
                caltrain_biking = future.result()
                if caltrain_biking is not None:
                    houses_with_biking.append(house.model_dump() | caltrain_biking.model_dump())
                else:
                    houses_with_biking.append(house.model_dump())
            except ActError as exc:
                print(f"Skipping house due to error: {exc}")
                houses_with_biking.append(house.model_dump())

    houses_df = pd.DataFrame(houses_with_biking)
    closest_house_data = houses_df.sort_values(by=["biking_time_hours", "biking_time_minutes", "biking_distance_miles"])

    print()
    print("Biking time and distance:")
    print(closest_house_data.to_string())


if __name__ == "__main__":
    fire.Fire(main)
