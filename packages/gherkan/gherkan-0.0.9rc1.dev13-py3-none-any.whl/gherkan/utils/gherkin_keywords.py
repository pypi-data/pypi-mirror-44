from gherkan.utils import constants as c

FEATURE = "Feature"
BACKGROUND = "Background"
SCENARIO = "Scenario"
GIVEN = "Given"
WHEN = "When"
THEN = "Then"
AND = "AND"
BUT = "BUT"
OR = "OR"


FEATURE_CS = "Požadavek"
BACKGROUND_CS = "Kontext"
SCENARIO_CS = "Scénář"
GIVEN_CS = "Pokud"
WHEN_CS = "Když"
THEN_CS = "Pak"
AND_CS = "A"
BUT_CS = "ALE"
OR_CS = "NEBO"
FORCE_CS = "Vynuť"
UNFORCE_CS = "Uvolni"

KEYWORDS_EN = {
    "feature": FEATURE,
    "background": BACKGROUND,
    "scenario": SCENARIO,
    "given": GIVEN,
    "when": WHEN,
    "then": THEN,
}

KEYWORDS_CS = {
    "feature": FEATURE_CS,
    "background": BACKGROUND_CS,
    "scenario": SCENARIO_CS,
    "given": GIVEN_CS,
    "when": WHEN_CS,
    "then": THEN_CS,
}

def get_kw(lang : str, key : str):
    if lang == c.LANG_EN:
        return KEYWORDS_EN[key.lower()]
    elif lang == c.LANG_CZ:
        return  KEYWORDS_CS[key.lower()]
    else:
        raise ValueError(f"Language not recognized: {lang}")