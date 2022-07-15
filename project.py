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
