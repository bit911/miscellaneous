#!/usr/bin/env python

def grps_to_elements_L01(dictGRPs):
	dictGRP_L01 = {}
	for grp in dictGRPs.iterkeys():
		elementsTMP = []
		elementsGRP = grp_elements_to_L01(grp, dictGRPs, dictGRPs.keys(), elementsTMP)
		dictGRP_L01[grp] = elementsGRP
	return dictGRP_L01

def grp_elements_to_L01(nameGRP, dictGRPs, listGRPsUniq, elements_L01):
	for grp in dictGRPs[nameGRP]:
		if grp in listGRPsUniq:
			grp_elements_to_L01(grp, dictGRPs, listGRPsUniq, elements_L01)
		else:
			elements_L01.append(grp)
	return elements_L01
