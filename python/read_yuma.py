import numpy as np


def read_yuma(almanac_file: str) -> np.ndarray:
    if almanac_file:
        alm = open(almanac_file)

        alm_lines = alm.readlines()
        all_sat = []
        for idx, value in enumerate(alm_lines):
            if value[0:3] == "ID:":
                one_sat_block = alm_lines[idx : idx + 13]
                one_sat = []
                for line in one_sat_block:
                    data = line.split(":")
                    one_sat.append(float(data[1].strip()))
                all_sat.append(one_sat)
        alm.close()
        all_sat = np.array(all_sat)

        return all_sat
