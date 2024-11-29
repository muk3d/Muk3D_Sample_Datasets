# Muk3D script
import json


with open('base_data.json','rb') as f:
    data = json.load(f)
    run_no = data['run_index']
print 'Current run is ', run_no