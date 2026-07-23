from dataclasses import dataclass

@dataclass
class Unit:

    phase: str = ""
    block: str = ""
    level: str = ""
    unit: str = ""

    list_price: int | None = None
    
    spa_price: int | None = None
    net_price: int | None = None

    type: str = ""
    size: int | None = None
    psf: int | None = None

    bedroom: str = ""
    bathroom: str = ""

    carpark: str = ""
    orientation: str = ""

    status: str = ""
    remarks: str = ""
    
    
@dataclass
class Phase:

    name: str
    code: str
    blocks: list[str]