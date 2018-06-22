echo 'set cms environment'
source /cvmfs/cms.cern.ch/cmsset_default.sh
echo 'set crab3 environment'
source /cvmfs/cms.cern.ch/crab3/crab.sh
echo 'set cms vo proxy'
voms-proxy-init -voms cms
cd ../..
echo 'set cmssw environment...'
cmsenv
echo 'set cmssw environment:' $CMSSW_RELEASE_BASE
cd CMGTools/H2TauTau
export X509_USER_PROXY=$HOME/private/cms.proxy
mkdir -p $HOME/private
