{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  shellHook = ''
    export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc
    ]}
  '';

  buildInputs = [
    pkgs.python313
    pkgs.nodePackages_latest.nodejs
  ];
}
