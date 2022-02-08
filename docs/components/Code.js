import Image from 'next/image'
import { useState } from 'react'
import Copy from '../public/icons/Copy.svg'
import Tick from '../public/icons/Tick.svg'

export const Code = ({ children }) => {
  const [icon, setIcon] = useState(Copy)

  const copyToClipboard = () => {
    navigator.clipboard.writeText(children.props.children.props.children)
    setIcon(Tick)
    setTimeout(() => setIcon(Copy), 3000)
  }

  try {
    children.props.children.props.children.replaceAll()
  } catch (e) {
    console.log(e)
    console.log(children)
  }

  return (
    <section className="flex items-center relative max-w-fit ">
      {children}
      <div className={`flex absolute right-3 top-10 w-6 h-6 duration-100
                            ${icon == Copy ? "cursor-pointer active:translate-y-1" : null}`}>
        <Image src={icon} alt="copy" onClick={copyToClipboard} />
      </div>
    </section>
  )
}