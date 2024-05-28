use rsjson;
use reqwest::blocking::Client;

const URL: &str = "https://ticketreservation-production.up.railway.app";

fn listEvents<T: ToString>(fromDate: Option<T>, toDate: Option<T>) {
    let mut client = Client::new();
    let mut request = client.post(
        if (fromDate != None && toDate != None) {
            format!("{}/api/list-events/{}&{}/", URL, fromDate, toDate)
        } else {
            format!("{}/api/list-events/")
        }
    );

    let mut result = request.send().unwrap();
    return rsjson::Json::fromString(result.text().unwrap());
}

fn newReservation<T: ToString>(event: T, token: T, places: T, paymentAccount: T) -> Result<rsjson::Json, String> {
    let mut client = Client::new();
    let mut request = client.post(format!("{}/api/new-reservation/", URL).form(&[
        ("event", event.to_string()),
        ("token", token.to_string()),
        ("places", places.to_string()),
        ("payment-accout", paymentAccount.to_string())
    ]);

    let result = request.send().unwrap();
    return rsjson::Json::fromString(result.text().unwrap());
}

fn checkReservation<T: ToString>(token: T, reservationID: T) -> Result<rsjson::Json, String> {
    let mut client = Client::new();
    let mut request = client.post(format!("{}/api/check-reservation/", URL))
        .form(
        &[
            ("token", token.to_string()),
            ("reservation-id", reservationID.to_string())
        ]
    );

    let mut result = request.send().unwrap();
    return rsjson::Json::fromString(result.text().unwrap());
}

fn listReservations<T: ToString>(token: T) -> Result<rsjson::Json, String> {
    let mut client = Client::new();
    let mut request = client.post(format!("{}/api/list-reservations/", URL))
        .form(
        &[
            ("token", token.to_string())
        ]
    );

    let mut result = request.send().unwrap();
    return rsjson::Json::fromString(result.text().unwrap());

}

fn createEvent<T: ToString>(token: T, title: T, description: T, price: T, date: T, places: T) -> Result<rsjson::Json, String> {
    let mut client = Client::new();
    let mut request = client.post(format!("{}/api/create-event/", URL))
        .form(
        &[
            ("token", token.to_string()),
            ("title", title.to_string()),
            ("description", description.to_string()),
            ("price", price.to_string()),
            ("date", date.to_string()),
            ("places", places.to_string())
        ]
    );

    let mut result = request.send().unwrap();
    return rsjson::Json::fromString(result.text().unwrap());
}

fn deleteReservation<T: ToString>(token: T, reservationID: T, paymentAccount Option<T>) -> Result<rsjson::Json, String> {
    let mut client = Client::new();
    let mut request = client.post(format!("{}/api/delete-reservation/", URL))
        .form(
        &[
            ("token", token.to_string()),
            ("reservation-id", reservationID.to_string()),
            ("payment-account",
                if paymentAccount == None {
                    paymentAccount.unwrap()
                } else {
                    String::new()
                }
            )
        ]
    );

    let mut result = request.send().unwrap();
    return rsjson::Json::fromString(result.text().unwrap());
}

fn updateReservation<T: ToString>(token: T, reservationID: T, places: T, paymentAccount: T) -> Result<Json, String> {
    let mut client = Client::new();
    let mut request = client.post(format!("{}/api/update-reservation/", URL))
        .form(
        &[
            ("token", token.to_string()),
            ("reservation-id", reservationID.to_string()),
            ("places", places.to_string()),
            ("payment-account", paymentAccount.to_string())
        ]
    );

    let mut result = request.send().unwrap();
    return rsjson::Json::fromString(result.text().unwrap());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test() {
        listReservations("bgDYN9E5aVp4na4ohaZAsWAgM9CCI3M1p80JdQ9HPNsmMcPsoZdCU9jW7JmgyrqQ");
    }
}
