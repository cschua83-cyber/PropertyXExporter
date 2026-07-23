from src.models import Unit
from config import (
    STANDARD_DISCOUNT,
    EARLY_BIRD_DISCOUNT,
    MOT_DISCOUNT,
    SPA_ROUNDING,
    PROGRESSIVE_DISCOUNT,
)

def calculate_prices(unit: Unit):

    if unit.list_price is None:
        return

    unit.spa_price = round(
        unit.list_price
        * STANDARD_DISCOUNT
        * EARLY_BIRD_DISCOUNT
        * MOT_DISCOUNT,
        SPA_ROUNDING,
    )

    unit.net_price = round(
        unit.spa_price
        * PROGRESSIVE_DISCOUNT
    )

    if unit.size is not None:
        unit.psf = round(
            unit.list_price / unit.size
        )