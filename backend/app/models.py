"""
Data models for the phylogeny analysis API
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum


class AnalysisRequest(BaseModel):
    """Request model for phylogeny analysis"""
    accessions: List[str] = Field(..., description="List of UniProt accession numbers", min_length=2)
    trim_motif: Optional[str] = Field(None, description="Optional motif to trim sequences after")
    trim_before_motif: Optional[str] = Field(None, description="Optional motif to trim sequences before")

    class Config:
        json_schema_extra = {
            "example": {
                "accessions": ["P0C6X7", "P17763", "P29991"],
                "trim_motif": None,
                "trim_before_motif": None
            }
        }


class SequenceInfo(BaseModel):
    """Information about a downloaded sequence"""
    id: str
    name: str
    description: str
    length: int
    organism: Optional[str] = None
    sequence: str


class AlignmentInfo(BaseModel):
    """Multiple sequence alignment information"""
    num_sequences: int
    alignment_length: int
    average_conservation: float
    highly_conserved_positions: int


class IdentityScore(BaseModel):
    """Pairwise identity score"""
    seq1: str
    seq2: str
    identity: float


class TreeNode(BaseModel):
    """Phylogenetic tree node"""
    name: Optional[str] = None
    branch_length: float = 0.0
    children: List['TreeNode'] = []


class AnalysisStatus(str, Enum):
    """Analysis status"""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    ALIGNING = "aligning"
    BUILDING_TREE = "building_tree"
    COMPLETE = "complete"
    ERROR = "error"


class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    status: AnalysisStatus
    message: str
    sequences: Optional[List[SequenceInfo]] = None
    identity_matrix: Optional[List[List[float]]] = None
    identity_scores: Optional[List[IdentityScore]] = None
    alignment_info: Optional[AlignmentInfo] = None
    alignment_preview: Optional[List[Dict[str, str]]] = None
    alignment_full: Optional[List[Dict[str, str]]] = None
    alignment_clustal_text: Optional[str] = None
    tree_newick: Optional[str] = None
    tree_data: Optional[Dict] = None
    distance_matrix: Optional[List[List[float]]] = None
    summary_report: Optional[str] = None

    class Config:
        use_enum_values = True


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    ready: bool
