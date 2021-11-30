#!/usr/bin/env python3
"""
Python3 module to print out some metrics from Apple Health App XML export data.

This is based heavily on the HealthDataExtractor class from:
   https://github.com/markwk/qs_ledger/blob/master/apple_health/apple-health-data-parser.py

Example:
$ python3 health.py --file apple_health_export/export.xml --start 2021-07-01 --end 2021-07-31
Reading data from apple_health_export/export.xml . . . done
workoutDistance : 103.52 km
  totalDistance : 178.30 km
  workoutEnergy : 9163.99 Cal
     restEnergy : 82239.54 Cal
   activeEnergy : 25981.13 Cal
      stepCount : 213263 steps
"""
from __future__ import print_function

import sys
import re
import os
import argparse

from datetime import datetime, timedelta
from lxml import etree

__version__ = "0.1"


class HealthMetricsExtractor:
    """
    Extract metrics from health data in Apple Health App's XML export, export.xml.
    Inputs:
        path:      Relative or absolute path to export.xml
    Outputs:
        Simple text output
    """

    def __init__(self, path, dates):
        """
        Initialize the data object. Probably not very 'pythonic'
        """
        self.dates = {"start": dates[0], "end": dates[1]}
        self.nodes = []
        self.stats = {"workout": [], "overall": []}
        self.units = {"energy": "", "distance": "", "time": ""}
        self.directory = os.path.abspath(os.path.split(path)[0])
        print("Reading data from %s . . . " % path, end="")
        self.full = etree.parse(path)
        print("done")
        sys.stdout.flush()

        self.root = self.full.getroot()
        numRecords = 0
        devRecords = 0
        goodRecords = 0
        for record in self.root:
            numRecords += 1
            device = record.get("device")
            if device is not None and re.search("Apple Watch", device) is not None:
                devRecords += 1
                sDate = datetime.strptime(record.get("startDate")[:10], "%Y-%m-%d")
                eDate = datetime.strptime(record.get("endDate")[:10], "%Y-%m-%d")

                if sDate is not None and sDate >= self.dates["start"] and eDate is not None and eDate <= self.dates["end"]:
                    if record.get("workoutActivityType") is not None:
                        record.set("type", record.get("workoutActivityType"))
                    if record.get("type") is None:
                        pass
                    elif record.get("type") in "HKQuantityTypeIdentifierAppleExerciseTime":
                        pass
                    elif record.get("type") in "HKQuantityTypeIdentifierEnvironmentalAudioExposure":
                        pass
                    elif record.get("type") in "HKQuantityTypeIdentifierFlightsClimbed":
                        pass
                    elif "HKQuantityTypeIdentifierHeartRate" in record.get("type"):
                        pass
                    elif record.get("type") in "HKCategoryTypeIdentifierAppleStandHour":
                        pass
                    else:
                        goodRecords += 1
                        self.nodes.append(record)

        self.summarize_data()

    def summarize_data(self):
        """
        Summarize the data in the nodes
        """
        for record in self.nodes:
            if record.get("workoutActivityType") is not None:
                self.stats["workout"].append(record)
            else:
                self.stats["overall"].append(record)

        self.stats["workoutDistance"] = 0.0
        self.stats["totalDistance"] = 0.0
        self.stats["workoutEnergy"] = 0.0
        self.stats["workoutDuration"] = 0.0
        self.stats["restEnergy"] = 0.0
        self.stats["activeEnergy"] = 0.0
        self.stats["stepCount"] = 0

        for record in self.stats["workout"]:
            if record.get("totalDistance") is not None:
                self.stats["workoutDistance"] += float(record.get("totalDistance"))
                self.units["distance"] = record.get("totalDistanceUnit")
            if record.get("totalEnergyBurned") is not None:
                self.stats["workoutEnergy"] += float(record.get("totalEnergyBurned"))
                self.units["energy"] = record.get("totalEnergyBurnedUnit")
            if record.get("duration") is not None:
                self.stats["workoutDuration"] += float(record.get("duration"))
                self.units["time"] = record.get("durationUnit")

        for record in self.stats["overall"]:
            if record.get("type") == "HKQuantityTypeIdentifierDistanceWalkingRunning":
                self.stats["totalDistance"] += float(record.get("value"))
                self.units["distance"] = record.get("unit")
            if record.get("type") == "HKQuantityTypeIdentifierStepCount":
                self.stats["stepCount"] += int(record.get("value"))
            if record.get("type") == "HKQuantityTypeIdentifierBasalEnergyBurned":
                self.stats["restEnergy"] += float(record.get("value"))
                self.units["energy"] = record.get("unit")
            if record.get("type") == "HKQuantityTypeIdentifierActiveEnergyBurned":
                self.stats["activeEnergy"] += float(record.get("value"))
                self.units["energy"] = record.get("unit")

    def print_stats(self):
        """
        Print out the data
        """
        for k in self.stats:
            if k not in ("workout", "overall"):
                statUnit = "steps"
                if k in ("workoutDistance", "totalDistance"):
                    statUnit = self.units["distance"]
                if k in ("restEnergy", "activeEnergy", "workoutEnergy"):
                    statUnit = self.units["energy"]
                if k in ("workoutDuration", ""):
                    statUnit = self.units["time"]

                if isinstance(self.stats[k], float):
                    print("%15s : %s" % (k, str(format(self.stats[k], ".2f")) + " " + statUnit))
                else:
                    print("%15s : %s" % (k, str(self.stats[k]) + " " + statUnit))


def parse_dates(dates):
    """
    Parse the command-line dates into proper date-like objects
    """
    startdate = None
    enddate = None

    if dates.start is not None:
        if re.match(r"20\d{2}-\d{2}-\d{2}", dates.start) is not None:
            startdate = datetime.strptime(dates.start, "%Y-%m-%d")
        elif re.match(r"20\d{2}-\d{2}", dates.start) is not None:
            startdate = datetime.strptime(dates.start, "%Y-%m")

    if dates.end is not None:
        if re.match(r"20\d{2}-\d{2}-\d{2}", dates.end) is not None:
            enddate = datetime.strptime(dates.end, "%Y-%m-%d")
        elif re.match(r"20\d{2}-\d{2}", dates.end) is not None:
            enddate = datetime.strptime(dates.end, "%Y-%m")

    if dates.duration is not None:
        if startdate is not None and enddate is None:
            enddate = startdate + timedelta(days=dates.duration - 1)
        elif enddate is not None and startdate is None:
            startdate = enddate - timedelta(days=dates.duration - 1)
        elif enddate is None and startdate is None:
            enddate = datetime.strptime(
                datetime.strftime(datetime.now() - timedelta(days=1), "%Y-%m-%d"),
                "%Y-%m-%d",
            )
            startdate = enddate - timedelta(days=dates.duration)

    if startdate is None:
        startdate = datetime.strptime("1900-01-01", "%Y-%m-%d")
        enddate = datetime.strptime("9999-01-01", "%Y-%m-%d")

    return [startdate, enddate]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", action="store", default="./apple_health_export/export.xml")
    parser.add_argument("--start", action="store", help="Start Date to summarize from")
    parser.add_argument("--end", action="store", help="End Date to summarize to")
    parser.add_argument("--duration", action="store", type=int, help="Duration to summarize")
    args = parser.parse_args(sys.argv[1:])

    if hasattr(args, "help"):
        parser.print_help()
        sys.exit()

    date_args = parse_dates(args)

    data = HealthMetricsExtractor(args.file, date_args)
    data.print_stats()
