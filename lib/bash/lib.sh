URL='https://ticketreservation-production.up.railway.app'

function listEvents {
    if [ $1 ] && [ $2 ]; then
        curl -X POST "${URL}/api/list-events/${1}&${2}"
    else
        curl -X POST "${URL}/api/list-events/"
    fi
}

function listReservations {
    curl -X POST -d "token=${1}" "${URL}/api/list-reservations/"
}

function checkReservation {
    curl -X POST -d "token=${1}&reservation-id=${2}" "${URL}/api/check-reservation/"
}

function createEvent {
    curl -X POST -d "token=${1}&title=${2}&description=${3}&price=${4}&date=${5}&places=${6}" "${URL}/api/create-event/"
}

function newReservation {
    curl -X POST -d "event=${1}&token=${2}&places=${3}&payment-account=${4}" "${URL}/api/new-reservation/"
}

function deleteReservation {
    curl -X POST -d "token=${1}&reservation-id=${2}&payment-account=${3}" "${URL}/api/delete-reservation/"
}

function updateReservation {
    curl -X POST -d "token=${1}&reservation-id=${2}&places=${3}&payment-account=${4}" "${URL}/api/update-reservation/"
}

function requestToken {
    curl -X POST -d "username=${1}&password=${2}" "${URL}/api/request-token/"
}

function deleteEvent {
    curl -X POST -d "token=${1}&event-id=${2}"
}