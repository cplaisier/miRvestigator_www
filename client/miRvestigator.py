from mod_python import apache
from mod_python import util
import re
import Pyro.core
import datetime
import MySQLdb


def index():
    s = """\
            <html>
            <head>
            <script language=JavaScript>
            function toggleVisible(id) {
                if (document.getElementById) {
                    obj = document.getElementById(id);
                    if (obj) {
                        if (obj.style.display == 'none') {
                            obj.style.display = ''
                        } else {
                            obj.style.display = 'none'
                        }
                    }
                }
            }
            var _gaq = _gaq || [];
            _gaq.push(['_setAccount', 'UA-19292534-1']);
            _gaq.push(['_trackPageview']);

            (function() {
                var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
                ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
                var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
            })();
            function addMir1()
            {
                document.forms[0].genes.value="103, 302, 303, 304, 376, 767, 1652, 1875, 1939, 2079, 2697, 3021, 3400, 4201, 4580, 5201, 5226, 5440, 5756, 5867, 5928, 6391, 6422, 6457, 7114, 7295, 8407, 8624, 8655, 8683, 10244, 26123, 26578, 26580, 28985, 29058, 29078, 30850, 51175, 51465, 54780, 55276, 55315, 55744, 57446, 57696, 64425, 79022, 80306, 81671, 83787, 84278, 84747, 90522, 140809, 143458, 200916, 201562, 253512, 341306, 352909, 378464, 390498, 440151, 440388, 440921, 441454, 441456"
                document.forms[0].bgModel.value='HS'
                document.forms[0].seedModel_6.value=6
                document.forms[0].seedModel_7.value=7
                document.forms[0].seedModel_8.value=8
                document.forms[0].wobble.value='no'
                document.forms[0].jobName.value='hsa-miR-1 (Sample)'
            }
            function addMir9()
            {
                document.forms[0].genes.value="79073, 900, 29957, 11167, 4154, 84270, 84061, 4001, 26503, 4086, 51585, 4734, 5873"
                document.forms[0].bgModel.value='HS3P'
                document.forms[0].seedModel_6.value=6
                document.forms[0].seedModel_7.value=7
                document.forms[0].seedModel_8.value=8
                document.forms[0].wobble.value='no'
                document.forms[0].jobName.value='hsa-miR-9 (Sample)'
            }
            function addMir16()
            {
                document.forms[0].genes.value="6867, 79960, 116224, 7465, 28987, 100132364, 996, 9874, 4603, 79751, 1352, 11059, 396, 23466, 6197, 5110, 10152, 80331, 127933, 79073, 113829, 4008, 6992, 22841, 29775, 79693, 55294, 54877, 127700, 6734, 23259, 10422, 3014, 55709, 55295, 9374, 4891, 1021, 8945, 3304, 3303, 167227, 79671, 51068, 51517, 2673, 127262, 2132, 1111, 26147, 51444, 80019, 8760, 64750, 9927, 90809, 23499, 9986, 6548, 220002, 23332, 54471, 203197, 653639, 11313, 10749, 84926, 4134, 613, 5193, 9371, 54443, 898, 84193, 9552, 25790, 26276, 55585, 121260, 54529, 55312, 56990, 60436, 83596, 6895, 143384, 54926, 7335, 730052, 387521, 387522, 55038, 56970, 64768, 9958, 55664, 79065, 10712, 638, 55317, 23294, 25847"
                document.forms[0].bgModel.value='HS'
                document.forms[0].seedModel_6.value=6
                document.forms[0].seedModel_7.value=7
                document.forms[0].seedModel_8.value=8
                document.forms[0].wobble.value='no'
                document.forms[0].jobName.value='hsa-miR-16 (Sample)'
            }
            function addMir132()
            {
                document.forms[0].genes.value="23271, 51099, 1968, 5814, 1655, 4254, 5925, 5534, 1852, 1490, 4683, 5921, 7266, 8140, 8776, 2764, 4673, 9467, 2965, 3612, 3925, 4001, 4664, 10438, 642538, 642521, 642812, 8539, 6388, 25842, 23413, 27043, 22834, 23002, 23219, 25798, 730010, 60496, 25963, 26065, 51496, 51763, 6607, 6606, 54765, 23264, 55366, 55871, 644019, 79003, 90268, 139285, 145773, 150468, 219902, 51585, 23443, 757, 169200, 81555"
                document.forms[0].bgModel.value='HS'
                document.forms[0].seedModel_6.value=6
                document.forms[0].seedModel_7.value=7
                document.forms[0].seedModel_8.value=8
                document.forms[0].wobble.value='no'
                document.forms[0].jobName.value='hsa-miR-132 (Sample)'
            }
            function addMir142()
            {
                document.forms[0].genes.value="728607, 63905, 7259, 57179, 81831, 79751, 286148, 7324, 55740, 3685, 56902, 6924, 57181, 770, 1073, 1783, 9522, 54502, 8658, 22841, 1525, 646243, 23142, 9698, 51430, 6856, 3632, 6502, 54906, 23406, 4891, 285636, 7181, 3093, 1605, 10434, 481, 7003, 5718, 84925, 4082, 9475, 3209, 5693, 7525, 10552, 23673, 80267, 93621, 2803, 2800, 79042, 5756, 6120, 729020, 26273, 6309, 55852, 54443, 5879, 55327, 57045, 84159, 64710, 2295, 55038, 91272, 54964, 22836, 93380, 84458, 7046, 6097, 50862, 134553, 252983, 9069, 284611, 84312, 148867, 80854"
                document.forms[0].bgModel.value='HS'
                document.forms[0].seedModel_6.value=6
                document.forms[0].seedModel_7.value=7
                document.forms[0].seedModel_8.value=8
                document.forms[0].wobble.value='no'
                document.forms[0].jobName.value='hsa-miR-142-3p (Sample)'
            }
            function addMir184()
            {
                document.forms[0].genes.value="140576, 396, 4150, 197370, 1487, 8644, 9516, 1605, 993, 64837, 8613, 6455, 84876, 56262, 208, 100130776, 51299"
                document.forms[0].bgModel.value='HS'
                document.forms[0].seedModel_6.value=6
                document.forms[0].seedModel_7.value=7
                document.forms[0].seedModel_8.value=8
                document.forms[0].wobble.value='no'
                document.forms[0].jobName.value='hsa-miR-184 (Sample)'
            }
            </script>
            <style>
            body { font-family: arial, sans-serif; }
            </style>
            <title>miRvestigator Framework: Detect the miRNAs Driving Co-Expression Signatures</title>
            </head>
            
            <body bgcolor='#333333' link='#ffcc00' vlink='#ffcc00'>
            <font face='arial'><center>
            <table width=620 bgcolor='#999966' cellpadding='10%'><tr><td><center>
            <table width=600 bgcolor='#333333' cellpadding='15%'><tr><td align='center' valign='center'><font size=6><b><font color='#ff0000'>miR</font><font color='#cccc00'>vestigator Framework</font></b></font></td></tr></table>
            <p><form action='miRvestigator.py/submitJob' method='post'>
            <table cellpadding='5%' cellspacing=3 width='100%'>
            <tr><td bgcolor='#000000' colspan=2><center><font color='#cccc00' size=4><a href="#whatIsMV" onclick="toggleVisible('whatIsMV'); return false;" style=\'color: rgb(204,204,0); text-decoration: none\'><b>What is the miRvestigator Framework? &nbsp; <font color="#ff0000">[?]</font></b></a></font></center></td></tr>
            <tr id="whatIsMV" style="display: none;"><td colspan=2 bgcolor='#333333'><font color='#ffffff'><p>The miRvestigator framework is designed to take as input a list of co-expressed genes and will return the most likely <a href='http://en.wikipedia.org/wiki/MicroRNA' style=\'color: rgb(204,204,0)\' target='_blank'>miRNA</a> regulating these genes. It does this by searching for over-represented sequence motifs in the <a href="http://en.wikipedia.org/wiki/3\'_UTR" style=\'color: rgb(204,204,0)\' target='_blank'>3' untranslated regions (UTRs)</a> of the genes using <a href='http://159.149.109.9/modtools/' style=\'color: rgb(204,204,0)\' target='_blank'>Weeder</a> and then comparing this to the miRNA seed sequences in <a href='http://www.mirbase.org' style=\'color: rgb(204,204,0)\' target='_blank'>miRBase</a> using our custom built <a href='http://github.com/cplaisier/miRvestigator/wiki/miRvestigator-hidden-Markov-Model-(HMM)' target='_blank' style=\'color: rgb(204,204,0)\'>miRvestigator hidden Markov model (HMM)</a>.</p></font></td></tr>
            <tr><td colspan=2></td><tr>
            <tr><td bgcolor='#000000' colspan=2><center><font color='#cccc00' size=4><a href="#geneList" onclick="toggleVisible('geneList'); return false;" style=\'color: rgb(204,204,0); text-decoration: none\'><b>Enter Co-Expressed Gene List &nbsp; <font color="#ff0000">[?]</font></b></a></font></center></td></tr>
            <tr id="geneList" style="display: none;"><td colspan=2 bgcolor='#333333'><font color='#ffffff'><b>What is gene Co-Expression?</b>
<p><a href='http://en.wikipedia.org/wiki/Post-transcriptional_regulation' style=\'color: rgb(204,204,0)\' target='_blank'>Post-transcriptional regulation</a> by a <a href='http://en.wikipedia.org/wiki/MicroRNA' style=\'color: rgb(204,204,0)\' target='_blank'>miRNA</a> is mediated through binding to complementary sequences in the <a href="http://en.wikipedia.org/wiki/3\'_UTR" style=\'color: rgb(204,204,0)\' target='_blank'>3\' untranslated regions (UTRs)</a> of transcripts and generates a biological context-specific signature of down-regulation for these transcripts, which is called a co-expression signature. Co-expression signatures observed in transcriptome studies are thus assumed to be of biological origins whereby the expression of genes are regulated by shared factors (transcription factors, miRNAs, genetics or enrivnmental factors). There are many methods available to identify co-expression signatures, and the miRvestigator framework does not bias toward any particular method.</p>
<b>What if I don't have Entrez gene identifiers (IDs)?</b>
<p>Currently the miRvestigator framework is able to take <a href='http://www.ncbi.nlm.nih.gov/gene' style=\'color: rgb(204,204,0)\' target='_blank'>Entrez gene IDs</a> as input. To convert any other type of identifier to Entrez gene IDs please use the <a href='http://david.abcc.ncifcrf.gov/home.jsp' style=\'color: rgb(204,204,0)\' target='_blank'>DAVID</a> bioinformatics resource <a href='http://david.abcc.ncifcrf.gov/conversion.jsp' style=\'color: rgb(204,204,0)\' target='_blank'>gene ID conversion tool</a>. The DAVID gene ID conversion tool has a great <a href='http://david.abcc.ncifcrf.gov/helps/conversion.html' style=\'color: rgb(204,204,0)\' target='_blank'>help page</a> please visit it if you have any questions.</p>
<b>What types of <a href='http://en.wikipedia.org/wiki/Delimiter' style=\'color: rgb(255,255,255)\' target='_blank'>delimiters</a> can be entered into the form?</b>
<p>You can enter the Entrez gene IDs separated by commas, spaces, tabs or <a href='http://en.wikipedia.org/wiki/Newline' style=\'color: rgb(204,204,0)\' target='_blank'>newlines</a>.</p></font></td></tr>
            <tr><td bgcolor='#333333'><b><center><font color='#ffffff'>Name the gene list:</font></center></b></td><td bgcolor='#666666'><table width='100%' cellpadding='5%'><tr><td bgcolor='#ffffff'><center><input type='text' name='jobName' size=50></center></td></tr></table></td></tr>
            <tr><td colspan=2 bgcolor='#333333'><b><font color='#ffffff'>Enter Entrez IDs for the co-expressed genes:</font></b></br><font color='#ffffff'>(Acceptable <a href='http://en.wikipedia.org/wiki/Delimiter' style=\'color: rgb(204,204,0)\' target='_blank'>delimiters</a> include: comma, space, tab or newline)</font></td></tr>
            <tr><td colspan=2 bgcolor='#666666'><center><textarea rows=20 cols=70 name='genes'></textarea></center></td></tr>
            <tr><td bgcolor='#333333'><center><a href="#sampData" onclick="toggleVisible('sampData'); return false;" style=\'color: rgb(255,255,255); text-decoration: none\'><b><font color='#ffffff'><b>Or load sample data:</b></font> <font color="#ff0000">[?]</font></a></center></td><td bgcolor='#666666'><table width='100%' cellpadding='5%'><tr><td bgcolor='#ffffff'><center><input type='button' value='hsa-miR-1' onClick='javascript:addMir1()'></center></td><td bgcolor='#ffffff'><center><input type='button' value='hsa-miR-9' onClick='javascript:addMir9()'></center></td><td bgcolor='#ffffff'><center><input type='button' value='hsa-miR-16' onClick='javascript:addMir16()'></center></td></tr>
            <tr><td bgcolor='#ffffff'><center><input type='button' value='hsa-miR-132' onClick='javascript:addMir132()'></center></td><td bgcolor='#ffffff'><center><input type='button' value='hsa-miR-142-3p' onClick='javascript:addMir142()'></center></td><td bgcolor='#ffffff'><center><input type='button' value='hsa-miR-184' onClick='javascript:addMir184()'></center></td></tr>
            </table></td></tr>
            <tr id="sampData" style="display: none;"><td colspan=2 bgcolor='#333333'><font color='#ffffff'>
            <b>Where does the sample data come from?</b><p>Sample data are co-expression signatures reduced to Entrez ID gene lists from studies where a miRNA was experimentally perturbed and the resultant effect ascertained by transcriptome measurements (e.g. gene expression microarray).</p>
            <ul><li><a href='http://www.mirbase.org/cgi-bin/mature.pl?mature_acc=MIMAT0000416' style='color: rgb(204,204,0)' target='_blank'><b>hsa-miR-1</b></a> - The HEK293T human embryonic kidney cell line with FLAG-Ago2 was transfected with and without exogenous miRNA. Genes significantly enriched (1% local FDR) in the co-immunoprecipitates of the FLAG-Ago2 transfected cell lines where the miRNA was included were considered targets of the miRNA.<p><a href='http://www.ncbi.nlm.nih.gov/pubmed/18461144' target='_blank' style='color: rgb(255,255,204)'>Hendrickson, D.G., Hogan, D.J., Herschlag, D., Ferrell, J.E. & Brown, P.O. Systematic identification of mRNAs recruited to argonaute 2 by specific microRNAs and corresponding changes in transcript abundance. <i>PLoS ONE</i> <b>3</b>, e2126 (2008).</a></p></li>
            <li><a href='http://www.mirbase.org/cgi-bin/mature.pl?mature_acc=MIMAT0000441' style='color: rgb(204,204,0)' target='_blank'><b>hsa-miR-9</b></a> - Only genes exceeding median expression in at least half of the experiments were assayed for differential expression. Differential expression (P-value &lt; 0.001) was required to be consistently observed at both the 12 hour and 24 hour time points after miRNA transfection in HeLa cells. This dataset was reanalyzed from data in GEO data repository GSE8501 using the specification in the publication stated above to identify perturbed miRNA target genes.<p><a href='http://www.ncbi.nlm.nih.gov/pubmed/17612493' target='_blank' style='color: rgb(255,255,204)'>Grimson, A. et al. MicroRNA targeting specificity in mammals: determinants beyond seed pairing. <i>Mol. Cell</i> <b>27</b>, 91-105 (2007).</a></p></li>
            <li><a href='http://www.mirbase.org/cgi-bin/mature.pl?mature_acc=MIMAT0000069' style='color: rgb(204,204,0)' target='_blank'><b>hsa-miR-16</b></a> - Down-regulated genes were identified at 24 hours after miRNA transfection with consistent differential expression (P-value &lt; 0.01) in HCT116 and DLD-1 colon tumor cell lines hypomorphic for Dicer (HCT116 Dicerex5 and DLD-1 Dicerex5, respectively) 2. Consensus miRNA down-regulated transcripts were also required to be significantly down-regulated (P-value &lt; 0.05) at 6 hours post-transfection in the colon cancer HTC116 Dicerex5 cell line 2.<p><a href='http://www.ncbi.nlm.nih.gov/pubmed/17242205' target='_blank' style='color: rgb(255,255,204)'>Linsley, P.S. et al. Transcripts targeted by the microRNA-16 family cooperatively regulate cell cycle progression. <i>Mol. Cell. Biol</i> <b>27</b>, 2240-2252 (2007).</a></p></li>
            <li><a href='http://www.mirbase.org/cgi-bin/mature.pl?mature_acc=MIMAT0000426' style='color: rgb(204,204,0)' target='_blank'><b>hsa-miR-132</b></a> - Only genes exceeding median expression in at least half of the experiments were assayed for differential expression. Differential expression (P-value &lt; 0.001) was required to be consistently observed at both the 12 hour and 24 hour time points after miRNA transfection in HeLa cells. This dataset was reanalyzed from data in GEO data repository GSE8501 using the specification in the publication stated above to identify perturbed miRNA target genes.<p><a href='http://www.ncbi.nlm.nih.gov/pubmed/17612493' target='_blank' style='color: rgb(255,255,204)'>Grimson, A. et al. MicroRNA targeting specificity in mammals: determinants beyond seed pairing. <i>Mol. Cell</i> <b>27</b>, 91-105 (2007).</a></p></li>
            <li><a href='http://www.mirbase.org/cgi-bin/mature.pl?mature_acc=MIMAT0000434' style='color: rgb(204,204,0)' target='_blank'><b>hsa-miR-142-3p</b></a> - Only genes exceeding median expression in at least half of the experiments were assayed for differential expression. Differential expression (P-value &lt; 0.001) was required to be consistently observed at both the 12 hour and 24 hour time points after miRNA transfection in HeLa cells. This dataset was reanalyzed from data in GEO data repository GSE8501 using the specification in the publication stated above to identify perturbed miRNA target genes.<p><a href='http://www.ncbi.nlm.nih.gov/pubmed/17612493' target='_blank' style='color: rgb(255,255,204)'>Grimson, A. et al. MicroRNA targeting specificity in mammals: determinants beyond seed pairing. <i>Mol. Cell</i> <b>27</b>, 91-105 (2007).</a></p></li>
            <li><a href='http://www.mirbase.org/cgi-bin/mature.pl?mature_acc=MIMAT0000454' style='color: rgb(204,204,0)' target='_blank'><b>hsa-miR-184</b></a> - Reported consistent down-regulation (log(FC) &lt; -1, P-value &lt; 0.05) of non-redundant genes in the glioma cell lines A172 and T98G 72 hours after miRNA transfection that also were predicted to be targets of this same miRNA by miRBase target database.<p><a href='http://www.ncbi.nlm.nih.gov/pubmed/19775293' target='_blank' style='color: rgb(255,255,204)'>Malzkorn, B. et al. Identification and functional characterization of microRNAs involved in the malignant progression of gliomas. <i>Brain Pathol</i> <b>20</b>, 539-550 (2010).</a></p></li></ul>
            <b>Loading and Using Sample Data</b> <p>Load the data by simply clicking the button with the corresponding miRNA on it, which will load the data and setup any parameters. Then click the submit button at the bottom of the page.</p>
            </font></td></tr>
            <tr><td><td></tr>
            <tr><td bgcolor='#000000' colspan=2><font color='#cccc00' size=4><b><a href="#weederParam" onclick="toggleVisible('weederParam'); return false;" style=\'color: rgb(204,204,0); text-decoration: none\'><center><b>Parameters for Weeder &nbsp; <font color="#ff0000">[?]</font></b></center></font></td></tr>
            <tr id="weederParam" style="display: none;"><td colspan=2 bgcolor='#333333'><font color='#ffffff'>
            <b>What is Weeder?</b>
            <p><a href='http://159.149.109.9/modtools/' style='color: rgb(204,204,0)' target='_blank'>Weeder</a> is an <a href='http://en.wikipedia.org/wiki/Enumerative' style='color: rgb(204,204,0)' target='_blank'>enumerative algorithm</a> used to identify over-represented <a href='http://en.wikipedia.org/wiki/Sequence_motif' style='color: rgb(204,204,0)' target='_blank'>sequence motifs</a> in the miRvestigator framework.</p>
            <b>What are the motif sizes?</b>
            <p>Weeder identifies both 6 base-pair (bp) and 8bp motifs for each run. Using this option it is possible to choose which motif size is subsequently used in the miRvestigator HMM is set by this option. Picking only one of the motif sizes will make the run faster. By default we have chosen to use 8bp motifs. (<b>Note:</b> It is possible that the 6bp motif and the 8bp motif will be different.)</p>
            <b>Background models?</b>
            <p>Weeder uses the background model to determine whether or not an oligo is enriched above background. The Weeder documentation states that the "Default Weeder Model" should be sufficient for 3' UTRs even though it was built based up on upstream sequences, which was consistent with our findings. Although in certain cases a model built upon the 3' UTR sequences was helpful. By default the "Default Weeder Model" is chosen. (<b>Note:</b> It is likely that the 3' UTR background model would improve given more complete 3'UTR annotations.)</p>
            </font></td></tr>
            <tr><td bgcolor='#333333'><b><center><font color='#ffffff'>Motif Sizes:</font></center></b></td><td bgcolor='#666666'><table cellpadding='5%' width='100%'><tr><td bgcolor='#ffffff'><center><b>6bp</b> <input type='checkbox' name='motif_6' value=6></input></center></td><td bgcolor='#ffffff'><center><b>8bp</b> <input type='checkbox' name='motif_8' value=8 checked></input></center></td></tr></table></td></tr>
            <tr><td bgcolor='#333333'><b><center><font color='#ffffff'>Background Model:</font></center></b></td><td bgcolor='#666666'><table width=100%><tr><td bgcolor='#ffffff'><center><select name='bgModel'><option value='HS' selected>Default Weeder Model</option><option value='HS3P'>3' UTR Specific Model</option></select></center></td></tr></table></td></tr>
            <tr><td><td></tr>
            <tr><td bgcolor='#000000' colspan=2><font color='#cccc00' size=4><b><a href="#mvParam" onclick="toggleVisible('mvParam'); return false;" style=\'color: rgb(204,204,0); text-decoration: none\'><center><b>Parameters for miRvestigator HMM &nbsp; <font color="#ff0000">[?]</font></a></b></center></font></td></tr>
            <tr id="mvParam" style="display: none;"><td colspan=2 bgcolor='#333333'><font color='#ffffff'>
            <b>What is the miRvestigator hidden Markov model (HMM)?</b>
            <p>The miRvestiator <a href='http://en.wikipedia.org/wiki/Hidden_Markov_model' style='color: rgb(204,204,0)' target='_blank'>hidden Markov model (HMM)</a> is a method designed to take an over-represented <a href='http://en.wikipedia.org/wiki/Sequence_motif' style='color: rgb(204,204,0)' target='_blank'>sequence motif</a> (in this case from <a href='http://159.149.109.9/modtools' style='color: rgb(204,204,0)' target='_blank'>Weeder</a>) and compare it to all the miRNA seed sequences from <a href='http://www.mirbase.org' style='color: rgb(204,204,0)' target='_blank'>miRBase</a> using the <a href='http://en.wikipedia.org/wiki/Viterbi_algorithm' style='color: rgb(204,204,0)' target='_blank'>Viterbi algorithm</a>. The over-represented sequence motif is turned into a profile HMM and each seed sequence in miRBase is aligned and a probability computed using the Viterbi algorithm. Then a Viterbi p-value is calculated for each miRNA by comparing it to an exhaustive distribution of Viterbi probabilities.<p>
            <b>What are the seed models?</b>
            <p>Base-pairing models for the seed regions of a miRNA to the 3' UTR of target transcripts. The 8mer, 7mer-m8, and 7mer-a1 models are the canonical models of miRNA to mRNA base-pairing. The 6mer models are considered marginal models as they typically have a reduced efficacy and are more likely to occur by chance alone. By default all of the seed models are used. The seed models are described in this figure:<center><img src='http://mirvestigator.systemsbiology.net/seedModels.gif' width='400' style='background: rgb(204,204,204)'></center></p>
            <b>Model Wobble Base-Pairing?</b>
            <p>The miRvestigator HMM can also model G:U wobble base-pairing which has been observed in miRNA to target transcript 3' UTR complementarity. The sequence motif is unlikely to be comprised completely of instances where a G:U wobble was used in the exact same spot. However, it may be possible and we do not want to exclude the possibility. Thus the miRvestigator framework can be enabled to model these G:U base pairings once the G or U nucleotide frequency in the sequence motif column passes a specified threshold. This threshold can be set with the "Min. Freq. of G or U". By default the wobble base-pairing is not modeled but if wobble base-pairing is enabled we reccomend a threshold of 0.25 for the "Min. Freq. of G or U".</p>
            </font></td></tr>
            <tr><td bgcolor='#333333'><center><b><font color='#ffffff'>Seed Models:</font></b></center></td><td bgcolor='#666666'><table cellpadding='5%' width='100%'><tr><td bgcolor='#ffffff'><b>6mer</b> <input type='checkbox' name='seedModel_6' value=6 checked></input></td><td bgcolor='#ffffff'><b>7mer</b> <input type='checkbox' name='seedModel_7' value=7 checked></input></td><td bgcolor='#ffffff'><b>8mer</b> <input type='checkbox' name='seedModel_8' value=8 checked></input></td></tr></table></td></tr>
            <tr><td bgcolor='#333333'><b><center><font color='#ffffff'>Model Wobble Base-Pairing:</font></center></b></td><td bgcolor='#666666'><table width='100%' cellpadding='5%'><tr><td bgcolor='#ffffff'><center><b>Yes</b><input type='radio' name='wobble' value='yes'></input> <b>No</b><input type='radio' name='wobble' value='no' checked></input></center></td><td bgcolor='#ffffff'><center><b>Min. Freq. of G or U:</b> <input type='text' name='cut' value='0.25' size=2></input></center></td></tr></table></td></tr>
            <tr><td><td></tr>
            <tr><td bgcolor='#000000' colspan=2><center><font color='#cccc00' size=4><b>Submit the Job</b></font></center></b></font></td></tr>
            <tr><td bgcolor='#333333'><center><b><font color='#ffffff'>Top miRNAs to return:</font></b></center></td><td bgcolor='#666666'><table cellpadding='5%' width='100%'><tr><td bgcolor='#ffffff'><center><select name='topRet'><option value='10' selected>Top 10</option><option value='25'>Top 25</option><option value='50'>Top 50</option><option value='75'>Top 75</option><option value='100'>Top 100</option><option value='all'>All</option></select></center></td></tr></table></td></tr>
            <tr><td bgcolor='#333333' colspan=2><center><table cellpadding='5%'><tr><td bgcolor='#ffffff'><input style='font-weight: bold' type='submit' value='         Submit         '></td></tr></table></center></tr></td></table>
            </form></p>
            
            <table width='100%' cellpadding='5%'><tr><td bgcolor='#c0c0c0'><center>Need help? Please contact <font color='#0000ff'>cplaisier(at)systemsbiology.org</font> if you have any questions, comments or concerns.<br>Developed at the <a href='http://www.systemsbiology.org' target='_blank' style=\'color: rgb(0,0,255)\'>Institute for Systems Biology</a> in the <a href='http://baliga.systemsbiology.net/' target='_blank' style=\'color: rgb(0,0,255)\'>Baliga Lab</a>.</center></td></tr></table>
            </center></td></tr></table>
            </center></font>
            </body></html>
        """
    return s

# </br><a href=''>Information about sample data.</a> - Need to add this back later.


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


def _get_db_connection():
    return MySQLdb.connect("localhost","mirv","mirvestigator","mirvestigator")

def _get_job_status(id):
    conn = _get_db_connection()
    try:
        created_at = datetime.datetime.now()
        cursor = conn.cursor()
        cursor.execute("select * from jobs where uuid=%s;", (id,))
        row = cursor.fetchone()
        created_at = row[1];
        updated_at = row[2];
        status = row[3];
        return (created_at, updated_at, status,)
    finally:
        try:
            cursor.close()
        except Exception as exception:
            print("Exception closing cursor: ")
            print(exception)
        try:
            conn.close()
        except Exception as exception:
            print("Exception closing conection: ")
            print(exception)

# return a JSON string encoding job status                                                            
def status(req):
    id = str(req.form.getfirst('id',''))
    req.content_type='application/json'
    return "{ \"created_at\": \"%s\", \"updated_at\": \"%s\", \"status\": \"%s\" }" % _get_job_status(id)







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

