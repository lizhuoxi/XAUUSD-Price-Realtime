#!/usr/bin/env python
# encoding: utf-8

import pickle

def str2dict():
    apiUser = raw_input("Please input your apiUser:")
    apiKey = raw_input("Please input your apiKey:")
    smsApiKey = raw_input("Please input your smsApiKey:")
    email = raw_input("Please input your email:")
    phone = raw_input("Please input your phone:")
    dic =  {"apiUser":apiUser,
            "apiKey":apiKey,
            "smsApiKey":smsApiKey,
            "email":email,
            "phone":phone
            }
    return dic

def saveKey(dic, path):
    with open(path, "wb") as f:
        pickle.dump(dic, f)

def loadKey(path):
    with open(path, "rb") as f:
        ret =  pickle.load(f)
    return ret
def main():
    dic = str2dict()
    path = (r'..\key.pkl')
    saveKey(dic, path)
    loadKey(path)

if __name__ == '__main__':
    main()