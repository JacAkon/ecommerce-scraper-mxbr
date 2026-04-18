import csv
import json
import os
from typing import List

from config.settings import Config
from utils.logger import Logger


class Storage:
    """Handles CSV and JSON persistence for scraped products."""

    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or Config.OUTPUT_PATH
        os.makedirs(self.output_dir, exist_ok=True)
        self.logger = Logger(__name__)

    # ------------------------------------------------------------------
    # CSV
    # ------------------------------------------------------------------

    def save_to_csv(
        self,
        records: List[dict],
        filename: str,
        append: bool = False,
        fieldnames: List[str] = None,
    ) -> str:
        """Save records to a CSV file.

        Args:
            records:    List of dicts to save.
            filename:   Output file name (relative to output_dir).
            append:     If True, append to an existing file; otherwise overwrite.
            fieldnames: Column names. Auto-detected from records when omitted.

        Returns:
            The absolute path of the written file.
        """
        if not records:
            self.logger.warning("save_to_csv: no records to save.")
            return ''

        fieldnames = fieldnames or Config.DATA_FIELDS or list(records[0].keys())
        filepath = os.path.join(self.output_dir, filename)
        mode = 'a' if append else 'w'
        write_header = not append or not os.path.exists(filepath)

        try:
            with open(filepath, mode, newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                if write_header:
                    writer.writeheader()
                writer.writerows(records)
            self.logger.info("Saved %d records to CSV: %s", len(records), filepath)
            return filepath
        except OSError as exc:
            self.logger.error("Failed to write CSV %s: %s", filepath, exc)
            return ''

    # ------------------------------------------------------------------
    # JSON
    # ------------------------------------------------------------------

    def save_to_json(
        self,
        records: List[dict],
        filename: str,
        append: bool = False,
    ) -> str:
        """Save records to a JSON file.

        Args:
            records:  List of dicts to save.
            filename: Output file name (relative to output_dir).
            append:   If True, load existing data and extend it; otherwise overwrite.

        Returns:
            The absolute path of the written file.
        """
        if not records:
            self.logger.warning("save_to_json: no records to save.")
            return ''

        filepath = os.path.join(self.output_dir, filename)
        data = records

        if append and os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                if isinstance(existing, list):
                    data = existing + records
            except (OSError, json.JSONDecodeError) as exc:
                self.logger.warning("Could not read existing JSON %s: %s", filepath, exc)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.info("Saved %d records to JSON: %s", len(data), filepath)
            return filepath
        except OSError as exc:
            self.logger.error("Failed to write JSON %s: %s", filepath, exc)
            return ''
