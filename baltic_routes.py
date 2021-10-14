import streamlit as st
from journey_comp import read_journey_files, graph_BE_routes
from custom_components.layout import _max_width_
_max_width_()

st.write('Baltic Exchange Routes CO2 Emissions from Handysize Bulk Carriers (Route Descriptions at https://www.balticexchange.com/en/data-services/routes.html)')
df = read_journey_files()
fig = graph_BE_routes(df)

st.plotly_chart(fig, use_container_width = True)
