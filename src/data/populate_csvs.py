"""
Algorithm to populate new csvs:
    1. Get list of csv's in the CSVSTORE
    2. Sort the list of csv's in decreasing order of their date.
    3. For each csv in sorted CSV list:
        3.1 If 
        4.1 Compare the csv date wiht dlcsv. 
        If greater:
            4.1.1 Populate csv
                # Ideally, population should be safe of record exists exception.
            4.1.2 Insert entry into CSVDB
        if less or equal: 
            4.1.3 break;
"""

