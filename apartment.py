from typing import TypedDict


class Apartment(TypedDict):
    addr: str
    floor: str
    price: float
    rooms: float
    sqm: float
    timeframe: str
    wbs: str
    year: str
    link: str
    image: str

