import { useState } from 'react';
import Image from 'next/image'
import SyntaxHighlighter from 'react-syntax-highlighter';
import { atomOneDark } from 'react-syntax-highlighter/dist/cjs/styles/hljs';
import Copy from '../public/icons/Copy.svg'
import Tick from '../public/icons/Tick.svg'

export const Code = ({ children, language, customStyle }) => {

    const [icon, setIcon] = useState(Copy)

    const copyToClipboard = () => {
        navigator.clipboard.writeText(children)
        setIcon(Tick)
        setTimeout(() => setIcon(Copy), 1200)
    }

    return (
        <section className="flex items-start mt-10 relative max-w-fit">
            <SyntaxHighlighter language={language} style={atomOneDark}
                customStyle={{
                    borderRadius: "10px",
                    background: "#1C1E25",
                    padding: "10px 20px",
                    maxWidth: "700px",
                    fontSize: "1.2rem",
                    color: "#7F818D"
                }}>
                {children}
            </SyntaxHighlighter>
            <div className="w-6 h-6 cursor-pointer absolute right-2 
                            top-2 active:scale-90 duration-100">
                <Image src={icon} alt="copy" onClick={copyToClipboard} />
            </div>

        </section>
    )
}
