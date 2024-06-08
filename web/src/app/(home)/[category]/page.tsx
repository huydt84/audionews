import NewsList from '@/components/news-list'
import { Suspense } from 'react'

type Props = {
  params: {
    category: string
  }
}

export default async function NewsCategory({ params }: Props) {
  const { category } = params

  return (
    <main className="">
      <Suspense key={category} fallback={<p>Loading...</p>}>
        <NewsList category={category} />
      </Suspense>
    </main>
  )
}
