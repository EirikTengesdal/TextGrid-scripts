#!/usr/bin/env python3
"""Script for creating TextGrid files with interval labels from CSV input file.

File:
    CSVtoTextGrid.py

Author:
    Eirik Tengesdal, OsloMet – Oslo Metropolitan University

Email:
    eirik.tengesdal@oslomet.no
    eirik.tengesdal@iln.uio.no
    eirik@tengesdal.name

Licence:
    MIT License

    Copyright (c) 2024 Eirik Tengesdal

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
"""

import csv
import textgrid

# Load the CSV data
with open("C:/Users/eiten9710/OneDrive - OsloMet/Documents/" + \
        "Github/TextGrid-scripts/textgrids/response_df.csv",
          "r", encoding="utf-8-sig") as f:  # If `utf-8 BOM` encoded
    reader = csv.DictReader(f,
                            delimiter=";"  # If semicolon separated, not comma
                            )
    data = [row for row in reader]

# Group data by participant
participants = {}
for row in data:
    participant = row["participant"]
    if participant not in participants:
        participants[participant] = []
    participants[participant].append(row)

# Create a TextGrid for each participant
for participant, rows in participants.items():
    # Create a TextGrid object
    tg = textgrid.TextGrid()

    # Create an IntervalTier object
    respons_tier = textgrid.IntervalTier(name="response")

    # Populate the interval tier
    for row in rows:
        start_time = float(row["start_time"])
        end_time = float(row["end_time"])
        label = row["response"]
        respons_tier.add(start_time, end_time, label)

    # Add the interval tier to the TextGrid
    tg.append(respons_tier)

    # Write the TextGrid to a file
    with open("C:/Users/eiten9710/OneDrive - OsloMet/Documents/"
        "Github/TextGrid-scripts/textgrids/"
        f"{participant}.TextGrid", "w", encoding="utf-8") as f:
        tg.write(f)
