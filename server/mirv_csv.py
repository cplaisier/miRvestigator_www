import mirv_db


# take sites as a list of dictionaries and returns a csv string
# each site is a dictionary w/ keys: gene, start, match, site
def sites_to_csv(sites):
    s = "Entrez Gene ID, Sequence of Site, Start Relative to Stop Codon (bp), %% Similarity to Consensus Motif\n"
    for site in sites:
        s += "%s, %s, %s, %s\n" % (site['gene'], site['site'], site['start'], site['match'])
    return s

# takes mirvestigator scores as a list of dictionaries and returns a csv string
# scores have keys: miRNA.name, miRNA.seed, model, statePath, vitPValue
def mirvestigator_scores_to_csv(scores):
    s = "miRNA Name, miRNA Seed, Seed Model, Length of Alignment, Alignment, Viterbi P-Value\n"
    for score in scores:
        statePath = score['statePath']
        alignment = "xxxxxxx\\r\\n|||||||\\r\\nyyyyyyy"
        s += "%s, %s, %s, %s, %s, %s\n" % (score['miRNA.name'], score['miRNA.seed'], score['model'], len(score['statePath']), alignment, score['vitPValue'])
    return s

def get_sites_as_csv(motif_id):
    return sites_to_csv(mirv_db.read_sites(motif_id))

def get_mirvestigator_scores_as_csv(motif_id):
    return mirvestigator_scores_to_csv(mirv_db.read_mirvestigator_scores(motif_id))


    