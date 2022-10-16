import radius


def r_login(username, password, google_auth, host_ip="<radius server ip>", secret="testing123"):
    r = radius.Radius(secret, host=host_ip, port=1812)
    if r.authenticate(username, password+google_auth):
        return 1
    return 0
