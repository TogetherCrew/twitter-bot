import logging

import numpy as np
from bot.utils.mongo_connection import get_saga_db_location
from bot.utils.rabbitmq_connection import prepare_rabbit_mq, get_rabbit_mq_credentials
from tc_messageBroker.rabbit_mq.saga.saga_base import Status, get_saga


def get_saga_instance(sagaId: str, connection: str, saga_db: str, saga_collection: str):
    saga = get_saga(
        sagaId=sagaId,
        connection_url=connection,
        db_name=saga_db,
        collection=saga_collection,
    )
    return saga


def sort_transactions(transactions: list):
    """
    sort transactions by their order and status
    the NOT_STARTED ones would be at the first of the list
    and they are ordered by `order` property

    Parameters:
    ------------
    transactions : list[ITransaction]
        the list of transactions to order

    Returns:
    ---------
    transactions_ordered : ndarray(ITransaction)
        the transactions ordered by status
        the `NOT_STARTED` ones are the firsts
        it is actually a numpy array for us to be able to
            change the properties in deep memory
    tx_not_started_count : int
        the not started transactions count
    """
    tx_not_started = []
    tx_other = []

    for tx in transactions:
        if tx.status == Status.NOT_STARTED:
            tx_not_started.append(tx)
        else:
            tx_other.append(tx)

    tx_not_started_count = len(tx_not_started)
    tx_not_started_sorted = sort_transactions_orderly(tx_not_started)

    transactions_ordered = list(tx_not_started_sorted)
    transactions_ordered.extend(tx_other)

    return np.array(transactions_ordered), tx_not_started_count


def publish_on_success(connection, result, *args, **kwargs):
    # we must get these three things
    logging.info(f"args in on_success callback: {args}")
    try:
        sagaId = args[0][0]
        mongo_creds = get_saga_db_location()
        rabbit_creds = get_rabbit_mq_credentials()
        logging.info(f"SAGAID: {sagaId}: ON_SUCCESS callback! ")

        saga = get_saga_instance(
            sagaId=sagaId,
            connection=mongo_creds["connection_str"],
            saga_db=mongo_creds["db_name"],
            saga_collection=mongo_creds["collection_name"],
        )
        rabbitmq = prepare_rabbit_mq(rabbit_creds)

        transactions = saga.choreography.transactions

        (transactions_ordered, tx_not_started_count) = sort_transactions(transactions)

        if tx_not_started_count != 0:
            guildId = saga.data["guildId"]
            tx = transactions_ordered[0]

            logging.info(f"GUILDID: {guildId}: Publishing for {tx.queue}")

            rabbitmq.connect(tx.queue)
            rabbitmq.publish(
                queue_name=tx.queue,
                event=tx.event,
                content={"uuid": sagaId, "data": saga.data},
            )
    except Exception as exp:
        logging.info(f"Exception occured in job on_success callback: {exp}")


def sort_transactions_orderly(transactions: list):
    """
    sort transactions by their `order` property

    Parameters:
    ------------
    transactions : list[ITransaction]
        the list of transactions to order

    Returns:
    ---------
    transactions_orderly_sorted : list[ITransaction]
        transactions sorted by their order
    """
    orders = [tx.order for tx in transactions]
    sorted_indices = np.argsort(orders)

    return np.array(transactions)[sorted_indices]
