import * as z from 'zod'

export const LoginSchema = z.object({
  username: z.string().min(1, {
    message: 'Username is required'
  }),
  password: z.string().min(1, {
    message: 'Password is required'
  })
})

export const ChangePasswordSchema = z
  .object({
    old_password: z.string().min(1, {
      message: 'Old password is required'
    }),
    new_password: z.string().min(1, {
      message: 'New password is required'
    }),
    confirm_password: z.string().min(1, {
      message: 'Confirm password is required'
    })
  })
  .refine(data => data.new_password === data.confirm_password, {
    message: 'Confirm password is not match',
    path: ['confirm_password']
  })
