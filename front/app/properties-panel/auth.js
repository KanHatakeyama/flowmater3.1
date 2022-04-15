import { getToken, getGraph } from "../network/api"

export function AuthForm() {
    const user = prompt('User name', "user")
    const pass = prompt('Password', "aNf4l03ZKEu46dkO5ZV9Bs0xdP8xnUEbF37s39F7xOUN3Kwvy50bnR4G7r0T")

    const tokenData = getToken(user, pass)
    console.log(tokenData)
    //console.log(getGraph())

}