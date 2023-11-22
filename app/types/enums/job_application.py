from enum import StrEnum


class JobApplicationStatus(StrEnum):
    saved = "saved"
    applied = "applied"
    in_process = "in_process"
    rejected = "rejected"
    offer_rejected = "offer_rejected"
    offer_accepted = "offer_accepted"
    offer_received = "offer_received"
    closed = "closed"
    withdrawn = "withdrawn"
