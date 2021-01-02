
import pandas as pd

def filter_by(df,writer,param_to_filter):
    last_cat = list()  # used to save The last Category to filter by it again
    single_cat_list = list()  # used to filter by

    single_date_list = list()
    last_date = list()


    if(param_to_filter.lower()=='category'):

        ###################################### Filter By Category ##########################################################

        catgories_list = df[param_to_filter.lower()].tolist()  # Filter by is variable contains the user ComboBox input from UI

        for i in range(len(catgories_list)):

            if catgories_list[i] not in last_cat:
                single_cat_list.append(catgories_list[i])
                last_cat.append(catgories_list[i])

                # DataFrame of Filtred Categories
                df_categories = df[df.category.isin(single_cat_list)]
                df_categories.to_excel(writer, sheet_name=str(single_cat_list[0]), index=False)

                ############# FORMAT CELLS #################################
                # Get the xlsxwriter workbook and worksheet objects.
                workbook=writer.book
                # Add some cell formats.
                cell_text_center = workbook.add_format({'align': 'center'})
                # cell_text_center.set_align('center')
                #Get the Worksheet to apply Format to
                Category_worksheet = writer.sheets[str(single_cat_list[0])]
                # Set the column width and format.
                Category_worksheet.set_column('A:A', 10,None)
                Category_worksheet.set_column('B:B', None,cell_text_center )
                Category_worksheet.set_column('C:C', None,cell_text_center )
                Category_worksheet.set_column('D:D', None,cell_text_center )
                Category_worksheet.set_column('E:E', None,cell_text_center )
                #############################################################

                single_cat_list.remove(catgories_list[i])
        #####################################################################################################################


    elif (param_to_filter.lower()=='date'):

        df['date_str'] = pd.to_datetime(df['date']).dt.strftime('%b')
        date_list = df['date_str'].tolist()  # Filter by is variable contains the user ComboBox input from UI

        for i in range(len(date_list)):

            if date_list[i] not in last_date:
                single_date_list.append(date_list[i])
                last_date.append(date_list[i])

                # DataFrame of Filtred Categories
                df_dates = df[df.date_str.isin(single_date_list)]
                df_dates=df_dates[['date','category','qte','total']]
                df_dates.to_excel(writer, sheet_name=str(single_date_list[0]), index=False)
                single_date_list.remove(date_list[i])

