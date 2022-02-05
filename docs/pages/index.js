import Image from 'next/image';

import styles from "../scss/Index.module.scss";
import solathon from "../public/solathon.svg";
import { Code } from '../components/Code';

export default function Index() {

  const codeString = `from solathon import Client, PublicKey

client = Client(“https://api.devnet.solana.com”)
public_key = PublicKey(“B3BhJ1nvPvEhx3hq3nfK8hx4WYcKZdbhavSobZEA44ai”)
balance = Client.get_balance(public_key)

print(balance)`;

  return (
    <div className={styles.index}>
      <h1>Introduction</h1>
      <div className="flex items-center gap-5 mt-10">
        <Image src={solathon} height="100" width="100" />
        <span>Solathon</span>
      </div>
      <Code language="bash" customStyle={{color: "red"}}>
        {"pip install solathon"}
      </Code>
      <p>High performance, easy to use and feature-rich Solana SDK for Python.</p>
      <Code language="python">
        {codeString}
      </Code>
    </div>
  )
}

