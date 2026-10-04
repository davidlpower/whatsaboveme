from geopy.geocoders import Nominatim  # type: ignore[import-untyped]
from opensky_api import OpenSkyApi, TokenManager  # type: ignore[import-untyped]
from rich.console import Console
from rich.table import Table


def main() -> None:

    console = Console()

    country = input("First, which country interests you? ")
    city = input("Which city would you like to observe? ")

    token_manager = TokenManager.from_json_file("credentials.json")
    api = OpenSkyApi(token_manager=token_manager)
    bbox = city_bbox(f"{city}, {country}")
    states = api.get_states(bbox=bbox)

    table = Table(title=f"Aircraft over {city}")
    table.add_column("Call Sign", style="cyan", no_wrap=True)
    table.add_column("Origin Country")
    table.add_column("Lon", justify="right")
    table.add_column("Lat", justify="right")
    table.add_column("Alt (m)", justify="right")
    table.add_column("Speed (m/s)", justify="right")

    for s in states.states:
        table.add_row(
            (s.callsign or "").strip(),
            s.origin_country,
            f"{s.longitude:.4f}",
            f"{s.latitude:.4f}",
            f"{s.baro_altitude:.0f}" if s.baro_altitude is not None else "-",
            f"{s.velocity:.0f}" if s.velocity is not None else "-",
        )

    console.print(table)


def city_bbox(name: str) -> tuple[float, float, float, float]:
    geolocator = Nominatim(user_agent="whatsaboveme")
    location = geolocator.geocode(name)
    if location is None:
        raise ValueError(f"Could not find {name!r}")
    south, north, west, east = (float(v) for v in location.raw["boundingbox"])
    return south, north, west, east


if __name__ == "__main__":
    main()
