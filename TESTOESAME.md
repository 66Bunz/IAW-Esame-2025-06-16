**Introduzione alle Applicazioni Web \- Appello del 16/06/2025**

# Progetto d’esame

# **MODALITÀ D’ESAME**

L’esame di Introduzione alle Applicazioni Web consta di due parti, strettamente collegate ed entrambe obbligatorie:

1. Progettazione e realizzazione individuale di un’applicazione web.
2. Dimostrazione e discussione orale sul progetto.

La valutazione dei progetti e la dimostrazione/orale riguarderà il materiale consegnato prima dell’appello. La dimostrazione e la breve discussione orale inerente il progetto è da svolgersi secondo il calendario che sarà reso disponibile qualche giorno prima dell’appello, previa registrazione all’appello stesso.

La discussione riguarderà le scelte di progettazione (layout, struttura del codice, struttura del DB, ecc.) nonché le scelte implementative e funzionali adottate.

# **DESCRIZIONE E REQUISITI**

Il progetto consiste in un’applicazione web che deve soddisfare alcuni requisiti tecnici, stilistici e funzionali, dettagliati in seguito.

L’applicazione web dovrà utilizzare le tecnologie illustrate e sperimentate durante il corso.

## Requisiti logistici

- Il progetto deve essere realizzato individualmente.
- Non è prevista né accettabile una consegna (parzialmente o totalmente) in comune con un altro studente del corso.
- Il progetto deve essere consegnato secondo le tempistiche riportate nell’ultima pagina di questo documento.
- Non è prevista né accettabile una consegna in ritardo.

## Requisiti tecnici

L’applicazione web deve rispettare i seguenti requisiti tecnici:

- Utilizzo di HTML5 e CSS3, avvalendosi se necessario di framework esterni come Bootstrap, ma personalizzandone lo stile tramite regole create ad-hoc.
- Utilizzo di Flask e di SQLite (come database relazionale), per il back-end.
- Utilizzo di Flask-Login per la gestione dell’autenticazione.

Inoltre:

- L’applicazione web deve avere un target di dispositivi ben preciso (desktop, mobile oppure tablet), a scelta degli studenti, eventualmente supportando la modalità responsive.
- Eventuali form utilizzati nel progetto devono essere **validati** sia nel front-end che nel back-end, come spiegato durante il corso.
- Il progetto consegnato deve essere interamente testabile dal docente e deve funzionare sulle ultime versioni di Chrome (111+) e Firefox (110+).
- Il codice sorgente deve essere ben scritto e corredato di opportuni commenti laddove necessario.
- Tutte le tecnologie elencate in precedenza devono essere integrate in maniera coesa e uniforme all’interno di un’unica applicazione web.

**Extra:**

- Fare il deploy dell’applicazione web su PythonAnywhere ([https://www.pythonanywhere.com/](https://www.pythonanywhere.com/)).

## Requisiti stilistici

L’applicazione web deve rispettare i seguenti requisiti stilistici:

- Utilizzo di tag HTML in maniera semantica (per esempio, non tutto è un \<div\>).
- No tag HTML deprecati.
- Non utilizzare dichiarazioni CSS inline, mantenendo cioè le regole CSS separate dalla struttura semantica del HTML.

Inoltre, l’applicazione web deve essere sufficientemente “usabile”.

## Descrizione (requisiti funzionali)

Si vuole creare un'applicazione web per la **gestione di un festival musicale** che si svolge in una località a scelta degli studenti/esse. Per semplicità, l’applicazione sarà dedicata a un solo festival e a una sola edizione (annuale), che si terrà durante un weekend, da venerdì a domenica. L’applicazione web deve supportare due tipi di utenti registrati: i **partecipanti** e gli **organizzatori**.

I **partecipanti** possono esplorare il programma delle performance musicali previste durante il weekend del festival e acquistare biglietti per partecipare. Prima di poter agire da partecipante, l’utente deve registrarsi e fare login. Il login/registrazione richiede un campo univoco che sarà utilizzato per riconoscere l’utente nel sito (per esempio, la mail). L’acquisto dei biglietti è simulato all’interno dell’applicazione e non prevede l’integrazione con servizi di pagamento reali.

Gli **organizzatori**, invece, potranno gestire le performance in programma, anch’essi attraverso login/registrazione. In particolare, gli organizzatori potranno inserire e modificare i dettagli delle performance e monitorare le vendite dei biglietti. Al momento della creazione di una nuova performance, il sistema dovrà impedire che vengano inserite performance che si sovrappongono nello stesso palco e orario **rispetto a quelle già pubblicate**, così da garantire che ogni palco ospiti una sola performance alla volta. **Gli organizzatori possono modificare liberamente le proprie performance finché non vengono pubblicate, inclusi data, ora e palco**.

Ogni performance presente nel sito avrà associate le seguenti informazioni (obbligatorie):

- Nome dell’artista o del gruppo (**ogni artista può esibirsi una sola volta all’interno dello stesso festival**)
- Giorno e orario di inizio (venerdì, sabato o domenica)
- Durata prevista (in minuti)
- Breve descrizione della performance
- Nome del palco (tra quelli disponibili, vedi sotto)
- Genere musicale
- Immagine/i promozionale/i dell’artista
- Se è pubblicata (= visibile a tutti) oppure no (= visibile solo all’organizzatore)

I palchi disponibili nel festival possono avere i nomi che preferite. Per semplicità, si propongono i seguenti esempi:

- Palco A (Main Stage)
- Palco B (Secondary Stage)
- Palco C (Experimental Stage)

I **partecipanti** possono acquistare uno dei seguenti tipi di biglietto:

- Biglietto Giornaliero (valido per un solo giorno, a scelta tra venerdì, sabato o domenica)
- Pass 2 Giorni (valido per due giorni consecutivi a scelta)
- Full Pass (valido per tutti e tre i giorni del festival)

Ogni partecipante può acquistare **un solo tipo di biglietto per edizione**. Una volta acquistato un biglietto, non sarà possibile comprarne un altro di tipo diverso (ad esempio, chi acquista un biglietto giornaliero non potrà successivamente acquistare un pass 2 giorni o un full pass). I biglietti non sono rimborsabili né modificabili. Inoltre, il numero massimo di partecipanti ammessi per ciascun giorno del festival è di **200 persone**: una volta raggiunta tale soglia, non sarà più possibile acquistare biglietti validi per quel giorno.

Nella homepage dell’applicazione, i **partecipanti** vedranno una versione breve delle performance disponibili (cioè pubblicate), ordinate per giorno e orario crescenti. Tramite appositi filtri, potranno anche esplorare le performance in base al giorno, al palco o al genere musicale. Cliccando su ogni performance, sarà possibile visualizzarne la versione completa con tutte le informazioni.

Una volta effettuato l’acquisto, i biglietti saranno visibili nella pagina profilo del partecipante, dove sarà indicato il tipo di biglietto e i giorni inclusi.

Gli **organizzatori**, in maniera simile, avranno una pagina profilo in cui saranno mostrate **tutte** le performance pubblicate, **mentre tra le performance non pubblicate saranno visibili solo le proprie bozze**. Per ogni performance, solo se non ancora pubblicata, sarà possibile modificarne le informazioni. Se pubblicata, non sarà più possibile apportare modifiche. Inoltre, gli organizzatori potranno visualizzare le statistiche delle vendite dei biglietti per ogni giorno del festival.

Gli organizzatori potranno navigare il sito come i partecipanti ma non potranno acquistare biglietti. Un partecipante non può diventare un organizzatore. Infine, un utente non registrato può navigare liberamente il sito (ma non inserire eventi o acquistare biglietti).

**Nota:** alla consegna, l’applicazione web dovrà contenere almeno **5** utenti registrati (due organizzatori e **tre** partecipanti), alcune performance inserite (almeno 5 per ogni giorno del festival, una delle quali non pubblicata), e biglietti acquistati con diverse tipologie (ad esempio, almeno una richiesta di acquisto di biglietto giornaliero, una di pass 2 giorni e una di full pass). I nomi utente e le password di questi account dovranno essere forniti ai docenti per la verifica.

🔥Si incoraggia a esprimere pienamente la propria creatività nella scelta degli artisti, del nome del festival, del tema e degli altri dettagli, per realizzare un progetto originale e personalizzato\!

# **ISTRUZIONI PER LA CONSEGNA DEL PROGETTO**

La consegna del progetto deve avvenire tramite lo strumento “**Consegna Elaborati**” presente nella pagina del corso sul *Portale della Didattica*, entro le **23:59 del 15 Giugno 2025**.

La consegna dovrà contenere in un unico archivio (.zip):

- Codice sorgente dell’applicazione web realizzata, incluse:
  - eventuali dipendenze (in un file come requirements.txt), immagini, …
  - file SQLite contenente il database
- Un documento di testo (.md o .txt) contenente:
  - le credenziali degli utenti;
  - eventuali istruzioni per provare l’applicazione web;
  - se è stato fatto, l’indirizzo a cui l’applicazione web è visibile dopo il deploy.