import asyncio
import asyncssh
from enum import IntEnum
from time import sleep


class SSHFilexferTypeEnum(IntEnum):
    """Enum for the SFTP protocol file type.

    SFTPv4+ types:
        * 1: SSH_FILEXFER_TYPE_REGULAR
        * 2: SSH_FILEXFER_TYPE_DIRECTORY
        * 3: SSH_FILEXFER_TYPE_SYMLINK
        * 4: SSH_FILEXFER_TYPE_SPECIAL
        * 5: SSH_FILEXFER_TYPE_UNKNOWN

    Sources:
        * https://asyncssh.readthedocs.io/en/latest/api.html#asyncssh.SFTPAttrs
        * https://datatracker.ietf.org/doc/html/draft-ietf-secsh-filexfer-04#section-5.2
    """

    REGULAR = 1
    DIRECTORY = 2
    SYMLINK = 3
    SPECIAL = 4
    UNKNOWN = 5


async def connect():
    async with asyncssh.connect(
        host="mockssh",
        options=asyncssh.SSHClientConnectionOptions(
            username="mountuser",
            password="Passw0rd!",
            known_hosts=None,
            encoding=None,
        ),
    ) as connection:
        async with connection.start_sftp_client() as sftp:
            sftp_names = await sftp.readdir("/data")
            filenames = sorted(
                name.filename
                for name in sftp_names
                if name.attrs.type != SSHFilexferTypeEnum.DIRECTORY
                and name.filename not in [".", ".."]
            )
            print(filenames)


if __name__ == "__main__":
    sleep(5)
    asyncio.run(connect())