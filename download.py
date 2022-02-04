#!/usr/bin/env python3

from typing import List, Tuple, Dict
import typer
import os
import pandas as pd
import requests, json


def ADDTL_INFO_URL(kerb_in: str):
    return "https://tlepeopledir.mit.edu/q/" + kerb_in


def get_additional_info(kerbs: List[str]) -> Tuple[List[Dict[str, str]], List[str]]:
    """
    Gets additional information for each kerberos from MIT LDAP.
    """
    out = []
    not_found = []
    for kerb in kerbs:
        print("Getting additional information for " + kerb)
        # query ADDL_INFO_URL for json
        r = requests.get(ADDTL_INFO_URL(kerb))
        # parse json
        data = json.loads(r.text)
        if len(data["result"]) == 0:
            print("ERROR: " + kerb + " not found in LDAP")
            print(data)
            not_found.append(kerb)
            continue
        for datap in data["result"]:
            try:
                our_data = {
                    "kerberos": datap["email_id"],
                    "first_name": datap["givenname"],
                    "last_name": datap["lastname"],
                    "year": datap["student_year"],
                    "department": datap["department"] if "department" in datap else "",
                }
            except:
                print("ERROR: " + kerb + " not found in LDAP")
                print(datap)
                not_found.append(kerb)
                continue
            out.append(our_data)

    return out, not_found


def chunks(l: List[str], n: int) -> List[List[str]]:
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i : i + n]


def save_kerb_infos_to_csv(kerb_infos: List[Dict[str, str]], csv_file: str):
    if not os.path.isfile(csv_file):
        with open(csv_file, "w") as f:
            f.write("kerberos,first_name,last_name,year,department\n")
            for i in kerb_infos:
                f.write(
                    i["kerberos"]
                    + ","
                    + i["first_name"]
                    + ","
                    + i["last_name"]
                    + ","
                    + i["year"]
                    + ","
                    + i["department"]
                    + "\n"
                )
    else:
        with open(csv_file, "a") as f:
            for i in kerb_infos:
                f.write(
                    i["kerberos"]
                    + ","
                    + i["first_name"]
                    + ","
                    + i["last_name"]
                    + ","
                    + i["year"]
                    + ","
                    + i["department"].replace(",", "")
                    + "\n"
                )


def get_additional_info_from_file_to_csv(
    kerbs_file: str, csv_file: str, not_found_file: str
):
    """
    Gets additional information for each kerberos from MIT LDAP.
    """
    with open(kerbs_file, "r") as f:
        kerbs = [line.strip() for line in f.readlines()]

    if os.path.isfile(csv_file):
        kerb_df = pd.read_csv(csv_file, sep=",")
        done_kerbs = set(kerb_df["kerberos"])
        kerbs = [k for k in kerbs if k not in done_kerbs]

    if os.path.isfile(not_found_file):
        with open(not_found_file, "r") as f:
            not_found_kerbs = [line.strip() for line in f.readlines()]
        kerbs = [k for k in kerbs if k not in not_found_kerbs]

    for kerbs_chunk in chunks(kerbs, 10):
        info, not_found = get_additional_info(kerbs_chunk)
        with open(not_found_file, "a") as f:
            for k in not_found:
                f.write(k + "\n")
        save_kerb_infos_to_csv(info, csv_file)


def main(kerb_in: str, info_csv: str, not_found_file: str):

    get_additional_info_from_file_to_csv(kerb_in, info_csv, not_found_file)


if __name__ == "__main__":
    typer.run(main)
