let
    pkgs = import <nixpkgs> {};
    stdenv = pkgs.stdenv;
 in rec {
     djroombaEnv = pkgs.myEnvFun {
       name = "djroomba-env";
       buildInputs = with pkgs; [
            git
            python34
            (import ./djroombaPkg.nix) 
       ];
     };
}
