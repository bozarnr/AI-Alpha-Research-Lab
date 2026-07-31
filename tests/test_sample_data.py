import json
import unittest
from pathlib import Path


class SampleDataTests(unittest.TestCase):
    def test_candidate_records_are_bounded_negative_examples(self):
        records = [
            json.loads(line)
            for line in Path("sample_data/candidate_records_sample.jsonl").read_text(encoding="utf-8").splitlines()
        ]

        self.assertEqual(len(records), 3)
        self.assertTrue(all(record["promoted"] is False for record in records))
        self.assertTrue(all("formula" in record and "reason" in record for record in records))


if __name__ == "__main__":
    unittest.main()
