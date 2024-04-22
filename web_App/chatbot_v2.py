from .generatengrams import ngrammatch
from .Contexts import *
import json
from .Intents import *
import random
import os
import re
from datetime import datetime
import pandas as pd
import sqlite3


def load_data_from_database(table_name):
	# Connect to SQLite database
	conn = sqlite3.connect('db.sqlite3')
	
	# Execute query to fetch data from table
	query = f"SELECT * FROM '{table_name}'"
	df = pd.read_sql_query(query, conn)
	
	# Close connection
	conn.close()
	
	return df


def load_bikename_from_database(table_name,bs):
	# Connect to SQLite database
	conn = sqlite3.connect('db.sqlite3')
	
	# Execute query to fetch data from table
	query = f"SELECT * FROM '{table_name}' WHERE Bike_station='{bs}'"
	df = pd.read_sql_query(query, conn)
	
	# Close connection
	conn.close()
	
	return df

def performAction(intentname, params):

	if intentname == "Book Bike":
		df = load_data_from_database('web_App_bikestation_details')
		print("\n*********All Bikestation Details*************")
		print(df)
		
		while True:
			bikestation_name = input('\nRosie: Enter NAME of the Bikestation you want to choose: ')
			bike_df = load_bikename_from_database('web_App_bike_detail', bikestation_name)
			
			if not bike_df.empty:
				print("\n*********Bike Names at the Chosen Bikestation*************")
				print(bike_df)
				
				while True:
					# Ask user to select a bike name
					selected_bike_name = input('\nRosie: Enter NAME of the Bike you want to book: ')
					selected_bike = bike_df[bike_df['Bike_name'] == selected_bike_name]

					if not selected_bike.empty:
						# Retrieve details of selected bike
						bike_details = selected_bike.iloc[0].to_dict()

						if bike_details['Bike_availability'] == 'Available':
							# Store bike details in a list
							bike_info = [bike_details['Bike_name'], bike_details['Bike_type'], 
										 bike_details['Bike_price'], bike_details['Bike_availability']]
							user_params = [params['Bike_station']]
							print("Booking completed!")
							return bike_info, user_params,df
						else:
							print('Rosie: Sorry, the selected bike is not available for booking. Choose another one.')
					else:
						print("Sorry, the specified bike was not found.")

					# Ask if the user wants to book another bike
					choice = input("Rosie: Would you like to book another bike? (yes/no): ")
					if choice.lower() != 'yes':
						break

				print("Thank you for using our service!")
				return None, None
			else:
				print("Sorry, no bikestation found at the chosen bike station. Please enter the correct bike station name.")



	elif intentname == "Book Homestay":
		df = load_data_from_database('web_App_homestay_details')
		print("\n*********All Homestay Details*************")
		print(df)
		print("*********END*************")
		locationcondition = df['House_location'].str.lower() == params['House_location'].lower()
		hotelclasscondition = df['House_type'].str.lower() == params['House_type'].lower()

		df_filtered  = df[locationcondition & hotelclasscondition] #roomtariffplancondition &
		if not df_filtered.empty:
			print("\n\n")
			print("--------Matched List----------")
			print(df_filtered)
			
			while True:
				homestay_name = input('\nRosie: Enter NAME of the Homestay you want to book: ')
				selected_homestay = df_filtered[df_filtered['House_name'] == homestay_name]

				if not selected_homestay.empty:
					# Retrieve details of selected homestay
					homestay_details = selected_homestay.iloc[0].to_dict()

					# Store homestay details in a list
					homestay_info = [homestay_details['House_name'], homestay_details['House_location'], 
									 homestay_details['House_type'], homestay_details['House_price'], homestay_details['House_Phone']]

					# Store user-entered parameters in a list
					user_params = [params['House_location'], params['House_type'], params['nights'], params['checkin']]

					print("Booking completed!")
					return homestay_info, user_params,df
				else:
					print("Sorry, the specified homestay was not found.")

				# Ask if the user wants to book another homestay
				choice = input("Rosie: Would you like to book another homestay? (yes/no): ")
				if choice.lower() != 'yes':
					break

			print("Thank you for using our service!")
			return None, None
		else:
			print("Sorry, no homestays found with the given information. Please try again.")

def check_actions(current_intent, attributes, context):
	'''This function performs the action for the intent
	as mentioned in the intent config file'''
	'''Performs actions pertaining to current intent
	for action in current_intent.actions:
		if action.contexts_satisfied(active_contexts):
			return perform_action()
	'''
	perform_action_result = performAction(current_intent.action, attributes)
	if perform_action_result:
		homestay_info, user_params = perform_action_result
		print("Homestay Details:", homestay_info)
		print("User Parameters:", user_params)
		print("Booking completed!")
		return 'close_chatbot',None  
	else:
		print("Your query is Completed. Try Another Options..")
	context = IntentComplete()
	return 'close_chatbot',None  
	# return 'action: ' + current_intent.action, context

def check_required_params(current_intent, attributes, context):
	'''Collects attributes pertaining to the current intent'''

	for para in current_intent.params:
		if para.required:
			if para.name not in attributes:
				#Example of where the context is born, implemented in Contexts.py
				if para.name=='nights':
					context = validatenights()

				if para.name=='checkin':
					context = validatecheckindate()

				#returning a random prompt frmo available choices.
				return random.choice(para.prompts), context

	return None, context


def input_processor(user_input, context, attributes, intent):
	'''Spellcheck and entity extraction functions go here'''

	#uinput = TextBlob(user_input).correct().string

	#update the attributes, abstract over the entities in user input
	attributes, cleaned_input = getattributes(user_input, context, attributes)

	return attributes, cleaned_input

def loadIntent(path, intent):
	with open(path) as fil:
		dat = json.load(fil)
		intent = dat[intent]
		return Intent(intent['intentname'],intent['Parameters'], intent['actions'])

def intentIdentifier(clean_input, context,current_intent):
	clean_input = clean_input.lower()

	#Scoring Algorithm, can be changed.
	scores = ngrammatch(clean_input)

	#print(classname,score)
	#choosing here the intent with the highest score
	scores = sorted_by_second = sorted(scores, key=lambda tup: tup[1])
	# print clean_input
	#print 'scores', scores

	#print ("Score:", scores)
	if(current_intent==None):
		return loadIntent('web_App/params/newparams.cfg',scores[-1][0])
	else:
		#If current intent is not none, stick with the ongoing intent
		return current_intent

def getattributes(uinput,context,attributes):
	'''This function marks the entities in user input, and updates
	the attributes dictionary'''
	#Can use context to context specific attribute fetching
	if context.name.startswith('IntentComplete'):
		return attributes, uinput
	else:
		#Code can be optimised here, loading the same files each time suboptimal
		files = os.listdir('web_App/entities/')
		entities = {}
		for fil in files:
			if (fil != '.ipynb_checkpoints'):
				lines = open('web_App/entities/'+fil).readlines()
				for i, line in enumerate(lines):
					lines[i] = line[:-1]
				entities[fil[:-4]] = '|'.join(lines)

		#Extract entity and update it in attributes dict
		for entity in entities:
			for i in entities[entity].split('|'):
				if i.lower() in uinput.lower():
					attributes[entity] = i
		for entity in entities:
				uinput = re.sub(entities[entity],r'$'+entity,uinput,flags=re.IGNORECASE)

		#Example of where the context is being used to do conditional branching.
		if context.name=='validatenights' and context.active:
			match = re.search('([1-9]|1[031])$', uinput) #Validate nights for max 31 nights
			if match:
				uinput = re.sub('([1-9]|1[031])$', '$nights', uinput)
				attributes['nights'] = match.group()
				context.active = False

		if context.name=='validatecheckindate' and context.active:
			regex = '(\d{2})[/.-](\d{2})[/.-](\d{4})$'
			match = re.search(regex, uinput)

			if match:
				try:
					checkinDate = datetime.strptime(match.group(), "%d/%m/%Y")
					if (checkinDate.date() >  datetime.now().date()):
						uinput = re.sub(regex, '$checkin', uinput)
						attributes['checkin'] = match.group()
						context.active = False
					else:
						print("Booking Date should be greater than today's date.")
				except ValueError:
						print("Checkin Date is not in dd/mm/yyyy format")
		return attributes, uinput

class Session_:
	def __init__(self, attributes=None, active_contexts=[FirstGreeting(), IntentComplete() ]):

		'''Initialise a default session'''

		#Active contexts not used yet, can use it to have multiple contexts
		self.active_contexts = active_contexts

		#Contexts are flags which control dialogue flow, see Contexts.py
		self.context = FirstGreeting()

		#Intent tracks the current state of dialogue
		#self.current_intent = First_Greeting()
		self.current_intent = None

		#attributes hold the information collected over the conversation
		self.attributes = {}

	def update_contexts(self):
		'''Not used yet, but is intended to maintain active contexts'''
		for context in self.active_contexts:
			if context.active:
				context.decrease_lifespan()

	def reply(self, user_input):
		'''Generate response to user input'''

		self.attributes, clean_input = input_processor(user_input, self.context, self.attributes, self.current_intent)
		#print(self.attributes, clean_input )
		self.current_intent = intentIdentifier(clean_input, self.context, self.current_intent)

		prompt, self.context = check_required_params(self.current_intent, self.attributes, self.context)

		#prompt being None means all parameters satisfied, perform the intent action
		if prompt is None:
			if self.context.name!='IntentComplete':
				prompt, dataframe = check_actions(self.current_intent, self.attributes, self.context)
				if dataframe:
					return {'text': prompt, 'df': dataframe}
				else:
					print("11111111111111111111111111111111111111111111111111111111")
					print(prompt)
					return {'text': prompt}

		#Resets the state after the Intent is complete
		if self.context.name=='IntentComplete':
			self.attributes = {}
			self.context = FirstGreeting()
			self.current_intent = None

		print("222222222222222222222222222222222")
		print(prompt)
		return {'text': prompt}
