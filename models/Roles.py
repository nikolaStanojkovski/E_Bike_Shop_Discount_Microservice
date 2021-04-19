from app import db
import enum


class Role(enum.Enum):
    InventoryMS = 1
    PaymentsMS = 2
    Administrator = 3