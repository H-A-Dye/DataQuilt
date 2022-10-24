



def extract_data(x_entry):
    """Description of the function/method.
    Move data into a dictionary. 
Parameters:
    <param>: Description of the parameter

Returns:
    <variable>: Description of the return value
"""

    # get date, Tmax, Tmin from an individual entry
    mydate = x_entry.get('date')[0:10]
    # date has empty time data attached
    mytype = x_entry.get('datatype')
    myvalue = x_entry.get('value')
    mydate = datetime.datetime.strptime(mydate, "%Y-%m-%d")
    mym = mydate.month
    myd = mydate.day
    return DayData(mym, myd), {mytype, myvalue}





def place_into_dict(daydata, tempinfo):
"""Description of the function/method.
   Place extracted data into dictionary for the Pillow module
   to use
Parameters:
    <param>: Description of the parameter
    row from a weather data frame
Returns:
    <variable>: Description of the return value
    Month, Day tuple and Data tuple
"""    
    if mydict.get(daydata) is None:
        mydict.update({daydata:tempinfo})

