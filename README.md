# capstone ebay sales reports

<!-- This is a program designed to take monthly sales reports in csv file format and produce accounting numbers for gross sales including shipping charges, total fees charged by the platform, and net sales. 

The program is designed to take an input year from the user, and use this input in searching all related sales reports. First it will drop unused columns from the data. It will then perform clean up on the data, removing NaN and other invalid rows/columns. After cleaning the data, the program then converts columns into the correct type and returns the data frame. 

In the next portion of the program, a function named run_totals() calculates the total final value fees, gross sales, and then net sales. It returns the data frame in summary format grouped by month.

The next function named yearly_reports() saves the created dataframe to a .csv file, then copies and renames the .csv file to the folder yearly_reports. The name of the .csv file is then appended with the year that the report corresponds to. 

In the graph() function the data is read from the newly created .csv file and used to form a graph. The graph currently illustrates the gross monthly sales of the current report year. The graph is then saved as an image file with the year appended to the file name.  -->
