"""
================================================================================

================================================================================
Author: Van-Kha Nguyen
References: deepmg package
====================================================================================================================
"""

from deepmg import experiment
options, args = experiment.para_cmd()

#check if read parameters from configuration file
import os
if options.config_file <> '':
    if os.path.isfile(options.config_file):
        experiment.para_config_file(options)
        #print options
    else:
        print 'config file does not exist!!!'
        exit()
else:
    experiment.get_default_value(options)

#convert options which type numeric
experiment.string_to_numeric(options)
#check whether parameters all valid
experiment.validation_para(options)

  
if __name__ == "__main__":   
    if options.type_run in ['predict']:  #predict based on weights trained
        experiment.run_holdout_deepmg(options,args, special_usecase = 'predict')   
    else:
        print 'the function you required is not available right now, please contact the author!'
