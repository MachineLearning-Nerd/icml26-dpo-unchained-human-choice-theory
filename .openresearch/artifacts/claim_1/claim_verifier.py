import json
from reproduction.falsification import claim_1_counterexample

result = claim_1_counterexample()
if result["verdict"] != "FALSIFIED" or result["smt_properness_and_decomposition"] != "UNSAT":
    raise SystemExit(1)
print(json.dumps(result, indent=2, sort_keys=True))
