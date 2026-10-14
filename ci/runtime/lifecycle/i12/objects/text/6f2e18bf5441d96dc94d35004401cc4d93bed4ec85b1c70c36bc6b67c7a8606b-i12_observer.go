package native_middleware

// Private source-copy observer. Never add this file to a release artifact.
// Calls occur after real writer/reader/socket operations. Payloads, headers,
// URIs and error messages are never retained here; only the two synthetic
// probe IDs are admitted. No engine or host result is changed by observation.
import (
	"encoding/json"
	"log"
	"os"
	"time"
)

// Linux x86_64 O_NOFOLLOW: the pinned Yaegi host excludes syscall imports.
// Keep the actual kernel nofollow flag, not a path-check substitution.
const i12LinuxNoFollow = 0x20000

var i12ObserverEpoch = time.Now()
var i12ObserverPath = "/task/runtime/logs/host-lifecycle.jsonl"

func i12Observe(transactionID, operation string, fields map[string]interface{}) {
	if transactionID != "tf-eos-target-53b4c671" && transactionID != "tf-eos-neighbor-8f217a3c" {
		return
	}
	now := time.Now()
	record := map[string]interface{}{
		"schema": "traefik-host-observed-v1", "pid": os.Getpid(),
		"transaction_id": transactionID, "operation": operation,
		"wall_ns": now.UnixNano(), "epoch_wall_ns": i12ObserverEpoch.UnixNano(),
		"elapsed_monotonic_ns": now.Sub(i12ObserverEpoch).Nanoseconds(), "fields": fields,
	}
	encoded, err := json.Marshal(record)
	if err != nil || len(encoded) > 2048 || len(fields) > 8 {
		log.Print("i12-host-observer: invalid bounded record")
		return
	}
	file, err := os.OpenFile(i12ObserverPath, os.O_WRONLY|os.O_APPEND|i12LinuxNoFollow, 0)
	if err != nil {
		log.Print("i12-host-observer: descriptor admission failed")
		return
	}
	info, statErr := file.Stat()
	if statErr != nil || !info.Mode().IsRegular() || info.Mode().Perm() != 0600 || info.Size() > 1<<20 {
		_ = file.Close()
		log.Print("i12-host-observer: output identity or budget invalid")
		return
	}
	encoded = append(encoded, '\n')
	count, writeErr := file.Write(encoded)
	closeErr := file.Close()
	if writeErr != nil || count != len(encoded) || closeErr != nil {
		log.Print("i12-host-observer: physical write incomplete")
	}
}
