# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 09:13:49 2017

@author: TA2761
cleaneded up ready for project
"""

expected = ["Alley", "Avenue", "Boulevard", "Broadway", "Bypass", "Center", "Circle", "Commons", "Court", "Cove", \
            "Drive", "Fork", "Glen", "Heights", "Highway", "Hills", "Hollow", "Landing", "Lane", "North", \
            "Park", "Parkway", "Pass", \
            "Pike", "Place", \
            "Plaza", "Road", "Square", \
            "Street", "Terrace", "Trace", 
            "Trail", "Way"]

type_mapping = { "A": "Avenue", 
            "ave": "Avenue",
            "Ave": "Avenue",
            "avenue": "Avenue",
            "AVENUE": "Avenue",
            "B": "Boulevard", 
            "Blvd": "Boulevard",
            "BLVD": "Boulevard",
            "Cir": "Circle",
            "Crt": "Court",
            "Ct": "Court",
            "Dr": "Drive",
            "hills": "Hills",
            "Hwy": "Highway",
            "Hwy.": "Highway",
            "Ln": "Lane",
            "pike": "Pike",
            "Pk": "Park",
            "Pkwy": "Parkway",
            "Pky": "Parkway",
            "Pl": "Place",
            "Rd": "Road",
            "Rd.": "Road",
            "S": "South", 
            "st": "Street",
            "St": "Street",
            "St.": "Street",
            }

not_found_mapping = {
        "1705": "",
        "1800": "",
        "37076,": "",
        "Ave": "Avenue",
        "Ave,": "Avenue",
        "B": "Boulevard",
        "Blvd": "Boulevard",
        "E": "East",
        "Dr": "Drive",
        "Hermitage,": "",
        "Hwy": "Highway",
        "Ln": "Lane",
        "N": "North",
        "Parkway,": "Parkway",
        "Pike,": "Pike",
        "S": "South",
        "S.": "South",
        "st.": "Street",
        "St.": "Street",
        "States": "State",
        "Ste": "Suite",
        "TN": "",
        "TN-76": "State Highway 76",
        "W": "West",
        "USA": "",
        }
