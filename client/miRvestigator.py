from mod_python import apache
from mod_python import util
import re
import Pyro.core
import datetime
from mirv_db import get_job_status



# stuff parameters into a dictionary and pop those onto a queue
def submitJob(req):
    # create a job object which will be queued
    job = {}
    job['created'] = datetime.datetime.now()

    # Get the variables
    job['genes'] = re.split('\s*[,;\s]\s*', req.form.getfirst('genes','').strip())
    job['s6'] = str(req.form.getfirst('seedModel_6',''))
    job['s7'] = str(req.form.getfirst('seedModel_7',''))
    job['s8'] = str(req.form.getfirst('seedModel_8',''))
    job['bgModel'] = str(req.form.getfirst('bgModel',''))
    job['wobble'] = str(req.form.getfirst('wobble',''))
    job['cut'] = str(req.form.getfirst('cut',''))
    job['m6'] = str(req.form.getfirst('motif_6',''))
    job['m8'] = str(req.form.getfirst('motif_8',''))
    job['topRet'] = str(req.form.getfirst('topRet',''))
    job['jobName'] = str(req.form.getfirst('jobName',''))

    # connect to miR server via Pyro
    uriFile = open('/var/www/uri','r')
    uri = uriFile.readline().strip()
    uriFile.close()
    miR_server = Pyro.core.getProxyForURI(uri)
    Pyro.core.initClient()

    # submit job to server process and redirect to status page
    job_id = miR_server.submit_job(job)
    util.redirect(req, req.construct_url("/status/%s/" % (job_id)))


# return a JSON string encoding job status
def status(req):
    id = str(req.form.getfirst('id',''))
    req.content_type='application/json'
    return "{ \"created_at\": \"%s\", \"updated_at\": \"%s\", \"status\": \"%s\" }" % get_job_status(id)

# display results
def results(req):
    # need weederPSSMs1
    # need topRet
    # need mV
    # miRNADict[j.strip()] ??
    # functions: conv2rna, reverseComplement

    s = """
<html>
<head>
  <title>Test results</title>
</head>

<body>
  <p>results!</p>
  <p>""" + req.form.getfirst('id','no id found?') + """</p>
</body>

</html>
"""

    """

    s = '<html>\n'
    s+= '<script language=JavaScript>\n\tvar _gaq = _gaq || [];\n\t_gaq.push([\'_setAccount\', \'UA-19292534-1\']);\n\t_gaq.push([\'_trackPageview\']);\n\t(function() {\n\t\tvar ga = document.createElement(\'script\');\n\t\tga.type = \'text/javascript\';\n\t\tga.async = true;\n\t\tga.src = (\'https:\' == document.location.protocol ? \'https://ssl\' : \'http://www\') + \'.google-analytics.com/ga.js\';\n\t\tvar s = document.getElementsByTagName(\'script\')[0];\n\t\ts.parentNode.insertBefore(ga, s);\n\t})();\n'
    s += 'function toggleVisible(id) {\n\tif (document.getElementById) {\n\t\tobj = document.getElementById(id);\n\t\tif (obj) {\n\t\t\tif (obj.style.display == \'none\') {\n\t\t\t\tobj.style.display = \'\'\n\t\t\t} else {\n\t\t\t\tobj.style.display = \'none\'\n\t\t\t}\n\t\t}\n\t}\n}\n'
    s += '</script>\n<style>\n\tbody { font-family: arial, sans-serif; }\n</style>\n</head>'
    s+= '<body bgcolor=\'#333333\' link=\'cc0000\' vlink=\'cc0000\'><center><table bgcolor=\'#999966\' cellpadding=\'10%\'><tr><td><center>'
    for pssm1 in weederPSSMs1:
        s += '<table width=\'100%\' cellpadding=\'15%\'><tr><td align=\'center\' valign=\'center\' bgcolor=\'#333333\'><font size=6><b><font color=\'#ff0000\'>miR</font><font color=\'#cccc00\'>vestigator Framework Results</font></b></font></a></td></tr>'
        s += '<p><table width=\'100%\'cellpadding=\'15%\'><tr><td align=\'center\' valign=\'center\' bgcolor=\'#333333\'><a href="#results" onclick="toggleVisible(\'results\'); return false;" style=\'color: rgb(204,204,0); text-decoration: none\'><font size=4><b><font color=\'#cccc00\'>'
        if not topRet=='all':
            s += 'Top <font color=\'#ff0000\' size=4>'+str(topRet)+'</font>'
        elif topRet=='all':
            s += '<font color=\'#ff0000\' size=4>All</font>'
        s += ' miRNAS Matching the Weeder Motif</font> <font color=\'#ff0000\'>'+str(pssm1.getName())+'</font> &nbsp; <font color="#ff0000">[?]</font></b></font></a></td></tr>\n'
        s += '<tr id="results" style="display: none;" width=600><td bgcolor="#333333"><font color="#ffffff">\n'
        s += '<b>What do the columns mean?</b> <p><ul><li><b>miRNA Name</b> = The name of the name(s) for the unique seed sequence. There may be more than one miRNA annotated for a unique seed seqeunce because they vary in the 3\' terminus of the mature miRNA. Each miRNA is a link to it\'s entry on <a href="http://www.mirbase.org" style="color: rgb(204,204,0)" target="_blank">miRBase</a></li>&nbsp;</br> <li><b>miRNA Seed</b> = The sequence for seed that aligned best to the over-represetned motif. The seed will be as long as the seed model described in the next column.</li>&nbsp;</br> <li><b>Seed Model</b> = Base-pairing models for the seed regions of a miRNA to the 3\' UTR of target transcripts. The 8mer, 7mer-m8, and 7mer-a1 models are the canonical models of miRNA to mRNA base-pairing. The 6mer models are considered marginal models as they typically have a reduced efficacy and are more likely to occur by chance alone. By default all of the seed models are used. The seed models are described in this figure:</br>&nbsp;</br><center><img src="http://mirvestigator.systemsbiology.net/seedModels.gif" width=400></center></li>&nbsp;</br><li><b>Length of Alignment</b> = The length of matching (or wobble if enabled) base-pairs that align between the sequence motif and the miRNA seed sequence.</li>&nbsp;</br> <li><b>Alignment</b> = The alignment of the over-represented sequence motif on top 5\'&rArr;3\' to the miRNA seed sequence given the seed model 3\'&rArr;5\'. (<b>Note:</b> <span style=\'background-color: rgb(255,255,255);\'>&nbsp;<b><font color="#ff0000">|</font></b>&nbsp;</span> = a match, <span style=\'background-color: rgb(255,255,255);\'>&nbsp;<b><font color="#0000ff">:</font></b>&nbsp;</span> = a wobble, <span style=\'background-color: rgb(255,255,255);\'><font color="#000000">"</font> <font color="#000000">"</font></span> (space) = not a match, and for the seqeucnes <span style=\'background-color: rgb(255,255,255);\'>&nbsp;<b><font color="#cccccc">-</font></b>&nbsp;</span> = a gapping at the start or end.)</li>&nbsp;</br> <li><b>Viterbi P-Value</b> = Significance of match between the over-represented sequence motif and the miRNA seed sequence. (<b>Note:</b> A perfect match for an 8mer seed model is 1.5e-05, for a 7mer seed model 6.1e-05, and for a 6mer seed model 0.00024.)</li></ul> <b>What is considered a good match?</b> <p>This will depend upon your data and what downstream analysis you plan to do with it. But a good rule of thumb is that if you find a perfect match for a 7mer or 8mer (Viterbi P-Value = <font color="#ff0000"><b>6.1e-05</b></font> and <font color="#ff0000"><b>1.5e-05</b></font>; respectively) this is likely to be of interest. Follow up with experimental studies will help to determine the false discovery rate for your dataset.</p></font></td></tr>'
        s += '</table>'
        scoreList = mV.getScoreList(pssm1.getName())
        if topRet=='all':
            topRet = len(scoreList)
        else:
            topRet = int(topRet)
        s += '<table width=\'100%\' cellpadding=\'15%\'><tr><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>miRNA Name</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>miRNA Seed</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>Seed Model</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>Length of</br>Alignment</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>Alignment</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>Viterbi P-Value</font></b></center></td></tr>'
        for k in range(topRet):
            i = scoreList[k]
            align1 = alignSeed(i['statePath'], i['miRNA.seed'], pssm1.getName())
            s += '<tr><td bgcolor=\'#ffffff\'><center>'+str('</br>'.join(['<a href=\'http://mirbase.org/cgi-bin/mature.pl?mature_acc='+str(miRNADict[j.strip()])+'\' target=\'_blank\'>'+str(j.strip())+'</a>' for j in i['miRNA.name'].split('_')]))+'</center></td><td bgcolor=\'#ffffff\'><center>'+conv2rna(reverseComplement(str(i['miRNA.seed'])))+'</center></td><td bgcolor=\'#ffffff\'><center>'+str(i['model'])+'</center></td><td bgcolor=\'#ffffff\'><center>'+str(align1[3])+'</center></td><td bgcolor=\'#ffffff\'>'
            s += '<center><pre>'+str(align1[0])+'\n'+str(align1[1])+'\n'+str(align1[2])+'</pre></center>'
            s += '</td><td bgcolor=\'#ffffff\'><center>'+str('%.2g' % float(i['vitPValue']))+'</center></td></tr>'
        s += '</table></p>'
        #'gene':seqDict[splitUp[0]], 'strand':splitUp[1], 'site':splitUp[2], 'start':splitUp[3], 'match':splitUp[4].lstrip('(').rstrip(')')
        # pssm1.nsites
        s += '<p><table width=\'100%\' bgcolor=\'#333333\' cellpadding=\'15%\'><tr><td align=\'center\' valign=\'center\'><a href="#sites" onclick="toggleVisible(\'sites\'); return false;" style=\'color: rgb(204,204,0); text-decoration: none\'><font size=4><b><font color=\'#cccc00\'>Position of Putative miRNA Binding Sites in Submitted Genes</br>for the Weeder Motif</font> <font color=\'#ff0000\'>'+str(pssm1.getName())+'</font> &nbsp; <font color="#ff0000">[?]</font></b></font></a></td></tr>\n'
        s += '<tr id="sites" style="display: none;" width=600><td bgcolor="#333333"><font color="#ffffff">\n'
        s += '<b>Where do these sites come from?</b>\n<p>As part of the miRvestigator framework <a href="http://159.149.109.9/modtools/" style="color: rgb(204,204,0)" target="_blank">Weeder</a> provides predicted miRNA binging sites in the 3\' untranslated regions (UTRs) of the analyzed genes. Predicted binding sites were split into three different similarity bins:  <font color="#ff0000">High quality</font> - &#8805; 95% similarity to the miRNA seed sequence (red), <font color="#cccc00">Medium quality</font> 95% &#8805; similarity &#8805; 90% to the miRNA seed sequence (yellow), and <font color="#00ff00">Fair quality</font> 90% &#8805; similarity &#8805; 85% to the miRNA seed sequence (green). These sites can be used to develop follow-up experiments such as luciferase reporter assays to validate the efficacy of these sites.</p>\n<b>What do the columns mean?</b>\n<p><ul><li><b>Entrez Gene ID</b> = The NCBI Entrez gene identifier (ID) where this site resides. The Entrez gene ID is also a link to <a href="http://www.ncbi.nlm.nih.gov/gene" style="color: rgb(204,204,0)" target="_blank">NCBI gene database</a> entry for the specified gene.</li></br>&nbsp;</br>\n<li><b>Site</b> = The sequence for site identified by Weeder. If it is in square brackets indicates that the site is of lower similarity.</li></br>&nbsp;</br>\n<li><b>Start Relative to Stop Codon</b> = The 3\' UTR begins following the stop codon (which is set at 0 base-pairs (bp)). Thus the values in this column descirbe the start of the site in bp after the stop codon.</li></br>&nbsp;</br>\n<li><b>% Similarity to Consensus Motif</b> = The similarity of the predicted site to the consensus motif is computed as a percentage. Predicted binding sites were split into three different similarity to consensusbins:  <font color="#ff0000">High quality</font> - &#8805; 95% similarity to the miRNA seed sequence (red), <font color="#cccc00">Medium quality</font> 95% &#8805; similarity &#8805; 90% to the miRNA seed sequence (yellow), and <font color="#00ff00">Fair quality</font> 90% &#8805; similarity &#8805; 85% to the miRNA seed sequence (green).</li></ul></p>'
        s += '</font></td></td></table>'
        s += '<table width=\'100%\' cellpadding=\'15%\'><tr><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>Entrez Gene ID</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>Seqeunce of Site</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>Start Relative to</br>Stop Codon (bp)</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>% Similarity to Consensus Motif</br>(Quality = </font><font color=\'#cc0000\'>High</font><font color=\'#ffffff\'> | </font><font color=\'#cccc00\'>Medium</font><font color=\'#ffffff\'> | </font><font color=\'#00cc00\'>Fair</font><font color=\'#ffffff\'>)</font></b></center></td></tr>'
        for i in pssm1.nsites:
            col1 = '#000000'
            if float(i['match']) >= float(95):
                col1 = '#cc0000'
            elif float(i['match']) >= float(90):
                col1 = '#cccc00'
            elif float(i['match']) >= float(85):
                col1 = '#00cc00'
            s += '<tr><td bgcolor=\'#ffffff\'><center>'+str('<a href=\'http://www.ncbi.nlm.nih.gov/gene/'+str(i['gene'])+'\' target=\'_blank\'>'+str(i['gene'])+'</a>')+'</center></td><td bgcolor=\'#ffffff\'><center>'+str(i['site'])+'</center></td><td bgcolor=\'#ffffff\'><center>'+str(i['start'])+'</center></td><td bgcolor=\'#ffffff\'><font color=\''+str(col1)+'\'><center><b>'+i['match']+'</b></center></font></td></tr>'
        s += '</table></p>'
    s += '<p><table width=\'100%\' cellpadding=\'5%\'><tr><td bgcolor=\'#c0c0c0\'><center>Need help? Please contact <font color=\'#0000ff\'>cplaisier(at)systemsbiology.org</font> if you have any questions, comments or concerns.<br>Developed at the <a href=\'http://www.systemsbiology.org\' target=\'_blank\' style=\'color: rgb(0,0,255)\'>Institute for Systems Biology</a> in the <a href=\'http://baliga.systemsbiology.net/\' target=\'_blank\' style=\'color: rgb(0,0,255)\'>Baliga Lab</a>.</center></td></tr></table></p>'
    s += '</center></td></tr></table></center></body></html>'
    """
    return s





# Please wait while we churn the butter...
def plsWait(req):
    # Get the variables
    out = req.form.getfirst('genes','').strip()
    genes = []
    for i in out.split('\n'):
        for j in i.strip().split('\r'):
            for k in j.strip().split(','):
                for l in k.strip().split('\t'):
                    for m in l.strip().split(' '):
                        if m:
                            genes.append(l)
    s6 = str(req.form.getfirst('seedModel_6',''))
    s7 = str(req.form.getfirst('seedModel_7',''))
    s8 = str(req.form.getfirst('seedModel_8',''))
    bgModel = str(req.form.getfirst('bgModel',''))
    wobble = str(req.form.getfirst('wobble',''))
    cut = str(req.form.getfirst('cut',''))
    m6 = str(req.form.getfirst('motif_6',''))
    m8 = str(req.form.getfirst('motif_8',''))
    topRet = str(req.form.getfirst('topRet',''))
    jobName = str(req.form.getfirst('jobName',''))
    #return out, s6, s7, s8, bgModel, wobble, cut, m6, m8
    seedModels = []
    if not s6=='' and int(s6)==6:
        seedModels += ['6mer']
    if not s7=='' and int(s7)==7:
        seedModels += ['7mer']
    if not s8=='' and int(s8)==8:
        seedModels += ['8mer']
    motifSizes = []
    if not m6=='' and int(m6)==6:
        motifSizes += ['6bp']
    if not m8=='' and int(m8)==8:
        motifSizes += ['8bp']
    if wobble=='yes':
        wobble1 = ''
    else:
        wobble1 = ' not'
    blab = ''
    if bgModel=='HS':
        blab = 'Default Weeder Model'
    elif bgModel=='HS3P':
        blab = '3\' UTR Specific Model'
    s = "<html>\n<head>\n<style>\n\tbody { font-family: arial, sans-serif; }\n</style>\n<script language=JavaScript>\n\tvar _gaq = _gaq || [];\n\t_gaq.push(['_setAccount', 'UA-19292534-1']);\n\t_gaq.push(['_trackPageview']);\n\t(function() {\n\t\tvar ga = document.createElement('script');\n\t\tga.type = 'text/javascript';\n\t\tga.async = true;\n\t\tga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';\n\t\tvar s = document.getElementsByTagName('script')[0];\n\t\ts.parentNode.insertBefore(ga, s);\n\t})();\n</script>\n"
    s+= "<meta http-equiv=refresh content='0; URL=doit?s6="+s6+"&s7="+s7+"&s8="+s8+"&genes="+','.join([i for i in genes if i])+"&bgModel="+bgModel+"&wobble="+wobble+"&cut="+cut+"&m6="+m6+"&m8="+m8+"&jobName="+jobName+"&topRet="+str(topRet)+"'>\n</head>\n"
    s += "<body bgcolor='#333333'>\n<center><table width=620 bgcolor='#999966' cellpadding='10%'>\n\t<tr><td><center><table width='100%' cellpadding='15%'><tr><td align='center' valign='center' bgcolor='#000000'><font size=6><b><font color='#ff0000'>miR</font><font color='#cccc00'>vestigator Framework</font></b></font></td></tr>\n</table><table width='100%' cellpadding='10%'><tr><td bgcolor='#333333'><center><b><font color='#cccc00' size=5>Parameters for Run"
    if not jobName=='':
        s += " on <font color='#ff0000'>"+str(jobName)+"</font>"
    s+= "</font></b></center><p><center><table width='100%' bgcolor='#ffffff' cellpadding='5%'><tr><td><center><b><p>Thank you for submitting <font color='#ff0000'>"+str(len(genes))+" genes</font> for analysis.</p> <p>You requested that Weeder be run with <font color='#ff0000'>"+str(motifSizes)+"</font> motif size(s) and the <font color='#ff0000'>"+str(blab)+"</font> background model.</p><p>The miRvestigator HMM will use <font color='#ff0000'>"+str(seedModels)+" seed model(s)</font> and <font color='#ff0000'>will"+wobble1+" </font> model wobble base pairing.</p><p>Returning <font color='#ff0000'>"+topRet+"</font> top miRNAs.</p></center></td></tr></table></center><p><center><p><font color='#cccc00' size=5>Please wait while your request is processed...</font></p></b></font></br><img src='http://spero.systemsbiology.net/miRvestigator/Scientists.gif'></center></td></tr></table></center><p><table width='100%' cellpadding='5%'><tr><td bgcolor='#c0c0c0'><center>Need help? Please contact <font color='#0000ff'>cplaisier(at)systemsbiology.org</font> if you have any questions, comments or concerns.<br>Developed at the <a href='http://www.systemsbiology.org' target='_blank' style=\'color: rgb(0,0,255)\'>Institute for Systems Biology</a> in the <a href='http://baliga.systemsbiology.net/' target='_blank' style=\'color: rgb(0,0,255)\'>Baliga Lab</a>.</center></td></tr></table></p></td></tr></table></center>\n</body>"
    req.content_type='text/html'
    return s

# Then run the job 
def doit(req):
    import Pyro.core
    uriFile = open('/var/www/uri','r')
    uri = uriFile.readline().strip()
    uriFile.close()
    miRwww = Pyro.core.getProxyForURI(uri)
    #miRwww = Pyro.core.getProxyForURI('PYRO://127.0.0.1:7767/7f00000111d81dfa634e7335080d868a2f')
    Pyro.core.initClient()
    data = util.FieldStorage(req)
    out = data['genes'].strip()
    if 's6' in data:
        s6 = int(data['s6'])
    else:
        s6 = ''
    if 's7' in data:
        s7 = int(data['s7'])
    else:
        s7 = ''
    if 's8' in data:
        s8 = int(data['s8'])
    else:
        s8 = ''
    bgModel = str(data['bgModel'])
    wobble = str(data['wobble'])
    cut = float(data['cut'])
    if 'm6' in data:
        m6 = int(data['m6'])
    else:
        m6 = ''
    if 'm8' in data:
        m8 = int(data['m8'])
    else:
        m8 = ''
    jobName = str(data['jobName'])
    topRet = data['topRet']
    """
    out = req.form.getfirst('genes','').strip()
    s6 = req.form.getfirst('seedModel_6','')
    s7 = req.form.getfirst('seedModel_7','')
    s8 = req.form.getfirst('seedModel_8','')
    bgModel = str(req.form.getfirst('bgModel',''))
    wobble = str(req.form.getfirst('wobble',''))
    cut = float(req.form.getfirst('cut',''))
    m6 = req.form.getfirst('motif_6','')
    m8 = req.form.getfirst('motif_8','')
    """
    #return out, s6, s7, s8, bgModel, wobble, cut, m6, m8
    seedModels = []
    if not s6=='' and int(s6)==6:
        seedModels += [6]
    if not s7=='' and int(s7)==7:
        seedModels += [7]
    if not s8=='' and int(s8)==8:
        seedModels += [8]
    motifSizes = []
    if not m6=='' and int(m6)==6:
        motifSizes += [6]
    if not m8=='' and int(m8)==8:
        motifSizes += [8]
    if wobble=='yes':
        wobble = True
    else:
        wobble = False
    genes = []
    for i in out.split('\n'):
        for j in i.strip().split('\r'):
            for k in j.strip().split(','):
                for l in k.strip().split('\t'):
                    for m in l.strip().split(' '):
                        if m:
                            genes.append(l)
    scoreList = miRwww.run(genes, seedModels, wobble, cut, bgModel, motifSizes, jobName, topRet)
    return scoreList

