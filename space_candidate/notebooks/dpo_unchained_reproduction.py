import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # DPO Unchained, checked at theorem scale

        **Live judge score: 5/10. Forecast after publication: 8–9/10, not a judge result.**

        | Claim | Exact verdict | Decisive evidence |
        |---|---|---|
        | 1 · composite loss | **FALSIFIED** | identity + sigmoid contradict endpoint properness |
        | 2 · regret/Bregman | **VERIFIED** | dimension-free symbolic identity; 200 exact checks |
        | 3 · KLST* abstention | **FALSIFIED** | axioms force `p(a>b)+p(b>a)=1` |
        | 4 · representation | **BLOCKED** | proof-domain gap; no witness in four routes |
        | 5 · triptych/DPO | **VERIFIED** | exact canonical and logistic identities |

        These are the already-produced formal results. Opening this notebook does not rerun the expensive adversarial search.
        """
    )
    return


@app.cell
def _():
    results = {
        "claim_1": {"verdict": "FALSIFIED", "confidence": "HIGH"},
        "claim_2": {"verdict": "VERIFIED", "confidence": "HIGH"},
        "claim_3": {"verdict": "FALSIFIED", "confidence": "HIGH"},
        "claim_4": {"verdict": "BLOCKED", "confidence": "LOW"},
        "claim_5": {"verdict": "VERIFIED", "confidence": "HIGH"},
    }
    return (results,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Why Claim 1 is false as stated

        The theorem quantifies over every increasing `psi` and `F`. Pick
        `psi(z)=z` and `F(z)=sigmoid(z)`. The decomposition forces
        `ell_0(sigmoid(z))=z`. If `c=ell_0(0)` is finite, properness when the
        true class is zero requires `ell_0(q) >= c` for every report `q`.
        Choosing `z=c-1` produces `q=sigmoid(c-1)>0` but
        `ell_0(q)=c-1<c`: contradiction. Z3 independently certifies the core
        inequality system `UNSAT`; reversing the properness inequality makes
        the mutant satisfiable.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Why KLST* cannot abstain

        For arbitrary atoms `a,b`, let `L=(ab)_alpha`. Expandability and
        bearability give

        `p(L>L)-1/2 = alpha(1-alpha)(p(a>b)+p(b>a)-1) = 0`.

        Because `alpha` is strictly between zero and one, every atomic pair
        has total choice probability one. Dropping mixed-lottery bearability
        restores a satisfiable abstaining model, so the control fails for the
        intended reason.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The unresolved representation theorem

        Four genuinely different routes were completed:

        1. a pointwise counterexample to a published proof lemma;
        2. complete enumeration of 125 reciprocal three-alternative grid models—19 satisfy the finite KLST* obligations and all 19 are representable;
        3. a type audit showing the proof's witness is a mixed lottery, while the cited representation premise is asserted on atomic alternatives;
        4. adversarial synthesis of 6,000 four-alternative models—5,987 are nonrepresentable, but every one violates exact monotonicity.

        A proof gap is not theorem falsification, and a failed search is not a proof. The only honest verdict is **BLOCKED**.
        """
    )
    return


@app.cell
def _(mo):
    verdict = mo.ui.dropdown(
        options=["claim_1", "claim_2", "claim_3", "claim_4", "claim_5"],
        value="claim_1",
        label="Inspect a claim",
    )
    return (verdict,)


@app.cell
def _(mo, results, verdict):
    mo.vstack([verdict, mo.md(f"Selected result: `{results[verdict.value]}`")])
    return


if __name__ == "__main__":
    app.run()
