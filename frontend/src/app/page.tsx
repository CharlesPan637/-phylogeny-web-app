'use client'

import { useState } from 'react'
import axios from 'axios'

// Function to parse Newick format and create ASCII tree
function parseNewick(newick: string): any {
  newick = newick.replace(/;$/, '').trim()

  const parseNode = (str: string): any => {
    str = str.trim()

    // If starts with '(', it's an internal node with children
    if (str.startsWith('(')) {
      const node: any = { children: [], name: null, length: 0 }

      // Find matching closing parenthesis
      let depth = 0
      let endParen = -1
      for (let i = 0; i < str.length; i++) {
        if (str[i] === '(') depth++
        else if (str[i] === ')') {
          depth--
          if (depth === 0) {
            endParen = i
            break
          }
        }
      }

      if (endParen === -1) return node

      // Parse children
      const childrenStr = str.substring(1, endParen)
      const children: string[] = []
      let current = ''
      depth = 0

      for (let i = 0; i < childrenStr.length; i++) {
        const char = childrenStr[i]
        if (char === '(') depth++
        else if (char === ')') depth--
        else if (char === ',' && depth === 0) {
          if (current.trim()) children.push(current.trim())
          current = ''
          continue
        }
        current += char
      }
      if (current.trim()) children.push(current.trim())

      node.children = children.map(child => parseNode(child))

      // Parse node label and branch length after ')'
      const afterParen = str.substring(endParen + 1)
      const colonIdx = afterParen.indexOf(':')
      if (colonIdx > 0) {
        node.name = afterParen.substring(0, colonIdx).trim() || 'Internal'
        node.length = parseFloat(afterParen.substring(colonIdx + 1)) || 0
      } else if (colonIdx === 0) {
        node.name = 'Internal'
        node.length = parseFloat(afterParen.substring(1)) || 0
      } else {
        node.name = afterParen.trim() || 'Internal'
      }

      return node
    } else {
      // Leaf node
      const colonIdx = str.indexOf(':')
      if (colonIdx > 0) {
        return {
          name: str.substring(0, colonIdx).trim(),
          length: parseFloat(str.substring(colonIdx + 1)) || 0,
          children: []
        }
      } else {
        return {
          name: str.trim(),
          length: 0,
          children: []
        }
      }
    }
  }

  return parseNode(newick)
}

// Function to render tree as ASCII art
function renderTreeAscii(tree: any, prefix: string = '', isLast: boolean = true): string {
  let result = ''
  const connector = isLast ? '└── ' : '├── '
  const name = tree.name || 'Internal Node'
  const length = tree.length ? ` (${tree.length.toFixed(4)})` : ''

  result += prefix + connector + name + length + '\n'

  if (tree.children && tree.children.length > 0) {
    const newPrefix = prefix + (isLast ? '    ' : '│   ')
    tree.children.forEach((child: any, index: number) => {
      result += renderTreeAscii(child, newPrefix, index === tree.children.length - 1)
    })
  }

  return result
}

export default function Home() {
  const [accessions, setAccessions] = useState('P03314\nP17763\nP29991\nP27909\nP09866')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [error, setError] = useState('')

  const handleAnalyze = async () => {
    setLoading(true)
    setError('')
    setResults(null)

    try {
      const accessionList = accessions.split('\n').map(a => a.trim()).filter(a => a)

      const response = await axios.post('/api/analyze', {
        accessions: accessionList
      })

      setResults(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            🧬 Phylogeny Web Analyzer
          </h1>
          <p className="text-xl text-gray-600">
            Professional phylogenetic analysis of protein sequences
          </p>
        </div>

        {/* Input Section */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">
            Enter UniProt Accession Numbers
          </h2>
          <p className="text-gray-600 mb-4">
            Enter UniProt IDs (one per line). Example: P0C6X7, P17763, P29991
          </p>

          <textarea
            className="w-full h-40 px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
            value={accessions}
            onChange={(e) => setAccessions(e.target.value)}
            placeholder="P0C6X7&#10;P17763&#10;P29991"
          />

          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="mt-4 w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:from-blue-700 hover:to-indigo-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                </svg>
                Analyzing sequences...
              </span>
            ) : (
              '🚀 Analyze Sequences'
            )}
          </button>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8 rounded">
            <p className="text-red-700 font-medium">{error}</p>
          </div>
        )}

        {/* Results */}
        {results && (
          <div className="space-y-8">
            {/* Summary */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h2 className="text-2xl font-bold mb-4 text-gray-800 flex items-center">
                <span className="mr-2">📊</span> Analysis Summary
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">
                    {results.sequences?.length || 0}
                  </div>
                  <div className="text-sm text-gray-600">Sequences</div>
                </div>
                <div className="bg-green-50 p-4 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">
                    {results.alignment_info?.alignment_length || 0}
                  </div>
                  <div className="text-sm text-gray-600">Alignment Length</div>
                </div>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">
                    {results.alignment_info?.average_conservation?.toFixed(1) || 0}%
                  </div>
                  <div className="text-sm text-gray-600">Avg Conservation</div>
                </div>
                <div className="bg-orange-50 p-4 rounded-lg">
                  <div className="text-2xl font-bold text-orange-600">
                    {results.identity_scores?.length || 0}
                  </div>
                  <div className="text-sm text-gray-600">Comparisons</div>
                </div>
              </div>
            </div>

            {/* Sequences */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h2 className="text-2xl font-bold mb-4 text-gray-800">
                📝 Downloaded Sequences
              </h2>
              <div className="space-y-3">
                {results.sequences?.map((seq: any) => (
                  <div key={seq.id} className="border-l-4 border-blue-500 pl-4 py-2 bg-gray-50 rounded-r">
                    <div className="font-semibold text-gray-800">{seq.id} - {seq.name}</div>
                    <div className="text-sm text-gray-600">{seq.organism}</div>
                    <div className="text-sm text-gray-500">{seq.length} amino acids</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Identity Matrix */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h2 className="text-2xl font-bold mb-4 text-gray-800">
                🎯 Pairwise Identity Scores
              </h2>
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead>
                    <tr>
                      <th className="px-4 py-2 text-left">Sequence 1</th>
                      <th className="px-4 py-2 text-left">Sequence 2</th>
                      <th className="px-4 py-2 text-right">Identity (%)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.identity_scores?.map((score: any, idx: number) => (
                      <tr key={idx} className="border-t hover:bg-gray-50">
                        <td className="px-4 py-2 font-mono text-sm">{score.seq1}</td>
                        <td className="px-4 py-2 font-mono text-sm">{score.seq2}</td>
                        <td className="px-4 py-2 text-right">
                          <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${
                            score.identity > 90 ? 'bg-green-100 text-green-800' :
                            score.identity > 70 ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                          }`}>
                            {score.identity.toFixed(2)}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Full Alignment */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h2 className="text-2xl font-bold text-gray-800">
                    📋 Complete Multiple Sequence Alignment (Clustal Format)
                  </h2>
                  <p className="text-gray-600 mt-2">
                    Full alignment of all {results.sequences?.length || 0} sequences.
                    Length: {results.alignment_info?.alignment_length || 0} positions.
                  </p>
                </div>
                <a
                  href="/api/download-alignment"
                  download="clustal_alignment.aln"
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors whitespace-nowrap"
                >
                  ⬇ Download Clustal File
                </a>
              </div>
              <div className="bg-gray-900 rounded-lg border-2 border-gray-700 overflow-auto max-h-[32rem]">
                <pre className="p-4 font-mono text-xs leading-relaxed text-green-400 whitespace-pre">
                  {results.alignment_clustal_text || 'Loading alignment...'}
                </pre>
              </div>
              <div className="mt-4 text-sm text-gray-600 space-y-1">
                <p>💡 Scroll vertically to view all blocks of the alignment</p>
                <p className="text-xs">
                  <strong>Conservation symbols:</strong>{' '}
                  <span className="text-yellow-400 font-mono">*</span> = Identical |
                  <span className="text-yellow-400 font-mono">:</span> = Low variation (≤2 residues) |
                  <span className="text-yellow-400 font-mono">.</span> = Fully aligned (no gaps) |
                  <span className="text-gray-400 font-mono">(space)</span> = Contains gaps
                </p>
              </div>
            </div>

            {/* Tree */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h2 className="text-2xl font-bold mb-4 text-gray-800">
                🌳 Phylogenetic Tree
              </h2>

              {/* Visual Tree */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-3 text-gray-700">Visual Representation</h3>
                <div className="bg-gray-900 p-6 rounded-lg">
                  <pre className="text-green-400 font-mono text-sm leading-relaxed">
                    {results.tree_newick && renderTreeAscii(parseNewick(results.tree_newick))}
                  </pre>
                </div>
                <p className="mt-2 text-sm text-gray-600">
                  📊 Branch lengths shown in parentheses represent evolutionary distance
                </p>
              </div>

              {/* Distance Matrix */}
              {results.distance_matrix && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-3 text-gray-700">Distance Matrix</h3>
                  <div className="overflow-x-auto">
                    <table className="min-w-full border border-gray-300">
                      <thead>
                        <tr className="bg-gray-100">
                          <th className="border border-gray-300 px-3 py-2 text-left text-sm">Sequence</th>
                          {results.sequences?.map((seq: any) => (
                            <th key={seq.id} className="border border-gray-300 px-3 py-2 text-sm font-mono">
                              {seq.id}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {results.distance_matrix.map((row: number[], i: number) => (
                          <tr key={i} className="hover:bg-gray-50">
                            <td className="border border-gray-300 px-3 py-2 font-mono text-sm font-semibold">
                              {results.sequences?.[i]?.id}
                            </td>
                            {row.map((val: number, j: number) => (
                              <td
                                key={j}
                                className={`border border-gray-300 px-3 py-2 text-center text-sm ${
                                  i === j ? 'bg-gray-200 font-bold' : ''
                                }`}
                              >
                                {val.toFixed(4)}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  <p className="mt-2 text-sm text-gray-600">
                    Lower values indicate more similar sequences
                  </p>
                </div>
              )}

              {/* Newick Format */}
              <div>
                <h3 className="text-lg font-semibold mb-3 text-gray-700">Newick Format (for external tools)</h3>
                <div className="bg-gray-50 p-4 rounded-lg border border-gray-300">
                  <pre className="font-mono text-xs overflow-x-auto text-gray-700">
                    {results.tree_newick}
                  </pre>
                </div>
                <p className="mt-2 text-sm text-gray-600">
                  💡 Copy this Newick string to visualize in tools like iTOL, FigTree, or MEGA
                </p>
              </div>
            </div>

            {/* Report */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h2 className="text-2xl font-bold mb-4 text-gray-800">
                📄 Summary Report
              </h2>
              <pre className="bg-gray-50 p-6 rounded-lg overflow-x-auto font-mono text-sm whitespace-pre-wrap">
                {results.summary_report}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
