"""
Phylogen

etic analysis engine
Contains all bioinformatics logic for sequence analysis
"""
import urllib.request
import urllib.error
from typing import List, Dict, Tuple, Optional
import numpy as np
from Bio import SeqIO, Align, Phylo
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from io import StringIO
import logging

logger = logging.getLogger(__name__)

UNIPROT_API_BASE = "https://rest.uniprot.org/uniprotkb/"


def download_uniprot_sequence(accession: str) -> Optional[Dict]:
    """
    Download a protein sequence from UniProt.

    Args:
        accession: UniProt accession number

    Returns:
        Dictionary with sequence information or None if failed
    """
    logger.info(f"Downloading sequence {accession} from UniProt")

    url = f"{UNIPROT_API_BASE}{accession}.fasta"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            fasta_data = response.read().decode('utf-8')

        lines = fasta_data.strip().split('\n')
        header = lines[0]
        sequence = ''.join(lines[1:])

        # Parse header
        header_parts = header.split('|')
        if len(header_parts) >= 3:
            acc = header_parts[1]
            description = header_parts[2]
        else:
            acc = accession
            description = header.replace('>', '')

        # Extract organism
        organism = "Unknown"
        if 'OS=' in fasta_data:
            try:
                organism = fasta_data.split('OS=')[1].split('OX=')[0].strip()
            except:
                pass

        return {
            'id': acc,
            'name': description.split(' ')[0] if description else acc,
            'description': description,
            'sequence': sequence,
            'organism': organism,
            'length': len(sequence)
        }

    except urllib.error.HTTPError as e:
        logger.error(f"HTTP error downloading {accession}: {e.code}")
        return None
    except Exception as e:
        logger.error(f"Error downloading {accession}: {e}")
        return None


def parse_fasta_file(file_content: str) -> List[Dict]:
    """
    Parse FASTA file content into SequenceInfo dictionaries.

    Args:
        file_content: Raw FASTA file content as string

    Returns:
        List of sequence dictionaries compatible with the analysis pipeline

    Raises:
        ValueError: If FASTA format is invalid or no sequences found
    """
    logger.info("Parsing FASTA file content")

    try:
        sequences = []
        fasta_io = StringIO(file_content)

        for record in SeqIO.parse(fasta_io, "fasta"):
            # Validate sequence contains only valid amino acids
            valid_aa = set("ACDEFGHIKLMNPQRSTVWY-")
            seq_upper = str(record.seq).upper()

            if not all(c in valid_aa for c in seq_upper):
                raise ValueError(f"Sequence {record.id} contains invalid amino acid characters")

            # Extract organism from description if present (format: >ID organism [annotation])
            organism = "Unknown"
            description = record.description

            # Try to extract organism from common FASTA formats
            if '[' in description and ']' in description:
                try:
                    organism = description.split('[')[1].split(']')[0].strip()
                except:
                    pass

            sequences.append({
                'id': record.id,
                'name': record.id,  # Use ID as name if not available
                'description': description,
                'sequence': str(record.seq),
                'organism': organism,
                'length': len(record.seq)
            })

        if len(sequences) < 2:
            raise ValueError(f"FASTA file must contain at least 2 sequences, found {len(sequences)}")

        logger.info(f"Successfully parsed {len(sequences)} sequences from FASTA file")
        return sequences

    except Exception as e:
        logger.error(f"Error parsing FASTA file: {str(e)}")
        raise ValueError(f"Invalid FASTA format: {str(e)}")


def trim_sequence(seq_info: Dict, motif: str) -> Dict:
    """
    Trim sequence after a specific motif.

    Args:
        seq_info: Sequence dictionary
        motif: Amino acid motif to search for

    Returns:
        Modified sequence dictionary
    """
    sequence = seq_info['sequence']
    pos = sequence.find(motif)

    if pos == -1:
        logger.warning(f"Motif '{motif}' not found in {seq_info['id']}")
        return seq_info

    trimmed_seq = sequence[:pos + len(motif)]
    original_length = len(sequence)

    logger.info(f"Trimmed {seq_info['id']} from {original_length} to {len(trimmed_seq)} aa")

    seq_info['sequence'] = trimmed_seq
    seq_info['length'] = len(trimmed_seq)
    seq_info['trimmed'] = True

    return seq_info


def trim_sequence_before(seq_info: Dict, motif: str) -> Dict:
    """
    Trim sequence before a specific motif (remove everything before motif, keep motif and after).

    Args:
        seq_info: Sequence dictionary
        motif: Amino acid motif to search for

    Returns:
        Modified sequence dictionary
    """
    sequence = seq_info['sequence']
    pos = sequence.find(motif)

    if pos == -1:
        logger.warning(f"Motif '{motif}' not found in {seq_info['id']}")
        return seq_info

    trimmed_seq = sequence[pos:]
    original_length = len(sequence)

    logger.info(f"Trimmed before motif in {seq_info['id']} from {original_length} to {len(trimmed_seq)} aa")

    seq_info['sequence'] = trimmed_seq
    seq_info['length'] = len(trimmed_seq)
    seq_info['trimmed_before'] = True

    return seq_info


def calculate_identity_matrix(sequences: List[Dict]) -> Tuple[np.ndarray, List[str]]:
    """
    Calculate pairwise sequence identity matrix.

    Args:
        sequences: List of sequence dictionaries

    Returns:
        Tuple of (identity matrix, sequence IDs)
    """
    logger.info(f"Calculating identity matrix for {len(sequences)} sequences")

    n = len(sequences)
    identity_matrix = np.zeros((n, n))
    seq_ids = [seq['id'] for seq in sequences]

    aligner = Align.PairwiseAligner()
    aligner.mode = 'global'
    aligner.match_score = 1
    aligner.mismatch_score = 0
    aligner.open_gap_score = -1
    aligner.extend_gap_score = -0.5

    for i in range(n):
        for j in range(i, n):
            if i == j:
                identity_matrix[i][j] = 100.0
            else:
                seq1 = sequences[i]['sequence']
                seq2 = sequences[j]['sequence']

                alignments = aligner.align(seq1, seq2)
                best_alignment = alignments[0]

                aligned_seq1 = str(best_alignment[0])
                aligned_seq2 = str(best_alignment[1])

                matches = sum(1 for a, b in zip(aligned_seq1, aligned_seq2) if a == b and a != '-')
                alignment_length = len(aligned_seq1)

                percent_identity = (matches / alignment_length) * 100

                identity_matrix[i][j] = percent_identity
                identity_matrix[j][i] = percent_identity

    return identity_matrix, seq_ids


def extract_clustal_conservation(clustal_file: str) -> str:
    """
    Extract conservation line from Clustal format alignment file.

    Args:
        clustal_file: Path to Clustal format alignment file

    Returns:
        Conservation line string with *, :, . symbols
    """
    conservation_line = ""
    try:
        with open(clustal_file, 'r') as f:
            lines = f.readlines()

        # Conservation lines are lines that start with spaces and contain conservation symbols
        for line in lines:
            # Skip header and empty lines
            if not line.strip() or line.startswith('CLUSTAL'):
                continue
            # Conservation lines start with spaces (no sequence ID)
            if line.startswith(' ') or line.startswith('\t'):
                # Extract the conservation symbols
                conservation_part = line.strip()
                if conservation_part and any(c in conservation_part for c in ['*', ':', '.']):
                    conservation_line += conservation_part

    except Exception as e:
        logger.warning(f"Could not extract conservation line: {e}")

    return conservation_line


def create_alignment(sequences: List[Dict]) -> Tuple[MultipleSeqAlignment, Dict, str, str]:
    """
    Create multiple sequence alignment using ClustalOmega.

    Args:
        sequences: List of sequence dictionaries

    Returns:
        Tuple of (alignment object, statistics dictionary, conservation line, raw clustal text)
    """
    import tempfile
    import subprocess
    from Bio import AlignIO

    logger.info(f"Creating alignment for {len(sequences)} sequences using ClustalOmega")

    seq_records = []
    for seq in sequences:
        record = SeqRecord(
            Seq(seq['sequence']),
            id=seq['id'],
            description=seq['description']
        )
        seq_records.append(record)

    # Create temporary files for input and output
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False) as input_file:
        SeqIO.write(seq_records, input_file.name, 'fasta')
        input_filename = input_file.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.aln', delete=False) as output_file:
        output_filename = output_file.name

    try:
        # Run ClustalOmega
        logger.info("Running ClustalOmega alignment...")
        cmd = [
            'clustalo',
            '-i', input_filename,
            '-o', output_filename,
            '--outfmt=clustal',
            '--force'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            logger.error(f"ClustalOmega failed: {result.stderr}")
            raise RuntimeError(f"ClustalOmega alignment failed: {result.stderr}")

        # Read the alignment
        alignment = AlignIO.read(output_filename, 'clustal')
        logger.info(f"Alignment complete: {len(alignment)} sequences, {alignment.get_alignment_length()} positions")

        # Extract conservation line from Clustal output
        conservation_line = extract_clustal_conservation(output_filename)

        # Save alignment to a persistent location for download and read content
        alignment_download_path = '/tmp/latest_alignment.aln'
        with open(output_filename, 'r') as src:
            clustal_text = src.read()
            with open(alignment_download_path, 'w') as dst:
                dst.write(clustal_text)
        logger.info(f"Alignment saved to {alignment_download_path}")

    finally:
        # Clean up temporary files
        import os
        try:
            os.unlink(input_filename)
            os.unlink(output_filename)
        except:
            pass

    # Calculate statistics
    aln_length = alignment.get_alignment_length()
    conservation_scores = []

    for i in range(aln_length):
        column = alignment[:, i]
        non_gaps = [c for c in column if c != '-']
        if len(non_gaps) > 0:
            most_common = max(set(non_gaps), key=non_gaps.count)
            conservation = (non_gaps.count(most_common) / len(non_gaps)) * 100
        else:
            conservation = 0
        conservation_scores.append(conservation)

    avg_conservation = np.mean(conservation_scores)
    highly_conserved = sum(1 for score in conservation_scores if score > 90)

    stats = {
        'num_sequences': len(alignment),
        'alignment_length': aln_length,
        'average_conservation': float(avg_conservation),
        'highly_conserved_positions': highly_conserved
    }

    return alignment, stats, conservation_line, clustal_text


def get_alignment_preview(alignment: MultipleSeqAlignment, length: int = 60) -> List[Dict[str, str]]:
    """
    Get a preview of the alignment for display.

    Args:
        alignment: MultipleSeqAlignment object
        length: Number of positions to show

    Returns:
        List of dictionaries with id and sequence segment
    """
    preview = []
    for record in alignment:
        seq_segment = str(record.seq)[:length]
        preview.append({
            'id': record.id,
            'sequence': seq_segment
        })

    # Add conservation line
    conservation_line = ""
    for i in range(min(length, alignment.get_alignment_length())):
        column = alignment[:, i]
        non_gaps = [c for c in column if c != '-']
        if len(non_gaps) > 0 and all(c == non_gaps[0] for c in non_gaps):
            conservation_line += "*"
        elif len(set(non_gaps)) <= 2 and len(non_gaps) > 1:
            conservation_line += ":"
        elif '-' not in column:
            conservation_line += "."
        else:
            conservation_line += " "

    preview.append({
        'id': 'Conservation',
        'sequence': conservation_line
    })

    return preview


def get_full_alignment(alignment: MultipleSeqAlignment, conservation_line: str = None) -> List[Dict[str, str]]:
    """
    Get the complete alignment for display.

    Args:
        alignment: MultipleSeqAlignment object
        conservation_line: Optional pre-calculated conservation line from Clustal

    Returns:
        List of dictionaries with id and full sequence
    """
    full_alignment = []
    for record in alignment:
        full_alignment.append({
            'id': record.id,
            'sequence': str(record.seq)
        })

    # Use provided conservation line or generate a simple one
    if conservation_line:
        full_alignment.append({
            'id': 'Conservation',
            'sequence': conservation_line
        })
    else:
        # Fallback: generate simple conservation line
        cons_line = ""
        for i in range(alignment.get_alignment_length()):
            column = alignment[:, i]
            non_gaps = [c for c in column if c != '-']
            if len(non_gaps) > 0 and all(c == non_gaps[0] for c in non_gaps):
                cons_line += "*"
            elif len(set(non_gaps)) <= 2 and len(non_gaps) > 1:
                cons_line += ":"
            elif '-' not in column:
                cons_line += "."
            else:
                cons_line += " "

        full_alignment.append({
            'id': 'Conservation',
            'sequence': cons_line
        })

    return full_alignment


def build_phylogenetic_tree(alignment: MultipleSeqAlignment) -> Tuple[str, np.ndarray]:
    """
    Build phylogenetic tree from alignment.

    Args:
        alignment: MultipleSeqAlignment object

    Returns:
        Tuple of (Newick string, distance matrix)
    """
    logger.info("Building phylogenetic tree")

    calculator = DistanceCalculator('identity')
    distance_matrix = calculator.get_distance(alignment)

    constructor = DistanceTreeConstructor(calculator)
    tree = constructor.upgma(distance_matrix)

    # Convert tree to Newick format
    handle = StringIO()
    Phylo.write(tree, handle, 'newick')
    newick_str = handle.getvalue().strip()

    # Convert distance matrix to numpy array
    n = len(alignment)
    dist_array = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_array[i][j] = distance_matrix[i, j]

    return newick_str, dist_array


def generate_summary_report(sequences: List[Dict], identity_matrix: np.ndarray,
                           alignment_stats: Dict, seq_ids: List[str]) -> str:
    """
    Generate a text summary report of the analysis.

    Args:
        sequences: List of sequence dictionaries
        identity_matrix: Pairwise identity matrix
        alignment_stats: Alignment statistics
        seq_ids: Sequence IDs

    Returns:
        Formatted summary report string
    """
    report = []
    report.append("=" * 70)
    report.append("PHYLOGENETIC ANALYSIS SUMMARY REPORT")
    report.append("=" * 70)
    report.append("")

    # Sequences
    report.append("SEQUENCES ANALYZED")
    report.append("-" * 70)
    for seq in sequences:
        report.append(f"  {seq['id']}: {seq['name']}")
        report.append(f"    Organism: {seq.get('organism', 'Unknown')}")
        report.append(f"    Length: {seq['length']} amino acids")
        if seq.get('trimmed'):
            report.append(f"    Status: Trimmed")
        report.append("")

    # Identity scores
    report.append("PAIRWISE SEQUENCE IDENTITY")
    report.append("-" * 70)

    # Find highest and lowest similarities
    n = len(seq_ids)
    identities = []
    for i in range(n):
        for j in range(i+1, n):
            identities.append((seq_ids[i], seq_ids[j], identity_matrix[i][j]))

    identities.sort(key=lambda x: x[2], reverse=True)

    report.append(f"Highest similarity: {identities[0][0]} ↔ {identities[0][1]}: {identities[0][2]:.2f}%")
    report.append(f"Lowest similarity: {identities[-1][0]} ↔ {identities[-1][1]}: {identities[-1][2]:.2f}%")
    report.append("")

    # Alignment stats
    report.append("ALIGNMENT STATISTICS")
    report.append("-" * 70)
    report.append(f"  Number of sequences: {alignment_stats['num_sequences']}")
    report.append(f"  Alignment length: {alignment_stats['alignment_length']} positions")
    report.append(f"  Average conservation: {alignment_stats['average_conservation']:.2f}%")
    report.append(f"  Highly conserved positions (>90%): {alignment_stats['highly_conserved_positions']}")
    report.append("")

    # Conclusions
    report.append("KEY FINDINGS")
    report.append("-" * 70)

    if identities[0][2] > 90:
        report.append(f"  • {identities[0][0]} and {identities[0][1]} are remarkably similar ({identities[0][2]:.2f}%)")
        report.append(f"    suggesting very recent divergence or strong evolutionary conservation.")

    avg_identity = np.mean([x[2] for x in identities])
    report.append(f"  • Average pairwise identity: {avg_identity:.2f}%")

    if alignment_stats['average_conservation'] > 60:
        report.append(f"  • High overall conservation ({alignment_stats['average_conservation']:.2f}%) indicates")
        report.append(f"    strong functional constraints across the protein family.")
    elif alignment_stats['average_conservation'] < 40:
        report.append(f"  • Moderate conservation ({alignment_stats['average_conservation']:.2f}%) suggests")
        report.append(f"    evolutionary flexibility with some divergence among sequences.")

    report.append("")
    report.append("=" * 70)
    report.append("Analysis complete. Review visualizations for detailed insights.")
    report.append("=" * 70)

    return "\n".join(report)
