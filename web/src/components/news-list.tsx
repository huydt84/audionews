'use client'

import Card from './card'
import { useGetAllNewsQuery } from '@/hooks/use-get-news-query'
import { useCallback, useRef } from 'react'

type Props = {
  category?: string
}

export default function NewsList({ category }: Props) {
  const { fetchNextPage, hasNextPage, isFetchingNextPage, data, isLoading } =
    useGetAllNewsQuery(category)

  const intObserver = useRef<IntersectionObserver>()
  const lastPostRef = useCallback(
    (stack: Element | null) => {
      if (isFetchingNextPage) return

      if (intObserver.current) intObserver.current.disconnect()

      intObserver.current = new IntersectionObserver(stacks => {
        if (stacks[0].isIntersecting && hasNextPage) fetchNextPage()
      })

      if (stack) intObserver.current.observe(stack)
    },
    [isFetchingNextPage, fetchNextPage, hasNextPage]
  )

  if (isLoading) {
    return <p>Loading...</p>
  }

  if (!data) {
    return <p>No news available.</p>
  }

  return (
    <>
      <div className="grid grid-cols-auto-fill gap-6">
        {data.pages.map(eachPage => eachPage.map(item => <Card key={item.id} newsData={item} />))}

        <div ref={lastPostRef} />
      </div>

      {isFetchingNextPage && hasNextPage && (
        <div className="flex-center w-full">
          <p className="text-center">Loading...</p>
        </div>
      )}
    </>
  )
}
