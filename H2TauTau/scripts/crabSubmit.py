#!/usr/bin/env python

from CMGTools.H2TauTau.proto.samples.component_index import ComponentIndex
from CMGTools.RootTools.utils.splitFactor import splitFactor

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

import imp 
import datetime

def create_task(component, options):
    fname = options.config
    config = None
    with open(fname) as ifile:
        mod = imp.load_source('mod', fname, ifile)
    config = mod.config
    request_name = None
    if options.request_name:
        request_name = options.request_name
    else: 
        request_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    request_name = '_'.join([component.name,request_name])
    config.General.requestName = request_name
    config.Data.inputDataset = component.dataset
    split = splitFactor(component, options.nevents_per_job)
    config.Data.unitsPerJob=split
    print config
    import pdb; pdb.set_trace()

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
    parser.add_option("-t", "--test", dest="test",
                      action='store_true',
                      default=False,
                      help='test mode, for development purpose')
    parser.add_option("-e", "--nevents_per_job", dest="nevents_per_job",
                      default=20e4,
                      help='desired approximate number of events per job')
    parser.add_option("-r", "--request_name", dest="request_name",
                      default=None,
                      help='base name for this request. default: <date_time>')
    
    options, args = parser.parse_args()

    if len(args)!=1:
        print parser.usage
        sys.exit(1)
    pattern = args[0]
    if options.test:
        options.dryrun=True
    if options.dryrun:
        print 'Dry run, will do nothing'

    index=ComponentIndex(options.module)
    
    selected_components = index.glob(pattern)
    if len(selected_components)==0:
        print 'No dataset matches pattern', pattern
        sys.exit(2)
    print 'datasets to be submitted:'
    pprint.pprint(index.glob(pattern))
    if not options.dryrun:
        print 
        answer=None
        while answer not in ['y','n']:
            answer=raw_input('Are you sure? [y/n]')

    for component in selected_components:
        create_task(component, options)
