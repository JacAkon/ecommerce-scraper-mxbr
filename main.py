"""Main entry point for the ecommerce scraper."""

import sys
from datetime import datetime, timezone

from apscheduler.schedulers.blocking import BlockingScheduler

from config.settings import Config
from data.data_processor import DataProcessor
from data.storage import Storage
from scrapers.mercado_libre_scraper import MercadoLibreScraper
from utils.logger import Logger

logger = Logger(__name__)


def scrape_all():
    """Run one full scrape cycle across all sites and keywords."""
    processor = DataProcessor()
    storage = Storage()

    timestamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')

    all_records = []

    for site_id in Config.MERCADO_LIBRE_SITES:
        scraper = MercadoLibreScraper(site_id)

        for keyword in Config.SEARCH_KEYWORDS:
            logger.info("Scraping site=%s keyword='%s'", site_id, keyword)
            try:
                raw = scraper.search(keyword)
                products = scraper.parse(raw, keyword)
            except Exception as exc:
                logger.error(
                    "Error scraping site=%s keyword='%s': %s", site_id, keyword, exc
                )
                continue

            records = [processor.product_to_dict(p) for p in products]
            records = processor.add_timestamp(records, keyword)
            records = processor.normalize_data(records)
            records = processor.clean_data(records)

            all_records.extend(records)
            logger.info(
                "Collected %d products for site=%s keyword='%s'",
                len(records),
                site_id,
                keyword,
            )

    if all_records:
        csv_file = f"products_{timestamp}.csv"
        json_file = f"products_{timestamp}.json"
        storage.save_to_csv(all_records, csv_file)
        storage.save_to_json(all_records, json_file)
        logger.info("Total records saved: %d", len(all_records))
    else:
        logger.warning("No records collected in this run.")


def main():
    logger.info("Starting ecommerce scraper...")

    # Run once immediately
    scrape_all()

    # Schedule subsequent runs
    interval = Config.SCHEDULER_INTERVAL_MINUTES
    if interval and interval > 0:
        scheduler = BlockingScheduler()
        scheduler.add_job(scrape_all, 'interval', minutes=interval)
        logger.info("Scheduler started: every %d minutes", interval)
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Scheduler stopped.")
            sys.exit(0)


if __name__ == '__main__':
    main()
