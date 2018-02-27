from optparse import OptionParser
import numpy as np
from sklearn import svm, metrics, preprocessing
from sklearn.externals import joblib
import warnings
import os
warnings.simplefilter("ignore")


parser = OptionParser()

parser.add_option('--files', type='string', action='store', dest='files', help='Input Files')
parser.add_option('--outname', type='string', action='store',default='outplots.root', dest='outname',help='Name of output file')
parser.add_option('--maxevents', type='int', action='store',default=-1,dest='maxevents',help='Number of events to run. -1 is all events')


(options, args) = parser.parse_args()
argv = []

import ROOT
import sys, copy
from array import array
from DataFormats.FWLite import Events, Handle


f = ROOT.TFile(options.outname, "RECREATE")
f.cd()

eventTree = ROOT.TTree('eventVars', 'eventVars')
prob_t = array('f', [-999.])
prob_W = array('f', [-999.])
prob_Z = array('f', [-999.])
prob_H = array('f', [-999.])
prob_j = array('f', [-999.])


jetsHandle = Handle("std::vector<pat::Jet>")
jetsLabel = ("BESTProducer", "savedJets", "ttbarACskim")
npvHandle = Handle("std::vector<int>")
npvLabel = ("BESTProducer", "nPV", "run")
nnLabels = []
nnLabels.append( ("BESTProducer", "FWmoment1H", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "FWmoment1W", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "FWmoment1Z", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "FWmoment1top", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "FWmoment2H", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "FWmoment2W", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "FWmoment2Z", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "FWmoment2top", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "FWmoment3H", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "FWmoment3W", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "FWmoment3Z", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "FWmoment3top", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "FWmoment4H", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "FWmoment4W", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "FWmoment4Z", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "FWmoment4top", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "SDmass", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "aplanarityH", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "aplanarityW", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "aplanarityZ", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "aplanaritytop", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "bDisc", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "bDisc1", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "bDisc2", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "et", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "eta", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "isotropyH", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "isotropyW", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "isotropyZ", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "isotropytop", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "q", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "sphericityH", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "sphericityW", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "sphericityZ", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "sphericitytop", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "sumPH", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "sumPW", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "sumPZ", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "sumPtop", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "sumPzH", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "sumPzW", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "sumPzZ", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "sumPztop", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "tau21", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "tau32", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "thrustH", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "thrustW", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "thrustZ", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "thrusttop", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m12H", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m23H", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m13H", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m1234H", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m12W", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m23W", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m13W", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m1234W", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m12Z", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m23Z", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m13Z", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m1234Z", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m12top", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m23top", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m13top", "ttbarACskim") )
nnLabels.append( ("BESTProducer", "m1234top", "ttbarACskim") )
nnHandles = [ Handle("vector<float>") ] * len(nnLabels)




filelist = options.files
files= []
nevents = 0
s = options.files
#s = 'root://cmsxrootd.fnal.gov/' + options.files
files.append(s)
print 'Added' + s

mlp = joblib.load('BEST_mlp.pkl')
scaler = joblib.load('BEST_scaler.pkl')



nevents_file = 0
for ifile in files:
	print 'Processing', ifile

	if options.maxevents > 0 and nevents > options.maxevents :
        	break

	events = Events( ifile )


	products = {}

	event.getByLabel(jetsLabel, jetsHandle)
	if not jetsHandle.isValid():
		continue
	jets = jetsHandle.product()

	for event in events:
		
		if options.maxevents > 0 and nevents > options.maxevents :
        		break
		nevents += 1
		nevents_file += 1
		if (nevents_file % 1000 == 0):
			print nevents, ' Completed'




		event.getByLabel(npvLabel, npvHandle)
		npv[0] = npvHandle.product()[0]
		for i in xrange(len(nnHandles)):
			event.getByLabel((nnLabels[i]), nnHandles[i])
			products[nnLabels[i][1]] = nnHandles[i].product() 

	
		for j in xrange(len(jets)):

			nhf = jets[j].neutralHadronEnergy() / jets[j].energy()
                	nef = jets[j].neutralEmEnergy() / jets[j].energy()
                	chf = jets[j].chargedHadronEnergy() / jets[j].energy()
                	cef = jets[j].chargedEmEnergy() / jets[j].energy()
                	nconstituents = jets[j].numberOfDaughters()
                	nch = jets[j].chargedMultiplicity()
                	goodJet = \
                  		nhf < 0.99 and \
                  		nef < 0.99 and \
                  		chf > 0.00 and \
                  		cef < 0.99 and \
                  		nconstituents > 1 and \
                  		nch > 0

                	if not goodJet :
				continue

			if jets[j].pt() < 400:
				continue

			#genPtV[0] =  products['genPt'][j]
			#topSizeV[0] = products['topSize'][j]
			#dRgenParticleV[0] = products['dRjetParticle'][j]

			jetPt[0] = jets[j].pt()
			jetPhi[0] = jets[j].phi()
			jetEta[0] = jets[j].eta()

			jetSDmass[0] = products['SDmass'][j]

			pzOverp_top = products['sumPztop'][j] / (products['sumPtop'][j] + 0.01) 
			pzOverp_W = products['sumPzW'][j] / (products['sumPW'][j] + 0.01) 
			pzOverp_Z = products['sumPzZ'][j] / (products['sumPZ'][j] + 0.01)
			pzOverp_H = products['sumPzH'][j] / (products['sumPH'][j] + 0.01)


			nnArray = np.array( [  products['SDmass'][j], products['tau32'][j], products['tau21'][j], products['FWmoment1top'][j], products['FWmoment2top'][j], products['FWmoment3top'][j], products['FWmoment4top'][j], products['isotropytop'][j], products['aplanaritytop'][j], products['sphericitytop'][j], products['thrusttop'][j], products['FWmoment1W'][j], products['FWmoment2W'][j], products['FWmoment3W'][j], products['FWmoment4W'][j], products['isotropyW'][j], products['aplanarityW'][j], products['sphericityW'][j], products['thrustW'][j], products['FWmoment1Z'][j], products['FWmoment2Z'][j], products['FWmoment3Z'][j], products['FWmoment4Z'][j], products['isotropyZ'][j], products['aplanarityZ'][j], products['sphericityZ'][j], products['thrustZ'][j], products['FWmoment1H'][j], products['FWmoment2H'][j], products['FWmoment3H'][j], products['FWmoment4H'][j], products['isotropyH'][j], products['aplanarityH'][j], products['sphericityH'][j], products['thrustH'][j], products['bDisc'][j], products['bDisc1'][j], products['bDisc2'][j], products['q'][j], products['m12W'][j], products['m13W'][j], products['m23W'][j], products['m1234W'][j], products['m12Z'][j], products['m13Z'][j], products['m23Z'][j], products['m1234Z'][j], products['m12top'][j], products['m13top'][j], products['m23top'][j], products['m1234top'][j], products['m12H'][j], products['m13H'][j], products['m23H'][j], products['m1234H'][j], pzOverp_top, pzOverp_W, pzOverp_Z, pzOverp_H  ])


			


			if np.isnan(np.min(nnArray)):
				continue

			nnArray_transformed = scaler.transform( nnArray )



			best_bin = mlp.predict( nnArray_transformed )

			best_probs = mlp.predict_proba( nnArray_transformed )

			htV[0] += jetPt[0]

			prob_j[0] = best_probs[0][0]
			prob_W[0] = best_probs[0][1]
			prob_Z[0] = best_probs[0][2]
			prob_H[0] = best_probs[0][3]
			prob_t[0] = best_probs[0][4]


			best_class[0] = best_bin[0]			
			


		eventTree.Fill()



f.cd()
f.Write()
f.Close()
