import { graph_id } from "../app";

//export const host_ip = process.env.REACT_APP_DIP
export const host_ip = "http://133.9.195.84:49088/"

export const toJson = async (res) => {
    const json = await res.json();
    if (res.ok) {
        return json;
    } else {
        throw new Error(json.message);
    }
}


export const getGraph = async () => {
    const res = await fetch(host_ip + "graph/", {
        method: "GET",
    })
    return await toJson(res)
}


export const getTargetGraph = async () => {

    //get graph id from url (e.g., http://...?gid=100)
    const current_url = new URL(window.location.href);
    const params = current_url.searchParams;
    const id = params.get('gid');

    const url = host_ip + `graph/` + String(id)
    const res = await fetch(url, {
        method: "GET",
    })


    let jsonRes = await toJson(res)
    jsonRes.pk = id
    return jsonRes
}

// new graph
export const postNewGraph = async (json) => {
    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(json),
    };
    const res = await fetch(host_ip + "graph/create", requestOptions)
    let jsonRes = await toJson(res)
    return jsonRes
}

//update graph
export const updateGraph = async (id, json) => {
    const requestOptions = {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(json),
    };
    fetch(host_ip + "graph/update/" + String(id), requestOptions)
}