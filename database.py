# -*- coding: utf-8 -*- noqa
"""
Created on Sun Dec 15 23:26:15 2024

@author: Joel Tapia Salvador
"""
import logging
import sqlite3


class Database():
    """SQL Lite Database."""

    conn = None
    cur = None

    def __init__(self):
        logging.info("Initialazing Database.")

        if self.conn is not None:
            return
        self.conn = sqlite3.connect("airQ.db")
        self.cur = self.conn.cursor()
        self.cur.row_factory = lambda cursor, row: row[0]

    def add_data(self, data_to_add: dict[str, float]):
        """
        Add air data to the Database.

        Parameters
        ----------
        data_to_add : dictionary[string, float]
            Dictionary with the data columns to add.

        Returns
        -------
        None.

        """
        logging.debug('Adding data to Database.')

        logging.debug(data_to_add)

        array = [
            data_to_add['Temp'],
            data_to_add['Hum'],
            data_to_add['VOC'],
            data_to_add['PM1'],
            data_to_add['PM2.5'],
            data_to_add['PM10'],
        ]

        self.cur.execute("INSERT INTO airq VALUES (?, ?, ?, ?, ?, ?)", array)
        self.conn.commit()

    def get_data(self) -> dict[str, float]:
        """
        Get the air data from the database.

        Returns
        -------
        data : dictionary[string, float]
            Dictionary with all the data of all the columns of the database.

        """
        logging.debug('Getting data from Database.')

        data = {
            'Temp': self.cur.execute("SELECT temp FROM airq").fetchall(),
            'Hum': self.cur.execute("SELECT hum FROM airq").fetchall(),
            'VOC': self.cur.execute("SELECT voc FROM airq").fetchall(),
            'PM1': self.cur.execute("SELECT pm1 FROM airq").fetchall(),
            'PM2.5': self.cur.execute("SELECT pm25 FROM airq").fetchall(),
            'PM10': self.cur.execute("SELECT pm10 FROM airq").fetchall(),
        }
        logging.debug(data)

        return data


if __name__ == "__main__":
    raise SystemExit(
        'You are executing a package-module file.' +
        ' Execute a main instead and import the module.')
