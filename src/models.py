from dataclasses import dataclass


@dataclass
class Unit:

    phase: str = ""
    block: str = ""
    level: str = ""
    unit: str = ""

    price: str = ""

    type: str = ""
    size: str = ""

    bedroom: str = ""
    bathroom: str = ""

    carpark: str = ""
    orientation: str = ""

    status: str = ""
    remarks: str = ""