import requests
import json


class Esercizio:
    def __init__(self, numero, testo, dati):
        self.numero = numero
        self.testo = testo
        self.dati = dati

    def consegna(self, risultato):
        r = requests.post(
            "{}/esercizi/{}".format(Verifica.url, self.numero),
            headers={"x-data": "True"},
            json={"data": risultato}
        )

        if r.status_code == 200:
            print(r.json()["message"])
        else:
            raise Exception(r.json()["message"])

    def __str__(self):
        return "{}\nDATI:\n{}".format(self.testo, json.dumps(self.dati, indent=4))


class Verifica:
    url = "http://192.168.1.231:8080"

    @staticmethod
    def firma(nome):
        r = requests.post(
            "{}/accreditamento".format(Verifica.url),
            json={"nome": nome.upper()}
        ).json()

        print(r["message"])

    @staticmethod
    def stampa_esercizi():
        r = requests.get("{}/esercizi".format(Verifica.url)).json()
        for i in range(len(r)):
            e = r[i]
            print("- {}: {} (+{})".format(i+1, e["message"], e["points"]))

    @staticmethod
    def stampa_voto():
        r = requests.get("{}/voto".format(Verifica.url))
        print(r.json().get("score", 0))

    @staticmethod
    def inizia_esercizio(numero):
        r = requests.get(
            "{}/esercizi/{}".format(Verifica.url, numero),
            headers={"x-data": "True"}
        )

        if r.status_code != 200:
            raise Exception(r.json()["message"])
        else:
            body = r.json()
            return Esercizio(numero, body["message"], body["data"])
