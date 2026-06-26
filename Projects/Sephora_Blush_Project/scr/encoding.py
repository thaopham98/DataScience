from __future__ import annotations

import pandas as pd

# Candidate "wrong" encodings that commonly cause this kind of mojibake.
# We try them in order and keep the result that round-trips cleanly.
_CANDIDATE_ENCODINGS = ("utf-8", "cp1252", "latin-1")

# Known single-character corruptions that don't round-trip cleanly through
# the general re-encode/decode strategy because the original second byte
# was dropped somewhere upstream (e.g. a stray "Â " where the source almost
# certainly had a non-breaking space). Seen in real shade names like
# "B210Â Bold Punch" (likely originally "B210° Bold Punch" or had a
# non-breaking space). Applied as a literal substring fix before the
# general repair pass.
_KNOWN_FRAGMENT_REPLACEMENTS = {
    "Â ": " ",  # mis-decoded non-breaking space (U+00A0) followed by ASCII space
}


def fix_mojibake(text: str) -> str:
    """
    Attempt to repair a string that was decoded with the wrong
    encoding one or more times.

    Strategy: re-encode the (already incorrectly-decoded) string back
    to bytes using each candidate encoding, then decode those bytes as
    UTF-8. If that round-trip succeeds without errors, and produces
    fewer "suspicious" characters (Ã, Â, â€¦ etc.) than the input, we
    treat it as fixed. This is applied repeatedly because some old
    data was double-corrupted.

    Safe to call on already-clean text: if no candidate improves it,
    the original string is returned unchanged.
    """
    if not isinstance(text, str) or not text:
        return text

    current = text
    for fragment, replacement in _KNOWN_FRAGMENT_REPLACEMENTS.items():
        current = current.replace(fragment, replacement)

    for _ in range(3):  # cap iterations; double-corruption is the worst we saw
        best = current
        best_score = _suspicion_score(best)

        for enc in _CANDIDATE_ENCODINGS:
            try:
                candidate = current.encode(enc).decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue
            score = _suspicion_score(candidate)
            if score < best_score:
                best, best_score = candidate, score

        if best == current:
            break  # no further improvement found
        current = best

    return current


def _suspicion_score(text: str) -> int:
    """Lower is cleaner. Counts characters that almost always indicate mojibake."""
    suspicious_chars = "ÃÂâ€™œ\ufffd"
    return sum(text.count(ch) for ch in suspicious_chars)


def fix_mojibake_in_dataframe(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """
    Apply fix_mojibake() to all string columns (or a specified subset).
    Returns a new DataFrame; does not mutate the input.
    """
    df = df.copy()
    if columns is not None:
        target_cols = columns
    else:
        target_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in target_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda v: fix_mojibake(v) if isinstance(v, str) else v)
    return df