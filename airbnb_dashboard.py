import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import hashlib
import random

st.set_page_config(
   page_title="Airbnb Dashboard"
)

@st.cache_data
def get_listings():
    return pd.read_csv("Data\\New_York\\09_04_2024_listings.csv")

@st.cache_data
def get_listings_deep():
    return pd.read_csv("Data\\New_York\\09_04_2024_listings_deep.csv")


dt = pd.read_csv("Data\\New_York\\09_04_2024_listings.csv")
df = dt.groupby(['neighbourhood_group', 'neighbourhood'])

df_deep = pd.read_csv("Data\\New_York\\09_04_2024_listings_deep.csv")

# Create and return dictionary linking borough -> [neighbourhood, ...], and creating a general options,
# for all boroughs and for all neighbourhoods within a borough 
def get_regions_dic() -> dict:
    neighbourhoods_df = pd.read_csv('Data\\New_York\\neighbourhoods.csv')

    regions_dic = neighbourhoods_df.groupby('neighbourhood_group')['neighbourhood'].unique().to_dict()

    # Add option to get all neighbourhoods from one borough
    for k, v in regions_dic.items():
        regions_dic[k] = np.insert(v, 0, 'All')

    # Add new york all option
    regions_dic['New York City']  = ['All']

    return regions_dic

regions_dic = get_regions_dic()


with st.container(border=True):
    col1, col2 = st.columns([1, 1])

    with col1:
        region = st.selectbox("Select Region", regions_dic.keys())

    with col2:
        if region:
            neighbourhoods = regions_dic[region]
            neighbourhood = st.selectbox("Select neighbourhood", neighbourhoods)
    

    df_main_2 = get_listings()
    df_deep_2 = get_listings_deep()

    total_listings_count = len(df_main_2)


    if region != 'New York City':
        if neighbourhood == 'All':
            df_main_2 = df_main_2[df_main_2['neighbourhood_group'] == region]
        else:
            df_main_2 = df_main_2[df_main_2['neighbourhood_group'] == region]
            df_main_2 = df_main_2[df_main_2['neighbourhood'] == neighbourhood]

    
    st.markdown(f"**{len(df_main_2)}** out of **{total_listings_count}** ({round(len(df_main_2)/total_listings_count*100, 1)}%)")
    



                              


with st.container(border=True):
    st.subheader("Room Type")
    #col1, col2 = st.columns([.6, .4], vertical_alignment="top")
    df = df_main_2.groupby('room_type')
    test = df.size().reset_index(name='count')

    options = ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room']

    for option in options:
        if option not in test['room_type'].values:
            new_row = pd.DataFrame({'room_type': [option], 'count': [0]})
            test = pd.concat([test, new_row], ignore_index=True)
    test.sort_values(by="count", ascending=False, inplace=True)
    
    st.bar_chart(test, x="room_type", y="count", horizontal=True, x_label="Listings", y_label="")

    
    total_listings = test['count'].sum()

    room_type_metrics = []
    for row in test.itertuples():
        percentage = row.count / total_listings
        percentage = round(percentage * 100, 2)

        #row_info = f'''{row.count} ({percentage}%) : {row.room_type}'''
        room_type_metrics.append((f'{row.count} : {row.room_type}', f'{percentage}%'))
        #st.markdown(row_info)
        
    with st.container():
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap='medium')

        with col1:
            st.metric(room_type_metrics[0][0], room_type_metrics[0][1])

        with col2:
            st.metric(room_type_metrics[1][0], room_type_metrics[1][1])
        
        with col3:
            st.metric(room_type_metrics[2][0], room_type_metrics[2][1])

        with col4:
            st.metric(room_type_metrics[3][0], room_type_metrics[3][1])
    
        
# Listings per host    
with st.container(border=True):
    st.subheader("Listings per Host")

    df = df_main_2.groupby(['host_id', 'host_name']).size().reset_index(name="count")
    #st.dataframe(df)
    df = df.groupby('count').size().reset_index(name="listing_count")
    #st.dataframe(df)

    temp = df[df['count'] < 10]
    room_type_metrics = []

    for row in temp.itertuples():
        room_type_metrics.append([row.count, row.count*row.listing_count])

    temp = df[df['count'] >= 10]
    sum = 0

    for row in temp.itertuples():
        sum += row.count * row.listing_count
    room_type_metrics.append([10, sum])

    df_out = pd.DataFrame(room_type_metrics, columns=['count', 'total'])

    st.bar_chart(df_out, x='count', y='total', x_label='listings per host', y_label='listings')\
    
# Licenses
with st.container(border=True):
    st.subheader("Licenses")
    d = {}
    license_df = get_listings_deep()

    temp_df = license_df[license_df['license'].isna()]
    unlicensed_count = len(temp_df)
    d['unlicensed'] = unlicensed_count
 
    license_df = license_df.groupby('license').size().reset_index(name='temp')
    exempt_count = license_df.loc[license_df['license'] == 'Exempt', 'temp'].values[0]
    d['exempt'] = int(exempt_count)

    temp_df = license_df[license_df['license'] != 'Exempt']
    licensed_count = len(temp_df)
    d['licensed'] = licensed_count

    test = []
    total = 0

    for k,v in d.items():
        test.append([k, v])
        total += v

    license_df = pd.DataFrame(test, columns=['License Type', 'Count'])
    fig2 = px.pie(license_df, values='Count', names='License Type')
    fig2.update_traces(textinfo='value')
    st.plotly_chart(fig2)

    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.metric("unlicensed", f"{d['unlicensed']} ({round((d['unlicensed']/total) * 100, 1)}%)")

        with col2:
            st.metric("licensed", f"{d['licensed']} ({round((d['licensed']/total) * 100, 1)}%)") 
        
        with col3:
            st.metric("exempt", f"{d['exempt']} ({round((d['exempt']/total) * 100, 1)}%)")



# short-term Rentals
with st.container(border=True):
    st.subheader("Short-Term Rentals")
    col1, col2 = st.columns([0.7, 0.3], vertical_alignment="center")

    # Column will contain the bar graph for short-term rentals
    with col1:
        rentals_df = df_main_2.groupby("minimum_nights").size().reset_index(name='count')
        st.bar_chart(rentals_df.head(25), x='minimum_nights', y_label="listings", x_label="minimum nights")

        val1  = rentals_df[rentals_df['minimum_nights'] < 30]['count'].sum()
        val2  = rentals_df[rentals_df['minimum_nights'] >= 30]['count'].sum()

        short_rentals_info = '''A short term rental is defined as being less than 30 days by the state of NY. '''

    with col2:
        st.metric(f"{val1} : short-term rentals", f"{round((val1 / (val1 + val2)) * 100, 1)}%")
        st.metric(f"{val2} : longer-term rentals", f"{round((val2 / (val1 + val2)) * 100, 1)}%")


# Top Hosts
with st.container(border=True):
    st.subheader("Top Hosts")

    room_type_counts = df_main_2.pivot_table(index=['host_id', 'host_name'], columns='room_type', aggfunc='size', fill_value=0)
    
    room_type_counts = room_type_counts.rename(columns={
        'host_name': 'Host name'
    })
    
    room_type_counts['Listings'] = room_type_counts.sum(axis=1)

    room_type_counts = room_type_counts.reset_index().drop(columns=['host_id'])
    room_type_counts = room_type_counts.sort_values(by='Listings', ascending=False)
    st.dataframe(room_type_counts, hide_index=True)


    #top_hosts_df = df_main_2.groupby(['host_id', 'host_name', 'room_type']).size()
    #top_hosts_df = top_hosts_df.groupby('host_id')
    #st.dataframe(top_hosts_df)
    







