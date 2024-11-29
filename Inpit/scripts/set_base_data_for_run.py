# Muk3D script
import json
from muk3d.ui.forms import ask, get_float, get_filename, get_integer, get_directory, get_choice
from muk3d.ooze import get_tailings_names

result = ask(fields=[
                    get_filename("Base grid", filters=['*.mgrid',], select_existing_file=True),
                    get_filename("Reclaim path", filters=['*.mcurve',],  select_existing_file=True),
                    get_choice('Tailings properties', get_tailings_names())
                    ],
                    last_values_key='inpit-set base data'
                    )
                    
if result is None:
    end() 
    
with open('base_data.json','wb') as f:
    data = {'base_grid': result["Base grid"],
                'reclaim_path': result["Reclaim path"],
                'run_index': 1,
                'tailings': result['Tailings properties']
                }
                
    json.dump(data, f)
    print 'Set the base data'
    