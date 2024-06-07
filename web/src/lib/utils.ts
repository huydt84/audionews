import { AxiosError } from 'axios'
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * Merges class names with tailwindcss
 * @param {string[]} inputs - The class names to merge
 * @returns {string} The merged class names
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
