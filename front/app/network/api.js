
import axios from 'axios';

//export const host_ip = process.env.REACT_APP_DIP
export const storageKey = {
    user: "JY6kb8N99co5Y5jjRlWJif7X59gMP3",
    token: "6aH3o2M8G7b9Is6iPaQbz9dRYsAL55",
    url: "wJ2eAz9iW4Z1Wag54p1EJDu7m4rK5N"
}

export const host_ip = localStorage.getItem(storageKey.url);

//Store JWT in localstorage
//CAUTION: This is not a great idea for seuciry
export const myJWT = "JWT " + localStorage.getItem(storageKey.token);


export const toJson = async (res) => {
    const json = await res.json();
    if (res.ok) {
        return json;
    } else {
        throw new Error(json.message);
    }
}

export const getToken = async (user, pass, ip) => {
    alert("begin set tokn with: " + user + " , " + ip)

    await axios.post(ip + "api/auth/jwt/create/",
        {
            "username": user,
            "password": pass,
        },
    ).then(response => {
        localStorage.setItem(storageKey.token, response.data.access)
        alert("Token was successfully set. Reload window")
    }).catch(e => {
        alert("Error setting the token", e)
    })

}


/*
export const getGraph = async () => {

    const res = await fetch(host_ip + "graph/", {
        method: "GET",
        headers: { "Authorization": myJWT },
    })
    return await toJson(res)
}
*/

export const getTargetGraph = async () => {


    //get graph id from url (e.g., http://...?gid=100)
    const current_url = new URL(window.location.href);
    const params = current_url.searchParams;
    const id = params.get('gid');

    const url = host_ip + `graph/` + String(id)
    const res = await fetch(url, {
        method: "GET",
        headers: { "Authorization": myJWT },
    }).catch(e => { alert(e) })


    let jsonRes = await toJson(res)
    jsonRes.pk = id
    return jsonRes
}

// new graph
export const newGraph = async (json) => {
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": myJWT
        },
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
        headers: {
            "Content-Type": "application/json",
            "Authorization": myJWT
        },
        body: JSON.stringify(json),
    };
    fetch(host_ip + "graph/update/" + String(id), requestOptions)
}