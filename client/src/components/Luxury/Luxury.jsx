import React from "react";
import styles from "./Luxury.module.css";

const Luxury = () => {
  return (
    <div className={styles.luxury}>
      <div className={styles.heading}>
        <h2>Intel-Powered Innovation</h2>
        <div className={styles.text_bg}>
          <p>
            <span>Unleash the Power of Intel: Accelerating AI Solutions for Unprecedented Performance</span>
          </p>
        </div>
      </div>

      {/* container for cards */}
      <div className={styles.container}>
        
        <div className={styles.card}>
          <img
            src="https://www.intel.com/content/dam/develop/public/us/en/images/thumbnails/tool-thumbnail-beta-oneapi.jpg"
            alt="/"
          />
          <div className={styles.content}>
            <h3>Intel oneAPI Base Toolkit</h3>
          </div>
        </div>

        <div className={styles.card}>
          <img
            src="https://aditech.in/wp-content/uploads/2020/03/Python-Logo.jpg"
            alt=""
          />
          <div className={styles.content}>
            <h3>Intel Distribution for Python</h3>
          </div>
        </div>

        <div className={styles.card}>
          <img
            src="https://www.logic.nl/wp-content/uploads/Intel%C2%AE-oneAPI-AI-Analytics-Toolkit.png"
            alt=""
          />
          <div className={styles.content}>
            <h3>Intel oneAPI AI Analytics Toolkit</h3>
          </div>
        </div>

        <div className={styles.card}>
          <img
            src="https://miro.medium.com/v2/resize:fit:2400/1*ukjX_Qp0nMwH2HjPlhqdDQ.png"
            alt=""
          />
          <div className={styles.content}>
            <h3>Intel Neural Compressor</h3>
          </div>
        </div>

      </div>
    </div>
  );
};

export default Luxury;
