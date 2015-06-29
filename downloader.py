import sys
import os
import urllib2
import gzip
from selenium import webdriver
import time

def retrieveData(captureUrl, fileName):
	'''

	With these new links, go to the page and 
	download the file.

	'''
	captureUrl = captureUrl + fileName

	data = urllib2.urlopen(captureUrl)

	outputFile = fileName
	print outputFile
	output = open(outputFile,'wb')
	output.write(data.read())
	output.close()
	unzip(outputFile)

def unzip(newGzip):
	inF = gzip.GzipFile(newGzip, 'rb')
	s = inF.read()
	inF.close()
	
	outF = file(newGzip[:-3], 'wb')
	outF.write(s)
	outF.close()

	os.remove(newGzip) # remove .gz file

def start_page():
	''' 
	This opens a new chrome page and enters and captures
	a bunch of links to download.  These links are census
	data from the Longitudinal Employer-Household Dynamics
	database.
	
	Future iterations will include what data to download. Here
	we are only downloading NY State and Residential.  These
	options are hard-coded.
	
	'''

	url = 'http://lehd.ces.census.gov/data'
	captureUrl = 'http://lehd.ces.census.gov/data/lodes/LODES7/ny/rac/'

	try:
		os_path = os.path.dirname(os.path.realpath(__file__))
		chrome_driver_location = os_path + '/chromedriver'
		ch = webdriver.Chrome(chrome_driver_location) # Get local session of firefox
		ch.get(url)
	except:
		print "Could not find the Chrome Driver.  Please download Google Chrome Driver"

	el = ch.find_element_by_id('lodes_version')
	for option in el.find_elements_by_tag_name('option'):
		if option.text == 'LODES7':
			option.click()

	time.sleep(0.2) # Let the page load, will be added to the API

	el = ch.find_element_by_id('lodes_state')
	for option in el.find_elements_by_tag_name('option'):
		if option.text == 'New York':
			option.click()
	time.sleep(0.2) # Let the page load, will be added to the API

	el = ch.find_element_by_id('lodes_type')
	for option in el.find_elements_by_tag_name('option'):
		if option.text == 'Residence Area Characteristics (RAC)':   
			option.click()

	time.sleep(0.2) # Let the page load, will be added to the API

	# Select the submit button
	el.find_elements_by_xpath('//*[@id="lodes_files_load"]')[0].click()

	time.sleep(0.2) # Let the page load, will be added to the API

	link = el.find_elements_by_xpath('//*[@id="lodes_file_list"]/div/div[*]/div[1]/a')

	for i in link:
		retrieveData(captureUrl, i.text)

if __name__ == "__main__":
	start_page()

