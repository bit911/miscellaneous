
##### LIBRARIES

import re
import sys

##### FUNCTIONS

def openFile_to_strFile(txtFile):
    ''' Lee un archivo y retorna un string '''
    try:
        file_object = open(txtFile, 'r')
        return file_object.read()
    except IOError, message:
		print message
		sys.exit( 1 )

def openFile_to_lstFile(txtFile):
    ''' Lee un archivo y retorna un list '''
    try:
        file_object = open(txtFile, 'r')
        return file_object.readlines()
    except IOError, message:
		print message
		sys.exit( 1 )

def lst_index_range(lines, genPattern, expPattern):
    '''
    '''
    index_gen = []
    index_exp = []                                               # lineas marcadas con criterio 1 
    index_rng = []
    lines.append('')                                             # ?????? 
    '''
    Marca los indices de las lineas que machan con el patron genPattern
    Tambien considera si o si el indice de la ultima linea (truco)
    '''
    for i in range(len(lines)):                                   # Para i del list FILE
        line = lines[i].rstrip()                                  # lo normaliza
        match = re.search(genPattern, line)                       # *** patron 01
        if not match:                                             # sino se NO cumple el match
            index_gen.append(i)                                   # marca la linea
    index_gen.append(len(lines)-1)                                # CUMPLA o NO marca la linea final 
    
    '''
    Para las lineas de los indices marcados por el patron genPattern
    verifica el segundo patron expPattern
    '''
    for i in index_gen:                                           # Para cada indice marcado             
		line = lines[i].rstrip()                                  # normaliza su linea            
		match = re.search(expPattern, line)						  # *** patron 00
		if match:                                                 # si la linea cumple
			index_exp.append(i)                                   # marca el indice
            
    '''
    Para cada uno de los indices que cumplen las 2 condiciones
    determina su indice final y lo guarda en un list y lo retorna
    '''
    for i in index_exp:                                           # para cada indice del expPattern
        a = index_gen.index(i)                                    # determina su ubicacion en el list genPattern
        index_rng.append([index_gen[a], index_gen[a+1]])          # determina su indice e indice + 1
    
    return index_rng

def lst_iDataRange(lines, genPattern, expPattern, desf):
    '''
    '''
    lst_iData = []                                                # list de resultados
    lstIndexRange = lst_index_range(lines, genPattern, expPattern)# determina los pares de indices
    for i in range(len(lstIndexRange)):                           # para cada par de indices        
		iData = lines[lstIndexRange[i][0]: lstIndexRange[i][1]]   # determina su data
		new_iData = []                                            # list para data normalizada            
		for line in iData:                                        # para cada linea de data
			new_iData.append(line[desf:].rstrip())                # corta la linea segun el desface   
		lst_iData.append(new_iData)                               # la nueva data lo guarda en un list	
    return lst_iData
