import sqlite3


class sqlite3_plus(object):
    def __init__(self, **args):
        self.path = args['path']
        self.tables = args['table']
        self.cmd = ''

    def _json(self, **args):
        data_arr = []
        for x in range(len(args['values'])):
            tmp = {}
            for i in range(len(args['keys'])):
                tmp[args['keys'][i]] = args['values'][x][i]
            data_arr.append(tmp)
        return data_arr

    def find(self):
        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        cursor.execute("PRAGMA table_info('"+self.tables+"')")
        res = cursor.fetchall()
        cursor.execute("select* from " + self.tables)
        data = cursor.fetchall()
        cols = []
        for x in res:
            cols.append(x[1])
        result = self._json(keys=cols, values=data)
        connect.commit()
        connect.close()
        return result

    def delete(self, **args):
        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        tmp = []
        for x in args:
            if type(args[x]) == list:
                for i in range(len(args[x])):
                    tmp.append(args[x][i])
            if len(tmp) > 0:
                self.cmd = 'DELETE FROM '+self.tables + ' WHERE ' + \
                    x+' in('+",".join(str(x) for x in tmp)+')'
            else:
                self.cmd = 'DELETE FROM '+self.tables + \
                    ' WHERE '+x+' in('+args[x]+')'
        cursor.execute(self.cmd)
        res = cursor.fetchall()
        connect.commit()
        connect.close()
        return res

    def add(self, **args):
        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        tmp_key = []
        tmp_value = []
        placeholder = []
        for x in args:
            tmp_key.append(x)
            placeholder.append('?')
            tmp_value.append(args[x])
        self.cmd = "INSERT INTO "+self.tables + " ("+",".join(str(x) for x in tmp_key)+") VALUES ("+",".join(str(x) for x in placeholder)+")"
        print(self.cmd)
        cursor.execute(self.cmd,tmp_value)
        res = cursor.fetchall()
        connect.commit()
        connect.close()
        return res

    def update(self, **args):
        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        tmp_value = []
        placeholder = []
        for x in args:
            if x !='ID':
                placeholder.append(x+'=?')
                tmp_value.append(args[x])
        if args['ID']:
            self.cmd = "UPDATE "+self.tables+" SET " + ",".join(str(x) for x in placeholder) + " where ID ="+args['ID']
        print(self.cmd)
        cursor.execute(self.cmd,tmp_value)
        res = cursor.fetchall()
        connect.commit()
        connect.close()
        return res

