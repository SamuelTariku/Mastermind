
import sqlite3

conn = sqlite3.connect(":memory:")
print("Database connected")


conn.execute(
    """
CREATE TABLE Todo (
	"ID"	INTEGER NOT NULL UNIQUE,
	"Name"	TEXT NOT NULL,
	"Type"	TEXT NOT NULL,
	"Repeat"	INTEGER NOT NULL,
	"Priority"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT)
)
    """
)


conn.execute(
    """
    insert into todo (name, type, repeat)
    values ('database', 'normal', 0);
    """
)
conn.execute(
    """
    insert into todo (name, type, repeat)
    values ('website', 'normal', 0);
    """
)

conn.execute(
    """
    insert into todo (name, type, repeat)
    values ('another website', 'normal', 0);
    """
)

conn.execute(
    """insert into todo (name, type, repeat)
    values ({taskName}, {taskType}, {taskRepeat});
    """.format(
        taskName="'workout'",
        taskType="'normal'",
        taskRepeat=0
    )
)

conn.execute(
    """
    update todo set {updateField} = {updateValue} where {idField}={idValue};
    """.format(updateField="Type", updateValue="'general'", idField="id", idValue=1)

)

conn.execute(
    """
    delete from todo where {idField}={idValue};
    """.format(idField="id", idValue=2)
)


# cursor = conn.execute("select id, name, type, repeat from todo;")
# for row in cursor:
#     print("ID: {id} | Name: {name} | Type: {type}| Repeat: {repeat}".format(
#         id=row[0], name=row[1], type=row[2], repeat=row[3]
#     ))

print()
cursor = conn.execute(
    "select id, name, type, repeat from todo where name LIKE '%database%';")
for row in cursor:
    print("ID: {id} | Name: {name} | Type: {type}| Repeat: {repeat}".format(
        id=row[0], name=row[1], type=row[2], repeat=row[3]
    ))


cursor = conn.execute(
    "select id, name, type, repeat from todo order by name asc;")

for row in cursor:
    print("ID: {id} | Name: {name} | Type: {type}| Repeat: {repeat}".format(
        id=row[0], name=row[1], type=row[2], repeat=row[3]
    ))
