from pathlib import Path

import pandas as pd


def noise_floor(path: Path) -> float:
    data = pd.read_pickle(path)
    minum = min(data)
    count = 0
    for point in data:
        count += (point < minum * 1.01)

    if count > 5:
        return minum
    else:
        return minum * 1.1

# desnt = Path('../Data/DFs/data11_dont_use/8 modes.pickle')

# nf = noise_floor(desnt)

# print(nf)
