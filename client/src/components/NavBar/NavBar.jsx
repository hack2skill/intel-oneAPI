import React, { useState } from "react";
import styles from "./Navbar.module.css";

import {
  AiOutlineMenu,
  AiOutlineClose,
  AiOutlineSearch,
  AiOutlineUser,
} from "react-icons/ai";

import logo from "../../assets/www.png";

const NavBar = () => {
  const [click, setClick] = useState(false);
  const handleChange = () => setClick(!click);

  return (
    <header className={styles.navbar}>
      <img src={logo} alt="/" />
      <nav>
        <ul className={click ? [styles.menu, styles.active].join(" "): [styles.menu]}>
          <li>
            <a href="/">Object Detection</a>
          </li>
          <li>
            <a href="/">Log in</a>
          </li>
          <li>
            <a href="/">Sign up</a>
          </li>
          <li>
            <AiOutlineSearch size={25} style={{ marginTop: "6px" }} />
          </li>
          <li>
            <AiOutlineUser size={25} style={{ marginTop: "6px" }} />
          </li>
        </ul>
      </nav>

      {/* Mobile menu view */}
      <div onClick={handleChange} className={styles.mobile_btn}>
        {click ? <AiOutlineClose size={25} /> : <AiOutlineMenu size={25} /> }
      </div>
    </header>
  );
};

export default NavBar;
