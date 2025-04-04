"use client";
import type { RelatedTopic } from "@/app/forum/topic/[topicId]/page";
import { cn } from "@/lib/utils";
import React from "react";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "./Carousel";
import { type Category, Topic } from "./Topic";

export interface TopicCarouselProps {
  relatedTopics: RelatedTopic[];
  category: Category;
}

export function RelatedTopicCarousel({
  relatedTopics,
  category,
}: TopicCarouselProps) {
  const isMobile = window?.innerWidth < 768;

  return (
    <Carousel className="size-full" opts={{ align: "start", loop: false }}>
      <CarouselContent className="gap-3 ml-0.5">
        {relatedTopics.map((item, index) => {
          if (!item.toTopic.about) return;
          return (
            <CarouselItem
              key={index}
              className={cn(
                "basis-1/1 md:basis-1/3 lg:basis-1/5 pl-0",
                index === relatedTopics.length - 1 && "mr-4",
              )}
            >
              <Topic item={item.toTopic} category={category} />
            </CarouselItem>
          );
        })}
      </CarouselContent>
      {!isMobile && (
        <>
          <CarouselNext className="right-0" />
          <CarouselPrevious className="left-0" />
        </>
      )}
    </Carousel>
  );
}
