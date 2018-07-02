import unittest
import tempfile

from harvest import *

class TestGFAL(unittest.TestCase):
    
    def test_rfile(self):
        gfal = GFAL()
        self.assertEqual(gfal._file('/store'),
                         'srm://lyogrid06.in2p3.fr:8446/srm/managerv2?SFN=/dpm/in2p3.fr/home/cms/data/store')
        self.assertEqual(gfal._file('test'),
                         'file:test')

    def test_ls(self):
        gfal = GFAL(False)
        self.assertEqual(gfal.ls('test'), 
                         'gfal-ls file:test')
        self.assertEqual(gfal.ls('/store/user/cbernet/heppyTrees'),
                         'gfal-ls srm://lyogrid06.in2p3.fr:8446/srm/managerv2?SFN=/dpm/in2p3.fr/home/cms/data/store/user/cbernet/heppyTrees')

    def test_run(self):
        gfal = GFAL(True)
        with tempfile.NamedTemporaryFile() as tfile:
            self.assertEqual(gfal.ls(tfile.name),
                             [''.join(['file:',tfile.name])])

    def test_ls_real(self):
        gfal = GFAL(True)
        path = '/store/user/cbernet/heppyTrees/CMSSW_8_0_28_patch1/tauMu_2017_cfg/HiggsSUSYBB1000/180625_123805/0000'
        result = gfal.ls(path)
        tgzs = [fname for fname in result if fname.endswith('.tgz')]
        self.assertEqual(len(tgzs),9)
            

class TestDataset(unittest.TestCase):

    def setUp(self):
        self.basepath = '/store/user/cbernet/heppyTrees/CMSSW_8_0_28_patch1/tauMu_2017_cfg/HiggsSUSYBB1000/180625_123805'
        self.ds = Dataset(self.basepath, tgzs='*[12].tgz')

    def test_paths(self):
        self.assertEqual(self.ds.subdirs, ['0000'])
        self.assertEqual(len(self.ds.tgzs['0000']), 2)

    def test_fetch(self):
        # ds = Dataset(self.basepath)
        ds = self.ds
        ds.fetch()

    def test_unpack(self):
        # ds = Dataset(self.basepath)
        ds = self.ds
        ds.unpack()

    def test_patterns(self):
        ds =  Dataset(self.basepath,subdirs='')
        self.assertEqual(ds.subdirs, [])

if __name__ == '__main__':
    unittest.main()
