"""
FastAPI application for phylogenetic analysis
Main API endpoints
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from typing import List

from .models import (
    AnalysisRequest,
    AnalysisResponse,
    AnalysisStatus,
    SequenceInfo,
    IdentityScore,
    AlignmentInfo,
    HealthResponse
)
from .phylogeny import (
    download_uniprot_sequence,
    trim_sequence,
    calculate_identity_matrix,
    create_alignment,
    get_alignment_preview,
    get_full_alignment,
    build_phylogenetic_tree,
    generate_summary_report
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Phylogeny Web Analyzer API",
    description="RESTful API for phylogenetic analysis of protein sequences",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        ready=True
    )


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_sequences(request: AnalysisRequest):
    """
    Main endpoint for phylogenetic analysis

    This endpoint:
    1. Downloads sequences from UniProt
    2. Optionally trims sequences
    3. Calculates pairwise identities
    4. Creates multiple sequence alignment
    5. Builds phylogenetic tree
    6. Generates summary report

    Args:
        request: AnalysisRequest with list of accession numbers

    Returns:
        AnalysisResponse with complete analysis results
    """
    logger.info(f"Starting analysis for accessions: {request.accessions}")

    try:
        # Step 1: Download sequences
        logger.info("Downloading sequences from UniProt...")
        sequences = []
        failed_accessions = []

        for acc in request.accessions:
            seq_info = download_uniprot_sequence(acc.strip())
            if seq_info:
                sequences.append(seq_info)
            else:
                failed_accessions.append(acc)

        if len(sequences) < 2:
            raise HTTPException(
                status_code=400,
                detail=f"Need at least 2 valid sequences. Failed to download: {failed_accessions}"
            )

        if failed_accessions:
            logger.warning(f"Failed to download: {failed_accessions}")

        # Step 2: Trim sequences if requested
        if request.trim_motif:
            logger.info(f"Trimming sequences at motif: {request.trim_motif}")
            sequences = [trim_sequence(seq, request.trim_motif) for seq in sequences]

        # Step 3: Calculate identity matrix
        logger.info("Calculating pairwise identities...")
        identity_matrix, seq_ids = calculate_identity_matrix(sequences)

        # Convert to list of IdentityScore objects
        identity_scores = []
        n = len(seq_ids)
        for i in range(n):
            for j in range(i+1, n):
                identity_scores.append(IdentityScore(
                    seq1=seq_ids[i],
                    seq2=seq_ids[j],
                    identity=float(identity_matrix[i][j])
                ))

        # Step 4: Create alignment
        logger.info("Creating multiple sequence alignment...")
        alignment, alignment_stats, conservation_line, clustal_text = create_alignment(sequences)
        alignment_preview = get_alignment_preview(alignment, length=80)
        alignment_full = get_full_alignment(alignment, conservation_line)

        # Step 5: Build phylogenetic tree
        logger.info("Building phylogenetic tree...")
        tree_newick, distance_matrix = build_phylogenetic_tree(alignment)

        # Step 6: Generate summary report
        logger.info("Generating summary report...")
        summary_report = generate_summary_report(
            sequences, identity_matrix, alignment_stats, seq_ids
        )

        # Prepare response
        response = AnalysisResponse(
            status=AnalysisStatus.COMPLETE,
            message=f"Analysis complete! Analyzed {len(sequences)} sequences.",
            sequences=[SequenceInfo(**seq) for seq in sequences],
            identity_matrix=identity_matrix.tolist(),
            identity_scores=identity_scores,
            alignment_info=AlignmentInfo(**alignment_stats),
            alignment_preview=alignment_preview,
            alignment_full=alignment_full,
            alignment_clustal_text=clustal_text,
            tree_newick=tree_newick,
            distance_matrix=distance_matrix.tolist(),
            summary_report=summary_report,
            tree_data={
                "newick": tree_newick,
                "sequence_ids": seq_ids,
                "distance_matrix": distance_matrix.tolist()
            }
        )

        logger.info("Analysis completed successfully")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.get("/api/download-alignment")
async def download_alignment():
    """
    Download the latest Clustal alignment file
    """
    from fastapi.responses import FileResponse
    import os

    alignment_path = '/tmp/latest_alignment.aln'

    if not os.path.exists(alignment_path):
        raise HTTPException(status_code=404, detail="No alignment file available. Please run an analysis first.")

    return FileResponse(
        path=alignment_path,
        media_type='text/plain',
        filename='clustal_alignment.aln',
        headers={
            "Content-Disposition": "attachment; filename=clustal_alignment.aln"
        }
    )


@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Phylogeny Web Analyzer API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
