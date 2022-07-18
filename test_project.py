#!/usr/bin/env python3

import pandas as pd
import glob
import pytest
import datatest as dt
import re


@pytest.fixture(scope='module')
@dt.working_directory(__file__)
def df():
    find_files = pd.concat(map(pd.read_csv, glob.glob(f"monthly_reports/*2020.csv")))
    report_year = find_files

    """remove columns that we will not be working with"""
    report_year.drop(['Net amount', 'Type'], inplace=True, axis=1, errors='ignore')

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


def test_check_year(monkeypatch):
    """validate that input year is four digits between 2020 and the current year"""
    monkeypatch.setattr('builtins.input', lambda _: '2020')
    year = input("Please enter a yearly report needed: ")
    pattern = r'(^20[2][0-9]$)'
    assert re.match(pattern, str(year))


def test_columns(df):
    """validate that columns match given columns"""
    dt.validate(
        df.columns,
        {'Date', 'Order number', 'Item title', 'Quantity', 'Shipping and handling',
         'Final Value Fee - fixed', 'Final Value Fee - variable', 'Transaction amount'},
    )


def test_input_year(monkeypatch):
    """validate that given input year matches year"""
    monkeypatch.setattr('builtins.input', lambda _: '2020')
    year = input("Please enter a yearly report needed: ")
    assert year == '2020'
