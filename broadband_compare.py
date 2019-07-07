from typing import Dict, List, Union
import contextlib
import pandas
import os
import sqlite3
from dataclasses import dataclass
import unittest as test

"""The main purpose is to create a data lookup and visualisation tool for
which can be used by technicians. You're free to choose between
console task, web application or even GUI if you like."""

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@dataclass
class Inputdata:
    """Dataclass for typehints such that it's obvious what's coming in from the CLI arguments"""
    report: str = "full"
    location: str = ""
    comparison_location: str = ""
    max_dl_speed: int = 0
    min_dl_speed: int = 0
    min_ul_speed: int = 0
    max_ul_speed: int = 0
    csv = ""


"""Convert more memorable names to database names"""
translations = {"location": "",
                "max_dl_speed": "Maximum download speed (Mbit/s)",
                "min_dl_speed": "Minimum download speed (Mbit/s)",
                "max_ul_speed": "Maximum upload speed (Mbit/s)",
                "min_ul_speed": "Minimum upload speed (Mbit/s)",
                "avg_dl_speed": "Average download speed (Mbit/s)",
                "avg_ul_speed": "Average upload speed (Mbit/s)",
                }


class Database:
    def __init__(self):
        pass

    @staticmethod
    def load_csv(filename):
        dataset = pandas.read_csv(filename, encoding="ISO-8859-1")

        if hasattr(dataset, 'laua_name'):
            translations['location'] = "laua_name"
        elif hasattr(dataset, 'la_name'):
            translations['location'] = "la_name"

        with contextlib.closing(sqlite3.connect('locations.sqlite')) as conn:
            dataset.to_sql("dataset", conn, if_exists='replace')
            conn.commit()

        # Load the dataset, right now just simply load one however depending on the arguments passed / location
        # load both / one.

    @staticmethod
    def get_data(name, where=""):
        # simply pass the sql query to be executed and return the results.
        with contextlib.closing(sqlite3.connect('locations.sqlite')) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            if where:
                t = (where,)
                sql = f"SELECT * FROM dataset WHERE \"{translations.get(name)}\" = ? COLLATE NOCASE;"
                c.execute(sql, t)
                result = c.fetchall()
                try:
                    return result[0]
                except IndexError:
                    raise Exception(f"{where} not found in provided CSV")

            else:
                sql = f"SELECT \"{translations.get(name)}\" FROM dataset"
                c.execute(sql)
                return c.fetchall()


def calc_avg(data: List) -> float:
    accum = 0
    for x in data:
        for y in x:
            accum += y

    return accum / len(data)


def get_value(data: Dict, name: str) -> Union[int, str, float]:
    return data[translations.get(name)]


def main(user_data):
    print(user_data.location)
    database = Database()
    database.load_csv(user_data.csv)

    location = database.get_data(name="location", where=user_data.location)

    print(f"Your location: '{user_data.location.capitalize()}': download speed {user_data.max_dl_speed}Mb/s\n")
    if(user_data.max_dl_speed or user_data.report == "full"):
        dl_speed_all = database.get_data(name="avg_dl_speed")
        print(
            f"Average download speed of country: {int(calc_avg(dl_speed_all))}Mb/s.\n"
            f"Average download speed of {user_data.location.capitalize()}: {get_value(location, 'avg_dl_speed')}Mb/s\n"
            f"Max download speed of {user_data.location.capitalize()}: {get_value(location, 'max_dl_speed')}Mb/s\n"
            f"Min download speed of {user_data.location.capitalize()}: {get_value(location, 'min_dl_speed')}Mb/s\n"
        )

    if(user_data.max_ul_speed or user_data.report == "full"):
        ul_speed_all = database.get_data(name="avg_ul_speed")
        print(
            f"Average upload speed of country: {int(calc_avg(ul_speed_all))}Mb/s.\n"
            f"Average upload speed of {user_data.location.capitalize()}: {get_value(location, 'avg_ul_speed')}Mb/s\n"
            f"Max upload speed of {user_data.location.capitalize()}: {get_value(location, 'max_ul_speed')}Mb/s\n"
            f"Min upload speed of {user_data.location.capitalize()}: {get_value(location, 'min_ul_speed')}Mb/s\n"
        )

    if(user_data.comparison_location):
        compare_location = database.get_data(name="location", where=user_data.comparison_location)
        print(
            f"Average download speed of {user_data.comparison_location}: "
            f"{get_value(compare_location,'avg_dl_speed')}Mb/s"
        )


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Internet speed and bandwidth comparison tool")
    parser.add_argument("-f", dest="csv", help="location of the CSV to load", required=True, type=str)
    parser.add_argument("-l", "--location", nargs='+', dest="location", help="The location to perform internet "
                                                                  "analysis. E.g. Leicester", type=str, required=True)
    parser.add_argument("-d", "--max_download_speed", dest="max_dl_speed", help="Maximum download speed Mb/s "
                        "this connection e.g 50", type=int)
    parser.add_argument("--min_download_speed", dest="min_dl_speed", help="Minimum download speed in Mb/s.", type=int)
    parser.add_argument("-u", "--max_upload_speed", dest="max_ul_speed", help="Maximum upload speed in Mb/s", type=int)
    parser.add_argument("--min_upload_speed", dest="max_ul_speed", help="Minimum upload speed in Mb/s", type=int)

    parser.add_argument("--compare", dest="comparison_location", type=str, help="If supplied will compare your location"
                                                                                "to another location.")
    parser.add_argument("-r", "--report", dest="report", choices=["full", "short"], type=str, default='full')

    userdata = Inputdata()
    parser.parse_args(namespace=userdata)
    userdata.location = ' '.join(userdata.location)
    return userdata


if __name__ == '__main__':
    main(parse_args())


class Testavg(test.TestCase):

    def test_avg(self):
        r = [[1, 2, 3, 4, 5]]

        val = 0
        for x in r:
            for y in x:
                val += y

        val = val / len(r)

        self.assertEqual(calc_avg(r), val)


