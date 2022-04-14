import { host_ip } from "../../../network/api"
import React from 'react';
export const parseLine = (item) => {

    // load graph
    if (item.indexOf("load") === 0) {

        //get pk
        try {
            const pk = (item.split(" ")[1]).split("_")[0]
            return '<a id="load-graph" className="item" href="/?gid=' + String(pk) + '"style={{ color: "#FF570D" }} target="_blank">' + item + '</a>'
        } catch (e) { }
    }


    if (item.indexOf("file") === 0) {
        //get pk
        //const title = (item.split(" ")[1]).split("_").slice(1)
        const title = (item.slice(item.indexOf("_"))).slice(1)

        let tag = '<img src=' + host_ip + 'uploaded/' + String(title)
        tag += ' alt=""></img><a id="load-graph" className="item" href='
        tag += host_ip + 'uploaded/' + String(title) + ' style={{ color: "#696969" }}target="_blank">' + item + '</a>'
        return tag

    }

    //smiles: show chemical strucrures
    if (item.indexOf("SMILES") === 0) {
        //get pk
        const smiles = item.slice(7)

        let tag = '<img src=' + host_ip + 'molecules/smiles/' + smiles + ' width="150 px " />'

        return tag


    }


    return ""

}