# -*- coding: utf-8 -*-

import os
import sys
from config import CONFIG
sys.path = sys.path + CONFIG['paths']
import re
import subprocess as sp

def actualizar(modo='post'):

    if modo.lower() != 'pre' and modo.lower() != 'post':
        raise Exception('Modo "%s" incorrecto' % modo)

    # leer actualizaciones realizadas
    realizados = []
    if os.path.exists('./updates-done'):
        f_done = file('./updates-done', 'rb')
        try:
            for linea in f_done:
                m_issue = re.search(r'^(\w+)\s+(pre|post)', linea)
                if m_issue and m_issue.group(2) == modo.lower() and \
                m_issue.group(1) not in realizados:
                    realizados.append('%s    %s' % \
                                      (m_issue.group(1), m_issue.group(2)))

        finally:
            f_done.close()

    # realizar actualizaciones pendientes
    f = file('./updates', 'rb')
    f_done = file('./updates-done', 'a')
    try:
        for linea in f:
            m_coment = re.search(r'^#.+', linea)
            if m_coment:
                continue

            m_issue = re.search(r'^(\w+)\s+(pre|post)\s+([\w./]+)', linea, re.I | re.U)
            if m_issue:
                if m_issue.group(1) in realizados or \
                m_issue.group(2).lower() != modo.lower():
                    sys.stderr.write('Saltando actualización %s (%s)\n' % \
                                        (m_issue.group(1), m_issue.group(2)))

                else:
                    # obtener extensión del fichero de actualización
                    ext = os.path.splitext(m_issue.group(3))[1]
                    try:
                        sys.stdout.write('Actualizando %s (%s)\n' % \
                                            (m_issue.group(1), m_issue.group(2)))
                        if ext == '.py':
                            # ejecutar Python
                            sp.check_call([sys.executable, m_issue.group(3)])

                        elif ext == '.sql':
                            # ejecutar SQL
                            sys.stdout.write('Ejecutando SQL...\n')
                            sp.check_call([os.path.join(CONFIG['pg_path'], 'psql'),
                                           '-h', CONFIG['host'], 
                                           '-U', CONFIG['user'],
                                           '-d', CONFIG['db'],
                                           '-f', m_issue.group(3)]
                                    )

                        # registrar en fichero de actualizaciones realizadas (updates-done)
                        f_done.write('%s    %s\n' % (m_issue.group(1), modo))

                    except Exception, e:
                        sys.stderr.write(str(e))

    finally:
        f.close()
        f_done.close()

if __name__ == '__main__':
    modo = 'post'
    if len(sys.argv) > 1:
        modo = sys.argv[1]

    actualizar(modo)