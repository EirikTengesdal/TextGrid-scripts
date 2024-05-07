#!/usr/bin/env python3
"""Script for generating or modifying TextGrid files.

This Python script is made for the purpose of generating TextGrid files based
on CSV input data for audio files to be forced alignment (Autophon.se). Then,
based on these, we modify the TextGrids to include specified tiers for
subsequent manual prosodic annotation. The script allows the user to choose
whether or not to run the TextGrid generation and/or modification. The script
also features translation of `realization` labels in Norwegian into English via
Google Translate.

File:
    TextGrid_script.py

Author:
    Eirik Tengesdal¹˒²

Affiliations:
    ¹ OsloMet – Oslo Metropolitan University (Assistant Professor of Norwegian)
    ² University of Oslo (Guest Researcher of Linguistics)

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

# =============================================================================
# Acknowledgements
# Parts of the script have been developed with the aid from Copilot (2024) and
# Sikt KI-chat (2024). Stack Overflow and GitHub pages have been helpful.
# In particular, the following have been influential:
# https://github.com/timmahrt/praatIO/blob/main/tutorials/tutorial1_intro_to_praatio.ipynb
# https://stackoverflow.com/a/67874518/17082981
#
# Parts also build on related versions of the same script.
# =============================================================================

# =============================================================================
# References
# GitHub. (2024). GitHub Copilot [Large language model].
#     https://github.com/features/copilot
# Sikt. (2024). Sikt KI-chat (GPT-4-8k version) [Large language model].
#     https://ki-chat.sikt.no/
# =============================================================================

# %% Step 0: Initialise script

# %%% 0.1: Import dependencies
import csv
import ffmpeg  # If script aborts on error, try: `pip install ffmpeg-python`
import os
from googletrans import Translator
# If error, try: `pip install googletrans==4.0.0rc1`
from praatio import textgrid  # If error, try: `pip install praatio`
from os.path import join


# %%% 0.2: Choose whether to generate and/or modify TextGrids
generate_new_textgrids_enabled = True if input(
    "Generate new TextGrids from "
    "CSV input ([y]/n)?: ").lower().strip() == "y" else False

modify_textgrids_enabled = True if input(
    "Modify TextGrids ([y]/n)?: ").lower().strip() == "y" else False

print("\n")
# %%% 0.2: Define functions
if modify_textgrids_enabled:
    # Populate `prosodic_unit` tier with 'σ' when `word` entries are not `''`
    def prosodic_word(s):
        if not s:
            return ""
        return "σ"

    # Google Translate API for automatic translation of `realization` strings
    translator = Translator()

    def translate_entry(s, src_lang="no", dest_lang="en"):
        if not s:
            return s
        return translator.translate(s,
                                    src=src_lang,
                                    dest=dest_lang).text


# %% 1: Generate TextGrids from CSV input data
# %%% 1.1: Define input and output paths
if generate_new_textgrids_enabled:
    input_path = "C:/Users/eiten9710/OneDrive - OsloMet/Documents/" + \
        "Github/TextGrid-scripts/"

    output_path = "C:/Users/eiten9710/OneDrive - OsloMet/Documents/" + \
        "Github/TextGrid-scripts/textgrids/"

    if not os.path.exists(output_path):
        os.mkdir(output_path)


# %%% 1.2: Load the CSV data
if generate_new_textgrids_enabled:
    with open(f"{input_path}realization.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        data = [row for row in reader]

# %%% 1.3: Obtain audio file duration for TextGrid interval durations
# Here we obtain information about the audio file's duration, as value for the
# `maxTime` argument of TextGrid IntervalTier objects.

# %%% 1.4: Define `audio_input_path`
# Specify another path if the audio files are not in `input_path`
if generate_new_textgrids_enabled:
    audio_input_path = input_path

    # Define `textgrid_output_path` if different from output_path
    textgrid_output_path = join(audio_input_path, "textgrids/")

    if not os.path.exists(textgrid_output_path):
        os.mkdir(textgrid_output_path)
        print(f"Created directory '{textgrid_output_path}'!")

# %%% 1.5: Obtain duration of audio files (within folder), populate TextGrids
# This option presupposes (a) that audio files are already prepared, (b) that
# you will generate new TextGrids for these, and (c) that the input data has
# some sort of interval information. Here, `end_time equals `duration` because
# the audio files per participants have been sliced per trial item. If the
# audio file on the other hand is long/contains more intervals than just one,
# the code for `start_time` and `end_time` should be adjusted accordingly.
if generate_new_textgrids_enabled:
    # duration_list = []
    for filename in os.listdir(audio_input_path):
        name, ext = os.path.splitext(filename)
        if ext != ".wav":  # Specify different audio file extension if needed
            continue
        print(f"Generating new TextGrid based on audio '{filename}' located "
              f"in '{audio_input_path}'.")

        # Find duration, store values in list for any subsequent use or export
        duration = str(float(ffmpeg.probe(join(audio_input_path,
                                               filename))["format"]["duration"]))
        # duration_list.append({"filename": filename, "duration": duration})

        # Create a TextGrid object
        tg = textgrid.Textgrid()

        # Create an IntervalTier object for realization and other variables
        realization_tier = textgrid.IntervalTier(
            "realization", [], 0, duration)

        # Add `realization_tier` to the TextGrid object
        tg.addTier(realization_tier)

        # Make loop groups for intervals specific to audio file and participant
        groups = {}
        for row in data:
            audio_filename = row["audio_filename"]
            participant = row["participant"]
            key = (audio_filename, participant)
            if key not in groups:
                groups[key] = []
            groups[key].append(row)

        # Loop through data from CSV for populating audio specific intervals
        for (audio_filename, participant), rows in groups.items():
            if audio_filename != filename:
                continue

            # Populate the `realization` IntervalTier object
            for row in rows:
                start_time = 0
                end_time = float(row["duration"].replace(
                    ",", "."))  # decimal sep
                label = row["realization"]
                realization_entry = [start_time, end_time, label]

                # Add the IntervalTier to the TextGrid
                realization_tier.insertEntry(realization_entry)

            # Write the TextGrid to a file (here naming with `audio_filename`)
            tg.save(join(textgrid_output_path, name + ".TextGrid"),
                    # format="short_textgrid",
                    format="long_textgrid",
                    includeBlankSpaces=True)
            print(f"Saved '{name}.TextGrid' to "
                  f"'{textgrid_output_path}'.\n")

    print("Generated all TextGrids!\n")

# %% 2: Modify forced aligned TextGrids and populate with new tiers

# %%% 2.1: Define input and output paths
if modify_textgrids_enabled:
    modified_textgrid_input_path = "C:/Users/eiten9710/OneDrive - OsloMet/" + \
        "Documents/Github/TextGrid-scripts/fa_textgrids/"

    # Define `textgrid_output_path` if different from output_path
    modified_textgrid_output_path = join(modified_textgrid_input_path,
                                         "modified_textgrids/")

    if not os.path.exists(modified_textgrid_output_path):
        os.mkdir(modified_textgrid_output_path)
        print(f"Created directory '{modified_textgrid_output_path}'!")

# %%% 2.2: Populate each TextGrid with new tiers and modify existing ones
# The Autophon.se Forced Aligner outputs the following three tiers:
# (1): `[input tier] - phone`;
# (2): `[input tier] - word`;
# (3): `[input tier]- trans`

# In the present case, [input tier] is `realization`. We will rename these.
if modify_textgrids_enabled:
    for textgrid_filename in os.listdir(modified_textgrid_input_path):
        ext = os.path.splitext(textgrid_filename)[1]
        if ext != ".TextGrid":
            continue

        print(f"Modifying '{textgrid_filename}' located in "
              f"'{modified_textgrid_input_path}'.")

        # Open the TextGrid
        tg = textgrid.openTextgrid(f"{modified_textgrid_input_path}"
                                   f"{textgrid_filename}",
                                   includeEmptyIntervals=True)

        # Rename the `realization - phone` tier to `phone`
        tg.renameTier("realization - phone",
                      "phone")

        # Rename the `realization - word` tier to `word`
        tg.renameTier("realization - word",
                      "word")
        word_tier = tg.getTier("word")

        # Add `realization` based on `realization - trans`
        rem_realization_tier = tg.getTier("realization - trans")
        realization_tier = rem_realization_tier.new(name="realization")
        translation_entries = [(start, stop, translate_entry(label,
                                                             src_lang="no",
                                                             dest_lang="en"))
                               for start, stop, label in realization_tier.entries]

        tg.addTier(realization_tier)
        rem_realization_tier = tg.removeTier("realization - trans")

        # Translate `realization` tier into English, add to `translation` tier
        translation_entries = [(start, stop, translate_entry(label,
                                                             src_lang="no",
                                                             dest_lang="en"))
                               for start, stop, label in realization_tier.entries]
        translation_tier = realization_tier.new(name="translation (Google)",
                                                entries=translation_entries)

        tg.addTier(translation_tier)

        # Duplicate the `word` tier and create new `prosodic_unit` (`σ`) tier
        prosodic_unit_entries = [(start, stop, prosodic_word(label))
                                 for start, stop, label in word_tier.entries]
        prosodic_unit_tier = word_tier.new(name="prosodic unit",
                                           entries=prosodic_unit_entries)

        tg.addTier(prosodic_unit_tier)

        # Now, simply add any new empty tiers
        stress_tier = textgrid.PointTier(
            "stress (PS|SS|0)", [], minT=0, maxT=tg.maxTimestamp)
        emphasis_tier = textgrid.PointTier(
            "emphasis (E)", [], minT=0, maxT=tg.maxTimestamp)
        comment_tier = textgrid.IntervalTier(
            "comment", [], minT=0, maxT=tg.maxTimestamp)
        # minT=realization_tier.entries[0][0],
        # maxT=realization_tier.entries[0][1])

        tg.addTier(stress_tier)
        tg.addTier(emphasis_tier)
        tg.addTier(comment_tier)

        # Write the TextGrid to a file (here naming with `audio_filename`)
        tg.save(join(modified_textgrid_output_path,
                     textgrid_filename),
                # format="short_textgrid",
                format="long_textgrid",
                includeBlankSpaces=True)
        print(f"Saved '{textgrid_filename}' to "
              f"'{modified_textgrid_output_path}'.\n")

    print("Modified all TextGrids!")
