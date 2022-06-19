import csv
import codecs

titles = ['Gossiping', 'C_Chat', 'Stock', 'NBA', 'Lifeismoney', 'Baseball', 'LoL', 'movie', 'MobileComm', 'Tech_Job', 'HatePolitics', 'KoreaStar', 'creditcard', 'Beauty', 'car']
posts_input = []
users_input = []
erroneous_data = []

def edit(str):
    str = str.replace('\'','’')
    return str.replace('"', '\\"')

for title in titles:
    with open(title + '.csv', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                user_to_insert = "insert into users (name) values ('" + row[0] + "');"
                if user_to_insert not in users_input:
                    users_input.append(user_to_insert)
                line_string = "('" + edit(row[1]) + "', '" + edit(row[5]) + "', '" + row[3] + "', '" + row[4] + "', '" + row[2] + "', '" + row[0] + "', '" + title + "');"
                table_string = "insert into posts (title, article, likes, hates, post_time, user_name, board_name) values "
                data_string = table_string + line_string
                posts_input.append(data_string)
                if len(row[2]) > 25:
                    erroneous_data.append(title + ', ' + row[1])
                line_count += 1

# for i in users_input[:3]:
#     print(i)
# for i in posts_input[:3]:
#     print(i)
print(len(users_input))
print(len(posts_input))
with open('users_input.sql', 'w') as f:
    for item in users_input:
        f.write("%s\n" % item)

file = codecs.open("posts_input.sql", "w", "utf-8")
for item in posts_input:
    file.write("%s\n" % item)
file.close()

file = codecs.open("error_data.sql", "w", "utf-8")
for item in erroneous_data:
    file.write("%s\n" % item)
file.close()