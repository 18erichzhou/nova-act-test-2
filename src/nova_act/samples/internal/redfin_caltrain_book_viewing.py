from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date

import fire  # type: ignore
import pandas as pd
from pydantic import BaseModel

from nova_act import ActError, NovaAct


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
    biking_time_minutes: int
    biking_distance_miles: float


class HouseWithBiking(BaseModel):
    address: str
    location: str
    price: int
    beds: int
    baths: float
    sq_ft: int
    biking_time_minutes: int | None = None  # Made optional
    biking_distance_miles: float | None = None  # Made optional


class RequestedShowing(BaseModel):
    date: date


def add_biking_distance(house: House, caltrain_city: str) -> CaltrainBiking | None:
    with NovaAct(starting_page="https://maps.google.com/") as client:
        client.act(
            f"Search for {caltrain_city} Caltrain station, "
            f"then get biking directions from {house.address}, {house.location}"
        )
        result = client.act(
            "Return the shortest time and distance for biking, or max values if no valid route is found",
            schema=CaltrainBiking.model_json_schema(),
        )
        if not result.matches_schema:
            print(f"Invalid JSON {result=}")
            return None
        return CaltrainBiking.model_validate(result.parsed_response)


def request_showing(house: HouseWithBiking, user_data_directory: str) -> RequestedShowing | None:
    with NovaAct(starting_page="https://www.redfin.com/", user_data_dir=user_data_directory) as client:
        client.act(
            f"Close any cookie banners. "
            f"Search for {house.address}, {house.location} and request a showing for this Saturday"
        )
        result = client.act("Return the date for the showing appointment", schema=RequestedShowing.model_json_schema())

        if not result.matches_schema:
            print(f"Invalid JSON {result=}")
            return None
        return RequestedShowing.model_validate(result.parsed_response)


def main(caltrain_city: str = "Redwood City", bedrooms: int = 2, baths: int = 1):
    user_data_directory = input("Input User Data Directory: ")
    with NovaAct(
        starting_page="https://www.redfin.com/",
        # headless=True,
    ) as client:
        client.act(
            "Close any cookie banners. "
            f"Search for homes near {caltrain_city}, CA, then filter for {bedrooms} bedrooms and {baths}+ baths. "
            "In 'All filters', filter for 'Open House'. "
            "If results mode is 'Split', switch to 'List'. "
            "Then change the view from photos to table.",
            timeout=240,
        )
        result = client.act("Return the currently visible table of houses", schema=HouseList.model_json_schema())

    if not result.matches_schema:
        print(f"Invalid JSON {result=}")
        return None

    house_list = HouseList.model_validate(result.parsed_response)

    houses_with_biking = []
    with ThreadPoolExecutor() as executor:
        future_to_house = {
            executor.submit(add_biking_distance, house, caltrain_city): house for house in house_list.houses
        }
        for future in as_completed(future_to_house.keys()):
            try:
                house = future_to_house[future]
                caltrain_biking = future.result()

                # Use model_validate
                house_data = house.model_dump()
                if caltrain_biking:
                    house_data.update(caltrain_biking.model_dump())

                house_with_biking = HouseWithBiking.model_validate(house_data)
                houses_with_biking.append(house_with_biking)

            except ActError as exc:
                print(f"Skipping house due to error: {exc}")
                houses_with_biking.append(HouseWithBiking.model_validate(house.model_dump()))

    houses_df = pd.DataFrame([house.model_dump() for house in houses_with_biking])

    print("\nBiking time and distance:")
    print(houses_df.to_string())

    if houses_df.empty:
        print("No valid houses found.")
        return

    closest_house_data = houses_df.sort_values(by=["biking_time_minutes", "biking_distance_miles"]).iloc[0].to_dict()
    closest_house = HouseWithBiking.model_validate(closest_house_data)

    print("\nClosest House:")
    print(closest_house)

    requested_showing = request_showing(closest_house, user_data_directory)
    if requested_showing:
        print(f"Requested showing at {closest_house.address} for {requested_showing.date.strftime('%m/%d/%Y')}")
    else:
        print(
            f"Could not request showing for {closest_house.address} due to scheduling conflicts or availability issues."
        )


if __name__ == "__main__":
    fire.Fire(main)
