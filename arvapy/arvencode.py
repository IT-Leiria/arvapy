from pathlib import Path
from os.path import expanduser  # This is needed to swap "~" for $HOME in strings


class ArvApyEncode:
    def __init__(self):
        # DEBUG -- PATH MUST BY DYNAMICALLY SET
        self.cfg_search_path = "~/Repos/vtm_360lib"

    def GetAvailableConfigFiles(self):
        cfg_files = [path for path in Path(expanduser(self.cfg_search_path)).rglob("*.cfg")]
        return cfg_files


# FOR SELF CONTAINED DEBUG ONLY!! TO BE ERASED IN FINAL VERSION
if __name__ == "__main__":
    encode_proc = ArvApyEncode()

    print(encode_proc.cfg_search_path)
    print(encode_proc.GetAvailableConfigFiles())
