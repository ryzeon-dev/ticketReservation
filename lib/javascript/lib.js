/*  !!! run `npm install sync-request` before using the library */
var request = require('sync-request');
const URL = 'https://ticketreservation-production.up.railway.app'

function post(url, arguments) {
    let response = request('POST', url, {
            body: arguments
        }
    );

    return JSON.parse(response.getBody('utf-8'));
}

function listEvents(fromDate=null, toDate=null) {
    if (fromDate && toDate) {
        return post(URL + `api/list-events/${fromDate}&${toDate}/`);
    }

    return post(URL + '/api/list-events/');
}

function newReservation(event, token, places, paymentAccount) {
    return post(
        URL + '/api/new-reservation/',
        `event=${event}&token=${token}&places=${places}&payment-account=${paymentAccount}`
    );
}

function checkReservation(token, reservationID) {
    return post(
        URL + '/api/check-reservation/',
        `token=${token}&reservation-id=${reservationID}}`
    );
}

function listReservations(token) {
    return post(
        URL + '/api/list-reservations/',
        `token=${token}`
    );
}

function createEvent(token, title, description, price, date, places) {
    return post(
        URL + '/api/create-event/,
        `token=${token}&title=${title}&description=${description}&price=${price}&date=${date}&places=${places}`
    );
}

function deleteReservation(token, reservationID, paymentAccount=null) {
    return post(
        URL + '/api/delete-reservation/',
        `token=${token}&reservation-id=${reservationID}&payment-account=${paymentAccount ? '' : paymentAccount}`
    );
}

function updateReservation(token, reservationID, places, paymentAccount) {
    return post(
        URL + '/api/new-reservation/',
        `token=${token}&reservation-id=${reservationID}&places=${places}&payment-account=${paymentAccount}`
    );
}

function deleteEvent(token, eventID) {
    return post(
        URL + '/api/delete-event/',
        `token=${token}&event-id=${eventID}`
    );
}+