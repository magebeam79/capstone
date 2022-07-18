#project.py eBay yearly sales reports

This is a program designed to take monthly sales reports in csv file format and produce accounting numbers for gross sales including shipping charges, total fees charged by the platform, and net sales.

Monthly reports contain a approximately 21 columns and approximately 35+ rows. Columns contain protected personal information pertaining to customers name and address. 

To reduce the demand on system resources while also protecting customer's PPI, unused columns will be dropped from the files.

It will then perform clean up on the data, removing NaN and other invalid rows/columns.

After cleaning the data, the program then converts columns into the correct type and returns the data frame.

In the next portion of the program, a function named run_totals() calculates the total final value fees, gross sales, and then net sales. It returns the data frame in summary format grouped by month.

The next function named yearly_reports() saves the created dataframe to a .csv file, then copies and renames the .csv file to the folder yearly_reports. The name of the .csv file is then appended with the year that the report corresponds to.

In the graph() function the data is read from the newly created .csv file and used to form a graph. The graph currently illustrates the gross monthly sales of the current report year. The graph is then saved as an image file with the year appended to the file name.

The final function creates an email within gmail and sends the created graph and yearly report files to the rec_email. The email address and passwords used
are contained in a separate file called .env. For further instructions on replacing email and passwords with variables please view documentation on python-dotenv



## CONTENT

- [EBAY YEARLY SALES REPORTS](#ebay-yearly-sales-reports)
  - [CONTENT](#content)
  - [REPO STRUCTURE](#repo-structure)
  - [`MONTHLY_REPORTS` FOLDER EXPLANATION](#data-folder-explanation)
  - [REQUIREMENTS](#requirements)
  - [USAGE](#usage)

<br/>

## REPO STRUCTURE

- [`requirements.txt`](requirements.txt): contains python packages required for the python code in this repo
- All codes and data are stored in [`src/`](/src/) folder:
  - [`src/monthly_reports/`](src/monthly_reports/): contains sample csv data for this repo
  - [`src/project.py`](src/project.py): contains all source code for this project
  - [`src/test_project.py`](src/test_project.py): contains all pyproject testing code for this project

<br/>

## `MONTHLY_REPORTS` FOLDER EXPLANATION

The monthly reports folder contains sampls csv files for processing yearly reports. It does not contain an exhaustive list for each year.

<br/>

## REQUIREMENTS

- Python 3.6+
- [Dependencies](requirements.txt)

<br/>

## USAGE

1. Clone this repository:

   ```console
   $ git clone https://github.com/magebeam79/capstone.git   #if you have git
   # if you don't have git, you can download the zip file then unzip
   ```

2. (Optional): create virtual environment for python to install dependency:
   Note: you can change the `pyvenv` to another name if desired.

   ```console
   $ python -m venv pyvenv   # Create virtual environment
   $ source pyvenv/bin/activate    # Activate the virtual environment on Linux
   # pyvenv\Scripts\activate    # Activate the virtual environment on Windows
   ```

3. Install python dependencies:

   ```console
   $ pip install -r requirements.txt
   ```

4. Example usage:

    - `project.py`

      ```console
      $ python src/project.py
      ```

<br/>
