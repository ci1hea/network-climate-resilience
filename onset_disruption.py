'''
    sample and calculate the scale of onset disruotion 
    for clmate-based, random and targeted failure scenarios 
'''

# Standard library imports
import csv
import numpy as np
import pandas as pd
import h5py
import pickle
import time

# Local application/library specific imports


# Constants 
N=1000
df_e = pd.read_pickle('/data/cip19ql/rail_psgr_tasmax/data_input/edge_nc_cells.pkl')
s_journeys = pd.read_pickle('/data/cip19ql/rail_psgr_tasmax/data_input/s_journeys.pkl')
sort_j_idx = df_e.sort_values(by='journeys', ascending=False, na_position='last').index.tolist()
NO_edges = df_e.shape[0]
# Input filenames and directory names.

with open('/data/cip19ql/rail_psgr_tasmax/data_input/dependent_od.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    E_i_dependent_od= list(csv_reader)


exp_file = open('/data/cip19ql/rail_psgr_tasmax/data_output/climate/exp_e_fail_pre_cal.txt', 'r')
lines = exp_file.readlines()
list_of_files = [item.split(', ')[0] for item in lines]

input_folder = '/data/cip19ql/rail_psgr_tasmax/data_output/climate/curves/'

# Output filenames
output_folder = '/data/cip19ql/rail_psgr_tasmax/data_output/onset_disruption/'

####################
# DEFINE FUNCTIONS #
####################
def calculate_service_disruption(fail_e_idx): 
    dependent_od = [E_i_dependent_od[idx] for idx in fail_e_idx]
    flat_od_list = list(set([int(item) for sublist in dependent_od for item in sublist]))
    service_down = 100 * s_journeys[flat_od_list].sum() / s_journeys.sum()
    return service_down


#input: filename, N (numbe rof random sample)
#return: [filename,sum(p_fail), climate_, random_, targeted_]
def onset_disruption_all(filename, N):

    filepath = input_folder + filename +'.hdf5'
    f = h5py.File(filepath,'r')
    p_fail = np.array(f['p_fail'])
    exp_e_fail_ = sum(p_fail)
    
    # Climate-based failure scenarios 
    climate_ = []
    N_sample_c =N_sample_c =[(np.random.uniform(size=N) < p) * 1 for p in p_fail]
    #0-functioning, 1-fail
    for i in range(N):
        a_scenario = np.array([item[i] for item in N_sample_c])
        fail_e_idx = np.where(a_scenario==1)[0]
        service_down = calculate_service_disruption(fail_e_idx)
        climate_.append(service_down)
        
    
    # random failure scenarios 
    random_ = []
    p_fail_uniform = [exp_e_fail_/NO_edges]*NO_edges
    N_sample_r = [(np.random.uniform(size=N) < p) * 1 for p in p_fail_uniform] 
    #0-functioning, 1-fail
    for i in range(N):
        a_scenario=np.array([item[i] for item in N_sample_r])
        fail_e_idx = np.where(a_scenario==1)[0]
        service_down = calculate_service_disruption(fail_e_idx)
        random_.append(service_down)
        
        
    # targeted failure scenarios
    targeted_ = []
    for i in range(N):
        a_scenario=np.array([item[i] for item in N_sample_r])
        NO_removal = sum(a_scenario)
        
        the_scenario = np.zeros(NO_edges)
        the_scenario[sort_j_idx[:NO_removal]]=1
        fail_e_idx = np.where(the_scenario==1)[0]
        service_down = calculate_service_disruption(fail_e_idx)
        targeted_.append(service_down)    
    
    
    results = [filename, exp_e_fail_, climate_, random_, targeted_]
    
    
    
    return results

################
#     Main     # . 
################

for filename in list_of_files[:5]:
    t0=time.time()
    result = onset_disruption_all(filename, N)
    output_file_path = output_folder + filename +'.pkl'
    t1 = time.time()
    
    with open(output_file_path, 'wb') as f:
        pickle.dump(result,f)
        
    print("{}, {}".format(filename, (t1-t0)/60))
    '''
    with open(output_file, 'a') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        # writing a single row 
        csvwriter.writerow(result)
    '''
    