import json
from reproduction.falsification import claim_3_counterexample

result = claim_3_counterexample()
if result["verdict"] != "FALSIFIED" or result["smt_abstention_under_axioms"] != "UNSAT":
    raise SystemExit(1)
print(json.dumps(result, indent=2, sort_keys=True))
