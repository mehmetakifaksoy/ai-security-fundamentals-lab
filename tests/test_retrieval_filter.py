import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from lab.semantic_search import main


class RetrievalFilterTests(unittest.TestCase):
    def run_cli(self, flags, ranked):
        chunks = [{"source": "identity.md#1", "text": "Use MFA."},
                  {"source": "network.md#1", "text": "Filter traffic."}]
        output = io.StringIO()
        with patch("sys.argv", ["semantic_search", "question", *flags]), \
             patch("lab.semantic_search.load_chunks", return_value=chunks), \
             patch("lab.semantic_search.load_model"), \
             patch("lab.semantic_search.rank", return_value=ranked), \
             patch("lab.semantic_search.build_prompt", return_value="preview") as preview, \
             patch("lab.semantic_search.generate_answer", return_value="Use MFA [identity.md#1].") as generate, \
             redirect_stdout(output):
            main()
        return output.getvalue(), preview, generate

    def test_below_cutoff_skips_prompt_and_model(self):
        output, preview, generate = self.run_cli(
            ["--min-score", "0.30", "--rag", "--generate"], [(0, 0.1169)])
        preview.assert_not_called()
        generate.assert_not_called()
        self.assertIn("Insufficient reference context", output)

    def test_only_eligible_sources_reach_model_and_preview(self):
        output, preview, generate = self.run_cli(
            ["--min-score", "0.30", "--rag", "--generate"], [(0, 0.4932), (1, 0.1799)])
        for call in [preview.call_args, generate.call_args]:
            self.assertEqual([hit["source"] for hit in call.args[1]], ["identity.md#1"])
        self.assertIn("Kept 1 of 2", output)

    def test_equal_cutoff_is_inclusive(self):
        _, _, generate = self.run_cli(["--min-score", "0.30", "--generate"], [(0, 0.30)])
        generate.assert_called_once()

    def test_no_cutoff_preserves_previous_behavior(self):
        _, _, generate = self.run_cli(["--generate"], [(0, 0.1), (1, 0.01)])
        self.assertEqual(len(generate.call_args.args[1]), 2)

    def test_invalid_cutoff_rejected_before_loading_model(self):
        for value in ["nan", "inf", "-1.1", "1.1"]:
            with self.subTest(value=value), \
                 patch("sys.argv", ["semantic_search", "question", f"--min-score={value}"]), \
                 patch("lab.semantic_search.load_model") as model, \
                 redirect_stdout(io.StringIO()), patch("sys.stderr", new_callable=io.StringIO):
                with self.assertRaises(SystemExit) as error:
                    main()
                self.assertEqual(error.exception.code, 2)
                model.assert_not_called()
