import { IStatisticData } from '@/@types/news'
import StatisticItem from './statistic-item'

type Props = {
  label: string
  data: IStatisticData
}

export default function StatisticCard({ label, data }: Props) {
  return (
    <div className="bg-white rounded-md shadow-md p-4">
      <div className="flex justify-between items-center gap-4 mb-2.5">
        <p className="font-medium text-lg">{label}</p>

        <StatisticItem label="" value={data.all} />
      </div>

      <div className="grid grid-cols-2 gap-2">
        <div>
          <p className="mb-1.5">Nguồn</p>

          <StatisticItem label="VnExpress: " value={data.sites?.VnExpress} />
          <StatisticItem label="Dân trí: " value={data.sites?.['Dân trí']} />
          <StatisticItem label="Tiền Phong: " value={data.sites?.['Tiền Phong']} />
          <StatisticItem label="Thanh Niên: " value={data.sites?.['Thanh Niên']} />
        </div>
        <div>
          <p className="mb-1.5">Thể loại</p>

          <StatisticItem label="Tin nhanh: " value={data.categories?.news} />
          <StatisticItem label="Thể thao: " value={data.categories?.sport} />
          <StatisticItem label="Thế giới: " value={data.categories?.world} />
          <StatisticItem label="Giáo dục: " value={data.categories?.education} />
        </div>
      </div>
    </div>
  )
}
