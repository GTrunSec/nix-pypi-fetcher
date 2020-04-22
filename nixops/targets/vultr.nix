{
  machine =
  { config, pkgs, nodes, ... }:
  {
    imports = [
      <nixpkgs/nixos/modules/profiles/qemu-guest.nix>
      ../configuration.nix
    ];
    boot.loader.grub.device = "/dev/vda";
    fileSystems."/" = { device = "/dev/vda1"; fsType = "ext4"; };
    boot.cleanTmpDir = true;
    networking.firewall.allowPing = true;
    services.openssh.enable = true;
    users.users.root.openssh.authorizedKeys.keys = [
      "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDuhpzDHBPvn8nv8RH1MRomDOaXyP4GziQm7r3MZ1Syk"
    ];
  };
}
