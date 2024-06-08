'use client'

import * as z from 'zod'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useTransition } from 'react'
import { CardWrapper } from './card-wrapper'
import { LoginSchema } from '@/schema/login'
import { login } from '@/server/actions/login'
import { useToast } from './ui/use-toast'
import { useRouter } from 'next/navigation'

export const LoginForm = () => {
  const [isPending, startTransition] = useTransition()
  const { toast } = useToast()
  const router = useRouter()

  const form = useForm<z.infer<typeof LoginSchema>>({
    resolver: zodResolver(LoginSchema),
    defaultValues: {
      username: '',
      password: ''
    }
  })

  const onSubmit = (values: z.infer<typeof LoginSchema>) => {
    startTransition(() => {
      const formData = new FormData()
      formData.append('username', values.username)
      formData.append('password', values.password)

      login(formData).then(data => {
        if ((data as any).error) {
          toast({
            title: 'Login failed',
            description: 'Invalid username or password'
          })
          return
        }

        toast({
          title: 'Login successfully',
          description: 'You are now logged in'
        })
        router.push('/admin')
      })
    })
  }

  return (
    <CardWrapper
      headerLabel="Admin Login"
      backButtonLabel="Don't have an account?"
      backButtonHref="/auth/register"
      showSocial
    >
      <Form {...form}>
        <form className="space-y-6" onSubmit={form.handleSubmit(onSubmit)}>
          <div className="space-y-4">
            <FormField
              control={form.control}
              name="username"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Username</FormLabel>
                  <FormControl>
                    <Input {...field} disabled={isPending} type="id" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <Input {...field} disabled={isPending} placeholder="******" type="password" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          <Button disabled={isPending} type="submit" className="w-full">
            Login
          </Button>
        </form>
      </Form>
    </CardWrapper>
  )
}
