const networkStatusIcon = document.getElementById('network-status-id')
const ICON_OK = "icon-ok fas fa-toggle-on fa-2x"
const ICON_ERROR = "icon-ok fas fa-toggle-on fa-2x"
const NETWORK_CHECK_URL = 'https://beta.0chain.net/sharder01/v1/block/get/latest_finalized'

const networkStatus = null

const networkCheck = () => {
    return fetch(NETWORK_CHECK_URL, {
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(res => {
        return res.json()
    }).then(resData => {
        // Check response status
        console.log(resData)

        // Set network status based on response status
        if(resData){
            networkStatus = 'ok'
        } else {
            networkStatus = 'error'
        }

        // Set network icon based on network status
        networkStatusIcon.className = networkStatus === 'ok' ? ICON_OK : ICON_ERROR
    }).catch(err => {
        console.error('There was an error in API request')
    })
}

setInterval(networkCheck, 2000)