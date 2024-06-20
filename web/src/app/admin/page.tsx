import { NewsTable } from '@/components/news-table'
import StatisticCard from '@/components/statistic-card'

import { getCurrentUser } from '@/server/actions/login'
import { getAllTimeStatistic, getLatestStatistic } from '@/server/actions/statistic'
import DeleteCookie from '@/components/delete-cookie'

type Props = {
  searchParams?: {
    page: string
  }
}

export default async function AdminPage({ searchParams }: Props) {
  const user = await getCurrentUser()
  const allTimeData = await getAllTimeStatistic()
  const latestData = await getLatestStatistic()
  const currentPage = searchParams?.page ? parseInt(searchParams.page) : 1

  if (!user || !allTimeData || !latestData) {
    return <DeleteCookie />
  }

  return (
    <div className="w-[95%] space-y-6">
      <div className="flex justify-start items-center gap-6">
        {latestData && <StatisticCard label="⏳Trong một giờ qua" data={latestData} />}
        {allTimeData && <StatisticCard label="📻Tổng quan" data={allTimeData} />}
      </div>

      <div className="bg-white rounded-md shadow-md py-6 px-4 space-y-4">
        <p className="font-semibold text-lg">Danh sách news đã crawl</p>

        <NewsTable currentPage={currentPage} />
      </div>
    </div>
  )
}
