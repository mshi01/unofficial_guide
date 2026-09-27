"""
Stage 4b of the pipeline (unit 2 stretch): combine store.py's semantic
search with bm25_store.py's keyword search.

The two are fused by Reciprocal Rank Fusion (RRF): each retriever's ranked
list contributes 1 / (RRF_K + rank) to every chunk it returned, and the two
contributions are summed. RRF works on rank position, not raw score, which
matters here because a cosine distance and a BM25 score are not on
comparable scales — averaging them directly would need a mixing weight with
no principled way to pick it.

The result is scaled against the best a chunk could theoretically do (rank 1
in both lists) so it stays interpretable across different questions, not
just relative to whatever else this one query happened to retrieve. See
config.HYBRID_THRESHOLD for what that means for the relevance gate.
"""

import config
from store import Result, search as semantic_search
from bm25_store import search as bm25_search


def search(
    question: str,
    top_k: int | None = None,
    corpus: str | None = None,
    variant: str = "default",
    fetch_k: int | None = None,
) -> list[Result]:
    """
    Retrieve with both retrievers and fuse the rankings.

    `fetch_k` is how many candidates each retriever contributes before
    fusion — wider than `top_k` on purpose, since a chunk that's mediocre by
    one method but strong by the other should still get a chance to be
    pulled up by the fusion, and that only works if it made it into the pool.
    """
    top_k = top_k or config.TOP_K
    fetch_k = fetch_k or max(top_k * 4, 20)
    rrf_k = config.RRF_K

    semantic_hits = semantic_search(question, top_k=fetch_k, corpus=corpus, variant=variant)
    keyword_hits = bm25_search(question, top_k=fetch_k, corpus=corpus, variant=variant)

    fused: dict[str, float] = {}
    by_label = {}

    for rank, hit in enumerate(semantic_hits, start=1):
        fused[hit.label] = fused.get(hit.label, 0.0) + 1.0 / (rrf_k + rank)
        by_label.setdefault(hit.label, hit)

    for rank, hit in enumerate(keyword_hits, start=1):
        fused[hit.label] = fused.get(hit.label, 0.0) + 1.0 / (rrf_k + rank)
        by_label.setdefault(hit.label, hit)

    # The best a chunk could possibly score: rank 1 in both lists at once.
    # Scaling against this fixed ceiling, rather than against whatever this
    # particular query's candidates happen to span, is what keeps 0 meaning
    # "about as good as fusion gets" and 1 meaning "barely made either list"
    # the same way from one question to the next.
    best_possible = 2.0 / (rrf_k + 1)

    ranked_labels = sorted(fused, key=lambda label: fused[label], reverse=True)[:top_k]

    results = []
    for label in ranked_labels:
        item = by_label[label]
        distance = 1.0 - (fused[label] / best_possible)
        results.append(
            Result(
                text=item.text,
                source=item.source,
                label=label,
                distance=distance,
                produced_by=item.produced_by,
            )
        )
    return results
