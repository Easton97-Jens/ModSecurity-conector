#!/usr/bin/env python3
"""Validate Envoy source proposals without changing canonical oracle results."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import evidence_io

REPOSITORY = Path(__file__).resolve().parents[5]
STORAGE_ROOTS = (Path('/var/tmp/codex/ModSecurity-conector'),
                 Path('/root/git/codex-storage-archives'))
ROUTES = {'envoy-ext-proc': (117, 51), 'envoy-ext-authz-request': (94, 40),
          'envoy-ext-authz-response-companion': (73, 34)}
CATEGORIES = {'SOURCE_SEMANTICS_CONFIRMED', 'FIXTURE_PENDING', 'OPEN'}
MAX_REFERENCE_BYTES = 128 * 1024 * 1024
MAX_SOURCE_BYTES = 8 * 1024 * 1024


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


class References:
    def __init__(self):
        self.cache = {}

    def check(self, reference, source=False):
        if not isinstance(reference, dict) or not isinstance(reference.get('path'), str):
            raise ValueError('reference requires a path and SHA256')
        value = reference['path']
        path = Path(value)
        if not value or '\\' in value or '..' in path.parts:
            raise ValueError('reference path traversal is forbidden')
        if path.is_absolute():
            if not any(root in path.parents for root in STORAGE_ROOTS):
                raise ValueError('absolute reference outside approved storage: ' + value)
        else:
            if any(part in ('.git', '.aws', '.codex', '.agents') for part in path.parts):
                raise ValueError('reference is not a product source path')
            path = REPOSITORY / path
        expected = reference.get('sha256')
        if not isinstance(expected, str) or not re.fullmatch('[a-f0-9]{64}', expected):
            raise ValueError('reference requires a lowercase SHA256: ' + value)
        with evidence_io.open_evidence(path, (REPOSITORY, *STORAGE_ROOTS), MAX_REFERENCE_BYTES) as (stream, before):
            identity = evidence_io.identity(before)
            cached = self.cache.get(path)
            if cached is None or cached['identity'] != identity:
                cached = {'identity': identity, 'sha256': evidence_io.digest_stream(stream, MAX_REFERENCE_BYTES),
                          'bytes': before.st_size}
                self.cache[path] = cached
            if source and 'line_count' not in cached:
                if before.st_size > MAX_SOURCE_BYTES:
                    raise ValueError('source reference exceeds line-check bound: ' + value)
                stream.seek(0)
                cached['line_count'] = len(stream.read(MAX_SOURCE_BYTES + 1).splitlines())
        if expected != cached['sha256']:
            raise ValueError('reference SHA256 mismatch: ' + value)
        if 'bytes' in reference and (type(reference['bytes']) is not int or reference['bytes'] != before.st_size):
            raise ValueError('reference byte size mismatch: ' + value)
        result = {'path': value, 'sha256': expected, 'bytes': before.st_size, 'verified': True}
        if source:
            if before.st_size > MAX_SOURCE_BYTES:
                raise ValueError('source reference exceeds line-check bound: ' + value)
            line = reference.get('line')
            if type(line) is not int or not 1 <= line <= cached['line_count']:
                raise ValueError('source reference line outside file: ' + value)
            if not isinstance(reference.get('symbol'), str) or not reference['symbol']:
                raise ValueError('source reference requires a symbol: ' + value)
            if not isinstance(reference.get('claim'), str) or not reference['claim']:
                raise ValueError('source reference requires a claim: ' + value)
            result.update(line=line, symbol=reference['symbol'], claim=reference['claim'])
        return result

    def nested(self, value):
        result = []
        if isinstance(value, dict):
            if 'path' in value or 'sha256' in value:
                result.append(self.check(value))
            for child in value.values():
                result.extend(self.nested(child))
        elif isinstance(value, list):
            for child in value:
                result.extend(self.nested(child))
        # Preserve only reference metadata; never read payloads into the output.
        return result


def validate(baseline, review_paths):
    """Return normalized proposal metadata; canonical 3/122 remains unchanged.

    ``baseline`` accepts a parsed baseline object or its physical JSON path.
    Review paths must contain exactly one complete review for each Envoy route.
    Raises ValueError/OSError on a contract, identity or physical integrity gap.
    """
    baseline_hash = None
    if not isinstance(baseline, dict):
        raw = evidence_io.read_bytes(baseline, (REPOSITORY, *STORAGE_ROOTS))
        baseline_hash = hashlib.sha256(raw).hexdigest()
        baseline = json.loads(raw)
    baseline_rows = baseline.get('rows')
    if not isinstance(baseline_rows, list) or len(baseline_rows) != 284:
        raise ValueError('baseline must retain exactly 284 original Envoy IDs')
    identifiers = [row.get('run_scoped_case_id') for row in baseline_rows]
    if len(set(identifiers)) != 284:
        raise ValueError('duplicate original baseline ID')
    originals = {}
    canonical_counts = {}
    for route, (total, count) in ROUTES.items():
        all_rows = [row for row in baseline_rows if row.get('leg_id') == route]
        selected = [row for row in all_rows if row.get('original_oracle_member') is True]
        if len(all_rows) != total or len(selected) != count:
            raise ValueError('baseline route membership/count differs: ' + route)
        resolved = sum((row.get('oracle_review') or {}).get('resolved') is True for row in selected)
        passes = sum(row.get('qualified_host_lifecycle_pass') is True for row in all_rows)
        if resolved != 1 or passes != 1:
            raise ValueError('baseline canonical resolution/lifecycle count differs: ' + route)
        canonical_counts[route] = {'resolved': resolved, 'open': count - resolved, 'lifecycle_pass': passes}
        originals[route] = {row['run_scoped_case_id']: row for row in selected}
    references = References()
    documents, normalized, by_route = [], {}, {}
    for review_path in review_paths:
        review_path = Path(review_path)
        raw = evidence_io.read_bytes(review_path, (REPOSITORY, *STORAGE_ROOTS))
        document = json.loads(raw)
        route = document.get('route')
        if route not in ROUTES or route in by_route:
            raise ValueError('unknown or duplicate review route')
        if 'records' in document and 'rows' in document:
            raise ValueError('review has competing records/rows arrays')
        rows = document.get('records', document.get('rows'))
        if not isinstance(rows, list):
            raise ValueError('review requires records or rows')
        for flag in ('lifecycle_qualification_performed', 'canonical_oracle_inventory_changed'):
            if flag in document and document[flag] is not False:
                raise ValueError('source review cannot change lifecycle/canonical results')
        if document.get('summary', {}).get('new_lifecycle_pass', 0) != 0:
            raise ValueError('source review cannot invent lifecycle PASS')
        if baseline_hash is not None and document.get('baseline_sha256', baseline_hash) != baseline_hash:
            raise ValueError('review names a different baseline SHA256')
        document_refs = references.nested(document)
        ids = [row.get('run_scoped_case_id') for row in rows]
        if len(set(ids)) != len(ids):
            raise ValueError('duplicate reviewed original ID: ' + route)
        if set(ids) != set(originals[route]):
            raise ValueError('reviewed original-ID membership differs: ' + route)
        category_ids = {category: [] for category in sorted(CATEGORIES)}
        proposed, bindings, partial, boundary = [], [], [], []
        for row in rows:
            identity = row['run_scoped_case_id']
            original = originals[route][identity]
            if row.get('route') != route or not identity.startswith('I12::' + route + '::'):
                raise ValueError('review row route membership differs: ' + identity)
            if canonical(row.get('original_oracle')) != canonical(original['original_oracle']):
                raise ValueError('original oracle changed: ' + identity)
            if row.get('lifecycle_qualified') is not False:
                raise ValueError('lifecycle_qualified must be explicitly false: ' + identity)
            for flag in ('full_lifecycle_qualified', 'host_lifecycle_qualified', 'qualified_host_lifecycle_pass',
                         'canonical_ledger_resolution_changed'):
                if flag in row and row[flag] is not False:
                    raise ValueError('source row invents lifecycle/canonical result: ' + identity)
            if any(row.get(field) == 'PASS' for field in ('outcome', 'status', 'host_acceptance')):
                raise ValueError('source row cannot assign host PASS: ' + identity)
            existing = (original.get('oracle_review') or {}).get('resolved') is True
            if 'existing_canonical_oracle_resolved' in row and row['existing_canonical_oracle_resolved'] is not existing:
                raise ValueError('existing canonical oracle flag changed: ' + identity)
            category = row.get('category')
            if category not in CATEGORIES:
                raise ValueError('unknown source-review category: ' + identity)
            category_ids[category].append(identity)
            refs = row.get('source_refs')
            if not isinstance(refs, list) or not refs:
                raise ValueError('every original oracle needs source references: ' + identity)
            checked_source = [references.check(reference, source=True) for reference in refs]
            binding = row.get('fixture_binding')
            checked_binding = []
            new_binding = False
            if binding is not None:
                if not isinstance(binding, dict):
                    raise ValueError('fixture binding must be an object: ' + identity)
                for field in ('original_id', 'run_scoped_case_id'):
                    if field in binding and binding[field] != identity:
                        raise ValueError('fixture binding names a different original ID: ' + identity)
                if 'route' in binding and binding['route'] != route:
                    raise ValueError('fixture binding route differs: ' + identity)
                checked_binding = references.nested(binding)
                if not checked_binding:
                    raise ValueError('fixture binding has no physical references: ' + identity)
                new_binding = binding.get('origin') == 'new_task_fixture_binding'
                if new_binding:
                    if not any(field in binding for field in ('original_id', 'run_scoped_case_id')):
                        raise ValueError('new binding requires an explicit original ID: ' + identity)
                    bindings.append(identity)
            effective = row.get('effective_oracle')
            if effective is not None and not isinstance(effective, dict):
                raise ValueError('effective oracle must be an object or null: ' + identity)
            oracle_ready = (category == 'SOURCE_SEMANTICS_CONFIRMED' and bool(effective)
                            and row.get('source_oracle_resolved', True) is True)
            if oracle_ready and not existing and not new_binding:
                raise ValueError('new source oracle lacks an explicit new fixture binding: ' + identity)
            if row.get('source_oracle_resolved') is True and not oracle_ready:
                raise ValueError('source_oracle_resolved contradicts category/effective oracle: ' + identity)
            if oracle_ready and not existing:
                proposed.append(identity)
            elif effective and not existing:
                partial.append(identity)
            elif category == 'SOURCE_SEMANTICS_CONFIRMED' and not existing:
                boundary.append(identity)
            canonical_effective = (original.get('oracle_review') or {}).get('effective_oracle')
            if existing and canonical_effective is not None and canonical(effective) != canonical(canonical_effective):
                raise ValueError('existing canonical effective oracle changed: ' + identity)
            remaining = row.get('remaining_requirements')
            if not isinstance(remaining, list) or not remaining or any(not isinstance(value, str) for value in remaining):
                raise ValueError('remaining host requirements must remain explicit: ' + identity)
            normalized[identity] = {'run_scoped_case_id': identity, 'route': route, 'category': category,
                'original_oracle': copy.deepcopy(original['original_oracle']),
                'canonical_oracle_resolved': existing, 'canonical_effective_oracle': copy.deepcopy(canonical_effective),
                'effective_source_proposal': copy.deepcopy(effective),
                'proposed_new_source_oracle': identity in proposed,
                'source_refs': checked_source,
                'fixture_binding': None if binding is None else {'origin': binding.get('origin'),
                    'original_id': identity, 'references': checked_binding},
                'remaining_requirements': list(remaining), 'lifecycle_qualified': False,
                'canonical_resolution_changed': False, 'review_file': str(review_path)}
        by_route[route] = {'original_count': len(originals[route]), 'reviewed_count': len(rows),
            'canonical_resolved': canonical_counts[route]['resolved'], 'canonical_open': canonical_counts[route]['open'],
            'existing_lifecycle_pass': canonical_counts[route]['lifecycle_pass'],
            'proposed_new_source_oracles': len(proposed), 'proposed_new_source_oracle_ids': sorted(proposed),
            'new_fixture_binding_ids': sorted(bindings), 'partial_oracle_proposal_ids': sorted(partial),
            'source_boundary_only_ids': sorted(boundary),
            'categories': {key: len(value) for key, value in category_ids.items()},
            'category_ids': {key: sorted(value) for key, value in category_ids.items()}}
        documents.append({'path': str(review_path), 'sha256': hashlib.sha256(raw).hexdigest(),
                          'physical_reference_occurrences_verified': len(document_refs)})
    if set(by_route) != set(ROUTES) or len(normalized) != 125:
        raise ValueError('all three complete route reviews and all 125 original oracles are required')
    return {'schema': 'i12.envoy.validated-source-proposals.v1', 'baseline_total_ids': 284,
        'original_count': 125, 'reviewed_count': len(normalized),
        'canonical_resolved': 3, 'canonical_open': 122, 'existing_lifecycle_pass': 3,
        'canonical_resolution_changed': False, 'new_lifecycle_pass': 0,
        'proposal_scope': 'Source proposals only; canonical oracle resolution and host qualification are unchanged.',
        'proposed_new_source_oracles': sum(value['proposed_new_source_oracles'] for value in by_route.values()),
        'routes': by_route, 'input_reviews': documents,
        'normalized_rows': [normalized[row['run_scoped_case_id']] for row in baseline_rows
                            if row.get('original_oracle_member') is True]}


def main():
    import qualify_originals

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--review', type=Path, action='append', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = validate(args.baseline, args.review)
    qualify_originals.write(args.output, result)
    print(json.dumps({'original_count': result['original_count'], 'reviewed_count': result['reviewed_count'],
        'canonical_resolved': 3, 'canonical_open': 122,
        'proposed_new_source_oracles': result['proposed_new_source_oracles'], 'new_lifecycle_pass': 0}))


if __name__ == '__main__':
    main()
