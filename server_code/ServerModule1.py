import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import numpy as np
import pandas as pd
import anvil.media
from datetime import datetime, time , date , timedelta
from .pick_calc import set_pick

@anvil.server.callable
def get_datetime():
  return datetime.now()



@anvil.server.callable
def delete_change_note(change_note):
  # check that the article being deleted exists in the Data Table
  if app_tables.change_notes.has_row(change_note):
      change_note.delete()
  else:
      raise Exception("Change Note does not exist")


@anvil.server.callable
def find_dups_back():
  """Launch a single crawler background task."""
  task = anvil.server.launch_background_task('find_dups')
  print(task.get_state())

  # Is the task complete yet?
  if task.is_completed():
    return task
  

@anvil.server.background_task
def find_dups():
    t = app_tables.change_notes.search()
    for row in t:
       print(row['change_note_id'])
       dups = app_tables.change_notes.search(change_note_id = row['change_note_id'])
       if len(dups) > 1:
           print('Duplicate=',row['change_note_id']) 
          
@anvil.server.callable
def add_change(new_change):
  
  change_note_id = (new_change['product_area'] + ' ' + str( new_change['change_date']) + ' '+ new_change['user']  )
  app_tables.change_notes.add_row(
#     created=datetime.now(),
    change_note_id = change_note_id, **new_change
  )
@anvil.server.callable
def get_changes(): 
    today = datetime.today()
    print(today)
    last_90_days = today - timedelta(days =900)
    print(last_90_days)
    results = app_tables.change_notes.search(stage = 'Submitted', change_date = q.greater_than_or_equal_to(last_90_days) )
    return results

@anvil.server.callable
def add_functions():
  functions = list({(r['function']) for r in  app_tables.change_notes.search(tables.order_by('function'))})
  for d in functions:
     app_tables.functions.add_row(function = d)

@anvil.server.callable
def load_data(file):
  """Launch a single crawler background task."""
  task = anvil.server.launch_background_task('store_data', file)
  print(task.get_state())
  
@anvil.server.callable
def reload_data(file):
  """Launch a single crawler background task."""
  task = anvil.server.launch_background_task('restore_data', file)
  print(task.get_state())
  
@anvil.server.background_task
@anvil.server.callable
def restore_data(file):
  with anvil.media.TempFile(file) as file_name:
#     if file.content_type == 'text/csv':
      df2 = pd.read_excel(file_name)
  for d in df2.to_dict(orient="records"):
      df2['difficulty'] = df2['difficulty'].fillna(0).astype(np.int64)
      df2['payoff'] = df2['payoff'].fillna(0).astype(np.int64)
      df2['ips'] = df2['ips'].fillna(0).astype(np.int64)
      df2['severity'] = df2['severity'].fillna(0).astype(np.int64)
      df2['visibility'] = df2['visibility'].fillna(0).astype(np.int64)
      df2['probability'] = df2['probability'].fillna(0).astype(np.int64)
      df2['rpn'] = df2['rpn'].fillna(0).astype(np.int64)
#       df2['Number'] = df2['Number'].fillna(0).astype(np.int64)
      df2['progress'] = df2['progress'].fillna(0).astype(np.int64)
      df2['change_note_id'] = df2['change_note_id'].astype(str)
      df2['found_in_version_no'] = df2['found_in_version_no'].astype(str)
      df2['found_in_last_two_years'] = df2['found_in_last_two_years'].astype(str)
      df2['released_in_version'] = df2['released_in_version'].astype(str)

      df2 = df2.replace(np.nan,'',regex=True)
      # d is now a dict of {columnname -> value} for this row
      # We use Python's **kwargs syntax to pass the whole dict as
      # keyword arguments
      # n= n +1
      # print('Change no=', d['change_note_id'], 'Row=',n)
      
      app_tables.change_notes_empty.add_row(**d)
    
@anvil.server.background_task
@anvil.server.callable
def store_data(file):
  with anvil.media.TempFile(file) as file_name:
#     if file.content_type == 'text/csv':
      df2 = pd.read_excel(file_name)
      print(df2)
#       df2['difficulty'] =df2['difficulty'].fillna(1, inplace=True)
#       df2['difficulty'] = df2['difficulty'].astype('int64')
      df2['difficulty'] = df2['difficulty'].fillna(0).astype(np.int64)
      df2['payoff'] = df2['payoff'].fillna(0).astype(np.int64)
      df2['ips'] = df2['ips'].fillna(0).astype(np.int64)
      df2['severity'] = df2['severity'].fillna(0).astype(np.int64)
      df2['visibility'] = df2['visibility'].fillna(0).astype(np.int64)
      df2['probability'] = df2['probability'].fillna(0).astype(np.int64)
      df2['rpn'] = df2['rpn'].fillna(0).astype(np.int64)
#       df2['Number'] = df2['Number'].fillna(0).astype(np.int64)
      df2['progress'] = df2['progress'].fillna(0).astype(np.int64)
      df2['change_note_id'] = df2['change_note_id'].astype(str)
      df2['found_in_version_no'] = df2['found_in_version_no'].astype(str)
      df2['found_in_last_two_years'] = df2['found_in_last_two_years'].astype(str)
      df2['released_in_version'] = df2['released_in_version'].astype(str)

      df2 = df2.replace(np.nan,'',regex=True)

#       df2 = df2.fillna('')
#   df['a':'b']
#       print (df2['change_note_id':'due_date'])
#       print('due_date',df2['due_date'])
#       df2['due_date'] =  pd.to_datetime(df2['due_date'])
#       df2['change_date'] =  pd.to_datetime(df2['change_date'])
#       df2['difficulty1'] =df2['difficulty'].fillna(1, inplace=True)
#       df2['payoff'] = df2['payoff'].fillna(1, inplace=True)
#       df2['severity'] = df2['severity'].fillna(1, inplace=True)
#       df2['rpn'] = df2['rpn'].fillna(1, inplace=True)
#       df2['ips'] = df2['ips'].fillna(1, inplace=True)
#       df2['visibility'] = df2['visibility'].fillna(1, inplace=True)
#       df2['probability'] = df2['probability'].fillna(1, inplace=True)
# #       df2['progress'] = df2['progress'].fillna(0, inplace=True)
#       df2['change_note_id'] = df2['change_note_id'].astype(str)
#     else:
#       df = pd.read_excel(file_name)
      print(df2)
  n = 0
  for d in df2.to_dict(orient="records"):
      print('syd')
      # d is now a dict of {columnname -> value} for this row
      # We use Python's **kwargs syntax to pass the whole dict as
      # keyword arguments
      n= n +1
      print('Change no=', d['change_note_id'], 'Row=',n)
      
      app_tables.change_notes.add_row(**d)
  t = app_tables.change_notes.search()
  for row in t:
    if row['priority'] == 'Low priority':
       row['priority'] = '3. Low Priority'
    if row['priority'] == 'Medium Priority':
       row['priority'] = '2. Medium Priority'
    if row['priority'] == 'High priority':
       row['priority'] = '1. High Priority'
    if not row['user']:
        row['user'] ='unknown@4s-dawn.com'

    if not row['new_change_note_id'] :        
         year =row['change_date'].year
         counter = get_next_value_in_sequence()
         counter = str(counter).zfill(6)
         row['new_change_note_id'] = str(year) + '-' +str(counter)
              
# populate function table
  # app_tables.functions.delete_all_rows()
  functions = list({(r['function']) for r in  app_tables.change_notes.search(tables.order_by('function'))})
  for i in functions:
      
       functionexist = app_tables.functions.get(function = i)
       if not functionexist:
         app_tables.functions.add_row(function = i)


      
@anvil.server.callable
def update_change(change_notes, change_copy, loggedinuser):
  print('change_copy', change_copy)
  change_copy['ips'] = change_copy['difficulty'] * change_copy['payoff']
  change_copy['rpn'] = change_copy['severity']*change_copy['probability']*change_copy['visibility']
#   change_copy['pick'] = set_pick(self)
#   change_dict['pick'] = set_pick(self)
  print('pick in update=', change_copy['pick'])
  if app_tables.change_notes.has_row(change_notes):
    change_notes.update(**change_copy)
    change_copy['user_changed'] = loggedinuser
    change_copy['when_changed'] = datetime.now()
    print('change_copy' ,change_copy)
    app_tables.change_notes_audit.add_row(**change_copy)
  else:
    raise Exception("Change Note does not exist")
    
def set_pick(change_copy):
  if  change_copy['difficulty'] >= 5 and change_copy['payoff'] > 5:
    change_copy['pick'] = "1. Implement"
  elif  self.difficulty_textbox.text <  5 and change_copy['difficulty'] >= 1 and change_copy['payoff'] >= 5:
    schange_copy['pick']  = "2. Challenge"
  elif self.difficulty_textbox.text >=5 and change_copy['payoff']  < 5 and change_copy['payoff']  >= 1:
    change_copy['pick']  ="3. Possible"
  elif change_copy['difficulty'] <  5 and change_copy['payoff'] >= 1  and  change_copy['payoff'] < 5 and change_copy['payoff'] >= 1:
    schange_copy['pick']  = "4. Kill"
  elif change_copy['difficulty'] is None or change_copy['payoff'] is None:
    change_copy['pick']  =  "5 Not Defined."
  return  change_copy

@anvil.server.callable
def change_id_number():
        datetoday = datetime.now()
        year = datetoday.year 
        print('Year=', year)
        # self.change_id_textbox.text = year
        
        counter = get_next_value_in_sequence()
        print('Counter in Chage_id=',counter)
        counter = str(counter).zfill(6) 
        return year, counter

@tables.in_transaction
def get_next_value_in_sequence():
  row = app_tables.change_id_counter.get()
  row['counter'] = row['counter'] + 1
  print('counter in transaction=', row['counter'])
  return row['counter']

@anvil.server.callable
def text_search_changes(query):
  query = query.lower()
  print (query)
  return [r for r in app_tables.change_notes.search()
            if query in r['title'].lower() or query in r['description'].lower()]
  