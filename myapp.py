# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OhOsupikopF6BVLrcQfL1z6lHjEXTwa6
"""

# Data handling
from bokeh.core.property.dataspec import value
from bokeh.models.layouts import Column
import pandas as pd
import numpy as np

# Adding Changes test for github

# Bokeh libraries
from bokeh.io import output_file, output_notebook
from bokeh.io import show,curdoc
from bokeh.plotting import figure, show
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import Slider, Select, callbacks
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6
from bokeh.models import ColumnDataSource, CDSView, GroupFilter, CustomJS, Select, Range1d, Dropdown
from bokeh.models import HoverTool
from bokeh.models.widgets.sliders import DateRangeSlider


df_covid = pd.read_csv('dataset.csv')
df_covid.info()

df_covid = pd.read_csv('dataset.csv', parse_dates=['Date'])
df_covid.info()

df_covid.head()
df_covid.shape

df_covid['Date'] = pd.to_datetime(df_covid['Date'])

location_list = list(df_covid['Location'].unique())

df_covid.rename(columns={'Total Active Cases':'Total_Active_Cases'}, inplace=True)
df_covid.rename(columns={'Total Deaths':'Total_Deaths'}, inplace=True)
df_covid.rename(columns={'New Cases':'New_Cases'}, inplace=True)


#Output file
output_file('no1.html', title='hasil visualisasi')

covid_cds = ColumnDataSource(df_covid)

DKI_Jakarta = df_covid[df_covid['Location'] == 'DKI Jakarta']
DKI_Jakarta_cds = ColumnDataSource(DKI_Jakarta)

Jawa_Barat = df_covid[df_covid['Location'] == 'Jawa Barat']
Jawa_Barat_cds = ColumnDataSource(Jawa_Barat)

Daerah_Istimewa_Yogyakarta = df_covid[df_covid['Location'] == 'Daerah Istimewa Yogyakarta']
Daerah_Istimewa_Yogyakarta_cds = ColumnDataSource(Daerah_Istimewa_Yogyakarta)

Riau = df_covid[df_covid['Location'] == 'Riau']
Riau_cds = ColumnDataSource(Riau)

Banten = df_covid[df_covid['Location'] == 'Banten']
Banten_cds = ColumnDataSource(Banten)

Kalimantan_Timur = df_covid[df_covid['Location'] == 'Kalimantan Timur']
Kalimantan_Timur_cds = ColumnDataSource(Kalimantan_Timur)

#create views
DKI_Jakarta_view = CDSView(source = covid_cds, filters=[GroupFilter(column_name='Location',group='DKI Jakarta')])
Jawa_Barat_view = CDSView(source = covid_cds, filters=[GroupFilter(column_name='Location',group='Jawa Barat')])
Daerah_Istimewa_Yogyakarta_view = CDSView(source = covid_cds, filters=[GroupFilter(column_name='Location',group='Daerah Istimewa Yogyakarta')])
Riau_view = CDSView(source = covid_cds, filters=[GroupFilter(column_name='Location',group='Riau')])
Banten_view= CDSView(source = covid_cds, filters=[GroupFilter(column_name='Location',group='Banten')])
Kalimantan_Timur_view = CDSView(source = covid_cds, filters=[GroupFilter(column_name='Location',group='Kalimantan Timur')])


# Create and configure the figure
fig_new_cases = figure(x_axis_type='datetime',
           plot_height=400, plot_width=800,
           title='Visualisasi Covid',
           x_axis_label='Date', y_axis_label='New Cases', y_axis_type="linear")

fig_active = figure(x_axis_type='datetime',
           plot_height=400, plot_width=800,
           title='Visualisasi Covid',
           x_axis_label='Date', y_axis_label='Total Active Cases')

fig_death = figure(x_axis_type='datetime',
           plot_height=400, plot_width=800,
           title='Visualisasi Covid',
           x_axis_label='Date', y_axis_label='Total Deaths',y_axis_type="linear")

# Connect to and draw the data
# fig active cases
fig_active.circle('Date', 'Total_Active_Cases', 
              color='red', legend_label='DKI Jakarta',
              source=covid_cds, view=DKI_Jakarta_view)
fig_active.circle('Date', 'Total_Active_Cases', 
              color='orange', legend_label='Jawa Barat',
              source=covid_cds, view=Jawa_Barat_view)
fig_active.circle('Date', 'Total_Active_Cases', 
              color='blue', legend_label='Daerah Istimewa Yogyakarta',
              source=covid_cds, view=Daerah_Istimewa_Yogyakarta_view)
fig_active.circle('Date', 'Total_Active_Cases', 
              color='green', legend_label='Riau',
              source=covid_cds, view=Riau_view)
fig_active.circle('Date', 'Total_Active_Cases', 
              color='purple', legend_label='Banten',
              source=covid_cds, view=Banten_view)
fig_active.circle('Date', 'Total_Active_Cases', 
              color='yellow', legend_label='Kalimantan Timur',
              source=covid_cds, view=Kalimantan_Timur_view)

# Format the tooltip
tooltips_new_cases = [
            ('New Cases', '@New_Cases'),
            ('Date','@Date{%F}')
            ]
tooltips_active = [
            ('Location','@Location'),
            ('Total Active Cases', '@Total_Active_Cases'),
            ('Date','@Date{%F}'),
           ]

tooltips_death = [
            ('Location','@Location'),
            ('Total Deaths', '@Total_Deaths'),
            ('Date','@Date{%F}'),
            ]


# Add the HoverTool to the figure
fig_new_cases.add_tools(HoverTool(tooltips=tooltips_new_cases, formatters={'@Date': 'datetime'}))
fig_active.add_tools(HoverTool(tooltips=tooltips_active, formatters={'@Date': 'datetime'}))
fig_death.add_tools(HoverTool(tooltips=tooltips_death, formatters={'@Date': 'datetime'}))

cols1_new_cases = df_covid[['Date','Location','New_Cases']]
cols2_new_cases = cols1_new_cases[cols1_new_cases['Location']=='DKI Jakarta']
col1_new_cases_cds = ColumnDataSource(data=cols1_new_cases)
col2_new_cases_cds = ColumnDataSource(data=cols2_new_cases)

# Callback for new cases
callback_new_cases = CustomJS(args=dict(source=col1_new_cases_cds, sc=col2_new_cases_cds), code="""
                    var f = cb_obj.value;
                    sc.data['Date'] = [];
                    sc.data['New_Cases'] = [];
                    for(var i = 0; i <= source.get_length(); i++){
                        if (source.data['Location'][i] == f){
                            sc.data['Date'].push(source.data['Date'][i]);
                            sc.data['New_Cases'].push(source.data['New_Cases'][i]);
                        }
                    }
                    sc.change.emit();
                    """)

menu_1 = Select(options=location_list, value='DKI Jakarta', title='Location')     #menu dropdown list
fig_new_cases.circle(x='Date',y='New_Cases',color='red', source=col2_new_cases_cds)
fig_new_cases.line('Date','New_Cases',color='red', source=col2_new_cases_cds)
fig_new_cases.vbar(x='Date',top='New_Cases',color='red', source=col2_new_cases_cds, width=0.5, bottom=0)
menu_1.js_on_change('value', callback_new_cases)

cols1_death = df_covid[['Date','Location','Total_Deaths']]
cols2_death = cols1_death[cols1_death['Location']=='DKI Jakarta']
col1_death_cds = ColumnDataSource(data=cols1_death)
col2_death_cds = ColumnDataSource(data=cols2_death)

# Callback for death
callback_death = CustomJS(args=dict(source=col1_death_cds, sc=col2_death_cds), code="""
                    var f = cb_obj.value;
                    sc.data['Date'] = [];
                    sc.data['Total_Deaths'] = [];
                    for(var i = 0; i <= source.get_length(); i++){
                        if (source.data['Location'][i] == f){
                            sc.data['Date'].push(source.data['Date'][i]);
                            sc.data['Total_Deaths'].push(source.data['Total_Deaths'][i]);
                        }
                    }
                    sc.change.emit();
                    """)

menu_2 = Select(options=location_list, value='DKI Jakarta', title='Location')     #menu dropdown list
fig_death.vbar(x='Date',top='Total_Deaths',color='red', source=col2_death_cds, width=3, bottom=0)
fig_death.line('Date','Total_Deaths',color='red', source=col2_death_cds)
menu_2.js_on_change('value', callback_death)

#Range datetime slider for new cases
slider_range_datetime_newcases = DateRangeSlider(value=(min(df_covid['Date']), max(df_covid['Date'])),
                                        start=min(df_covid['Date']),end=max(df_covid['Date']),width=300
                                        )
slider_range_datetime_newcases.js_link('value', fig_new_cases.x_range, 'start', attr_selector=0)
slider_range_datetime_newcases.js_link('value', fig_new_cases.x_range, 'end', attr_selector=1)

#Range datetime slider for deaths
slider_range_datetime_deaths = DateRangeSlider(value=(min(df_covid['Date']), max(df_covid['Date'])),
                                        start=min(df_covid['Date']),end=max(df_covid['Date']),width=300
                                        )
slider_range_datetime_deaths.js_link('value', fig_death.x_range, 'start', attr_selector=0)
slider_range_datetime_deaths.js_link('value', fig_death.x_range, 'end', attr_selector=1)

#Create layout
lcol_1 = column(menu_1, slider_range_datetime_newcases)
lcol_2 = column(menu_2, slider_range_datetime_deaths)
layout_1 = row(lcol_1,fig_new_cases)
layout_2 = row(lcol_2, fig_death)

#Tab panel
panel_new_cases = Panel(child = layout_1, title='New Cases')
panel_active = Panel(child = fig_active, title='Active Cases')
panel_dead = Panel(child = layout_2, title='Deaths')

#assign tabs
main = Tabs(tabs=[panel_new_cases, panel_active, panel_dead])

# Visualize
show(main) #not localhost

#With localhost
# curdoc().add_root(tabs) 

#Cara menjalankan
## Setelah run
## ketik 'bokeh serve --show myapp.py' di terminal