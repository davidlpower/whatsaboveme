from geopy.geocoders import Nominatim  # type: ignore[import-untyped]
from opensky_api import OpenSkyApi, TokenManager  # type: ignore[import-untyped]
from rich.console import Console
from rich.table import Table


def main() -> None:

    print("1. Discover the aircraft above you.")
    print("2. Look-up a flight by ID.")
    choice = int(input("Please choose: "))

    console = Console()
    token_manager = TokenManager.from_json_file("credentials.json")
    api = OpenSkyApi(token_manager=token_manager)

    match choice:
        case 1:
            location = input("Where would you like to observe? ")
            bbox = city_bbox(location)
            states = api.get_states(bbox=bbox)

            table = Table(title=f"Aircraft over {location}")
            table.add_column("ICAO", style="yellow", no_wrap=True)
            table.add_column("Call Sign", style="cyan", no_wrap=True)
            table.add_column("Origin Country")
            table.add_column("Lon", justify="right")
            table.add_column("Lat", justify="right")
            table.add_column("Alt (m)", justify="right")
            table.add_column("Speed (m/s)", justify="right")

            for s in states.states:
                table.add_row(
                    (s.icao24 or "").strip(),
                    (s.callsign or "").strip(),
                    s.origin_country,
                    f"{s.longitude:.4f}",
                    f"{s.latitude:.4f}",
                    f"{s.baro_altitude:.0f}" if s.baro_altitude is not None else "-",
                    f"{s.velocity:.0f}" if s.velocity is not None else "-",
                )
        case 2:
            icoa = input("Please enter a valid ICAO number: ")
            states = api.get_states(icao24=icoa.lower())

            table = Table(title=f"Aircraft {icoa}")
            table.add_column("ICAO", style="yellow", no_wrap=True)
            table.add_column("Call Sign", style="cyan", no_wrap=True)
            table.add_column("Lon", justify="right")
            table.add_column("Lat", justify="right")
            table.add_column("Ground", justify="right")
            table.add_column("Last Contact", justify="right")

            for s in states.states:
                table.add_row(
                    icoa,
                    (s.callsign or "").strip(),
                    f"{s.longitude:.4f}",
                    f"{s.latitude:.4f}",
                    f"{s.baro_altitude:.0f}" if s.baro_altitude is not None else "-",
                    f"{s.velocity:.0f}" if s.velocity is not None else "-",
                    f"{(s.on_ground)}" if s.on_ground is not False else "-",
                    f"{(s.last_contact)}" if s.last_contact is not None else "-",
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
