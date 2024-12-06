from Bio import Align
 

def local_aligner():
    # reproducing the same aligner as in EMBOSS's needle (see above)
    aligner = Align.PairwiseAligner()
    aligner.mode = "local"
    # Same as EDNAFULL in 'needle' above
    # https://rosalind.info/glossary/dnafull/
    # It's a simple symmetric matrix that assign each match a score of 5
    # and each mismatch a score of -4
    aligner.substitution_matrix = Align.substitution_matrices.load("NUC.4.4")
    # Open and extend penalties the same as 'needle' above
    aligner.open_gap_score = -10
    aligner.extend_gap_score = -0.5
    # Do not pay the opening gap price at the edges of the alignment
    aligner.target_end_gap_score = 0.0
    aligner.query_end_gap_score = 0.0
    return aligner


def align(seq1, seq2, aligner = None):
    if aligner is None:
        aligner = local_aligner()

    alignments = aligner.align(seq1, seq2)

    results = []
    for al in alignments:
        score = al.score
        aligned_seq1, pattern, aligned_seq2 = al._format_unicode().splitlines()
        results.append((score, aligned_seq1, pattern, aligned_seq2, al))
    return results

def align_sorted(seq1, seq2, aligner = None):
    als = align(seq1, seq2, aligner)
    if len(als) == 0: return None
    return sorted(als, key = lambda al: al[0], reverse = True)

# Return the top scoring alignment
def align_top(seq1, seq2, aligner = None):
    return align_sorted(seq1, seq2, aligner)[0]

# USAGE:
# from local_align import local_aligner, align_top

# aligner = local_aligner()

# for chunk in chunks:
#     al = align_top("TCGAAAGCGTGGACAAACAA", chunk, aligner=aligner) # file 1
#     score, aligned_seq1, pattern, aligned_seq2, _alignment = al

#     coords = _alignment.aligned
#     target_start, target_end = coords[0,0,0], coords[0,-1,1]
#     chunk_start, chunk_end = coords[1,0,0], coords[1,-1,1]
#     print(target_start, target_end)
#     print(chunk_start, chunk_end)
#     print(score)
#     print(aligned_seq1)
#     print(pattern)
#     print(aligned_seq2)

#     print()
