import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#
def fix_due_date():
    t = app_tables.change_notes.search()
    count = 0
    for row in t:
        # if row['rpn'] == 0 and row['priority'] == '3. Low Priority':
        #     print(row['new_change_note_id'],'due_Date =',row['due_date'],' ', row['priority'],' ', row['rpn'],' ' , row['severity'], ' ' , \
        #      row['probability'], ' ' ,row['visibility']    )
        #     row['rpn'] = 0
        #     row['priority'] = '4. Not Defined'
        #     row['severity'] = 0
        #     row['probability'] = 0
        #     row['visibility'] = 0
        #     row['due_date'] = None
        #     print(row['new_change_note_id'],'due_Date =',row['due_date'],' ', row['priority'],' ', row['rpn'],' ' , row['severity'], ' ' , \
        #      row['probability'], ' ' ,row['visibility']    )
        # if row['priority'] == '2.. Medium Priority':
        #    row['priority'] = '2. Medium Priority'
        
        if  row['type']:
           count = count + 1
           # print(row['change_note_id'])
    print('Count of Type=', count)