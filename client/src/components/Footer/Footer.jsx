import React from 'react'
import styles from "./Footer.module.css"

import Logo from "../../assets/www.png"

const Footer = () => {
  return (
    <div className={styles.footer}>
        <div className={styles.container}>
            <img src={Logo} alt='/'/>
        </div>
    </div>
  )
}

export default Footer