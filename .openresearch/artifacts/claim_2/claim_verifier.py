import json
from reproduction.proof_certificates import claim_2_certificate

result = claim_2_certificate()
if result["verdict"] != "VERIFIED" or result["symbolic_residual"] != "0":
    raise SystemExit(1)
print(json.dumps(result, indent=2, sort_keys=True))
