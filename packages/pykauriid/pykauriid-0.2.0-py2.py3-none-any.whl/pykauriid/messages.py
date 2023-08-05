# -*- coding: utf-8 -*-
"""Messages exchanged between participating parties."""

# Created: 2018-09-21 Guy K. Kloss <guy@mysinglesource.io>
#
# (c) 2018-2019 by SingleSource Limited, Auckland, New Zealand
#     http://mysinglesource.io/
#     Apache 2.0 Licence.
#
# This work is licensed under the Apache 2.0 open source licence.
# Terms and conditions apply.
#
# You should have received a copy of the licence along with this
# program.

__author__ = 'Guy K. Kloss <guy@mysinglesource.io>'

from typing import Dict, Union

import pykauriid
from sspyjose.jwe import Jwe
from sspyjose.jwk import Jwk


class Message:
    """Base class for messages to exchange between parties."""

    message_type = None  # type: str
    """Type of message."""
    _message = None  # type: Dict
    """Plain text message content in raw."""

    def __init__(self, message_type: str, *, message: Dict = None):
        """
        Constructor.

        :param message_type: Type of message.
        """
        self.message_type = message_type
        if message:
            self._message = message

    def serialise(self, recipient_dh_pk: Union[Jwk, str, Dict]) -> str:
        """
        Serialise the message object.

        :param recipient_dh_pk: Public encryption key of rhe recipient.
        :return: JSON serialised data structure.
        """
        raise NotImplementedError('Needs to be implemented by child class.')

    @classmethod
    def deserialise(cls, message: Union[str, bytes],
                    recipient_dh_sk: Union[Jwk, str, Dict]) -> 'Message':
        """
        Deserialise a message, and returns a `Message` (sub-) class object.

        :param message: The message to deserialise.
        :param recipient_dh_sk: Secret/private DH key of the recipient.
        :return: A plain text message object.
        """
        if isinstance(recipient_dh_sk, dict):
            recipient_dh_sk = Jwk.get_instance(
                crv='X25519', from_dict=recipient_dh_sk)
        elif isinstance(recipient_dh_sk, str):
            recipient_dh_sk = Jwk.get_instance(
                crv='X25519', from_json=recipient_dh_sk)
        decrypter = Jwe.get_instance(alg='ECDH-ES', jwk=recipient_dh_sk)
        decrypter.load_compact(message)
        recovered = decrypter.decrypt()
        message_type = recovered['message_type']
        if message_type in MESSAGE_TYPES:
            klass = MESSAGE_TYPES[message_type]
            return klass(message=recovered)
        else:
            return cls(message_type, message=recovered)


class AttestationRequest(Message):
    """Request for attestation of a claim set."""

    claim_set_keys = None  # type: pykauriid.claims.ClaimSetKeys
    """
    Keys to the claim set to attest (includes claim set of a reference to it).
    """
    ancestors = None  # type: Dict[str, str]
    """
    Ancestor entities in the attestation trail. The key of the dictionary
    is the IPFS references, and the value contains the internal attestation
    entity ID from the attestation PROV graph. The new attestation to be
    generated will link up with these entities.
    """

    def __init__(self, *,
                 claim_set_keys: Dict = None,
                 message: Dict = None,
                 ancestors: Dict[str, str] = None):
        """
        Constructor.

        :param claim_set_keys: Cryptographic keys to the serialised/encrypted
            claim set for the attestation request.
        :param message: Plain text message to use for initialising the
            content.
        :param ancestors: Ancestor entities in the attestation trail. The
            key of the dictionary is the IPFS reference, and the value
            contains the internal attestation entity ID from the attestation
            PROV graph. The new attestation to be generated will link up
            with these entities.
        """
        super().__init__('attestation_request')
        if claim_set_keys:
            self.claim_set_keys = claim_set_keys
        if message:
            self.claim_set_keys = message['claim_set_keys']
        if ancestors:
            self.ancestors = ancestors

    def serialise(self, recipient_dh_pk: Union[Jwk, str, Dict]) -> str:
        """
        Serialise the attestation request object.

        :param recipient_dh_pk: Public encryption key of the recipient.
        :return: JWE encrypted JSON serialised data structure.
        """
        content = {
            'message_type': self.message_type,
            'claim_set_keys': self.claim_set_keys
        }
        self._message = content
        if isinstance(recipient_dh_pk, dict):
            recipient_dh_pk = Jwk.get_instance(crv='X25519',
                                               from_dict=recipient_dh_pk)
        elif isinstance(recipient_dh_pk, str):
            recipient_dh_pk = Jwk.get_instance(crv='X25519',
                                               from_json=recipient_dh_pk)
        encrypter = Jwe.get_instance(alg='ECDH-ES', jwk=recipient_dh_pk)
        encrypter.message = content
        encrypter.encrypt()
        return encrypter.serialise()


class AttestationResponse(Message):
    """Response with attestation of a claim set."""

    claim_set_keys = None  # type: pykauriid.claims.ClaimSetKeys
    """
    Keys to the claim set attested (includes claim set of a reference to it).
    """
    attestation = None  # type: str
    """
    Issued serialised attestation of the claim set.
    """

    def __init__(self, *,
                 claim_set_keys: Dict = None,
                 message: Dict = None,
                 attestation: str = None):
        """
        Constructor.

        :param claim_set_keys: Cryptographic keys to the serialised/encrypted
            claim set attested.
        :param message: Plain text message to use for initialising the
            content.
        :param attestation: Encrypted/serialised attestation object to send.
        """
        super().__init__('attestation_response')
        if claim_set_keys:
            self.claim_set_keys = claim_set_keys
        if message:
            self.claim_set_keys = message['claim_set_keys']
        if attestation:
            self.attestation = attestation

    def serialise(self, recipient_dh_pk: Union[Jwk, str, Dict]) -> str:
        """
        Serialise the attestation response object.

        :param recipient_dh_pk: Public encryption key of the recipient.
        :return: JWE encrypted JSON serialised data structure.
        """
        content = {
            'message_type': self.message_type,
            'claim_set_keys': self.claim_set_keys,
            'attestation': self.attestation
        }
        self._message = content
        if isinstance(recipient_dh_pk, dict):
            recipient_dh_pk = Jwk.get_instance(crv='X25519',
                                               from_dict=recipient_dh_pk)
        elif isinstance(recipient_dh_pk, str):
            recipient_dh_pk = Jwk.get_instance(crv='X25519',
                                               from_json=recipient_dh_pk)
        encrypter = Jwe.get_instance(alg='ECDH-ES', jwk=recipient_dh_pk)
        encrypter.message = content
        encrypter.encrypt()
        return encrypter.serialise()


MESSAGE_TYPES = {
    None: Message,
    'attestation_request': AttestationRequest,
    'attestation_response': AttestationResponse
}
