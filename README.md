# Data Check Script

This repository provides a script to check data availability and validity for a list of assets within a specified time range. The script outputs a CSV file summarizing the results of the checks.

## Usage

To use this script, simply run the `check_data.py` file located in the `scripts` folder. The script will perform the following steps:
1. Fetch data for each asset from the API within the last 12 hours.
2. Check data availability, column consistency, and threshold compliance.
3. Save the results to a CSV file in the `Dataresult` folder.

### Example
The script needs to be run automatically every 12 hours.
Run the following command to execute the script:

```bash
python scripts/check_data.py

```
## Output

The script generates a CSV file summarizing the results of the data checks. The file is saved in the `Dataresult` folder with a name in the format:


### Columns in the Output

- **`Asset ID`**: Unique identifier for the asset being checked.
- **`Asset Type`**: Type of the asset.
- **`Asset Key`**: Key associated with the asset for identification.
- **`Asset Name`**: Name of the asset for easier recognition.
- **`Has Data (API)`**: Indicates if the API returned data for the asset. Possible values:
- `True`: Data is available.
- `API Error`: output the type of error directly(eg http error).
- **`Check NaN`**: Indicates if all data columns (excluding metadata) are empty. Possible values:
- `True`: At least one data column has valid data.
- `False`: All data columns are `NaN`.
- `"No Data"`: No data was fetched from the API.
- **`data_availability`**: Indicates if data is both available and not entirely `NaN`. Possible values:
- `True`: Data is available and valid.
- `False`: Data is unavailable or invalid.
- **`threshold_check`**: Indicates if the data values meet the defined thresholds. Possible values:
- `"TRUE"`: All data is within valid thresholds.
- List of columns failing the threshold check.

## Thresholds

The script applies the following thresholds to check the validity of asset data. Any column containing values outside these thresholds will be flagged in the `threshold_check` column in the output CSV file.

| **Column Name**          | **Minimum Value** | **Maximum Value** |
|---------------------------|-------------------|-------------------|
| `active_power`           | 0                 | 1000              |
| `battery`                | 0                 | 100               |
| `co2`                    | 0                 | 5000              |
| `current`                | 0                 | 1000              |
| `humidity`               | 0                 | 100               |
| `temperature`            | -20               | 50                |
| `setTemperature`         | -20               | 50                |
| `temperature.current`    | -20               | 50                |
| `temperature.set`        | -20               | 50                |
| `pressure`               | 900               | 1100              |
| `tvoc`                   | 0                 | 1000              |

