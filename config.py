from src.models import Phase


PHASE_3A = Phase(
    name="Phase 3A",
    code="3A",
    blocks=[
        "C1",
    ],
)

PHASE_3B = Phase(
    name="Phase 3B",
    code="3B",
    blocks=[
        "C2-1",
        "C2-2",
        "C2-3",
    ],
)

PHASE_3C = Phase(
    name="Phase 3C",
    code="3C",
    blocks=[
        "C3-1",
        "C3-2",
    ],
)

ALL_PHASES = [
    PHASE_3A,
    PHASE_3B,
    PHASE_3C,
]

CURRENT_PHASE = PHASE_3A


def get_phase_code():
    return CURRENT_PHASE.code


# ==========================
# Scraper Settings
# ==========================

WAIT_TIMEOUT = 10

DETAIL_MAX_RETRY = 5

DETAIL_RETRY_DELAY = 0.5

SCROLL_DELAY = 2

DETAIL_OPEN_DELAY = 1

DETAIL_CLOSE_DELAY = 1.5