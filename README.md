This program was created in IntelliJ PyCharm 2019.3.1 and compiled with Python 3.6.
### Overview & Summary
This program allows the managing and analysis of employee records which are stored locally in both a CSV file and SQLite database. Features include linear regression modeling, statistical analysis, data visualization, and database manipulation through adding, removing, and querying employees. A sample model comparing the effect of employee age and weight on salary is included in the *data* directory.

#### Employee Data
Employee data can be found in the data directory labeled employee-data.csv. Sample employee data can be downloaded [here](http://eforexcel.com/wp/wp-content/uploads/2017/07/1000-Records.zip) and contains 1000 randomly generated employee records that were used for testing. Employee data such as age and company age are automatically updated on program run while records are synced between both the CSV file and database. <br>  
Additional qualitative and quantitative columns may be appended before salary and at the end of the CSV file respectively for further analysis; however, all entries for those columns will have to be entered manually and will not be included in the database. <br><br>
All data columns in order: ID, Name, DOB, DOJ, Phone, Email, Salary, Gender, Age, Company, Weight <br><br>
*Note: Gender is converted to binary 0 (female) or 1 (male) to allow for statistical analysis.*

#### Models
Linear regression models are dynamically generated based on the variables selected and test size with the feature of salary prediction. Only the model and residual graphs are saved in the */data/graphs* directory and can be manually deleted. <br><br>
Statistical analysis includes the count, mean, standard deviation, extremes, and quartiles of each quantitative column.

#### Managing Records
Employees can be added, removed by ID, and queried by any column. While adding an employee, basic regex matching is used to validate that entered names, phones, and emails are as realistic as possible. <br><br>
Existing employee records will have to be manually edited in the CSV file to change information.
