import Link from 'next/link'
import { useRouter } from "next/router";
import { sidebarContent } from "./sidebarContent";
import styles from "../scss/components/Sidebar.module.scss"

export const Sidebar = () => {
  return (
    <div className={styles.navbar}>
      <SidebarContent />
    </div>
  )
}

const SidebarContent = () => {
  const { pathname } = useRouter();
  return (
    <>
      {sidebarContent.map((section, i) => (
        <div key={i} className={styles.navItem}>

          {section.title != null && (
            <h3 className={styles.sectionName}>
              {section.title}
            </h3>
          )}

          <ul>
            {section.pages.map(page => (
              <li key={page.route} className={styles.links}>
                <a className={pathname == page.route ? styles.linkNameActive : styles.linkName}>
                  <Link href={page.route}>
                    {page.name}
                  </Link>
                </a>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </>
  );
};
