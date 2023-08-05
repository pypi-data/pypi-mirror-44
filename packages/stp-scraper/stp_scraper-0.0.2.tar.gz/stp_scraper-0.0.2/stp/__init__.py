import datetime
import os
import random
import re
import time

import boto3

from .client import Client
from .exceptions import EmptyFile, StpException
from .redshift_client import RedshiftClient

DEST_FILE_S3 = 'STP/transactions.txt'
DELAY_REQUEST = 30  # delay to load transactions correctly


client = Client()

# initialize redshift client
rs_client = RedshiftClient(
    os.environ['REDSHIFT_DATABASE_NAME'],
    os.environ['REDSHIFT_USER'],
    os.environ['REDSHIFT_PASSWORD'],
    os.environ['REDSHIFT_HOST'],
    os.environ['REDSHIFT_PORT'],
)


def random_gen():
    return str(random.randint(10 ** 15, 10 ** 16 - 1))


def remove_header(data):
    return re.split('\n', data, 1)[1]


def validate_date(date):
    if date:
        try:
            date = datetime.datetime.strptime(date, '%d/%m/%Y')
            now = datetime.datetime.now()
            if date > now:
                raise ValueError('Date cannot be greater than today')
        except ValueError:
            raise ValueError('Incorrect format date')


def verify_response(data):
    if data == '':
        raise EmptyFile('The transaction file obtained is empty')

    if data[:2] != 'id':
        raise StpException(
            'An error has occurred obtaining the transaction file'
        )


def extract(from_, to):
    validate_date(from_)
    validate_date(to)
    if not from_ and to:
        raise ValueError(
            'You cannot leave the "from" param in '
            'blank when set the "to" param'
        )
    elif from_ and not to:
        start_date = from_
        now = datetime.datetime.now()
        final_date = now.strftime('%d/%m/%Y')
    elif not from_ and not to:
        now = datetime.datetime.now()
        final_date = now.strftime('%d/%m/%Y')
        start_date = now - datetime.timedelta(days=7)
        start_date = start_date.strftime('%d/%m/%Y')
    else:
        start_date = from_
        final_date = to

    rs_client.execute(
        "INSERT INTO stp.transactions "
        "SELECT * "
        "FROM stp.temp_transactions stp "
        "WHERE stp.id not in (SELECT id from stp.transactions);"
    )
    rs_client.execute("DELETE FROM stp.temp_transactions;")
    rs_client.commit()

    # Sent Orders
    client.get(
        f'?wicket:interface=:2:mainBorder:menu:panel:menuSpei:panel:men'
        f'uConsultaOrdenes:tabs-container:tabs:1:link:'
        f'{client.interface}:ILinkListener::'
    )

    # Setting dates
    client.post(
        f'?wicket:interface=:2:mainBorder:menu:panel:menuSpei:panel:men'
        f'uConsultaOrdenes:panel:commonPanelBorder:enviadasPanel:histor'
        f'icosForm:btnBuscar:{client.interface}:IActivePageBehaviorList'
        f'ener:0:&wicket:ignoreIfNotActive=true&random=0.{random_gen()}',
        {
            'fechaInicialField:efDateTextField': start_date,
            'fechaFinalField:efDateTextField': final_date,
        },
    )

    # aux request
    client.get(
        f'?wicket:interface=:2:mainBorder:menu:panel:menuSpei:panel:men'
        f'uConsultaOrdenes:panel:commonPanelBorder:enviadasPanel:histor'
        f'icosForm:panelInferior:filter-form:dataTable:topToolbars:2:to'
        f'olbar:tableDataCell:exportTextLink:{client.interface}:IBehavi'
        f'orListener:0:-1&ramdom=0.{random_gen()}',
        increment_interface=False,
    )

    # Download request
    time.sleep(DELAY_REQUEST)
    response = client.get(
        f'?wicket:interface=:2:mainBorder:menu:panel:menuSpei:panel:men'
        f'uConsultaOrdenes:panel:commonPanelBorder:enviadasPanel:histor'
        f'icosForm:panelInferior:filter-form:dataTable:topToolbars:2:to'
        f'olbar:tableDataCell:hiddenExportTextLink:'
        f'{client.interface}:ILinkListener::'
    )

    verify_response(response)

    transactions = response
    if not to:
        client.post(
            f'?wicket:interface=:2:mainBorder:menu:panel:menuSpei:panel:men'
            f'uConsultaOrdenes:panel:commonPanelBorder:enviadasPanel:histor'
            f'icosForm:btnBuscar:{client.interface}:IActivePageBehaviorList'
            f'ener:0:&wicket:ignoreIfNotActive=true&random=0.{random_gen()}',
            dict(historicoActualBox='on'),
        )

        client.get(
            f'?wicket:interface=:2:mainBorder:menu:panel:menuSpei:panel:men'
            f'uConsultaOrdenes:panel:commonPanelBorder:enviadasPanel:histor'
            f'icosForm:panelInferior:filter-form:dataTable:topToolbars:2:to'
            f'olbar:tableDataCell:exportTextLink:{client.interface}:IBehavi'
            f'orListener:0:-1&ramdom=0.{random_gen()}',
            increment_interface=False,
        )

        time.sleep(DELAY_REQUEST)
        response = client.get(
            f'?wicket:interface=:2:mainBorder:menu:panel:menuSpei:panel:men'
            f'uConsultaOrdenes:panel:commonPanelBorder:enviadasPanel:histor'
            f'icosForm:panelInferior:filter-form:dataTable:topToolbars:2:to'
            f'olbar:tableDataCell:hiddenExportTextLink:'
            f'{client.interface}:ILinkListener::'
        )

        verify_response(response)

        transactions += remove_header(response)

    # Received Orders
    client.get(
        f'?wicket:interface=:2:mainBorder:menu:panel:menuSpei:panel:men'
        f'uConsultaOrdenes:tabs-container:tabs:2:link:{client.interface}'
        f':ILinkListener::'
    )

    # Setting dates
    client.post(
        f'?wicket:interface=:2:mainBorder:menu:panel:menuSpei:panel:menu'
        f'ConsultaOrdenes:panel:commonPanelBorder:recibidasPanel:histori'
        f'cosForm:btnBuscar:{client.interface}:IActivePageBehaviorListen'
        f'er:0:&wicket:ignoreIfNotActive=true&random=0.{random_gen()}',
        {
            'fechaInicialField:efDateTextField': start_date,
            'fechaFinalField:efDateTextField': final_date,
        },
    )

    client.get(
        f'?wicket:interface=:2:mainBorder:menu:panel:menuSpei:panel:men'
        f'uConsultaOrdenes:panel:commonPanelBorder:recibidasPanel:histo'
        f'ricosForm:panelInferior:filter-form:dataTable:topToolbars:2:t'
        f'oolbar:tableDataCell:exportTextLink:{client.interface}:IBehav'
        f'iorListener:0:-1&random=0.{random_gen()}',
        increment_interface=False,
    )

    # Download request
    time.sleep(DELAY_REQUEST)
    response = client.get(
        f'?wicket:interface=:2:mainBorder:menu:panel:menuSpei:panel:men'
        f'uConsultaOrdenes:panel:commonPanelBorder:recibidasPanel:histo'
        f'ricosForm:panelInferior:filter-form:dataTable:topToolbars:2:t'
        f'oolbar:tableDataCell:hiddenExportTextLink:{client.interface}:'
        f'ILinkListener::'
    )

    verify_response(response)

    transactions += remove_header(response)

    if not to:
        client.post(
            f'?wicket:interface=:2:mainBorder:menu:panel:menuSpei:panel:men'
            f'uConsultaOrdenes:panel:commonPanelBorder:recibidasPanel:histor'
            f'icosForm:btnBuscar:{client.interface}:IActivePageBehaviorList'
            f'ener:0:&wicket:ignoreIfNotActive=true&random=0.{random_gen()}',
            dict(historicoActualBox='on'),
        )

        client.get(
            f'?wicket:interface=:2:mainBorder:menu:panel:menuSpei:panel:men'
            f'uConsultaOrdenes:panel:commonPanelBorder:recibidasPanel:histor'
            f'icosForm:panelInferior:filter-form:dataTable:topToolbars:2:to'
            f'olbar:tableDataCell:exportTextLink:{client.interface}:IBehavi'
            f'orListener:0:-1&ramdom=0.{random_gen()}',
            increment_interface=False,
        )

        time.sleep(DELAY_REQUEST)
        response = client.get(
            f'?wicket:interface=:2:mainBorder:menu:panel:menuSpei:panel:men'
            f'uConsultaOrdenes:panel:commonPanelBorder:recibidasPanel:histor'
            f'icosForm:panelInferior:filter-form:dataTable:topToolbars:2:to'
            f'olbar:tableDataCell:hiddenExportTextLink:'
            f'{client.interface}:ILinkListener::'
        )

        verify_response(response)

        transactions += remove_header(response)

    # Upload to S3
    s3 = boto3.resource('s3')
    s3.meta.client.put_object(
        Body=transactions, Bucket=os.environ['S3_BUCKET'], Key=DEST_FILE_S3
    )
