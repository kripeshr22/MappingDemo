from import_to_heroku import connect_to_heroku_db
import psycopg2 as pg
import psycopg2.extras

def main():
    ''' 
    Creates the table laclean_pre2018_table, which contains all the data 
    from cleanlacountytable except the rows that have landbaseyear from 
    2018 to 2021. This table is used by rf_lvpersqft.py to get the most recent
    assessed value for each property excluding the years 2018 to 2021.
    '''
    conn = connect_to_heroku_db()
    cur = conn.cursor()

    # create table/rewrite it if it exists
    cur.execute("drop table if exists laclean_pre2018_table")
    # create a copy of the cleanlacountytable
    cur.execute("create table laclean_pre2018_table as table cleanlacountytable")
    # delete the rows where landbase year is 2018-2021
    cur.execute("delete from laclean_pre2018_table where landbaseyear=\'2018\' or landbaseyear=\'2019\' or landbaseyear=\'2020\' or landbaseyear=\'2021\'")
    conn.commit()
    cur.close()

if __name__ == "__main__":
    main()
