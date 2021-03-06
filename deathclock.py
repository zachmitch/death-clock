#  Death Clock v1.1 by Zach Mitchell 11/23/15
#
# Addition from last version:  Added the ability to choose your country of residence (cor). Data was imported from the Population Division of the United Nations Department of Economic and Social Affairs (UN DESA), released World Population Prospects, The 2010 Revision.  The data in 'life_expectancy.csv' shows the life expectancy at birth for the period 2009 to 2012.
#
# This version assumes that you will live an average lifespan for someone of your sex in your country of residence.  Future versions will take into account lifestyle choices and risk. 
#
# - - - - - - - - - - - - - - - - - - - -

from datetime import date, timedelta
import csv

#- - - - - - -BASIC INPUTS - - - - - -

no = ('no', "n", 'nope')
yes = ('yes', 'y', 'yep', 'yup')

extended_test = raw_input('Do you want to take the extended test? Y or N: ')


# DATE OF BIRTH

print "Please enter your birthday: "
y = int(raw_input("\nYear (ex: 1988, 1939, 2004): "))
m = int(raw_input("\nMonth (ex: 1 - Jan, 2 - Feb, etc...): "))
d = int(raw_input("\nDay (ex: 1-31):  "))
now = date.today()
bday = date(y, m, d)

# SEX

m_f = raw_input("\nAre you male(M), female(F), or prefer not to answer(D)? ")

# COUNTRY OF RESIDENCE

life_expect = []
country_list = ['list']

with open('life_expectancy.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		life_expect.append(row)
		country_list.append(row['Country'].lower())
		
cor = raw_input("\nWhat country do you live in?  \nTo see a list of countries, type 'list'. ")
cor = cor.lower()

#IF USER WANTS TO SEE A LIST OF AVAILABLE COUNTRIES

if cor.lower() == 'list':
	for row in life_expect:
		print row['Country']
	cor = raw_input("\nAlrighty, so what country do you live in?  Be sure to spell it correctly. ")

# ERROR HANDLING COUNTRY OF RESIDENCE INPUT

while not(cor.lower() in country_list):
	print "That is not a valid country."
	cor = raw_input("\nWhat country do you live in? type 'list' to see all the countries. ")
	if cor.lower() == 'list':
		for row in life_expect:
			print row['Country']
		cor = raw_input("\nAlrighty, so what country do you live in?  Be sure to spell it correctly. ")


# RETRIEVING LIFE EXPECTANCY FOR COUNTRY OF RESIDENCE 

for row in life_expect:
	country = (row['Country'])
	male = (row['Male'])
	female = (row['Female'])
	overall = (row['Overall'])
	if country.lower() == cor.lower():
		if m_f.lower() == ("m" or 'male'):
			life_expect = float(male) * 365
		elif m_f.lower() == ("f" or 'female'):
			life_expect = float(female) * 365
		else:
			life_expect = float(overall) * 365

			
life_expect = int(life_expect)


# - - - -  - EXTENDED TEST CALCULATIONS - - - - - - - 


# All calculations will affect only the life_expect base variable


#Smoking Cigarettes
#According to NYT article heavy smokers can estimate 10yrs off life expectancy #http://well.blogs.nytimes.com/2013/01/23/putting-a-number-to-smokings-toll/

def cigs(prompt):
	if prompt in no:
		return 0
	elif prompt in yes:
		cigs_heavy = (raw_input("Would you say that you are a heavy smoker?  Do you smoke more than a pack a day? "))
		if cigs_heavy in yes:
			return -3650 
		else:
			cigs_num = int(raw_input("So then, 1-20, how many cigs do you smoke a day? "))
			while cigs_num not in range(1,20):
				cigs_num = int(raw_input("So then, 1-20, how many cigs do you smoke a day? "))
			return cigs_num * -183
			
#Drinking alcohol
#http://www.psmag.com/health-and-behavior/truth-wont-admit-drinking-healthy-87891
#this questionnaire takes the position that low-moderate consumption isn't unhealthy (double negative for impact), but extended binge drinking is.

def alcohol(prompt):
	if prompt in no:
		return -365
	else:
		alcohol_heavy = (raw_input("When you drink, do you binge drink? "))
		if alcohol_heavy in no:
			return 0
		else:
			alcohol_heavy_times = int(raw_input("How many days a week do you binge drink? "))
			return alcohol_heavy_times * -525



life_choices = 0 # number that will +- days to your life based on your behavior
genetics = 0 # number that will +- days to your life based on your genes

if extended_test in yes:
	life_choices =  int(cigs(raw_input("Do you smoke cigarettes? ").lower())) + int(alcohol(raw_input("Do you drink alcohol? ").lower()))
	life_expect = life_expect + life_choices

#- - - - BASIC CALCULATIONS - - - - - - - 

#AGE 

age = now - bday
age = int(age.days)
age_year = (age / 365)
age_month = (age % 365) / 30
age_week = ((age % 365) % 30) / 7
age_day = ((age % 365) % 30) % 7

# TIME LEFT UNTIL DEATH

time_left = life_expect - age
dod = now + timedelta(days=time_left)
death_year = (time_left / 365)
death_month = (time_left % 365) / 30
death_week = ((time_left % 365) % 30) / 7
death_day = ((time_left % 365) % 30) % 7
spacer = 3 * "\n*"

#  DEATH AGE

died_year = (life_expect / 365)
died_month = (life_expect % 365) / 30
died_week = ((life_expect % 365) % 30) / 7
died_day = ((life_expect % 365) % 30) % 7


#- - - - - READOUT TO THE USER - - - - - - - - 


print spacer, "You are", age_year, "years,", age_month, "months,", age_week, "weeks, and", age_day, "days old today.", spacer

print "You should live for about", death_year, "years,", death_month, "months,", death_week, "weeks, and", death_day, "more days after today.", spacer

print "When you die, you will be", died_year, "years,", died_month, "months,", death_week, "weeks, and", death_day, "more days old.", spacer

print "Your expected date of death: ", repr(dod.strftime("%m %d %Y")), spacer