export interface ApiResponse<T> {
  message: T
}

export interface PaginationApiResponse<T> {
  message: string
  data: T
  pagination: {
    totalPages: number
    currentPage: number
    total: 68
  }
}
