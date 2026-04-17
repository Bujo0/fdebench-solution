import json, requests, sys, time, traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, 'common/libs/fdebenchkit/src')
from ms.common.fdebenchkit.scorers.document_extraction import score_submission, score_document

BASE = 'http://localhost:8010'

with open('data/task2/public_eval_50.json') as f:
    inputs = json.load(f)
with open('data/task2/public_eval_50_gold.json') as f:
    golds = json.load(f)

gold_map = {g['document_id']: g for g in golds}

# ════════════════════════════════════════════════════════════════════
# TEST 1 & 2 & 3 & 4: Per-item extraction + scoring + quality + latency
# ════════════════════════════════════════════════════════════════════
print("=" * 70)
print("TEST 1-4: Per-item extraction, scoring, quality checks, latency")
print("=" * 70)

N = 5  # items to test
results = []
latencies = []
errors = []

for i, inp in enumerate(inputs[:N]):
    doc_id = inp['document_id']
    schema = json.loads(inp.get('json_schema', '{}'))
    schema_props = schema.get('properties', {})
    
    print(f"\n{'─'*60}")
    print(f"[{i+1}/{N}] {doc_id} (format={inp['content_format']}, content_len={len(inp.get('content',''))}, schema_fields={len(schema_props)})")
    
    t0 = time.time()
    try:
        resp = requests.post(f'{BASE}/extract', json=inp, timeout=120)
        lat = (time.time() - t0) * 1000
        latencies.append({'doc_id': doc_id, 'latency_ms': lat, 'status': resp.status_code})
        
        if resp.status_code == 200:
            result = resp.json()
            results.append(result)
            print(f"  ✓ Status: {resp.status_code} | Latency: {lat:.0f}ms")
            
            # Quality checks
            result_keys = set(result.keys()) - {'document_id', 'difficulty'}
            schema_keys = set(schema_props.keys())
            missing = schema_keys - result_keys
            extra = result_keys - schema_keys
            
            print(f"  Schema fields: {len(schema_keys)} | Result fields: {len(result_keys)}")
            if missing:
                print(f"  ⚠ MISSING fields: {missing}")
            if extra:
                print(f"  ⚠ EXTRA fields: {extra}")
            
            # Check document_id match
            if result.get('document_id') != doc_id:
                print(f"  ⚠ document_id MISMATCH: expected {doc_id}, got {result.get('document_id')}")
            
            # Type checks
            type_issues = []
            for field, spec in schema_props.items():
                val = result.get(field)
                if val is None:
                    continue
                expected_type = spec.get('type', '')
                if expected_type == 'number' and isinstance(val, str):
                    type_issues.append(f"{field}: got string '{val}' expected number")
                elif expected_type == 'integer' and isinstance(val, str):
                    type_issues.append(f"{field}: got string '{val}' expected integer")
                elif expected_type == 'boolean' and not isinstance(val, bool):
                    type_issues.append(f"{field}: got {type(val).__name__} '{val}' expected boolean")
                elif expected_type == 'array' and not isinstance(val, list):
                    type_issues.append(f"{field}: got {type(val).__name__} expected array")
                elif expected_type == 'object' and not isinstance(val, dict):
                    type_issues.append(f"{field}: got {type(val).__name__} expected object")
            
            if type_issues:
                print(f"  ⚠ TYPE ISSUES:")
                for ti in type_issues:
                    print(f"    - {ti}")
            else:
                print(f"  ✓ All types correct")
            
            # Per-item scoring
            if doc_id in gold_map:
                gold = gold_map[doc_id]
                info, fidelity = score_document(result, gold)
                composite = 0.7 * info + 0.3 * fidelity
                print(f"  SCORE: info_accuracy={info:.3f} | text_fidelity={fidelity:.3f} | composite={composite:.3f}")
                
                # Per-field breakdown
                gold_fields = {k: v for k, v in gold.items() if k not in ('document_id', 'difficulty')}
                for field, gold_val in gold_fields.items():
                    from ms.common.fdebenchkit.scorers.document_extraction import score_value
                    pred_val = result.get(field)
                    fi, ff = score_value(pred_val, gold_val)
                    if fi < 1.0 or ff < 1.0:
                        pred_preview = str(pred_val)[:80] if pred_val is not None else 'MISSING'
                        gold_preview = str(gold_val)[:80]
                        print(f"    Field '{field}': info={fi:.3f} fidelity={ff:.3f}")
                        print(f"      predicted: {pred_preview}")
                        print(f"      gold:      {gold_preview}")
        else:
            print(f"  ✗ Status: {resp.status_code} | Latency: {lat:.0f}ms")
            print(f"    Body: {resp.text[:200]}")
            errors.append({'doc_id': doc_id, 'status': resp.status_code, 'body': resp.text[:200]})
            results.append({'document_id': doc_id})
            
    except requests.exceptions.Timeout:
        lat = (time.time() - t0) * 1000
        print(f"  ✗ TIMEOUT after {lat:.0f}ms")
        errors.append({'doc_id': doc_id, 'error': 'timeout'})
        latencies.append({'doc_id': doc_id, 'latency_ms': lat, 'status': 'timeout'})
        results.append({'document_id': doc_id})
    except Exception as e:
        lat = (time.time() - t0) * 1000
        print(f"  ✗ ERROR: {e}")
        errors.append({'doc_id': doc_id, 'error': str(e)})
        latencies.append({'doc_id': doc_id, 'latency_ms': lat, 'status': 'error'})
        results.append({'document_id': doc_id})

# Aggregate scoring
print(f"\n{'='*70}")
print("AGGREGATE SCORING (items 0-4)")
print(f"{'='*70}")
gold_subset = [gold_map[r['document_id']] for r in results if r['document_id'] in gold_map]
if results and gold_subset:
    scores = score_submission(results, gold_subset)
    print(f"Resolution: {scores['resolution']:.1f}")
    print(f"Info Accuracy: {scores['dimension_scores']['information_accuracy']:.3f}")
    print(f"Text Fidelity: {scores['dimension_scores']['text_fidelity']:.3f}")
    print(f"Scored: {scores['documents_scored']} | Errored: {scores['documents_errored']}")

# Latency summary
print(f"\n{'='*70}")
print("LATENCY DISTRIBUTION")
print(f"{'='*70}")
valid_lats = [l['latency_ms'] for l in latencies if isinstance(l['status'], int)]
if valid_lats:
    valid_lats.sort()
    print(f"Min: {valid_lats[0]:.0f}ms")
    print(f"P50: {valid_lats[len(valid_lats)//2]:.0f}ms")
    print(f"P95: {valid_lats[int(len(valid_lats)*0.95)]:.0f}ms")
    print(f"Max: {valid_lats[-1]:.0f}ms")
    print(f"Mean: {sum(valid_lats)/len(valid_lats):.0f}ms")

