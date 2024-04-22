import os
import re
import json
import random
import pandas as pd
import sqlite3
from datetime import datetime
from .Contexts import *
from .Intents import *
from .generatengrams import ngrammatch
from .views import *

def load_data_from_database(table_name):
    # Connect to SQLite database
    conn = sqlite3.connect('db.sqlite3')
    
    # Execute query to fetch data from table
    query = f"SELECT * FROM '{table_name}'"
    df = pd.read_sql_query(query, conn)
    
    # Close connection
    conn.close()
    
    return df

def load_bikename_from_database(table_name, bs):
    # Connect to SQLite database
    conn = sqlite3.connect('db.sqlite3')
    
    # Execute query to fetch data from table
    query = f"SELECT * FROM '{table_name}' WHERE Bike_station='{bs}' and Bike_availability='Available'"
    df = pd.read_sql_query(query, conn)
    
    # Close connection
    conn.close()
    
    return df

def performAction(intentname, params):
    if intentname == "Book Bike":
        df = load_data_from_database('web_App_bikestation_details')
        print("\n*********All Bikestation Details*************")
        print(df)

        return df


def bike_check_actions(current_intent, attributes, context):
    perform_action_result = performAction(current_intent.action, attributes)
    if perform_action_result is not None:  
        if isinstance(perform_action_result, pd.DataFrame) and not perform_action_result.empty:
            global bike_result_df
            bike_result_df = perform_action_result
            columns_to_drop = ['Sl_no', 'latitude', 'longitude']
            bike_result_df.drop(columns=columns_to_drop, inplace=True)
            column_mapping = {'Bikestation_name': 'Name', 'Bikestation_location': 'Location'}
            bike_result_df.rename(columns=column_mapping, inplace=True)

            column_names = bike_result_df.columns.tolist()
            formatted_column_names = ' | '.join(column_names)

            formatted_rows = '\n'.join(['• ' + ', '.join(map(str, row)) for row in bike_result_df.values])

            result_string = f"<b>{formatted_column_names}:</b>\n--------------------------------\n{formatted_rows}\n--------------------------------\nEnter the Bikestation NAME you want to choose:"

            return result_string, None
        else:
            print("Invalid result returned from performAction function.")
            return None, None
    else:
        print("Your query is Completed. Try Another Options..")
        context = IntentComplete()
        return 'close_chatbot', None

###########this is the portion of shwoing bikes from a bike station
#           selected_bike = bike_df[bike_df['Bike_name'] == choosed_bike_name]

#           if not selected_bike.empty:
#               # Retrieve details of selected bike
#               bike_details = selected_bike.iloc[0].to_dict()

#               if bike_details['Bike_availability'] == 'Available':
#                   # Store bike details in a list
#                   bike_info = [bike_details['Bike_name'], bike_details['Bike_type'], 
#                                bike_details['Bike_price'], bike_details['Bike_availability']]
#                   user_params = [params['Bike_station']]
#                   print("Booking completed!")
#                   return bike_info, user_params,df

def check_required_params(current_intent, attributes, context):
    print('------------------')
    print(current_intent.params)
    print('--------------------')
    for para in current_intent.params:
        if para.required:
            if para.name not in attributes:
                if para.name=='nights':
                    context = validatenights()

                if para.name=='checkin':
                    context = validatecheckindate()

                return random.choice(para.prompts), context

    return None, context

def input_processor(user_input, context, attributes, intent):
    attributes, cleaned_input = getattributes(user_input, context, attributes)
    return attributes, cleaned_input

def loadIntent(path, intent):
    with open(path) as fil:
        dat = json.load(fil)
        print('-----------------------------')
        print(intent)
        print('-----------------------------')
        intent = dat[intent]
        return Intent(intent['intentname'], intent['Parameters'], intent['actions'])

def intentIdentifier(clean_input, context, current_intent):
    clean_input = clean_input.lower()

    scores = ngrammatch(clean_input)
    scores = sorted_by_second = sorted(scores, key=lambda tup: tup[1])

    if current_intent is None:
        return loadIntent('web_App/params/bikeparams_old.cfg', scores[-1][0])
    else:
        return current_intent

def getattributes(uinput, context, attributes):
    if context.name.startswith('IntentComplete'):
        return attributes, uinput
    else:
        files = os.listdir('web_App/entities/')
        entities = {}
        for fil in files:
            if fil != '.ipynb_checkpoints':
                lines = open('web_App/entities/'+fil).readlines()
                for i, line in enumerate(lines):
                    lines[i] = line[:-1]
                entities[fil[:-4]] = '|'.join(lines)

        for entity in entities:
            for i in entities[entity].split('|'):
                if i.lower() in uinput.lower():
                    attributes[entity] = i
        for entity in entities:
            uinput = re.sub(entities[entity], r'$'+entity, uinput, flags=re.IGNORECASE)

        if context.name == 'validatenights' and context.active:
            match = re.search('([1-9]|1[031])$', uinput) 
            if match:
                uinput = re.sub('([1-9]|1[031])$', '$nights', uinput)
                attributes['nights'] = match.group()
                context.active = False

        if context.name == 'validatecheckindate' and context.active:
            regex = '(\d{2})[/.-](\d{2})[/.-](\d{4})$'
            match = re.search(regex, uinput)

            if match:
                try:
                    checkinDate = datetime.strptime(match.group(), "%d/%m/%Y")
                    if checkinDate.date() >  datetime.now().date():
                        uinput = re.sub(regex, '$checkin', uinput)
                        attributes['checkin'] = match.group()
                        context.active = False
                    else:
                        print("Booking Date should be greater than today's date.")
                except ValueError:
                    print("Checkin Date is not in dd/mm/yyyy format")
        return attributes, uinput



class MySession:
    def __init__(self, attributes=None, active_contexts=[FirstGreeting(), IntentComplete()]):
        '''Initialise a default session'''
        self.active_contexts = active_contexts
        self.context = FirstGreeting()
        self.current_intent = None
        self.attributes = {}
        self.flag = 0  # Add a flag attribute to keep track of booking process
        self.var=0

    def update_contexts(self):
        '''Not used yet, but is intended to maintain active contexts'''
        for context in self.active_contexts:
            if context.active:
                context.decrease_lifespan()

    def reply(self, user_input):
        '''Generate response to user input'''
        self.attributes, clean_input = input_processor(user_input, self.context, self.attributes, self.current_intent)
        self.current_intent = intentIdentifier(clean_input, self.context, self.current_intent)

        prompt, self.context = check_required_params(self.current_intent, self.attributes, self.context)

        if prompt is None:
            if self.context.name != 'IntentComplete':
                if self.flag == 0:
                    prompt, dataframe = bike_check_actions(self.current_intent, self.attributes, self.context)
                    self.flag = 1
                else:
                    if self.var == 0:
                        # Assuming user has provided bike station name and we need to show available bikes
                        choosed_bike_station = user_input.strip()  # Get the chosen bike station name
                        self.attributes['bike_station'] = choosed_bike_station
                        bikes_df = load_bikename_from_database('web_App_bike_detail', choosed_bike_station)  # Load bikes for the chosen bike station
                        columns_to_drop = ['Sl_no', 'Bike_station', 'Bike_availability','Bike_type','Bike_image']
                        bikes_df.drop(columns=columns_to_drop, inplace=True)
                        column_mapping = {'Bike_name': 'Name', 'Bike_price': 'Price'}
                        bikes_df.rename(columns=column_mapping, inplace=True)
                        if not bikes_df.empty:

                            column_names = bikes_df.columns.tolist()
                            formatted_column_names = '| '.join(column_names)

                            formatted_rows = '\n'.join(['• ' +', '.join(map(str, row)) for row in bikes_df.values])

                            prompt = f"<b>{formatted_column_names}:</b>\n--------------------------------\n{formatted_rows}\n--------------------------------\nEnter the Bikename you want to book:"

                            self.var = 1
                        else:
                            prompt = "No bikes available in the selected bike station."
                            self.flag = 0  # Reset flag for next interaction
                    else:
                        choosed_bikename = user_input.strip()
                        with open('bike_booking_info.txt', 'w') as f:
                            f.write(f"Bike Name: {choosed_bikename}, Bike Station: {self.attributes.get('bike_station', 'N/A')},Nights: {self.attributes.get('nights', 'N/A')}, Check-in Date: {self.attributes.get('checkin', 'N/A')}\n")
                        
                        # add_to_table(choosed_bikename,{self.attributes.get('bike_station', 'N/A')},{self.attributes.get('checkin', 'N/A')})
                        
                        prompt = "Booked successfully!"
                        self.context = IntentComplete()  # Mark intent as complete after booking

                return {'text': prompt}

        if self.context.name == 'IntentComplete':
            self.reset_session()
            prompt = "Your session has been reset."
            return {'text': prompt}

        return {'text': prompt}




    def reset_session(self):
        '''Reset the session state'''
        self.attributes = {}
        self.context = FirstGreeting()
        self.current_intent = None

