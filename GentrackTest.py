#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 21:59:45 2022

This script converts a local XML file to a CSV file following the 
instructions and guidelines supplied by GenTrack

CSVIntervalData row types:
    100 - header
    200 - data, divides following data body into other CSV files
        second field = csv file name
    300 - data
    900 - trailer, file end
    
Assumes:  - each row begins with either 100,200,300,900 in both the input
             CSV Interval Data, and the output CSV file(s)
          - Rows beginning with 200 signals the beginning/end of a CSV file
              to be made
          The input file will always contain:
               - A Header element
               - A Transactions element, containing 1 Transaction element
               - A Transaction element will contain transactionDate and 
               transactionID attributes
               - Required data will be in 
               Transactions->Transaction->MeterDataNotification->CSVIntervalData
               
@author: Julian Ward
"""

#   Import relevant libraries and resources
import os
import csv
from xml.etree import ElementTree


filename = "testfile.xml"
fullfile = os.path.abspath(filename)

dom = ElementTree.parse(fullfile)

csvdata = dom.find('Transactions/Transaction/MeterDataNotification/CSVIntervalData')


#Transactions->Transaction->MeterDataNotification->CSVIntervalData


#   Removes internal whitespace and converts string to list    
csvdata = csvdata.text
csvlist = csvdata
for x in csvlist:
    if (x.isalpha() or x.isnumeric() or x == ',' or x == '.') is False:
        csvlist = csvlist.replace(x,',')
cleanlist = csvlist.split(',')


#   Finds 100,200,300,900 nodes in CSVdata
find100 = []
find200 = []
find300 = []
find900 = []
for x in range (len(cleanlist)-1):
    if cleanlist[x] == '100':
        find100.append(x)
    if cleanlist[x] == '200':
        find200.append(x)
    if cleanlist[x] == '300':
        find300.append(x)
    if cleanlist[x] == '900':
        find900.append(x)

nodes = find100 + find200 + find300 + find900
nodes.sort()

#   Establishes header and trailer rows for CSV file

headerRow = cleanlist[find100[0]:find200[0]]
trailerRow = cleanlist[find900[0]]

    #   Works through cleaned XML file to make CSV file(s)
for i in range (len(find200)):
    #   Makes new CSV file and establishes writing
    fileTitle = cleanlist[find200[i]+1]
    csvfile = open(fileTitle,'w',newline='')
    writefile = csv.writer(csvfile)
    
    #   Writes the header to the new file
    writefile.writerow(headerRow)
    
    #   Generates next CSV row from node map against cleanlist
    current = nodes.index(find200[i])
    nextRow = cleanlist[nodes[current]:nodes[current+1]]
    
    #   Writes the CSV 200 row to the CSV file
    writefile.writerow(nextRow)
    
    #   Moves the row starting node
    current+=1
    
    #   Loops to write 300 rows pertaining to the current 200
    while (nodes[current] in find900 or nodes[current] in find200) is False:
        nextRow = cleanlist[nodes[current]:nodes[current+1]]
        writefile.writerow(nextRow)
        current+=1
        
        #   if the next proposed node is a new 200 or 900 file end, close the file
        if nodes[current] in find900 or nodes[current] in find200:
            writefile.writerow(trailerRow)
            csvfile.close()
            

            
