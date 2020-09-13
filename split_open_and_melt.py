#Import packages
import pandas as pd
from tkinter import filedialog 
import time
import xlrd

#Create Functions



#Function that opens a filedialog box and returns the file selected by the user
def get_filename():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File") 
    return filename



#Function that opens a filedialog box and returns the file selected by the user
def set_filename():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File") 
    return filename



#Function that splits the filename provided by the user and tests to see if it exists in the list of
#usable filetypes.  As of now these include xlsx, csv, and pickle.  Future updates will include SQL inputs.
def get_filetype(filename):
    filetype = filename.split('.')[-1]
    
    usable_filetypes = ['xlsx', 'csv', 'pickle']
    
    if filetype in usable_filetypes:
        return filetype
    else:
        print('Sorry, I cannot process this filetype.  Please select a filetype from the list below' + 
              ' or edit this script:\n')
        for ft in usable_filetypes:
            print(ft)



#For xlsx files with more than one sheet, this function captures user selection for which sheet to import
def get_xl_sheet_name(filename):
    print('You entered an Excel file with more than one sheet. \n' + 
          'Please enter the number of the sheet you wish to split open and melt: \n')
    
    xl = pd.ExcelFile(filename)
    
    if len(xl.sheet_names) == 1:
        return xl_sheet_names(0)
    
    else:
        sheet_dict = {}
        i = 1
        for x in xl.sheet_names:
            sheet_dict[str(i)] = x
            print(str(i) + ': ' + x)
            i += 1

        sheet_key = str(input())
        return sheet_dict[sheet_key]



#Create a dataframe from a xlsx file
def get_df_from_xl(filename, sheet):
    df = pd.read_excel(filename, sheet_name = sheet, header=1)
    return df



#Create a dataframe from a csv file
def get_df_from_csv(filename):
    df = pd.read_csv(filename, header = 1)
    return df



#Create a dataframe from a pickle file
def get_df_from_csv(filename):
    df = pd.read_pickle(filename, header = 1)
    return df






#Main script
print('Hello, I will split open and melt an xlsx or csv file for you.\n' + 
      'Please be advised, I ASSUME YOU INCLUDE COLUMN HEADERS IN THE FIRST ROW!\n' +
      'Select your file...')
time.sleep(1)

filename = get_filename()

filetype = get_filetype(filename)

if filetype == 'xlsx':
    sheet = get_xl_sheet_name(filename)
    df = get_df_from_xl(filename, sheet)
elif filetype == 'csv':
    df = get_df_from_csv(filename)
else:
    df = get_df_from_pickle(filename)

#Prompt user to enter columns to melt into rows
print('The available columns are listed below.\n' + 
      'Enter the number of the column headers you wish to melt into rows and enter any non-number to continue:')

#Provide all column headers to inlcude a number to be entered by the user
col_dict = {}
i = 1
for c in df.columns:
    col_dict[str(i)] = c
    print(str(i) + ': ' + c)
    i += 1

#While the user enters valid values, those are added to a list for melting
#Any invalid entry ends the while loop
user_cols_num = []
user_input = str(input())

while user_input in col_dict.keys():
    user_cols_num.append(user_input)
    user_input = str(input())
    
user_col_names = []
    
#Show user what columns will be melted into rows
print('\nI will melt the following columns into row values:\n')
for uc in user_cols_num:
    print(uc + ': ' + col_dict[uc])
    user_col_names.append(col_dict[uc])

#Define the id values prior to melting
id_vals = []

for c in df.columns:
    if c not in user_col_names:
        id_vals.append(c)

#Melt the df
df_melt = df.melt(id_vars = id_vals, 
                  value_vars = user_col_names, 
                  var_name = 'melted_name', 
                  value_name = 'melted_value')

#Use original filename to get the original folder where outfile is saved (as csv)
out_list = filename.split('/')
out_list.reverse()
out_list = out_list[1:-1]
out_list.reverse()

outfile = ''

for ss in out_list:
    outfile = outfile + '/' + ss
    
outfile = outfile + '/' + filename.split('/')[-1].split('.')[0] + '_split_open_and_melted.csv'

df_melt.to_csv(outfile)