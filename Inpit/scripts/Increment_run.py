# Muk3D script
import json
from muk3d.ui.forms import ask, get_float, get_filename, get_integer, get_directory, get_choice, get_checkbox
from muk3d.ooze import get_tailings_names

with open('base_data.json','rb') as f:
    data = json.load(f)
    run_no = data['run_index']
    

    
with  open('base_data.json','wb') as f:
    data['run_index'] = run_no+1
    json.dump(data, f)
    print 'new run index is ', run_no + 1
    
    