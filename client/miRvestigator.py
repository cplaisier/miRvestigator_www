from mod_python import apache
from mod_python import util
import re
import sys
import traceback
import datetime
import json
import Pyro.core
from Pyro.errors import ProtocolError
from mirv_db import get_job_status, read_parameters, read_motifs, read_mirvestigator_scores
import admin_emailer


adminEmailer = admin_emailer.AdminEmailer()


# Reverse complement
def reverseComplement(seq):
    seq = list(seq)
    seq.reverse()
    return ''.join(complement(seq))

# Complement
def complement(seq):
    complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C', 'N':'N', 'U':'A'}
    complseq = [complement[base] for base in seq]
    return complseq

# Convert to RNA
def conv2rna(seq):
    conversion = {'A':'A', 'T':'U', 'C':'C', 'G':'G', 'N':'N', 'U':'U'}
    rnaSeq = [conversion[base] for base in list(seq)]
    return ''.join(rnaSeq)


def alignSeed(alignment, seed, motif):
    alignment.pop() # Get rid of the extra state which is added by the forwardViterbi function
    start = 1    
    if alignment[0]=='NM1':
        for i in alignment:
            if i=='NM1':
                start += 1
    # Alignment
    motifAlign = '<font color=\'#CC0000\'><b>Motif</b></font><font color=\'#ffffff\'>_</font>5\'<font color=\'#ffffff\'>_</font>'
    seed = list(conv2rna(complement(seed)))
    seedAlign = '<font color=\'#ffffff\'>______</font>3\'<font color=\'#ffffff\'>_</font>'
    motif = list(conv2rna(motif))
    alignMe = alignment
    aligned = '<font color=\'#ffffff\'>_________</font>'
    lenMatch = 0
    # First get them zero'd to the same point
    if start>1:
        for i in range(start-1):
            seedAlign += seed.pop(0)
            aligned += '<font color=\'#ffffff\'>_</font>'
            motifAlign += '-'
            alignMe.pop(0)
    if len(alignMe)>0 and not alignMe[0]=='PSSM0' and not alignMe[0]=='WOBBLE0':
        if alignMe[0][0]=='P':
            upTo = int(alignMe[0][4])
        elif alignMe[0][0]=='W':
            upTo = int(alignMe[0][6])
        for i in range(upTo):
            seedAlign += '<font color=\'#cccccc\'>-</font>'
            aligned += '<font color=\'#ffffff\'>_</font>'
            motifAlign += motif.pop(0)
    # Then add the parts that align
    while 1:
        if len(alignMe)==0 or alignMe[0]=='NM2':
            break
        seedAlign += seed.pop(0)
        if alignMe[0][0]=='P':
            aligned += '<font color=\'#ff0000\'>|</font>'
        elif alignMe[0][0]=='W':
            aligned += '<font color=\'#0000ff\'>:</font>'
        lenMatch += 1
        motifAlign += motif.pop(0)
        alignMe.pop(0)
    # Then do the ending
    if len(alignMe)>0:
        for i in alignMe:
            seedAlign += seed[0]
            seed = seed[1:]
            aligned += '<font color=\'#ffffff\'>_</font>'
            motifAlign += '<font color=\'#cccccc\'>-</font>'
        alignMe = []
    if len(motif)>0 and len(alignMe)==0:
        for i in motif:
            seedAlign += '<font color=\'#cccccc\'>-</font>'
            aligned += '<font color=\'#ffffff\'>_</font>'
            motifAlign += i
    motifAlign += '<font color=\'#ffffff\'>_</font>3\'<font color=\'#ffffff\'>___________</font>'
    aligned +=    '<font color=\'#ffffff\'>______________</font>'
    seedAlign +=  '<font color=\'#ffffff\'>_</font>5\'<font color=\'#ffffff\'>_</font><font color=\'#cc0000\'><b>miRNA Seed</b></font>'
    return [motifAlign, aligned, seedAlign, lenMatch]





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
    job['notify_mail'] = str(req.form.getfirst('notify_mail',None))

    try:
        # connect to miR server via Pyro
        uriFile = open('/var/www/uri','r')
        uri = uriFile.readline().strip()
        uriFile.close()
        miR_server = Pyro.core.getProxyForURI(uri)
        Pyro.core.initClient()

        # submit job to server process and redirect to status page
        job_id = miR_server.submit_job(job)
    except ProtocolError as e:
        traceback.print_stack()
        traceback.print_exc()
        sys.stderr.flush()
        adminEmailer.warn("miRvestigator server is unreachable: \n\n" + str(e))
        util.redirect(req, req.construct_url("/error"))
        return
    except Exception as e:
        traceback.print_stack()
        traceback.print_exc()
        sys.stderr.flush()
        adminEmailer.warn("miRvestigator server error: \n\n" + str(sys.exc_info()[0]))
        util.redirect(req, req.construct_url("/error"))
        return

    util.redirect(req, req.construct_url("/status/%s/" % (job_id)))



# return a JSON string encoding job status
def status(req):
    id = str(req.form.getfirst('id',''))
    req.content_type='application/json'
    return json.dumps(get_job_status(id))

def parameters(req):
    id = str(req.form.getfirst('id',''))
    req.content_type='application/json'
    return json.dumps(read_parameters(id))
    

# display results
def results(req):
    # need weederPSSMs1
    # need topRet
    # need mV
    # miRNADict[j.strip()] ??
    # functions: conv2rna, reverseComplement
    id = str(req.form.getfirst('id',''))
    motifs = read_motifs(id)
    parameters = read_parameters(id)
    topRet = parameters['topRet']

    # read mirbase miRNAs so we can link back to mirbase
    import gzip
    miRNAFile = gzip.open('/home/ubuntu/miRwww_server/mature.fa.gz','r')
    miRNADict = {}
    while 1:
        miRNALine = miRNAFile.readline()
        seqLine = miRNAFile.readline()
        if not miRNALine:
            break
        # Get the miRNA name
        miRNAData = miRNALine.lstrip('>').split(' ')
        curMiRNA = miRNAData[0]
        if (curMiRNA.split('-'))[0]=='hsa':
            miRNADict[curMiRNA] = miRNAData[1]
    miRNAFile.close()

    s = '<html>\n'
    s+= '<head>'
    s+= '<title>miRvestigator Framework</title>\n'
    s+= '<script language=JavaScript>\n\tvar _gaq = _gaq || [];\n\t_gaq.push([\'_setAccount\', \'UA-19292534-1\']);\n\t_gaq.push([\'_trackPageview\']);\n\t(function() {\n\t\tvar ga = document.createElement(\'script\');\n\t\tga.type = \'text/javascript\';\n\t\tga.async = true;\n\t\tga.src = (\'https:\' == document.location.protocol ? \'https://ssl\' : \'http://www\') + \'.google-analytics.com/ga.js\';\n\t\tvar s = document.getElementsByTagName(\'script\')[0];\n\t\ts.parentNode.insertBefore(ga, s);\n\t})();\n'
    s += 'function toggleVisible(id) {\n\tif (document.getElementById) {\n\t\tobj = document.getElementById(id);\n\t\tif (obj) {\n\t\t\tif (obj.style.display == \'none\') {\n\t\t\t\tobj.style.display = \'\'\n\t\t\t} else {\n\t\t\t\tobj.style.display = \'none\'\n\t\t\t}\n\t\t}\n\t}\n}\n'
    s += '</script>\n<style>\n\tbody { font-family: arial, sans-serif; }\n</style>\n</head>'
    s+= '<body bgcolor=\'#333333\' link=\'cc0000\' vlink=\'cc0000\'><center><table bgcolor=\'#999966\' cellpadding=\'10%\'><tr><td><center>'
    for motif in motifs:
        s += '<table width=\'100%\' cellpadding=\'15%\'><tr><td align=\'center\' valign=\'center\' bgcolor=\'#333333\'><font size=6><b><font color=\'#ff0000\'>miR</font><font color=\'#cccc00\'>vestigator Framework Results</font></b></font></a></td></tr>'
        s += '<p><table width=\'100%\'cellpadding=\'15%\'><tr><td align=\'center\' valign=\'center\' bgcolor=\'#333333\'><a href="#results" onclick="toggleVisible(\'results\'); return false;" style=\'color: rgb(204,204,0); text-decoration: none\'><font size=4><b><font color=\'#cccc00\'>'
        if not topRet=='all':
            s += 'Top <font color=\'#ff0000\' size=4>'+str(topRet)+'</font>'
        elif topRet=='all':
            s += '<font color=\'#ff0000\' size=4>All</font>'
        s += ' miRNAS Matching the Weeder Motif</font> <font color=\'#ff0000\'>'+motif['name']+'</font> &nbsp; <font color="#ff0000">[?]</font></b></font></a></td></tr>\n'
        s += '<tr id="results" style="display: none;" width=600><td bgcolor="#333333"><font color="#ffffff">\n'
        s += '<b>What do the columns mean?</b> <p><ul><li><b>miRNA Name</b> = The name of the name(s) for the unique seed sequence. There may be more than one miRNA annotated for a unique seed seqeunce because they vary in the 3\' terminus of the mature miRNA. Each miRNA is a link to it\'s entry on <a href="http://www.mirbase.org" style="color: rgb(204,204,0)" target="_blank">miRBase</a></li>&nbsp;</br> <li><b>miRNA Seed</b> = The sequence for seed that aligned best to the over-represetned motif. The seed will be as long as the seed model described in the next column.</li>&nbsp;</br> <li><b>Seed Model</b> = Base-pairing models for the seed regions of a miRNA to the 3\' UTR of target transcripts. The 8mer, 7mer-m8, and 7mer-a1 models are the canonical models of miRNA to mRNA base-pairing. The 6mer models are considered marginal models as they typically have a reduced efficacy and are more likely to occur by chance alone. By default all of the seed models are used. The seed models are described in this figure:</br>&nbsp;</br><center><img src="http://mirvestigator.systemsbiology.net/seedModels.gif" width=400></center></li>&nbsp;</br><li><b>Length of Alignment</b> = The length of matching (or wobble if enabled) base-pairs that align between the sequence motif and the miRNA seed sequence.</li>&nbsp;</br> <li><b>Alignment</b> = The alignment of the over-represented sequence motif on top 5\'&rArr;3\' to the miRNA seed sequence given the seed model 3\'&rArr;5\'. (<b>Note:</b> <span style=\'background-color: rgb(255,255,255);\'>&nbsp;<b><font color="#ff0000">|</font></b>&nbsp;</span> = a match, <span style=\'background-color: rgb(255,255,255);\'>&nbsp;<b><font color="#0000ff">:</font></b>&nbsp;</span> = a wobble, <span style=\'background-color: rgb(255,255,255);\'><font color="#000000">"</font> <font color="#000000">"</font></span> (space) = not a match, and for the seqeucnes <span style=\'background-color: rgb(255,255,255);\'>&nbsp;<b><font color="#cccccc">-</font></b>&nbsp;</span> = a gapping at the start or end.)</li>&nbsp;</br> <li><b>Viterbi P-Value</b> = Significance of match between the over-represented sequence motif and the miRNA seed sequence. (<b>Note:</b> A perfect match for an 8mer seed model is 1.5e-05, for a 7mer seed model 6.1e-05, and for a 6mer seed model 0.00024.)</li></ul> <b>What is considered a good match?</b> <p>This will depend upon your data and what downstream analysis you plan to do with it. But a good rule of thumb is that if you find a perfect match for a 7mer or 8mer (Viterbi P-Value = <font color="#ff0000"><b>6.1e-05</b></font> and <font color="#ff0000"><b>1.5e-05</b></font>; respectively) this is likely to be of interest. Follow up with experimental studies will help to determine the false discovery rate for your dataset.</p></font></td></tr>'
        s += '</table>'
        
        scoreList = read_mirvestigator_scores(motif['motif_id'])
        if topRet=='all':
            topRet = len(scoreList)
        else:
            topRet = int(topRet)
        s += '<table width=\'100%\' cellpadding=\'15%\'><tr><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>miRNA Name</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>miRNA Seed</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>Seed Model</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>Length of</br>Alignment</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>Alignment</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>Viterbi P-Value</font></b></center></td></tr>'
        for k in range(topRet):
            i = scoreList[k]
            align1 = alignSeed(i['statePath'], i['miRNA.seed'], motif['name'])
            s += '<tr><td bgcolor=\'#ffffff\'><center>'+str('</br>'.join(['<a href=\'http://mirbase.org/cgi-bin/mature.pl?mature_acc='+str(miRNADict[j.strip()])+'\' target=\'_blank\'>'+str(j.strip())+'</a>' for j in i['miRNA.name'].split('_')]))+'</center></td><td bgcolor=\'#ffffff\'><center>'+conv2rna(reverseComplement(str(i['miRNA.seed'])))+'</center></td><td bgcolor=\'#ffffff\'><center>'+str(i['model'])+'</center></td><td bgcolor=\'#ffffff\'><center>'+str(align1[3])+'</center></td><td bgcolor=\'#ffffff\'>'
            s += '<center><pre>'+str(align1[0])+'\n'+str(align1[1])+'\n'+str(align1[2])+'</pre></center>'
            s += '</td><td bgcolor=\'#ffffff\'><center>'+str('%.2g' % float(i['vitPValue']))+'</center></td></tr>'
        s += '</table></p>'
        #'gene':seqDict[splitUp[0]], 'strand':splitUp[1], 'site':splitUp[2], 'start':splitUp[3], 'match':splitUp[4].lstrip('(').rstrip(')')
        # pssm1.nsites
        s += '<p><table width=\'100%\' bgcolor=\'#333333\' cellpadding=\'15%\'><tr><td align=\'center\' valign=\'center\'><a href="#sites" onclick="toggleVisible(\'sites\'); return false;" style=\'color: rgb(204,204,0); text-decoration: none\'><font size=4><b><font color=\'#cccc00\'>Position of Putative miRNA Binding Sites in Submitted Genes</br>for the Weeder Motif</font> <font color=\'#ff0000\'>'+motif['name']+'</font> &nbsp; <font color="#ff0000">[?]</font></b></font></a></td></tr>\n'
        s += '<tr id="sites" style="display: none;" width=600><td bgcolor="#333333"><font color="#ffffff">\n'
        s += '<b>Where do these sites come from?</b>\n<p>As part of the miRvestigator framework <a href="http://159.149.109.9/modtools/" style="color: rgb(204,204,0)" target="_blank">Weeder</a> provides predicted miRNA binging sites in the 3\' untranslated regions (UTRs) of the analyzed genes. Predicted binding sites were split into three different similarity bins:  <font color="#ff0000">High quality</font> - &#8805; 95% similarity to the miRNA seed sequence (red), <font color="#cccc00">Medium quality</font> 95% &#8805; similarity &#8805; 90% to the miRNA seed sequence (yellow), and <font color="#00ff00">Fair quality</font> 90% &#8805; similarity &#8805; 85% to the miRNA seed sequence (green). These sites can be used to develop follow-up experiments such as luciferase reporter assays to validate the efficacy of these sites.</p>\n<b>What do the columns mean?</b>\n<p><ul><li><b>Entrez Gene ID</b> = The NCBI Entrez gene identifier (ID) where this site resides. The Entrez gene ID is also a link to <a href="http://www.ncbi.nlm.nih.gov/gene" style="color: rgb(204,204,0)" target="_blank">NCBI gene database</a> entry for the specified gene.</li></br>&nbsp;</br>\n<li><b>Site</b> = The sequence for site identified by Weeder. If it is in square brackets indicates that the site is of lower similarity.</li></br>&nbsp;</br>\n<li><b>Start Relative to Stop Codon</b> = The 3\' UTR begins following the stop codon (which is set at 0 base-pairs (bp)). Thus the values in this column descirbe the start of the site in bp after the stop codon.</li></br>&nbsp;</br>\n<li><b>% Similarity to Consensus Motif</b> = The similarity of the predicted site to the consensus motif is computed as a percentage. Predicted binding sites were split into three different similarity to consensusbins:  <font color="#ff0000">High quality</font> - &#8805; 95% similarity to the miRNA seed sequence (red), <font color="#cccc00">Medium quality</font> 95% &#8805; similarity &#8805; 90% to the miRNA seed sequence (yellow), and <font color="#00ff00">Fair quality</font> 90% &#8805; similarity &#8805; 85% to the miRNA seed sequence (green).</li></ul></p>'
        s += '</font></td></td></table>'
        s += '<table width=\'100%\' cellpadding=\'15%\'><tr><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>Entrez Gene ID</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>Seqeunce of Site</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>Start Relative to</br>Stop Codon (bp)</font></b></center></td><td bgcolor=\'#333333\'><center><b><font color=\'#ffffff\'>% Similarity to Consensus Motif</br>(Quality = </font><font color=\'#cc0000\'>High</font><font color=\'#ffffff\'> | </font><font color=\'#cccc00\'>Medium</font><font color=\'#ffffff\'> | </font><font color=\'#00cc00\'>Fair</font><font color=\'#ffffff\'>)</font></b></center></td></tr>'
        for i in motif['sites']:
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
    return s

