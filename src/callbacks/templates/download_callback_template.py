"""
TEMPLATE: Download Callback Implementation Pattern

This file demonstrates how to add download functionality to any chart in the dashboard.
Follow these steps to implement downloads for your charts:

STEP 1: Import download helpers in your callback file
-------------------------------------------------------
Add to your imports:
    from ...utils.download_helpers import prepare_csv_download, prepare_multi_csv_download

STEP 2: Add download callback to your register function
-------------------------------------------------------
Example for single CSV download:

    @app.callback(
        Output('your-chart-download', 'data'),
        Input('your-chart-download-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def download_your_chart_data(n_clicks):
        """Download data used in your chart as CSV"""
        if n_clicks is None or n_clicks == 0:
            return None

        try:
            # Load full dataset (raw data, no filtering)
            data = load_your_data()

            filename = "your_chart_data"

            return prepare_csv_download(data, filename)

        except Exception as e:
            print(f"Error preparing download: {str(e)}")
            return None


Example for multiple CSV files (ZIP download):

    @app.callback(
        Output('your-chart-download', 'data'),
        Input('your-chart-download-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def download_your_chart_data(n_clicks):
        """Download multiple data files as ZIP"""
        if n_clicks is None or n_clicks == 0:
            return None

        try:
            # Load multiple datasets (raw data, no filtering)
            dataset1 = load_first_dataset()
            dataset2 = load_second_dataset()

            # Create dictionary of dataframes (keys become filenames)
            dataframes_dict = {
                'first_dataset_name': dataset1,
                'second_dataset_name': dataset2
            }

            filename = "your_chart_data"

            # Return ZIP download
            return prepare_multi_csv_download(dataframes_dict, filename)

        except Exception as e:
            print(f"Error preparing download: {str(e)}")
            return None


STEP 3: Add download button to layout
---------------------------------------
In your orchestrator file (e.g., urbanization_callbacks.py or disaster_callbacks.py):

1. Import create_download_button:
   from ..utils.ui_helpers import create_download_button

2. Add the button after your indicator note:

   html.Div([
       html.P([...your indicator note...], className="indicator-note"),
       create_download_button('your-chart-download')  # Must match Output ID in callback
   ], className="indicator-note-container")


STEP 4: Test your implementation
---------------------------------
1. Start the dashboard: python app.py
2. Navigate to your chart
3. Click "Download Data" button
4. Verify CSV/ZIP downloads with correct data and filename


HELPER FUNCTIONS AVAILABLE
---------------------------

prepare_csv_download(df, filename)
    - Downloads a single DataFrame as CSV
    - Args: DataFrame, filename (without extension)
    - Returns: Complete raw dataset

prepare_multi_csv_download(dataframes_dict, zip_filename)
    - Downloads multiple DataFrames as ZIP file
    - Args: dict of {filename: DataFrame}, ZIP filename (without extension)
    - Returns: Complete raw datasets


COMPLETE WORKING EXAMPLES
--------------------------
See implementations in:
- src/callbacks/urbanization/Urban_Population_Projections_callbacks.py (single CSV)
- src/callbacks/urbanization/GDP_vs_Urbanization_callbacks.py (multiple CSV as ZIP)

Note: Downloads provide the complete raw dataset without any filtering.
"""
