# Note: Need to 'pip install openpyxl'
import pandas as pd
from pathlib import Path

def normalize_route_segments(file_name):
    combined_segments_df = pd.DataFrame()
    segment_sheets = pd.read_excel(file_name, engine="openpyxl", sheet_name=None, header=2)

    # Add segment and indicate loop segments
    for segment_name, segment_df in segment_sheets.items():
        segment_df = segment_df.loc[:, ~segment_df.columns.str.contains("^Unnamed")]
        segment_df["Segment"] = segment_name
        
        if segment_name.lower().find("loop") != -1:
            segment_df["is_loop"] = True
        else:
            segment_df["is_loop"] = False
        combined_segments_df = pd.concat([combined_segments_df, segment_df], ignore_index=True)

    return combined_segments_df


def save_to_csv(df, excel_file_name):
    csv_file_name = Path(excel_file_name).with_suffix(".csv")
    df.to_csv(csv_file_name, index=False)
    return df


def main():
    # Set Excel file name
    excel_file_name = "route-steps-2022.xlsx"

    # Normalize route steps
    combined_segments_df = normalize_route_segments(excel_file_name)

    # Save combined DataFrame to CSV
    save_to_csv(combined_segments_df, excel_file_name)


if __name__ == "__main__":
    main()