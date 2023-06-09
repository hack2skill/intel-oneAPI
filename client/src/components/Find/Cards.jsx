import React from 'react'
import styles from "./Find.module.css";


const Cards = ({image,make}) => {
  return (
    <div className={styles.cards}>
        <img src={image} alt='/'/>
        <p>{make}</p>

    </div>
  )
}

export default Cards