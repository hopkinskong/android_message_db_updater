import sys
import os.path
from shutil import copyfile
import sqlite3

new_sql_db_template = 'mmssms_android_7_1_2.db'

if len(sys.argv) != 3:
	print("Usage: " + sys.argv[0] + " <filename of old sms database> <filename of new sms database>")
	exit()

old_sql_db = sys.argv[1]
new_sql_db = sys.argv[2]

print("Android Message DB Updater by Hopkins Kong\n")

if old_sql_db == new_sql_db or new_sql_db == new_sql_db_template:
	print ("Please use another file name for hte new sms database, exiting...")
	exit()

if os.path.isfile(new_sql_db_template) != True:
	print ("Error: Template database file does not exists, exiting...")
	exit()

if os.path.isfile(old_sql_db) != True:
	print ("Error: Old SMS DB does not exists, exiting...")
	exit()
	

print("Using the following database for reading: " + old_sql_db)
print("Using the following database for writing: " + new_sql_db)

print("Creating new database from template...")
copyfile(new_sql_db_template, new_sql_db)
	
old_db_conn = sqlite3.connect(old_sql_db)
new_db_conn = sqlite3.connect(new_sql_db)
old_db_cursor = old_db_conn.cursor()
new_db_cursor = new_db_conn.cursor()

# Processing table "addr"
print("Update table \"addr\"...")
old_db_cursor.execute('SELECT * FROM addr')
data = old_db_cursor.fetchall()
print("addr: total rows=" + str(len(data)))
new_db_cursor.executemany('INSERT INTO addr VALUES(?,?,?,?,?,?)', data)
new_db_conn.commit()

# Processing table "android_metadata", only one row exists
print("Update table \"android_metadata\"...")
old_db_cursor.execute('SELECT * FROM android_metadata')
data = old_db_cursor.fetchone()
print("android_metadata: locale=" + str(data[0]))
new_db_cursor.execute('INSERT INTO android_metadata VALUES(?)', (str(data[0]),))
new_db_conn.commit()

# Processing table "attachments"
print("Update table \"attachments\"...")
old_db_cursor.execute('SELECT * FROM attachments')
data = old_db_cursor.fetchall()
print("attachments: total rows=" + str(len(data)))
new_db_cursor.executemany('INSERT INTO attachments VALUES(?,?,?)', data)
new_db_conn.commit()

# Table "blocklist" does not exists in new DB format, ignored

# Processing table "canonical_addresses"
print("Update table \"canonical_addresses\"...")
old_db_cursor.execute('SELECT * FROM canonical_addresses')
data = old_db_cursor.fetchall()
print("canonical_addresses: total rows=" + str(len(data)))
new_db_cursor.executemany('INSERT INTO canonical_addresses VALUES(?,?)', data)
new_db_conn.commit()

# Table "cbch", "cmas", "contacts1", "contacts2" does not exists in new DB format, ignored

# Processing table "drm"
print("Update table \"drm\"...")
old_db_cursor.execute('SELECT * FROM drm')
data = old_db_cursor.fetchall()
print("drm: total rows=" + str(len(data)))
new_db_cursor.executemany('INSERT INTO drm VALUES(?,?)', data)
new_db_conn.commit()

# Table "htcmsgs", "htcthreads", "name_lookup" does not exists in new DB format, ignored

# Processing table "part", only some of the columns are selected
print("Update table \"part\"...")
old_db_cursor.execute('SELECT _id,mid,seq,ct,name,chset,cd,fn,cid,cl,ctt_s,ctt_t,_data,text FROM part')
data = old_db_cursor.fetchall()
print("part: total rows=" + str(len(data)))
new_db_cursor.executemany('INSERT INTO part VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)', data)
new_db_conn.commit()

# Processing table "pdu", only some of the columns are selected
print("Update table \"pdu\"...")
old_db_cursor.execute('SELECT _id,thread_id,date,date_sent,msg_box,read,m_id,sub,sub_cs,ct_t,ct_l,exp,m_cls,m_type,v,m_size,pri,rr,rpt_a,resp_st,st,tr_id,retr_st,retr_txt,retr_txt_cs,read_status,ct_cls,resp_txt,d_tm,d_rpt,locked,sub_id,seen,creator,text_only FROM pdu')
data = old_db_cursor.fetchall()
print("pdu: total rows=" + str(len(data)))
new_db_cursor.executemany('INSERT INTO pdu VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', data)
new_db_conn.commit()

# Processing table "pending_msgs"
print("Update table \"pending_msgs\"...")
old_db_cursor.execute('SELECT * FROM pending_msgs')
data = old_db_cursor.fetchall()
print("pending_msgs: total rows=" + str(len(data)))
new_db_cursor.executemany('INSERT INTO pending_msgs VALUES(?,?,?,?,?,?,?,?,?,?)', data)
new_db_conn.commit()

# Processing table "rate"
print("Update table \"rate\"...")
old_db_cursor.execute('SELECT * FROM rate')
data = old_db_cursor.fetchall()
print("rate: total rows=" + str(len(data)))
new_db_cursor.executemany('INSERT INTO rate VALUES(?)', data)
new_db_conn.commit()

# Table "raw" will be ignored, there are extra columns in the new DB, don't know how to handle it yet

# Processing table "sms", only some of the columns is selected
print("Update table \"sms\"...")
old_db_cursor.execute('SELECT _id,thread_id,address,person,date,date_sent,protocol,read,status,type,reply_path_present,subject,body,service_center,locked,sub_id,error_code,creator,seen,priority FROM sms')
data = old_db_cursor.fetchall()
print("sms: total rows=" + str(len(data)))
new_db_cursor.executemany('INSERT INTO sms VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', data)
new_db_conn.commit()

# Processing table "sqlite_sequence"
print("Update table \"sqlite_sequence\"...")
old_db_cursor.execute('SELECT * FROM sqlite_sequence')
data = old_db_cursor.fetchall()
print("sqlite_sequence: total rows=" + str(len(data)))
new_db_cursor.executemany('INSERT INTO sqlite_sequence VALUES(?,?)', data)
new_db_conn.commit()

# Processing table "sr_pending"
print("Update table \"sr_pending\"...")
old_db_cursor.execute('SELECT * FROM sr_pending')
data = old_db_cursor.fetchall()
print("sr_pending: total rows=" + str(len(data)))
new_db_cursor.executemany('INSERT INTO sr_pending VALUES(?,?,?)', data)
new_db_conn.commit()

# Processing table "threads", there are extra columns in the new DB too, we are treating them as blank/null
print("Update table \"threads\"...")
old_db_cursor.execute('SELECT _id,date,message_count,recipient_ids,snippet,snippet_cs,read,archived,type,error,has_attachment FROM threads') # missing column "attachment_info" and "notification"
data = old_db_cursor.fetchall()
print("threads: total rows=" + str(len(data)))
new_db_cursor.executemany('INSERT INTO threads VALUES(?,?,?,?,?,?,?,?,?,?,?,NULL,0)', data)
new_db_conn.commit()

# Processing table "words_content"
print("Update table \"words_content\"...")
old_db_cursor.execute('SELECT * FROM words_content')
data = old_db_cursor.fetchall()
print("words_content: total rows=" + str(len(data)))
new_db_cursor.executemany('INSERT INTO words_content VALUES(?,?,?,?,?)', data)
new_db_conn.commit()

# Processing table "words_segdir"
print("Update table \"words_segdir\"...")
old_db_cursor.execute('SELECT * FROM words_segdir')
data = old_db_cursor.fetchall()
print("words_segdir: total rows=" + str(len(data)))
new_db_cursor.executemany('INSERT INTO words_segdir VALUES(?,?,?,?,?,?)', data)

# Processing table "words_segments"
print("Update table \"words_segments\"...")
old_db_cursor.execute('SELECT * FROM words_segments')
data = old_db_cursor.fetchall()
print("words_segments: total rows=" + str(len(data)))
new_db_cursor.executemany('INSERT INTO words_segments VALUES(?,?)', data)
new_db_conn.commit()

old_db_conn.close()
new_db_conn.close()

print("All done.")