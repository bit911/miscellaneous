
##### LIBRARIES

import re
import ipcalc
import py_ng_rbgn as rb
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 500000)
pd.set_option('display.max_columns', 150)
pd.set_option('display.width', 1000)
#pd.set_option('display.height', 1000)

##### FUNCTIONS


def interfacesEth2pdf(file_name):																# interfaces fisicas activo/backup
	dctIMB = {}
	lstInterfaces = []
	
	lines = rb.openFile_to_lstFile(file_name)
	lstMasterBkp = rb.lst_iDataRange(lines, '^\s+', '^redundancy-interface', 0)
	
	for iMB in lstMasterBkp:
		iM = iMB[0].strip().split(' ')[3]
		iB = iMB[0].strip().split(' ')[6]
		dctIMB[iM] = iM + ' - '+ iB

	lstInterface  = rb.lst_iDataRange(lines, '^\s+', '^interface ethernet', 2)
	
	for eth in lstInterface:
		if len(eth) > 2:
			if_name = eth[0].strip().split('terface ')[1].split(' ')[1]
			if_mode = 'master - backup'
			lstILGC = rb.lst_iDataRange(eth, '^\s+', '^logical', 2)
			for lgc in lstILGC:
				line1 = lgc[0].strip().split(' ')
				lgcNm = line1[1]
				vlanI = line1[3]
				icrt  = lgc[1].strip().split(' ')[1]
				lstInterfaces.append([icrt, dctIMB[if_name], if_mode, lgcNm, vlanI, '-'])
        #if len(eth) == 2:
            #if_name = eth[0].strip().split('terface ')[1].split(' ')[1]
            #if_mode = 'standby'
            #lstInterfaces.append(['-', if_name, if_mode, '-', '-', '-'])
	data  = np.array(lstInterfaces)
	dfIfs = pd.DataFrame(data, columns=['circuit', 'if-name','if-mode', 'lg-name', 'vlan-in', 'trunk'])

	return dfIfs
		
def groupInterfacesEth2pdf(file_name):															# interfaces fisicas port channel
    lstGrpInterfaces = []
    lines = rb.openFile_to_lstFile(file_name)
    lstGrpInterface = rb.lst_iDataRange(lines, '^\s+', '^group-interface', 2)

    for grp in lstGrpInterface:
        lstInterfaces = []
        gi_name = grp[0].strip().split('oup-interface ')[1]
        if_mode = 'group'
        for i in grp:
            match = re.search('^interface ', i)
            if match:
                lstInterfaces.append(i.rstrip().split(' ')[1])
        lstILGC = rb.lst_iDataRange(grp, '^\s+', '^logical', 0)
        for lgc in lstILGC:
            line1 = lgc[0].strip().split(' ')
            lgcNm = line1[1]
            vlanI = line1[3]
            icrt  = lgc[1].strip().split(' ')[1]
            if_name   = ' - '.join(lstInterfaces)
            #for if_name in lstInterfaces:
            lstGrpInterfaces.append([icrt, if_name, if_mode, lgcNm, vlanI, gi_name])
    data  = np.array(lstGrpInterfaces)
    dfIfs = pd.DataFrame(data, columns=['circuit', 'if-name','if-mode', 'lg-name', 'vlan-in', 'trunk'])
    return dfIfs



def filter_if_netws(file_name):																	# vrrp failover-group
    routes = []
    dc_routes = {}
    lines = rb.openFile_to_lstFile(file_name)
    fw_list_idata_01 = rb.lst_iDataRange(lines, '^\s+', 'vrrp failover-group', 2)
    
    for i in range(len(fw_list_idata_01)):
        fw_list_idata_02 = rb.lst_iDataRange(fw_list_idata_01[i], '^\s+', 'virtual-router vrrp-id', 0)

        for iData in fw_list_idata_02:
            ln0 = iData[0].strip().split('circuit')
            circuit = ln0[1].strip()
            vrrp_id = ln0[0].split('vrrp-id')[1]
            for k in iData[1:]:
                match1 = re.search('priority-delta', k)
                match2 = re.search('mac-usage', k)
                match3 = re.search('backup-stay-up', k)
                match4 = re.search('vap-group', k)
                match5 = re.search('  ip', k)
                if match1:
                    pr  = k.strip().split(' ')[1]
                if match2:
                    mu  = k.strip().split(' ')[1]
                if match3:
                    bs  = k.strip()
                if match4:
                    fw  = k.strip().split(' ')[1]
                if match5:
                    ip  = k.strip().split(' ')[1]
                    dst = str(ipcalc.Network(ip).network()) + '/' + str(ipcalc.Network(ip).mask)
                    
            if fw == 'FW_INTERNET':
                fw = 'FW_INT'
                routes.append([fw, dst, '0.0.0.0', circuit])
            elif fw == 'FW_SERVICIOS':
                fw = 'FW_SRV'
                routes.append([fw, dst, '0.0.0.0', circuit])
            elif fw == 'FW_RED':
                fw = 'FW_RED'
                routes.append([fw, dst, '0.0.0.0', circuit])
            elif fw == 'FW_CORPORATIVO':
                fw = 'FW_CRP'
                routes.append([fw, dst, '0.0.0.0', circuit])
            elif fw == 'FW_VPN':
                fw = 'FW_VPN'
                routes.append([fw, dst, '0.0.0.0', circuit])

    np_routes = np.array(routes)
    dc_routes['fw'] = np_routes[:,0]
    dc_routes['dst'] = np_routes[:,1]
    dc_routes['gw'] = np_routes[:,2]
    dc_routes['dev'] = np_routes[:,3]
    df_routes = pd.DataFrame(dc_routes, columns=['fw','dst','gw','dev'])
    return df_routes
    
def filter_ip_route(file_name):																	# routes								
    routes = []
    dc_routes = {}
    routes_all = []
    
    file_lines = rb.openFile_to_lstFile(file_name)
    for i in file_lines:
        line = i.strip()
        match = re.search("^ip route", line)
        if match:
            routes_all.append(line)

    for route in routes_all:
        r = route.split(' ')
        if r[0] == 'ip' and r[1] == 'route' and r[4] == 'vap-group' and r[6] == "circuit":
            if re.search("FW_INTERNET", route):
                routes.append(['FW_INT', r[2], r[3], r[7]])
            elif re.search("FW_SERVICIOS", route):
                routes.append(['FW_SRV', r[2], r[3], r[7]])
            elif re.search("FW_RED", route):
                routes.append(['FW_RED', r[2], r[3], r[7]])
            elif re.search("FW_CORPORATIVO", route):
                routes.append(['FW_CRP', r[2], r[3], r[7]])
            elif re.search("FW_VPN", route):
                routes.append(['FW_VPN', r[2], r[3], r[7]])
            else:
                #routes['FW_NOVAL'] += [route]
                aa = 0
                #print route
        elif r[2] == '0.0.0.0' and r[3] == '0.0.0.0':
            #routes['FW_BYDFT'] += [route]
            aa = 0
            #print route
        else:
            #routes['FW_NOVAL'] += [route]
            aa = 0
            #print route

    np_routes = np.array(routes)
    dc_routes['fw'] = np_routes[:,0]
    dc_routes['dst'] = np_routes[:,1]
    dc_routes['gw'] = np_routes[:,2]
    dc_routes['dev'] = np_routes[:,3]
    df_routes = pd.DataFrame(dc_routes, columns=['fw','dst','gw','dev'])
    return df_routes

    
def circuits2pdf(file_name):																	# circuits / vap-group
    lstCircuits = []
    lines = rb.openFile_to_lstFile(file_name)
    lstCircuit  = rb.lst_iDataRange(lines, '^\s+', '^circuit', 2)
    for iCrt in lstCircuit:
        line1  = iCrt[0].strip().split(' ')
        crtNm  = line1[1]
        crtId  = line1[3]
        domain = line1[5] if len(line1) > 4 else '-'
        line2  = iCrt[1].strip().split(' ')
        devNm  = line2[1]

        lstCVG = rb.lst_iDataRange(iCrt, '^\s+', '^vap-group', 2)
        for iCVG in lstCVG:
            crtVG = iCVG[0].strip().split(' ')[1]
            line3 = iCVG[1].strip().split(' ') if len(iCVG) > 1 else '-'
            vlanO = line3[1] if len(line3) > 1 else '-'
            hvhdr = line3[2] if len(line3) > 2 else '-'
            line4 = iCVG[2].strip().split(' ') if len(iCVG) > 2 else '-'
            ipVG  = line4[1] if len(line4) > 1 else '-'
            inPV  = line4[4] if len(line4) > 1 else '-'
            lstCircuits.append([crtNm, crtId, domain, devNm, crtVG, vlanO, hvhdr, ipVG, inPV])
    data  = np.array(lstCircuits)
    dfCrt = pd.DataFrame(data, columns=['circuit', 'circuit-id', 'domain', 'dev-name', 'vap-group', 'vlan-out', 'hide-vlan-header', 'circuit-ip', 'increment-per-vap'])
    return dfCrt

def vrrpFailOverGrps2pdf(file_name):															# vrrp_failover-group / virtual-router
    lstVFOGs = []
    lines = rb.openFile_to_lstFile(file_name)
    lstVFOG  = rb.lst_iDataRange(lines, '^\s+', '^vrrp failover-group', 2)
    for vfog in lstVFOG:
        fog_nm = vfog[0].strip().split(' ')[2]
        fog_id = vfog[0].strip().split(' ')[4]
        lstVRV = rb.lst_iDataRange(vfog, '^\s+', '^virtual-router', 2)
        for vrv in lstVRV:
            line0   = vrv[0].strip().split(' ')
            idVRRP  = line0[2]
            circuit = line0[4]
            prDLT = '-'
            mcUSG = '-'
            bkSUP = '-'
            vpGRP = '-'
            dst   = '-'
            for k in vrv:
                match1 = re.search('priority-delta', k)
                match2 = re.search('mac-usage', k)
                match3 = re.search('backup-stay-up', k)
                match4 = re.search('vap-group', k)
                match5 = re.search('  ip', k)
                if match1:
                    prDLT  = k.strip().split(' ')[1]
                if match2:
                    mcUSG  = k.strip().split(' ')[1]
                if match3:
                    bkSUP  = k.strip()
                if match4:
                    vpGRP  = k.strip().split(' ')[1]
                if match5:
                    ip  = k.strip().split(' ')[1]
                    dst = str(ipcalc.Network(ip).network()) + '/' + str(ipcalc.Network(ip).mask)
            lstVFOGs.append([fog_nm, fog_id, idVRRP, circuit, prDLT, mcUSG, bkSUP, vpGRP, ip])
    data   = np.array(lstVFOGs)
    dfVFOG = pd.DataFrame(data, columns=['vfog-name', 'vfog-id', 'vrrp-id', 'circuit', 'prio-delta', 'mac-usage', 'bkp-stay-up', 'vap-group', 'circuit-vrrp-ip'])
    return dfVFOG

def ipRoute2pdf(file_name):
    routes = []
    routes_all = []
    lines = rb.openFile_to_lstFile(file_name)
    for i in lines:
        line = i.strip()
        match = re.search("^ip route", line)
        if match:
            routes_all.append(line)

    for route in routes_all:
        r = route.split(' ')
        if r[0] == 'ip' and r[1] == 'route' and r[4] == 'vap-group' and r[6] == "circuit":
            if re.search("FW_INTERNET", route):
                routes.append(['FW_INTERNET', r[2], r[3], r[7]])
            elif re.search("FW_SERVICIOS", route):
                routes.append(['FW_SERVICIOS', r[2], r[3], r[7]])
            elif re.search("FW_RED", route):
                routes.append(['FW_RED', r[2], r[3], r[7]])
            elif re.search("FW_CORPORATIVO", route):
                routes.append(['FW_CORPORATIVO', r[2], r[3], r[7]])
            elif re.search("FW_VPN", route):
                routes.append(['FW_VPN', r[2], r[3], r[7]])
            else:
                #routes['FW_NOVAL'] += [route]
                aa = 0
                #print route
#        elif r[2] == '0.0.0.0' and r[3] == '0.0.0.0':
            #routes['FW_BYDFT'] += [route]
#            aa = 0
            #print route
#        else:
            #routes['FW_NOVAL'] += [route]
#            aa = 0
            #print route
    data     = np.array(routes)
    dfroutes = pd.DataFrame(data, columns=['vap-group','dst','gw','dev-name'])
    return dfroutes

def ifRoute2pdf(file_name):
    routes = []
    lines = rb.openFile_to_lstFile(file_name)
    fw_list_idata_01 = rb.lst_iDataRange(lines, '^\s+', '^vrrp failover-group', 2)
    for i in range(len(fw_list_idata_01)):
        fw_list_idata_02 = rb.lst_iDataRange(fw_list_idata_01[i], '^\s+', 'virtual-router vrrp-id', 0)

        for iData in fw_list_idata_02:
            ln0 = iData[0].strip().split('circuit')
            circuit = ln0[1].strip()
            vrrp_id = ln0[0].split('vrrp-id')[1]
            for k in iData[1:]:
                match1 = re.search('priority-delta', k)
                match2 = re.search('mac-usage', k)
                match3 = re.search('backup-stay-up', k)
                match4 = re.search('vap-group', k)
                match5 = re.search('  ip', k)
                if match1:
                    pr  = k.strip().split(' ')[1]
                if match2:
                    mu  = k.strip().split(' ')[1]
                if match3:
                    bs  = k.strip()
                if match4:
                    fw  = k.strip().split(' ')[1]
                if match5:
                    ip  = k.strip().split(' ')[1]
                    dst = str(ipcalc.Network(ip).network()) + '/' + str(ipcalc.Network(ip).mask)
                    
            if fw == 'FW_INTERNET':
                fw = 'FW_INTERNET'
                routes.append([fw, dst, '0.0.0.0', circuit])
            elif fw == 'FW_SERVICIOS':
                fw = 'FW_SERVICIOS'
                routes.append([fw, dst, '0.0.0.0', circuit])
            elif fw == 'FW_RED':
                fw = 'FW_RED'
                routes.append([fw, dst, '0.0.0.0', circuit])
            elif fw == 'FW_CORPORATIVO':
                fw = 'FW_CORPORATIVO'
                routes.append([fw, dst, '0.0.0.0', circuit])
            elif fw == 'FW_VPN':
                fw = 'FW_VPN'
                routes.append([fw, dst, '0.0.0.0', circuit])
    data     = np.array(routes)
    dfroutes = pd.DataFrame(data, columns=['vap-group','dst','gw','dev-name'])
    return dfroutes    


def show_ip_route(ip, pdf_routes):
    ls_routes = []
    psr_dst = pdf_routes.dst
    for i, dst in psr_dst.items():
        if ipcalc.Network(ip) in ipcalc.Network(dst):                                        # *
            sr_route = pdf_routes.loc[i]
            ls_routes.append(sr_route)
    labels = ['fw', 'dst', 'gw', 'dev']
    pdf_routes = pd.DataFrame.from_records(ls_routes, columns=labels)
    #pdf_routes = show_ip_route_optimice(ip, pdf_routes)
    return pdf_routes

def show_ip_route_optimice(ip, df_routes):    
    for fw in df_routes.fw.unique():                                                        # **                    
        df_routes_fw = df_routes.loc[(df_routes['fw'] == fw)]
        drf = df_routes_fw
        if drf.fw.unique().size == 1 and drf.gw.unique().size == 1 and drf.dev.unique().size == 1:
            if drf.size > 4:
                indx = 0
                band = 0
                for i in drf.index:                                                            # ***
                    if ipcalc.Network(drf.dst[i]).mask > band:
                        band = ipcalc.Network(drf.dst[i]).mask
                        indx = i
                a = list(drf.index)
                a.remove(indx)
                df_routes = df_routes.drop(a)
        else:
            print 'existe un error en las siguientes rutas... para la IP: ', ip
            print df_routes
            exit()
    return df_routes


def X80config2pdf(file_name):
	#df1 = interfacesEth2pdf(file_name)
	#df2 = groupInterfacesEth2pdf(file_name)
	#dfx = pd.concat([df1, df2], ignore_index=True)
	
	df3 = circuits2pdf(file_name)
	df4 = vrrpFailOverGrps2pdf(file_name)
	
	return df4
	
def help():
	print "..."

    
##### MAIN PROGRAM

#if __name__== "__main__":
#  main()  