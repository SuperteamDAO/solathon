import Image from 'next/image'
import { useState, useEffect } from 'react'
import Copy from '../public/icons/Copy.svg'
import Tick from '../public/icons/Tick.svg'

export const Code = ({ children }) => {
    const [icon, setIcon] = useState(Copy)
    const [codeBlock, setCodeBlock] = useState(children)
    useEffect(() => {
        let newLinesCodeBlock = {
            ...children,
            props: {
                ...children.props,
                children: {
                    ...children,
                    props: {
                        ...children.props.children.props,
                        children: codeBlock.props.children.props.children
                            .replaceAll(";", "\r")
                    }
                }
            }
        }
        setCodeBlock(newLinesCodeBlock)
    }, [])

    const copyToClipboard = () => {
        navigator.clipboard.writeText(codeBlock.props.children.props.children)
        setIcon(Tick)
        setTimeout(() => setIcon(Copy), 3000)
    }

    return (
        <section className="flex items-center relative max-w-fit ">
            {codeBlock}
            <div className={`flex absolute right-3 top-10 w-6 h-6 duration-100
                             ${icon == Copy ? "cursor-pointer active:translate-y-1" : null}`}>
                <Image src={icon} alt="copy" onClick={copyToClipboard} />
            </div>
        </section>
    )
}