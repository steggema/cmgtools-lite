#!/usr/bin/env python

from CMGTools.H2TauTau.proto.samples.component_index import ComponentIndex

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

import imp 
import datetime
import copy

def nfiles_per_job(nevents_per_job, nevents, nfiles):
    nevents_per_file=nevents/nfiles
    nfiles_per_job = nevents_per_job/nevents_per_file
    if nfiles_per_job == 0: 
        nfiles_per_job+=1
    return nfiles_per_job
    
def get_selected_components(pattern_or_fname):
    if os.path.isfile(pattern_or_fname):
        sys.exit(4)
    patterns = pattern_or_fname.split(',')
    selected=[]
    for pattern in patterns:
        selected.extend(index.glob(pattern))
    return selected
    
def load_base_config(fname):
    config = None
    with open(fname) as ifile:
        mod = imp.load_source('mod', fname, ifile)
    config = mod.config
    return config

def create_config(component, options, base_config):
    config = copy.copy(base_config)
    request_name = None
    if options.request_name:
        request_name = options.request_name
    else: 
        request_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    request_name = '_'.join([component.name,request_name])
    config.General.requestName = request_name
    config.Data.inputDataset = component.dataset
    nfiles = len(component.files)
    config.Data.unitsPerJob=nfiles_per_job(options.nevents_per_job,
                                           component.dataset_entries,
                                           nfiles)
    print 'Task:', 
    print '\t', component.dataset
    print '\tfiles/job =', config.Data.unitsPerJob
    print '\tn jobs    =', nfiles/config.Data.unitsPerJob
    if options.verbose: 
         print config
    component.config = config


if __name__ == '__main__':
    import os
    import sys
    import imp
    import pprint
    from optparse import OptionParser
    usage = "usage: %prog [options] pattern"
    parser = OptionParser(usage=usage)

    default_module = os.path.expandvars('$CMSSW_BASE/src/CMGTools/H2TauTau/python/proto/samples/summer16/htt_common.py')
    parser.add_option("-c", "--config", dest="config",
                      default='crabConfig.py',
                      help='base crab configuration file. defaults to crabConfig.py')
    parser.add_option("-m", "--module", dest="module",
                      default=default_module,
                      help='module where the components are defined')
    parser.add_option("-n", "--dry-run", dest="dryrun",
                      action='store_true',
                      default=False,
                      help='set up the jobs and do nothing')
    parser.add_option("-v", "--verbose", dest="verbose",
                      action='store_true',
                      default=False,
                      help='verbose mode')
    parser.add_option("-e", "--nevents_per_job", dest="nevents_per_job",
                      default=20e4,
                      type='int',
                      help='desired approximate number of events per job')
    parser.add_option("-r", "--request_name", dest="request_name",
                      default=None,
                      help='base name for this request. default: <date_time>')
    
    options, args = parser.parse_args()

    if len(args)!=1:
        print parser.usage
        sys.exit(1)
    pattern = args[0]
  
    if options.dryrun:
        print 'Dry run, will do nothing'

    index=ComponentIndex(options.module)
    
    selected_components=get_selected_components(pattern)
    if len(selected_components)==0:
        print 'No dataset matches pattern', pattern
        sys.exit(2)
#    print 'datasets to be submitted:'
#    pprint.pprint(index.glob(pattern))

    base_config = load_base_config(options.config)
    for component in selected_components:
        create_config(component, options, base_config)
        
    if not options.dryrun:
        print 
        answer=None
        while answer not in ['y','n']:
            answer=raw_input('Confirm submission? [y/n]')
        if answer == 'n':
            print 'submission cancelled.'
            sys.exit(3)

    if not options.dryrun:
        for component in selected_components:
            print 'submitting:'
            print component.dataset
            crabCommand('submit', config=component.config)
        
    
