import random
import uuid
from datetime import datetime, timedelta

from faker import Faker

fake = Faker()
EVENT_TYPES = ["user_created", "product_viewed", "order_created", "payment_completed"]
SOURCES = ["web", "mobile", "api"]
PAYMENT_METHODS = ["credit_card", "paypal", "bank_transfer"]


class EventState:
    def __init__(self):
        self.user_ids = []
        self.product_ids = []
        self.orders = {}

    def _new_user_id(self):
        user_id = fake.uuid4()
        self.user_ids.append(user_id)
        return user_id

    def get_or_create_user_id(self):
        if self.user_ids and random.random() < 0.9:
            return random.choice(self.user_ids)
        return self._new_user_id()

    def get_or_create_product_id(self):
        if self.product_ids and random.random() < 0.85:
            return random.choice(self.product_ids)
        product_id = fake.uuid4()
        self.product_ids.append(product_id)
        return product_id

    def create_order(self, user_id, total_amount):
        order_id = fake.uuid4()
        self.orders[order_id] = {
            "user_id": user_id,
            "total_amount": total_amount,
            "paid": False,
        }
        return order_id

    def get_unpaid_order(self):
        unpaid_orders = [order_id for order_id, order in self.orders.items() if not order["paid"]]
        if not unpaid_orders:
            return None, None
        order_id = random.choice(unpaid_orders)
        return order_id, self.orders[order_id]


STATE = EventState()


def _user_created_payload(state):
    return {
        "user_id": state._new_user_id(),
        "email": fake.email(),
        "name": fake.name(),
    }


def _product_viewed_payload(state):
    return {
        "user_id": state.get_or_create_user_id(),
        "product_id": state.get_or_create_product_id(),
        "category": fake.word(),
    }


def _order_created_payload(state):
    user_id = state.get_or_create_user_id()
    total_amount = round(random.uniform(10.0, 500.0), 2)
    order_id = state.create_order(user_id=user_id, total_amount=total_amount)

    return {
        "user_id": user_id,
        "order_id": order_id,
        "total_amount": total_amount,
    }


def _payment_completed_payload(state):
    order_id, order = state.get_unpaid_order()
    if order is None:
        user_id = state.get_or_create_user_id()
        amount = round(random.uniform(10.0, 500.0), 2)
        order_id = state.create_order(user_id=user_id, total_amount=amount)
        order = state.orders[order_id]

    order["paid"] = True

    return {
        "user_id": order["user_id"],
        "order_id": order_id,
        "payment_method": random.choice(PAYMENT_METHODS),
        "amount": order["total_amount"],
    }


PAYLOAD_BUILDERS = {
    "user_created": _user_created_payload,
    "product_viewed": _product_viewed_payload,
    "order_created": _order_created_payload,
    "payment_completed": _payment_completed_payload,
}


def build_payload(event_type, state=STATE):
    payload_builder = PAYLOAD_BUILDERS.get(event_type)
    if payload_builder is None:
        raise ValueError(f"Unsupported event_type: {event_type}")
    return payload_builder(state)


def build_event(state=STATE):
    event_type = random.choice(EVENT_TYPES)
    now = datetime.now().isoformat()
    now_ingestion = datetime.now()
    ingestion_time = now_ingestion + timedelta(seconds=random.randint(0, 30))

    return {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "source": random.choice(SOURCES),
        "event_timestamp": now,
        "ingestion_timestamp": ingestion_time.isoformat(),
        "payload": build_payload(event_type, state=state),
    }
