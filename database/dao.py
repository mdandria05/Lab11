from database.DB_connect import DBConnect
from model.rifugio import Rifugio as r
from model.connessione import Connessione as c

class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    # TODO
    @staticmethod
    def getAllrifugi():
        conn = DBConnect.get_connection()
        result = []
        query = "SELECT * FROM rifugio"
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            result.append(r(row["id"], row["nome"], row["localita"]))
        cursor.close()
        conn.close()
        return result

    def getAllconnessioni_for_year(year : int):
        conn = DBConnect.get_connection()
        result = []
        query = """SELECT
                        r1.id as id1, r2.id as id2
                    FROM
                        connessione c,
                        rifugio r1,
                        rifugio r2
                    WHERE
                        r1.id = c.id_rifugio1 AND
                        r2.id = c.id_rifugio2 AND
                        r1.id != r2.id AND
                        c.anno <= %s
                    """
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query,(year,))
        for row in cursor:
            result.append(c(row["id1"], row["id2"]))
        cursor.close()
        conn.close()
        return result
