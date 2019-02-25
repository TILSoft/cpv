# Project TODO list

- Parameters cleanup and preparation
  - [ ] all numeric 4 decimal places
  - [ ] all MM:SS formats - remove the date part and apply formating
  - [ ] if date value has time 00:00:00 take only date part
  - [ ] drop dates starting with 0 or 28
  - [ ] if year 1899 take only the time part

- Scheduler
  - [ ] have a way to run the db update periodically, possibly based on the recorded last extraction date
  - [ ] update db with only new or changed parameters after the last date, use the inputdate as a indicator
  - [ ] assess the performance when running weekly, daily or hourly

- Dataframes
  - [ ] copy all values into a single values column
  - [ ] have another column indicating unit or datatype
  - [ ] df with process orders: po, batch, material, launch date
  - [ ] df with all finished or intermediate materials descriptions

- Parameter special cases
  - [ ] get missing parameters from APR queries
  - [ ] have an extra column marking parameters for agg functions
  - [ ] agg column can have more than 1 entry eg "min,avg"
  - [ ] have a way to process agg parameters separately and then merge results with the rest

- Mysql database
  - [ ] table with all the parameter names, codes and ?types
  - [ ] main table with results: (parameter name, po) as PK, input date, value, (unit or type)
  - [ ] table for POs
  - [ ] table for material descriptions

- XFP connection
  - [ ] have class with a method to execute SQL select and return dataframe

- LIMS data
  - [ ] get sql query from QV
  - [ ] if possible match product families names to XFP for braincube joining

- CPV
  - [ ] script to dump parameters into separate files per product family

- Braincube
  - [ ] script to dump data into separate files for parameters, POs and descriptions