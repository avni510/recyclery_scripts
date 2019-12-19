# Please make sure the P and L is a csv NOT a xslx

import pandas as pd
import os

### VARIABLES TO UPDATE
# Please make sure the working directory has a slash at the end
working_directory = "/Users/avnikothari/Desktop/recyclery/august_2019/"
input_filename = "P_L_August2019.csv" 
output_filename = "P_L_Collapsed_August2019.csv"
empty_rows_in_footer = 4

# Keys are variables that will be outputted in the collapsed csv, 
# the values in the list should exist
# as rows in the input_filename. Please update if there is a mismatch
categories = {
    "Class Income": ["Class Income"],
    "Contributions": ["Individual Contributions", "Corporate Contributions"],
    "Grants": ["Grant Income - Allocated"],
    "Bicycle Sales": ['Bicycles Sold'],
    "Part Sales": ["New Items Sold", "Special Orders Sold", "Used Parts Sold"],
    "Program Income": [],
    "Other Income": ["Rounding - Inc", "Interest Income"],
    "Cost of Goods Sold": ["Bike Parts & Accessories", "Non-Inventory Bike Parts", "Freight & Delivery - COGS"],
    "Bank Expenses": ["PayPal Fees", "Card Processing Fees"],
    "Event Expenses": [],
    "Bike Pickup Expenses": ["Gas for Bike Pickups", "Insurance"],
    "Payroll Expenses": ["Payroll Processing", "Taxes", "Wages", "Worker's Comp Insurance"],
    "Rent": ["Rent or Lease"],
    "Subcontractors": ["Subcontractors"],
    "Utilities": ["Gas", "Telephone & Internet"],
    "Other Expenses": ["Dues & Subscriptions", "Reconciliation Discrepancies", "Food for Meetings", "Food for Volunteers", "Rounding - Exp"],
    "Office and Admin Expenses": ["Accounting Software"],
    "Tools and shop supplies": ["Tools", "Supplies"],
}

### Read and clean p and l 
os.chdir(working_directory)

def str_to_float(value):
    if isinstance(value, str):
        cleaned_value = value.replace('$', '').replace(',', '').replace('\t', '')
        return float(cleaned_value)

# Skips the first 5 rows 
# The header row is denoted in the 6th row
# The headers are renamed to Category and Current Year
# Clean all strings in category column, for column Current Year convert all currency values to a float
# Only use the first 2 columns (drop 2018)
# Do not read the rows in the footer
df = pd.read_csv(
        input_filename, 
        skiprows = range(0, 2),
        header = 3,
        names = ['Category', 'Current Year'],
        converters = {'Category': (lambda x: x.strip()), 'Current Year': str_to_float},
        usecols = range(0, 2),
        skipfooter = empty_rows_in_footer,
        engine = 'python'
        )

# drop all rows that have a Current Year value of 0
df = df[df['Current Year'] != 0]

# drop all rows that have a Current Year value of NaN
df = df.dropna()

# drop all categories related to totals
totals = [
        "Total Other Expenses",
        "Total Sales",
        "Total Cost of Goods Sold",
        "Total Payroll Expenses", 
        "Total Utilities",
        "Net Income",
        "Gross Profit",
        "Total Other Income",
        "Total Expenses", 
        "Net Operating Income", 
        "Total Contributions",
        "Total Income",
        "Net Other Income"
        ]

df = df[~df['Category'].isin(totals)]

# Create a list of all the categories in p and l
categories_in_csv = df['Category'].to_list()

# categories the script will look for in the csv
categories_to_find_in_csv = [item for sublist in categories.values() for item in sublist]

# categories that exist in the script and the csv
categories_in_both = set(categories_in_csv).intersection(categories_to_find_in_csv)
# categories that exist in the script but do not exist in the csv
categories_not_found_in_csv = set(categories_to_find_in_csv) - categories_in_both

# categories that exist in the csv but do not exist in the script
categories_not_in_script = set(categories_in_csv) - categories_in_both

if len(categories_not_found_in_csv) != 0:
    print("These categories exist in the script but do not exist in the P and L (either because the value is 0 or the row does not exist)") 
    print("")
    print(categories_not_found_in_csv)
    print("")
    print("Please delete them in the values of the categories variable in the script")
    print("")

if len(categories_not_in_script) != 0:
    print("These categories exist in P and L, but not in the script") 
    print("")
    print(categories_not_in_script)
    print("")
    print("Please add them in the values of the categories variable in the script")
    print("")

if len(categories_not_found_in_csv) != 0 or len(categories_not_in_script) != 0:
    print("Please update the categories variable in the script and rerun it")
    print("")

    raise Exception

#### Create the collapased data
collapsed_data = []

# for all the values in the categories dictionary find them in the input file and total them
for key, value in categories.items():
    summation = 0
    for category in value:
        row = df.loc[df['Category'] == category].values[0]
        category_value = row[1]
        summation += category_value

    collapsed_data.append([key, round(summation)])

### Add the total categories

# These values comprise of the total income 
total_income_categories = ['Contributions', 'Grants', 'Bicycle Sales', 'Part Sales', 'Other Income', 'Program Income', 'Class Income']

# These values comprise of the total expenses 
total_expenses_categories = ['Cost of Goods Sold', 'Payroll Expenses', 'Rent', 'Utilities', 'Other Expenses', 'Tools and shop supplies', 'Subcontractors', 'Bike Pickup Expenses', 'Bank Expenses', "Office and Admin Expenses"]

# find the corresponding values of each category and total them
total_income = 0
total_expenses = 0
cost_of_goods_sold = 0
for category, value in collapsed_data:
    if category in total_income_categories:
        total_income += value
    elif category in total_expenses_categories:
        total_expenses += value
        if category == "Cost of Goods Sold":
            cost_of_goods_sold = value

total_income = round(total_income)
total_expenses = round(total_expenses)
net_income = round(total_income - total_expenses)
gross_profit = round(total_income - cost_of_goods_sold)

collapsed_data.append(['Total Income', total_income])
collapsed_data.append(['Gross Profit', gross_profit])
collapsed_data.append(['Total Expenses', total_expenses])
collapsed_data.append(['Net Income', net_income])

collapsed_df = pd.DataFrame(collapsed_data)
collapsed_df.columns = ['Category', 'Current Year']

print(collapsed_df)

collapsed_df.to_csv(working_directory + output_filename)
print("Successfully exported to " + working_directory + output_filename)
