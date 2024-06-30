import os
import sys
from pathlib import Path

import uvicorn

# Change dir to project root (three levels up from this file)
os.chdir(Path(__file__).parents[2])
# Get arguments from command
args = sys.argv[1:]

ssl_args =( 
    [
        "--ssl-ca-certs=/run/secrets/certificate_ca.crt",
        "--ssl-keyfile=/run/secrets/certificate.key",
        "--ssl-certfile=/run/secrets/certificate.crt",
        "--host=0.0.0.0"
    ]
    if os.getenv("PROD")
    else []
)


uvicorn.main.main(
    [
        "src.api.app:app",
        "--use-colors",
        "--proxy-headers",
        "--forwarded-allow-ips=*",
        *ssl_args,
        *args,
    ]
)
