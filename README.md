[Deployment link](https://ticketreservation-production.up.railway.app/)

# Ticket Reservation
## API
- all API requests (except for listing events) require a valid token, which can only be obtained by the client website


- ### `/api/list-events/` | `/api/list-events/from-date&to-date/`
  - possono essere usati sia il metodo GET che il metodo POST
  - restituisce un JSON contenente la lista degli eventi disponibli
  - se specificate, verranno mostrati solo gli eventi interni al range di date
    - le date devono essere nel formato `YYYY-MM-DD`


- ### `/api/new-reservation/`
  - è necessario impiegare il metodo POST, specificando i dati necessari come segue
```json
{
  "event" : eventID,
  "token" : token,
  "payment-account" : paymentAccount
}
```
  - chiamata API atta a creare nuova prenotazione
  - devono essere specificati l'ID dell'evento, il token associato all'account in uso e il numero della carta di pagamento
  - in ogni caso (errore o successo) viene resituito un JSON
    - in caso di errore, il parametro "status" equivale a "error", e il parametro "reason" alla descrizione dell'errore
    - in caso di successo, il parametro "status" è impostato a "ok", e il parametro "reservation-id" equivale al numero di prenotazione

- ### `/api/check-reservation/`
  - è necessario impiegare il metodo POST, specificando i dati necessari come segue
```json
{
  "token" : token,
  "reservation" : reservationID
}
```
  - chiamata API atta a richiedere i dati relativi ad una prenotazione
  - devono essere specificati il token di autenticazione, e il numero di prenotazione
  - sia in caso di successo che di errore viene restituito un JSON
    - in caso di successo, il parametro "status" è impostato su "ok", e il campo "reservation" contiene i dati relativi alla prenotazione
    - in caso di errore, il parametro "status" è impostato su "error", e il campo "reason" descrive l'errore in oggetto

- ### `/api/list-reservations/`
  - è necessario impiegare il metodo POST, specificando i dati necessari come segue
```json
{
  "token" : token
}
```
  - la chiamata API è atta a richiedere i dettagli relativi a tutte le prenotazioni eseguite da un certo utente
  - deve essere specificato il token di accesso dell'utente stesso
  - sia in caso di successo che di errore viene restituito un JSON
    - in caso di errore, il parametro "status" è impostato su "error", e il campo "reason" descrive l'errore in oggetto
    - in caso di success, il parametro "status" equivale a "ok", e il campo "reservations" continene una lista dei dettagli circa le varie prenotazioni effettuate dall'account associato al token di autenticazione

- ### `/api/create-event/`
  - è necessario impiegare il metodo POST, specificando i dati necessari come segue
```json
{
  "token" : token,
  "title" : title,
  "description" : description,
  "price" : price,
  "date" : date,
  "places" : places
}
```
  - la chiamata API è atta a creare un nuovo evento
  - la creazione è possibile solo da parte degli utenti con sufficienti privilegi di accesso (che devono essere richiesti ai proprietari del sistema e manualmente abilitati)
  - devono essere specificati: il token di autenticazione, il titolo, la descrizione, il prezzo, la data e i posti disponibili del nuovo evento
    - in caso di errore, il parametro "status" è impostato su "error", e il campo "reason" descrive l'errore in oggetto
    - in caso di success, il parametro "status" equivale a "ok", e il campo "id" corrisponde all'identificatore del nuovo evento creato

## Lib
- all'interno della cartella "lib" è fornito un file .py da impiegare come libreria di collegamento con l'API
- assicura la corretta formattazione dei dati, prima di inviare la richiesta stessa

## Client
- il client HTTP fornisce servizi quali:
  - autenticazione
  - registrazione
  - richiesta di token di accesso
  - mostrare tutti gli eventi disponibili 
  - mostrare il formato delle varie chiamate API disponibili