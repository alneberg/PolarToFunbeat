#!/usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import xmltodict
import pandas as pd

def main(args):
    with open(args.polarxml, 'r') as xml_input:
        doc = xmltodict.parse(xml_input)
    exercises = {}
    for i, exercise in enumerate(doc['polar-exercise-data']['calendar-items']['exercise']):
        exercise_d = {}
        exercise_d['Träningstyp'] = exercise["sport"]
        exercise_d['Datum'] = exercise['time'].split(" ")[0]
        h, m, s = exercise['result']['duration'].split(":") 
        if int(h) != 0:
            minutes = int(h)*60 + int(m)
        else:
            minutes = int(m)
        exercise_d['Minuter'] = minutes
        exercise_d['Sekunder'] = float(s)
        exercises[i] = exercise_d
    df = pd.DataFrame.from_dict(exercises, orient="index")
    df.to_csv(args.output_file)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("polarxml", 
            help=("XML file containing training data, e.g. "
                "a file extracted from polarpersonaltrainer.com."))
    parser.add_argument("output_file",
            help=("Output csv file that will be created or "
                "over written."))
    args = parser.parse_args()
    main(args)

