#################################################################
# @Program: miRvestigator.py                                    #
# @Version: 1                                                   #
# @Author: Chris Plaisier                                       #
# @Sponsored by:                                                #
# Nitin Baliga, ISB                                             #
# Institute for Systems Biology                                 #
# 1441 North 34th Street                                        #
# Seattle, Washington  98103-8904                               #
# (216) 732-2139                                                #
# @Also Sponsored by:                                           #
# Luxembourg Systems Biology Grant                              #
#                                                               #
# If this program is used in your analysis please mention who   #
# built it. Thanks. :-)                                         #
#                                                               #
# Copyrighted by Chris Plaisier  10/23/2010                     #
#################################################################

from mod_python import apache
from mod_python import util

def index():
    s = """\
            <html>
            <head>
            <script language=JavaScript>
            function addMir9()
            {
                document.forms[0].genes.value="79073, 900, 29957, 11167, 4154, 84270, 84061, 4001, 26503, 4086, 51585, 4734, 5873"
                document.forms[0].bgModel.value='HS3P'
                document.forms[0].seedModel_6.value=6
                document.forms[0].seedModel_7.value=7
                document.forms[0].seedModel_8.value=8
                document.forms[0].wobble.value='no'
            }
            function addMir132()
            {
                document.forms[0].genes.value="23271, 51099, 1968, 5814, 1655, 4254, 5925, 5534, 1852, 1490, 4683, 5921, 7266, 8140, 8776, 2764, 4673, 9467, 2965, 3612, 3925, 4001, 4664, 10438, 642538, 642521, 642812, 8539, 6388, 25842, 23413, 27043, 22834, 23002, 23219, 25798, 730010, 60496, 25963, 26065, 51496, 51763, 6607, 6606, 54765, 23264, 55366, 55871, 644019, 79003, 90268, 139285, 145773, 150468, 219902, 51585, 23443, 757, 169200, 81555"
                document.forms[0].bgModel.value='HS'
                document.forms[0].seedModel_6.value=6
                document.forms[0].seedModel_7.value=7
                document.forms[0].seedModel_8.value=8
                document.forms[0].wobble.value='no'
            }
            function addMir16()
            {
                document.forms[0].genes.value="6867, 79960, 116224, 7465, 28987, 100132364, 996, 9874, 4603, 79751, 1352, 11059, 396, 23466, 6197, 5110, 10152, 80331, 127933, 79073, 113829, 4008, 6992, 22841, 29775, 79693, 55294, 54877, 127700, 6734, 23259, 10422, 3014, 55709, 55295, 9374, 4891, 1021, 8945, 3304, 3303, 167227, 79671, 51068, 51517, 2673, 127262, 2132, 1111, 26147, 51444, 80019, 8760, 64750, 9927, 90809, 23499, 9986, 6548, 220002, 23332, 54471, 203197, 653639, 11313, 10749, 84926, 4134, 613, 5193, 9371, 54443, 898, 84193, 9552, 25790, 26276, 55585, 121260, 54529, 55312, 56990, 60436, 83596, 6895, 143384, 54926, 7335, 730052, 387521, 387522, 55038, 56970, 64768, 9958, 55664, 79065, 10712, 638, 55317, 23294, 25847"
                document.forms[0].bgModel.value='HS'
                document.forms[0].seedModel_6.value=6
                document.forms[0].seedModel_7.value=7
                document.forms[0].seedModel_8.value=8
                document.forms[0].wobble.value='no'
            }
            function addMir184()
            {
                document.forms[0].genes.value="140576, 396, 4150, 197370, 1487, 8644, 9516, 1605, 993, 64837, 8613, 6455, 84876, 56262, 208, 100130776, 51299"
                document.forms[0].bgModel.value='HS'
                document.forms[0].seedModel_6.value=6
                document.forms[0].seedModel_7.value=7
                document.forms[0].seedModel_8.value=8
                document.forms[0].wobble.value='no'
            }
            function addMir1()
            {
                document.forms[0].genes.value="103, 302, 303, 304, 376, 767, 1652, 1875, 1939, 2079, 2697, 3021, 3400, 4201, 4580, 5201, 5226, 5440, 5756, 5867, 5928, 6391, 6422, 6457, 7114, 7295, 8407, 8624, 8655, 8683, 10244, 26123, 26578, 26580, 28985, 29058, 29078, 30850, 51175, 51465, 54780, 55276, 55315, 55744, 57446, 57696, 64425, 79022, 80306, 81671, 83787, 84278, 84747, 90522, 140809, 143458, 200916, 201562, 253512, 341306, 352909, 378464, 390498, 440151, 440388, 440921, 441454, 441456"
                document.forms[0].bgModel.value='HS'
                document.forms[0].seedModel_6.value=6
                document.forms[0].seedModel_7.value=7
                document.forms[0].seedModel_8.value=8
                document.forms[0].wobble.value='no'
            }
            function addMir142()
            {
                document.forms[0].genes.value="728607, 63905, 7259, 57179, 81831, 79751, 286148, 7324, 55740, 3685, 56902, 6924, 57181, 770, 1073, 1783, 9522, 54502, 8658, 22841, 1525, 646243, 23142, 9698, 51430, 6856, 3632, 6502, 54906, 23406, 4891, 285636, 7181, 3093, 1605, 10434, 481, 7003, 5718, 84925, 4082, 9475, 3209, 5693, 7525, 10552, 23673, 80267, 93621, 2803, 2800, 79042, 5756, 6120, 729020, 26273, 6309, 55852, 54443, 5879, 55327, 57045, 84159, 64710, 2295, 55038, 91272, 54964, 22836, 93380, 84458, 7046, 6097, 50862, 134553, 252983, 9069, 284611, 84312, 148867, 80854"
                document.forms[0].bgModel.value='HS'
                document.forms[0].seedModel_6.value=6
                document.forms[0].seedModel_7.value=7
                document.forms[0].seedModel_8.value=8
                document.forms[0].wobble.value='no'
            }
            </script>
            </head>
            
            <body bgcolor='#333333' link='#ffcc00' vlink='#ffcc00'>
            <font face='arial'><center>
            <table width=620 bgcolor='#999966' cellpadding='10%'><tr><td><center>
            <table width=600 bgcolor='#333333' cellpadding='15%'><tr><td align='center' valign='center'><font size=6><b><font color='#ff0000'>miR</font><font color='#cccc00'>vestigator Framework</font></b></font></td></tr></table>
            <p><form action='miRvestigator.py/plsWait' method='post'>
            <table cellpadding='5%' cellspacing=3 width='100%'>
            <tr><td bgcolor='#000000' colspan=2><font color='#cccc00' size=4><b><center>Enter Co-Expressed Gene List</center></b></font></td></tr>
            <tr><td colspan=2 bgcolor='#333333'><b><font color='#ffffff'>Enter Entrez IDs for the co-expressed genes:</font></b></br><font color='#ffffff'>(Any format is acceptable: comma, space, tab or newline delimited)</font></td></tr>
            <tr><td colspan=2 bgcolor='#666666'><center><textarea rows=20 cols=70 name='genes'></textarea></center></td></tr>
            <tr><td bgcolor='#333333'><center><font color='#ffffff'><b>Or load sample data:</b></font></center></td><td bgcolor='#666666'><table width='100%' cellpadding='5%'><tr><td bgcolor='#ffffff'><center><input type='button' value='hsa-miR-1' onClick='javascript:addMir1()'></center></td><td bgcolor='#ffffff'><center><input type='button' value='hsa-miR-9' onClick='javascript:addMir9()'></center></td><td bgcolor='#ffffff'><center><input type='button' value='hsa-miR-16' onClick='javascript:addMir16()'></center></td></tr>
            <tr><td bgcolor='#ffffff'><center><input type='button' value='hsa-miR-132' onClick='javascript:addMir132()'></center></td><td bgcolor='#ffffff'><center><input type='button' value='hsa-miR-142-3p' onClick='javascript:addMir142()'></center></td><td bgcolor='#ffffff'><center><input type='button' value='hsa-miR-184' onClick='javascript:addMir184()'></center></td></tr>
            </table></td></tr>
            <tr><td><td></tr>
            <tr><td bgcolor='#000000' colspan=2><font color='#cccc00' size=4><b><center>Parameters for Weeder</center></b></font></td></tr>
            <tr><td bgcolor='#333333'><b><center><font color='#ffffff'>Motif Sizes:</font></center></b></td><td bgcolor='#666666'><table cellpadding='5%' width='100%'><tr><td bgcolor='#ffffff'><center><b>6bp</b> <input type='checkbox' name='motif_6' value=6></input></center></td><td bgcolor='#ffffff'><center><b>8bp</b> <input type='checkbox' name='motif_8' value=8 checked></input></center></td></tr></table></td></tr>
            <tr><td bgcolor='#333333'><b><center><font color='#ffffff'>Background Model:</font></center></b></td><td bgcolor='#666666'><table width=100%><tr><td bgcolor='#ffffff'><center><select name='bgModel'><option value='HS' selected>Default Weeder Model</option><option value='HS3P'>3' UTR Specific Model</option></select></center></td></tr></table></td></tr>
            <tr><td><td></tr>
            <tr><td bgcolor='#000000' colspan=2><font color='#cccc00' size=4><b><center>Parameters for miRvestigator HMM</center></b></font></td></tr>
            <tr><td bgcolor='#333333'><center><b><font color='#ffffff'>Seed Models:</font></b></center></td><td bgcolor='#666666'><table cellpadding='5%' width='100%'><tr><td bgcolor='#ffffff'><b>6mer</b> <input type='checkbox' name='seedModel_6' value=6 checked></input></td><td bgcolor='#ffffff'><b>7mer</b> <input type='checkbox' name='seedModel_7' value=7 checked></input></td><td bgcolor='#ffffff'><b>8mer</b> <input type='checkbox' name='seedModel_8' value=8 checked></input></td></tr></table></td></tr>
            <tr><td bgcolor='#333333'><b><center><font color='#ffffff'>Model Wobble Base-Pairing:</font></center></b></td><td bgcolor='#666666'><table width='100%' cellpadding='5%'><tr><td bgcolor='#ffffff'><center><b>Yes</b><input type='radio' name='wobble' value='yes'></input> <b>No</b><input type='radio' name='wobble' value='no' checked></input></center></td><td bgcolor='#ffffff'><center><b>Min. Freq. of G or U:</b> <input type='text' name='cut' value='0.25' size=1></input></center></td></tr></table></td></tr>
            <tr><td><td></tr>
            <tr><td bgcolor='#000000' colspan=2><center><font color='#cccc00' size=4><b>Submit the Job</b></font></center></b></font></td></tr>
            <tr><td bgcolor='#333333' colspan=2><center><table cellpadding='5%'><tr><td bgcolor='#ffffff'><input type='submit' value='         Submit         '></td></tr></table></center></tr></td></table>
            </form></p>
            
            <table width='100%' cellpadding='5%'><tr><td bgcolor='#c0c0c0'><center>Need help? Please contact <font color='#0000ff'>cplaisier(at)systemsbiology.org</font> if you have any questions, comments or concerns.<br>Developed at the <a href='http://www.systemsbiology.org' target='_blank' style=\'color: rgb(0,0,255)\'>Institute for Systems Biology</a> in the <a href='http://baliga.systemsbiology.net/' target='_blank' style=\'color: rgb(0,0,255)\'>Baliga Lab</a>.</center></td></tr></table>
            </center></td></tr></table>
            </center></font>
            </body></html>
        """
    return s

# </br><a href=''>Information about sample data.</a> - Need to add this back later.

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
    s = "<html><head><meta http-equiv=refresh content='0; URL=doit?s6="+s6+"&s7="+s7+"&s8="+s8+"&genes="+','.join([i for i in genes if i])+"&bgModel="+bgModel+"&wobble="+wobble+"&cut="+cut+"&m6="+m6+"&m8="+m8+"'></head>"
    s += "<body bgcolor='#333333'><font face='arial'><center><table width=620 bgcolor='#999966' cellpadding='10%'><tr><td><center><table width='100%' cellpadding='15%'><tr><td align='center' valign='center' bgcolor='#000000'><font size=6><b><font color='#ff0000'>miR</font><font color='#cccc00'>vestigator Framework</font></b></font></td></tr></table><table width='100%' cellpadding='10%'><tr><td bgcolor='#333333'><center><b><font color='#cccc00' size=5>Parameters for Run</font></b></center><p><center><table width='100%' bgcolor='#ffffff' cellpadding='5%'><tr><td><center><b><p>Thank you for submitting <font color='#ff0000'>"+str(len(genes))+" genes</font> for analysis.</p> <p>You requested that Weeder be run with <font color='#ff0000'>"+str(motifSizes)+"</font> motif size(s).</p><p>The miRvestigator HMM will use <font color='#ff0000'>"+str(seedModels)+" seed model(s)</font> and <font color='#ff0000'>will"+wobble1+" </font> model wobble base pairing.</p></center></td></tr></table></center><p><center><p><font color='#cccc00' size=5>Please wait while your request is processed...</font></p></b></font></br><img src='../Scientists.gif'></center></td></tr></table></center><p><table width='100%' cellpadding='5%'><tr><td bgcolor='#c0c0c0'><center>Need help? Please contact <font color='#0000ff'>cplaisier(at)systemsbiology.org</font> if you have any questions, comments or concerns.<br>Developed at the <a href='http://www.systemsbiology.org' target='_blank' style=\'color: rgb(0,0,255)\'>Institute for Systems Biology</a> in the <a href='http://baliga.systemsbiology.net/' target='_blank' style=\'color: rgb(0,0,255)\'>Baliga Lab</a>.</center></td></tr></table></p></td></tr></table></center></font></body>"
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
    scoreList = miRwww.run(genes, seedModels, wobble, cut, bgModel, motifSizes)
    return scoreList

