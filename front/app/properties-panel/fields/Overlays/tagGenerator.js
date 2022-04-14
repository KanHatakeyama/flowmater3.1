import { host_ip } from "../../../network/api"
import React from 'react';
export const parseLine = (item) => {

    // load graph
    if (item.indexOf("load") === 0) {

        //get pk
        const pk = (item.split(" ")[1]).split("_")[0]
        return '<a id="load-graph" className="item" href="/?gid=' + String(pk) + '"style={{ color: "#FF570D" }} target="_blank">' + item + '</a>'
    }
    //        return <a id="load-graph" className="item" href={"/graph/" + String(pk)} style={{ color: '#FF570D' }}
    //            target="_blank">{item}</a>


    if (item.indexOf("file") === 0) {
        //get pk
        //const title = (item.split(" ")[1]).split("_").slice(1)
        const title = (item.slice(item.indexOf("_"))).slice(1)

        return (
            <>
                <img src={host_ip + "uploaded/" + String(title)} alt=""></img>
                <a id="load-graph" className="item" href={host_ip + "uploaded/" + String(title)} style={{ color: '#696969' }}
                    target="_blank">{item}</a>
            </>
        )
    }

    //smiles: show chemical strucrures
    if (item.indexOf("SMILES") === 0) {
        //get pk
        //const smiles = (item.split(" ")[1])
        const smiles = item.slice(6)

        return (
            <>
                <div style={{ color: '#009900' }}> SMILES {smiles}</div>
                <img src={host_ip + 'molecules/smiles/' + smiles} width={"130px"} />
            </>

        )

    }

    if (item.indexOf(":") > 0) {
        return <div style={{ color: '#696969' }}> {item}</div>
    }

    return ""
    return <div>{item}</div>

}