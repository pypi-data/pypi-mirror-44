from .misc import misc
from .exceptions import alttprException

import hashlib
import aiofiles

class romfile:
    async def read(srcfilepath, verify_checksum=True):
        """Reads a ROM and converts it to a list of bytes, preparing it for patching.
        
        Arguments:
            srcfilepath {str} -- A path (either relative or absolute) to a file on the filesystem to be read.
            verify_checksum {bool} -- Verify the checksum of the file to ensure it is an unheadered ALTTPR Japan 1.0 ROM.
        
        Raises:
            alttprException -- Returns if the sha256 checksum does not match a ALTTPR Japan 1.0 ROM.
        
        Returns:
            list -- A list of bytes depicting the read ROM file.
        """
        if verify_checksum:
            expected_rom_sha256='794e040b02c7591b59ad8843b51e7c619b88f87cddc6083a8e7a4027b96a2271'
            sha256_hash = hashlib.sha256()
            with open(srcfilepath,"rb") as f:
                for byte_block in iter(lambda: f.read(4096),b""):
                    sha256_hash.update(byte_block)
            if not sha256_hash.hexdigest() == expected_rom_sha256:
                raise alttprException('Expected checksum "{expected_rom_sha256}", got "{actual_checksum}" instead.  Verify the source ROM is an unheadered Japan 1.0 Link to the Past ROM.'.format(
                    expected_rom_sha256=expected_rom_sha256,
                    actual_checksum=sha256_hash.hexdigest()
                ))
        fr = await aiofiles.open(srcfilepath,"rb")
        baserom_array = list(await fr.read())
        await fr.close()
        return baserom_array

    async def write(rom, dstfilepath):
        fw = await aiofiles.open(dstfilepath,"wb")
        patchrom = bytes()
        for idx, chunk_array in enumerate(misc.chunk(rom,256)):
            patchrom += bytes(chunk_array)
        await fw.write(patchrom)
        fw.close

