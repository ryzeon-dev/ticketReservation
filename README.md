[Deployment link](https://ticketreservation-production.up.railway.app/)

# Ticket Reservation
## API
- tuttel le richieste API (eccetto la visualizzazione degli eventi) richiede il possesso di un token di autenticazione, che può essere ottenuto unicamente tramite il sito client 

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

- ### `/api/delete-reservation/`
  - è necessario impiegare il metodo POST, specificando i dati necessari come segue
```json 
{
  "token" : token,
  "reservation-id" : reservationID,
  "payment-account" : paymentAccount [optional]
} 
```
  - la chiamata API è atta a eliminare una prenotazione
  - l'eliminazione è possibile solo da parte dell'utente che ha eseguito la prenotazione in primo luogo 
  - è necessario specificare: il token utente, l'identificatore della prenotazione e opzionalmente un account bancario sul quale eseguire lo storno
    - in caso di errore, il parametro "status" è impostato su "error", e il campo "reason" contiene la descrizione dell'errore
    - in caso di successo, "status" contiene "ok", e "transfer-account" contiene l'account di pagamento su cui è stato eseguito lo storno

- ### `/api/update-reservation/`
  - è necessario impiegare il metodo POST, specificando i dati necessari come segue 
```json 
{
  "token" : token,
  "reservation-id" : reservationID,
  "places" : places,
  "payment-account" : paymentAccount,
}
```
  - la chiamata API è atta a modificare una prenotazione esistente, cambiando il numero di posti prenotati
    - nel caso in cui il nuovo numero sia minore del precedente, il profilo di pagamento fornito serve ad eseguire lo storno
    - altrimenti, sarà il destinatario dell'addebito
  - è necessario specificare: il token utente, l'identificatore della prenotazione, un account bancario, e il numero di posti desiderato
    - in caso di errore, il parametro "status" è impostato su "error", e il campo "reason" contiene la descrizione dell'errore
    - se il numero di posti richiesti è uguale a quello già presente, viene restituito uno "status" pari ad "alert", e il campo "problem" che spiega il problema incontrato
    - in caso di successo, "status" contiene "ok", e "action" descrive l'azione eseguita

- ### `/api/delete-event/`
  - è necessario impiegare il metodo POST, specificando i dati necessari come segue
```json 
{
  "token" : token,
  "event-id" : eventID
}
```
  - la chiamata api è atta a eliminare un evento 
  - solo il creatore dell'evento lo può eliminare
  - inoltre, un evento è eliminabile solo se nessuna prenotazione circa quell'evento è stata effettuata
  - è necessario specificare il token dell'utente e l'identificatore dell'evento
    - in caso di errore il campo "status" contiene error, e "reason" il motivo dell'errore
    - in caso di successo il campo "status" contiene "ok"

## Lib
- all'interno della cartella "lib" sono presenti quattro sottocartelle: rust, python, javascript, bash
- ognuna contiene al suo interno i file di libreria associati al linguaggio nominato nella cartella

## Client
- il client HTTP fornisce servizi quali:
  - autenticazione
  - registrazione
  - richiesta di token di accesso
  - mostrare tutti gli eventi disponibili 
  - mostrare il formato delle varie chiamate API disponibili