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



def load_data_from_database(table_name):
    # Connect to SQLite database
    conn = sqlite3.connect('db.sqlite3')
    
    # Execute query to fetch data from table
    query = f"SELECT * FROM '{table_name}'"
    df = pd.read_sql_query(query, conn)
    
    # Close connection
    conn.close()
    
    return df


def performAction(intentname, params):

    if intentname == "Book Homestay":
        df = load_data_from_database('web_App_homestay_details')
        print("\n*********All Homestay Details*************")
        print(df)
        print("*********END*************")
        locationcondition = df['House_location'].str.lower() == params['House_location'].lower()
        hotelclasscondition = df['House_type'].str.lower() == params['House_type'].lower()

        df_filtered = df[locationcondition & hotelclasscondition] 

        if not df_filtered.empty:
            print("\n\n")
            print("--------Matched List----------")
            print(df_filtered)
            
        else:
            print("Sorry, no homestays found with the given information. Please try again.")

        return df_filtered



def check_actions(current_intent, attributes, context):
    perform_action_result = performAction(current_intent.action, attributes)
    if perform_action_result is not None:  
        if isinstance(perform_action_result, pd.DataFrame) and not perform_action_result.empty:
            result_df = perform_action_result
            # columns_to_drop = ['Sl_no', 'House_type', 'House_location']
            # result_df.drop(columns=columns_to_drop, inplace=True)

            column_names = result_df.columns.tolist()
            formatted_column_names = ', '.join(column_names)

            formatted_rows = '\n'.join([', '.join(map(str, row)) for row in result_df.values])

            result_string = f"Available Homestays Details\n\n{formatted_column_names}\n{formatted_rows}\nEnter the Homestay NAME you want to book:"

            return result_string, None
        else:
            print("Invalid result returned from performAction function.")
            return None, None
    else:
        print("Your query is Completed. Try Another Options..")
        context = IntentComplete()
        return 'close_chatbot', None

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
        intent = dat[intent]
        return Intent(intent['intentname'], intent['Parameters'], intent['actions'])

def intentIdentifier(clean_input, context, current_intent):
    clean_input = clean_input.lower()

    scores = ngrammatch(clean_input)
    scores = sorted_by_second = sorted(scores, key=lambda tup: tup[1])

    if current_intent is None:
        return loadIntent('web_App/params/newparams_old.cfg', scores[-1][0])
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

flag = 0

class Session_:
    def __init__(self, attributes=None, active_contexts=[FirstGreeting(), IntentComplete()]):
        '''Initialise a default session'''
        self.active_contexts = active_contexts
        self.context = FirstGreeting()
        self.current_intent = None
        self.attributes = {}
        self.booking_info = {}

    def update_contexts(self):
        '''Not used yet, but is intended to maintain active contexts'''
        for context in self.active_contexts:
            if context.active:
                context.decrease_lifespan()

    def reply(self, user_input):
        '''Generate response to user input'''
        global flag
        self.attributes, clean_input = input_processor(user_input, self.context, self.attributes, self.current_intent)
        self.current_intent = intentIdentifier(clean_input, self.context, self.current_intent)

        prompt, self.context = check_required_params(self.current_intent, self.attributes, self.context)

        print(user_input)
        print('***************')

        
        if prompt is None:
            if self.context.name != 'IntentComplete':
                if flag == 0:
                    prompt, dataframe = check_actions(self.current_intent, self.attributes, self.context)
                    flag = 1
                else:
                    self.booking_info['homestay_name'] = user_input 
                    self.booking_info['nights'] = self.attributes['nights']  # Store number of nights
                    self.booking_info['checkin'] = self.attributes['checkin'] 
                    # Assuming booking is completed successfully here
                    self.reset_session()
                    prompt = "Booking completed! Your session has been reset."
                    flag = 0
                    with open('homestay_booking_info.txt', 'w') as f:
                        f.write(f"Homestay Name: {self.booking_info['homestay_name']},Number of Nights: {self.booking_info.get('nights', 'N/A')},Check-in Date: {self.booking_info.get('checkin', 'N/A')}\n")

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
