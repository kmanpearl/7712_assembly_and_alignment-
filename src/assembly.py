__author__ = "Keenan Manpearl"
__date__ = "2023/03/06"

"""
Functions needed to assemble sequence reads 
"""


class Contig:
    def __init__(self, contig_id, aligned_reads, sequence, direction):
        self.contig_id = contig_id
        self.sequence = sequence
        self.direction = direction
        self.aligned_reads = aligned_reads

    def add_kmers(self, kmers):
        self.kmers = kmers


class AlignedRead:
    def __init__(
        self,
        read_id,
        contig_id,
        sequence,
        read_start,
        read_stop,
        contig_start,
        contig_stop,
    ):
        self.read_id = read_id
        self.contig_id = contig_id
        self.sequence = sequence
        self.read_start = read_start
        self.read_stop = read_stop
        self.contig_start = contig_start
        self.contig_stop = contig_stop


def get_contig_kmers(all_paths, read_kmers):
    contig_kmers = {}
    for path in all_paths:
        contig_id = path.contig_id
        for node in path.path:
            for kmer in read_kmers:
                if node == kmer.sequence:
                    if contig_id in contig_kmers.keys():
                        contig_kmers[contig_id].append(kmer)
                    else:
                        contig_kmers[contig_id] = [kmer]
                    break
    return contig_kmers


def get_contig_start(kmer, kmers, contig_start):
    overlap = 0
    while kmers[kmer - overlap - 1].sufix == kmers[kmer].prefix:
        overlap += 1
    return contig_start + overlap


def assemble_contigs(contig_kmers, read_dict):
    contigs = []
    for contig_id, kmers in contig_kmers.items():
        aligned_reads = []
        sequence = kmers[0].sequence
        read_id = kmers[0].read_id
        read_start = kmers[0].start
        contig_start = 0
        for kmer in range(1, len(kmers)):
            read_num = kmers[kmer].read_id
            if read_num != read_id:
                read_stop = kmers[kmer - 1].stop
                # contig_start = get_contig_start(kmer-1, kmers, contig_start)
                contig_stop = contig_start + len(sequence)
                sequence = read_dict[read_id][read_start:read_stop]
                read = AlignedRead(
                    read_id=read_id,
                    contig_id=contig_id,
                    sequence=sequence,
                    read_start=read_start,
                    read_stop=read_stop,
                    contig_start=contig_start,
                    contig_stop=contig_stop,
                )
                read_id = read_num
                read_start = kmers[kmer].start
                contig_start = contig_stop + 1
                aligned_reads.append(read)
        sequence += kmers[kmer - 1].sequence[-1]
        contig = Contig(
            contig_id=contig_id,
            aligned_reads=aligned_reads,
            sequence=sequence,
            direction=1,
        )
        contigs.append(contig)
    return contigs


def assembly(path_dict, read_kmers, read_dict):
    contig_kmers = get_contig_kmers(path_dict, read_kmers)
    contigs = assemble_contigs(contig_kmers, read_dict)
    # rvs_contigs = get_reverse_contigs(contigs, read_dict)
    return contigs
