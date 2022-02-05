import styles from "../scss/components/Attributes.module.scss"

export const Attributes = ({ items }) => {
  return (

    <div className={styles.attributes}>
      Attributes
      {items.map((item, i) => (
        <>
          <h1>{item}</h1>
        </>
      ))}
    </div>
  )
}
