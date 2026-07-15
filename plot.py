import pandas as pd
import plotly.express as px
import os

# ==========================================
# CONFIGURATION
# ==========================================
# Replace this with your actual file name
INPUT_FILE = r'U:\ТЕСТОВЫЕ ЗАКАЗЫ ГТР\СП\raw\bbbb\аа.xlsx' 
OUTPUT_FILE = r'U:\ТЕСТОВЫЕ ЗАКАЗЫ ГТР\СП\raw\bbbb\aa.html'

# Check if file exists
if not os.path.exists(INPUT_FILE):
    print(f"Error: The file '{INPUT_FILE}' was not found in the current directory.")
else:
    # 1. Load the Excel file
    # Assuming the first row contains headers
    try:
        df = pd.read_excel(INPUT_FILE)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        exit()

    # 2. Data Preparation
    # Ensure 'nm' is the first column as requested. 
    # If your excel loads an index column automatically, uncomment the line below:
    # df = df.reset_index() 

    # Check if 'nm' column exists
    if 'nm' not in df.columns:
        print("Error: Could not find a column named 'nm' in the Excel file.")
        print(f"Found columns: {df.columns.tolist()}")
        exit()

    # Optional: Sort data by 'nm' to ensure lines draw correctly (850 -> 190)
    # We assume descending based on your prompt (850 to 190), 
    # but change ascending=True if your data is messed up.
    df = df.sort_values(by='nm', ascending=False)

    # Identify Y-axis columns (everything except 'nm')
    y_columns = [col for col in df.columns if col != 'nm']

    # 3. Create the Interactive Chart
    # px.line creates a line chart for every column passed to y=...
    
    # fig = px.line(
    #     df, 
    #     x='nm', 
    #     y=y_columns,
    #     title='Transmittance',
    #     labels={'nm': 'Wavelength (nm)', 'value': 'T%'}, # Axis labels
    #     # markers=True # Adds dots to data points (optional, looks good for spectra)
    # )
    
    # Define your custom colors (names or hex codes)
    color_map = {
        'baseline (air)': 'red',
        'HY_flat': '#00FF00',  # Green hex
        'HY_flat2': '#00FF00',
        'HY_flat3': '#00FF00',
        'HY_convex': 'blue',
        'HY_convex2': 'blue',
        'HY_convex3': 'blue',
    }
    
    fig = px.line(
        df, 
        x='nm', 
        y=y_columns,
        title='Transmittance',
        labels={'nm': 'Wavelength (nm)', 'value': 'T%'},
        color_discrete_map=color_map  # Apply the map
        )
    
    columns_to_hide = ['HY_flat', 'HY_convex']  # Add your column names here
    
    for trace in fig.data:
        if trace.name in columns_to_hide:
            trace.visible = 'legendonly'   
    
    
    # Customize the layout slightly
    fig.update_layout(
        hovermode="x unified", # Shows all values at specific X point on hover
        template="plotly_dark",
        legend_title_text='Data Series',
        xaxis=dict(
                showticklabels=True,
                ticks='outside',
                ticklen=5,
                tickwidth=1,
                tickcolor='gray',
                dtick=10           # Every 10 units
            ),
        yaxis=dict(
            showticklabels=True,
            ticks='outside',
            ticklen=5,
            tickwidth=1,
            tickcolor='gray',
            dtick=5
            ),
    )

    fig.update_traces(
        hovertemplate=
        "%{fullData.name}: %{y:.2f}" +
        "<extra></extra>"
    )

    # 4. Export to HTML
    fig.write_html(OUTPUT_FILE)
    
    print(f"Success! Chart generated: {os.path.abspath(OUTPUT_FILE)}")
    print("Open this file in your web browser to view the interactive chart.")
