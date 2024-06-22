import React from 'react'
import { MdArrowRightAlt } from 'react-icons/md'

import { INewsData } from '@/@types/news'
import Image from 'next/image'
import Button from './button'
import { formatTime } from '@/lib/data-time'
import Link from 'next/link'

type Props = {
  newsData: INewsData
}

export default function Card({ newsData }: Props) {
  return (
    <div className="relative">
      <div className="block cursor-pointer bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 transition-all duration-200">
        <Image
          src={newsData.image_url}
          alt={newsData.title}
          width={1920}
          height={1080}
          className="w-full h-[15rem] object-cover aspect-21/9 rounded-t-lg"
        />

        <div className="px-6 py-2">
          <div className="flex justify-start items-start gap-2">
            <Image
              src={newsData.logo_url}
              alt={newsData.title}
              width={100}
              height={100}
              className="w-[5rem] object-contain"
            />
            <p className="mb-2">{formatTime(newsData.written_at)}</p>
          </div>

          <h5 className="mb-2 text-xl font-bold tracking-tight text-gray-900 h-16 text-wrap break-words truncate">
            {newsData.title}
          </h5>
          <p className="font-normal text-gray-700 h-24 text-wrap break-words truncate">
            {newsData.description}
          </p>

          <div className="h-8"></div>
        </div>
      </div>

      <Link
        href={`/news/${newsData.slug_url}`}
        className="flex absolute text-blue-700 bottom-2 left-6 hover:underline group items-center gap-0.5 text-lg font-medium mt-2 z-[3]"
      >
        Read more
        <MdArrowRightAlt className="text-2xl group-hover:translate-x-[3px] transition-transform duration-150" />
      </Link>

      <Link
        href={`/news/${newsData.slug_url}`}
        className="w-full h-full absolute top-0 left-0 z-[2]"
      />
    </div>
  )
}
