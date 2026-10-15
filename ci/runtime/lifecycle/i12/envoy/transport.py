"""Keep observed local closure separate from successful remote gRPC status."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys


def terminal(observation):
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
    unary = observation.get('unary_authorization_grpc_end')
    authorization = {'method': 'Authorization/Check', 'remote_grpc_status': None,
                     'successful_grpc_completion': False, 'classification': 'unknown'}
    if process['scope_verified'] and unary:
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
    result = terminal(module.observe(args.raw.read_text(), args.path))
    with args.output.open('x') as output:
        json.dump(result, output, indent=2)
        output.write('\n')


if __name__ == '__main__':
    main()
