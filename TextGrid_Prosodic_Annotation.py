#!/usr/bin/env python3
"""Script for generating or modifying TextGrid files.

This Python script was adapted 08.05.2024 based on `TextGrid_script.py` to
modify TextGrids for prosodic annotation.

File:
    TextGrid_Prosodic_Annotation.py

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
import os
from praatio import textgrid
from os.path import join

# %%% 0.2: Define function
# Populate `prosodic_unit` tier with `s` when given entries are not `''`


def prosodic_unit(s):
    if not s:
        return ""
    return s

# %% 1: Modify forced aligned TextGrids and populate with new tiers


# %%% 1.1: Define input and output paths
modified_textgrid_input_path = "C:/Users/eirik/OneDrive - OsloMet/" + \
    "/Documents/Github/" + \
    "TextGrid-scripts/Prosodic_Annotation/NorwegianTextGrids/"

# Define `textgrid_output_path` if different from output_path
modified_textgrid_output_path = join(modified_textgrid_input_path,
                                     "modified_textgrids/")
if not os.path.exists(modified_textgrid_output_path):
    os.mkdir(modified_textgrid_output_path)
    print(f"Created directory '{modified_textgrid_output_path}'!")

# %%% 1.2: Populate each TextGrid with new tiers and modify existing ones
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

    # Remove `word` and `phone` tiers for placing them below prosodic tiers
    word_tier = tg.removeTier("word")
    phone_tier = tg.removeTier("phone")

    # Add `stress_tier`
    stress_tier = textgrid.PointTier(
        "stress (S|SS|0)", [], minT=0, maxT=tg.maxTimestamp)
    tg.addTier(stress_tier)

    # Duplicate the `word` tier and create new `prosodic_unit` tier
    prosodic_unit_entries = [(start, stop, prosodic_unit(label))
                             for start, stop, label in word_tier.entries]
    prosodic_unit_tier = word_tier.new(name="prosodic unit",
                                       entries=prosodic_unit_entries)
    tg.addTier(prosodic_unit_tier)

    # Now reintroduce `word` and `phone` tiers
    tg.addTier(word_tier)
    tg.addTier(phone_tier)

    # Add remaining tiers
    emphasis_tier = textgrid.PointTier(
        "emphasis (E)", [], minT=0, maxT=tg.maxTimestamp)
    comment_tier = textgrid.IntervalTier(
        "comment", [], minT=0, maxT=tg.maxTimestamp)

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
