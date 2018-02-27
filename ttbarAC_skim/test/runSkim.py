import FWCore.ParameterSet.Config as cms

process = cms.Process("ttbarACskim")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(

	'/store/mc/RunIISpring16MiniAODv2/ZprimeToTT_M-3000_W-30_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/70000/1A405524-3E3D-E611-B103-047D7BD6DDB2.root'

	)
)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.BESTProducer = cms.EDProducer('BESTProducer',
	pdgIDforMatch = cms.int32(6),
	NNtargetX = cms.int32(1),
	NNtargetY = cms.int32(1),
	isMC = cms.int32(1),
	doMatch = cms.int32(0)

)

process.selectedMuons = cms.EDFilter('EtaPtMinCandViewSelector',
    src = cms.InputTag('slimmedMuons'),
    ptMin = cms.double(40.),
    etaMin = cms.double(-2.4),
    etaMax = cms.double(2.4)
)

process.selectedElectrons = cms.EDFilter('EtaPtMinCandViewSelector',
    src = cms.InputTag('slimmedElectrons'),
    ptMin = cms.double(40.),
    etaMin = cms.double(-2.4),
    etaMax = cms.double(2.4)
)

process.selectedAK8Jets = cms.EDFilter('EtaPtMinCandViewSelector',
    src = cms.InputTag('slimmedJetsAK8'),
    ptMin = cms.double(350.),
    etaMin = cms.double(-2.4),
    etaMax = cms.double(2.4)
)

process.selectedAK4Jets = cms.EDFilter('EtaPtMinCandViewSelector',
    src = cms.InputTag('slimmedJets'),
    ptMin = cms.double(50.),
    etaMin = cms.double(-2.4),
    etaMax = cms.double(2.4)
)

process.selectedMET = cms.EDFilter('PtMinCandViewSelector',
    src = cms.InputTag('slimmedMETs'),
    ptMin = cms.double(-999.),
)


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("ana_out.root"),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      'keep *_*BEST*_*_*',
								      'keep *_*TriggerResults*_*_*',
								      'keep *_*_*_*ttbarAC*'
                                                                      #, 'keep *_goodPatJetsCATopTagPF_*_*'
                                                                      #, 'keep recoPFJets_*_*_*'
                                                                      ) 
                               )


process.outpath = cms.EndPath(process.out)

process.p = cms.Path(process.BESTProducer*
		     process.selectedMuons*
		     process.selectedElectrons*
	 	     process.selectedAK8Jets*
		     process.selectedAK4Jets*
		     process.selectedMET
)


