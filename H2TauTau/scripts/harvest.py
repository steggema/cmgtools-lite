#!/usr/bin/env python

import os 
import subprocess
import re
import shutil
import fnmatch

class GFAL(object):

    def __init__(self, run=True):
        self.rprefix = 'srm://lyogrid06.in2p3.fr:8446/srm/managerv2?SFN=/dpm/in2p3.fr/home/cms/data'
        self.lprefix = 'file:'
        self.run = run

    def _file(self, path):
        if path.startswith('/store'):
            return ''.join([self.rprefix, path])
        else:
            return ''.join([self.lprefix, path])

    def _run(self, cmd):
        pipe = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE)
        return pipe.communicate()[0]

    def ls(self, path, opt=None):
        if opt: 
            cmd = 'gfal-ls {opt} {path}'.format( opt=opt, 
                                                 path=self._file(path))
        else: 
            cmd = 'gfal-ls {path}'.format(path=self._file(path))    
        if self.run: 
            return self._run(cmd).splitlines() 
        else:
            return cmd

    def cp(self, src, dest, opt=None):
        if opt: 
            cmd = 'gfal-copy {opt} {src} {dest}'.format( 
                opt=opt, 
                src=self._file(src),
                dest=self._file(dest)
                )
        else: 
            cmd = 'gfal-copy {src} {dest}'.format(
                src=self._file(src),
                dest=self._file(dest)
                )    
        if self.run: 
            return self._run(cmd).splitlines() 
        else:
            return cmd

gfal = GFAL()

class Dataset(object):
    
    def __init__(self,path,subdirs='*',tgzs='*'):
        self.path = path
        self.name = self.path.split('/')[-2]
        self.subdir_pattern = subdirs
        self.tgz_pattern = tgzs
        self.subdirs = self.find_subdirs(path)
        self.tgzs = dict()
        for subd in self.subdirs:
            self.tgzs[subd] = self.find_tgzs(subd)
        self.dest = None

    def abspath(self, path):
        return '/'.join([self.path, path])

    def find_subdirs(self,path):
        subdirs = gfal.ls(self.path)
        pattern = re.compile('^\d{4}$')
        subdirs = [subd for subd in subdirs if pattern.match(subd)
                   and fnmatch.fnmatch(subd, self.subdir_pattern)]
        return subdirs

    def find_tgzs(self, subd):
        subd = self.abspath(subd)
        files = gfal.ls(subd)
        files = [f for f in files if f.endswith('.tgz')
                 and fnmatch.fnmatch(f, self.tgz_pattern)]
        return files

    def fetch(self, dest=None):
        if dest is None: 
            dest = '/'.join(self.path.split('/')[-2:])
        if os.path.isdir(dest):
            answer = None
            while answer not in ['y','n']:
                answer = raw_input('destination {} exists. continue? [y/n]'.format(dest))
            if answer == 'n':
                return 
            shutil.rmtree(dest)
        basepath=os.getcwd()
        os.makedirs(dest)
        self.dest = dest
        os.chdir(dest)
        destpath=os.getcwd()
        for subd, files in self.tgzs.iteritems():
            print 'fetching subdir', subd
            os.mkdir(subd)
            os.chdir(subd)
            for f in files:
                path = self.abspath('/'.join([subd, f]))
                print gfal.ls(path)
                gfal.cp(path, '.')
            os.chdir(destpath)
        os.chdir(basepath)

    def unpack(self):
        if self.dest is None:
            print 'dataset was not fetched, fetching now'
            self.fetch()
        basepath=os.getcwd()
        os.chdir(self.dest)
        destpath = os.getcwd()
        for subd, files in self.tgzs.iteritems():
            print 'upackging subdir', subd
            os.chdir(subd)
            for i, f in enumerate(files): 
                print 'unpacking', f
                os.system('tar -zxf ' + f)
                os.rename('Output', 
                          '{}_Chunk{}'.format(self.name, str(i)))
                os.remove(f)
            os.chdir(destpath)
        os.chdir(basepath)

def get_options():
    import os
    import sys
    from optparse import OptionParser
    usage = "usage: %prog [options] <src_dir>"
    parser = OptionParser(usage=usage)
    parser.add_option("-t", "--tgz-pattern", dest="tgz_pattern",
                      default='*',
                      help='tgz pattern')
    parser.add_option("-s", "--subdir-pattern", dest="subdir_pattern",
                      default='*',
                      help='subdir pattern')
 
    
    (options,args) = parser.parse_args()
    if len(args)!=1:
        print parser.usage
        sys.exit(1)
    return options, args


if __name__ == '__main__':

    options, args = get_options()
    src = args[0]
    ds = Dataset(src, 
                 subdirs=options.subdir_pattern, 
                 tgzs=options.tgz_pattern)
    ds.fetch()
    ds.unpack()
