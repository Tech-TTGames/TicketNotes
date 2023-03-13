"""
This script is to be used to load the config file into the database.
It will create the schema and tables if they do not exist.
An interactive prompt will guide you through the creation of the config file.
"""
import json
import pathlib
import sys

from sqlalchemy import URL, create_engine, schema
from sqlalchemy.orm import create_session

PROG_DIR = pathlib.Path(__file__).parent.parent.absolute()
print(PROG_DIR)
sys.path.append(str(PROG_DIR))


# pylint: disable=wrong-import-position
# pylint: disable=import-error # It works, I promise.
from tickets_plus.database.models import (  # isort:skip
    Base,
    CommunityRole,
    Guild,
    ObserversRole,
    StaffRole,
    TicketBot,
)
from tickets_plus.database.statvars import Config, MiniConfig  # isort:skip


# pylint: disable=invalid-name
if __name__ == "__main__":
    print("Starting migration script...")
    new = 0
    legacy = 0
    if pathlib.Path(PROG_DIR, "config.json").exists():
        print("Existing config file found. Attempting to cache...")
        cnfg = Config("offline", True)
        try:
            cnfg.cnfg()["guild"]
        except KeyError:
            print(
                "Config is not pre-v0.1 template. Attempting to cache v0.1 template..."
            )
        else:
            print("Config is pre-v0.1 template.")
            legacy = 1
        if not legacy:
            cnfg = MiniConfig()
            try:
                cnfg.get_url()
            except KeyError:
                print("Config is not a valid template.")
            else:
                print("Config is a v0.1 template.")
                new = 1
    print("Entering interactive prompt...")
    match new:
        case 0:
            print(
                "This is a migration script to help you"
                " migrate from the old config file to the new database."
            )
            print(
                "The new config file contains information about the database connection."
            )
            print(
                "The new database contains all the information about the tickets and"
                " the guilds and the data previously stored in config."
            )
            print(
                "This script will create the database schema and tables if they do not exist."
            )
            print("It will also load the config file into the database.")
            create = input("Would you like to create the new config file? (Y/N)\n")
            if create == "Y":
                print(
                    "I will now guide you through the creation of the new config file."
                )
                print("Please answer the following questions.")
                print("The default values are in parentheses.")
                print(
                    "If you are unsure of the answer,"
                    " please consult the documentation or a professional."
                )
                config = {}
                dbarch = input("What is the database type? (postgresql)\n")
                if dbarch == "":
                    dbarch = "postgresql"
                dbdriver = input("What is the database driver? (psycopg)\n")
                if dbdriver == "":
                    dbdriver = "psycopg"
                config["dbtype"] = dbarch + "+" + dbdriver
                dbhost = input("What is the database host? (localhost)\n")
                if dbhost == "":
                    dbhost = "localhost"
                config["dbhost"] = dbhost
                dbport = input("What is the database port? (5432)\n")
                if dbport == "":
                    dbport = "5432"
                config["dbport"] = int(dbport)
                dbname = input("What is the database name? (tickets_plus)\n")
                if dbname == "":
                    dbname = "tickets_plus"
                config["dbname"] = dbname
                dbuser = input("What is the database user? (postgres)\n")
                if dbuser == "":
                    dbuser = "postgres"
                config["dbuser"] = dbuser
                dbpass = input("What is the database password? (password)\n")
                if dbpass == "":
                    dbpass = "password"
                config["dbpass"] = dbpass

                print("This is the end of the database configuration.")
                dev_guild_id = input("What is the developer guild ID?\n")
                config["dev_guild_id"] = int(dev_guild_id)

                print("This is the end of the configuration.")
                print(
                    "The following is the configuration that will be written to the file."
                )
                configjson = json.dumps(config, indent=4)
                print(configjson)
                write = input(
                    "Would you like to write this to the config file? (Y/N)\n"
                )
                if write == "Y":
                    if new:
                        write = input(
                            "Would you like to overwrite the existing config file? (Y/N)\n"
                        )
                    if write == "Y":
                        with open(
                            pathlib.Path(PROG_DIR, "config.json"), "w", encoding="utf-8"
                        ) as f:
                            f.write(configjson)
                        print("Config file saved.")
                print(
                    "I will now create the database schema and tables if they do not exist."
                )
                engine = create_engine(URL.create(**config))
                with engine.begin() as conn:
                    conn.execute(
                        schema.CreateSchema("tickets_plus", if_not_exists=True)
                    )
                    Base.metadata.create_all(engine, checkfirst=True)
                    print("Database schema and tables created.")
                if legacy:
                    upld = input(
                        "Would you like to upload the old config file to the database? (Y/N)\n"
                    )
                    if upld == "Y":
                        print("Parsing old config file...")
                        dic = cnfg.cnfg()  # type: ignore
                        print("Uploading old config file to database...")
                        for item in dic.items():
                            with create_session(engine) as session:
                                data = Guild(
                                    guild_id=dic["guild_id"],
                                    open_message=dic["open_msg"],
                                    staff_team_name=dic["staff_team"],
                                    msg_discovery=dic["msg_discovery"],
                                    strip_buttons=dic["strip_buttons"],
                                )
                                session.add(data)
                                tusers = []
                                for tusers in dic["ticket_users"]:
                                    tusers.append(TicketBot(user_id=tusers, guild=data))
                                session.add_all(tusers)
                                data.ticket_bots = tusers
                                staff = []
                                for staff in dic["staff"]:
                                    staff.append(StaffRole(role_id=staff, guild=data))
                                session.add_all(staff)
                                data.staff_roles = staff
                                obsr = []
                                for obsr in dic["observers"]:
                                    obsr.append(ObserversRole(role_id=obsr, guild=data))
                                session.add_all(obsr)
                                data.observers_roles = obsr
                                croles = []
                                for croles in dic["community_roles"]:
                                    croles.append(
                                        CommunityRole(role_id=croles, guild=data)
                                    )
                                session.add_all(croles)
                                data.community_roles = croles
                                session.commit()
                                print("Old config file uploaded to database.")
                                session.close()

        case 1:
            print("A valid v0.1 config file was found.")
            print(
                "If you would like to create a new config file, please delete the existing one."
            )
            print(
                "I will now create the database schema and tables if they do not exist."
            )
            engine = create_engine(cnfg.get_url())  # type: ignore
            with engine.begin() as conn:
                conn.execute(schema.CreateSchema("tickets_plus", if_not_exists=True))
                Base.metadata.create_all(engine, checkfirst=True)
                print("Database schema and tables created.")

    data = input("This script has finished, enter ev to enter an interactive eval.\n")
    if data == "ev":
        while True:
            try:
                code = input(">>> ")
                if code == "exit":
                    break
                exec(code)  # pylint: disable=exec-used # skipcq: PYL-W0122
            except Exception as e:  # pylint: disable=broad-except # skipcq: PYL-W0703
                print(e)
    print("Goodbye!")
