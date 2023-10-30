
EXP_E_FAILURE = '/data/cip19ql/rail_psgr_tasmax/data_output/climate/exp_e_fail.txt'
LOG  = '/data/cip19ql/rail_psgr_tasmax/data_output/climate/simulation_log.txt'

    
# Opening the file with append mode
file_exp_e_fail = open(EXP_E_FAILURE, "a")
content = "\n"
file_exp_e_fail.write(content)
file_exp_e_fail.close()


# Opening the file with append mode
file_log= open(LOG, "a")
content = "\n\n# This Content is added through the program #"
file_log.write(content)
file_log.close()