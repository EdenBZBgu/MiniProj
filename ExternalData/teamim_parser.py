import pandas as pd
from cachetools import cached, TTLCache

BOOK_CODES = {"gn": "Genesis", "ex": "Exodus", "lv": "Leviticus", "nu": "Numbers", "dt": "Deuteronomy"}


def get_pasuk_encoded_teamim(pasuk_id: str):
    teamim = load_torah_teamim()
    return teamim[pasuk_id].strip()


def parse_pasuk_id(pid):
    pid = pid.strip()
    book = BOOK_CODES.get(pid[:2])
    chapter, pasuk = pid[2:].split(":")
    return f"Tanakh.Torah.{book}.{chapter}.{pasuk}"


@cached(cache=TTLCache(maxsize=1, ttl=600))
def load_torah_teamim():
    df = pd.read_excel(
        "ExternalData/Teamim.xlsx",
        usecols=[1, 2],
        names=["pasuk_id", "teamim"],
        header=None,
    )
    df = df[df.pasuk_id.str[1:3].isin(BOOK_CODES.keys())]
    df.pasuk_id = df.pasuk_id.apply(parse_pasuk_id)
    return df.set_index("pasuk_id").to_dict()["teamim"]
