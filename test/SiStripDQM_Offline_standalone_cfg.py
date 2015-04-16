
import FWCore.ParameterSet.Config as cms

process = cms.Process("SiStrpDQMQTestTuning")


## Empty Event Source
process.source = cms.Source("EmptyIOVSource",
                              lastRun = cms.untracked.uint32(100),
                              timetype = cms.string('runnumber'),
                              firstValue= cms.uint64(1),
                              lastValue= cms.uint64(1),
                              interval = cms.uint64(1)
                            )

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = "GR09_P_V2::All"
process.GlobalTag.globaltag = "DESRUN1_73_V2::All"
#process.GlobalTag.globaltag = "GR_E_V43::All"
# loading TrackerTopologyEP via GeometryDB (since 62x)
process.load('Configuration.StandardSequences.GeometryDB_cff')

# DQM Environment
process.load("DQMServices.Core.DQM_cfg")

process.TkDetMap = cms.Service("TkDetMap")
process.SiStripDetInfoFileReader = cms.Service("SiStripDetInfoFileReader")

# SiStrip Offline DQM Client
# SiStrip Offline DQM Client
process.siStripOfflineAnalyser = cms.EDAnalyzer("SiStripOfflineDQM",
       GlobalStatusFilling      = cms.untracked.int32(-1),
       CreateSummary            = cms.untracked.bool(False),
       SummaryConfigPath        = cms.untracked.string("DQM/SiStripMonitorClient/data/sistrip_monitorelement_config.xml"),
       UsedWithEDMtoMEConverter = cms.untracked.bool(False),
       PrintFaultyModuleList    = cms.untracked.bool(False),
#       InputFileName            = cms.untracked.string("file:/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/data/Online//110/998/DQM_V0002_R000110998.root"),
#       InputFileName            = cms.untracked.string("file:/afs/cern.ch/work/r/rrabadan/public/trkDQMsw/CMSSW_7_3_0/src/DQMServices/Components/test/1425955901/3/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO_4.root"),
       InputFileName		= cms.untracked.string("DQM_V0003_R000239622__StreamExpressCosmics__Commissioning2015-Express-v1__DQM.root"),
       OutputFileName           = cms.untracked.string("test.root"),
       CreateTkMap              = cms.untracked.bool(True),
       TkmapParameters          = cms.untracked.PSet(
          loadFedCabling    = cms.untracked.bool(True),
          trackerdatPath    = cms.untracked.string('CommonTools/TrackerMap/data/'),
          trackermaptxtPath = cms.untracked.string('CommonTools/TrackerMap/data/'),
       ),
#       TkMapOptions         = cms.untracked.vstring('QTestAlarm','FractionOfBadChannels','NumberOfCluster','NumberOfDigi','NumberOfOfffTrackCluster','NumberOfOnTrackCluster','StoNCorrOnTrack')
       TkMapOptions	     = cms.untracked.VPSet(
          cms.PSet(mapName=cms.untracked.string('QTestAlarm')),
#	  cms.PSet(mapName=cms.untracked.string('NumberOfCluster'),TopNmodules=cms.untracked.bool(True),
#                   minTopNmodules=cms.untracked.int32(35))
#,
          cms.PSet(mapName=cms.untracked.string('NumberOfDigi'),TopNmodules=cms.untracked.bool(True),
		   minTopNmodules=cms.untracked.int32(10))
,
	  cms.PSet(mapName=cms.untracked.string('NumberOfOfffTrackCluster')),
          cms.PSet(mapName=cms.untracked.string('NumberOfOnTrackCluster'))
       )
)


# QTest module
process.siStripQTester = cms.EDAnalyzer("QualityTester",
                              qtList = cms.untracked.FileInPath('DQM/SiStripMonitorClient/data/sistrip_qualitytest_config.xml'),
                              prescaleFactor = cms.untracked.int32(1),
                              getQualityTestsFromFile = cms.untracked.bool(True)
                          )


# Tracer service
#process.Tracer = cms.Service('Tracer',indentation = cms.untracked.string('$$'))
process.load('DQM.SiStripCommon.MessageLogger_cfi')

process.p1 = cms.Path(process.siStripOfflineAnalyser)
