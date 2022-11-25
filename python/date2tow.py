from typing import Tuple

from datetime import date


def date2tow(data: list[int, int, int, int, int, int]) -> Tuple[int, int]:
    dd = date.toordinal(date(data[0], data[1], data[2])) - date.toordinal(
        date(2019, 4, 7)
    )
    week = dd // 7
    dow = dd % 7
    tow = dow * 86400 + data[3] * 3600 + data[4] * 60 + data[5]
    return week, tow
