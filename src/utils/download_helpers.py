""" 
Helper functions for creating data download callbacks
Provides reusable utilities for generating CSV downloads from dashboard data
"""

from dash import dcc, Input, Output
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


def create_simple_download_callback(app, download_id, data_loader, filename):
    """
    Create a standard download callback for a chart with automatic error handling
    
    This eliminates the need to write repetitive download callback code in each chart file.
    
    Args:
        app: Dash app instance
        download_id: ID of the dcc.Download component (e.g., 'disaster-frequency-download')
        data_loader: Callable that returns a DataFrame (e.g., lambda: load_emdat_data())
                    Or a DataFrame directly if data is pre-loaded
        filename: Base filename for the CSV without extension (e.g., 'african_disasters_emdat')
        
    Usage in callback files:
        # At the end of register_callbacks function:
        from src.utils.download_helpers import create_simple_download_callback
        
        # For dynamic data loading:
        create_simple_download_callback(
            app, 
            'disaster-frequency-download',
            lambda: load_emdat_data(),
            'african_disasters_emdat'
        )
        
        # For pre-loaded static data (captured in closure):
        create_simple_download_callback(
            app,
            'slums-download', 
            lambda: slums_data,  # Reference to pre-loaded data
            'urban_population_slums'
        )
    """
    @app.callback(
        Output(download_id, 'data'),
        Input(f'{download_id}-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def download_data(n_clicks):
        """Generic download callback handler"""
        if n_clicks is None or n_clicks == 0:
            return None
        
        try:
            # Get the data (either by calling function or using pre-loaded data)
            data = data_loader() if callable(data_loader) else data_loader
            return prepare_csv_download(data, filename)
        except Exception as e:
            print(f"Error preparing download: {str(e)}")
            return None
    
    return download_data


def create_multi_csv_download_callback(app, download_id, dataframes_dict_loader, zip_filename):
    """
    Create a download callback for multiple CSV files packaged as a ZIP
    
    Args:
        app: Dash app instance
        download_id: ID of the dcc.Download component
        dataframes_dict_loader: Callable that returns a dict mapping filenames to DataFrames
                               Or a dict directly if data is pre-loaded
        zip_filename: Base filename for the ZIP file without extension
        
    Usage:
        # For dynamic data:
        create_multi_csv_download_callback(
            app,
            'gdp-vs-urbanization-download',
            lambda: {
                f'gdp_per_capita_{GDP_INDICATOR}': load_wdi_data(GDP_INDICATOR),
                f'urbanization_rate_{URBAN_INDICATOR}': load_wdi_data(URBAN_INDICATOR)
            },
            'gdp_urbanization'
        )
        
        # For pre-loaded data:
        create_multi_csv_download_callback(
            app,
            'chart-download',
            lambda: {'file1': df1, 'file2': df2},
            'combined_data'
        )
    """
    @app.callback(
        Output(download_id, 'data'),
        Input(f'{download_id}-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def download_multi_csv_data(n_clicks):
        """Generic multi-CSV download callback handler"""
        if n_clicks is None or n_clicks == 0:
            return None
        
        try:
            # Get the dataframes dict (either by calling function or using pre-loaded data)
            dataframes_dict = dataframes_dict_loader() if callable(dataframes_dict_loader) else dataframes_dict_loader
            return prepare_multi_csv_download(dataframes_dict, zip_filename)
        except Exception as e:
            print(f"Error preparing download: {str(e)}")
            return None
    
    return download_multi_csv_data