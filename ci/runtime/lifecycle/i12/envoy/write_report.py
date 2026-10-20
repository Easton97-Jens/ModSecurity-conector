#!/usr/bin/env python3
"""Write this Envoy task's EN/DE reports; never modify the shared I12 ledger."""
import argparse
import json
from pathlib import Path
import validate_oracles
import qualify_originals
import evidence_io
import current_base_evidence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
STEM = 'i12-envoy-host-evidence-20261015'


def reference(path):
    return evidence_io.reference(path)


def load(path):
    return evidence_io.read_json(path)


def validate_controls_receipt(path):
    receipt = load(path)
    expected_argv = [
        'rtk', 'proxy', '/root/git/ModSecurity-conector/.venv/bin/python', '-B',
        '-m', 'unittest', '-v', 'tests.test_i12_envoy_evidence'
    ]
    if (receipt.get('schema_version') != 1 or receipt.get('argv') != expected_argv or
            receipt.get('cwd') != str(ROOT) or receipt.get('exit_code') != 0 or
            receipt.get('tests') != 232 or receipt.get('skips') != 0):
        raise ValueError('current complete Envoy control receipt is not a 232-test PASS')
    if set(receipt.get('logs', {})) != {'stdout', 'stderr'}:
        raise ValueError('control receipt must retain both raw logs')
    for log in receipt['logs'].values():
        if reference(Path(log['path'])) != log:
            raise ValueError('control receipt raw log changed')
    sources = sorted((ROOT / 'ci/runtime/lifecycle/i12/envoy').glob('*.py'))
    sources.append(ROOT / 'tests/test_i12_envoy_evidence.py')
    expected_sources = {str(source.relative_to(ROOT)): reference(source)['sha256']
                        for source in sources}
    if receipt.get('source_sha256') != expected_sources:
        raise ValueError('control receipt source hashes are stale')
    return receipt


def encode_report(data):
    """Keep one inspectable record per original ID or host run in large arrays."""
    lines = ['{']
    for index, (key, value) in enumerate(data.items()):
        prefix = '  ' + json.dumps(key) + ': '
        if key in ('original_ids', 'host_measurements', 'qualified_originals'):
            lines.append(prefix + '[')
            lines.extend('    ' + json.dumps(item, separators=(',', ':'))
                         + (',' if item_index + 1 < len(value) else '')
                         for item_index, item in enumerate(value))
            lines.append('  ]')
        else:
            rendered = json.dumps(value, indent=2).splitlines()
            lines.append(prefix + rendered[0])
            lines.extend('  ' + line for line in rendered[1:])
        if index + 1 < len(data):
            lines[-1] += ','
    result = '\n'.join(lines + ['}', ''])
    if json.loads(result) != data:
        raise ValueError('report serialization changed evidence')
    return result


def additional_findings(data, german):
    lines = [('## Unabhängige Oracle-Prüfung und Original-ID-Retakes' if german else
              '## Independent oracle review and original-ID retakes'), '',
        ('Alle 125 Original-Oracles wurden einzeln gegen Quell-, SDK- und Hostsemantik geprüft. Die drei Envoy-eigenen Reviewdateien erhalten die Original-Oracles unverändert. Konkrete neue Fixture-/Erwartungsvorschläge stehen getrennt von kanonischer Auflösung und Hostabnahme:' if german else
         'All 125 original oracles were individually reviewed against source, SDK and host semantics. The three Envoy-owned review files preserve original oracles unchanged. Concrete new fixture/expectation proposals remain separate from canonical resolution and host acceptance:'), '',
        '| Route | Reviewed original oracles | New source proposals | Retaken original IDs |', '| --- | ---: | ---: | ---: |']
    for route, values in data['source_oracle_progress']['routes'].items():
        retakes = data['original_id_retakes']['routes'].get(route, {})
        lines.append(f"| {route} | {values['reviewed_count']} | {values['proposed_new_source_oracles']} | {retakes.get('unique_original_ids', 0)} |")
    lines += ['', ('Neue individuell geprüfte Lifecycle-PASS:' if german else 'New individually reviewed lifecycle PASS:'), '']
    lines.extend('- `' + item['run_scoped_case_id'] + '` — `' + item['receipt']['sha256'] + '`.'
                 for item in data['qualified_originals'])
    current = data['current_oracle_result']
    lines += ['', ('Der eigene aktuelle Abnahmestand hat ' if german else 'This task’s current acceptance state has ')
              + str(current['resolved']) + (' aufgelöste und ' if german else ' resolved and ')
              + str(current['open']) + (' offene Original-Oracles. Der zentrale Baseline-Bestand bleibt unverändert.' if german else
                                       ' open original oracles. The central baseline inventory remains unchanged.')]
    lines += ['', ('Jeder neue Vorschlag hat eine explizite Original-ID-/Fixture-Bindung und physische Quellreferenzen. Die zugehörigen Retakes bleiben bis zur vollständigen Prüfung aller fallbezogenen Nachweise unqualifiziert; auch ein passendes HTTP-Ergebnis löst kein Original-Oracle automatisch auf.' if german else
         'Every new proposal has an explicit original-ID/fixture binding and physical source references. Associated retakes remain unqualified until every case-specific proof is reviewed; even a matching HTTP result does not automatically resolve an original oracle.'), '',
        ('Die Postcommit-Proben synchronisieren den absichtlichen Backend-EOF mit einer tatsächlichen Client-Receipt des ersten Entitybytes. ext_proc und Companion liefern jeweils HTTP 200/32 Bodybytes vor unvollständigem Chunk-Framing. Der Client endet mit Fehler; der erste physische Common-Fehler bleibt protocol_error mit originalem/sichtbarem Status 200 und gesetztem Commit. Free/Cleanup sind beobachtet; ein erfolgreicher runtime_finish wird dafür nicht erfunden.' if german else
         'Postcommit probes synchronize deliberate backend EOF with an actual client receipt of the first entity byte. ext_proc and companion each deliver HTTP 200/32 body bytes before incomplete chunk framing. The client exits with an error; the first physical Common error remains protocol_error with original/visible status 200 and commitment set. Free/cleanup are observed; successful runtime_finish is not invented.'), '',
        ('Die vollständige Bilingual-Prüfung endet mit Exit 2 wegen 22 unveränderter Links in den nicht initialisierten Framework-Gitlink dieses Worktrees. Die Parent-Sprachverträge und sämtliche neuen Dokumentlinks bestehen die abgegrenzte API-Prüfung. Das ist kein globales Bilingual-PASS. Alle 2.105 Buildquellen wurden unabhängig aus dem archivierten Parent und den Capture-Overlays rekonstruiert; Fall-/Routen-/Parent-Austausch und der äußere Timeoutpfad haben eigene Negativkontrollen.' if german else
         'The complete bilingual check exits 2 because 22 unchanged links target this worktree’s uninitialized Framework gitlink. Parent language contracts and every new document link pass the scoped API check. This is not a global bilingual PASS. All 2,105 build sources were independently reconstructed from the archived Parent and capture overlays; case/route/Parent substitution and the outer timeout path have dedicated negative controls.'), '']
    return lines


def qualified_heading(german):
    return [
        '',
        'Exakt qualifizierte IDs:' if german else 'Exact qualified IDs:',
        ''
    ]


def host_intro(german):
    return [
        '',
        'Die erhaltene Baseline enthielt 281 IDs ohne vollständige Hostabnahme: 8 reine Konfigurations-PASS und 273 unqualifizierte Fälle. Von den ursprünglichen 125 offenen Oracles waren 3 aufgelöst und 122 offen. Die erhaltene Baseline und ihre physischen Quellen wurden mit den aktuellen zentralen Validatoren erneut geprüft. Dieser Envoy-Task änderte keinen gemeinsamen Validator. Neue Qualifikationen stehen separat mit ihren vollständigen Receipts im aktuellen Stand oben.' if german else
                   'The retained baseline contained 281 IDs without full host acceptance: 8 configuration-only PASS and 273 unqualified cases. Of the original 125 open oracles, 3 were resolved and 122 open. The retained baseline and its physical sources were revalidated with the current central validators. This Envoy task modified no shared validator. New qualifications are recorded separately with full receipts in the current state above.',
        '',
        '## Neue physische Hostmessungen' if german else '## New physical host measurements',
        '',
        'Jede Zeile ist eine gemessene Probe, kein Lifecycle-Verdikt. HTTP/Framing, Transportabschluss, native Phasen und Cleanup bleiben getrennt. Frühere Fehlversuche und Wiederholungen bleiben sichtbar. Bei Envoy ext_proc kann bereits vor einem P2-Deny ein unvollständiger Backendrequest beginnen.' if german else
         'Each row is a measured probe, not a lifecycle verdict. HTTP/framing, transport closure, native phases and cleanup remain separate. Earlier failed attempts and retakes remain visible. Envoy ext_proc can begin an incomplete backend request before a P2 deny.',
        '',
        '| Batch / probe | Route | Runner exit | Target HTTP | Neighbor HTTP | Backend starts | Overlap |'
    ]


def native_identity(data, german):
    return [
        '',
        '`None` bezeichnet fehlende Messung. Ein unterer Backend-Zähler bleibt in JSON ausdrücklich als `request_count_is_lower_bound` gekennzeichnet. Runner-Exit 0 ist keine Oracle-Abnahme; Exit 77 bleibt Nicht-PASS.' if german else
                   '`None` denotes a missing measurement. A lower-bound backend count remains explicitly marked `request_count_is_lower_bound` in JSON. Runner exit 0 is not oracle acceptance; exit 77 remains non-PASS.',
        '',
        '## Native Identität und Nachweiskette' if german else '## Native identity and evidence chain',
        '',
        ('- Quellrevision der nativen/Hostevidenz: `' if german else '- Native/host evidence source revision: `') + data['parent_sha'] + '`.',
        '- Envoy: `b579d07d3ad7ee11d32b105e91a5a39ad24718d7/1.39.1/Clean/RELEASE/BoringSSL`.',
        '- Envoy image SHA256: `002c6e1c69ed0fa0ea381887247cadadfaec9481375fa8d8d2b1731eeabf40b8`.'
    ]


def fault_probe_findings(data, german):
    probes = [item for item in data['host_measurements'] if 'fault_proxy' in item]
    if not probes:
        return []
    if len(probes) != 1:
        raise ValueError('exactly one independently reviewed fault probe expected')
    item = probes[0]
    fault = item['fault_proxy']
    status = fault['envoy_received_status']
    client = fault['target_client_incomplete_response']
    target_client = item['clients']['target']
    neighbor_client = item['clients']['neighbor']
    target_scopes = [scope for scope in item['native']['scopes']
                     if scope['completed_transition_count'] == 0]
    neighbor_scopes = [scope for scope in item['native']['scopes']
                       if scope['completed_transition_count'] == 1]
    if len(target_scopes) != 1 or len(neighbor_scopes) != 1:
        raise ValueError('fault target and healthy neighbor native scopes must remain distinct')
    target, neighbor = target_scopes[0], neighbor_scopes[0]
    target_counts = target['observed_return_counts']
    neighbor_counts = neighbor['observed_return_counts']
    target_chunks = [row['body_bytes'] for row in target['typed_body_callbacks']
                     if row.get('operation') == 1 and row.get('response_direction') == 1]
    required = [
        fault['host_lifecycle_qualified'] is False,
        fault['new_lifecycle_pass'] == 0,
        all(fault['source_contract_checks'].values()),
        status['grpc_status'] == 14 and status['successful_grpc_completion'] is False,
        fault['target']['remote_wire_status_observed'] is False,
        client['framing_complete'] is False and client['terminal_zero_chunk_observed'] is False,
        client['entity_prefix_bytes'] == 96 and client['complete_chunk_sizes'] == [64, 32],
        target_client['raw_http_status'] == 200 and target_client['process_exit'] == 1,
        neighbor_client['raw_http_status'] == 200 and neighbor_client['process_exit'] == 0,
        item['runner_exit_code'] == 77 and item['controller']['exitcode'] == 1,
        item['controller']['surviving_namespace_pid_count'] == 0,
        item['controller']['outside_mount_leak_count'] == 0,
        item['driver']['remaining_owned_process_count'] == 0,
        target_chunks == [64, 32],
        target_counts.get('native_process_request_headers') == 1,
        target_counts.get('native_process_request_body') == 1,
        target_counts.get('native_process_response_headers') == 1,
        target_counts.get('native_process_response_body', 0) == 0,
        target['return_result_counts']['runtime_finish'] == {'0': 1},
        target_counts.get('native_process_logging') == 1,
        target_counts.get('native_cleanup') == 1,
        target_counts.get('common_cleanup') == 1,
        neighbor_counts.get('native_process_response_body') == 1,
        neighbor['return_result_counts']['runtime_finish'] == {'1': 1},
    ]
    if not all(required):
        raise ValueError('fault probe lost a required independent physical observation')
    if german:
        text = (
            'Die gerichtete echte `envoy-ext-proc`-Probe entfernt ausschließlich das leere '
            'Response-EOS des Zielstreams und führt danach den tatsächlichen gRPC-Half-Close aus. '
            'Die Engine liefert API-Status 14. Envoys eigener Trace bindet den empfangenen Trailer, '
            'Remote-Close und Fehlercallback mit Status 14 über Ziel-Nonce, Connection-ID und Stream-ID '
            'an denselben HTTP-Stream; danach folgt ein Reset, nachdem HTTP-200-Header bereits gesendet '
            'waren. Der Proxy beobachtet weiterhin keinen Wire-Status und erfindet daraus keinen Erfolg. '
            'Der Zielclient erhält den exakten 96-Byte-Prefix in Chunks 64+32, aber keinen terminalen '
            'Nullchunk, und endet mit Fehler. Nativ laufen P1–P3; P4 und Response-EOS fehlen, '
            '`runtime_finish` wird einmal versucht und liefert 0, während Logging, Free und Cleanup je '
            'einmal beobachtet werden. Der Nachbarstream schließt mit P1–P4 und erfolgreichem Finish. '
            'Runner-Exit 77, Controller-Exit 1, Client-Exit 1 und `new_lifecycle_pass=0` bleiben erhalten.'
        )
        heading = '## Gerichtete Response-EOS-Fehlerprobe'
    else:
        text = (
            'The directed real `envoy-ext-proc` probe removes only the target stream’s empty response '
            'EOS and then performs the actual gRPC half-close. The engine returns API status 14. '
            'Envoy’s own trace binds the received status-14 trailer, remote close and error callback to '
            'the same HTTP stream through the target nonce, connection ID and stream ID; a reset follows '
            'after HTTP 200 headers were already sent. The proxy still observes no wire status and does '
            'not turn that absence into success. The target client receives the exact 96-byte prefix in '
            '64+32 chunks but no terminal zero chunk, then exits with an error. Native P1–P3 run; P4 and '
            'response EOS are absent, `runtime_finish` is attempted once and returns 0, while logging, '
            'free and cleanup are each observed once. The neighbor stream completes P1–P4 with a '
            'successful finish. Runner exit 77, controller exit 1, client exit 1 and '
            '`new_lifecycle_pass=0` are retained.'
        )
        heading = '## Directed response-EOS fault probe'
    return ['', heading, '', text, '']


def native_capture(german):
    return [
        '- SDK: `ModSecurity v3.0.14 (Linux)`; SHA256 `32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407`.',
        '- Go: `go1.27.2`; `go.mod`: `go 1.26.9`; `golang.org/x/net v0.61.0`.',
        '',
        'Die frische C17-/C++17-/CGo-Erzeugung nutzt dieselbe Envoy-Capture-Variante und den gemeinsamen Observer. Quellkopie, acht Overlays, geladene Images, effektive Konfiguration, getrennte echte Clients/Backend, native Scopes, tatsächliche EOS-Argumente, P1–P4, Logging/Free, Finish-Aufrufe und physische Eventlogs sind hashgebunden. Pro normaler Transaktion sind native Logging/Free und logischer Finish-Übergang jeweils einmal zu prüfen; zwei idempotente Common-Finish-Aufrufe sind kein doppelter Übergang.' if german else
         'The fresh C17/C++17/CGo build uses the same Envoy capture variant and common observer. Source copy, eight overlays, loaded images, effective configuration, separate real clients/backend, native scopes, actual EOS arguments, P1–P4, logging/free, Finish calls and physical event logs are hash-bound. A normal transaction needs one native logging/free and one logical Finish transition; two idempotent Common Finish calls are not two transitions.',
        '',
        'Eine abgeschlossene HTTP-Entity kann von einem TCP-Reset gefolgt werden. Ein beobachteter lokaler HTTP/2-Reset belegt keinen Remote-`grpc-status`. Fehlt dieser Status, bleibt erfolgreicher gRPC-Abschluss false/unknown. Authorization-Erfolg braucht explizite Trailer und den zugehörigen Streamabschluss.' if german else
         'A complete HTTP entity can be followed by a TCP reset. An observed local HTTP/2 reset does not prove remote `grpc-status`. With that status absent, successful gRPC completion remains false/unknown. Authorization success requires explicit trailers and the associated stream close.',
        '',
        '## Request-Sample und Response-Companion' if german else '## Request sample and response companion'
    ]


def sample_companion_cleanup(german):
    return [
        '',
        '`max_request_bytes` ist die Hostbuffer-Grenze. Die nativen Limitproben verwenden eine vollständige Probe unterhalb der größeren Hostkapazität. Host-413 vor der Engine, verworfene Partial-Metadaten mit technischem gRPC-Fehler, native 403-Intervention und echte Backendwirkung werden getrennt erfasst. Mehrere Client-Schreibvorgänge sind bei Authorization/Check keine mehreren Engine-Bodycallbacks.' if german else
         '`max_request_bytes` is the host buffer boundary. Native limit probes use a complete sample below the larger host capacity. Host 413 before the engine, rejected partial metadata with a technical gRPC error, native 403 intervention and actual backend effects are recorded separately. Multiple client writes are not multiple engine body callbacks for Authorization/Check.',
        '',
        'Der Companion hat eigene Läufe für P3/P4, Streaming, native Response-Limits, fehlende/abgelaufene Leases und Cancellation. Die gleiche HTTP-Receipt qualifiziert Request und Response nicht automatisch gemeinsam. Zeitliche Client-Überlappung belegt nur die beobachtete Parallelität; eine mehrdeutige gRPC-Zuordnung bleibt unbekannt.' if german else
         'The companion has its own runs for P3/P4, streaming, native response limits, missing/expired leases and cancellation. One shared HTTP receipt does not automatically qualify request and response together. Client timing overlap proves only the observed concurrency; ambiguous gRPC correlation remains unknown.',
        '',
        '## Cleanup und Isolation' if german else '## Cleanup and isolation',
        '',
        'UID/GID 65534, Capabilities 0, NoNewPrivs 1 sowie private Netzwerk-/PID-/Mount-Namespaces und die Listenergrenzen bleiben erhalten. Ein alter v5-Lauf meldete einen fremden Traefik-Prozess als Survivor; dessen Identität und Namespace-ID sprechen für eine Wiederverwendung der Namespace-ID nach Ende des Envoy-Laufs. Dieser Prozess wurde nicht signalisiert; der ursprüngliche Exit 77 bleibt erhalten. Die Envoy-spezifische Controllerkopie hält jetzt einen positiv an die eigene Init-Identität gebundenen Namespace-FD bis nach Cleanup offen, validiert die Identität vor/nach Open und behandelt nicht belegbare Ownership als Fehler.' if german else
         'UID/GID 65534, zero capabilities, NoNewPrivs 1, private network/PID/mount namespaces and listener boundaries are preserved. An old v5 run misclassified a foreign Traefik process as a survivor; its identity and namespace inode support inferred namespace-ID reuse after the Envoy run ended. It was not signalled; original exit 77 is retained. The Envoy-specific controller copy now holds a namespace FD positively bound to its own init through cleanup, revalidates identity before/after open and treats unprovable ownership as an error.'
    ]


def verification_limits(german):
    return [
        '',
        '## Verifikation und Grenzen' if german else '## Verification and limits',
        '',
        'Native/CGo Go `./...`, Race `./...`, Vet `./...` und 32 gemeinsame native Observer-Kontrollen: PASS. Die aktuelle vollständige Envoy-Evidenzsuite hat 232 PASS ohne Skip. Neue Kontrollen prüfen unveränderte IDs/Oracles, physische Hashes, fehlende gRPC-Trailer, geordnete Streamweiterleitung, versiegelte Fault-Fixtures, Quell-/Binary-Austausch, Backend-Framing und Namespace-Ownership-Rennen. Exakte Kommandos, Ergebnisse und Loghashes stehen in den referenzierten Receipts.' if german else
         'Native/CGo Go `./...`, race `./...`, vet `./...` and 32 common native observer controls: PASS. The current complete Envoy evidence suite has 232 PASS with no skips. New controls cover unchanged IDs/oracles, physical hashes, absent gRPC trailers, ordered stream forwarding, sealed fault fixtures, substituted source/binaries, backend framing and namespace ownership races. Exact commands, outcomes and log hashes are in the referenced receipts.',
        '',
        'Offen bleiben die vollständige unabhängige Oracle-/Original-ID-Abnahme, direkte native MIME-/Charset-Auswahl, vollständig korrelierte parallele gRPC-Terminalstatus, gezielt fehlende/wiederholte Hostcallbacks, alle physischen Event-Sink-Fehler und der vollständige Observer-Stop/Restart-Vertrag. P4 Strict wird nicht als unterstützt oder abgenommen behauptet. Unit-, Native- und Race-Erfolg ersetzen diese Hostnachweise nicht.' if german else
         'Still open: complete independent oracle/original-ID acceptance, direct native MIME/charset selection, fully correlated concurrent gRPC terminal status, deliberate missing/repeated host callbacks, all physical event-sink failures and the complete observer stop/restart contract. P4 Strict is not claimed supported or accepted. Unit, native and race success do not replace these host proofs.',
        ''
    ]


def references_heading(german):
    return [
        '## Physische Referenzen' if german else '## Physical references',
        ''
    ]


def storage_footer(german):
    return [
        '',
        'Die Referenzen liegen im task-eigenen externen Speicher; der PR enthält nur Quellcode und bereinigte Metadaten, keine Binaries, Caches, privaten Schlüssel oder Rohpayloads.' if german else
                   'References reside in task-owned external storage; the PR contains source and sanitized metadata, not binaries, caches, private keys or raw payloads.',
        ''
    ]


def add_current_base_evidence(data, path):
    if path is None:
        return
    supplement = current_base_evidence.validate(path)
    data['current_base_evidence'] = supplement
    data['physical_inputs']['current_base_supplement'] = reference(path)


def current_base_findings(data, german):
    supplement = data.get('current_base_evidence')
    if supplement is None:
        return []
    heading = '## Ergänzende Hostproben auf der aktuellen Base' if german else '## Supplemental host probes on the current base'
    text = (
        'Die separat hashgebundene Ergänzung prüft die Base `' + supplement['parent_sha'] + '` '
        'mit dem von der Base geforderten Go 1.27.2 für den Enginebuild, x/net 0.61.0, ModSecurity 3.0.14 und Envoy 1.39.1. '
        'Die Hostumgebung meldet separat das installierte Go 1.27.3; diese Messung belegt keinen Enginebuild. '
        'Der frühere Enginebuild mit Go 1.27.3 und seine drei Hostproben bleiben als überholte, nicht qualifizierende Evidenz erhalten. '
        'Ein weiterer verworfener Build scheiterte vor dem Hoststart technisch an der Mischung aus Go-1.27.2-Treiber und Go-1.27.3-Compiler; Receipt und Fehlerlog bleiben hashgebunden erhalten. '
        'Drei frühere Admission-Fehler bleiben Exit 77 mit unbekannter Hostausführung und ohne Cleanup-Behauptung erhalten. '
        'Drei neue Streaming-Proben haben Runner-Exit 0 und physisch geprüftes Cleanup. '
        'Je Route sind Zielrequest/-response 95/96 Bytes, Nachbarrequest/-response 6/7 Bytes und zwei Backendrequests belegt. '
        'Die folgende Tabelle erhält den tatsächlich belegten Authorization-Status je Route und Client. '
        'Nicht zuordenbare Trailer bleiben unbekannt und erfolgreicher Abschluss false. '
        'Der fehlende Process-gRPC-Status bleibt unbekannt und erfolgreicher Abschluss false. '
        'Diese Proben qualifizieren keine Original-ID: `new_lifecycle_pass=0`. '
        'Die historischen Messungen, Retakes, Oracle-Zähler und die Quellrevision der bisherigen nativen Evidenz bleiben erhalten.'
        if german else
        'The separately hash-bound supplement checks base `' + supplement['parent_sha'] + '` '
        'with the Base-required Go 1.27.2 for the engine build, x/net 0.61.0, ModSecurity 3.0.14 and Envoy 1.39.1. '
        'The host environment separately reports installed Go 1.27.3; that measurement does not prove the engine build toolchain. '
        'The earlier engine build using Go 1.27.3 and its three host probes are retained as superseded, nonqualifying evidence. '
        'A further rejected build failed technically before host launch because it mixed a Go1.27.2 driver with a Go1.27.3 compiler; its receipt and error log remain hash-bound. '
        'Three earlier admission failures retain exit 77, unknown host execution and no cleanup claim. '
        'Three fresh streaming probes have runner exit 0 and physically verified cleanup. '
        'Each route proves target request/response 95/96 bytes, neighbor request/response 6/7 bytes and two backend requests. '
        'The following table retains the actually proven Authorization status for each route and client. '
        'Unscoped trailers remain unknown and successful completion false. '
        'The absent Process gRPC status remains unknown and successful completion false. '
        'These probes qualify no original ID: `new_lifecycle_pass=0`. '
        'Historical measurements, retakes, oracle counts and the prior native evidence source revision are retained.')
    lines = ['', heading, '', text, '',
        '| Route | Client | Authorization grpc-status | Successful completion |',
        '| --- | --- | --- | --- |']
    for route, roles in supplement['route_transport_observations'].items():
        for role, transport in roles.items():
            auth = transport['authorization']
            status = auth['remote_grpc_status']
            lines.append('| ' + route + ' | ' + role + ' | '
                         + ('unknown' if status is None else str(status)) + ' | '
                         + str(auth['successful_grpc_completion']).lower() + ' |')
    return lines + ['']


def report(data, german):
    language = f'**Sprache:** [English]({STEM}.md) | Deutsch' if german else f'**Language:** English | [Deutsch]({STEM}.de.md)'
    lines = [('# I12 Envoy: Hostmessungen und verbleibende Abnahme' if german else '# I12 Envoy: host measurements and remaining acceptance'), '', language, '',
        ('Status: **PARTIAL**. Die vollständige Abnahme aller 284 Originalfälle ist nicht erreicht.' if german else
         'Status: **PARTIAL**. Full acceptance of all 284 original cases has not been achieved.'), '',
        ('Quellrevision der nativen/Hostevidenz: ' if german else 'Native/host evidence source revision: ') + '`' + data['parent_sha'] + '`.', '',
        ('Die JSON-Begleitdatei erhält alle 284 exakten Original-IDs und ihre Baseline-Ergebnisse. Neue synthetische Hostproben haben eigene Identitäten; nur separat validierte, einzeln freigegebene vollständige Nachweispakete qualifizieren Originalfälle.' if german else
         'The companion JSON preserves all 284 exact original IDs and their baseline results. New synthetic host probes have their own identities; only separately validated, individually approved full packets qualify original cases.'), '',
        f'[{STEM}.json]({STEM}.json)', '',
        ('## Drei getrennte Routenergebnisse' if german else '## Three separate route results'), '',
        '| Route | Original IDs | Lifecycle PASS | Config PASS | Without lifecycle | Original oracles | Open |',
        '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for route, counts in data['current_route_results'].items():
        values = [counts['original_ids'], counts['lifecycle_pass'], counts['configuration_only_pass'],
                  counts['without_lifecycle'], counts['original_oracles'], counts['open_oracles']]
        lines.append('| ' + route + ' | ' + ' | '.join(map(str, values)) + ' |')
    lines += qualified_heading(german)
    for counts in data['current_route_results'].values():
        lines.extend('- `' + identity + '`' for identity in counts['qualified_case_ids'])
    lines += host_intro(german)
    lines.append('| --- | --- | ---: | ---: | ---: | ---: | --- |')
    for item in data['host_measurements']:
        clients = item.get('clients', {})
        status = lambda who: clients.get(who, {}).get('raw_http_status')
        lines.append('| ' + ' | '.join(map(str, [item['batch'] + '/' + item['scenario'], item['route'], item['runner_exit_code'],
            status('target'), status('neighbor'), item.get('backend', {}).get('request_count'), item.get('client_time_overlap_observed')])) + ' |')
    lines += fault_probe_findings(data, german)
    lines += native_identity(data, german)
    lines += native_capture(german)
    lines += sample_companion_cleanup(german)
    lines += verification_limits(german)
    lines += additional_findings(data, german)
    lines += current_base_findings(data, german)
    lines += references_heading(german)
    for label, value in data['physical_inputs'].items():
        lines.append('- `' + label + '`: `' + value['path'] + '` — SHA256 `' + value['sha256'] + '`.')
    lines += storage_footer(german)
    return '\n'.join(lines)


def add_route_results(data, baseline, qualified):
    data['current_route_results'] = {}
    for route, previous in baseline['routes'].items():
        added = [item['run_scoped_case_id'] for item in qualified if item['route'] == route]
        existing = previous['existing_pass_ids']
        if set(added) & set(existing):
            raise ValueError('existing qualification cannot count as new')
        data['current_route_results'][route] = {
            'original_ids': previous['original_ids'], 'baseline_lifecycle_pass': previous['existing_lifecycle_pass'],
            'new_lifecycle_pass': len(added), 'lifecycle_pass': previous['existing_lifecycle_pass'] + len(added),
            'configuration_only_pass': previous['configuration_only_pass'],
            'without_lifecycle': previous['original_ids'] - previous['existing_lifecycle_pass'] - len(added),
            'original_oracles': previous['original_oracles'], 'open_oracles': previous['open_original_oracles'] - len(added),
            'qualified_case_ids': existing + added}


def add_source_reviews(data, source_review, args):
    data['source_oracle_progress'] = {key: value for key, value in source_review.items() if key != 'normalized_rows'}
    source_rows = {row['run_scoped_case_id']: row for row in source_review['normalized_rows']}
    for row in data['original_ids']:
        if row['run_scoped_case_id'] in source_rows:
            reviewed = source_rows[row['run_scoped_case_id']]
            row['task_source_review'] = {key: reviewed[key] for key in ('category', 'proposed_new_source_oracle',
                'effective_source_proposal', 'remaining_requirements', 'lifecycle_qualified', 'review_file')}
    for path in args.oracle_review:
        data['physical_inputs'][path.stem] = reference(path)
    return source_rows


def add_host_measurements(data, paths):
    for path in paths:
        review = load(path)
        if review['parent_sha'] != data['parent_sha'] or review['host_lifecycle_qualified'] is not False:
            raise ValueError('review scope or source mismatch')
        data['physical_inputs'][path.stem] = reference(path)
        for item in review['scenarios']:
            kept = {key: item[key] for key in ('scenario', 'route', 'runner_exit_code', 'expected_http_status',
                'attempt', 'controller', 'observation_state', 'clients', 'backend', 'native', 'events',
                'grpc_transport', 'client_time_overlap_observed', 'artifact_integrity_issues', 'unknown',
                'original_oracle_case_ids', 'oracle_review_sha256', 'loaded_images', 'source_equality', 'build',
                'native_logs', 'command_exit_codes', 'driver', 'versions', 'fault_proxy') if key in item}
            kept['batch'] = Path(item['attempt']).parents[1].name
            kept['physical_file_hashes'] = item.get('physical_files', {})
            data['host_measurements'].append(kept)


def supplement_binding(supplement, path, source_rows):
    identity = supplement['original_id']
    original = source_rows.get(identity)
    rows = supplement.get('normalized_rows', [])
    if original is None or supplement['route'] != original['route']:
        raise ValueError('supplement claims an unreviewed or sibling original ID')
    if len(rows) != 1 or rows[0]['run_scoped_case_id'] != identity or rows[0]['route'] != original['route']:
        raise ValueError('supplement normalized row differs from exact original ID')
    if supplement['origin_review'] != reference(Path(original['review_file'])):
        raise ValueError('supplement origin differs from independently validated source review')
    if supplement['review_file'] != reference(path):
        raise ValueError('supplement differs from freshly validated physical review')
    if supplement['canonical_resolution_changed'] is not False or supplement['new_lifecycle_pass'] != 0:
        raise ValueError('supplement cannot assign canonical resolution or lifecycle PASS')
    return identity, supplement['review_file']['sha256']


def add_oracle_supplements(data, paths, source_review, source_rows):
    allowed, supplements = {}, []
    for path in paths:
        supplement = validate_oracles.validate_supplement(path, source_review)
        identity, sha = supplement_binding(supplement, path, source_rows)
        if identity in allowed or path.stem in data['physical_inputs']:
            raise ValueError('duplicate oracle supplement identity or physical input')
        allowed[identity] = {sha}
        supplements.append({key: value for key, value in supplement.items() if key != 'normalized_rows'})
        data['physical_inputs'][path.stem] = reference(path)
    if supplements:
        data['oracles_supplements'] = supplements
    return allowed


def add_retaken_ids(item, ids, source_rows, by_id, allowed_review_hashes=None):
    for identity in ids:
        if identity not in source_rows or source_rows[identity]['route'] != item['route']:
            raise ValueError('host observation claims an unreviewed or sibling original ID')
        review_path = Path(source_rows[identity]['review_file'])
        hashes = {reference(review_path)['sha256']}
        hashes.update((allowed_review_hashes or {}).get(identity, set()))
        if item.get('oracle_review_sha256') not in hashes:
            raise ValueError('host original-ID binding differs from independently verified review')
        by_id.setdefault(identity, []).append({key: item[key] for key in (
            'batch', 'scenario', 'runner_exit_code', 'attempt', 'observation_state')})


def add_original_retakes(data, source_rows, allowed_review_hashes=None):
    by_id = {}
    route_ids, route_runs = {}, {}
    for item in data['host_measurements']:
        ids = item.get('original_oracle_case_ids', [])
        if not ids:
            continue
        route_runs[item['route']] = route_runs.get(item['route'], 0) + 1
        route_ids.setdefault(item['route'], set()).update(ids)
        add_retaken_ids(item, ids, source_rows, by_id, allowed_review_hashes)
    for row in data['original_ids']:
        row['current_task_execution_observed'] = row['run_scoped_case_id'] in by_id
        row['current_task_unqualified_host_runs'] = by_id.get(row['run_scoped_case_id'], [])
    data['original_id_retakes'] = {'unique_original_ids': len(by_id), 'host_runs': sum(route_runs.values()),
        'full_lifecycle_qualified': False,
        'routes': {route: {'unique_original_ids': len(ids), 'host_runs': route_runs[route],
                          'exact_original_ids': sorted(ids)} for route, ids in route_ids.items()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--review', type=Path, action='append', default=[])
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--validation', type=Path, required=True)
    parser.add_argument('--oracle-review', type=Path, action='append', required=True)
    parser.add_argument('--qualified', type=Path, action='append', default=[])
    parser.add_argument('--oracle-supplement', type=Path, action='append', default=[])
    parser.add_argument('--current-base-supplement', type=Path)
    args = parser.parse_args()
    baseline = load(args.baseline)
    native = load(args.native)
    validate_controls_receipt(args.validation)
    source_review = validate_oracles.validate(args.baseline, args.oracle_review)
    qualified = [qualify_originals.validate_approved(path) for path in args.qualified]
    if len({row['run_scoped_case_id'] for row in qualified}) != len(qualified):
        raise ValueError('duplicate individually qualified original ID')
    if native['status'] != 'pass' or baseline['summary']['original_ids'] != 284:
        raise ValueError('validated baseline and passing native receipt required')
    data = {'schema': 'i12.envoy.task-report.v1', 'status': 'PARTIAL', 'parent_sha': native['actual_source_commit'],
            'routes': baseline['routes'], 'summary': baseline['summary'], 'new_original_id_qualifications': len(qualified),
            'physical_inputs': {'baseline': reference(args.baseline), 'native': reference(args.native),
                                'validation': reference(args.validation)},
            'original_ids': [{key: row[key] for key in ('run_scoped_case_id', 'leg_id', 'status', 'qualification_scope',
                'original_oracle_member', 'original_oracle', 'residual', 'existing_host_packet')} for row in baseline['rows']],
            'host_measurements': []}
    data['qualified_originals'] = qualified
    add_route_results(data, baseline, qualified)
    data['current_oracle_result'] = {'resolved': 3 + len(qualified), 'open': 122 - len(qualified),
                                     'baseline_unchanged': True}
    data['baseline_summary'] = data.pop('summary')
    data['baseline_routes'] = data.pop('routes')
    data['summary'] = {'original_ids': 284, 'lifecycle_pass': 3 + len(qualified),
        'configuration_only_pass': 8, 'without_full_lifecycle': 281 - len(qualified),
        'unqualified': 273 - len(qualified), 'original_oracles': 125,
        'resolved_original_oracles': 3 + len(qualified), 'open_original_oracles': 122 - len(qualified)}
    qualified_by_id = {item['run_scoped_case_id']: item for item in qualified}
    for row in data['original_ids']:
        item = qualified_by_id.get(row['run_scoped_case_id'])
        row['current_task_qualification'] = item
    for path in args.qualified:
        data['physical_inputs'][path.stem] = reference(path)
    source_rows = add_source_reviews(data, source_review, args)
    allowed_review_hashes = add_oracle_supplements(data, args.oracle_supplement, source_review, source_rows)
    add_host_measurements(data, args.review)
    add_original_retakes(data, source_rows, allowed_review_hashes)
    add_current_base_evidence(data, args.current_base_supplement)
    directory = ROOT / 'reports/testing'
    (directory / (STEM + '.json')).write_text(encode_report(data))
    for german in (False, True):
        (directory / (STEM + ('.de.md' if german else '.md'))).write_text(report(data, german))
    print(json.dumps({'status': data['status'], 'original_ids': len(data['original_ids']),
                      'host_measurements': len(data['host_measurements']), 'new_original_id_qualifications': len(qualified)}))


if __name__ == '__main__':
    main()
