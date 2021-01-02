from datetime import datetime
import os

import pandas as pd
import plotly
import plotly.graph_objects as go

# my Modules
import allFunctions as myAll
import createDirectory as new_dir
import filterByAR as filter


def script(revenues_per_month,
           revenues_each_category_per_year,
           revenues_each_category_qte_per_month,
           revenues_period, file_path, filter_by, from_date, to_date):


    excelReportsPath = r'C:\users\%username%\Desktop\التقارير' + str(
        '\\' + datetime.today().strftime('%Y-%m-%d')) + '\تقارير_الاكسل'
    graphReportsPaht = r'C:\users\%username%\Desktop\التقارير' + str(
        '\\' + datetime.today().strftime('%Y-%m-%d')) + '\المنحنيات_البيانية'

    new_dir.createDirectory(excelReportsPath)
    new_dir.createDirectory(graphReportsPaht)

    timestump = datetime.today().strftime('%Y-%m-%d-%H_%M_%S')


    file_path = file_path
    from_date = from_date
    to_date = to_date
    list_of_months=['جانفي','فيفري','مارس','أفريل','ماي','جوان','جويلية','أوت','سبتمبر','أكتوبر','نوفمبر','ديسمبر']

    ################   Read Arabic Excel ###############################
    # Create DataFrame from Excel file
    df = pd.read_excel(file_path, usecols=['التاريخ', 'الصنف', 'الكمية', 'السعر', 'اجمالي'])
    df = df.dropna()
    df = df.reset_index(drop=True)
    ####################################################################

    # Create DataFrame from Excel file
    # df = pd.read_excel(file_path)

    # print the data frame to the console
    print("############# ORIGINAL FILE ################")
    print(df)
    print("############################################")

    # Create a Pandas Excel writer object
    # using XlsxWriter as the engine.
    writer = pd.ExcelWriter(os.path.expandvars(excelReportsPath) + r'\التقارير_' + timestump + '.xlsx',
                            engine='xlsxwriter', date_format='%Y/%m/%d', datetime_format='yyyy/mm/dd')

    ''' Check The Problem Is Here '''

    # Call the Filter By Function
    filter.filter_by(df, writer, filter_by)


    '''create column month from the Date field to be able to group by Month
    %m month as 0 padded decimal number user %B for Full Name month exp: %B %Y => Month Year (December 2012)
    '''

    # df['month'] = pd.to_datetime(df['date']).dt.month
    df['الشهر'] = pd.to_datetime(df['التاريخ']).dt.strftime('%m %B').sort_index()
    # df['month'] = pd.to_datetime(df['date']).dt.strftime('%B')

    if revenues_per_month:
        ########################## Revenues per Month #############################
        df3 = df.groupby('الشهر').sum()
        df_total_each_month = df3[['اجمالي']]
        df_total_each_month.to_excel(writer, sheet_name='الايرادات الشهرية')

        ################# Format the Cells of the Sheet #######################
        workbook=writer.book
        df_total_each_month_formated = writer.sheets['الايرادات الشهرية']
        cell_text_center = workbook.add_format({'align': 'center'})
        right_to_left=workbook.add_format({'reading_order': 2,'bold': True})
        # Change the direction for the worksheet.
        df_total_each_month_formated.right_to_left()
        df_total_each_month_formated.set_column('A:A',20,right_to_left)
        df_total_each_month_formated.set_column('B:B',20,right_to_left)
        df_total_each_month_formated.set_column('B:B',20,cell_text_center)
        #######################################################################

        # These Are Axises
        # x_axis_per_month = df_total_each_month.index
        x_axis_per_month = list_of_months
        y_axis_df_total_each_category_per_month = df_total_each_month['اجمالي']

        colors = myAll.generate_colors(12)
        fig3 = go.Figure(data=[
            go.Bar(
                name='الايرادات الشهرية',
                x=x_axis_per_month,
                y=y_axis_df_total_each_category_per_month,
                marker_color=colors
            )
        ])

        # Edit the layout Figure3
        fig3.update_layout(title='الايرادات الشهرية',
                           xaxis_title='الاشهر',
                           yaxis_title='الايرادات (دينار جزائري)')
        plotly.offline.plot(fig3,
                            filename=os.path.expandvars(graphReportsPaht) + r'\الارادات_الشهرية_' + timestump + '.html',
                            auto_open=False)


        # print("This is Per Month:\n",df_total_each_month)
        ###########################################################################

    if revenues_each_category_per_year:
        ############################ Revenues of each Category per year############
        df_total_each_category = df.groupby(['الصنف']).sum()

        df_total_each_category = df_total_each_category[['اجمالي']]
        df_total_each_category.to_excel(writer, sheet_name='الايرادات السنوية')

        ################# Format the Cells of the Sheet #######################
        workbook=writer.book
        df_total_each_category_formated = writer.sheets['الايرادات السنوية']
        cell_text_center = workbook.add_format({'align': 'center'})
        right_to_left=workbook.add_format({'reading_order': 2,'bold': True})
        # Change the direction for the worksheet.
        df_total_each_category_formated.right_to_left()
        df_total_each_category_formated.set_column('B:B',20,right_to_left)
        df_total_each_category_formated.set_column('B:B',20,cell_text_center)
        #######################################################################

        x_axis_per_year = df_total_each_category.index
        y_axis_df_total_each_category = df_total_each_category['اجمالي']

        colors = myAll.generate_colors(3)
        fig2 = go.Figure(data=[
            go.Bar(
                name='الايرادات السنوية',
                x=x_axis_per_year,
                y=y_axis_df_total_each_category,
                marker_color=colors
            )
        ])

        # Edit the layout Figure2
        fig2.update_layout(title='الايرادات السنوية',
                           xaxis_title='الاصناف',
                           yaxis_title='الايرادات (دينار جزائري)')
        plotly.offline.plot(fig2,
                            filename=os.path.expandvars(graphReportsPaht) + r'\الايرادات_السنوية_' + timestump + '.html',
                            auto_open=False)

        # print(df_total_each_category)
        ###########################################################################

    if revenues_each_category_qte_per_month:
        ###################### Revenues of each category and quantity sold per Month #####################
        df_total_each_category_per_month = df.groupby(['الصنف', 'الشهر']).sum()
        df_total_each_category_per_month = df_total_each_category_per_month[['الكمية', 'اجمالي']]
        df_total_each_category_per_month.to_excel(writer, sheet_name='ايرادات كل صنف في الشهر')

        ################# Format the Cells of the Sheet #######################
        workbook = writer.book
        df_total_each_category_per_month_formated = writer.sheets['ايرادات كل صنف في الشهر']
        cell_text_center = workbook.add_format({'align': 'center'})
        right_to_left = workbook.add_format({'reading_order': 2, 'bold': True})
        # Change the direction for the worksheet.
        df_total_each_category_per_month_formated.right_to_left()
        # df_total_each_category_per_month_formated.set_column('B:B', 20, right_to_left)
        # df_total_each_category_per_month_formated.set_column('C:C', 20, right_to_left)
        df_total_each_category_per_month_formated.set_column('D:D', 20, right_to_left)
        df_total_each_category_per_month_formated.set_column('B:B', 20, cell_text_center)
        df_total_each_category_per_month_formated.set_column('C:C', 20, cell_text_center)
        df_total_each_category_per_month_formated.set_column('D:D', 20, cell_text_center)
        #######################################################################


        df_cat1 = df_total_each_category_per_month.loc["صنف1", ["الكمية", "اجمالي"]]
        df_cat2 = df_total_each_category_per_month.loc["صنف2", ["الكمية", "اجمالي"]]
        df_cat3 = df_total_each_category_per_month.loc["صنف3", ["الكمية", "اجمالي"]]

        # x_axis_cat1 = df_cat1.sort_index().index
        # x_axis_cat2 = df_cat2.sort_index().index
        # x_axis_cat3 = df_cat3.sort_index().index

        x_axis_cat1=list_of_months
        x_axis_cat2=list_of_months
        x_axis_cat3=list_of_months

        y_axis_cat1 = df_cat1['اجمالي']
        y_axis_cat2 = df_cat2['اجمالي']
        y_axis_cat3 = df_cat3['اجمالي']
        y_axis_cat1_qte = df_cat1['الكمية']
        y_axis_cat2_qte = df_cat2['الكمية']
        y_axis_cat3_qte = df_cat3['الكمية']

        # Revenues of each category Per Month
        fig1 = go.Figure()

        # Quantity sold in each month of each category
        fig4 = go.Figure()

        fig1.add_trace(go.Scatter(x=x_axis_cat1, y=y_axis_cat1,
                                  mode='lines+markers',
                                  name='الصنف 1',
                                  line=dict(color='firebrick', width=4, dash='dot')
                                  ))

        fig1.add_trace(go.Scatter(x=x_axis_cat2, y=y_axis_cat2,
                                  mode='lines+markers',
                                  name='الصنف 2',
                                  line_color='rgb(231,20,243)',
                                  ))

        fig1.add_trace(go.Scatter(x=x_axis_cat3, y=y_axis_cat3,
                                  mode='lines+markers',
                                  name='الصنف 3'))

        fig4.add_trace(go.Scatter(x=x_axis_cat1, y=y_axis_cat1_qte,
                                  mode='lines+markers',
                                  name='الصنف 1',
                                  line=dict(color='firebrick', width=4, dash='dot')
                                  ))

        fig4.add_trace(go.Scatter(x=x_axis_cat2, y=y_axis_cat2_qte,
                                  mode='lines+markers',
                                  name='الصنف 2',
                                  line_color='rgb(231,20,243)',
                                  ))

        fig4.add_trace(go.Scatter(x=x_axis_cat3, y=y_axis_cat3_qte,
                                  mode='lines+markers',
                                  name='الصنف 3'))

        # Edit the layout Figure1
        fig1.update_layout(title='ايرادات كل صنف في الشهر',
                           xaxis_title='الشهر',
                           yaxis_title='الايرادات (دينار جزائري)')

        # Edit the layout Figure4
        fig4.update_layout(title='الكمية المباعة في الشهر',
                           xaxis_title='الاشهر',
                           yaxis_title='الكمية (عدد القطع)')

        plotly.offline.plot(fig1,
                            filename=os.path.expandvars(graphReportsPaht) + r'\الايرادات_الشهرية_' + timestump + '.html',
                            auto_open=False)
        plotly.offline.plot(fig4, filename=os.path.expandvars(
            graphReportsPaht) + r'\الكمية_المباعة_الشهر_' + timestump + '.html', auto_open=False)

        # print(df_total_each_category_per_month[['qte','total']])
        ##################################################################################################

    if revenues_period:
        ############################### get Revenues of each category in a certain period ###############
        df_total_period_indexed = df.set_index(["التاريخ"])

        if (from_date not in df.values) or (to_date not in df.values):
            return False

        df_total_period = df_total_period_indexed.loc[from_date:to_date]
        df_total_period = df_total_period.groupby(['الصنف']).sum()
        df_total_period = df_total_period[['الكمية', 'اجمالي']]
        df_total_period.to_excel(writer, sheet_name='الايرادات_في_فترة_معينة')

        # ################# Format the Cells of the Sheet #######################
        workbook = writer.book
        df_total_period_formated = writer.sheets['الايرادات_في_فترة_معينة']
        cell_text_center = workbook.add_format({'align': 'center'})
        right_to_left = workbook.add_format({'reading_order': 2, 'bold': True})
        # Change the direction for the worksheet.
        df_total_period_formated.right_to_left()
        df_total_period_formated.set_column('D:D', 20, right_to_left)
        df_total_period_formated.set_column('C:C', 20, right_to_left)
        df_total_period_formated.set_column('B:B', 20, cell_text_center)
        df_total_period_formated.set_column('C:C', 20, cell_text_center)
        # #######################################################################

        x_axis_period = df_total_period.index
        y_axis_df_total_priod = df_total_period['اجمالي']
        y_axis_df_total_priod_qte = df_total_period['الكمية']

        colors = myAll.generate_colors(3)
        fig5 = go.Figure(data=[
            go.Bar(
                name='الايرادات في الفترة المحددة',
                x=x_axis_period,
                y=y_axis_df_total_priod,
                marker_color=colors
            )
        ])

        colors = myAll.generate_colors(3)
        fig6 = go.Figure(data=[
            go.Bar(
                name='الكمية المباعة في الفترة المحددة',
                x=x_axis_period,
                y=y_axis_df_total_priod_qte,
                marker_color=colors
            )
        ])

        # Edit the layout Figure5
        fig5.update_layout(title='ايرادات الفترة المحددة',
                           xaxis_title='الاصناف',
                           yaxis_title='الايرادات (دينار جزائري)')

        # Edit the layout Figure6
        fig6.update_layout(title='الكمية المباعة في الفترة المحددة',
                           xaxis_title='الاصناف',
                           yaxis_title='الكمية (عدد القطع)')
        plotly.offline.plot(fig5,
                            filename=os.path.expandvars(graphReportsPaht) + r'\ايرادات_الفترة_' + timestump + '.html',
                            auto_open=False)
        plotly.offline.plot(fig6, filename=os.path.expandvars(
            graphReportsPaht) + r'\الكمية_المباعة_خلال_الفترة_' + timestump + '.html', auto_open=False)

        # print(df_total_period)
        ##################################################################################################
    writer.save()

    return True
