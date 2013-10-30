from pyisemail.diagnosis import BaseDiagnosis


class DeprecatedDiagnosis(BaseDiagnosis):

    """A diagnosis indicating the presence of deprecated address features.

    """

    DESCRIPTION = ("Address contains deprecated elements "
                   "but may still be valid in restricted contexts.")

    ERROR_CODES = {
        'LOCALPART': 33,
        'FWS': 34,
        'QTEXT': 35,
        'QP': 36,
        'COMMENT': 37,
        'CTEXT': 38,
        'CFWS_NEAR_AT': 49,
    }

    MESSAGES = {
        'LOCALPART': "Address contains a local part in deprecated form.",
        'FWS': "Address contains Folding White Space in deprecated form.",
        'QTEXT': "Address contains a quoted string in deprecated form.",
        'QP': "Address contains a quoted pair in deprecated form.",
        'COMMENT': "Address contains a comment in deprecated form.",
        'CTEXT': "Address contains a comment with a deprecated character.",
        'CFWS_NEAR_AT': ("Address contains a comment or Folding White Space "
                         "around the @ sign."),
    }

    REFERENCES = {
        'LOCALPART': ['obs-local-part'],
        'FWS': ['obs-local-part', 'obs-domain'],
        'QTEXT': ['obs-qtext'],
        'QP': ['obs-qp'],
        'COMMENT': ['obs-local-part', 'obs-domain'],
        'CTEXT': ['obs-ctext'],
        'CFWS_NEAR_AT': ['CFWS-near-at', 'SHOULD-NOT'],
    }
