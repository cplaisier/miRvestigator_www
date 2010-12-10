import mirv_db

# note: these use \r\n line endings for compatibility with Excel.

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

def _build_alignment_string(alignment, seed, motif):
    alignment.pop() # Get rid of the extra state which is added by the forwardViterbi function
    start = 1    
    if alignment[0]=='NM1':
        for i in alignment:
            if i=='NM1':
                start += 1
    # Alignment
    motifAlign = ''
    seed = list(conv2rna(complement(seed)))
    seedAlign = ''
    motif = list(conv2rna(motif))
    alignMe = alignment
    aligned = ''
    lenMatch = 0
    # First get them zero'd to the same point
    if start>1:
        for i in range(start-1):
            seedAlign += seed.pop(0)
            aligned += ' '
            motifAlign += '-'
            alignMe.pop(0)
    if len(alignMe)>0 and not alignMe[0]=='PSSM0' and not alignMe[0]=='WOBBLE0':
        if alignMe[0][0]=='P':
            upTo = int(alignMe[0][4])
        elif alignMe[0][0]=='W':
            upTo = int(alignMe[0][6])
        for i in range(upTo):
            seedAlign += '-'
            aligned += ' '
            motifAlign += motif.pop(0)
    # Then add the parts that align
    while 1:
        if len(alignMe)==0 or alignMe[0]=='NM2':
            break
        seedAlign += seed.pop(0)
        if alignMe[0][0]=='P':
            aligned += '|'
        elif alignMe[0][0]=='W':
            aligned += ':'
        lenMatch += 1
        motifAlign += motif.pop(0)
        alignMe.pop(0)
    # Then do the ending
    if len(alignMe)>0:
        for i in alignMe:
            seedAlign += seed[0]
            seed = seed[1:]
            aligned += ' '
            motifAlign += '-'
        alignMe = []
    if len(motif)>0 and len(alignMe)==0:
        for i in motif:
            seedAlign += '-'
            aligned += ' '
            motifAlign += i
    return [motifAlign, aligned, seedAlign, lenMatch]


# take sites as a list of dictionaries and returns a csv string
# each site is a dictionary w/ keys: gene, start, match, site
def sites_to_csv(sites):
    s = "Entrez Gene ID,Sequence of Site,Start Relative to Stop Codon (bp),% Similarity to Consensus Motif\r\n"
    for site in sites:
        s += "%s,%s,%s,%s\n" % (site['gene'], site['site'], site['start'], site['match'])
    return s

# takes mirvestigator scores as a list of dictionaries and returns a csv string
# scores have keys: miRNA.name, miRNA.seed, model, statePath, vitPValue
def mirvestigator_scores_to_csv(scores, motif):
    s = "miRNA Name, miRNA Seed, Seed Model, Length of Alignment, Alignment, Viterbi P-Value\r\n"
    for score in scores:
        statePath = score['statePath']
        motifAlign, aligned, seedAlign, lenMatch = _build_alignment_string(score['statePath'], score['miRNA.seed'], motif)
        alignment = "%s\r\n%s\r\n%s" % (motifAlign, aligned, seedAlign)
        s += "%s,%s,%s,%s,\"%s\",%s\r\n" % (score['miRNA.name'], score['miRNA.seed'], score['model'], lenMatch, alignment, score['vitPValue'])
    return s

def get_sites_as_csv(motif_id):
    return sites_to_csv(mirv_db.read_sites(motif_id))

def get_mirvestigator_scores_as_csv(motif_id):
    motif = mirv_db.read_motif(motif_id)
    return mirvestigator_scores_to_csv(mirv_db.read_mirvestigator_scores(motif_id), motif['name'])


    