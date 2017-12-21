# android_message_db_updater
Upgrade Android mmssms.db

# Prerequisite
Python 3

# Usage
`python main.py old_mms_db.db new_mms_db.db`

Where `old_mms_db.db` is the SMS/MMS database file from your old rom/phone, 

`new_mms_db.db` is the new SMS/MMS database file you gonna create.

# Paths

For Android 7.0 Nougat, the new database is located at:

`/data/user_de/0/com.android.providers.telephony/databases`

Source: https://forum.xda-developers.com/showpost.php?p=68354161&postcount=5

[My orginal solution to Android 7.0 Nougat SMS/MMS Database Migration](https://forum.xda-developers.com/showpost.php?p=74281647&postcount=23)

