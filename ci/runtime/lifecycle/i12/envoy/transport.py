"""Keep observed local closure separate from successful remote gRPC status."""
import argparse
import importlib.util
import json
import re
from pathlib import Path
import sys


def authorization_observation(raw, path, host_logs):
    """Bind one unary completion independently of the companion Process stream."""
    unknown = {'verified': False}
    host = host_logs.extract(raw, path)
    if not host.get('scope_verified'):
        return unknown
    lines = raw.splitlines()
    start = host['decoded_nonce_original_line'] - 1
    end = next((i for i in range(start + 1, len(lines))
                if 'request headers complete (end_stream=' in lines[i]
                and 'conn_manager_impl.cc:' in lines[i]), len(lines))
    records = []
    for i in range(start, end):
        if not host_logs.STAMP.match(lines[i]):
            continue
        tag = host_logs.TAGS.search(lines[i])
        try:
            tags = json.loads('{' + tag.group(1) + '}') if tag else {}
        except json.JSONDecodeError:
            return unknown
        records.append({'original_line': i + 1, 'text': lines[i], 'tags': tags})
    methods = [r for r in records if 'router.cc:' in r['text'] and
               "match for URL '/envoy.service.auth.v3.Authorization/Check'" in r['text']]
    if len(methods) != 1 or not all(methods[0]['tags'].get(k) for k in ('ConnectionId', 'StreamId')):
        return unknown
    method = methods[0]
    # Stop at the next asynchronous method construction, before Process traffic.
    boundary = next((r['original_line'] for r in records
                     if r['original_line'] > method['original_line'] and
                     r['tags'].get('ConnectionId') == method['tags']['ConnectionId'] and
                     'router.cc:' in r['text'] and 'match for URL ' in r['text']), end + 1)
    rows = [r for r in records if method['original_line'] < r['original_line'] < boundary]
    payload = []
    for row in rows:
        match = re.search(r'Http2Visitor: remaining data payload: [1-9]\d*, stream_id: (\d+), end_stream: false', row['text'])
        if match and 'http2/codec_impl.cc:' in row['text']:
            payload.append((row['tags'].get('ConnectionId'), match.group(1), row))
    keys = {(c, s) for c, s, _ in payload}
    if len(keys) != 1 or not payload:
        return unknown
    connection, stream = next(iter(keys))
    if not connection:
        return unknown
    trailers = []
    for row in rows:
        if 'async_client_impl.cc:' not in row['text'] or not row['text'].endswith('async http request response trailers:'):
            continue
        if row['tags'] != method['tags']:
            return unknown
        i = row['original_line']
        block = []
        while i < boundary - 1 and not host_logs.STAMP.match(lines[i]):
            block.append(lines[i])
            i += 1
        statuses = [line for line in block if line.startswith("'grpc-status',")]
        if statuses != ["'grpc-status', '0'"]:
            return unknown
        trailers.append({'original_line': row['original_line'] + 1, 'text': statuses[0]})
    closes = [r for r in rows if r['tags'].get('ConnectionId') == connection
              and 'http2/codec_impl.cc:' in r['text']
              and re.search(r' stream ' + re.escape(stream) + r' closed: \d+$', r['text'])]
    if (len(trailers) != 1 or len(closes) != 1
            or not closes[0]['text'].endswith(' closed: 0')
            or not payload[-1][2]['original_line'] < trailers[0]['original_line'] < closes[0]['original_line']):
        return unknown
    return {'verified': True, 'method': method, 'http2_connection': connection,
            'http2_stream': stream, 'actual_success_trailer': trailers[0],
            'actual_stream_close': closes[0], 'downstream_actual_tags': host['actual_host_stream_tags']}


def terminal(observation, unary=None):
    """Classify the existing capture's explicit facts without filling unknowns."""
    process = {
        'method': 'ExternalProcessor/Process',
        'scope_verified': observation.get('verified') is True,
        'local_http2_close_code': observation.get('numeric_actual_close_code'),
        'remote_grpc_status': None,
        'successful_grpc_completion': False,
        'classification': 'unknown',
    }
    if (process['scope_verified'] and observation.get('actual_pool_request_reset')
            and observation.get('actual_sent_reset_callback')
            and observation.get('actual_stream_close')):
        process['classification'] = 'observed_local_reset'
    authorization = {'method': 'Authorization/Check', 'remote_grpc_status': None,
                     'successful_grpc_completion': False, 'classification': 'unknown'}
    if unary and unary.get('verified') is True:
        trailer = unary.get('actual_success_trailer', {}).get('text')
        close = unary.get('actual_stream_close', {}).get('text', '')
        if trailer == "'grpc-status', '0'" and close.endswith(' closed: 0'):
            authorization.update(remote_grpc_status=0, successful_grpc_completion=True,
                                 classification='explicit_remote_status_and_close')
    return {'process': process, 'authorization': authorization,
            'source_observation': observation, 'host_lifecycle_qualified': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--helpers', type=Path, required=True)
    parser.add_argument('--raw', type=Path, required=True)
    parser.add_argument('--path', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    # Only pure capture parsers are imported; the driver/backend are not run.
    sys.path.insert(0, str(args.helpers.resolve(strict=True)))
    module_path = args.helpers / 'grpc_stream_observations.py'
    spec = importlib.util.spec_from_file_location('envoy_grpc_capture', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    raw = args.raw.read_text()
    import host_log_observations
    result = terminal(module.observe(raw, args.path),
                      authorization_observation(raw, args.path, host_log_observations))
    with args.output.open('x') as output:
        json.dump(result, output, indent=2)
        output.write('\n')


if __name__ == '__main__':
    main()
