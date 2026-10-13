"""Apply fixed child log/descriptor bounds before executing an owned command."""
import os
import resource
import sys

resource.setrlimit(resource.RLIMIT_FSIZE, (8 << 20, 8 << 20))
resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 4096))
os.execv(sys.argv[1], sys.argv[1:])
