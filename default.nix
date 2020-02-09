with import <nixpkgs> {};
pkg: version:
  let
    hash = builtins.hashString "sha256" pkg;
    bucket =
        builtins.elemAt (lib.stringToCharacters hash) 0
        + builtins.elemAt (lib.stringToCharacters hash) 1;
    pypi-sources = import (./pypi + "/${bucket}.nix");
  in
  pkgs.fetchurl {
    url = pypi-sources."${pkg}"."${version}"."url";
    sha256 = pypi-sources."${pkg}"."${version}"."sha256";
}
