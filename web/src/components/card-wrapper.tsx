'use client'

import { Card, CardContent, CardHeader, CardFooter } from '@/components/ui/card'
import React from 'react'

interface CardWrapperProps {
  children: React.ReactNode
  headerLabel: string
}

export const CardWrapper = ({ children, headerLabel }: CardWrapperProps) => {
  return (
    <Card className="w-[28rem]">
      <CardHeader>
        <div className="w-full flex flex-col gap-y-4 items-center justify-center">
          <p className="text-muted-foreground text-lg">{headerLabel}</p>
        </div>
      </CardHeader>

      <CardContent>{children}</CardContent>
    </Card>
  )
}
