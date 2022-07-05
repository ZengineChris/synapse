# Copyright 2022 The Matrix.org Foundation C.I.C.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Extra, StrictStr, constr, validator

from synapse.util.threepids import validate_email


class AuthenticationData(BaseModel):
    class Config:
        extra = Extra.allow

    session: Optional[StrictStr] = None
    type: Optional[StrictStr] = None


class EmailRequestTokenBody(BaseModel):
    if TYPE_CHECKING:
        client_secret: str
    else:
        # See also assert_valid_client_secret()
        client_secret: constr(
            regex="[0-9a-zA-Z.=_-]", min_length=0, max_length=255  # noqa: F722
        )
    email: str
    id_access_token: Optional[str]
    id_server: Optional[str]
    next_link: Optional[str]
    send_attempt: int

    # Canonicalise the email address. The addresses are all stored canonicalised
    # in the database. This allows the user to reset his password without having to
    # know the exact spelling (eg. upper and lower case) of address in the database.
    # Without this, an email stored in the database as "foo@bar.com" would cause
    # user requests for "FOO@bar.com" to raise a Not Found error.
    _email_validator = validator("email", allow_reuse=True)(validate_email)
