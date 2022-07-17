#!/usr/bin/env python3

import pandas as pd
import glob
import matplotlib.pyplot as plt
import os
import shutil
import sys
from datetime import datetime
import re


def main():
    year = input("Please enter a yearly report needed: ")
    check_year(year)
    check_path(year)
    find_files = read_files(year)
    find_totals = clean_data(find_files)
    totals = run_totals(find_totals)
    run_totals(find_totals)
    (yearly_report(totals, year))
    graph(year)


def check_year(year):
    """verify that input year is four digits between 2020 and the current year"""
    current_year = datetime.now().year
    pattern = r'(^20[2][0-9]$)'

    while True:
        try:
            year = int(year)
            if 2020 > year or year > current_year:
                sys.exit(f'There are no reports for that year. Please enter a year between 2020 and {current_year}.')
            if re.match(pattern, str(year)):
                print(f'Your report for year {year} will be processed shortly.')
                break
            else:
                sys.exit(f'Please enter a four digit year between 2020 and {current_year}.')

        except ValueError:
            print("Please enter a valid four digit year.")
            break


def check_path(year):
    """verify file path with given year"""
    path = f"monthly_reports/*{year}.csv"

    if glob.glob(path):
        print(f"Files exist for {year}.")
    else:
        sys.exit(f"No files exist for {year}.")


def read_files(year):
    """find sales reports for the inputted year"""
    find_files = pd.concat(map(pd.read_csv, glob.glob(f"monthly_reports/*{year}.csv")))
    return find_files


def clean_data(find_files):
    """clean data, remove and format columns"""
    report_year = find_files

    """keep only the columns that are needed for the reports"""
    report_year.drop(report_year.columns.difference(['Gross transaction amount', 'Transaction creation date',
                                                     'Transaction amount', 'Shipping and handling',
                                                     'Final Value Fee - fixed',
                                                     'Final Value Fee - variable', 'Quantity', 'Order number',
                                                     'Item title']), inplace=True, axis=1, errors='ignore')

    """clean the data; drop na and drop -- (empty columns)"""
    report_year = report_year[report_year != '--']
    report_year = report_year.dropna(how='any')

    """rename column"""
    report_year.rename(columns={'Gross transaction amount': 'Transaction amount'}, inplace=True)
    report_year.rename(columns={'Transaction creation date': 'Date'}, inplace=True)

    """remove comma from column"""
    report_year['Transaction amount'] = report_year['Transaction amount'].astype(str)
    report_year['Transaction amount'] = report_year['Transaction amount'].str.replace(',', '')

    """convert columns to the correct type"""
    report_year['Transaction amount'] = pd.to_numeric(report_year['Transaction amount'])
    report_year['Shipping and handling'] = pd.to_numeric(report_year['Shipping and handling'])
    report_year['Final Value Fee - fixed'] = pd.to_numeric(report_year['Final Value Fee - fixed'])
    report_year['Final Value Fee - variable'] = pd.to_numeric(report_year['Final Value Fee - variable'])
    report_year['Quantity'] = pd.to_numeric(report_year['Quantity'])

    """convert transaction create date to datetime"""
    report_year['Date'] = pd.to_datetime(report_year['Date'])

    return report_year


def run_totals(find_totals):
    totals = find_totals

    """add a total final value fee column"""
    totals['Final Value Fee - total'] = totals['Final Value Fee - fixed'] + totals['Final Value Fee - variable']

    """add a gross sales amount that totals the transaction amount with the shipping and handling"""
    totals['Gross sales'] = totals['Transaction amount'] + totals['Shipping and handling']

    """add a net sales amount that subtracts the total final value fees from the gross sales"""
    totals['Net sales'] = totals['Gross sales'] - totals['Final Value Fee - total']

    """reorder the columns"""
    totals = totals[['Date', 'Order number', 'Item title', 'Quantity', 'Transaction amount',
                     'Shipping and handling', 'Gross sales',
                     'Final Value Fee - fixed', 'Final Value Fee - variable', 'Final Value Fee - total', 'Net sales']]

    # print(totals.describe())
    # print(totals.to_string())

    """group by Date sorted by gross transaction amount"""
    return totals.groupby(pd.Grouper(key='Date', axis=0, freq='M')).sum()


def yearly_report(totals, year):
    totals.reset_index(inplace=True)
    year = str(year)

    """return monthly sales for year as csv file"""
    totals.to_csv('monthly_totals.csv')

    """save the the report in the yearly reports directory with the correct report year"""
    if os.path.isfile(f'yearly_reports/monthly_totals_{year}.csv'):
        pass
    else:
        shutil.copy('monthly_totals.csv', 'yearly_reports/monthly_totals.csv')
        os.rename('yearly_reports/monthly_totals.csv', f'yearly_reports/monthly_totals_{year}.csv')


def graph(year):
    """configure bar graph for monthly sales for year and input data"""
    data = pd.read_csv('monthly_totals.csv')
    df = pd.DataFrame(data)

    plt.rcParams['figure.figsize'] = [10, 6]
    plt.rcParams['figure.autolayout'] = True
    plt.tick_params(rotation=45)
    plt.bar(df['Date'], df['Gross sales'], color='cyan', edgecolor='darkblue')
    plt.title(f'Monthly Gross Sales\n{year}', fontsize=16)
    plt.xlabel('Month')
    plt.ylabel('Sales in USD ($)')

    """Save sales graph"""
    plt.savefig('sales_graph.png')
    plt.show()

    """save sales graph in the yearly reports directory with the correct year"""
    if os.path.isfile(f'yearly_reports/sales_graph_{year}.png'):
        pass
    else:
        shutil.copy('sales_graph.png', 'yearly_reports/sales_graph.png')
        os.rename('yearly_reports/sales_graph.png', f'yearly_reports/sales_graph_{year}.png')


if __name__ == '__main__':
    main()
