# create_db.py

# creates an sqlite database runed introns.db containing annotation
# information for all introns in all specified genoes, including
# designation of intron class and a table annotating homologous
# relationships between all annotated introns.

import subprocess as sp
import argparse

def main():
    MakeDB()

class MakeDB():
    # create command-line arguments
    def __init__(self):
        parser = argparse.ArgumentParser(description='Creates an SQLite \
        database containing intron annotation information from a given genome \
        by running intronIC, a program designed to identify U12-type introns \
        given a genome annotation file and a whole-genome FASTA file.')
        parser.add_argument('-n', '--name_of_genome_assembly', help='E.g. \
        GRCh38 or hg38 for the latest version of the human genome.')
        parser.add_argument('-t', '--taxonomic_name',
            help='E.g. Homo_sapiens; be sure to use snake_case or CamelCase.')
        parser.add_argument('-c', '--common_name', help='E.g. human or \
        rhesus_macaque; be sure to use snake_case or CamelCase.')
        parser.add_argument('-a', '--annotation_file', help='Path to a gtf or \
        gff3 file containing annotation information for the genome of \
        interest. This pipeline was built using ones from Ensembl, but should \
        work on any annotation files.')
        parser.add_argument('-s', '--whole_genome_sequence_file',
            help='Path to a whole-genome FASTA file.')
        parser.add_argument('-g', '--gene_symbols', help='If your genome has \
        annotation information on Ensembl, you can pull gene names out of \
        Biomart if you know which Biomart division (default, GRCh37, plants, \
        metazoa, fungi) the genome is in by providing the name of the biomart \
        division as the value to this argument (Googling the genome name and \
        the word "ensembl" is the fastest way to find out which division \
        it\'s in). If your genome is not annotated in Biomart and you still \
        want to be able to search for introns using their gene, you can \
        provide a path to a tab-delimited file with gene IDs (as annotated in \
        the annotation file you provide) in the first column and gene symbols \
        in the second column. If you don\'t want to be able to search for \
        introns by gene names and/or don\'t want to deal with the Biomart \
        thing, leave this blank.')

        args = parser.parse_args()
        self.create_db(args)

    def create_db(self, args):
        genome_name = args.name_of_genome_assembly
        tax_name = args.taxonomic_name
        com_name = args.common_name
        gtf_path = args.annotation_file
        fasta_path = args.whole_genome_sequence_file
        mart_type = args.gene_symbols

        with open('log_file.txt', 'w') as log_file:
            print('Creating directories to hold intermediate and output files.')
            log_file.write('Creating directories for intermediate files.')
            # store all of these stdouts and stderrs in a dummy variable so they
            # don't print to the screen; ignore warnings about preexisting dirs
            # intronIC output we need, intronIC output we don't need, logs
            x = sp.run('mkdir info', stderr=sp.PIPE, shell=True)
            x = sp.run('mkdir tmp', stderr=sp.PIPE, shell=True)
            x = sp.run('mkdir intronIC_logs', stderr=sp.PIPE, shell=True)

            print(f'Running intronIC on {genome_name} ({tax_name})')
            log_file.write(f'Running intronIC on {genome_name} ({tax_name})')
            sp.run(f'python intronIC_devlin.py -nc -na -a {gtf_path}' +
                 f'-g {fasta_path} -n {genome_name}_cds', shell=True)
            sp.run(f'python intronIC_devlin.py -nc -na -e -a {gtf_path}' +
                 f'-g {fasta_path} -n {genome_name}_exon', shell=True)
            print('Removing duplicate introns from intronIC output.')
            log_file.write('Removing duplicate introns.')
            #sp.run(f'python deduplicate.py {genome}', shell=True)
            self.deduplicate(genome)
            if mart_type is not 'custom' and mart_type is not None:
                print('Querying Ensembl Biomart for gene symbols.')
                log_file.write('Querying Biomart for gene symbols.')
                sp.run(f'Rscript get_gene_symbols.R {mart_type} {genome}' +
                    f' {tax_name}', shell=True)
            elif '/' in mart_type: # mart_type is a path to gene symbols file
                sp.run(f'cp {mart_type} info/{genome_name}_gene_symbols.tsv',
                        shell=True)
            elif mart_type is None:
                # make an empty gene_symbols file so that reformatting.py
                # doesn't break but no gene symbols get inserted
                sp.run(f'echo > info/{genome_name}_gene_symbols.tsv',
                shell=True)

            # insert annotation information into database
            print(f'Adding annotation information for {genome_name} ({tax_name})')
            log_file.write(f'Adding annotation information to database for ' +
                f'{genome_name} ({tax_name}).')
            sp.run('python reformatting.py {genome_name} {tax_name} {com_name}',
                    shell=True)

            # remove intermediate files
            sp.run('rm -r tmp', shell=True)

    def deduplicate(self, genome):
        # get the list of all intron ids from the exon-defined intron file and
        # the cds-defined intron file, and make them sets so we can use the
        # difference method to get all the unique introns
        # have to define these out of the with block
        exon_ids = cds_ids = []
        with open(f'info/{genome}_cds_info.iic', 'r') as cds_file, \
        open(f'info/{genome}_exon_info.iic', 'r') as exon_file:
            cds_lines = cds_file.readlines()
            cds_coords = set(['\t'.join(x.split('\t')[4:7]) for x in cds_lines])
            exon_lines = exon_file.readlines()
            exon_coords = set(['\t'.join(x.split('\t')[4:7]) for x in exon_lines])

        # this will give us all the elements in exon_ids that aren't also in
        # cds_ids
        exon_only_coords = exon_coords.difference(cds_coords)

        with open(f'info/{genome}_exon_info.iic', 'r') as exon_file, \
        open(f'info/{genome}_cds_info.iic', 'r') as cds_file, \
        open(f'info/{genome}_info.iic', 'w') as out_file:
            i = 0
            matches = 0
            for line in exon_file:
                i += 1
                test_coords = '\t'.join(line.split('\t')[4:7])
                if test_coords in exon_only_coords:
                    matches += 1
                    out_file.write(line)
            # now that all of the exon-only introns are in the output file we
            # need to add in the cds-only introns
            out_file.write(''.join(cds_file.readlines()))
