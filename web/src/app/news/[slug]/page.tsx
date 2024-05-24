import AudioItem from '@/components/audio-item'
import { formatTime } from '@/lib/data-time'
import { getNewsBySlug } from '@/server/actions/news'
import Image from 'next/image'
import Link from 'next/link'
import { FaArrowLeft, FaExternalLinkAlt } from 'react-icons/fa'

type Props = {
  params: {
    slug: string
  }
}

export const generateMetadata = async ({ params }: Props) => {
  const news = await getNewsBySlug(params.slug)

  if (!news) return

  return {
    title: `${news.title} - ${news.site_name}`
  }
}

export default async function NewsDetailPage({ params }: Props) {
  const { slug } = params

  const news = await getNewsBySlug(slug)

  if (!news) return <p>News not found</p>

  return (
    <main className="flex justify-center items-start relative">
      <div className="grow sticky top-[7.063rem]">
        <Link
          href="/"
          className="flex justify-center items-center w-min whitespace-nowrap font-medium gap-2 group hover:underline transition-all duration-200"
        >
          <FaArrowLeft className="group-hover:translate-x-[-3px] transition-transform duration-200" />
          <span>Trở về</span>
        </Link>
      </div>
      <div className="max-w-[800px] mx-auto space-y-6">
        <Image
          src={news.image_url}
          width={1920}
          height={1080}
          alt={news.title}
          className="object-cover w-full h-[20rem] rounded-md"
        />

        <h1 className="text-4xl font-semibold">{news.title}</h1>

        <div className="flex justify-between items-start">
          <div className="flex justify-start items-center gap-2">
            <Image
              src={news.logo_url}
              width={200}
              height={200}
              alt={news.site_name}
              className="object-contain w-[9rem]"
            />
            <div>
              <h5 className="font-semibold leading-5">{news.site_name}</h5>
              <p className="leading-5 text-sm opacity-80">{formatTime(news.written_at)}</p>
            </div>
          </div>

          <a
            href={news.link_source}
            target="_blank"
            className="text-lg font-medium underline flex items-center gap-2"
          >
            Bài viết gốc <FaExternalLinkAlt className="text-sm" />
          </a>
        </div>

        <div className="space-y-2">
          <AudioItem
            title="Giọng nam-bắc:"
            url={`${process.env.NEXT_PUBLIC_AUDIO_SRC}${news['audio_female-central']}`}
          />

          <AudioItem
            title="Giọng nữ-bắc:"
            url={`${process.env.NEXT_PUBLIC_AUDIO_SRC}${news['audio_female-central']}`}
          />

          <AudioItem
            title="Giọng nam-nam:"
            url={`${process.env.NEXT_PUBLIC_AUDIO_SRC}${news['audio_female-central']}`}
          />

          <AudioItem
            title="Giọng nữ-name:"
            url={`${process.env.NEXT_PUBLIC_AUDIO_SRC}${news['audio_female-central']}`}
          />
        </div>

        {news.content.length === 0 && (
          <p className="font-medium text-lg opacity-60">News content empty.</p>
        )}

        <p>{news.content}</p>
      </div>
      <div className="grow"></div>
    </main>
  )
}
