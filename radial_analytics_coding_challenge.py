import csv
import math


#function should calculate the percentage of hospitals in the given county that are private non profits
#by cycling through the hospitals of the county and taking the total number of private non profits
#over the total number of hospitals
def pct_private_non_profit(list_of_county_hospitals):
	total_hospitals = 0
	hospitals_non_profit = 0
	percetage_non_profit = 0.0
	for row in list_of_county_hospitals:
		if row[9] == 'Voluntary non-profit - Private':
			hospitals_non_profit += 1
		total_hospitals += 1
	if total_hospitals == 0:
		return 0
	percetage_non_profit = float(hospitals_non_profit) / float(total_hospitals)
	percetage_non_profit = percetage_non_profit*100
	percetage_non_profit = round(percetage_non_profit,2)
	return percetage_non_profit


#function should calculate number of acute care hospitals in the given county
def num_acute_care(list_of_county_hospitals):
	hospitals_acute_care = 0
	for row in list_of_county_hospitals:
		if row[8] == 'Acute Care Hospitals':
			hospitals_acute_care += 1
	return hospitals_acute_care


#function should calculate the average rating of acute care hospitals in the given county (mean) by 
#cycling through all of the hospitals of the county and averaging all of the acute care hospitals'
#when the rating is not set to "not available"
def avg_acute_care_rating(list_of_county_hospitals):
	hospitals_acute_care = 0
	total_acute_care_rating = 0
	avg_rating = 0
	for row in list_of_county_hospitals:
		if row[8] == 'Acute Care Hospitals' and row[12] != 'Not Available':
			hospitals_acute_care += 1
			total_acute_care_rating = total_acute_care_rating + int(row[12])
	if hospitals_acute_care == 0:
		return 0
	avg_rating =  float(total_acute_care_rating) / float(hospitals_acute_care)
	return round(avg_rating, 3)


#function should calculate the median rating of acute care hospitals in the given county by cycling through
#the hospitals in the county and saving all of the acute care hospitals with a rating and then finding the 
#middle index and returning its value
def median_acute_care_rating(list_of_county_hospitals):
	acute_care_hospitals_in_county = []
	acute_care_hospital_counter = 0
	median_cell = 0
	median_value = 0

	for row in list_of_county_hospitals:
		if row[8] == 'Acute Care Hospitals' and row[12] != 'Not Available':
			acute_care_hospitals_in_county.append(row[12])
			acute_care_hospital_counter += 1

	if acute_care_hospital_counter == 0:
		return 0

	acute_care_hospitals_in_county_sorted = sorted(acute_care_hospitals_in_county, key=lambda row: row[0], reverse=False)

	if len(acute_care_hospitals_in_county_sorted) % 2 == 1:
		median_cell = len(acute_care_hospitals_in_county_sorted) / 2
		median_value = acute_care_hospitals_in_county_sorted[median_cell]
		return float(median_value)
	else: 
		median_cell = len(acute_care_hospitals_in_county_sorted) / 2
		median_value = int(acute_care_hospitals_in_county_sorted[median_cell]) + int(acute_care_hospitals_in_county_sorted[median_cell - 1])
		return float(median_value) / 2


#this function should return the correlation between the hospital's overall rating and the mortality and readmission rates
#of the hospital
#though a general correlation function could have been used in order to reduce the amount of written code, I chose against 
#it because I felt that it would be more arduous to make new structures to hold the values of the hospitals before sending them
#out to be tested
def hospital_overall_rating_sucess(list_of_hospitals):
	mean_overall_rating = 0
	mean_mortality_and_readmission = 0
	total_overall_rating = 0
	total_mortality_and_readmission = 0

	x_minus_xbar = 0
	y_minus_ybar = 0
	x_minus_xbar_squared_sum = 0
	y_minus_ybar_squared_sum = 0
	sum_for_top_of_correlation = 0
	sum_of_bottom_of_correlation = 0
	correlation = 0


	for row in list_of_hospitals:
		total_overall_rating = total_overall_rating + row[1]
		total_mortality_and_readmission = total_mortality_and_readmission + row[2]

	mean_overall_rating = float(total_overall_rating) / float(len(list_of_hospitals))
	mean_mortality_and_readmission = float(total_mortality_and_readmission) / float(len(list_of_hospitals))

	for row in list_of_hospitals:
		x_minus_xbar = float(row[1]) - mean_overall_rating
		y_minus_ybar = float(row[2]) - mean_mortality_and_readmission
		sum_for_top_of_correlation = sum_for_top_of_correlation + x_minus_xbar*y_minus_ybar
		x_minus_xbar_squared_sum = x_minus_xbar_squared_sum + pow(x_minus_xbar,2)
		y_minus_ybar_squared_sum = y_minus_ybar_squared_sum + pow(y_minus_ybar,2)

	sum_of_bottom_of_correlation = math.sqrt(x_minus_xbar_squared_sum*y_minus_ybar_squared_sum)
	correlation = sum_for_top_of_correlation/sum_of_bottom_of_correlation
	return correlation



#import the csv file and create a reader for it before sorting it by the county name
referenceToCSV = open('Hospital General Information.csv') 
csvReader = csv.reader(referenceToCSV)
sortedList = sorted(csvReader, key=lambda row: row[6], reverse=False)

#create a list to hold all of the hospitals' data as well as lists to hold the csv data and current county data
hosipitalList = []
hospitals_by_county = []
current_county_list = []

#create variables to hold all of the upcoming values for the results of the coding challenge 
county_state = ''
prev_county_state = ''
counter = -1
private_non_profit_percentage = 0
acute_care = 0
mean_acute_care = 0
median_acute_care = 0

#add a first row which holds the names of the csv collumns
hospitals_by_county.append(['county_state', 'num_hospitals', 'pct_private_non_profit', 'num_acute_care_hospitals', 'avg_acute_care_rating', 'median_acute_care_rating'])

#run through the sorted list and get the values for all of the csv collumns
#in the case that the county and state have been seen already simply add the instance
#to the current country list and increase the value of the counter
#in the case that the code has reached a new country the algorithm should find all of the csv
#collumn values and add them to final list before resetting the variables and starting the 
#new county
for row in sortedList:
	if row[6] != '':		#this should remove all of the hospitals which do not have a county
		county_state = row[6] + ', ' + row[4]
		if county_state != prev_county_state:
			private_non_profit_percentage = pct_private_non_profit(current_county_list)
			acute_care = num_acute_care(current_county_list)
			mean_acute_care = avg_acute_care_rating(current_county_list)
			median_acute_care = median_acute_care_rating(current_county_list)
			hospitals_by_county.append([prev_county_state, counter, private_non_profit_percentage, acute_care, mean_acute_care, median_acute_care])
			current_county_list[:] = []
			current_county_list.append(row)
			counter = 1
			prev_county_state = county_state
		else:
			current_county_list.append(row)
			counter += 1
		

#create variables for extra credit portion
hospital_name = ''
hospital_overall_rating = 0
mortality_national_comparison = 0
readmission_national_comparison = 0
mortality_and_readmission_comparrison = 0
extra_collumns_removed_list = []
correlation_overall_rating_mortality_and_readmission = 0


#reduce the information to only that which is necesary for the extra credit portion
#only the hospital name, the hospital overall rating, the mortality and readmission ratings are necesary
#I took the value of below average to be -1 average to be 0 and above average to be 1
#then I summed the readmission and mortality rates and added three to them to put the total
# on a 1 to 5 scale like the overall rating
#I then sent it out to check the correlation of the two sets
for row in sortedList:
	if row[12] != 'Not Available' and row[12] != 'Hospital overall rating' and row[14] != 'Not Available' and row[18] != 'Not Available':
		hospital_name = row[2]
		hospital_overall_rating = int(row[12])
		if row[14] == 'Below the national average':
			mortality_national_comparison = -1
		elif row[14] == 'Same as the national average':
			mortality_national_comparison = 0
		else:
			mortality_national_comparison = 1
		if row[18] == 'Below the national average':
			readmission_national_comparison = -1
		elif row[18] == 'Same as the national average':
			readmission_national_comparison = 0
		else:
			readmission_national_comparison = 1
		mortality_and_readmission_comparrison = mortality_national_comparison + readmission_national_comparison + 3
		extra_collumns_removed_list.append([hospital_name, hospital_overall_rating, mortality_and_readmission_comparrison])

correlation_overall_rating_mortality_and_readmission = hospital_overall_rating_sucess(extra_collumns_removed_list)


print correlation_overall_rating_mortality_and_readmission



#delete ehrrant row from the list
del hospitals_by_county[1]

#sort the list by number of hospitals descending
hospitals_by_county = sorted(hospitals_by_county, key=lambda row: row[1], reverse=True)

#create the csv and store all of the values into it
with open("hospitals_by_county.csv",'wb') as resultFile:
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(hospitals_by_county)
