# Baselight / Xytech Frame Mapper

A Python command-line script that turns a Baselight export and a Xytech work order into a clean CSV of frames to fix.

Colorists' Baselight exports list frame numbers under Baselight's own storage paths, while the work order uses different (Xytech) storage locations. This script matches the two, replaces each Baselight path with the correct Xytech location, and collapses consecutive frames into ranges (for example, `25 26 27 28 29` becomes `25-29`).

## Features

- Maps Baselight folder paths to the matching Xytech work-order locations
- Collapses consecutive frame numbers into ranges
- Reads Producer, Operator, Job and Notes directly from the work order
- Writes a ready-to-use CSV report
- Warns about (and skips) any Baselight folder with no matching Xytech location
- No third-party dependencies

## Requirements

- Python 3

## Usage

Run with the default filenames:

```
python mpr_tool.py
```

Or specify your own files:

```
python mpr_tool.py BASELIGHT_FILE XYTECH_FILE
python mpr_tool.py BASELIGHT_FILE XYTECH_FILE -o output.csv
```

| Argument | Description | Default |
|---|---|---|
| `baselight` | Baselight export file | `Baselight.txt` |
| `xytech` | Xytech work order file | `Xytech.txt` |
| `-o`, `--output` | Output CSV file | `MPR_Result.csv` |

## Example

**Baselight export** (one line per folder, followed by frame numbers):

```
/baselightfilesystem1/Spiderman/reel1/partA/1920x1080 25 26 27 28 29 60 222 223 255
```

**Xytech work order** (excerpt):

```
Producer: Elizabeth Holmes
Operator: Tom Cruise
Job: Dirtfixing

Location:
/hpsans15/production/Spiderman/reel1/partA/1920x1080
```

**Output CSV** (`Project_1.csv`):

```
Producer,Operator,Job,Notes
Elizabeth Holmes,Tom Cruise,Dirtfixing,Please clean files noted per Colorist Jacob from Twilight

Location,Frames to Fix
/hpsans15/production/Spiderman/reel1/partA/1920x1080,25-29
/hpsans15/production/Spiderman/reel1/partA/1920x1080,60
/hpsans15/production/Spiderman/reel1/partA/1920x1080,222-223
/hpsans15/production/Spiderman/reel1/partA/1920x1080,255
```

## How it works

1. **Parse the work order:** read the header fields and the list of Xytech locations.
2. **Match paths:** strip the Baselight root folder from each line and find the Xytech location that contains the remaining path.
3. **Build ranges:** walk through each line's frame numbers, grouping runs of consecutive frames into `start-end` ranges and leaving isolated frames as single numbers.
4. **Write the CSV:** output the header block followed by one row per location and frame range.

## Project structure

```
.
├── mpr_tool.py                    # the script
├── Baselight.txt   # sample Baselight export
├── Xytech.txt             # sample Xytech work order
├── Sample_Output.csv                   # sample output
└── README.md
```