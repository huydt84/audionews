export interface INewsData {
  id: number
  title: string
  link_source: string
  image_url: string
  description: string
  slug_url: string
  site_name: string
  logo_url: string
  written_at: Date
}

export interface IStatisticData {
  all: number
  categories: {
    news: number
    sport: number
    world: number
    education: number
  }
  sites: {
    VnExpress: number
    'Dân trí': number
    'Tiền Phong': number
    'Thanh Niên': number
  }
}

export interface INewsDetail extends INewsData {
  content: string
  'audio_male-north'?: string
  'audio_female-north'?: string
  'audio_male-south'?: string
  'audio_female-south'?: string
  'audio_female-central'?: string
}
