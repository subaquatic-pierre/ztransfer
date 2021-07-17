const networkStatusIcon = document.getElementById('network-status-icon')
const ICON_OK = `<i class="fas icon-ok fa-toggle-on fa-2x"></i>`
const ICON_ERROR = `<i class="fas icon-error fa-toggle-off fa-2x"></i>`

const NETWORK_CHECK_URL = 'https://beta.0chain.net/sharder01/v1/block/get/latest_finalized'
const NETWORK_CHECK_INTERVAL = 10000

let networkStatus = null

const networkCheck = () => {
    return fetch(NETWORK_CHECK_URL, {
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(res => {
        return res.json()
    }).then(resData => {
        // Set network status based on response status
        if(resData.creation_date > 0){
            networkStatus = 'ok'
        } else {
            networkStatus = 'error'
        }
        // Set network icon based on network status
        networkStatusIcon.innerHTML = networkStatus === 'ok' ? ICON_OK : ICON_ERROR
    }).catch(err => {
        console.error(`There was an error in API request: ${err}`)
    })
}

setInterval(networkCheck, NETWORK_CHECK_INTERVAL)