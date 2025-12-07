import { createSystem, defaultConfig } from '@chakra-ui/react'

export const system = createSystem(defaultConfig, {
  theme: {
    tokens: {
      fonts: {
        heading: { value: `'EB Garamond', serif` },
        body: { value: `'EB Garamond', serif` },
      },
    },
  },
})