from enum import Enum


class JobApplicationStatus(Enum):
    saved = "saved"
    applied = "applied"
    rejected = "rejected"
    in_process = "in_process"
    offer_rejected = "offer_rejected"
    offer_accepted = "offer_accepted"
    closed = "closed"
    withdrawn = "withdrawn"
