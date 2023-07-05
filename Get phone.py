@app.route('/GetPhone', methods=['POST'])
def getphone():
        ret = {}
        ret["UID"] = []
        ret["Phone"] = []
        json_data = request.get_json()
        uids = json_data["UIDS"]
        if type(uids) == type(str(" ")):
                cheking_phone = ("""SELECT telephone FROM destination WHERE id = %s""")
                cursor.execute(cheking_phone, [uids])
                phone = cursor.fetchall()
                ret["UID"].append(uids)
                if phone[0][0] == None:
                        ret["Phone"].append("Phone not found")
                elif phone:
                        ret["Phone"].append(phone[0][0])
                else:
                        ret["Phone"].append("Phone not found")
        else:
                for uid in json_data["UIDS"]:
                        cheking_phone = ("""SELECT telephone FROM destination WHERE id = %s""")
                        cursor.execute(cheking_phone, [uid])
                        phone = cursor.fetchall()
                        ret["UID"].append(uid)
                        if phone[0][0] == None:
                                ret["Phone"].append("Phone not found")
                        elif phone:
                                ret["Phone"].append(phone[0][0])
                        else:
                                ret["Phone"].append("Phone not found")
        return jsonify(ret)