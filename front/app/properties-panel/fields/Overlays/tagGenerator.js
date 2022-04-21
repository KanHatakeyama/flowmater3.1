import { host_ip } from "../../../network/api"
import { myJWT } from "../../../network/api"
export const parseLine = (item) => {

    // load graph
    if (item.indexOf("load") === 0) {

        //get pk
        try {
            const pk = (item.split(" ")[1]).split("_")[0]
            return '<NOBR><a id="load-graph" className="item" href="/?gid=' + String(pk) + "&server=" + host_ip + "&token=" + myJWT.replace("JWT ", "") + '" target="_blank">' + item + '</a>' + "</NOBR><br>"
        } catch (e) { }
    }


    if (item.indexOf("file") === 0) {
        const title = (item.slice(item.indexOf("_"))).slice(1)

        let tag = '<NOBR><img src=' + host_ip + 'uploaded/' + String(title)
        tag += ' alt=""></img><a id="load-graph" className="item" href='
        tag += host_ip + 'uploaded/' + String(title) + ' target="_blank">' + item + '</a>'
        return tag + "</NOBR><br>"

    }

    //smiles: show chemical strucrures
    if (item.indexOf("SMILES") === 0) {
        const smiles = item.slice(7)
        let tag = '<img src=' + host_ip + 'molecules/smiles/' + smiles + ' width="150 px " />'
        return tag + "<br>"
    }

    if (item.search("=") > 0) {
        let tag = "<NOBR>"
        const title = item.replace(/ *=.*/, "") + " "
        tag += '<font color="green" size=0.5% >' + title + "</font>"

        const vals = item.replace(/.*= */, "")
        tag += '<font color="gray" size=0.5%>' + vals + "</font>"
        //let unit = vals.replace(/[0-9, \-]* /, "")
        //let prop = vals.replace(/ *[^0-9, \-]*/, "")
        //tag += '<font color="gray" size=0.5%>' + prop + "</font>"
        //tag += '<font color="black" size=0.5%>' + unit + "</font>"
        return tag + "</NOBR><br>"
    }

    return ""

}