from typing import List, Dict, Union
import datetime as dt
import asyncio

from op_brains.config import SUMMARIZER_MODEL, USE_SUMMARY_MOCK_DATA
from op_brains.documents.optimism import ForumPostsProcessingStrategy
from op_brains.summarizer.summarizer import summarize_thread
from op_brains.exceptions import OpChatBrainsException

from op_data.db.models import RawTopic, RawTopicSummary


class RawTopicSummaryService:
    @staticmethod
    async def get_topics_urls_to_summarize(out_of_date: bool = True) -> List[str]:
        if out_of_date:
            topics = await ForumPostsProcessingStrategy.get_threads_documents_not_summarized()
        else:
            topics = await ForumPostsProcessingStrategy.get_threads_documents()

        return [topic.metadata["url"] for topic in topics if topic.metadata["url"]]

    @staticmethod
    async def summarize_single_topic(
        url: str, model_name: str
    ) -> Dict[str, Union[str, Dict[str, str]]]:
        try:
            summary = await summarize_thread(
                url, model_name, use_mock_data=USE_SUMMARY_MOCK_DATA
            )
            return {"url": url, "data": summary, "error": False}
        except OpChatBrainsException as e:
            return {"url": url, "data": {"error": str(e)}, "error": True}

    @classmethod
    async def summarize_topics(
        cls, out_of_date: bool = True
    ) -> List[Dict[str, Union[str, Dict[str, str]]]]:
        topics_urls = await cls.get_topics_urls_to_summarize(out_of_date=out_of_date)
        summaries = []

        if not topics_urls:
            return summaries

        tasks = [
            asyncio.create_task(cls.summarize_single_topic(url, SUMMARIZER_MODEL))
            for url in topics_urls
        ]

        summaries = await asyncio.gather(*tasks)

        return summaries

    @staticmethod
    async def bulk_save_summaries(summaries: List[Dict[str, str]]):
        raw_summaries = [
            RawTopicSummary(
                url=summary["url"],
                data=summary["data"],
                error=summary["error"],
                lastGeneratedAt=dt.datetime.now(dt.UTC),
            )
            for summary in summaries
        ]

        await RawTopicSummary.bulk_create(raw_summaries)

    @staticmethod
    async def update_raw_topics_as_summarized(urls: List[str]) -> bool:
        await RawTopic.filter(url__in=urls).update(
            lastSummarizedAt=dt.datetime.now(dt.UTC)
        )

    @staticmethod
    def get_summaries_urls(summaries: List[Dict[str, str]]) -> List[str]:
        return [summary["url"] for summary in summaries]

    @classmethod
    async def acquire_and_save(cls):
        print("Acquiring and saving summaries")
        summaries = await cls.summarize_topics()
        summaries_urls = cls.get_summaries_urls(summaries)

        print(f"Summarized {len(summaries)} topics")

        if not summaries:
            return

        await asyncio.gather(
            cls.bulk_save_summaries(summaries),
            cls.update_raw_topics_as_summarized(summaries_urls),
        )
        print("Summaries saved successfully")

    @staticmethod
    async def update_relationships():
        pass
