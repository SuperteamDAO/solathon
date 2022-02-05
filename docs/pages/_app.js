import '../styles/globals.css'
import { Sidebar } from '../components/Sidebar'

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Sidebar />
      <Component {...pageProps} />
    </>
  )
}

export default MyApp
