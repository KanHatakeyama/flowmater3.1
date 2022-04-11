import React from "react";
import { useEffect, useState } from 'react';
import { slide as Menu } from "react-burger-menu";
import { styles } from "./MenuStyle"
import { host_ip } from "../../../network/api";

const listURLs = (data) => {
  try {
    return (
      data.map((v) => (
        <li>
          <a id="home" className="menu-item" href={"/?gid=" + String(v.pk)} style={{ color: "white" }}>  {String(v.pk)} {String(v.title)} </a><br></br>
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
    //console.log('fetching data...');

    fetch(host_ip + "graph/")
      .then(res => res.json(), {
        method: "GET",
      })
      .then(json => {
        setData(json);
      });

  }, []);


  //<a id="home" className="menu-item" href="/" style={{ color: 'white' }}>Home</a>
  return (
    <Menu styles={styles} {...props} width={"20%"} >
      <a id="home" className="menu-item" href={host_ip + "admin/"} style={{ color: 'white' }} target="_blank">Admin</a>
      <br></br>

      <h3>Recent data</h3>
      <br></br>
      <a id="home" className="menu-item" href="/" style={{ color: 'white' }}>{listURLs(data)}</a>
    </Menu>
  );
};


/*
      <a id="home" className="menu-item" href="/graph/create" style={{ color: 'white' }}>Create New</a>
      <br></br>
*/