#!/bin/python3

import re

input_str = 'ifadiof=aio=ejsapo.fjdpdp.jofevento1=5423.fofsnofdpsfpifp=ifnspfsonf.sevento3=9999.fspnofsp.nisdpifsd=evento2=0001.fjifsdpopmsvs.='

eventos = re.split(r'(evento[0-9]*=[0-9]*)', input_str, flags=re.IGNORECASE)
eventos = sorted(filter(lambda x: x.startswith('evento'), eventos))

print(' / '.join(eventos))

print(' / '.join(filter(lambda x: int(x.split('=')[1]) < 6000, eventos)))

for eve in eventos:
    if eve.split('=')[1] == '0001':
        print('Vou entrar no QA', end='')
    elif int(eve.split('=')[1]) > 2:
        print('!', end='')
print('')
