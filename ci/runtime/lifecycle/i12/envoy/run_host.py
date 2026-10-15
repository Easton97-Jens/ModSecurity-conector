#!/usr/bin/env python3
"""Run sealed Envoy cases sequentially; retain failures without assigning PASS."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import subprocess
import os
import signal
import time


def identity(pid):
    try:
        value = Path('/proc/' + str(pid) + '/stat').read_text()
        return value[value.rfind(')') + 2:].split()[19]
    except (OSError, IndexError):
        return None


def signal_owned_group(process, started, value):
    # The unreaped direct child and its start time bind this process group.
    # Never signal a numeric process group after losing that identity.
    if started is None or identity(process.pid) != started:
        return False
    try:
        if os.getpgid(process.pid) != process.pid:
            return False
        os.killpg(process.pid, value)
        return True
    except ProcessLookupError:
        return False


def communicate_bounded(process, started):
    state = {'outer_timeout': False, 'cleanup_grace_timeout': False,
             'cleanup_requires_review': False, 'owned_process_start': started}
    try:
        out, err = process.communicate(timeout=300)
    except subprocess.TimeoutExpired as first:
        state['outer_timeout'] = True
        state['term_sent_to_owned_group'] = signal_owned_group(process, started, signal.SIGTERM)
        try:
            out, err = process.communicate(timeout=30)
        except subprocess.TimeoutExpired as second:
            state['cleanup_grace_timeout'] = state['cleanup_requires_review'] = True
            state['kill_sent_to_owned_group'] = signal_owned_group(process, started, signal.SIGKILL)
            out, err = second.stdout or first.stdout or b'', second.stderr or first.stderr or b''
            try:
                # Reap the direct child even if a detached descendant retains a pipe.
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                state['direct_child_reaped'] = False
            else:
                state['direct_child_reaped'] = True
            finally:
                process.stdout.close()
                process.stderr.close()
    return out, err, state


def controller_packets(stdout):
    packets, errors = [], 0
    for line in stdout.splitlines():
        if line.startswith('{"attempt":'):
            try:
                packets.append(json.loads(line))
            except json.JSONDecodeError:
                errors += 1
    return packets, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--matrix', type=Path, required=True)
    parser.add_argument('--only', action='append', default=[])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--workers', type=int, choices=(1, 2, 3), default=1,
                        help='Cases have disjoint private PID/net/mount namespaces and data roots')
    args = parser.parse_args()
    matrix = json.loads(args.matrix.read_text())
    cases = [case for case in matrix['scenarios'] if not args.only or case['label'] in args.only]
    if not cases or set(args.only) - {case['label'] for case in cases}:
        parser.error('unknown or empty case selection')
    if args.output.exists(): parser.error('fresh output required')
    controller = Path(matrix['controller'])
    if hashlib.sha256(controller.read_bytes()).hexdigest() != matrix['controller_sha256']:
        raise ValueError('controller changed after preparation')
    result = {'parent_sha': matrix['parent_sha'], 'qualification': 'unreviewed_host_measurements', 'runs': []}
    failures = 0
    def execute(case):
        argv = ['rtk', 'proxy', '/usr/local/bin/python3', '-I', str(controller), case['spec']]
        started = time.time_ns()
        # Controller has its own setup/run deadline, resource monitor and reap.
        # Outer timeout leaves that normal controller cleanup time to finish.
        process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        out, err, timeout_state = communicate_bounded(process, identity(process.pid))
        stdout, stderr = out.decode(errors='replace'), err.decode(errors='replace')
        output = args.output.parent / (args.output.stem + '-' + case['label'])
        output.with_suffix('.stdout').write_bytes(out)
        output.with_suffix('.stderr').write_bytes(err)
        packets, packet_errors = controller_packets(stdout)
        record = {'case': case, 'argv': argv, 'started_ns': started, 'finished_ns': time.time_ns(),
                  'exit_code': 124 if timeout_state['outer_timeout'] else (125 if packet_errors else process.returncode),
                  'process_exit_code': process.returncode, 'timeout_state': timeout_state,
                  'controller_packet_parse_errors': packet_errors,
                  'controller_result': packets[-1] if packets else None,
                  'stdout_sha256': hashlib.sha256(out).hexdigest(),
                  'stderr_sha256': hashlib.sha256(err).hexdigest()}
        return record
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for future in as_completed([pool.submit(execute, case) for case in cases]):
            record = future.result()
            result['runs'].append(record)
            args.output.write_text(json.dumps(result, indent=2) + '\n')
            print(json.dumps({'label': record['case']['label'], 'exit_code': record['exit_code'],
                              'attempt': record['controller_result']}), flush=True)
            failures += record['exit_code'] != 0
    raise SystemExit(1 if failures else 0)


if __name__ == '__main__':
    main()
