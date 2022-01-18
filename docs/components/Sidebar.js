import React from 'react'
import Link from 'next/link'
import { useRouter } from "next/router";
import { sidebarContent } from "./sidebarContent";


export const Sidebar = () => {
    return(
        <SidebarContent/>
    )
}

const SidebarContent = () => {
    const { pathname } = useRouter();
    return (
      <>
        {sidebarContent.map((section, i) => (
          <React.Fragment key={i}>
            {section.title != null && (
              <h5 className=''>
                {section.title}
              </h5>
            )}
  
            <ul>
              {section.pages.map(page => (
                <li key={page.route}>
                  <Link
                    href={page.route}
                  >
                    {page.name}
                  </Link>
                </li>
              ))}
            </ul>
          </React.Fragment>
        ))}
      </>
    );
  };