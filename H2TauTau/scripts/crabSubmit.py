from CMGTools.H2TauTau.proto.samples.component_index import ComponentIndex

if __name__ == '__main__':
    import os
    import sys
    import imp
    import pprint
    from optparse import OptionParser
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    default_module = os.path.expandvars('$CMSSW_BASE/src/CMGTools/H2TauTau/python/proto/samples/summer16/htt_common.py')
    parser.add_option("-m", "--module", dest="module",
                      default=default_module,
                      help='module where the components are defined')
    parser.add_option("-n", "--dry-run", dest="dryrun",
                      action='store_true',
                      default=False,
                      help='set up the jobs and do nothing')
    parser.add_option("-p", "--pattern", dest="pattern",
                      default='*',
                      help='pattern selecting the datasets to submit')
    options, args = parser.parse_args()

    if options.dryrun:
        print 'Dry run, will do nothing'

    index=ComponentIndex(options.module)
    
    print 'datasets to be submitted:'
    pprint.pprint(index.glob(options.pattern))
    if not options.dryrun:
        print 
        answer=None
        while answer not in ['y','n']:
            answer=raw_input('Are you sure? [y/n]')

