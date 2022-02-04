#!/usr/bin/env python3

from typing import List, Tuple, Dict
import typer
import os
import pandas as pd
import requests, json


def save_stratified_to_files(sdf, base_out):
    for group in sdf.group.unique():
        sdf_group = sdf[sdf.group == group]
        fname = base_out + str(group) + ".txt"
        # save kerberos to file
        with open(fname, "w") as f:
            for _, row in sdf_group.iterrows():
                f.write(row["kerberos"] + "\n")


def main(csv_in: str, base_out: str, N: int = 100):
    df = pd.read_csv(csv_in, sep=",")

    stratified_dfs = []

    df2 = df.copy()

    m = round(len(df2) / N)

    for i in range(m - 1):
        frac = 1 / (m - i)
        df_sample = df2.groupby("year", group_keys=False).apply(
            lambda x: x.sample(frac=frac)
        )
        stratified_dfs.append(df_sample)
        df2 = df2[~df2.index.isin(df_sample.index)]

    stratified_dfs.append(df2)

    for i, sdf in enumerate(stratified_dfs):
        stratified_dfs[i] = sdf.assign(group=i)

    sdf = pd.concat(stratified_dfs)

    save_stratified_to_files(sdf, base_out)


if __name__ == "__main__":
    typer.run(main)
