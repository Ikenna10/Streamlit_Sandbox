# Soil properties App

# Import modules
import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.palettes import Turbo256
from bokeh.transform import linear_cmap
from bokeh.models import ColorBar

# Read dataset
df = pd.read_excel('mesonet_QC_data.xlsx')
df = df.groupby(['station_name', 'nominal_depth'], as_index=False).mean()
df.drop(['ring_number', 'core_number'], axis='columns', inplace=True)

# Add title and description
st.title('Kansas Mesonet Soil App')
st.write('Databse of soil physical properties.')

# Create column layout
col_1, col_2 = st.columns([1,3])

with col_1:
    x_var = st.selectbox("Select x variable", (df.columns[1:]), index=5)
    y_var = st.selectbox("Select y variable", (df.columns[1:]), index=6)
    z_var = st.selectbox("Select color variable", (df.columns[1:]), index=7)
    
with col_2:
    # Map colors for z variable
    mapper = linear_cmap(field_name=z_var,
                         palette=Turbo256,
                         low=df[z_var].min(),
                         high=df[z_var].max())

    # Create colorbar object using the mapper we created above
    color_bar = ColorBar(color_mapper=mapper['transform'], height=10, title=z_var)

    # Create plot
    p = figure(title='Kansas Mesonet Soils', width=600, height=500)
    p.circle(source=df, x=x_var, y=y_var, size=10, color=mapper)
    p.xaxis.axis_label = x_var
    p.yaxis.axis_label = y_var
    p.add_layout(color_bar, 'below')
    st.bokeh_chart(p)
    
# Display the dataset as a dataframe table
st.header("Dataset")
st.write(df)

# Add a download button for your dataset
st.download_button(label='Download',
                   data=df.to_csv(index=False).encode('utf8'),
                   file_name='mesonet_dataset.csv',
                   mime='text/csv')

# UTF-8 is an encoding system for Unicode. UTF-8 is a variable-length character encoding standard used for electronic communication.

# A media type (also known as a Multipurpose Internet Mail Extensions or MIME type) indicates the nature and format of a document or file.