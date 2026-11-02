import re


def verify_review_cues(text: str) -> list[dict]:
    """Identify review candidates; this is not fact-checking."""
    cues = []
    patterns = [
        ("Numeric expression", r"(?<!\w)\d+(?:[.,]\d+)?\s*(?:%|mm|cm|m|km|kg|g|N|kN|V|A|W|kW|Hz|°C)?"),
        ("Citation marker", r"\([^()]{2,80},\s*(?:19|20)\d{2}\)|\[[0-9,;\s-]+\]"),
        ("Equation-like expression", r"[^\n]{0,45}(?:=|≈|≤|≥)[^\n]{0,45}"),
    ]
    for label, pattern in patterns:
        for match in re.finditer(pattern, text):
            snippet = match.group(0).strip()
            if snippet:
                cues.append({"type": label, "text": snippet[:180],
                             "instruction": "Check against an authoritative source and the assessment context."})
    return cues[:100]


def localize_matches(text: str, profile: dict) -> list[dict]:
    """Literal matching against configured terms; not standards interpretation."""
    results = []
    requirements = profile.get("localization_requirements", [])
    for req in requirements:
        for term in req.get("terms", []):
            if not term:
                continue
            count = len(re.findall(re.escape(term), text, flags=re.IGNORECASE))
            results.append({
                "requirement": req.get("label", req.get("id", "Configured requirement")),
                "term": term,
                "occurrences": count,
                "source": req.get("source", "Not supplied"),
                "interpretation": "Literal occurrence count only; examiner must assess contextual compliance."
            })
    for term in profile.get("required_terms", []):
        count = len(re.findall(re.escape(term), text, flags=re.IGNORECASE))
        results.append({"requirement": "Required term", "term": term, "occurrences": count,
                        "source": "Institution profile", "interpretation": "Presence check only."})
    for term in profile.get("prohibited_or_review_terms", []):
        count = len(re.findall(re.escape(term), text, flags=re.IGNORECASE))
        results.append({"requirement": "Review term", "term": term, "occurrences": count,
                        "source": "Institution profile", "interpretation": "Flag for contextual human review; not an automatic violation."})
    return results


def draft_defense_questions(text: str, limit: int = 6) -> list[str]:
    """Draft prompts from report sentences; examiner must review and edit."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip().split()) >= 8]
    questions = []
    for sentence in sentences[:limit]:
        excerpt = sentence[:240]
        questions.append(f"You state: “{excerpt}” What evidence or reasoning supports this statement?")
    if not questions:
        questions.append("Explain the main claim of your report and identify the evidence that supports it.")
    return questions


def lexical_response_signal(question: str, answer: str) -> dict:
    """Descriptive token overlap only; never interpret as understanding or authorship."""
    tokens = lambda s: {w.lower() for w in re.findall(r"[A-Za-z0-9]+", s) if len(w) > 3}
    q, a = tokens(question), tokens(answer)
    overlap = sorted(q & a)
    return {"shared_content_words": overlap,
            "shared_word_count": len(overlap),
            "notice": "Descriptive lexical overlap only. It is not a score of understanding, correctness or authorship."}
