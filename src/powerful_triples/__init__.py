"""Exact tools for the Erdős–Mollin–Walsh conjecture on three consecutive powerful numbers."""

from .predicates import (  # noqa: F401
    canonical_decomposition,
    factor_sympy,
    factor_trial,
    is_powerful,
    is_powerful_certified,
    is_powerful_sympy,
    is_powerful_trial,
    is_squarefree,
    iter_powerful,
    next_powerful,
    powerful_leq,
    radical,
    squarefree_leq,
)
from .residues import (  # noqa: F401
    admissible_density_product,
    count_triple_admissible,
    factor_modulus,
    is_triple_admissible,
    powerful_residues_mod,
    prime_allowed_residues,
    triple_admissible_residues,
)
from .search import (  # noqa: F401
    SearchResult,
    consecutive_pairs_leq,
    pairs_differing_by_2,
    reformulation,
    search_direct,
    search_generated,
    search_modular,
    search_parameters,
    search_smt,
    verify_triple,
)
from .scale import (  # noqa: F401
    ScaleResult,
    count_odd_powerful,
    generate_odd_powerful_class,
    pairs_diff2_fast,
    search_triples_fast,
)

__version__ = "1.0.0"