"""
Flask API Backend for Fashion Intelligence
Server-side processing with enhanced scraping
"""

import re
import sys
import asyncio
import traceback
from pathlib import Path
from datetime import datetime

# Force UTF-8 stdout/stderr so emoji in print() don't crash on Windows cp1252 consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from flask import Flask, request, jsonify
from flask_cors import CORS

sys.path.append(str(Path(__file__).parent))

from backend.orchestrator import run_fashion_query

app = Flask(__name__)
CORS(app)

OUTPUT_BASE = Path("outputs")
OUTPUT_BASE.mkdir(exist_ok=True)


def _safe_dirname(text: str) -> str:
    """Strip characters that are invalid in directory names on all platforms."""
    safe = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', text)
    safe = safe.replace(' ', '_')
    return safe[:60]  # cap length


@app.route('/api/analyze', methods=['POST'])
def analyze_fashion():
    """
    Main endpoint for fashion analysis.
    POST /api/analyze  —  body: { "query": "denim jacket" }
    """
    try:
        data = request.get_json(force=True, silent=True) or {}
        query = data.get('query', '').strip()

        if not query:
            return jsonify({'error': 'Query is required', 'status': 'error'}), 400

        print(f"\n{'=' * 60}")
        print(f"📥 Received request: '{query}'")
        print(f"{'=' * 60}\n")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = OUTPUT_BASE / f"{_safe_dirname(query)}_{timestamp}"
        output_dir.mkdir(parents=True, exist_ok=True)

        # asyncio.run() is correct here — Flask runs synchronously in a single
        # thread so there is no running event loop to conflict with.
        result = asyncio.run(run_fashion_query(query, output_dir))
        result['output_directory'] = str(output_dir.absolute())

        print(f"\n{'=' * 60}")
        print(f"✅ Analysis complete for '{query}'")
        print(f"📁 Results saved to: {output_dir}")
        print(f"{'=' * 60}\n")

        return jsonify({'status': 'success', 'data': result})

    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc(),
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Fashion Intelligence API',
        'version': '2.0.0',
    })


@app.route('/api/outputs', methods=['GET'])
def list_outputs():
    """List all saved output directories."""
    try:
        outputs = []
        for output_dir in sorted(OUTPUT_BASE.iterdir(), reverse=True):
            if output_dir.is_dir():
                outputs.append({
                    'name': output_dir.name,
                    'path': str(output_dir.absolute()),
                    'files': [f.name for f in output_dir.iterdir()],
                })
        return jsonify({'status': 'success', 'outputs': outputs})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Fashion Intelligence API Server")
    print("=" * 60)
    print("📍 Running on: http://localhost:5000")
    print("📊 API Endpoints:")
    print("   POST /api/analyze — Analyze fashion query")
    print("   GET  /api/health  — Health check")
    print("   GET  /api/outputs — List saved outputs")
    print("=" * 60 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=False)
