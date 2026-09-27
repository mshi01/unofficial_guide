"""
Stage 3b / 4b of the pipeline (unit 2 stretch): keyword search alongside the
vector index in store.py.

Why this exists: all-MiniLM-L6-v2 embeds meaning, not exact tokens. On this
corpus every dining hall doc has the same templated sentence — "Hours are X
to Y ___. Costs one meal swipe, or $Z cash." — so the embedding barely
separates 7:00am from 1:00am; it mostly sees "a dining hours sentence." BM25
scores exact term overlap instead, so "1:00am" in the question matches the
one chunk that actually contains "1:00am," regardless of how many other
chunks share the surrounding template words.

Persisted the same way store.py persists its Chroma collection — one file
per (corpus, variant) under config.BM25_DIR — so `index` and a later
`retrieve`/`ask` can run as separate processes and still find it.
"""

import pickle
import re
from dataclasses import dataclass
from pathlib import Path

import config
from chunker import Chunk

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


@dataclass
class Hit:
    """One chunk found by keyword search.

    HIGHER score is better — the opposite convention from store.Result's
    distance, because that's how BM25 itself scores.
    """

    text: str
    source: str
    label: str
    score: float
    produced_by: str


def _index_path(corpus: str | None, variant: str) -> Path:
    config.BM25_DIR.mkdir(exist_ok=True)
    name = config.collection_name(corpus, variant)
    return config.BM25_DIR / f"{name}.pkl"


def build_index(
    chunks: list[Chunk],
    corpus: str | None = None,
    variant: str = "default",
) -> int:
    """
    Tokenize every chunk and save the tokenized corpus to disk.

    Rebuilding the actual BM25Okapi object is cheap even for a few thousand
    chunks, so what's persisted is the tokenized text, not the object itself
    — that also sidesteps pickling a third-party class across versions.
    """
    payload = {
        "tokenized": [_tokenize(c.text) for c in chunks],
        "texts": [c.text for c in chunks],
        "sources": [c.source for c in chunks],
        "labels": [c.label for c in chunks],
        "produced_by": [c.produced_by for c in chunks],
    }
    with open(_index_path(corpus, variant), "wb") as f:
        pickle.dump(payload, f)

    return len(chunks)


def search(
    question: str,
    top_k: int | None = None,
    corpus: str | None = None,
    variant: str = "default",
) -> list[Hit]:
    """Retrieve the chunks with the most exact-term overlap with the question."""
    from rank_bm25 import BM25Okapi

    top_k = top_k or config.TOP_K
    path = _index_path(corpus, variant)

    if not path.exists():
        raise RuntimeError(
            f"No BM25 index at {path}. Run `python app.py index` first."
        )

    with open(path, "rb") as f:
        payload = pickle.load(f)

    bm25 = BM25Okapi(payload["tokenized"])
    scores = bm25.get_scores(_tokenize(question))

    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    ranked = ranked[:top_k]

    return [
        Hit(
            text=payload["texts"][i],
            source=payload["sources"][i],
            label=payload["labels"][i],
            score=float(scores[i]),
            produced_by=payload["produced_by"][i],
        )
        for i in ranked
    ]
