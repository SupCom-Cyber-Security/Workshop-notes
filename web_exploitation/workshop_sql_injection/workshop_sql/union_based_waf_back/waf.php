<?php
/**
 * Intentionally weak WAF for CTF purposes.
 *
 * Blocks the obvious stuff (naive blacklist on raw "UNION SELECT",
 * comment markers, common tautologies) but has classic bypass gaps:
 *   - Only checks UPPERCASE/lowercase exact words, not case variants like UnIoN
 *   - Doesn't normalize whitespace, so tabs/newlines/comments between
 *     keywords slip through (e.g. UNION then an inline SQL comment then SELECT,
 *     or UNION%0aSELECT using a newline)
 *   - Doesn't catch inline comment obfuscation inside keywords themselves
 *   - Only scans the raw GET param once, no recursive/decoded re-check
 *
 * This is deliberately NOT production-grade. Don't ship this. It's a target.
 */

function waf_inspect(string $input): ?string {
    // crude decode of + and %20 only (real browsers already urldecode GET,
    // but double-encoding tricks are intentionally left unhandled)
    $normalized = str_replace('+', ' ', $input);

    $blacklist = [
        'union select',   // blocks the laziest payload: UNION SELECT
        '--',             // classic comment
        ' or 1=1',        // classic tautology
        'sleep(',         // time-based
        'benchmark(',
        'information_schema.tables', // blocks lazy full-phrase enumeration
    ];

    // Intentionally NOT lowercased: the blacklist patterns below are
    // lowercase literals, so a case-varied payload like "UnIoN SeLeCT"
    // (or fully uppercase "UNION SELECT") will NOT match strpos() here,
    // even though MySQL itself is case-insensitive for keywords. This is
    // the comment-matching real bypass gap.
    foreach ($blacklist as $bad) {
        if (strpos($normalized, $bad) !== false) {
            return "Forbidden pattern detected: \"$bad\"";
        }
    }

    // naive length cap, also bypassable by anyone who knows it exists
    if (strlen($input) > 500) {
        return "Payload too long";
    }

    return null; // allowed through
}