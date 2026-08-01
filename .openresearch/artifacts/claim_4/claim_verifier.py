import json
from reproduction.falsification import claim_4_proof_dependency_check
from reproduction.representation_search import claim_4_exhaustive_search
from reproduction.reduction_audit import claim_4_reduction_audit
from reproduction.adversarial_search import claim_4_adversarial_falsification

result = {
    "route_1": claim_4_proof_dependency_check(),
    "route_2": claim_4_exhaustive_search(),
    "route_3": claim_4_reduction_audit(),
    "route_4": claim_4_adversarial_falsification(),
}
if any(route["verdict"] != "BLOCKED" for route in result.values()):
    raise SystemExit(1)
print(json.dumps(result, indent=2, sort_keys=True))
