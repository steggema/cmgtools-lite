#!/usr/bin/env python

from CMGTools.H2TauTau.proto.samples.component_index import ComponentIndex

if __name__ == '__main__':
    import os
    import sys
    import imp
    import pprint
    from optparse import OptionParser
    usage = "usage: %prog [options] pattern"
    parser = OptionParser(usage=usage)

    default_module = os.path.expandvars('$CMSSW_BASE/src/CMGTools/H2TauTau/python/proto/samples/summer16/htt_common.py')
    parser.add_option("-m", "--module", dest="module",
                      default=default_module,
                      help='column containing event number')

    (options,args) = parser.parse_args()
    if len(args)!=1:
        print parser.usage
        sys.exit(1)
    pattern = args[0]
    index=ComponentIndex(options.module)
    pprint.pprint(index.glob(pattern))
