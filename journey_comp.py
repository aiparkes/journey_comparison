import pandas as pd
import glob

import plotly.graph_objects as go
import plotly.express as px

def read_journey_files():
    df = pd.DataFrame()
    files = glob.glob('journeys/*_journey_analysis.csv')
    for file in files:
        temp = pd.read_csv(file)
        temp['ship'] = file[9:-21]
        df = df.append(temp,ignore_index=True)
    df['measured_co2'] = df.AE_CO2 + df.ME_CO2
    df['IMO_CO2_consump'] = df.IMO_CO2_consump/1000000
    df['desmo_CO2'] = df.desmo_CO2/1000000
    df['measured_co2'] = df.measured_co2/1000000
    df = df[df.desmo_CO2 < 10000000000]
    return df

def graph_port_operation_vs_journey(df):
    df['port'] = 'Journey'
    df.at[df[df.route_name == 'port_activity'].index, 'port'] = 'Port Operation'
    df = df[df.port == 'Port Operation']
    tdf = df[['port','IMO_CO2_consump','desmo_CO2','measured_co2']]
    tdf = tdf.rename({'IMO_CO2_consump':'4th IMO method','desmo_CO2': 'DESMO DTU method','measured_co2': 'High frequency data'}, axis=1)
    fig = px.box(tdf, color='port')
    fig.update_layout(
    	title_text = 'CO2 Emissions from Handysize Bulk Carriers in Port',
    	showlegend = True,
    	xaxis_title='Estimation Method',
        yaxis_title='Total Tonnes CO2 Emitted',
        legend_title='Activity')
    fig.show()
    fig.update_layout(
    	width=2000,
        height=1000)
    fig.write_image('initial_port.png')

def graph_BE_routes(df):
    tdf = df[~df.route_name.isna()]
    tdf = tdf[tdf.route_name.str.startswith('H')]

    imo = tdf[['route_name','IMO_CO2_consump']].pivot(columns='route_name')
    imo.columns = imo.columns.droplevel()
    imo['method'] = '4th IMO method'
    '''
    desmo = tdf[['route_name','desmo_CO2']].pivot(columns='route_name')
    desmo.columns = desmo.columns.droplevel()
    desmo['method'] = 'DESMO DTU method'
    '''
    data = tdf[['route_name','measured_co2']].pivot(columns='route_name')
    data.columns = data.columns.droplevel()
    data['method'] = 'High frequency data'

    pdf = imo.append(data, ignore_index=True)#desmo.append(data, ignore_index=True), ignore_index=True)
    fig = px.box(pdf, color='method')
    fig.update_layout(
    	#title_text = '',
    	showlegend = True,
    	xaxis_title='Route Code',
        yaxis_title='Total Tonnes CO2 Emitted',
        legend_title='Estimation Method')
    #fig.show()
    fig.update_layout(
    	width=2000,
        height=700)

    return fig
    #fig.write_image('initial_BA_routes.png')

def main():
    df = read_journey_files()
    #import pdb; pdb.set_trace()
    graph_BE_routes(df)
    graph_port_operation_vs_journey(df)

if __name__ == '__main__':
    main()
