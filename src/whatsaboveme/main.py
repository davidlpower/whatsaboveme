from geopy.geocoders import Nominatim  # type: ignore[import-untyped]
from opensky_api import OpenSkyApi, OpenSkyStates, TokenManager
from rich.console import Console
from rich.table import Table


def main() -> None:

    print("1. Discover the aircraft above you.")
    print("2. Look-up a flight by ID.")
    choice = int(input("Please choose: "))

    console = Console()
    table = None
    token_manager = TokenManager.from_json_file("credentials.json")
    api = OpenSkyApi(token_manager=token_manager)

    match choice:
        case 1:
            location = input("Where would you like to observe? ")
            bbox = city_bbox(location)
            states = api.get_states(bbox=bbox)
            table = get_all_aircraft_above(location, states)

        case 2:
            icoa = input("Please enter a valid ICAO number: ")
            states = api.get_states(icao24=icoa.lower())
            table = get_specific_aircraft(icoa, states)

    console.print(table)


def city_bbox(name: str) -> tuple[float, float, float, float]:
    geolocator = Nominatim(user_agent="whatsaboveme")
    location = geolocator.geocode(name)
    if location is None:
        raise ValueError(f"Could not find {name!r}")
    south, north, west, east = (float(v) for v in location.raw["boundingbox"])
    return south, north, west, east


def fmt(value: float | None, digits: int = 0) -> str:
    return "-" if value is None else f"{value:.{digits}f}"


def get_all_aircraft_above(location: str, states: OpenSkyStates | None) -> Table:
    table = Table(title=f"Aircraft over {location}")
    table.add_column("ICAO", style="yellow", no_wrap=True)
    table.add_column("Call Sign", style="cyan", no_wrap=True)
    table.add_column("Origin Country")
    table.add_column("Lon", justify="right")
    table.add_column("Lat", justify="right")
    table.add_column("Alt (m)", justify="right")
    table.add_column("Speed (m/s)", justify="right")

    if states is None or not states.states:
        table.caption = "No aircraft found"
        return table

    for s in states.states:
        table.add_row(
            s.icao24.strip(),
            (s.callsign or "").strip(),
            s.origin_country,
            fmt(s.longitude, 4),
            fmt(s.latitude, 4),
            fmt(s.baro_altitude),
            fmt(s.velocity),
        )
    return table


def get_specific_aircraft(icao: str, states: OpenSkyStates | None) -> Table:
    table = Table(title=f"Aircraft {icao}")
    table.add_column("ICAO", style="yellow", no_wrap=True)
    table.add_column("Call Sign", style="cyan", no_wrap=True)
    table.add_column("Lon", justify="right")
    table.add_column("Lat", justify="right")
    table.add_column("Alt (m)", justify="right")
    table.add_column("Speed (m/s)", justify="right")
    table.add_column("On Ground", justify="right")
    table.add_column("Last Contact", justify="right")

    if states is None or not states.states:
        table.caption = "Not currently being received"
        return table

    for s in states.states:
        table.add_row(
            icao,
            (s.callsign or "").strip(),
            fmt(s.longitude, 4),
            fmt(s.latitude, 4),
            fmt(s.baro_altitude),
            fmt(s.velocity),
            "Yes" if s.on_ground else "No",
            str(s.last_contact),
        )
    return table


if __name__ == "__main__":
    main()
