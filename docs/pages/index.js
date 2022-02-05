import { Attributes } from "../components/Attributes"
import styles from "../scss/Index.module.scss"
import { Sidebar } from '../components/Sidebar'

export default function Index() {

  return (
    <div className={styles.index}>
      <h1>Introduction</h1>
      <p>High performance, easy to use and feature-rich Solana SDK for Python.</p>
      <Attributes items={[1,2]}/>
    </div>
  )
}
