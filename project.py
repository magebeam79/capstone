#!/usr/bin/env python3

import pandas as pd
import glob
import matplotlib.pyplot as plt
import os
import shutil

def input_year(year):
    """find sales reports for the inputted year"""
    find_files = pd.concat(map(pd.read_csv, glob.glob(f"monthly_reports/*{year}.csv")))
    return find_files

def clean_data(find_files):
    """clean data, remove and format columns"""
    report_year = find_files

    """remove columns that we will not be working with"""
    report_year.drop(['Net amount', 'Type'], inplace=True, axis=1, errors='ignore')

    """clean the data; drop na and drop -- (empty columns)"""
    report_year = report_year[report_year != '--']
    report_year = report_year.dropna(how='any')

    """rename column"""
    report_year.rename(columns={'Gross transaction amount': 'Transaction amount'}, inplace=True)
    report_year.rename(columns={'Transaction creation date':'Date'}, inplace=True)

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
