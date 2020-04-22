with import <nixpkgs> {};
pkg: version:
  let
    pkg_name = (lib.replaceStrings ["_"] ["-"] (lib.toLower pkg));
    hash = builtins.hashString "sha256" pkg_name;
    bucket =
        builtins.elemAt (lib.stringToCharacters hash) 0
        + builtins.elemAt (lib.stringToCharacters hash) 1;
    pypi-sources = builtins.fromJSON (builtins.readFile (./pypi + "/${bucket}.json"));
  in
  pkgs.fetchurl {
    url = "https://files.pythonhosted.org/packages/" + pypi-sources."${pkg_name}"."${version}"."url";
    sha256 = pypi-sources."${pkg_name}"."${version}"."sha256";
}
