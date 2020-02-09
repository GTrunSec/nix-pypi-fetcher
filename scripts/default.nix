with import <nixpkgs> {};
rec {
  python = python37;
  ujson = python.pkgs.buildPythonPackage {
    name = "ujson-1.35";
    src = pkgs.fetchurl {
      url = "https://files.pythonhosted.org/packages/16/c4/79f3409bc710559015464e5f49b9879430d8f87498ecdc335899732e5377/ujson-1.35.tar.gz";
      sha256 = "f66073e5506e91d204ab0c614a148d5aa938bdbf104751be66f8ad7a222f5f86";
    };
    doCheck = false;
    format = "setuptools";
    meta = with pkgs.stdenv.lib; {
      homepage = "http://www.esn.me";
      license = licenses.bsdOriginal;
      description = "Ultra fast JSON encoder and decoder for Python";
    };
  };
  interpreter = python.withPackages (ps: with ps; [
    requests
    peewee
    ujson
  ]);
}
