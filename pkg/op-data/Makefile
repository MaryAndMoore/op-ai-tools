init:
	@poetry install
	@poetry shell

seed_categories:
	@poetry install
	@poetry run sync categories

seed_raw_topics:
	@poetry install
	@poetry run sync raw_topics

seed_topics:
	@poetry install
	@poetry run sync topics

seed_summaries:
	@poetry install
	@poetry run sync summaries

seed_snapshot:
	@poetry install
	@poetry run sync snapshot

seed_agora:
	@poetry install
	@poetry run sync agora

seed_all: seed_categories seed_raw_topics seed_snapshot seed_agora seed_summaries seed_topics