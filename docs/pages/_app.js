import '../scss/globals.scss'
import { Sidebar } from '../components/Sidebar'

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Sidebar />
      <div className="pages"><Component {...pageProps} /></div>
    </>
  )
}

export default MyApp
