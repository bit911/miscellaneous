
def groups_to_tree_level_one(dictGROUPS):
	levels = 0
	dictGROUPS_NEW = {}
	for nameGROUP in dictGROUPS.keys():
		interGALAXI = []
		namesGROUPS = dictGROUPS.keys()
		interGALAXI = group_to_tree_level_one(nameGROUP, dictGROUPS, namesGROUPS, interGALAXI, levels)
		dictGROUPS_NEW[nameGROUP] = interGALAXI
	return dictGROUPS_NEW
  
def group_to_tree_level_one(nameGRP, dictGRPs, nameGRPs, interGLX, lvl):
	lvl = lvl + 1
	elmGRP = dictGRPs[nameGRP]
	for elm in elmGRP:
		tmp = {}
		if elm in nameGRPs:
			group_to_tree_level_one(elm, dictGRPs, nameGRPs, interGLX, lvl)
		else:
			tmp['grp'] = nameGRP
			tmp['elm'] = elm
			tmp['lvl'] = lvl
			interGLX.append(tmp)
	return interGLX
  
def group_to_tree_level_two(group):
	cont = 0
	tree = {}
	for i in group:
		tree[i['lvl']] = i['grp']
		if i['lvl'] > cont:
			cont = i['lvl']
			
	for i in range(1, cont+1):
		abc = []
		cde = ''
		for j in group:
			if i == j['lvl']:
				for k in range(1, i+1):
					if not (j['grp'] in abc):
						#abc.append(tree[k])
						cde = cde + "\t" +tree[k]
				print cde.lstrip(), "\t" ,j['elm']
		print "------------------------------------------------------------------------------"
    
##### MAIN PROGRAM

groups = {}

groups['group_01'] = ['element_grp01_01', 'element_grp01_02', 'element_grp01_03', 'element_grp01_04', 'element_grp01_05']
groups['group_02'] = ['element_grp02_01', 'element_grp02_02', 'element_grp02_03', 'element_grp02_04', 'element_grp02_05', 'group_01']
groups['group_03'] = ['element_grp03_01', 'element_grp03_02', 'element_grp03_03', 'element_grp03_04', 'element_grp03_05', 'group_02']
groups['group_04'] = ['element_grp04_01', 'element_grp04_02', 'element_grp04_03', 'element_grp04_04', 'element_grp04_05', 'group_03']
groups['group_05'] = ['element_grp05_01', 'element_grp05_02', 'element_grp05_03', 'element_grp05_04', 'element_grp05_05', 'group_04']

groups_new = groups_to_tree_level_one(groups)

group_to_tree_level_two(groups_new['group_05'])    
