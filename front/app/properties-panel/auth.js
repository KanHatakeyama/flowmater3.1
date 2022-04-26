import { getToken, storageKey } from "../network/api"

export function AuthForm(err) {

    //alert(err)
    alert("token or url seem invalid. reaccess this page from admin page")
    /*
    let username = localStorage.getItem(storageKey.user);
    let host_ip = localStorage.getItem(storageKey.url);

    host_ip = prompt('server url', host_ip)
    let user = prompt('User name', username)
    let pass = prompt('Password', "")
    localStorage.setItem(storageKey.user, user)
    localStorage.setItem(storageKey.url, host_ip)
    getToken(user, pass, host_ip)

    //window.location.reload();
    */
}