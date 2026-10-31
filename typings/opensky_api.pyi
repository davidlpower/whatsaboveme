from collections.abc import Sequence

class TokenManager:
    def __init__(self, client_id: str, client_secret: str) -> None: ...
    def get_token(self) -> str: ...
    def auth_headers(self) -> dict[str, str]: ...
    @classmethod
    def from_json_file(cls, path: str) -> TokenManager: ...

class StateVector:
    icao24: str
    callsign: str | None
    origin_country: str
    time_position: int | None
    last_contact: int
    longitude: float | None
    latitude: float | None
    geo_altitude: float | None
    baro_altitude: float | None
    on_ground: bool
    velocity: float | None
    true_track: float | None
    vertical_rate: float | None
    squawk: str | None
    spi: bool
    position_source: int
    category: int
    def __init__(self, arr: Sequence[object]) -> None: ...

class OpenSkyStates:
    time: int
    states: list[StateVector] | None
    def __init__(self, states_dict: dict[str, object]) -> None: ...

class FlightData:
    icao24: str
    firstSeen: int
    estDepartureAirport: str | None
    lastSeen: int
    estArrivalAirport: str | None
    callsign: str | None
    def __init__(self, arr: Sequence[object]) -> None: ...

class Waypoint:
    time: int
    latitude: float | None
    longitude: float | None
    baro_altitude: float | None
    true_track: float | None
    on_ground: bool
    def __init__(self, arr: Sequence[object]) -> None: ...

class FlightTrack:
    icao24: str
    startTime: int
    endTime: int
    path: list[Waypoint]
    def __init__(self, arr: Sequence[object]) -> None: ...

class OpenSkyApi:
    def __init__(
        self,
        token_manager: TokenManager | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> None: ...
    def close(self) -> None: ...
    def __enter__(self) -> OpenSkyApi: ...
    def __exit__(self, *args: object) -> None: ...
    def get_states(
        self,
        time_secs: int = 0,
        icao24: str | list[str] | None = None,
        bbox: tuple[float, ...] = (),
    ) -> OpenSkyStates | None: ...
    def get_my_states(
        self,
        time_secs: int = 0,
        icao24: str | list[str] | None = None,
        serials: int | list[int] | None = None,
    ) -> OpenSkyStates | None: ...
    def get_flights_from_interval(self, begin: int, end: int) -> list[FlightData] | None: ...
    def get_flights_by_aircraft(self, icao24: str, begin: int, end: int) -> list[FlightData] | None: ...
    def get_arrivals_by_airport(self, airport: str, begin: int, end: int) -> list[FlightData] | None: ...
    def get_departures_by_airport(self, airport: str, begin: int, end: int) -> list[FlightData] | None: ...
    def get_track_by_aircraft(self, icao24: str, t: int = 0) -> FlightTrack | None: ...
