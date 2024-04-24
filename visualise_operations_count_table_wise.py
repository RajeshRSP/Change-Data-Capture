import streamlit as st
import pandas as pd
import plotly.express as px

# Load your DataFrame
df = pd.read_csv("/Users/udaya_surya_azhagudurai/Downloads/Tasks/CDC/cortal_DB_mar28_summary.csv")

# Remove any unwanted columns
df = df.filter(regex='^(?!Unnamed)')

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Streamlit setup
st.title('DB Operations Summary')

# User input for date and hour
date = st.text_input('Enter date (YYYY-MM-DD)', '')
hour = st.text_input('Enter hour (optional):', '')

# Filter the DataFrame based on the user input date and hour, if provided 
if date:
    filtered_df = df[df['date'].dt.date == pd.to_datetime(date).date()]
    if hour:
        filtered_df = filtered_df[filtered_df['hour'] == int(hour)]

# Display the filtered DataFrame
if 'filtered_df' in locals():
    st.write(filtered_df)

    # Get unique table names
    table_names = filtered_df['table_name'].unique()

    # Add multiselect for selecting table names
    selected_tables = st.multiselect("Select tables:", table_names)

    # Filter data based on selected table names
    selected_data = filtered_df[filtered_df['table_name'].isin(selected_tables)]

    # Plot button to plot selected data
    if st.button('Plot'):
        if not selected_data.empty:
            # Plot each operation's summary separately
            for operation in ['total', 'insert_sum', 'update_sum', 'truncate_sum','delete_sum']:
                fig = px.line(selected_data, x='hour', y= operation, color='table_name', 
                              title=f'Table operations summary',
                              labels={'hour': 'Hour', operation: 'Total operations count', 'table_name': 'Table Name'})

                # Add hover tooltips
                fig.update_traces(mode='lines+markers', hovertemplate="Hour: %{x}<br>Total operations count: %{y}<extra></extra>")

                st.plotly_chart(fig)
        else:
            st.warning("No data available for the selected tables.")


