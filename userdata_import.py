#!/usr/bin/env python

import os,django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OnlineSystem.settings")
django.setup()


from django.contrib.auth.models import User



def main():

    user_list = ['Cheng Vicky', 'Fan Yixiang', 'Francesco Abrahao', 'Gao Allen', 'Li Shaw', 'Liu Athena', 'Shi Leo',
                 'Shou Cabby', 'Farinelli Alexandre', 'Veronica YIN', 'XU Gary', 'Yan Jun', 'Zhan Ye', 'Zhang Yupeng',
                 'Zhu Frank']
    for user in user_list:
        user_firstname=user.split(' ')[0]
        user_lastname=user.split(' ')[1]
        User.objects.create(username=user_lastname,first_name=user_firstname,last_name=user_lastname,password='123qweasdzxc')

if __name__ == '__main__':
    main()
    print('User import done!')