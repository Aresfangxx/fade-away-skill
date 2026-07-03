# History-Retrieval Module

Load this only when the user asks about the course or timing of past work
("当时怎么修的", "上个月那个...", "什么时候做的 X", "那次怎么解决的") and the
answer is not a plain continuation. Plain resumes ("继续 X", "上次做到哪")
stay on the breadcrumb / topic-match path and must not load this module. This
module is read-only.

## Retrieval Order

1. **Topic hit**: if the question maps to a topic in `_Index.md` (active table or
   the graveyard section), read that topic page's `## 📍 现状` and
   `## 🕐 Sessions` anchors, plus `## 🪤 踩过的坑` when present. Stop here if this
   answers the question.
2. **Weekly-index routing**: infer a time window from the question. Search the
   headline and main-thread sections of
   `03 Journal/<YYYY-MM>/<YYYY-Wnn>/YYYY-Wnn 周索引.md` within the window (`rg` on
   those files only). Follow the `[[YYYY-MM-DD#HH:MM]]` anchors and open 1-2
   daily journals to locate the exact entry.
3. **Fallback**: if the window has no weekly index (current week, or one the user
   never generated), `rg` daily journals restricted by filename date range.
   Never run an unrouted, unbounded full-vault grep.
4. If the retrieved material meets the Knowledge admission bar, nominate it via
   `references/knowledge-candidate-trigger.md` (do not write).
