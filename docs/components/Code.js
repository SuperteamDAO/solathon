import Image from 'next/image'
import { useState } from 'react'
import Copy from '../public/icons/Copy.svg'
import Tick from '../public/icons/Tick.svg'

export const Code = ({ children } = {props:{children:{props:{children:"Hi"}}}}) => {
  const [icon, setIcon] = useState(Copy)

  const copyToClipboard = () => {
    navigator.clipboard.writeText(children.props.children.props.children)
    setIcon(Tick)
    setTimeout(() => setIcon(Copy), 3000)
  }
console.log(children.props.children.props.children.replaceAll(";", "\r"))

  return (
    <section className="flex items-center relative max-w-fit ">
      {{
        ...children,
        props: {
          ...children.props,
          children: {
            ...children,
            props: {
              ...children.props.children.props,
              children: children.props.children.props.children
                .replaceAll(";", "\r")
            }
          }
        }
      }}
      <div className={`flex absolute right-3 top-10 w-6 h-6 duration-100
                            ${icon == Copy ? "cursor-pointer active:translate-y-1" : null}`}>
        <Image src={icon} alt="copy" onClick={copyToClipboard} />
      </div>
    </section>
  )
}