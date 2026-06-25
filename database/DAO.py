from database.DB_connect import DBConnect
from model.Constructor import Constructor


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllConstructors():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct constructorId, constructorRef, name, nationality
                    FROM constructors c 
                    order by constructorId """

        cursor.execute(query)

        for row in cursor:
            results.append(Constructor(row["constructorId"],
                                       row["constructorRef"],
                                       row["name"],
                                       row["nationality"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(year1, year2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct c.constructorId 
                    FROM constructors c 
                    join results r on c.constructorId = r.constructorId 
                    join races r2 on r2.raceId =r.raceId 
                    where r2.`year` BETWEEN %s AND %s
                    and r.`position` is not NULL  """

        cursor.execute(query,(year1,year2))

        for row in cursor:
            results.append(row["constructorId"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(year1, year2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT r.constructorId as IdCostruttore1, r2.constructorId as IdCostruttore2, count(distinct r.driverId) as peso
                    FROM results r 
                    join results r2 on r.driverId=r2.driverId 
                    join races r3 on r3.raceId=r.raceId 
                    join races r4 on r4.raceId =r2.raceId 
                    where r2.raceId != r.raceId 
                    and r.constructorId<r2.constructorId 
                    and r3.year  BETWEEN %s and %s
                    and r4.year BETWEEN %s and %s
                    and r2.`position` is not NULL 
                    and r.`position` is not NULL 
                    GROUP BY IdCostruttore1, IdCostruttore2 """

        cursor.execute(query, (year1, year2, year1, year2))

        for row in cursor:
            results.append((row["IdCostruttore1"],
                           row["IdCostruttore2"],
                            row["peso"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def setOlderDriver(idMapConstructors, year1, year2):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT r.constructorId, min(d.dob) as driverAnziano
                    FROM results r 
                    join drivers d on r.driverId = d.driverId 
                    JOIN races r2 on r.raceId  = r2.raceId 
                    where r.`position` IS NOT NULL 
                    and r2.`year` BETWEEN %s and %s
                    GROUP BY r.constructorId """

        cursor.execute(query, (year1, year2))

        for row in cursor:
            constructor= idMapConstructors[row["constructorId"]]
            constructor.oldest_driver_dob = row["driverAnziano"]
        cursor.close()
        conn.close()


