import mirv_db

print "Make gene dictionary"
genes = ['Gm10033', 'H2-Q3', 'morn2', 'pram1', 'adora3', 'flapdoodle']
genes_dictionary = mirv_db.get_gene_dictionary(genes, "symbol", "mmu")
print genes_dictionary


print "\n\nMap symbols"
entrez_ids = mirv_db.map_genes_to_entrez_ids('foo', 'symbol', 'mmu')
print entrez_ids

mappings = mirv_db.get_gene_mapping('foo')
print mappings

print "\n\nMap entrez ids"
entrez_ids = mirv_db.map_genes_to_entrez_ids('bar', 'entrez', 'mmu')
print entrez_ids
mappings = mirv_db.get_gene_mapping('bar')
print mappings


