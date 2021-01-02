from datetime import datetime
import os

import pandas as pd
import plotly
import plotly.graph_objects as go

# my Modules
import allFunctions as myAll
import createDirectory as new_dir
import filterBy as filter


def script(revenues_per_month,
           revenues_each_category_per_year,
           revenues_each_category_qte_per_month,
           revenues_period, file_path, filter_by, from_date, to_date):

    excelReportsPath = r'C:\users\%username%\Desktop\Reports' + str(
        '\\' + datetime.today().strftime('%Y-%m-%d')) + '\ExcelReports'
    graphReportsPaht = r'C:\users\%username%\Desktop\Reports' + str(
        '\\' + datetime.today().strftime('%Y-%m-%d')) + '\Graphs'

    new_dir.createDirectory(excelReportsPath)
    new_dir.createDirectory(graphReportsPaht)

    timestump = datetime.today().strftime('%Y-%m-%d-%H_%M_%S')


    file_path = file_path
    from_date = from_date
    to_date = to_date

    ################   Read Arabic Excel ###############################
    # Create DataFrame from Excel file
    # df = pd.read_excel('sells_Arab.xlsx', usecols=['التاريخ', 'الصنف', 'الكمية', 'السعر', 'الإجمالي'])
    # df = df.dropna()
    # df = df.reset_index(drop=True)
    ####################################################################

    # Create DataFrame from Excel file
    df = pd.read_excel(file_path)

    # print the data frame to the console
    print("############# ORIGINAL FILE ################")
    print(df)
    print("############################################")

    # Create a Pandas Excel writer object
    # using XlsxWriter as the engine.
    writer = pd.ExcelWriter(os.path.expandvars(excelReportsPath) + r'\ExcelReports_' + timestump + '.xlsx',
                            engine='xlsxwriter', date_format='%Y/%m/%d', datetime_format='yyyy/mm/dd')

    # Call the Filter By Function
    filter.filter_by(df, writer, filter_by)

    '''create column month from the Date field to be able to group by Month
    %m month as 0 padded decimal number user %B for Full Name month exp: %B %Y => Month Year (December 2012)
    '''

    # df['month'] = pd.to_datetime(df['date']).dt.month
    df['month'] = pd.to_datetime(df['date']).dt.strftime('%m %B').sort_index()
    # df['month'] = pd.to_datetime(df['date']).dt.strftime('%B')

    if revenues_per_month:
        ########################## Revenues per Month #############################
        df3 = df.groupby('month').sum()
        df_total_each_month = df3[['total']]
        df_total_each_month.to_excel(writer, sheet_name='RevnuesPerMonth')

        # These Are Axises
        x_axis_per_month = df_total_each_month.index
        y_axis_df_total_each_category_per_month = df_total_each_month['total']

        colors = myAll.generate_colors(12)
        fig3 = go.Figure(data=[
            go.Bar(
                name='Revenues Per Month',
                x=x_axis_per_month,
                y=y_axis_df_total_each_category_per_month,
                marker_color=colors
            )
        ])

        # Edit the layout Figure3
        fig3.update_layout(title='Revenues per Month',
                           xaxis_title='Months',
                           yaxis_title='Revenues (Dinar DZ)')
        plotly.offline.plot(fig3,
                            filename=os.path.expandvars(graphReportsPaht) + r'\RevenuesPerMonth_' + timestump + '.html',
                            auto_open=False)

        # print("This is Per Month:\n",df_total_each_month)
        ###########################################################################

    if revenues_each_category_per_year:
        ############################ Revenues of each Category per year############
        df_total_each_category = df.groupby(['category']).sum()
        df_total_each_category = df_total_each_category[['total']]
        df_total_each_category.to_excel(writer, sheet_name='RevnuesPerYear')

        x_axis_per_year = df_total_each_category.index
        y_axis_df_total_each_category = df_total_each_category['total']

        colors = myAll.generate_colors(3)
        fig2 = go.Figure(data=[
            go.Bar(
                name='Revenues Of Year',
                x=x_axis_per_year,
                y=y_axis_df_total_each_category,
                marker_color=colors
            )
        ])

        # Edit the layout Figure2
        fig2.update_layout(title='Categories Revenues Of Year',
                           xaxis_title='Categories',
                           yaxis_title='Revenues (Dinar DZ)')
        plotly.offline.plot(fig2,
                            filename=os.path.expandvars(graphReportsPaht) + r'\RevenuesPerYear_' + timestump + '.html',
                            auto_open=False)

        # print(df_total_each_category)
        ###########################################################################

    if revenues_each_category_qte_per_month:
        ###################### Revenues of each category and quantity sold per Month #####################
        df_total_each_category_per_month = df.groupby(['category', 'month']).sum()
        df_total_each_category_per_month = df_total_each_category_per_month[['qte', 'total']]
        df_total_each_category_per_month.to_excel(writer, sheet_name='RevnuesOfEachCategoryPerMonth')

        df_cat1 = df_total_each_category_per_month.loc["cat1", ["qte", "total"]]
        df_cat2 = df_total_each_category_per_month.loc["cat2", ["qte", "total"]]
        df_cat3 = df_total_each_category_per_month.loc["cat3", ["qte", "total"]]

        x_axis_cat1 = df_cat1.sort_index().index
        x_axis_cat2 = df_cat2.sort_index().index
        x_axis_cat3 = df_cat3.sort_index().index

        y_axis_cat1 = df_cat1['total']
        y_axis_cat2 = df_cat2['total']
        y_axis_cat3 = df_cat3['total']
        y_axis_cat1_qte = df_cat1['qte']
        y_axis_cat2_qte = df_cat2['qte']
        y_axis_cat3_qte = df_cat3['qte']

        # Revenues of each category Per Month
        fig1 = go.Figure()

        # Quantity sold in each month of each category
        fig4 = go.Figure()

        fig1.add_trace(go.Scatter(x=x_axis_cat1, y=y_axis_cat1,
                                  mode='lines+markers',
                                  name='Category 1',
                                  line=dict(color='firebrick', width=4, dash='dot')
                                  ))

        fig1.add_trace(go.Scatter(x=x_axis_cat2, y=y_axis_cat2,
                                  mode='lines+markers',
                                  name='Category 2',
                                  line_color='rgb(231,20,243)',
                                  ))

        fig1.add_trace(go.Scatter(x=x_axis_cat3, y=y_axis_cat3,
                                  mode='lines+markers',
                                  name='Category 3'))

        fig4.add_trace(go.Scatter(x=x_axis_cat1, y=y_axis_cat1_qte,
                                  mode='lines+markers',
                                  name='Category 1',
                                  line=dict(color='firebrick', width=4, dash='dot')
                                  ))

        fig4.add_trace(go.Scatter(x=x_axis_cat2, y=y_axis_cat2_qte,
                                  mode='lines+markers',
                                  name='Category 2',
                                  line_color='rgb(231,20,243)',
                                  ))

        fig4.add_trace(go.Scatter(x=x_axis_cat3, y=y_axis_cat3_qte,
                                  mode='lines+markers',
                                  name='Category 3'))

        # Edit the layout Figure1
        fig1.update_layout(title='Categories Revenues Per Month',
                           xaxis_title='Month',
                           yaxis_title='Revenues (Dinar DZ)')

        # Edit the layout Figure4
        fig4.update_layout(title='Quantity sold per Month',
                           xaxis_title='Months',
                           yaxis_title='Quantity (N° pieces)')

        plotly.offline.plot(fig1,
                            filename=os.path.expandvars(graphReportsPaht) + r'\RevenuesPerMonth_' + timestump + '.html',
                            auto_open=False)
        plotly.offline.plot(fig4, filename=os.path.expandvars(
            graphReportsPaht) + r'\QuantitySoldEachMonth_' + timestump + '.html', auto_open=False)

        # print(df_total_each_category_per_month[['qte','total']])
        ##################################################################################################

    if revenues_period:
        ############################### get Revenues of each category in a certain period ###############
        df_total_period_indexed = df.set_index(["date"])

        if (from_date not in df.values) or (to_date not in df.values):
            return False

        df_total_period = df_total_period_indexed.loc[from_date:to_date]
        df_total_period = df_total_period.groupby(['category']).sum()
        df_total_period = df_total_period[['qte', 'total']]
        df_total_period.to_excel(writer, sheet_name='RevnuesInPeriod')

        x_axis_period = df_total_period.index
        y_axis_df_total_priod = df_total_period['total']
        y_axis_df_total_priod_qte = df_total_period['qte']

        colors = myAll.generate_colors(3)
        fig5 = go.Figure(data=[
            go.Bar(
                name='Revenues of The Period: From' + ' ' + 'To' + ' ',
                x=x_axis_period,
                y=y_axis_df_total_priod,
                marker_color=colors
            )
        ])

        colors = myAll.generate_colors(3)
        fig6 = go.Figure(data=[
            go.Bar(
                name='Quantity sold in a given period',
                x=x_axis_period,
                y=y_axis_df_total_priod_qte,
                marker_color=colors
            )
        ])

        # Edit the layout Figure5
        fig5.update_layout(title='Revenues Of Period',
                           xaxis_title='Categories',
                           yaxis_title='Revenues (Dinar DZ)')

        # Edit the layout Figure6
        fig6.update_layout(title='Quantity sold in the Period',
                           xaxis_title='Categories',
                           yaxis_title='Quantity (N° pieces)')
        plotly.offline.plot(fig5,
                            filename=os.path.expandvars(graphReportsPaht) + r'\RevenuesPeriod_' + timestump + '.html',
                            auto_open=False)
        plotly.offline.plot(fig6, filename=os.path.expandvars(
            graphReportsPaht) + r'\QuantitySoldInPeriod_' + timestump + '.html', auto_open=False)

        # print(df_total_period)
        ##################################################################################################
    writer.save()

    return True
