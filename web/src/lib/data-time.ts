import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import updateLocale from 'dayjs/plugin/updateLocale'

export const formatTime = (time: Date) => {
  dayjs.extend(relativeTime)

  dayjs.extend(updateLocale)

  dayjs.updateLocale('en', {
    relativeTime: {
      future: 'trong %s',
      past: '%s trước',
      s: 'vài giây',
      m: 'một phút',
      mm: '%d phút',
      h: 'một giờ',
      hh: '%d giờ',
      d: 'một ngày',
      dd: '%d ngày',
      M: 'một tháng',
      MM: '%d tháng',
      y: 'một năm',
      yy: '%d năm'
    }
  })

  return dayjs(time).fromNow()
}
