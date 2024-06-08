export interface ApiResponse<T> {
  message: T
}

export interface IApiResponse<T> {
  message: string
  data: T
}

export interface PaginationData {
  totalPages: number
  currentPage: number
  total: number
}

export interface PaginationApiResponse<T> {
  message: string
  data: T
  pagination: PaginationData
}
