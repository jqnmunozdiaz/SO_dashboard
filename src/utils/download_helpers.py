""" 
Helper functions for creating data download callbacks
Provides reusable utilities for generating CSV downloads from dashboard data
"""

import pandas as pd
from dash import dcc
import io
import zipfile


def prepare_csv_download(df, filename):
    """
    Prepare a DataFrame for CSV download
    
    Args:
        df (pd.DataFrame): DataFrame to download
        filename (str): Filename without extension (e.g., 'urban_population_data')
        
    Returns:
        dict: Download data dictionary for dcc.send_data_frame
    """
    return dcc.send_data_frame(df.to_csv, f"{filename}.csv", index=False)


def prepare_multi_csv_download(dataframes_dict, zip_filename):
    """
    Prepare multiple DataFrames for download as a ZIP file
    
    Args:
        dataframes_dict (dict): Dictionary mapping filenames (without extension) to DataFrames
        zip_filename (str): Name for the ZIP file without extension
        
    Returns:
        dict: Download data dictionary for dcc.send_bytes
    """
    # Create a bytes buffer for the ZIP file
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, df in dataframes_dict.items():
            # Convert DataFrame to CSV
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            # Add to ZIP
            zip_file.writestr(f"{filename}.csv", csv_data)
    
    zip_buffer.seek(0)
    return dcc.send_bytes(zip_buffer.getvalue(), f"{zip_filename}.zip")