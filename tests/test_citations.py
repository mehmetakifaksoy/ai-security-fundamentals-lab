import unittest

from lab.citations import citation_warnings


class CitationTests(unittest.TestCase):
    def setUp(self):
        self.hits = [{"source": "identity.md#1", "text": "MFA requires additional proof."}]

    def test_exact_and_prefixed_labels_are_accepted(self):
        for label in ["identity.md#1", "source: identity.md#1", "SOURCE:identity.md#1"]:
            with self.subTest(label=label):
                self.assertEqual(citation_warnings(f"Use MFA [{label}].", self.hits), [])

    def test_unknown_and_numeric_labels_are_flagged(self):
        for label in ["fake.md#99", "1", "identity.md#2"]:
            with self.subTest(label=label):
                warnings = citation_warnings(f"A claim [{label}].", self.hits)
                self.assertEqual(len(warnings), 1)
                self.assertIn(label, warnings[0])

    def test_valid_label_does_not_hide_invalid_label(self):
        warnings = citation_warnings("Claim [identity.md#1]. Other [fake.md#99].", self.hits)
        self.assertIn("fake.md#99", warnings[0])

    def test_no_citation_is_reported_even_for_abstention(self):
        self.assertIn("No source citations", citation_warnings("I do not know.", self.hits)[0])

    def test_sources_are_specific_to_current_retrieval(self):
        self.assertTrue(citation_warnings("Claim [network.md#1].", self.hits))
        self.assertEqual(citation_warnings("Claim [network.md#1].", [{"source": "network.md#1"}]), [])

    def test_supported_label_is_not_a_truth_check(self):
        self.assertEqual(citation_warnings("MFA prevents every attack [identity.md#1].", self.hits), [])
