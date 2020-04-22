with import ./default.nix;
{ config, pkgs, nodes, ... }:
{ deployment.targetHost = "136.244.105.227";
  environment.systemPackages = [
    interpreter
  ];
}