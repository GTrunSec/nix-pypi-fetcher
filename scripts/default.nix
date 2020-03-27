with import <nixpkgs> {};
rec {
  python = python37;
  interpreter = python.withPackages (ps: with ps; [
    requests
    peewee
  ]);
}
