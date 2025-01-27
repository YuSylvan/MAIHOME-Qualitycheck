# Data Check Script

This repository provides a script to check data availability and validity for a list of assets within a specified time range. The script outputs a CSV file summarizing the results of the checks.

## Usage

To use this script, simply run the `check_data.py` file located in the `scripts` folder. The script will perform the following steps:
1. Fetch data for each asset from the API within the last 12 hours.
2. Check data availability, column consistency, and threshold compliance.
3. Save the results to a CSV file in the `Dataresult` folder.

### Example

Run the following command to execute the script:

```bash
python scripts/check_data.py

The script needs to be run automatically every 12 hours.
