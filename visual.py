import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib as mpl
from sklearn import preprocessing

map_names = {
    'Cyprus': 'N. Cyprus',
    'Russian federation': 'Russia',
    'Sudan': 'S. Sudan',
    'Korea, republic of': 'South Korea',
    'Tanzania, United Republic of': 'Tanzania',
    'Bolivia, Plurinational State of': 'Bolivia',
    'Viet Nam': 'Vietnam',
    'Bosnia and herzegovina': 'Bosnia and Herz.',
    'Brunei Darussalam': 'Brunei',
    'Central African Republic': 'Central African Rep.',
    'Czech republic': 'Czechia',
    'Congo, Democratic Republic of the': 'Dem. Rep. Congo',
    'Dominican Republic': 'Dominican Rep.',
    'Equatorial Guinea': 'Eq. Guinea',
    'Iran, Islamic Republic of': 'Iran',
    'Lao People\'s Democratic Republic': 'Laos',
    'Libya, state of': 'Libya',
    'Macedonia, north': 'Macedonia',
    'Moldova, republic of': 'Moldova',
    'Afghanistan': 'Afghanistan',
    'Albania': 'Albania',
    'Algeria': 'Algeria',
    'Angola': 'Angola',
    'Argentina': 'Argentina',
    'Armenia': 'Armenia',
    'Australia': 'Australia',
    'Austria': 'Austria',
    'Azerbaijan': 'Azerbaijan',
    'Bahamas': 'Bahamas',
    'Bangladesh': 'Bangladesh',
    'Belarus': 'Belarus',
    'Belgium': 'Belgium',
    'Belize': 'Belize',
    'Benin': 'Benin',
    'Botswana': 'Botswana',
    'Brazil': 'Brazil',
    'Bulgaria': 'Bulgaria',
    'Burkina Faso': 'Burkina Faso',
    'Burundi': 'Burundi',
    'Cambodia': 'Cambodia',
    'Cameroon': 'Cameroon',
    'Canada': 'Canada',
    'Chad': 'Chad',
    'Chile': 'Chile',
    'China': 'China',
    'Colombia': 'Colombia',
    'Congo': 'Congo',
    'Costa Rica': 'Costa Rica',
    'Croatia': 'Croatia',
    'Cuba': 'Cuba',
    'Cyprus': 'Cyprus',
    "Côte d'Ivoire": "Côte d'Ivoire",
    'Denmark': 'Denmark',
    'Djibouti': 'Djibouti',
    'Ecuador': 'Ecuador',
    'Egypt': 'Egypt',
    'El Salvador': 'El Salvador',
    'Estonia': 'Estonia',
    'Eswatini': 'eSwatini',
    'Ethiopia': 'Ethiopia',
    'Fiji': 'Fiji',
    'Finland': 'Finland',
    'France': 'France',
    'Gabon': 'Gabon',
    'Gambia': 'Gambia',
    'Georgia': 'Georgia',
    'Germany': 'Germany',
    'Ghana': 'Ghana',
    'Greece': 'Greece',
    'Guatemala': 'Guatemala',
    'Guinea': 'Guinea',
    'Guinea-Bissau': 'Guinea-Bissau',
    'Guyana': 'Guyana',
    'Haiti': 'Haiti',
    'Honduras': 'Honduras',
    'Hungary': 'Hungary',
    'Iceland': 'Iceland',
    'India': 'India',
    'Indonesia': 'Indonesia',
    'Iraq': 'Iraq',
    'Ireland': 'Ireland',
    'Israel': 'Israel',
    'Italy': 'Italy',
    'Jamaica': 'Jamaica',
    'Japan': 'Japan',
    'Jordan': 'Jordan',
    'Kazakhstan': 'Kazakhstan',
    'Kenya': 'Kenya',
    'Kuwait': 'Kuwait',
    'Kyrgyzstan': 'Kyrgyzstan',
    'Latvia': 'Latvia',
    'Lebanon': 'Lebanon',
    'Lesotho': 'Lesotho',
    'Liberia': 'Liberia',
    'Lithuania': 'Lithuania',
    'Luxembourg': 'Luxembourg',
    'Madagascar': 'Madagascar',
    'Malawi': 'Malawi',
    'Malaysia': 'Malaysia',
    'Mali': 'Mali',
    'Mauritania': 'Mauritania',
    'Mexico': 'Mexico',
    'Mongolia': 'Mongolia',
    'Montenegro': 'Montenegro',
    'Morocco': 'Morocco',
    'Mozambique': 'Mozambique',
    'Myanmar': 'Myanmar',
    'Namibia': 'Namibia',
    'Nepal': 'Nepal',
    'Netherlands': 'Netherlands',
    'New Zealand': 'New Zealand',
    'New caledonia': 'New Caledonia',
    'Nicaragua': 'Nicaragua',
    'Niger': 'Niger',
    'Norway': 'Norway',
    'Oman': 'Oman',
    'Pakistan': 'Pakistan',
    'Papua New Guinea': 'Papua New Guinea',
    'Paraguay': 'Paraguay',
    'Peru': 'Peru',
    'Philippines': 'Philippines',
    'Poland': 'Poland',
    'Portugal': 'Portugal',
    'Qatar': 'Qatar',
    'Romania': 'Romania',
    'Rwanda': 'Rwanda',
    'Saudi Arabia': 'Saudi Arabia',
    'Senegal': 'Senegal',
    'Serbia': 'Serbia',
    'Sierra Leone': 'Sierra Leone',
    'Slovakia': 'Slovakia',
    'Slovenia': 'Slovenia',
    'Somalia': 'Somalia',
    'South africa': 'South Africa',
    'Spain': 'Spain',
    'Sri Lanka': 'Sri Lanka',
    'Sudan': 'Sudan',
    'Suriname': 'Suriname',
    'Sweden': 'Sweden',
    'Switzerland': 'Switzerland',
    'Tajikistan': 'Tajikistan',
    'Thailand': 'Thailand',
    'Togo': 'Togo',
    'Trinidad and Tobago': 'Trinidad and Tobago',
    'Tunisia': 'Tunisia',
    'Turkey': 'Turkey',
    'Turkmenistan': 'Turkmenistan',
    'Uganda': 'Uganda',
    'Ukraine': 'Ukraine',
    'United Kingdom': 'United Kingdom',
    'United States of America': 'United States of America',
    'United arab emirates': 'United Arab Emirates',
    'Uruguay': 'Uruguay',
    'Uzbekistan': 'Uzbekistan',
    'Yemen': 'Yemen',
    'Zambia': 'Zambia',
    'Zimbabwe': 'Zimbabwe'
}

without_countries = ['Antarctica', 'Greenland']

def geoplot_network(export_data: pd.DataFrame, country_data: pd.DataFrame):

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    _, ax = plt.subplots(1, 1, figsize=(20,20), dpi=100)

    world.plot(
        color='#efefef',
        edgecolor='#a3a3a3',
        ax=ax,
        legend_kwds={'orientation': 'horizontal'},
    )

    # divide exports with country GDP
    for export_country, row in export_data.iterrows():
        for import_country in export_data.columns.values:
            row = row / float(country_data[country_data['Country Name'] == export_country]['GDP'])

    # normalize export figures into interval [0,1]
    x = export_data.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    export_data = pd.DataFrame(x_scaled, columns=export_data.columns.values, index=export_data.index.values)
    
    # draw edges between countries
    for export_country, row in export_data.iterrows():
        for import_country in export_data.columns.values:
            export = row[import_country]

            export_lat = float(country_data[country_data['Country Name'] == export_country]['Latitude'])
            export_lng = float(country_data[country_data['Country Name'] == export_country]['Longitude'])

            import_lat = float(country_data[country_data['Country Name'] == import_country]['Latitude'])
            import_lng = float(country_data[country_data['Country Name'] == import_country]['Longitude'])

            linewidth = export * 0.8
            alpha = export * 0.5

            plt.plot([export_lng, import_lng], [export_lat, import_lat], linewidth=linewidth, alpha=alpha, linestyle='-', color='#316df7')

    minx, miny, maxx, maxy = world.total_bounds
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    
    ax.set_axis_off()

def geoplot_numbers(country_number: dict[str, float], label: str):

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    _, ax = plt.subplots(1, 1, figsize=(20,20), dpi=100)
    
    world = world[~world.name.isin(without_countries)]
    world[label] = [np.nan]*len(world)

    for key, number in country_number.items():
        if key in map_names:
            geo_key = map_names[key]
            world.loc[world['name'] == geo_key, label] = number

    world.plot(
        column=label, 
        ax=ax, 
        legend=True,
        cmap=mpl.colors.LinearSegmentedColormap.from_list('', ['#c7eaff', '#005588', '#001d2f']),
        legend_kwds={'label': label, 'orientation': 'horizontal'},
        missing_kwds={'color': 'lightgrey'}
    )

    minx, miny, maxx, maxy = world.total_bounds
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    
    ax.set_axis_off()