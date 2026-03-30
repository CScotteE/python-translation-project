#! /usr/bin/env python3

import sys
import find_orf 
import translate

def translate_orf(sequence,
    start_codons = ['AUG'],
    stop_codons = ['UAA', 'UAG', 'UGA'],
    genetic_code = {'GUC': 'V', 'ACC': 'T', 'GUA': 'V', 'GUG': 'V', 'ACU': 'T', 'AAC': 'N', 'CCU': 'P', 'UGG': 'W', 'AGC': 'S', 'AUC': 'I', 'CAU': 'H', 'AAU': 'N', 'AGU': 'S', 'GUU': 'V', 'CAC': 'H', 'ACG': 'T', 'CCG': 'P', 'CCA': 'P', 'ACA': 'T', 'CCC': 'P', 'UGU': 'C', 'GGU': 'G', 'UCU': 'S', 'GCG': 'A', 'UGC': 'C', 'CAG': 'Q', 'GAU': 'D', 'UAU': 'Y', 'CGG': 'R', 'UCG': 'S', 'AGG': 'R', 'GGG': 'G', 'UCC': 'S', 'UCA': 'S', 'UAA': '*', 'GGA': 'G', 'UAC': 'Y', 'GAC': 'D', 'UAG': '*', 'AUA': 'I', 'GCA': 'A', 'CUU': 'L', 'GGC': 'G', 'AUG': 'M', 'CUG': 'L', 'GAG': 'E', 'CUC': 'L', 'AGA': 'R', 'CUA': 'L', 'GCC': 'A', 'AAA': 'K', 'AAG': 'K', 'CAA': 'Q', 'UUU': 'F', 'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'GCU': 'A', 'GAA': 'E', 'AUU': 'I', 'UUG': 'L', 'UUA': 'L', 'UGA': '*', 'UUC': 'F'}):

    """
    Finds the first ORF (open reading frame) in a sequence and subsequently translates 
    that ORF into a chain of amino acids. 

    Required Parameters
    --------
    sequence: A string representing your DNA or RNA sequence to be translated

    Optional Parameters
    --------
    start_codons: A list of start codons to use for determining the beginning of the ORF.
    Can either have one or stop multiple codons, but each must be a string of three nucleotides.
    Default: ['AUG']

    stop_codons: A list of start codons to use for determining the end of the ORF.
    Can either have one or multiple stop codons, but each must be a string of three nucleotides.
    Default: ['UAA', 'UAG', 'UGA']

    genetic_code: A dictionary of all possible codon -> amino acid translations. 
    Amino acids are represented by a single letter in the output.

    Returns
    -------
    A string where each single letter corresponds to an amino acid. This string begins AFTER your first start codon and ends
    BEFORE your stop codon. If no open reading frame is available or found, nothing is returned to STDOUT.
    
    """

    ORF = find_orf.find_first_orf(sequence, start_codons = start_codons, stop_codons = stop_codons)
    amino_seq = translate.translate_sequence(ORF, genetic_code)
    return amino_seq

def main():
    import argparse

    #Create a command line parser object 
    parser = argparse.ArgumentParser()

    default_start_codons = ['AUG']
    default_stop_codons = ['UAA', 'UAG', 'UGA']

    #Tell parser what command line arguments can be accepted and used
    parser.add_argument('sequence', 
            metavar = 'SEQUENCE',
            type = str,
            help = ('The sequence that will be used to find and translate it"s ORF. ' 
                    'If the path -p or --path is specified, then this should be a a path '  
                    'to the file containing the sequence to be used'))
    parser.add_argument('-p', '--path',
            action = 'store_true',
            help = ('The sequence arguement should be treated as a path to a file'
                    ' containing the sequence to be used'))
    parser.add_argument('-s', '--start-codon',
            type = str,
            action = 'append', #append each argument to a list (just like the default is formatted)
            default = None,
            help = ('A start codon. This option can be used multiple times if there are multiple start codons. '
                    'Default: {0}.'.format(" ".join(default_start_codons))))
    parser.add_argument('-x', '--stop-codon',
            type = str,
            action = 'append', # append each argument to a list
            default = None,
            help = ('A stop codon. This option can be used multiple times if there are multiple stop codons. '
                    'Default: {0}.'.format(" ".join(default_stop_codons))))

    #Parse the command-line arguments into a dict-like container
    args = parser.parse_args()
    print(args)

    #Check to see if the path option was set to True by the caller. If so, parse the sequence from the path.
    if args.path:
        sequence = parse_sequence_from_path(args.sequence)
    else:
        sequence = args.sequence
    
    #Check to see if start/stop codons were provided by the caller. If not, use the defaults
    if not args.start_codon:
        args.start_codon = default_start_codons
    if not args.stop_codon:
        args.stop_codon = default_stop_codons

    orf = translate_orf(sequence = sequence,
            start_codons = args.start_codon,
            stop_codons = args.stop_codon)
    sys.stdout.write('{}\n'.format(orf))

if __name__ == '__main__':
    main()