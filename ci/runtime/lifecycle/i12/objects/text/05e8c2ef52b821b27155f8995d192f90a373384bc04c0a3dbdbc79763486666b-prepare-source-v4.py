"""Retain source-v2; snapshot validated observer wall-clock sampling update."""
import hashlib
import json
from pathlib import Path
import shutil
BASE=Path(__file__).resolve().parent
WT=Path('/var/tmp/codex/ModSecurity-conector/worktrees/pr410-sonar-host-repair-20261014')
OUT=BASE/'source-v4';shutil.copytree(BASE/'source-v3',OUT)
for path in OUT.rglob('*'):path.chmod(0o700 if path.is_dir() else 0o600|(path.stat().st_mode&0o111))
OUT.chmod(0o700)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
relative=Path('ci/runtime/common/response-header-test-backend.py')
source=BASE/'response-header-test-backend.observed-v2.py'
assert sha(source)=='fdd8342fd7c0c4554309f7d4fe562f7efaa7368b32b3297224e55616a7833c16'
shutil.copyfile(source,OUT/relative)
files={str(path.relative_to(OUT)):sha(path) for path in OUT.rglob('*') if path.is_file()}
ledger=BASE/'source-v4-ledger.json';ledger.write_text(json.dumps({'files':files},indent=2,sort_keys=True)+'\n');ledger.chmod(0o444)
for path in OUT.rglob('*'):path.chmod(0o555 if path.is_dir() or path.stat().st_mode&0o111 else 0o444)
OUT.chmod(0o555)
(BASE/'source-v4-overlay-manifest.json').write_text(json.dumps({
    'previous_source_ledger_sha256':sha(BASE/'source-v3-ledger.json'),'source_ledger_sha256':sha(ledger),
    'changed_backend_source_sha256':sha(OUT/relative),
    'validated_control_receipt':str(BASE.parent/'native-observer-worker/control-09/receipt.json'),
    'purpose':'Transparent backend capture failures retain stderr while original response handler proceeds; same immutable module05 and observer API. Previous snapshots retained.',
    'host_launched':False},indent=2)+'\n')
print(json.dumps({'files':len(files),'source_ledger_sha256':sha(ledger)}))
