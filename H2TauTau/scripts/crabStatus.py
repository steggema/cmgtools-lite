#!/usr/bin/env python


from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException
import pprint 

def get_options():
    import os
    import sys
    from optparse import OptionParser
    usage = "usage: %prog [options] <crab_config_dir>"
    parser = OptionParser(usage=usage)
    parser.add_option("-e", "--error-code", dest="error_code",
                      default=None,
                      type = 'int',
                      help='get status of jobs with this error code')
 
    (options,args) = parser.parse_args()
    if len(args)!=1:
        print parser.usage
        sys.exit(1)
    return options, args


def filter_by_error_code(result, error_code):
    jobs = result['jobs']
    filtered = dict()
    for jobid,job in jobs.iteritems(): 
        error = job.get('Error')
        if error and (error[0]==error_code or error_code is None): 
            filtered[jobid]=job
    return filtered

def print_jobs(jobs): 
    pprint.pprint(jobs)

def print_job_ids(jobs):
    ids = jobs.keys()
    print len(ids), 'selected jobs'
    print ','.join(ids)

def print_one(jobs):
    print 'this is one of your jobs:'
    pprint.pprint(jobs.itervalues().next())

if __name__ == '__main__':
    options, args = get_options()
    config_dir = args[0]
    
    result = crabCommand('status', dir=config_dir)
    
    filtered = filter_by_error_code(result, options.error_code)
    print_one(filtered)
    print_job_ids(filtered)
     
