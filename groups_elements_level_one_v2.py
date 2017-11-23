##### FUNCTIONS

def dict_elements_level_one(dictG):
  dictN = {}
  for iKey in dictG.iterkeys():
		tmpValues = []
		valuesTMP = grp_elements_level_one(iKey, dictG, dictG.keys(), tmpValues)
		dictN[iKey] = tmpValues
	return dictN

def grp_elements_level_one(nameGRP, dictGRPs, listGRPsUniq, elements_L01):
	for grp in dictGRPs[nameGRP]:
		if grp in listGRPsUniq:
			grp_elements_level_one(grp, dictGRPs, listGRPsUniq, elements_L01)
		else:
			elements_L01.append(grp)
	return elements_L01
	
##### MAIN PROGRAM

groups = {}

groups['group_01'] = ['element_grp01_01', 'element_grp01_02', 'element_grp01_03', 'element_grp01_04', 'element_grp01_05']
groups['group_02'] = ['element_grp02_01', 'element_grp02_02', 'element_grp02_03', 'element_grp02_04', 'element_grp02_05', 'group_01']
groups['group_03'] = ['element_grp03_01', 'element_grp03_02', 'element_grp03_03', 'element_grp03_04', 'element_grp03_05', 'group_02']
groups['group_04'] = ['element_grp04_01', 'element_grp04_02', 'element_grp04_03', 'element_grp04_04', 'element_grp04_05', 'group_03']
groups['group_05'] = ['element_grp05_01', 'element_grp05_02', 'element_grp05_03', 'element_grp05_04', 'element_grp05_05', 'group_04']

groups_new = dict_elements_level_one(groups)

for i in groups_new['group_05']:
	print 'group_05 \t', i
