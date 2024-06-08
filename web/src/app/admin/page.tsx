import NewsPagination from '@/components/news-pagination'
import { NewsTable } from '@/components/news-table'
import StatisticCard from '@/components/statistic-card'

import { getCurrentUser } from '@/server/actions/login'
import { getAllTimeStatistic, getLatestStatistic } from '@/server/actions/statistic'

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

  if (!user) return <p>Unauthorized</p>

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
