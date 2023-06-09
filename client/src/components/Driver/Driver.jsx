import React from 'react'
import styles from "./Driver.module.css";

import Drive from "../../assets/drive.png";

const Driver = () => {
  return (
    <div className={styles.driver}>

        {/* containers grid */}
        <div className={styles.left}>
            <img src={Drive} alt='/'/>
        </div>

        <div className={styles.right}>
            <h2>Driving the Future:<span>Innovating Autonomous Vehicles with Intel AI</span></h2>
            <p>"Inspiring the Road Ahead: Pioneering Intel AI for Autonomous Vehicles" and
"Revolutionizing Mobility: Unleashing the Power of Intel AI in Self-Driving Technology"</p>
        </div>
    </div>
  )
}

export default Driver