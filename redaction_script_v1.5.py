from java.awt import BorderLayout, GridLayout
from javax.swing import JFileChooser, JFrame, JPanel, JOptionPane, JButton 
from datetime import datetime
import os
import csv

"""
Redaction Script for NUIX Productions

Date: 2020-08-07
Author(s): HR, TW

"""

markupSets = current_case.getMarkupSets()
target_markup_set = []
for i in range(len(markupSets)):
	temp_mus = str(markupSets[i])
	clean_mus = temp_mus.strip()
	target_markup_set.append(clean_mus)

print(target_markup_set)
# GUI Window to get User input.

jp = JOptionPane()
f = JFrame()
selectedFile = jp.showInputDialog(f, 'Enter the full absolute file path of the redaction tracker.')

params = []

with open(selectedFile, 'r') as f:
	csvreader = csv.reader(f,delimiter='|')
	next(f)
	for line in csvreader:
		docID = str(line[0])
		GUID = str(line[1])
		selectedPages = str(line[2])
		redaction_type = str(line[3]).strip()
		print("++++++++ CSV ++++++++")
		print("DocID: " + docID)
		print("GUID: " + GUID)
		print("Pages: " + selectedPages)
		print("Redaction Type: " + redaction_type)
		print(" =============== Markup ==============")
		
		if redaction_type in target_markup_set:
			selected_markup_set = target_markup_set.index(redaction_type)
			print("Selected Set (CSV): " + str(selected_markup_set))
		else:
			selected_markup_set = 0
			print("Selected Set (Default): " + str(selected_markup_set))

		print("++++++ Query ++++++")
		query = 'guid:'+GUID
		print(query)
		items = current_case.search(query)
		
		if len(items) != 1:
			print("Error with GUID: " + GUID)
			exit()
		else:
			pages = ''
			if selectedPages:
				pages = [int(x) for x in selectedPages.split(',')]
				print("Pages: " + str(pages))
			printedPages = items[0].getPrintedImage().getPages()
			
			if printedPages == None:
				print("Error: " + docID + " has no Images")
			else:
				for i in range(len(printedPages)):
					print(printedPages[i])
					if pages:
						if i not in pages:
							printedPages[i].createRedaction(redaction_type, 0, 0, printedPages[i].getPageWidth(), printedPages[i].getPageHeight())
						else:
							printedPages[i].createRedaction(selected_markup_set, 0, 0, printedPages[i].getPageWidth(), printedPages[i].getPageHeight())
