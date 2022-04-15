import React from "react";
import { useEffect, useState } from 'react';
import { slide as Menu } from "react-burger-menu";
import { styles } from "./MenuStyle"
import { host_ip, myJWT } from "../../../network/api";
const listURLs = (data) => {
  try {
    return (
      data.map((v) => (
        <li>
          <a id="home" className="menu-item" href={"/?gid=" + String(v.pk)} style={styles.linkButton}>  {String(v.pk)} {String(v.title)} </a>
        </li>
      )))
  } catch (e) {

  }
}

//export default Menu= (props)=> {
export default props => {

  //get graph data list by api
  const [data, setData] = useState();
  useEffect(() => {

    fetch(host_ip + "graph/", {
      method: "GET",
      headers: { "Authorization": myJWT }
    })
      .then(res => res.json())
      .then(json => {
        setData(json);
      });

  }, []);


  //<a id="home" className="menu-item" href="/" style={{ color: 'white' }}>Home</a>
  return (
    <Menu styles={styles} {...props} width={"100%"} >
      <a id="home" className="menu-item" href={host_ip + "admin/"} style={styles.linkButton} target="_blank"> [Admin]</a>
      {listURLs(data)}

    </Menu>
  );
};


//<a id="home" className="menu-item" href="/" style={{ color: 'white' }}>{listURLs(data)}</a>
/*
      <a id="home" className="menu-item" href="/graph/create" style={{ color: 'white' }}>Create New</a>
      <br></br>
*/