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
    print 'the package is running!!'
    print options
    if options.type_run in ['learn','config']:         #if learning

        if options.test_size in [0,1]:   #if use cross-validation
            if options.n_folds <> 1: #if use k= 1, skip this
                print 'learning with Cross validation'
                time_text = experiment.run_kfold_deepmg(options,args)    
        else: #if set the size of test set, so use holdout validation
            time_text = experiment.run_holdout_deepmg(options,args)    
               
        if options.save_entire_w in ['y'] or options.test_exte in ['y']:        #if get weights on whole dataset  
            if options.n_folds <> 1:
                print 'learning with whole training set, then predict on test set'
                experiment.run_holdout_deepmg(options,args, special_usecase = 'train_test_whole',txt_time_pre=time_text)  
            else: #if use k= 1, training on whole training set, and test on test set
                from time import gmtime, strftime
                time_text = str(strftime("%Y%m%d_%H%M%S", gmtime())) 
                experiment.run_holdout_deepmg(options,args, special_usecase = 'train_test_whole',txt_time_pre=time_text)

    elif options.type_run in ['predict']: #if predict or test from a pretrained model
        experiment.run_holdout_deepmg(options,args, special_usecase = 'predict')   
    else:
        print 'this function you required is not available right now, please contact the author'
