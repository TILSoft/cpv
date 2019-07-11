# Project TODO list

- Special Parameters
  - [ ] from params main filter out non special params and save as df_spec
  - if not redo
    - [ ] get all df_spec params from the database to ensure agg functions are recalculated based on all values
  - [ ] get list of tasks for special
  - [ ] if thickness manuall present, ignore AT4 parameter
  - [ ] ignore hardness 0 values to not affect MIN value

- Parameters cleanup and preparation
  - [ ] all numeric 4 decimal places
  - [ ] all MM:SS formats - remove the date part and apply formating
  - [ ] if date value has time 00:00:00 take only date part
  - [x] drop dates starting with 0 or 28
  - [x] if year 1899 take only the time part

- Scheduler
  - [ ] have a way to run the db update periodically, possibly based on the recorded last extraction date
  - [x] update db with only new or changed parameters after the last date, use the inputdate as a indicator
  - [x] assess the performance when running weekly, daily or hourly

- Dataframes
  - [x] copy all values into a single values column
  - [x] have another column indicating unit or datatype
  - [x] df with process orders: po, batch, material, launch date
  - [x] df with all finished or intermediate materials descriptions

- Parameter special cases
  - [x] get missing parameters from APR queries
  - [x] have an extra column marking parameters for agg functions
  - [ ] have a way to process agg parameters separately and then merge results with the rest

- Mysql database
  - [x] table with all the parameter names, codes and ?types
  - [x] main table with results: (parameter name, po) as PK, input date, value, (unit or type)
  - [ ] table for POs
  - [ ] table for material descriptions

- XFP connection
  - [x] have class with a method to execute SQL select and return dataframe
  - [x] extract parameters
  - [x] extract work orders

- LIMS data
  - [ ] get sql query from QV
  - [ ] if possible match product families names to XFP for braincube joining

- CPV/APR
  - [ ] script to dump parameters into separate files per product family

- Braincube
  - [ ] script to dump data into separate files for parameters, POs and descriptions