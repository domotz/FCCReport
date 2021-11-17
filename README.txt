# Banned Device Reports v1.0

This report helps users to find all banned vendors devices by using 
the Domotz Public API. 

---

## Requirements

The project was tested on Python 3.8.5, and it is required to run on that and
subsequent versions.
Python can be downloaded and installed from the following link:  

[Python](https://www.python.org/downloads/)   

*Note* : Knowing how to run a command in the command line system is required.

The next requirement is to have Domotz account and a valid API key that can be 
taken from :  

[How to create an API key](https://help.domotz.com/user-guide/domotz-api/)


---
## Installation 

Extract the project from the .zip file.

##How to use

This procedure should be carried out using the command line in Windows or the
Terminal in Mac or Linux. To generate the report, use your own API key
and enter it in the command. 

Move in the directory containing this README file, for example:

```
cd c:\Users\myself\downloads\FCC_Report
```


Note: You just need to replace your Endpoint and API-key.

```
python -m fcc_covered_list_discovery main_report --endpoint=[Endpoint]  --api_key=[Your API-key]
```

*How the script works*:

It uses the Public-API to connect the user to Domotz, retrieves data from the
user's account, and generates a report file in .xlsx(Excel) format.  

*The output of the script:*

If you run it successfully, you can see the output for the script like:

    The Output file is created
    The Headers are specified
    Columns are fetched to the output file
    All the devices fetched with their agent id
    File `FCC_Report.xlsx` is populated successfully
    Total number of calls which are used :277
    The number of remaining daily call :10323
    consumed Time for preparation of the Report:2.6925208568573 sec

The file FCC_Report.xlsx will contain the details of the banned devices found in your networks.



##  API Reference

 please take a look at the API documentation which includes all the requests are provided in different programming languages :         
* 
   [Domotz Portal ](https://portal.domotz.com/portal/agent_manager/list)


----

## Author

*Mehrdad Babazadeh*
