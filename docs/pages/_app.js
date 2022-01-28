import '../styles/globals.css'
import MDXComponents from '../components/MDXComponents'
import { MDXProvider } from '@mdx-js/react'
import { Sidebar } from '../components/Sidebar'

function MyApp({ Component, pageProps }) {
  return (
      <MDXProvider components={MDXComponents}>
        <Sidebar />
        <Component {...pageProps} />
      </MDXProvider>
  )
}

export default MyApp
