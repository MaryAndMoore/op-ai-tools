"use server";
import type { Category, TopicContent } from "@/components/forum/Topic";
import prisma from "@/lib/prisma";
import type { Prisma } from "@prisma/client";
import { TopicPage } from "./(components)/topic-page";

export type RelatedTopic = {
  toTopic: TopicContent;
};

export type TopicPageProps = {
  topic: Prisma.TopicGetPayload<{
    include: {
      category: true;
    };
  }> & {
    relatedTopics: RelatedTopic[];
    category: Category;
  };
};

export default async function Page({ params }: { params: any }) {
  const { topicId } = params;

  const topic = (await prisma.topic.findUnique({
    where: {
      id: Number(topicId),
    },
    include: {
      category: {
        select: {
          id: true,
          name: true,
          externalId: true,
        },
      },
      relatedTopics: {
        select: {
          toTopic: {
            select: {
              id: true,
              title: true,
              about: true,
            },
          },
        },
      },
    },
  })) as TopicPageProps["topic"];

  return <TopicPage topic={topic} />;
}
