import json
from reproduction.proof_certificates import claim_5_certificate

result = claim_5_certificate()
if result["verdict"] != "VERIFIED" or result["general_certificate"]["subgradient_residual"] != "0":
    raise SystemExit(1)
print(json.dumps(result, indent=2, sort_keys=True))
