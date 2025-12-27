# Phylogeny Web Analyzer

A comprehensive web-based bioinformatics tool for phylogenetic analysis of protein sequences. This application downloads sequences from UniProt, performs multiple sequence alignment using ClustalOmega, calculates pairwise identities, and builds phylogenetic trees.

## Features

- **Sequence Retrieval**: Download protein sequences from UniProt database by accession number
- **Multiple Sequence Alignment**: Generate high-quality alignments using ClustalOmega
- **Phylogenetic Tree**: Build and visualize phylogenetic trees using UPGMA algorithm
- **Identity Matrix**: Calculate pairwise sequence identities with interactive heatmap
- **Conservation Analysis**: Identify highly conserved regions across sequences
- **Sequence Trimming**: Optional trimming at specific motifs
- **Download Alignment**: Export Clustal format alignment files
- **Summary Report**: Comprehensive analysis report with key findings
- **Real-time Analysis**: Fast processing with visual feedback

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework for high-performance APIs
- **Biopython**: Bioinformatics library for sequence analysis
- **ClustalOmega**: Industry-standard multiple sequence alignment tool
- **NumPy**: Numerical computing for matrix operations
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for production deployment

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Modern UI**: Responsive design with real-time analysis updates

### Deployment
- **Docker**: Containerized application for consistent deployment
- **Docker Compose**: Multi-container orchestration

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Git (for cloning the repository)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd phylogeny-web-app
```

2. Build and start the application using Docker Compose:
```bash
docker-compose up --build
```

3. Access the application:
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/api/docs

### Usage

1. **Enter UniProt Accessions**:
   - Add at least 2 UniProt accession numbers (one per line)
   - Example: P17763, P29991, P03314

2. **Optional Trimming**:
   - Specify a motif to trim sequences (e.g., "GSVGFN")
   - Sequences will be trimmed after the specified motif

3. **Run Analysis**:
   - Click "Analyze Sequences"
   - Wait for the analysis to complete (typically 10-30 seconds)

4. **View Results**:
   - **Sequences**: View downloaded sequence information with organism and length
   - **Identity Matrix**: Pairwise sequence identity heatmap
   - **Phylogenetic Tree**: Visual ASCII representation of evolutionary relationships
   - **Sequence Alignment**: Full multiple sequence alignment in Clustal format
   - **Summary Report**: Comprehensive analysis with key findings and statistics

5. **Download Alignment**:
   - Click "Download Clustal File" to save the alignment in standard Clustal format

## Example Analysis

Try these Flavivirus envelope protein sequences:
- **P17763**: Dengue virus type 1
- **P29991**: Dengue virus type 2
- **P27915**: Japanese encephalitis virus
- **P03314**: Yellow fever virus

Or these betacoronavirus spike proteins:
- **P59594**: SARS coronavirus
- **K9N7C7**: MERS coronavirus

## Project Structure

```
phylogeny-web-app/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # API endpoints
│   │   ├── models.py       # Pydantic models
│   │   └── phylogeny.py    # Bioinformatics logic
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/               # Next.js frontend
│   ├── src/
│   │   └── app/
│   │       └── page.tsx    # Main application page
│   ├── package.json        # Node dependencies
│   ├── tailwind.config.ts  # Tailwind configuration
│   └── Dockerfile          # Frontend container
├── docker-compose.yml      # Multi-container setup
└── README.md              # This file
```

## API Endpoints

### Health Check
```
GET /api/health
```
Returns the health status of the API.

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "ready": true
}
```

### Analyze Sequences
```
POST /api/analyze
```
Performs complete phylogenetic analysis.

**Request Body**:
```json
{
  "accessions": ["P17763", "P29991", "P03314"],
  "trim_motif": "GSVGFN"
}
```

**Response**: Complete analysis results including:
- Sequences with metadata (ID, organism, length, description)
- Identity matrix (pairwise sequence identities)
- Identity scores (list of pairwise comparisons)
- Alignment information (statistics and conservation data)
- Full sequence alignment in Clustal format
- Phylogenetic tree in Newick format
- Distance matrix
- Summary report with key findings

### Download Alignment
```
GET /api/download-alignment
```
Downloads the latest Clustal alignment file from the most recent analysis.

**Response**: Plain text file in Clustal format

## Development

### Running Locally Without Docker

#### Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install ClustalOmega (system-wide)
# Ubuntu/Debian: sudo apt-get install clustalo
# macOS: brew install clustal-omega

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Access at http://localhost:3000
```

### Environment Variables

Backend (`backend/.env`):
```
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
```

Frontend (`frontend/.env.local`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Scientific Background

### Multiple Sequence Alignment (MSA)
Multiple sequence alignment is a fundamental technique in bioinformatics for comparing three or more biological sequences. This application uses **ClustalOmega**, which employs:
- Progressive alignment with guide trees
- HMM profile-profile techniques
- Optimized for large numbers of sequences
- Industry-standard output format

### Phylogenetic Tree Construction
Phylogenetic trees represent evolutionary relationships. This application uses:
- **UPGMA** (Unweighted Pair Group Method with Arithmetic Mean): A hierarchical clustering method that assumes a constant rate of evolution
- **Distance Matrix**: Based on sequence identity from the alignment
- **Newick Format**: Standard format for representing phylogenetic trees
- **Identity Calculator**: Measures sequence similarity from aligned sequences

### Conservation Symbols
In Clustal alignment format:
- `*` (asterisk): Positions with identical residues in all sequences
- `:` (colon): Positions with strongly similar properties (conserved substitutions)
- `.` (period): Positions with weakly similar properties
- ` ` (space): No conservation

### Pairwise Identity Calculation
Sequence identity is calculated as:
```
Identity = (Number of identical positions / Alignment length) × 100%
```

## Technical Details

### Alignment Algorithm
The application uses ClustalOmega through BioPython's subprocess interface:
1. Sequences are written to a temporary FASTA file
2. ClustalOmega is invoked via command line
3. Results are read from the output Clustal file
4. Conservation symbols are extracted directly from ClustalOmega output
5. Alignment is parsed and returned in multiple formats

### Tree Construction
The phylogenetic tree is built using:
1. Distance calculation from aligned sequences
2. UPGMA clustering algorithm
3. Newick format output for interoperability
4. ASCII visualization for quick viewing

### Performance
- Average analysis time: 10-30 seconds for 4-6 sequences
- Handles sequences up to 1000+ amino acids
- Supports 2-100+ sequences (practical limit)
- Alignment scales with O(n²) complexity

## Troubleshooting

### Docker Issues
If containers fail to start:
```bash
docker-compose down
docker-compose up --build
```

### Port Conflicts
If ports 3000 or 8000 are in use, modify `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # Change frontend port
  - "8001:8000"  # Change backend port
```

### ClustalOmega Not Found
If running locally without Docker:
- Ubuntu/Debian: `sudo apt-get install clustalo`
- macOS: `brew install clustal-omega`
- Windows: Download from http://www.clustal.org/omega/

## License

This project is open source and available under the MIT License.

## Acknowledgments

- **UniProt**: Comprehensive protein sequence database
- **ClustalOmega**: Multiple sequence alignment algorithm
- **Biopython**: Python tools for computational biology and bioinformatics
- **FastAPI**: Modern, fast web framework for building APIs
- **Next.js**: React framework for production-grade applications

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Guidelines
1. Follow PEP 8 for Python code
2. Use TypeScript for frontend code
3. Add tests for new features
4. Update documentation as needed

## Citation

If you use this tool in your research, please cite:
- UniProt Consortium
- Sievers F, et al. (2011) Fast, scalable generation of high-quality protein multiple sequence alignments using Clustal Omega. Molecular Systems Biology 7:539
- Cock PJA, et al. (2009) Biopython: freely available Python tools for computational molecular biology and bioinformatics. Bioinformatics 25(11):1422-1423

## Support

For issues, questions, or suggestions:
- Open an issue in the GitHub repository
- Check existing issues for solutions
- Consult the API documentation at http://localhost:8000/api/docs

## Version History

**Version 1.0.0** (December 2024)
- Initial release with ClustalOmega integration
- Full-featured web interface
- Download alignment functionality
- Comprehensive analysis reports
- Docker deployment support

---

Built with bioinformatics in mind for researchers, educators, and students.
