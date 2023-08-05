from typing import Callable, Dict, List, NamedTuple

from .prefix import OrderedKeyPrefixTree
from spectra_lexer.steno.rules import RuleFlags, StenoRule
from spectra_lexer.steno.system import StenoSystem
from spectra_lexer.utils import str_prefix, str_without


class SpecialRules:
    """ Identifiers for special rules that are handled individually in code. """
    CONFLICT = "CF"
    PROPER = "PR"
    ABBREVIATION = "AB"
    AFFIX = "PS"
    FINGERSPELL = "FS"
    OBSCENE = "OB"


class LexerRule(NamedTuple):
    """ Container for a steno rule with s-keys for finding matches. """
    rule: StenoRule  # Original immutable rule.
    skeys: str       # Lexer-formatted steno keys that make up the rule.
    letters: str     # Raw English text of the word.


class LexerRuleMatcher:
    """ A master dictionary of steno rules. Each component dict maps strings to steno rules in some way. """

    _convert_keys: Callable[[str], str]  # Conversion function from s-keys to RTFCRE.
    _key_sep: str                        # Steno key used as stroke separator in both stroke formats.
    _key_star: str                       # Steno key used for special translation-wide matches.
    _rule_sep: LexerRule                 # Separator rule constant.
    _rule_unknown: LexerRule             # Unknown special rule constant.

    _special_dict: Dict[str, LexerRule] = None  # Rules that match by reference name.
    _stroke_dict: Dict[str, LexerRule] = None   # Rules that match by full stroke only.
    _word_dict: Dict[str, LexerRule] = None     # Rules that match by exact word only (whitespace-separated).
    _prefix_tree: OrderedKeyPrefixTree = None   # Rules that match by starting with certain keys in order.
    _translations: Dict[str, str] = {}          # Optional translation search dict for stroke conflicts.

    def load(self, system:StenoSystem) -> None:
        """ Construct constants and a specially-structured series of dictionaries from a steno system. """
        sep = self._key_sep = system.keys.SEP
        star = self._key_star = system.keys.SPECIAL
        self._convert_keys = system.to_rtfcre
        # The separator rule needs a flag to show up below other rules on output.
        r_sep = StenoRule(sep, "", frozenset({RuleFlags.SEPARATOR}), "Stroke separator", ())
        self._rule_sep = LexerRule(r_sep, sep, "")
        # The unknown rule constant is required in case the special rules don't match (or aren't loaded).
        r_unknown = StenoRule(star, "", frozenset(), "purpose unknown\nPossibly resolves a conflict", ())
        self._rule_unknown = LexerRule(r_unknown, star, "")
        special_dict = self._special_dict = {}
        stroke_dict = self._stroke_dict = {}
        word_dict = self._word_dict = {}
        # Steno order may be ignored for certain keys. This has a large performance and accuracy cost.
        # Only the asterisk is used in such a way that this treatment is worth it.
        prefix_tree = self._prefix_tree = OrderedKeyPrefixTree(self._star_filter)
        # Sort rules into specific dictionaries based on specific flags for the lexer matching system.
        match_name = RuleFlags.SPECIAL
        match_stroke = RuleFlags.STROKE
        match_word = RuleFlags.WORD
        for (n, r) in system.rules.items():
            # All rules must have their keys parsed into the case-unique s-keys format.
            skeys = system.from_rtfcre(r.keys)
            letters = r.letters
            flags = r.flags
            lr = LexerRule(r, skeys, letters)
            # Internal rules are only used in special cases, by name.
            if match_name in flags:
                special_dict[n] = lr
            # Filter stroke and word rules into their own dicts.
            elif match_stroke in flags:
                stroke_dict[skeys] = lr
            elif match_word in flags:
                word_dict[letters] = lr
            # Everything else gets added to the tree-based prefix dictionary.
            else:
                prefix_tree.add_entry(skeys, letters, lr)

    def set_translations(self, d:dict) -> None:
        """ Set up an optional translations dict for finding asterisk conflicts. """
        self._translations = d

    def match(self, skeys:str, letters:str, all_skeys:str, all_letters:str) -> List[LexerRule]:
        """ Return a list of rules that match the given keys and letters in any of the dictionaries.
            For single-key end-cases, there are no better matches, so return immediately if one is found. """
        # If our current stroke is empty, a stroke separator is next. Return its rule.
        skeys_fs = skeys.split(self._key_sep, 1)[0]
        if not skeys_fs:
            return [self._rule_sep]
        # If we only have a star left at the end of a stroke, try to match a star rule explicitly by name.
        # If execution reaches the end without finding one, return the "ambiguous" rule.
        if skeys_fs == self._key_star:
            name = self._analyze_star(skeys, all_skeys, all_letters)
            return [self._special_dict.get(f"{self._key_star}:{name}") or self._rule_unknown]
        # Try to match keys by prefix. This may yield a large number of rules.
        matches = self._prefix_tree.prefix_match(skeys, letters)
        # We have a complete stroke next if we just started or a stroke separator was just matched.
        is_start = (skeys == all_skeys)
        if is_start or all_skeys[-len(skeys) - 1] == self._key_sep:
            stroke_rule = self._stroke_match(skeys_fs, letters)
            if stroke_rule:
                matches.append(stroke_rule)
        # We have a complete word if we just started or the word pointer is sitting on a space.
        if is_start or letters[:1] == ' ':
            word_rule = self._word_match(skeys, letters)
            if word_rule:
                matches.append(word_rule)
        return matches

    def _stroke_match(self, skeys_fs:str, letters:str) -> LexerRule:
        """ For the stroke dictionary, the rule must match the next full stroke and a subset of the given letters. """
        r = self._stroke_dict.get(skeys_fs)
        if r and r.letters in letters:
            return r

    def _word_match(self, skeys:str, letters:str) -> LexerRule:
        """ For the word dictionary, the rule must match a prefix of the given keys and the next full word."""
        r = self._word_dict.get(str_prefix(letters.lstrip()))
        if r and skeys.startswith(r.skeys):
            return r

    def _analyze_star(self, skeys:str, all_skeys:str, all_letters:str) -> str:
        """ Try to guess the meaning of an asterisk from the remaining keys, the full set of keys,
            the full word, and the current rulemap. Return the reference name for the best-guess rule (if any). """
        # If the word contains a period, it's probably an abbreviation (it must have letters to make it this far).
        if "." in all_letters:
            return SpecialRules.ABBREVIATION
        # If the word has uppercase letters in it, it's probably a proper noun.
        if all_letters != all_letters.lower():
            return SpecialRules.PROPER
        # If we have a multi-stroke word and are at the beginning or end of it, it's probably a prefix or suffix.
        splits_left, all_splits = skeys.count(self._key_sep), all_skeys.count(self._key_sep)
        if all_splits and (not splits_left or splits_left == all_splits):
            return SpecialRules.AFFIX
        # If we loaded a translations dict, we can check if there's an entry with every key *except* the star.
        # If there is, the star is probably there because of a conflict.
        if self._translations.get(str_without(self._convert_keys(all_skeys), self._key_star)):
            return SpecialRules.CONFLICT

    def _star_filter(self, sk, _empty=frozenset()):
        """ Filter out asterisks in the first stroke that may be consumed at any time and return them.
            Also return the remaining ordered keys that must be consumed starting from the left. """
        star = self._key_star
        if (star not in sk) or (star not in sk.split(self._key_sep, 1)[0]):
            return sk, _empty
        return str_without(sk, star), frozenset([star])
