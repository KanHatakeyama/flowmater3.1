import { getToken } from "../network/api"

export function AuthForm() {
    const user = prompt('User name', "user")
    const pass = prompt('Password', "")

    getToken(user, pass)

}