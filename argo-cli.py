import argoscuolanext;
import sys;
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter

isRepl = False

session = argoscuolanext.Session()
history = InMemoryHistory()
completer = WordCompleter(["docenti" ,"esci", "anagrafica", "giustifica", "voti", "assenze", "argomenti", "filtro"])
if sys.stdout.isatty():
    ps = PromptSession(history=history, enable_history_search=True, auto_suggest=AutoSuggestFromHistory(), completer=completer, complete_while_typing=False)
print("Argo CLI")
login = session.login("ss16825", "mascolo", "manoplay");
print("Accesso eseguito")
command = ""
while command != "esci":
    if 'ps' in vars():
        command = ps.prompt("Argo>")
    else:
        command = input("Argo>")
    if command == "docenti":
        for item in session.docenticlasse():
            print(item["docente"]["nome"] + " " + item["docente"]["cognome"] + item["materie"])
    elif command == "promemoria":
        for promemoria in session.promemoria()['dati']:
            print(promemoria['desAnnotazioni'] + " (" + promemoria['desMittente'] + ") - " + promemoria['datGiorno'])
    elif command == "assenze":
        for assenza in session.assenze()["dati"]:
            giustificata = ""
            if assenza["flgDaGiustificare"]:
                giustificata = "giustificata"
            else:
                giustificata = "non giustificata"
            print("Assenza " + giustificata + " in giorno " + assenza["datAssenza"] + " registrata da " + assenza["registrataDa"])
    elif command == "anagrafica":
        print("Alunno: " + login[0] ["alunno"]["desNome"] + " " + login[0]["alunno"]["desCognome"])
        print("Indirizzo: " + login[0]["alunno"]["desVia"] + " - " + login[0]["alunno"]["desComuneRecapito"])
        print("Nato il " + login[0]["alunno"]["datNascita"] + " a " + login[0]["alunno"]["desComuneNascita"])
        print("Sesso: " + login[0]["alunno"]["flgSesso"])
        if (login[0]["alunno"]["desTelefono"] is None):
            print("Telefono: " + login[0]["alunno"]["desCellulare"] + " - Numero di casa non disponibile")
        else:
            print("Telefono: " + login[0]["alunno"]["desCellulare"] + " (cellulare) - " + login[0]["alunno"]["desTelefono"] + " (casa)")
        print("Scuola: " + login[0]["desScuola"])
    elif command.startswith("giustifica"):
        print("Giustificare assenze non è ancora possibile, non per colpa nostra. Per ovvi motivi non è possibile giustificare le assenze direttamente dal registro.")
    elif command == "voti":
        if (session.votigiornalieri() == {}):
            print("I voti non sono attualmente disponibili. Forse sono stati cancellati. Riprova in un altro momento")
        else:
            print("Non implementato")
    elif command.startswith("argomenti"):
        args = command.replace("argomenti", "").strip(" ").lower()
        if args == "":
            for argomento in session.argomenti()["dati"]:
                print(argomento["desMateria"] + ": " + argomento["desArgomento"] + " " + argomento["docente"])
        elif args.startswith("del docente"):
            docente = args.replace("del docente", "").lstrip(" ")
            for argomento in session.argomenti()["dati"]:
                if docente in argomento["docente"].lower():
                    print(argomento["desArgomento"] + " - " + argomento["desMateria"])
        else:
            for argomento in session.argomenti()["dati"]:
                if args in argomento["desMateria"].lower():
                    print(argomento["desArgomento"] + " " + argomento["docente"])

    elif command.startswith("filtro"):
        print("Sintassi: filtro [categoria] [valore]\nEsempio: filtro argomenti LINGUA E CULTURA LATINA")
        print("Non ancora implementato")
    elif command == "compiti":
        for compito in session.compiti()["dati"]:
            print(compito["desMateria"] + ": " + compito["desCompiti"] + compito["docente"] + " - " + compito["datGiorno"])